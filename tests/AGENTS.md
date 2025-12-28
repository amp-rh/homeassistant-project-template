# AGENTS.md - Tests

See @AGENTS.md for project-wide rules.

## Documentation

### Testing

- @.agents/docs/tooling/pytest.md - pytest commands and configuration
- @.agents/docs/workflows/testing.md - Testing workflow and requirements

### Patterns

- @.agents/docs/patterns/error-handling.md - Testing error cases

## Rules

- MUST name test files `test_*.py`
- MUST name test functions `test_*`
- MUST use fixtures from `conftest.py` when available
- MUST run `uv run pytest` before committing

## Structure

```
tests/
├── AGENTS.md           # This file
├── conftest.py         # Shared fixtures
├── test_*.py           # Test modules
└── integration/        # Integration tests (optional)
    └── test_*.py
```

## Fixtures

Shared fixtures are defined in `conftest.py`. Check there first before creating test-specific setup.

Common fixtures:
- See `conftest.py` for available fixtures

## Running Tests

```bash
# All tests
uv run pytest

# Verbose
uv run pytest -v

# Specific file
uv run pytest tests/test_example.py

# With coverage
uv run pytest --cov=src
```
