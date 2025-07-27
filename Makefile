# Makefile for acoustic-solo-dadaGP

.PHONY: help install install-dev test test-cli test-all clean build

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install the package in development mode"
	@echo "  install-dev  - Install the package with development dependencies"
	@echo "  test         - Run all tests"
	@echo "  test-cli     - Run only CLI tests"
	@echo "  test-all     - Run all tests with coverage"
	@echo "  clean        - Clean up build artifacts"
	@echo "  build        - Build the package"
	@echo "  install-cli  - Install the CLI globally"

# Install the package in development mode
install:
	pip install -e .

# Install with development dependencies
install-dev:
	pip install -e ".[dev]"

# Run all tests
test:
	python -m pytest tests/ -v

# Run only CLI tests
test-cli:
	python -m pytest tests/test_cli.py -v

# Run all tests with coverage
test-all:
	python -m pytest tests/ -v --cov=asdadagp --cov-report=term-missing --cov-report=html

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Build the package
build:
	python -m build

# Install the CLI globally
install-cli:
	pip install -e .
	@echo "CLI installed. You can now use 'asdadagp' command."

# Development setup
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to run tests" 