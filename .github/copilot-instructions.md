# Copilot Instructions for repostats

## Project Overview

**repostats** is a Python CLI tool that fetches GitHub repository statistics via the GitHub REST API. The codebase is small and focused:
- **Entry point**: `repostats` command → `repostats.cli:main()`
- **Architecture**: Two-layer design:
  - [cli.py](../src/repostats/cli.py) - Click-based CLI with output formatting (text/JSON/YAML)
  - [github.py](../src/repostats/github.py) - GitHub API client using `requests`

## Development Workflow

### Setup & Dependencies
```bash
# Use `uv` (modern Python package manager) - NOT pip for dev work
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Key Commands
- **Tests**: `pytest` (uses mocks, no real API calls)
- **Formatting**: `black . && isort .` (line-length: 88)
- **Type checking**: `mypy src` (Python 3.8+ compatible)
- **Run locally**: `repostats owner/repo` or `python -m repostats.cli owner/repo`

## Code Patterns & Conventions

### Error Handling Strategy
- **CLI layer**: Catch all exceptions, print user-friendly messages to stderr, exit with code 1
  - Example: Invalid repo format → "Repository should be in the format 'owner/repo'"
- **GitHub client**: Raise `RuntimeError` with detailed HTTP status/message from API response
  - Parse `response.json()["message"]` for GitHub error details
  - Include status code + reason in error messages (e.g., "404 Not Found: Repository not found")

### Output Formatting
- **Text (default)**: Human-readable with aligned labels, thousands separators (`:,`), blank lines for readability
- **JSON/YAML**: `--format json|yaml` outputs raw stats dict (keys: name, stars, forks, open_issues, watchers, created_at, updated_at, language)
- **YAML handling**: Optional dependency - gracefully fail with helpful message if PyYAML not installed

### Testing Approach
- **Mock everything**: Use `unittest.mock.patch` on `requests.get` and `GitHubClient`
- **Test exit codes**: Check `result.exit_code` (0 = success, 1 = failure)
- **Test stderr output**: Check `result.output` for error messages
- **Coverage areas**: Happy path, invalid inputs, HTTP errors, JSON parsing, all output formats
- **Mock location**: Patch at usage location (`repostats.cli.GitHubClient`, not `repostats.github.GitHubClient`)

### Type Hints & None Handling
- Use `Union[str, None]` or `Union[int, float]` (Python 3.8 compatible - no `|` syntax)
- API client expects nullable values (e.g., `language: str | None` → fallback to "Unknown")

## GitHub API Integration

### Authentication
- Token via `--token` flag OR `GITHUB_TOKEN` env var (Click's `envvar` feature)
- Unauthenticated requests have 60/hour rate limit
- **Headers**: Always set `User-Agent: repostats/{__version__}` and `Accept: application/vnd.github+json`

### Endpoint
- Single endpoint: `GET /repos/{owner}/{repo}` (https://api.github.com)
- **Timeout**: Default 10 seconds (configurable in `GitHubClient.__init__`)

### Rate Limit Handling
- **Current**: Fails with error message from API (roadmap: add retry/backoff logic)
- Helpful error messages guide users to authenticate for higher limits

## Roadmap Context

See [ROADMAP.md](../ROADMAP.md) for planned features:
- Multi-output formats stabilized (text/JSON/YAML) ✓
- **Next priorities**: Retry logic, batch repo lookups, integration tests with mocked API
- **Future**: Web dashboard/TUI, expose reusable Python API

## Common Pitfalls

1. **Exit codes**: Non-zero exit required for script integration - use `raise SystemExit(1)` after printing errors
2. **YAML dependency**: Optional in dependencies list but required for `--format yaml` - handle ImportError gracefully
3. **Type checking**: Target Python 3.8 - avoid modern type union syntax (`X | Y`)
4. **User-Agent header**: Always include version number from `__version__` for API tracking
