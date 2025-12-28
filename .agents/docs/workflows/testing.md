# Testing Workflow

See @AGENTS.md for project-wide rules.

## Overview

Testing requirements and workflow for this project.

## When to Write Tests

- MUST write tests for new functionality
- MUST write tests when fixing bugs (regression tests)
- SHOULD write tests before implementing (TDD)

## Test Types

### Unit Tests

Test individual functions/methods in isolation:

```python
def test_validate_email_valid():
    assert validate_email("user@example.com") is True

def test_validate_email_invalid():
    assert validate_email("not-an-email") is False
```

### Integration Tests

Test interactions between components:

```python
def test_user_service_creates_user(db_session):
    service = UserService(db_session)
    user = service.create_user("test@example.com")
    assert user.id is not None
```

## Test Organization

```
tests/
├── conftest.py         # Shared fixtures
├── test_models.py      # Unit tests for models
├── test_services.py    # Unit tests for services
└── integration/        # Integration tests
    └── test_api.py
```

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src

# Specific file
uv run pytest tests/test_models.py

# Matching pattern
uv run pytest -k "test_validate"
```

## Related

- @.agents/docs/tooling/pytest.md - pytest commands and configuration
- @tests/AGENTS.md - Test directory index
- @.agents/docs/patterns/error-handling.md - Testing error cases


