# AGENTS.md

This file is the authoritative index for AI agents working on this project. Read this before making any changes.

## Project Structure

```
project-root/
├── AGENTS.md           # This file (root index)
├── .agents/            # Agent documentation
│   ├── commands/       # Slash command definitions
│   ├── docs/           # Granular, linked docs
│   │   ├── tooling/    # uv, pytest, ruff
│   │   ├── patterns/   # Error handling, typing, logging
│   │   ├── conventions/# Naming, imports, structure
│   │   ├── workflows/  # PR process, testing, releases
│   │   └── architecture/# Design decisions
│   ├── learnings/      # Discovered patterns and insights
│   ├── plans/          # Implementation plans
│   ├── scratch/        # Agent working space (gitignored)
│   ├── tasks/          # Task tracking
│   └── templates/      # Reusable templates
├── src/                # Source code - see @src/AGENTS.md
└── tests/              # Tests - see @tests/AGENTS.md
```

## Core Rules

- MUST read the relevant AGENTS.md before modifying files in any directory
- MUST run `uv sync` after modifying `pyproject.toml`
- MUST run `pytest` before committing changes
- MUST NOT add dependencies without documenting in @.agents/docs/tooling/uv.md
- MUST update relevant docs when patterns are learned or decisions made

## Documentation Index

### Tooling

- @.agents/docs/tooling/uv.md - Package management with uv
- @.agents/docs/tooling/pytest.md - Testing with pytest
- @.agents/docs/tooling/ruff.md - Linting and formatting

### Patterns

- @.agents/docs/patterns/error-handling.md - Error handling patterns
- @.agents/docs/patterns/typing.md - Type hints and annotations
- @.agents/docs/patterns/logging.md - Logging conventions

### Conventions

- @.agents/docs/conventions/coding-style.md - Coding style (clean, OOP, TDD)
- @.agents/docs/conventions/naming.md - Naming conventions
- @.agents/docs/conventions/imports.md - Import organization
- @.agents/docs/conventions/project-structure.md - Project layout

### Workflows

- @.agents/docs/workflows/pr-process.md - Pull request workflow
- @.agents/docs/workflows/testing.md - Testing workflow
- @.agents/docs/workflows/releases.md - Release process
- @.agents/docs/workflows/contributing.md - Contributing to this template

### Architecture

- @.agents/docs/architecture/decisions.md - Architecture Decision Records

## Commands

Slash commands are defined in `.agents/commands/`. When a `/command` is used, read the corresponding file.

- @.agents/commands/commit.md - `/commit` - Stage and commit changes
- @.agents/commands/extract-learnings.md - `/extract-learnings` - Document learnings
- @.agents/commands/extract-templates.md - `/extract-templates` - Extract reusable templates
- @.agents/commands/git-squash.md - `/git-squash` - Squash multiple commits
- @.agents/commands/update-agents-md.md - `/update-agents-md` - Update AGENTS.md files

See @.agents/commands/AGENTS.md for command format.

## Scratch Workspace

Use `.agents/scratch/` for working notes, decisions, and drafts. Templates are provided; working files are gitignored.

- @.agents/scratch/AGENTS.md - Workspace usage guide
- @.agents/scratch/decisions/_template.md - Decision-making template
- @.agents/scratch/notes/_template.md - Notes template
- @.agents/scratch/context/_template.md - Session context template
- @.agents/scratch/research/_template.md - Research template

## Directory Indexes

- @.agents/AGENTS.md - Agent resources
- @src/AGENTS.md - Source code guidance
- @tests/AGENTS.md - Test guidance
