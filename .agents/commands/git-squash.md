# /git-squash

Squash multiple commits into a single commit.

## Purpose

Combine multiple commits into one clean commit before merging or pushing, keeping git history clean and readable.

## Steps

1. **Identify commits**: Determine which commits to squash
2. **Check branch state**: Ensure working directory is clean (`git status`)
3. **Interactive rebase**: Squash commits using `git rebase -i`
4. **Write commit message**: Create a clear, combined commit message
5. **Force push** (if needed): Push the rewritten history

## Methods

### Method 1: Squash Last N Commits

```bash
# Squash last 3 commits
git rebase -i HEAD~3
```

In the editor, change `pick` to `squash` (or `s`) for commits to combine:
```
pick abc1234 First commit
squash def5678 Second commit
squash ghi9012 Third commit
```

### Method 2: Squash to Branch Point

```bash
# Squash all commits since branching from main
git rebase -i main
```

### Method 3: Soft Reset (Alternative)

```bash
# Reset to N commits back, keeping changes staged
git reset --soft HEAD~3

# Create new single commit
git commit -m "feat: combined feature"
```

### Method 4: Squash Merge (for branches)

```bash
# Merge branch with squash (doesn't modify source branch)
git checkout main
git merge --squash feature-branch
git commit -m "feat: add feature"
```

## Commit Message for Squashed Commits

Combine the intent of all commits:

```
type(scope): summary of all changes

- Detail from commit 1
- Detail from commit 2
- Detail from commit 3

Squashed commits:
- abc1234 First commit message
- def5678 Second commit message
- ghi9012 Third commit message
```

## Safety Checks

Before squashing:
```bash
# Check current branch
git branch --show-current

# View commits to be squashed
git log --oneline HEAD~N..HEAD

# Ensure clean state
git status
```

## After Squashing

```bash
# Force push if already pushed (CAUTION: rewrites history)
git push --force-with-lease

# Or if on a feature branch with no collaborators
git push --force
```

## Rules

- MUST NOT squash commits already on main/shared branches
- MUST use `--force-with-lease` over `--force` when possible
- MUST run tests after squashing to verify nothing broke
- SHOULD squash before creating PR, not after review
- SHOULD preserve meaningful commit boundaries when appropriate

## Common Issues

### Conflict During Rebase
```bash
# Fix conflicts, then
git add .
git rebase --continue

# Or abort if needed
git rebase --abort
```

### Wrong Commits Squashed
```bash
# Undo the rebase (if not pushed)
git reflog
git reset --hard HEAD@{N}  # N from reflog
```

## Related

- @.agents/commands/commit.md - Commit message format
- @.agents/docs/workflows/pr-process.md - PR workflow


