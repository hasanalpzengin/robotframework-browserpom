# Makefile for linting, formatting, and type-checking with Poetry

# Directories to check, update with your source directories
SRC=BrowserPOM

.PHONY: format
format:
	@echo "Running code formatters..."
	poetry run ruff format ${SRC}

.PHONY: validations
validations: check test

.PHONY: check
check:
	@echo "Running code linters..."
	poetry run ruff check ${SRC}

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
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