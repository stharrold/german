# Worktree Cleanup Guide

## Problem

Orphaned worktrees and branches can accumulate when features are merged without proper cleanup. This wastes disk space and creates confusion about repository state.

## Prevention Strategies

### 1. Use Atomic Cleanup Script (Recommended)

**Always use the atomic cleanup script after merging a feature PR:**

```bash
cd /Users/stharrold/Documents/GitHub/german

python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  <slug> \
  --summary "Brief description of what was completed" \
  --version "X.Y.Z" \
  --project-name german
```

**Example:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  auth-system \
  --summary "Implemented user authentication with JWT tokens" \
  --version "1.5.0" \
  --project-name german
```

**Why this script?**
- ✅ **Atomic operation**: Either everything succeeds or nothing changes (safe to retry)
- ✅ **Correct ordering**: Archive TODO → Delete worktree → Delete branches
- ✅ **Single command**: Replaces 4 manual steps that can be forgotten
- ✅ **Prevents orphans**: Cannot delete worktree without archiving TODO first

### 2. Post-Merge Checklist

After merging any feature PR, follow this checklist:

- [ ] ✅ Verify PR merged successfully in GitHub UI
- [ ] ✅ Return to main repo: `cd /Users/stharrold/Documents/GitHub/german`
- [ ] ✅ Run atomic cleanup: `cleanup_feature.py <slug> --summary "..." --version "X.Y.Z"`
- [ ] ✅ Verify worktree removed: `git worktree list` (should only show main repo)
- [ ] ✅ Verify branches deleted locally: `git branch --list 'feature/*<slug>*'` (should be empty)
- [ ] ✅ Verify branches deleted remotely: `gh api repos/:owner/:repo/git/refs/heads --jq '.[] | select(.ref | contains("<slug>"))'` (should be empty)

### 3. Periodic Audit

Run weekly or monthly to detect orphaned worktrees:

```bash
# List all worktrees (should only show main repo when no active work)
git worktree list

# Find merged feature branches that should be deleted
git branch --merged contrib/stharrold | grep 'feature/'

# Find remote branches that might need cleanup
gh api repos/:owner/:repo/git/refs/heads --jq '.[] | select(.ref | contains("feature/")) | .ref'
```

### 4. Small Fixes Without TODO Files

For small fixes that don't warrant a TODO file (like PR review feedback), you still need to clean up worktrees and branches:

**Manual cleanup (when no TODO file exists):**

```bash
# 1. Remove worktree (use --force if it has uncommitted changes)
git worktree remove /Users/stharrold/Documents/GitHub/german_feature_<timestamp>_<slug>
# Or with force:
git worktree remove --force /Users/stharrold/Documents/GitHub/german_feature_<timestamp>_<slug>

# 2. Delete local branch
git branch -D feature/<timestamp>_<slug>

# 3. Delete remote branch (use gh CLI for reliability)
gh api repos/:owner/:repo/git/refs/heads/feature/<timestamp>_<slug> --method DELETE
```

**Example:**
```bash
git worktree remove --force /Users/stharrold/Documents/GitHub/german_feature_20251118T130351Z_issue-259-todo-status-fix
git branch -D feature/20251118T130351Z_issue-259-todo-status-fix
gh api repos/:owner/:repo/git/refs/heads/feature/20251118T130351Z_issue-259-todo-status-fix --method DELETE
```

## Manual Cleanup Walkthrough

If orphaned worktrees already exist, here's how to clean them up:

### Step 1: Identify Orphaned Worktrees

```bash
# List all worktrees
git worktree list

# Check which feature branches are merged
git branch --merged contrib/stharrold | grep 'feature/'
```

### Step 2: For Each Orphaned Worktree

Extract the slug from the worktree path (e.g., `german_feature_20251118T130351Z_issue-259-todo-status-fix` → slug is `issue-259-todo-status-fix`)

**If TODO file exists:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  <slug> \
  --summary "..." \
  --version "X.Y.Z" \
  --project-name german
```

**If TODO file does NOT exist (small fixes):**
```bash
# Use manual cleanup commands above
git worktree remove --force /Users/stharrold/Documents/GitHub/german_feature_<timestamp>_<slug>
git branch -D feature/<timestamp>_<slug>
gh api repos/:owner/:repo/git/refs/heads/feature/<timestamp>_<slug> --method DELETE
```

### Step 3: Verify Cleanup

```bash
# Should only show main repo
git worktree list

# Should be empty (no merged feature branches)
git branch --merged contrib/stharrold | grep 'feature/'

# Should be empty (no feature branches with this slug)
gh api repos/:owner/:repo/git/refs/heads --jq '.[] | select(.ref | contains("<slug>")) | .ref'
```

## Why GitHub API Instead of git push?

When GitHub's git server has issues (HTTP 500), the REST API often still works:

```bash
# ❌ May fail with "Internal Server Error"
git push origin --delete feature/<branch-name>

# ✅ More reliable - uses different infrastructure
gh api repos/:owner/:repo/git/refs/heads/feature/<branch-name> --method DELETE
```

## Common Errors

### Error: "contains modified or untracked files"

**Solution:** Use `--force` flag
```bash
git worktree remove --force /path/to/worktree
```

### Error: "Reference does not exist (HTTP 422)"

**Solution:** Branch was already deleted remotely. This is OK - continue with cleanup.

### Error: "No TODO file found for slug"

**Solution:** Small fixes don't always have TODO files. Use manual cleanup instead of `cleanup_feature.py`.

## Recovery

If you accidentally deleted a worktree but forgot to delete branches:

```bash
# List orphaned branches (worktree is gone but branch exists)
git branch -vv | grep ': gone]'

# Delete orphaned local branch
git branch -D <branch-name>

# Delete orphaned remote branch
gh api repos/:owner/:repo/git/refs/heads/<branch-name> --method DELETE
```

## Integration with Workflow

This cleanup process is **Phase 4.6** of the standard workflow:

1. Phase 4.1: Create PR (feature → contrib)
2. Phase 4.2: Review & approve PR
3. Phase 4.3: Merge PR in GitHub UI
4. Phase 4.4: (Optional) Generate work-items from PR feedback
5. **Phase 4.6: Atomic cleanup** ← YOU ARE HERE
6. Phase 4.7: Rebase contrib onto develop
7. Phase 4.8: Create PR (contrib → develop)
8. Phase 4.9: Merge to develop

## Automation Opportunities (Future)

Potential improvements to automate cleanup:

1. **Post-merge Git hook**: Warn if worktrees exist for merged branches
2. **GitHub Actions workflow**: Detect stale branches and create issues
3. **Cron job**: Weekly audit report of orphaned worktrees
4. **Enhanced cleanup script**: Auto-detect merged branches and prompt for cleanup

## Related Documentation

- **[WORKFLOW.md](../WORKFLOW.md)** - Complete 6-phase workflow guide
- **[CLAUDE.md](../CLAUDE.md)** - Quick reference commands
- **[.claude/skills/git-workflow-manager/SKILL.md](../.claude/skills/git-workflow-manager/SKILL.md)** - Git workflow manager skill documentation

---

**Version:** 1.0.0
**Created:** 2025-11-18
**Last Updated:** 2025-11-18
