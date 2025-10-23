---
type: workflow-manifest
workflow_type: feature
slug: workflow
timestamp: 20251023T123254Z
github_user: stharrold

metadata:
  title: "Release Workflow Automation"
  description: "Implement automation scripts for Phase 5 release workflow (create_release.py, tag_release.py, backmerge_release.py, cleanup_release.py)"
  created: "2025-10-23T12:32:54Z"
  stack: python
  package_manager: uv
  test_framework: pytest
  containers: []

workflow_progress:
  phase: 2
  current_step: "2.4"
  last_task: null
  last_update: "2025-10-23T12:32:54Z"
  status: "implementation"

quality_gates:
  test_coverage: 80
  tests_passing: false
  build_successful: false
  linting_clean: false
  types_clean: false
  semantic_version: "1.2.0"

tasks:
  implementation:
    - id: impl_001
      description: "Create create_release.py script"
      status: pending
      files:
        - .claude/skills/git-workflow-manager/scripts/create_release.py
      dependencies: []
    - id: impl_002
      description: "Create tag_release.py script"
      status: pending
      files:
        - .claude/skills/git-workflow-manager/scripts/tag_release.py
      dependencies: []
    - id: impl_003
      description: "Create backmerge_release.py script"
      status: pending
      files:
        - .claude/skills/git-workflow-manager/scripts/backmerge_release.py
      dependencies: []
    - id: impl_004
      description: "Create cleanup_release.py script"
      status: pending
      files:
        - .claude/skills/git-workflow-manager/scripts/cleanup_release.py
      dependencies: []
    - id: impl_005
      description: "Update git-workflow-manager SKILL.md with new scripts"
      status: pending
      files:
        - .claude/skills/git-workflow-manager/SKILL.md
      dependencies: [impl_001, impl_002, impl_003, impl_004]
  testing:
    - id: test_001
      description: "Unit tests for create_release.py"
      status: pending
      files:
        - tests/skills/test_create_release.py
      dependencies: [impl_001]
    - id: test_002
      description: "Integration test for full release workflow"
      status: pending
      files:
        - tests/skills/test_release_workflow.py
      dependencies: [impl_001, impl_002, impl_003, impl_004]
  documentation:
    - id: doc_001
      description: "Update CLAUDE.md with Phase 5 commands reference"
      status: pending
      files:
        - CLAUDE.md
      dependencies: [impl_005]
---

# TODO: Release Workflow Automation

Implement automation scripts for Phase 5 release workflow to enable production releases following git-flow pattern.

## Context

**Current State:**
- Phase 5 documentation complete in WORKFLOW.md (commit 8b7d9c4)
- Documented 8-step release process
- No automation scripts exist yet
- Users must use manual git/gh commands

**Goal:**
Implement 4 Python scripts to automate release workflow, following best practices from create_worktree.py and daily_rebase.py.

**Reference Documentation:**
- WORKFLOW.md lines 487-703 (Phase 5 section)
- ARCHIVED/Workflow-v5x2.md lines 663-669 (original Phase 5 spec)

---

## Implementation Tasks

### impl_001: Create create_release.py

**File:** `.claude/skills/git-workflow-manager/scripts/create_release.py`

**Purpose:** Create release branch from develop with TODO file

**Command Signature:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  <version> <base_branch>
```

**Arguments:**
- `version`: Semantic version (e.g., v1.1.0, v2.0.0)
- `base_branch`: Branch to release from (typically 'develop')

**Implementation Requirements:**

1. **Input Validation:**
   - Version must match pattern `v[0-9]+\.[0-9]+\.[0-9]+`
   - Base branch must exist
   - Working directory must be clean (no uncommitted changes)

2. **Version Verification:**
   - Call `semantic_version.py` to calculate recommended version from base_branch
   - If provided version differs, warn user and ask for confirmation
   - Check that version doesn't already exist as tag

3. **Branch Creation:**
   - Create `release/v1.1.0` branch from base_branch
   - Push to origin

4. **TODO File Creation:**
   - Filename: `TODO_release_<timestamp>_<version-slug>.md` (e.g., TODO_release_20251023T143000Z_v1-1-0.md)
   - Use workflow-orchestrator TODO_template.md
   - Set workflow_type: release
   - Set slug: version with hyphens (v1-1-0)

5. **Error Handling:**
   - Try/except for all git operations
   - Helpful messages for: branch exists, dirty working tree, network failures
   - Cleanup on failure (delete branch if TODO creation fails)

6. **Constants to Document:**
   - RELEASE_BRANCH_PREFIX = 'release/'
   - VERSION_PATTERN = r'^v\d+\.\d+\.\d+$'
   - Rationale: git-flow release branch naming convention

**Output:**
```
✓ Created release branch: release/v1.1.0
✓ Base: develop (commit abc123)
✓ TODO file: TODO_release_20251023T143000Z_v1-1-0.md
✓ Ready for final QA and documentation updates
```

---

### impl_002: Create tag_release.py

**File:** `.claude/skills/git-workflow-manager/scripts/tag_release.py`

**Purpose:** Create annotated tag on main branch after release merge

**Command Signature:**
```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  <version> <branch>
```

**Arguments:**
- `version`: Semantic version to tag (e.g., v1.1.0)
- `branch`: Branch to tag (typically 'main')

**Implementation Requirements:**

1. **Input Validation:**
   - Version must match pattern `v[0-9]+\.[0-9]+\.[0-9]+`
   - Branch must exist
   - Tag must not already exist (locally or remotely)

2. **Branch Operations:**
   - Checkout specified branch
   - Pull latest from origin
   - Verify branch is up-to-date with remote

3. **Tag Creation:**
   - Create annotated tag (not lightweight)
   - Tag message format: "Release {version}: {one-line summary}"
   - Extract summary from recent commits or CHANGELOG.md

4. **Tag Push:**
   - Push tag to origin
   - Verify push succeeded

5. **GitHub Release (Optional):**
   - Attempt to trigger GitHub release creation via gh CLI
   - If gh CLI available: `gh release create {version} --generate-notes`
   - Non-fatal if gh not available (just skip)

6. **Error Handling:**
   - Check if tag already exists (locally and remotely)
   - Handle network failures on push
   - Handle gh CLI not found gracefully

7. **Constants to Document:**
   - TAG_MESSAGE_TEMPLATE = "Release {version}: {summary}"
   - Rationale: Annotated tags include metadata, recommended for releases

**Output:**
```
✓ Checked out main branch
✓ Pulled latest changes (commit def456)
✓ Created annotated tag: v1.1.0
   Message: "Release v1.1.0: Production release with vocabulary modules"
✓ Pushed tag to origin
✓ GitHub release created: https://github.com/user/german/releases/tag/v1.1.0
```

---

### impl_003: Create backmerge_release.py

**File:** `.claude/skills/git-workflow-manager/scripts/backmerge_release.py`

**Purpose:** Merge release branch back to develop after main merge

**Command Signature:**
```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  <version> <target_branch>
```

**Arguments:**
- `version`: Release version (e.g., v1.1.0)
- `target_branch`: Branch to merge into (typically 'develop')

**Implementation Requirements:**

1. **Input Validation:**
   - Version must match pattern `v[0-9]+\.[0-9]+\.[0-9]+`
   - Release branch `release/{version}` must exist
   - Target branch must exist
   - Tag `{version}` must exist (ensures release was tagged)

2. **Branch Operations:**
   - Checkout target branch (develop)
   - Pull latest from origin
   - Verify clean working tree

3. **Merge Strategy:**
   - Attempt `git merge release/{version} --no-ff`
   - Use `--no-ff` to preserve release branch history

4. **Conflict Handling:**
   - **No conflicts:** Push merge to origin, complete
   - **Conflicts detected:**
     - Create PR via gh CLI for manual resolution
     - PR title: "chore(release): back-merge {version} to develop"
     - PR body: List conflicts, link to release tag
     - Do NOT push conflicted state

5. **Error Handling:**
   - Abort merge on conflicts, create PR instead
   - Handle push failures
   - Handle gh CLI not available (abort with manual instructions)

6. **Constants to Document:**
   - MERGE_STRATEGY = '--no-ff'
   - Rationale: Preserves release branch history in develop

**Output (no conflicts):**
```
✓ Checked out develop
✓ Pulled latest changes
✓ Merged release/v1.1.0 into develop (fast-forward)
✓ Pushed to origin/develop
✓ Back-merge complete
```

**Output (with conflicts):**
```
⚠ Merge conflicts detected
✓ Created PR: https://github.com/user/german/pull/46
  Title: "chore(release): back-merge v1.1.0 to develop"

Please resolve conflicts in GitHub UI and merge.
```

---

### impl_004: Create cleanup_release.py

**File:** `.claude/skills/git-workflow-manager/scripts/cleanup_release.py`

**Purpose:** Delete release branch after successful release and back-merge

**Command Signature:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  <version>
```

**Arguments:**
- `version`: Release version (e.g., v1.1.0)

**Implementation Requirements:**

1. **Input Validation:**
   - Version must match pattern `v[0-9]+\.[0-9]+\.[0-9]+`
   - Release branch `release/{version}` must exist

2. **Safety Checks (all must pass):**
   - Tag `{version}` must exist (ensures release was tagged)
   - Tag must be on main branch (ensures release was merged)
   - Release commits must be in develop (ensures back-merge completed)
   - If any check fails: abort with error message

3. **Branch Deletion:**
   - Delete local branch: `git branch -d release/{version}`
   - Use `-d` (not `-D`) to ensure branch is fully merged
   - Delete remote branch: `git push origin --delete release/{version}`

4. **TODO File Archival:**
   - Find `TODO_release_*_{version-slug}.md` in repo root
   - Use workflow-utilities/scripts/archive_manager.py
   - Update TODO.md manifest

5. **Error Handling:**
   - If tag doesn't exist: "ERROR: Tag {version} not found. Release may not be complete."
   - If tag not on main: "ERROR: Tag {version} not on main. Release merge incomplete."
   - If not in develop: "ERROR: Release not back-merged to develop. Run backmerge_release.py first."
   - If branch delete fails: show manual commands

6. **Constants to Document:**
   - REQUIRED_BRANCHES = ['main', 'develop']
   - Rationale: Ensures release is in production and integration branches

**Output:**
```
✓ Verified tag v1.1.0 exists
✓ Verified tag on main branch
✓ Verified back-merge to develop complete
✓ Deleted local branch: release/v1.1.0
✓ Deleted remote branch: origin/release/v1.1.0
✓ Archived: TODO_release_20251023T143000Z_v1-1-0.md
✓ Release workflow complete for v1.1.0
```

---

### impl_005: Update git-workflow-manager SKILL.md

**File:** `.claude/skills/git-workflow-manager/SKILL.md`

**Add documentation for 4 new scripts:**

1. Under "Scripts" section, add subsections for each:
   - create_release.py
   - tag_release.py
   - backmerge_release.py
   - cleanup_release.py

2. Follow same format as existing scripts (create_worktree.py, daily_rebase.py, semantic_version.py)

3. Include:
   - Purpose
   - Command signature
   - Arguments
   - Output example

4. Add "Release Workflow" section explaining:
   - When to use release workflow (vs. hotfix)
   - Typical sequence: create → QA → tag → backmerge → cleanup
   - Integration with Phase 5 in WORKFLOW.md

---

## Testing Tasks

### test_001: Unit Tests for create_release.py

**File:** `tests/skills/test_create_release.py`

**Test Cases:**
1. Valid release creation
2. Invalid version format
3. Version already exists as tag
4. Base branch doesn't exist
5. Dirty working tree
6. Version mismatch with semantic_version.py recommendation

**Coverage target:** ≥80%

---

### test_002: Integration Test for Full Release Workflow

**File:** `tests/skills/test_release_workflow.py`

**Test Scenario:**
1. Create test git repo with develop branch
2. Run create_release.py v1.0.0 develop
3. Mock release merge to main
4. Run tag_release.py v1.0.0 main
5. Run backmerge_release.py v1.0.0 develop
6. Run cleanup_release.py v1.0.0
7. Verify all branches/tags in correct state

**Coverage target:** Integration test (no coverage requirement)

---

## Documentation Tasks

### doc_001: Update CLAUDE.md

**File:** `CLAUDE.md`

**Add Phase 5 commands to "Common Development Commands" section:**

```markdown
### Release Management

```bash
# Create release branch
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.1.0 develop

# Tag release on main
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.1.0 main

# Back-merge to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.1.0 develop

# Cleanup release branch
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.1.0
```
```

---

## Quality Gates

Before creating PR, verify:

1. **Test Coverage:** ≥80% on all new scripts
2. **All Tests Passing:** pytest runs clean
3. **Linting Clean:** ruff check passes
4. **Type Checking Clean:** mypy passes
5. **Build Successful:** uv build completes
6. **Integration Test:** Full release workflow executes without errors

---

## Semantic Version Calculation

**Base version:** v1.1.0 (current, from commit 8b7d9c4)

**Changes:**
- New feature: 4 new scripts for release automation
- Enhancement: Complete release workflow support

**Recommended version:** v1.2.0 (MINOR)

**Rationale:** New features (release automation), no breaking changes

---

## Commit Message Template

```
feat(release): implement automated release workflow scripts

Implemented 4 automation scripts for Phase 5 release workflow:

1. create_release.py - Create release branch from develop
   - Input validation (version format, branch existence)
   - Version verification with semantic_version.py
   - TODO file generation
   - Error handling with cleanup on failure

2. tag_release.py - Tag release on main branch
   - Annotated tag creation with metadata
   - GitHub release generation (optional)
   - Tag push verification

3. backmerge_release.py - Merge release back to develop
   - No-fast-forward merge strategy
   - Conflict detection with PR creation
   - Safety checks (tag exists, etc.)

4. cleanup_release.py - Delete release branch after completion
   - Safety checks (tag exists, in main, in develop)
   - Local and remote branch deletion
   - TODO file archival

All scripts follow best practices:
- Comprehensive error handling
- Input validation
- Documented constants
- Helpful error messages
- Cleanup on failure

Updated:
- git-workflow-manager/SKILL.md (script documentation)
- CLAUDE.md (command reference)

Tests:
- Unit tests for create_release.py (85% coverage)
- Integration test for full workflow

Implements: impl_001, impl_002, impl_003, impl_004, impl_005
Tests: test_001, test_002
Docs: doc_001
Coverage: 85%

Refs: TODO_feature_20251023T123254Z_workflow.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Notes

**Best Practices Applied:**
- Follow patterns from create_worktree.py and daily_rebase.py
- Use timezone-aware datetime (datetime.now(timezone.utc))
- Document constants with rationale
- Comprehensive error handling
- Input validation before operations
- Cleanup on failure
- stderr for errors, stdout for data

**Technical Decisions:**
- Annotated tags (not lightweight) for release metadata
- --no-ff merge for back-merge (preserves history)
- Safety checks in cleanup (prevents premature deletion)
- PR creation for merge conflicts (safer than forced merge)

**Future Enhancements (out of scope):**
- Hotfix workflow automation
- Automated CHANGELOG.md generation
- Release notes from commit history
- Version bumping in pyproject.toml
- Multi-release branch support

---

## Progress Tracking

Update task status using:
```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_20251023T123254Z_workflow.md <task_id> <status>
```

Status values: `pending`, `in_progress`, `complete`, `blocked`
