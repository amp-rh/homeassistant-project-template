# Architecture Decision Records

See @AGENTS.md for project-wide rules.

## Overview

This document tracks significant architecture and design decisions for this project.

## ADR Template

When adding a new decision, use this format:

```markdown
### ADR-NNN: Title

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded

**Context**: What is the issue?

**Decision**: What was decided?

**Consequences**: What are the results?
```

---

## Decisions

### ADR-001: Use uv for Package Management

**Date**: 2024-01-01
**Status**: Accepted

**Context**: Need a fast, reliable Python package manager that handles virtual environments and dependency resolution.

**Decision**: Use [uv](https://github.com/astral-sh/uv) for all package management.

**Consequences**:
- Fast dependency installation
- Consistent lock files
- Integrated virtual environment management
- See @.agents/docs/tooling/uv.md for usage

---

### ADR-002: Use Ruff for Linting and Formatting

**Date**: 2024-01-01
**Status**: Accepted

**Context**: Need consistent code style and linting. Previously required multiple tools (black, isort, flake8).

**Decision**: Use [Ruff](https://github.com/astral-sh/ruff) for both linting and formatting.

**Consequences**:
- Single tool for linting and formatting
- Extremely fast (written in Rust)
- Configuration in `pyproject.toml`
- See @.agents/docs/tooling/ruff.md for usage

---

### ADR-003: AGENTS.md as Documentation Index

**Date**: 2024-01-01
**Status**: Accepted

**Context**: AI agents need guidance when working on code. Documentation should be discoverable and granular.

**Decision**: Use AGENTS.md files as indexes in each directory where agents work, linking to focused documentation in `.agents/docs/`.

**Consequences**:
- Agents can discover relevant docs via directory-local AGENTS.md
- Documentation is granular and selectively loadable
- Heavy use of @-linking reduces duplication
- Agent docs separated from human docs
- Documentation must be kept up to date

## Related

- @AGENTS.md - Root project index
- @.agents/docs/workflows/pr-process.md - Documentation update requirements


