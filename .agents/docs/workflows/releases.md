# Release Process

See @AGENTS.md for project-wide rules.

## Overview

Process for creating releases of this project.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

## Release Checklist

1. [ ] All tests pass
2. [ ] CHANGELOG updated
3. [ ] Version bumped in `pyproject.toml`
4. [ ] Documentation updated
5. [ ] Git tag created

## Version Bump

Update version in `pyproject.toml`:

```toml
[project]
version = "X.Y.Z"
```

## Creating a Release

```bash
# Ensure clean state
uv run pytest
uv run ruff check .

# Create tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

## Changelog Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description
```

## Related

- @.agents/docs/workflows/pr-process.md - PR requirements before release
- @.agents/docs/tooling/uv.md - Dependency management


