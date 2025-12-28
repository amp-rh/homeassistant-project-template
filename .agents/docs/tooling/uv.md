# uv Package Manager

See @AGENTS.md for project-wide rules.

## Overview

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

## Commands

```bash
# Install dependencies
uv sync

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Run a command in the virtual environment
uv run <command>

# Update lock file
uv lock
```

## Optional Dependency Groups

```bash
# Install with dev dependencies (pytest, ruff)
uv sync --extra dev
```

| Group | Packages | Purpose |
|-------|----------|---------|
| `dev` | pytest, pytest-cov, ruff | Testing and linting |

## Rules

- MUST run `uv sync` after cloning the repository
- MUST run `uv sync` after modifying `pyproject.toml`
- MUST use `uv add` to add dependencies (not manual editing)
- MUST NOT commit without `uv.lock` being up to date

## Related

- @.agents/docs/tooling/pytest.md - Running tests with uv
- @.agents/docs/workflows/pr-process.md - Dependency change process
