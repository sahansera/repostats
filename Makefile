.PHONY: help install install-dev test format lint type-check clean build run

VENV = .venv/bin

help:
	@echo "Available commands:"
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install package with dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run linters"
	@echo "  make type-check   - Run mypy type checking"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make build        - Build distribution packages"
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

run:
	$(VENV)/repostats $(ARGS)
