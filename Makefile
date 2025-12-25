.PHONY: help install install-dev test format lint type-check clean build run release check ci

VENV = .venv/bin

help:
	@echo "Available commands:"
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install package with dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run linters (check formatting without changing)"
	@echo "  make type-check   - Run mypy type checking"
	@echo "  make check        - Format code, then run all checks (lint + type-check + test)"
	@echo "  make ci           - Run CI checks locally (lint + type-check + test, no formatting)"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make release      - Build and publish to PyPI (requires VERSION=x.y.z)"
	@echo "  make run          - Run repostats (use ARGS='owner/repo' to pass arguments)"

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

test:
	$(VENV)/pytest

test-cov:
	$(VENV)/pytest --cov=src --cov-report=html --cov-report=term

format:
	$(VENV)/black .
	$(VENV)/isort .

lint:
	$(VENV)/black --check .
	$(VENV)/isort --check .

type-check:
	$(VENV)/mypy src

check: format lint type-check test
	@echo "✅ All checks passed!"

ci: lint type-check test
	@echo "✅ CI checks passed! Safe to push."

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	uv build

release: clean build
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make release VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "Building release $(VERSION)..."
	$(VENV)/python -m pip install --upgrade twine
	$(VENV)/python -m twine check dist/*
	@echo "Ready to publish version $(VERSION) to PyPI"
	@echo "Continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	$(VENV)/python -m twine upload dist/*
	git tag v$(VERSION)
	git push origin v$(VERSION)
	@echo "Released version $(VERSION)!"

run:
	$(VENV)/repostats $(ARGS)
