# ⚡️ repostats

[![PyPI version](https://badge.fury.io/py/repostats.svg)](https://pypi.org/project/repostats/)
[![Tests](https://github.com/sahansera/repostats/workflows/Python%20CI/badge.svg)](https://github.com/sahansera/repostats/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to fetch GitHub repository statistics.

## Installation

```bash
pip install repostats
```

## Usage

```bash
# Basic usage
repostats python/cpython

# With GitHub token for higher rate limits
export GITHUB_TOKEN=your_token_here
repostats python/cpython

# Or pass token directly
repostats python/cpython --token your_token_here

# Output as JSON
repostats python/cpython --format json

# Output as YAML
repostats python/cpython --format yaml
```

### Example output

**Text format (default):**
```text
python/cpython statistics
-------------------------
Stars       : 58,000
Forks       : 29,000
Open issues : 992
Watchers    : 3,400
Language    : Python
Created     : 2007-02-20T00:00:00Z
Updated     : 2024-01-15T12:34:56Z
```

**JSON format:**
```json
{
  "name": "python/cpython",
  "stars": 58000,
  "forks": 29000,
  "open_issues": 992,
  "watchers": 3400,
  "language": "Python",
  "created_at": "2007-02-20T00:00:00Z",
  "updated_at": "2024-01-15T12:34:56Z"
}
```

**YAML format:**
```yaml
name: python/cpython
stars: 58000
forks: 29000
open_issues: 992
watchers: 3400
language: Python
created_at: '2007-02-20T00:00:00Z'
updated_at: '2024-01-15T12:34:56Z'
```

The command exits with code `1` when the GitHub API request fails (for example, when the repository is missing or you hit a rate limit), which makes it easy to integrate into scripts.

## Features

- Fetch repository statistics including stars, forks, issues, and more
- Multiple output formats: text (default), JSON, and YAML
- Support for GitHub API token authentication
- Clean, accessible output that works well in plain-text terminals
- Helpful error messages and non-zero exit codes on failure
- Cross-platform compatibility

## Development

```bash
# Clone the repository
git clone https://github.com/sahansera/repostats.git
cd repostats

# Create virtual environment
uv venv
source .venv/bin/activate

# Install in development mode
make install-dev

# Run tests
make test

# Format code
make format

# Type checking
make type-check

# See all available commands
make help
```

## License

MIT
