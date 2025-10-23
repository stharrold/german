---
name: git-workflow-manager
version: 5.0.0
description: |
  Manages git operations: worktree creation, branch management, commits,
  PRs, semantic versioning, and daily rebase workflow.

  Use when: Creating branches/worktrees, committing, pushing, versioning

  Triggers: create worktree, commit, push, rebase, version, PR
---

# Git Workflow Manager

## Purpose

Handles all git operations following git-flow + GitHub-flow hybrid model.

## Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑
release/vX.Y.Z                ← Release candidate
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution branch
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
hotfix/vX.Y.Z-hotfix.N       ← Production hotfix (worktree)
```

## Scripts

### create_worktree.py

Creates feature/release/hotfix worktree with TODO file.

```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  <feature|release|hotfix> <slug> <base_branch>
```

**Arguments:**
- `workflow_type`: feature, release, or hotfix
- `slug`: Short descriptive name (e.g., 'json-validator')
- `base_branch`: Branch to create from (e.g., 'contrib/username')

**Output:**
- Creates worktree directory
- Creates new branch
- Generates TODO file in main repo

### daily_rebase.py

Performs daily rebase of contrib branch onto develop.

```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  <contrib_branch>
```

**Steps:**
1. Checkout contrib branch
2. Fetch origin
3. Rebase onto origin/develop
4. Force push with lease

### semantic_version.py

Calculates semantic version based on component changes.

```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  <base_branch> <current_version>
```

**Version bump logic:**
- **MAJOR**: Breaking changes (API changes, removed features)
- **MINOR**: New features (new files, new functions)
- **PATCH**: Bug fixes, refactoring, docs

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

**Example:**
```
feat(validator): add JSON schema validation endpoint

Implements REST API endpoint for validating JSON against schemas.
Uses jsonschema library for validation logic.

Implements: impl_003
Spec: specs/json-validator/spec.md
Tests: tests/test_validator.py
Coverage: 85%

Refs: TODO_feature_20251022T143022Z_json-validator.md
```

## PR Creation

```bash
# Feature → contrib/<gh-user>
gh pr create \
  --base "contrib/<gh-user>" \
  --head "<feature-branch>" \
  --title "feat: <description>" \
  --body "See TODO_feature_*.md for details"

# After user merges in GitHub UI:
# Contrib → develop
gh pr create \
  --base "develop" \
  --head "contrib/<gh-user>" \
  --title "feat: <description>" \
  --body "Completed feature: <name>"
```

## Integration with Other Skills

Other skills call these scripts:

```python
import subprocess

# Create worktree
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
    'feature', 'my-feature', 'contrib/user'
], capture_output=True, text=True)

# Calculate version
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/semantic_version.py',
    'develop', 'v1.0.0'
], capture_output=True, text=True)

new_version = result.stdout.strip()
```
