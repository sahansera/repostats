# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of repostats CLI tool
- Fetch GitHub repository statistics (stars, forks, issues, watchers, language)
- Support for GitHub API token authentication via `--token` flag or `GITHUB_TOKEN` env var
- Multiple output formats: text (default), JSON (`--format json`), YAML (`--format yaml`)
- Helpful error messages and proper exit codes for scripting
- User-Agent header with version tracking
- Development tooling: Makefile, pytest suite, black/isort formatting, mypy type checking

## [0.1.0] - TBD

### Added
- Initial release

[Unreleased]: https://github.com/sahansera/repostats/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sahansera/repostats/releases/tag/v0.1.0
