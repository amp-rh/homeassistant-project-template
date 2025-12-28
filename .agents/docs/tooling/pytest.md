# Testing with pytest

See @AGENTS.md for project-wide rules.

## Overview

This project uses [pytest](https://docs.pytest.org/) for testing.

## Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_example.py

# Run specific test function
uv run pytest tests/test_example.py::test_function_name

# Run with coverage
uv run pytest --cov=src
```

## Rules

- MUST run `pytest` before committing changes
- MUST add tests for new functionality
- MUST name test files `test_*.py`
- MUST name test functions `test_*`

## Test Structure

```
tests/
├── AGENTS.md           # Test index - see @tests/AGENTS.md
├── conftest.py         # Shared fixtures
├── test_*.py           # Test modules
└── unit/               # Optional: organized by type
    └── test_*.py
```

## Related

- @tests/AGENTS.md - Test directory guidance
- @.agents/docs/patterns/error-handling.md - Testing error cases
- @.agents/docs/workflows/testing.md - Testing workflow


