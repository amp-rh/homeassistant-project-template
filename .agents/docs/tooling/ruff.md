# Linting and Formatting with Ruff

See @AGENTS.md for project-wide rules.

## Overview

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting Python code.

## Commands

```bash
# Check for linting issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

## Configuration

Ruff is configured in `pyproject.toml`. See the `[tool.ruff]` section.

## Rules

- MUST run `ruff check` before committing
- MUST run `ruff format` before committing
- SHOULD fix linting issues rather than disabling rules

## Related

- @.agents/docs/conventions/imports.md - Import sorting (handled by Ruff)
- @.agents/docs/workflows/pr-process.md - Pre-commit checks


