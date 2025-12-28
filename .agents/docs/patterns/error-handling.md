# Error Handling Patterns

See @AGENTS.md for project-wide rules.

## Overview

Consistent error handling patterns for this project.

## Principles

1. **Be specific** - Catch specific exceptions, not bare `except:`
2. **Fail fast** - Validate inputs early
3. **Preserve context** - Use exception chaining with `from`
4. **Log appropriately** - See @.agents/docs/patterns/logging.md

## Patterns

### Exception Chaining

```python
try:
    result = external_api_call()
except RequestError as e:
    raise ServiceError("Failed to fetch data") from e
```

### Custom Exceptions

```python
class ProjectError(Exception):
    """Base exception for this project."""
    pass

class ValidationError(ProjectError):
    """Raised when input validation fails."""
    pass
```

### Input Validation

```python
def process_data(data: dict) -> Result:
    if not data:
        raise ValidationError("Data cannot be empty")
    # ... process
```

## Related

- @.agents/docs/patterns/logging.md - Logging errors
- @.agents/docs/patterns/typing.md - Type hints for error handling
- @.agents/docs/tooling/pytest.md - Testing error cases


