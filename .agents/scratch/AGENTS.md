# AGENTS.md - Scratch Workspace

See @AGENTS.md for project-wide rules.

## Overview

This is a structured working area for agents to take notes, work through decisions, and maintain session context.

## Structure

```
scratch/
├── session.md          # Current session context (overwritten each session)
├── decisions/          # Work through choices with structured templates
├── notes/              # General working notes
├── context/            # Persistent context between sessions
├── drafts/             # Work-in-progress code and docs
└── research/           # Investigation findings
```

## Usage

### Session Context

Use `session.md` to track the current session's state. This file is overwritten each session - use `context/` for things that should persist.

### Making Decisions

1. Copy `decisions/_template.md` to a new file (e.g., `decisions/auth-approach.md`)
2. Work through each section
3. Document the final decision
4. Reference from commits or ADRs if the decision is significant

### Taking Notes

Use `notes/` for any working notes. Copy `notes/_template.md` or create freeform files.

### Research

When investigating a topic, use `research/_template.md` to structure findings.

### Drafts

Use `drafts/` for work-in-progress code, documentation, or other files that aren't ready for the main codebase.

## Git Behavior

- **Tracked**: This AGENTS.md and all `_template.md` files
- **Gitignored**: All other files in this workspace

This keeps templates versioned while keeping working files out of git history.

## Templates

- @.agents/scratch/decisions/_template.md - Decision-making template
- @.agents/scratch/notes/_template.md - Notes template
- @.agents/scratch/context/_template.md - Context template
- @.agents/scratch/research/_template.md - Research template

