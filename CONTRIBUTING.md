# Contributing to repostats

Thank you for considering contributing to repostats! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Getting Started

```bash
# Clone the repository
git clone https://github.com/sahansera/repostats.git
cd repostats

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
make install-dev

# Run tests to verify setup
make test
```

## Development Workflow

### Making Changes

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following the code style guidelines below

3. **Run the test suite**:
   ```bash
   make test
   ```

4. **Format your code**:
   ```bash
   make format
   ```

5. **Check types**:
   ```bash
   make type-check
   ```

6. **Run linters**:
   ```bash
   make lint
   ```

### Code Style

- **Formatting**: We use [black](https://github.com/psf/black) with 88 character line length
- **Import sorting**: We use [isort](https://pycqa.github.io/isort/) with black profile
- **Type hints**: All functions should have type annotations
- **Type checking**: We use [mypy](http://mypy-lang.org/) for static type checking

Run `make format` before committing to automatically format your code.

### Testing

- Write tests for all new features and bug fixes
- Place tests in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Mock external API calls using `unittest.mock`
- Aim for high test coverage

Run tests with:
```bash
make test           # Run all tests
make test-cov       # Run with coverage report
```

### Commit Messages

Write clear, concise commit messages:

```
Add rate limit information to error messages

- Show remaining API calls in 403 responses
- Display rate limit reset time
- Suggest authentication when limit is exceeded

Fixes #123
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed explanation if needed
- Reference related issues

## Pull Request Process

1. **Update documentation** if you're adding or changing features
2. **Update CHANGELOG.md** under the `[Unreleased]` section
3. **Ensure all tests pass** and type checking succeeds
4. **Create a pull request** with a clear description of:
   - What changes you made
   - Why you made them
   - Any related issues

5. **Wait for review** - maintainers will review your PR and may request changes

## Project Structure

```
repostats/
├── src/                    # Source code
│   ├── __init__.py        # Package version
│   ├── cli.py             # Click CLI interface
│   └── github.py          # GitHub API client
├── tests/                 # Test files
│   ├── test_cli.py
│   └── test_github.py
├── .github/
│   └── workflows/         # CI/CD workflows
├── Makefile               # Development commands
├── pyproject.toml         # Project configuration
└── README.md              # User documentation
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, repostats version)
- **Error messages** or stack traces

### Feature Requests

When requesting features, please:

- **Explain the use case** - why is this feature needed?
- **Describe the proposed solution** - how should it work?
- **Consider alternatives** - are there other ways to solve this?
- **Check existing issues** - has this been discussed before?

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## Questions?

- Open an issue with the "question" label
- Check existing issues and discussions first

## Development Commands Reference

```bash
make help          # Show all available commands
make install       # Install package
make install-dev   # Install with dev dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make format        # Format code (black + isort)
make lint          # Check code formatting
make type-check    # Run mypy type checking
make clean         # Remove build artifacts
make build         # Build distribution packages
```

## License

By contributing to repostats, you agree that your contributions will be licensed under the MIT License.
