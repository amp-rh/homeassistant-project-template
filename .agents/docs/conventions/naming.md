# Naming Conventions

See @AGENTS.md for project-wide rules.

## Overview

Consistent naming conventions following PEP 8 and project standards.

## Rules

| Type | Convention | Example |
|------|------------|---------|
| Modules | `snake_case` | `user_service.py` |
| Packages | `snake_case` | `my_package/` |
| Classes | `PascalCase` | `UserService` |
| Functions | `snake_case` | `get_user_by_id` |
| Variables | `snake_case` | `user_count` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES` |
| Private | `_leading_underscore` | `_internal_helper` |

## Specific Patterns

### Boolean Variables

Prefix with `is_`, `has_`, `can_`, `should_`:

```python
is_active = True
has_permission = user.check_permission()
can_edit = is_admin or is_owner
```

### Collections

Use plural nouns:

```python
users = get_all_users()
item_ids = [item.id for item in items]
```

### Functions

Use verb phrases:

```python
def get_user(user_id: int) -> User: ...
def create_order(items: list[Item]) -> Order: ...
def validate_input(data: dict) -> bool: ...
```

## Related

- @.agents/docs/conventions/imports.md - Module naming in imports
- @.agents/docs/conventions/project-structure.md - File naming


