# Project Structure

See @AGENTS.md for project-wide rules.

## Overview

Standard project layout for this Python project.

## Structure

```
project-root/
├── AGENTS.md               # Root agent index
├── README.md               # Project documentation
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── .agents/                # Agent documentation
│   └── docs/
│       ├── tooling/
│       ├── patterns/
│       ├── conventions/
│       ├── workflows/
│       └── architecture/
├── src/
│   ├── AGENTS.md           # Source code index
│   ├── __init__.py
│   └── package_name/       # Main package
│       ├── __init__.py
│       ├── models.py
│       ├── services.py
│       └── utils.py
└── tests/
    ├── AGENTS.md           # Test index
    ├── conftest.py         # Shared fixtures
    └── test_*.py           # Test modules
```

## Rules

- MUST place source code under `src/`
- MUST place tests under `tests/`
- MUST place agent documentation under `.agents/docs/`
- MUST have AGENTS.md in directories where agents will work

## Module Organization

### Single Responsibility

Each module should have a clear, single purpose:

- `models.py` - Data models and schemas
- `services.py` - Business logic
- `utils.py` - Utility functions
- `exceptions.py` - Custom exceptions

### Package Growth

When a module grows large, convert to a package:

```
services.py  →  services/
                ├── __init__.py
                ├── user_service.py
                └── order_service.py
```

## Related

- @.agents/docs/conventions/naming.md - File naming conventions
- @src/AGENTS.md - Source code guidance
- @tests/AGENTS.md - Test organization


