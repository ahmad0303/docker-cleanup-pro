.PHONY: help install install-dev test lint format clean build publish docker-test

# Default target
help:
	@echo "Docker Cleanup Pro - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  install       - Install package for production"
	@echo "  install-dev   - Install package with development dependencies"
	@echo "  test          - Run tests with coverage"
	@echo "  test-quick    - Run tests without coverage"
	@echo "  lint          - Run linting checks (flake8)"
	@echo "  format        - Format code with black"
	@echo "  format-check  - Check code formatting without modifying"
	@echo "  type-check    - Run type checking with mypy"
	@echo "  clean         - Remove build artifacts and cache"
	@echo "  build         - Build distribution packages"
	@echo "  publish       - Publish to PyPI (requires credentials)"
	@echo "  docker-test   - Set up Docker test environment"
	@echo "  docker-clean  - Clean up Docker test environment"
	@echo "  all-checks    - Run all quality checks (format, lint, type, test)"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing targets
test:
	pytest --cov=docker_cleanup --cov-report=term-missing --cov-report=html

test-quick:
	pytest -v

# Code quality targets
lint:
	flake8 docker_cleanup tests --count --show-source --statistics

format:
	black docker_cleanup tests examples

format-check:
	black --check docker_cleanup tests examples

type-check:
	mypy docker_cleanup || true

# All checks at once
all-checks: format-check lint type-check test
	@echo "All checks passed!"

# Cleanup targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build and publish targets
build: clean
	python -m build

publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Docker testing targets
docker-test:
	@echo "Setting up Docker test environment..."
	docker-compose -f docker-compose.test.yml up -d
	@echo "Creating test containers..."
	docker run --name old_container_1 alpine:3.17 echo "test" || true
	docker run --name old_container_2 alpine:3.16 echo "test" || true
	@echo "Pulling test images..."
	docker pull nginx:1.23 || true
	docker pull nginx:1.22 || true
	docker pull nginx:1.21 || true
	@echo ""
	@echo "Test environment ready!"
	@echo "Run: docker-cleanup --dry-run"

docker-clean:
	@echo "Cleaning up Docker test environment..."
	docker-compose -f docker-compose.test.yml down -v
	docker rm -f old_container_1 old_container_2 2>/dev/null || true
	@echo "Test environment cleaned!"

# Development workflow
dev: install-dev
	@echo "Development environment ready!"
	@echo "Try: docker-cleanup --version"

# Quick start for contributors
setup: install-dev docker-test
	@echo "Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Make your changes"
	@echo "  2. Run: make all-checks"
	@echo "  3. Test manually: docker-cleanup --dry-run"
	@echo "  4. Submit a PR!"

# Run the tool in safe mode (for testing)
run-safe:
	docker-cleanup --safe

run-dry:
	docker-cleanup --dry-run

# Show Docker disk usage
docker-stats:
	@echo "Docker Disk Usage:"
	@docker system df
