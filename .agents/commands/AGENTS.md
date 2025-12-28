# AGENTS.md - Commands

See @AGENTS.md for project-wide rules.

## Overview

This directory contains slash command definitions for AI agents.

## Usage

When a user invokes a slash command (e.g., `/commit`), the agent should:

1. Look for a matching `.md` file in this directory (e.g., `commit.md`)
2. Read and follow the instructions in that file
3. If no matching command exists, create one based on the user's intent

## Command File Format

Each command file should contain:

- **Purpose**: What the command does
- **Steps**: Ordered steps to execute
- **Rules**: Constraints and requirements
- **Examples**: Usage examples (optional)

## Available Commands

- @.agents/commands/commit.md - Stage and commit changes
- @.agents/commands/extract-learnings.md - Extract and document learnings
- @.agents/commands/extract-templates.md - Extract reusable templates from codebase
- @.agents/commands/git-squash.md - Squash multiple commits
- @.agents/commands/update-agents-md.md - Update AGENTS.md files
