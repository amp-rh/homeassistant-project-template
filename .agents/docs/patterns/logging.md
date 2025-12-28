# Logging Conventions

See @AGENTS.md for project-wide rules.

## Overview

Consistent logging patterns for this project using Python's `logging` module.

## Setup

```python
import logging

logger = logging.getLogger(__name__)
```

## Log Levels

| Level | Use Case |
|-------|----------|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | General operational events |
| `WARNING` | Something unexpected but handled |
| `ERROR` | A failure that needs attention |
| `CRITICAL` | System-wide failure |

## Patterns

### Structured Logging

```python
logger.info("Processing item", extra={"item_id": item.id, "status": "started"})
```

### Exception Logging

```python
try:
    risky_operation()
except SomeError:
    logger.exception("Operation failed")  # Includes traceback
```

### Contextual Information

```python
logger.info("Request processed", extra={
    "duration_ms": duration,
    "user_id": user.id,
    "endpoint": request.path,
})
```

## Rules

- MUST use `logger = logging.getLogger(__name__)` per module
- MUST NOT use `print()` for operational output
- SHOULD include relevant context in log messages
- SHOULD use `logger.exception()` when logging caught exceptions

## Related

- @.agents/docs/patterns/error-handling.md - Logging errors


