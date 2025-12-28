# /extract-learnings

Extract and document learnings from the current session or codebase.

## Purpose

Capture insights, patterns, gotchas, and decisions discovered during development and save them to `.agents/learnings/` for future reference.

## Steps

1. **Review session**: Look back at the current session for:
   - Problems solved and their solutions
   - Patterns that worked well
   - Gotchas or pitfalls encountered
   - Decisions made and their rationale
2. **Check scratch notes**: Review `.agents/scratch/` for any notes worth preserving
3. **Analyze code changes**: Look at recent changes for implicit learnings
4. **Document learnings**: Create or update files in `.agents/learnings/`
5. **Update related docs**: If a learning is significant, add it to appropriate docs in `.agents/docs/`

## Learning Categories

### Patterns
Reusable solutions that worked well:
```markdown
# Pattern: <name>

## Context
When you need to...

## Solution
```python
# code example
```

## Why It Works
Explanation...
```

### Gotchas
Pitfalls to avoid:
```markdown
# Gotcha: <name>

## Problem
What went wrong...

## Cause
Why it happened...

## Solution
How to avoid or fix it...
```

### Decisions
Significant choices made:
```markdown
# Decision: <name>

## Context
What prompted this...

## Options Considered
1. Option A
2. Option B

## Choice
What was chosen and why...
```

### Tips
Useful shortcuts or techniques:
```markdown
# Tip: <name>

## When to Use
Situation...

## How
Instructions...
```

## Output Location

Save to `.agents/learnings/` with descriptive filenames:
- `pattern-<name>.md`
- `gotcha-<name>.md`
- `decision-<name>.md`
- `tip-<name>.md`

Or organize by topic:
- `testing/async-fixtures.md`
- `deployment/container-caching.md`

## What to Extract

- Error messages and their fixes
- Configuration that took trial and error
- Performance optimizations discovered
- Integration quirks between tools
- Workarounds for known issues
- Best practices learned the hard way

## Rules

- MUST be actionable and specific
- MUST include context (when does this apply?)
- MUST include examples where helpful
- SHOULD reference related docs with @-links
- SHOULD NOT duplicate existing documentation

## Related

- @.agents/learnings/ - Where learnings are stored
- @.agents/scratch/ - Source for session notes
- @.agents/docs/patterns/ - For patterns worth promoting to docs
- @.agents/docs/architecture/decisions.md - For significant decisions (ADRs)


