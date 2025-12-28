# AGENTS.md - Source Code

See @AGENTS.md for project-wide rules.

## Documentation

### Patterns

- @.agents/docs/patterns/error-handling.md - Error handling patterns
- @.agents/docs/patterns/typing.md - Type hints and annotations
- @.agents/docs/patterns/logging.md - Logging conventions

### Conventions

- @.agents/docs/conventions/naming.md - Naming conventions
- @.agents/docs/conventions/imports.md - Import organization
- @.agents/docs/conventions/project-structure.md - Module organization

### Tooling

- @.agents/docs/tooling/ruff.md - Linting and formatting

## Rules

- MUST follow coding style in @.agents/docs/conventions/coding-style.md
- MUST use type hints on all public functions
- MUST use dataclasses for data structures
- MUST write tests first (TDD)
- MUST NOT include comments (code should self-document)
- MUST NOT use `print()` for operational output (use logging)
- MUST follow naming conventions in @.agents/docs/conventions/naming.md

## Structure

```
src/
├── AGENTS.md                   # This file
├── __init__.py                 # Package root
└── my_package/                 # Main package (TODO: rename to your package)
    └── __init__.py             # Package init with version
```
