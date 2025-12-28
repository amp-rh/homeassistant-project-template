# /commit

Commit staged changes or all changes to git.

## Purpose

Create a git commit with a well-formatted message following project conventions.

## Steps

1. **Check status**: Run `git status` to see what files have changed
2. **Run checks**: Before committing, ensure:
   - `uv run pytest` passes
   - `uv run ruff check .` passes
   - `uv run ruff format --check .` passes (or run `ruff format .` to fix)
3. **Stage files**: Either stage specific files or use `git add -A` for all changes
4. **Generate commit message**: Create a message following the conventional commit format
5. **Commit**: Run `git commit -m "<message>"`

## Commit Message Format

```
type(scope): description

[optional body]
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `refactor` - Code refactoring (no feature change)
- `test` - Adding or updating tests
- `chore` - Maintenance, dependencies, config
- `style` - Formatting, whitespace (no code change)

### Scope

Optional. The area of the codebase affected (e.g., `auth`, `api`, `models`).

### Description

- Use imperative mood ("add feature" not "added feature")
- Don't capitalize first letter
- No period at the end
- Keep under 50 characters

## Examples

```bash
# Simple feature
git commit -m "feat: add user authentication"

# With scope
git commit -m "feat(auth): add password reset flow"

# Bug fix
git commit -m "fix: resolve null pointer in user service"

# Documentation
git commit -m "docs: update API reference"

# Breaking change (add ! after type)
git commit -m "feat!: change API response format"
```

## Rules

- MUST run tests before committing
- MUST run linting before committing
- MUST use conventional commit format
- SHOULD keep commits atomic (one logical change per commit)
- SHOULD NOT commit generated files (check `.gitignore`)

## Related

- @.agents/docs/workflows/pr-process.md - Full PR workflow


