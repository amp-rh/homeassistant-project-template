# /update-agents-md

Update AGENTS.md files to reflect current project state.

## Purpose

Ensure all AGENTS.md files are accurate and up-to-date with the current project structure, documentation, and learnings.

## Steps

1. **Scan project structure**: List all directories and identify which have/need AGENTS.md files
2. **Check for missing AGENTS.md**: Create AGENTS.md in any directory where agents will work but one doesn't exist
3. **Update directory listings**: Ensure file/folder listings in each AGENTS.md match actual contents
4. **Update documentation links**: Verify all @-links point to existing files
5. **Add new learnings**: If patterns were learned during the session, document them in appropriate docs
6. **Update root AGENTS.md**: Ensure the root index reflects any structural changes

## Checklist

- [ ] All working directories have AGENTS.md
- [ ] Project structure in root AGENTS.md is accurate
- [ ] Documentation index links are valid
- [ ] Command list is current
- [ ] Scratch workspace templates are linked
- [ ] New directories are documented

## Rules

- MUST follow existing AGENTS.md header format
- MUST use @-linking for cross-references
- MUST NOT remove existing documentation without reason
- SHOULD add learnings to @.agents/learnings/ when discovered

## What to Update

### Root AGENTS.md
- Project structure tree
- Documentation index
- Command list
- Directory indexes

### Directory AGENTS.md files
- File listings
- Related documentation links
- Directory-specific rules

### .agents/AGENTS.md
- Structure listing
- New directories or files

## Related

- @AGENTS.md - Root index to update
- @.agents/AGENTS.md - Agent resources index
- @.agents/learnings/ - Document new patterns here


