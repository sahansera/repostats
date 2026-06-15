from unittest.mock import MagicMock, patch

import pytest
import requests

from repostats import __version__
from repostats.github import GitHubClient


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {
        "full_name": "test/repo",
        "stargazers_count": 100,
        "forks_count": 50,
        "open_issues_count": 10,
        "subscribers_count": 25,
        "created_at": "2022-01-01T00:00:00Z",
        "updated_at": "2022-02-01T00:00:00Z",
        "language": "Python",
    }
    return mock


def test_get_repo_stats(mock_response):
    # Mock for latest release endpoint (returns 404 - no releases)
    release_mock = MagicMock()
    release_mock.status_code = 404

    with patch("requests.get", side_effect=[mock_response, release_mock]) as mock_get:
        client = GitHubClient()
        stats = client.get_repo_stats("test", "repo")

        # Should be called twice: once for repo, once for latest release
        assert mock_get.call_count == 2

        # Check first call (repo stats)
        first_call_args = mock_get.call_args_list[0]
        assert first_call_args[1]["timeout"] == 10
        assert first_call_args[1]["headers"]["User-Agent"] == f"repostats/{__version__}"
        assert first_call_args[1]["headers"]["Accept"] == "application/vnd.github+json"
        assert stats["name"] == "test/repo"
        assert stats["stars"] == 100
        assert stats["forks"] == 50
        # open_pull_requests field removed; open_issues holds actual open issue count
        assert stats["open_issues"] == 10
        assert "open_pull_requests" not in stats


def test_github_client_with_token():
    client = GitHubClient("test_token")
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "******"


def test_github_client_without_token():
    client = GitHubClient()
    assert "Authorization" not in client.headers
    assert client.headers["User-Agent"] == f"repostats/{__version__}"


def test_get_repo_stats_http_error(mock_response):
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.reason = "Not Found"
    error_response.headers = {}
    error_response.json.return_value = {"message": "Repository not found"}
    http_error = requests.HTTPError(response=error_response)

    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "missing")

    assert "not found" in str(exc.value).lower()
    assert "test/missing" in str(exc.value)


def test_get_repo_stats_invalid_json(mock_response):
    mock_response.json.side_effect = ValueError("no json")

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "repo")

    assert "invalid JSON" in str(exc.value)


def test_get_repo_stats_rate_limit(mock_response):
    """Test that a 403 with X-RateLimit-Remaining: 0 produces a helpful message."""
    error_response = MagicMock()
    error_response.status_code = 403
    error_response.reason = "Forbidden"
    error_response.headers = {
        "X-RateLimit-Remaining": "0",
        "X-RateLimit-Reset": "9999999999",
    }
    error_response.json.return_value = {"message": "API rate limit exceeded"}
    http_error = requests.HTTPError(response=error_response)

    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "repo")

    assert "rate limit" in str(exc.value).lower()
    assert "--token" in str(exc.value)
    assert "UTC" in str(exc.value)


def test_get_repo_stats_403_forbidden(mock_response):
    """Test that a 403 without rate-limit headers shows the API message."""
    error_response = MagicMock()
    error_response.status_code = 403
    error_response.reason = "Forbidden"
    error_response.headers = {}
    error_response.json.return_value = {"message": "Must have push access"}
    http_error = requests.HTTPError(response=error_response)

    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "private-repo")

    assert "403 Forbidden" in str(exc.value)
    assert "Must have push access" in str(exc.value)


def test_get_latest_release_success(mock_response):
    """Test _get_latest_release returns the tag name on success."""
    release_mock = MagicMock()
    release_mock.status_code = 200
    release_mock.raise_for_status.return_value = None
    release_mock.json.return_value = {"tag_name": "v2.0.0"}

    with patch("requests.get", side_effect=[mock_response, release_mock]):
        client = GitHubClient()
        stats = client.get_repo_stats("test", "repo")

    assert stats["latest_release"] == "v2.0.0"


def test_get_latest_release_none_when_no_releases(mock_response):
    """Test _get_latest_release returns None when no releases exist (404)."""
    release_mock = MagicMock()
    release_mock.status_code = 404

    with patch("requests.get", side_effect=[mock_response, release_mock]):
        client = GitHubClient()
        stats = client.get_repo_stats("test", "repo")

    assert stats["latest_release"] is None


def test_get_latest_release_none_on_error(mock_response):
    """Test _get_latest_release returns None when the release request fails."""
    release_mock = MagicMock()
    release_mock.status_code = 500
    release_mock.raise_for_status.side_effect = requests.RequestException(
        "server error"
    )

    with patch("requests.get", side_effect=[mock_response, release_mock]):
        client = GitHubClient()
        stats = client.get_repo_stats("test", "repo")

    assert stats["latest_release"] is None
