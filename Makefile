# Makefile for linting, formatting, and type-checking with Poetry

# Directories to check, update with your source directories
SRC=BrowserPOM

# Default target
.PHONY: all
all: format lint type-check test

# Format the code using black and isort
.PHONY: format
format:
	@echo "Running code formatters..."
	poetry run black $(SRC)
	poetry run isort $(SRC)

# Lint the code using flake8 and pylint
.PHONY: lint
lint:
	@echo "Running linters..."
	poetry run flake8 $(SRC)
	poetry run pylint $(SRC)

# Type-check the code using mypy
.PHONY: type-check
type-check:
	@echo "Running type checks..."
	poetry run mypy $(SRC)

# Run all checks without modifying files
.PHONY: check
check:
	@echo "Running all checks (no formatting)..."
	poetry run flake8 $(SRC)
	poetry run pylint $(SRC)
	poetry run mypy $(SRC)

# Run test coverage (optional, update with your test command)
.PHONY: coverage
coverage:
	@echo "Running test coverage..."
	poetry run coverage run -m pytest $(SRC)
	poetry run coverage report

# Clean temporary and cache files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type d -name .mypy_cache -exec rm -r {} +
	find . -type f -name .coverage -delete

# Run tests
.PHONY: test
test:
	@echo "Running tests..."#
	poetry run pytest

# Display help message
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all         - Run format, lint, and type-check targets"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Run linters (flake8 and pylint)"
	@echo "  type-check  - Run type checks with mypy"
	@echo "  check       - Run all checks without formatting"
	@echo "  coverage    - Run test coverage"
	@echo "  test        - Run all tests"
	@echo "  clean       - Remove temporary and cache files"
