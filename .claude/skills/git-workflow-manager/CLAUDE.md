# Claude Code Context: git-workflow-manager

## Purpose

Git Workflow Manager provides **automated git operations** for the git-flow + GitHub-flow hybrid workflow with worktrees. It handles branch creation, worktree management, commits, PRs, semantic versioning, and daily rebase operations. All operations are designed to work with the isolated worktree development pattern and VCS provider abstraction (GitHub/Azure DevOps).

## Directory Structure

```
.claude/skills/git-workflow-manager/
├── scripts/                      # Git operation automation
│   ├── create_worktree.py        # Create feature/release/hotfix worktrees (Phase 2)
│   ├── daily_rebase.py          # Rebase contrib onto develop (daily maintenance)
│   ├── semantic_version.py       # Calculate semantic version from changes (Phase 3)
│   ├── create_release.py         # Create release branch from develop (Phase 5)
│   ├── tag_release.py            # Tag release on main after merge (Phase 5)
│   ├── backmerge_release.py      # Back-merge release to develop (Phase 5)
│   ├── cleanup_release.py        # Cleanup release branch after completion (Phase 5)
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### create_worktree.py

**Purpose:** Create isolated worktree for feature/release/hotfix development with automatic TODO file creation

**When to use:** Phase 2 (Implementation) - after BMAD planning (optional), before SpecKit

**Invocation:**
```bash
# Feature worktree from contrib branch
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/<gh-user>

# Release worktree from develop
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  release <version> develop

# Hotfix worktree from main
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix <slug> main
```

**Examples:**
```bash
# Feature: Create feature/20251104T143000Z_auth-system from contrib/stharrold
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature auth-system contrib/stharrold

# Release: Create release/v1.6.0 from develop
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  release v1.6.0 develop

# Hotfix: Create hotfix/20251104T150000Z_security-patch from main
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix security-patch main
```

**What it does:**
1. Validates workflow type (feature/release/hotfix) and slug format
2. Generates timestamp in compact ISO8601 format (YYYYMMDDTHHMMSSZ)
3. Creates branch: `<type>/<timestamp>_<slug>` or `release/<version>`
4. Creates worktree directory: `../german_<type>_<slug>/`
5. Creates TODO file: `TODO_<type>_<timestamp>_<slug>.md` in **main repo**
6. Initializes TODO with YAML frontmatter and basic structure
7. Prints worktree path and instructions

**Key features:**
- Timestamp format avoids shell escaping issues (no colons/hyphens)
- TODO file stored in main repo (not worktree) for persistence
- Validates base branch exists
- Creates compliant directory structure
- Error handling with cleanup on failure

---

### daily_rebase.py

**Purpose:** Rebase contrib branch onto develop to stay current with integration branch

**When to use:** Daily maintenance, before starting new work, before creating PR

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/<gh-user>
```

**Example:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold
```

**What it does:**
1. Validates branch starts with `contrib/`
2. Checks for uncommitted changes (fails if dirty)
3. Checks out contrib branch
4. Fetches from origin
5. Rebases onto origin/develop
6. Force pushes with `--force-with-lease` (safe force push)

**Key features:**
- Safe force push: `--force-with-lease` prevents overwriting others' work
- Validates clean working tree before rebase
- Comprehensive error handling
- Target branch: `origin/develop` (documented rationale)

---

### semantic_version.py

**Purpose:** Calculate semantic version automatically based on code changes

**When to use:** Phase 3 (Quality Gates) - after implementation, before PR

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  <base-branch> <current-version>
```

**Example:**
```bash
# From feature branch, compare to develop, current version v1.5.0
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.6.0 (if new features detected)
```

**What it does:**
1. Compares changed files between current branch and base branch
2. Analyzes changes using semver rules:
   - **MAJOR** (X.0.0): Breaking changes (API changes, removed features)
   - **MINOR** (1.X.0): New features (new files in src/, new endpoints)
   - **PATCH** (1.5.X): Bug fixes, refactoring, docs, tests
3. Calculates next version from current version + change type
4. Outputs new version (e.g., `1.6.0`)

**Key features:**
- Automatic version calculation (no manual decisions)
- File-based change analysis
- Semantic versioning compliance
- Used by quality-enforcer to update TODO frontmatter

---

### create_release.py

**Purpose:** Create release branch from develop for final QA and release preparation

**When to use:** Phase 5 (Release) - when develop is ready for production

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  <version> <base-branch>
```

**Example:**
```bash
# Create release/v1.6.0 from develop
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.6.0 develop
```

**What it does:**
1. Validates version format (vX.Y.Z)
2. Creates branch: `release/<version>` from base branch
3. Creates TODO file: `TODO_release_<timestamp>_<version-slug>.md`
4. Initializes TODO with YAML frontmatter
5. Prints instructions for next steps

**Key features:**
- Version format validation (semantic versioning)
- TODO file tracking for release workflow
- Prevents duplicate release branches

---

### tag_release.py

**Purpose:** Tag release on main branch after PR merge

**When to use:** Phase 5 (Release) - after merging release PR to main

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  <version> <branch>
```

**Example:**
```bash
# Tag v1.6.0 on main branch
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.6.0 main
```

**What it does:**
1. Validates version format (vX.Y.Z)
2. Checks out specified branch (usually main)
3. Creates annotated git tag: `<version>`
4. Pushes tag to origin
5. Updates CHANGELOG.md (if exists)

**Key features:**
- Annotated tags (includes message)
- Version validation
- Automatic CHANGELOG updates

---

### backmerge_release.py

**Purpose:** Back-merge release changes to develop after tagging

**When to use:** Phase 5 (Release) - after tagging release on main

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  <version> <target-branch>
```

**Example:**
```bash
# Merge release/v1.6.0 back to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.6.0 develop
```

**What it does:**
1. Checks out target branch (develop)
2. Merges release branch
3. Resolves conflicts if any (manual intervention required)
4. Pushes to origin

**Key features:**
- Keeps develop in sync with production
- Handles merge conflicts gracefully
- Validates branches exist

---

### cleanup_release.py

**Purpose:** Delete release branch after successful completion

**When to use:** Phase 5 (Release) - after back-merge completes

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  <version>
```

**Example:**
```bash
# Delete release/v1.6.0 locally and remotely
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.6.0
```

**What it does:**
1. Validates release is tagged and merged
2. Deletes local branch: `release/<version>`
3. Deletes remote branch: `origin/release/<version>`
4. Archives TODO file to ARCHIVED/

**Key features:**
- Safety checks (tag must exist, branch must be merged)
- Cleans up both local and remote branches
- Archives release TODO file

---

## Usage by Claude Code

### Phase 2: Create Feature Worktree

**Context:** User wants to start implementing a feature

**User says:**
- "Create feature worktree for auth system"
- "Start working on new feature"
- "Begin implementation"

**Claude Code should:**
```python
import subprocess

# Call create_worktree.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
    'feature',
    'auth-system',  # slug
    'contrib/stharrold'  # base branch
], check=True)

# After worktree created, move to SpecKit (Phase 2.3)
```

---

### Daily Maintenance: Rebase Contrib

**Context:** User starts new session or before creating PR

**User says:**
- "Rebase my branch"
- "Update contrib branch"
- "Sync with develop"

**Claude Code should:**
```python
import subprocess

# Call daily_rebase.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/daily_rebase.py',
    'contrib/stharrold'
], check=True)
```

---

### Phase 3: Calculate Version

**Context:** Implementation complete, need semantic version for PR

**User says:**
- "What version should this be?"
- "Calculate semantic version"
- "Run quality gates"

**Claude Code should:**
```python
import subprocess

# Call semantic_version.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/semantic_version.py',
    'develop',  # base branch
    'v1.5.0'    # current version
], capture_output=True, text=True, check=True)

new_version = result.stdout.strip()  # e.g., "1.6.0"

# Use new_version in TODO file, PR title, etc.
```

---

### Phase 5: Release Workflow

**Context:** Develop ready for production release

**User says:**
- "Create release"
- "Prepare v1.6.0 for production"
- "Start release process"

**Claude Code should execute sequence:**
```python
import subprocess

# Step 1: Create release branch
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_release.py',
    'v1.6.0',
    'develop'
], check=True)

# Step 2: User performs QA, updates docs in release branch

# Step 3: User creates PR (release/v1.6.0 → main) and merges in GitHub UI

# Step 4: Tag release on main
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/tag_release.py',
    'v1.6.0',
    'main'
], check=True)

# Step 5: Back-merge to develop
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/backmerge_release.py',
    'v1.6.0',
    'develop'
], check=True)

# Step 6: Cleanup release branch
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/cleanup_release.py',
    'v1.6.0'
], check=True)
```

---

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls create_worktree.py at Phase 2 start
- Orchestrator calls semantic_version.py at Phase 3
- Orchestrator calls daily_rebase.py as needed

**speckit-author:**
- SpecKit runs in worktrees created by create_worktree.py
- SpecKit reads TODO file created by create_worktree.py

**quality-enforcer:**
- Quality enforcer calls semantic_version.py to calculate version
- Updates TODO frontmatter with semantic_version result

**workflow-utilities:**
- Uses workflow_archiver.py to archive TODO files
- Uses vcs abstraction for PR creation (gh/az cli)

**bmad-planner:**
- BMAD planning happens before create_worktree.py
- Worktree references ../planning/<slug>/ for context

---

## Git-Flow + GitHub-Flow Hybrid

This skill implements a hybrid workflow:

**Git-Flow elements:**
- Long-lived branches: main, develop, contrib/<user>
- Feature branches from contrib
- Release branches from develop
- Hotfix branches from main

**GitHub-Flow elements:**
- PRs for all merges
- Short-lived feature branches
- Continuous integration via develop
- Worktree isolation

**Worktree pattern:**
- Feature work happens in isolated worktrees
- TODO files stored in main repo (persistent)
- Clean separation between main repo and worktrees

---

## Constants and Rationale

**TIMESTAMP_FORMAT:** `YYYYMMDDTHHMMSSZ` (compact ISO8601)
- **Rationale:** No colons/hyphens avoids shell escaping issues. Remains intact when branch names are parsed by underscores.

**VALID_WORKFLOW_TYPES:** `['feature', 'release', 'hotfix']`
- **Rationale:** Supports all workflow phases with clear naming

**TARGET_BRANCH:** `origin/develop`
- **Rationale:** Integration branch for all contributions. All contrib branches rebase onto develop.

**Force push safety:** `--force-with-lease`
- **Rationale:** Only force-pushes if remote hasn't changed since last fetch. Prevents accidental overwrites.

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[WORKFLOW.md](../../WORKFLOW.md)** - Complete 6-phase workflow guide

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Calls git-workflow-manager scripts
- **speckit-author** - Runs in worktrees created by this skill
- **quality-enforcer** - Uses semantic_version.py
- **workflow-utilities** - Provides VCS abstraction and TODO utilities
- **bmad-planner** - Planning happens before worktree creation
