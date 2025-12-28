.PHONY: help install dev test lint format check build run clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Install with dev dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## Run all checks (lint + test)

build: ## Build container image
	podman build -t python-project-template:latest .

run: ## Run container
	podman run --rm -p 8000:8000 python-project-template:latest

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
