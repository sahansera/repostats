# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-12-25

### Added
- Terminal User Interface (TUI) for interactive repository exploration
- `repostats-tui` command for launching the TUI
- Optional `[tui]` installation extra for TUI dependencies (textual framework)
- Rich formatting with colors and organized sections in TUI
- Keyboard shortcuts in TUI (r: refresh, q: quit)
- Real-time repository input validation in TUI
- Auto-fetch stats when TUI launched with repository argument

### Changed
- Restructured as a dual-interface tool (CLI + TUI)
- Core `GitHubClient` remains library-friendly for reuse
- Updated README with TUI installation and usage examples
- Enhanced feature list to highlight both interfaces

## [1.2.0] - 2025-12-21

### Added
- Support for multiple repositories in a single command
- `--output` / `-o` flag to save results to a file
- Additional repository metrics: license, size, default branch, open PRs, latest release
- `make check` command that automatically formats code before running checks
- Comprehensive error messages for rate limits with reset time
- Specific error message for 404 (repository not found)
- README badges for PyPI, tests, Python version, and license
- CONTRIBUTING.md with complete development guidelines

### Changed
- CLI now accepts multiple repository arguments
- Text output conditionally displays fields based on availability
- Repository size automatically converted to MB when appropriate
- Improved test coverage with new test cases for multi-repo and file output

### Fixed
- Code formatting issues in CI
- Type checking errors with mypy
- Import order with isort

## [1.1.0] - 2025-12-21

### Added
- Makefile for common development tasks (test, format, lint, type-check, build, release)
- Automated release workflow with GitHub Actions
- CHANGELOG.md to track version history
- Multiple output formats: text (default), JSON (`--format json`), YAML (`--format yaml`)

### Changed
- Renamed project from `githubstats` to `repostats`
- Improved package structure with flat module layout under `src/`
- Updated CI to use GitHub-hosted runners
- Fixed mypy type checking errors and updated to Python 3.9+

### Fixed
- Type annotations for better mypy compatibility
- Import structure for flat module layout

## [0.1.0] - 2025-07-06

### Added
- Initial release of repostats CLI tool
- Fetch GitHub repository statistics (stars, forks, issues, watchers, language)
- Support for GitHub API token authentication via `--token` flag or `GITHUB_TOKEN` env var
- Helpful error messages and proper exit codes for scripting
- User-Agent header with version tracking
- Development tooling: pytest suite, black/isort formatting, mypy type checking

[Unreleased]: https://github.com/sahansera/repostats/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/sahansera/repostats/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/sahansera/repostats/compare/v0.1.0...v1.1.0
[0.1.0]: https://github.com/sahansera/repostats/releases/tag/v0.1.0
