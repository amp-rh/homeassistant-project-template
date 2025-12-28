# Pull Request Process

See @AGENTS.md for project-wide rules.

## Overview

Workflow for creating and reviewing pull requests.

## Before Creating a PR

1. **Sync dependencies**: `uv sync`
2. **Run tests**: `uv run pytest`
3. **Run linting**: `uv run ruff check .`
4. **Format code**: `uv run ruff format .`

## PR Checklist

- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Code is formatted
- [ ] AGENTS.md updated if patterns learned
- [ ] Relevant docs updated

## Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code refactoring
- `test` - Adding tests
- `chore` - Maintenance

## Branch Naming

```
type/short-description
```

Examples:
- `feat/user-authentication`
- `fix/validation-error`
- `docs/api-reference`

## Related

- @.agents/docs/workflows/testing.md - Testing requirements
- @.agents/docs/tooling/ruff.md - Linting checks
- @.agents/docs/tooling/pytest.md - Running tests


