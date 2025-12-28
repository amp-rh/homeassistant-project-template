.PHONY: help install dev test lint format check build run clean setup build-addon test-addon

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --extra dev

setup: ## Setup local development environment
	@./scripts/setup-local-dev.sh

dev: ## Start local development server
	@./scripts/test-local.sh

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

build: build-addon ## Build add-on container (alias for build-addon)

build-addon: ## Build Home Assistant add-on container
	@./scripts/build-addon.sh

run: ## Run add-on locally (without HA)
	@./scripts/test-local.sh

test-addon: ## Test add-on with Home Assistant
	@./scripts/test-with-ha.sh

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info data
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
