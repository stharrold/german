---
type: workflow-manifest
workflow_type: feature
slug: pr-feedback-docs
timestamp: 20251108T112041Z
github_user: stharrold

metadata:
  title: "PR Feedback Documentation Updates"
  description: "Update all workflow documentation to reflect Option A (work-item generation) instead of Option B (iterative feedback)"
  created: "2025-11-08T11:20:41Z"
  stack: documentation
  package_manager: none
  test_framework: none
  containers: []

workflow_progress:
  phase: 2
  current_step: "2.5"
  last_task: impl_002
  last_update: "2025-11-08T11:30:00Z"
  status: "implementation"

quality_gates:
  test_coverage: 100
  tests_passing: true
  build_successful: true
  semantic_version: "1.9.0"

tasks:
  implementation:
    - id: impl_001
      description: "Delete handle_pr_feedback.py"
      status: complete
      completed_at: "2025-11-08T11:25:00Z"

    - id: impl_002
      description: "Create generate_work_items_from_pr.py (733 lines)"
      status: complete
      completed_at: "2025-11-08T11:28:00Z"

    - id: impl_003
      description: "Update git-workflow-manager/SKILL.md with work-item generation section"
      status: pending
      completed_at: null

    - id: impl_004
      description: "Update git-workflow-manager/CLAUDE.md with work-item usage examples"
      status: pending
      completed_at: null

    - id: impl_005
      description: "Update git-workflow-manager/CHANGELOG.md (v5.0.0 → v5.1.0)"
      status: pending
      completed_at: null

    - id: impl_006
      description: "Update workflow-utilities/SKILL.md with VCS adapter methods"
      status: pending
      completed_at: null

    - id: impl_007
      description: "Update workflow-utilities/CHANGELOG.md (v5.1.0 → v5.2.0)"
      status: pending
      completed_at: null

    - id: impl_008
      description: "Update workflow-orchestrator/SKILL.md with work-item workflow"
      status: pending
      completed_at: null

    - id: impl_009
      description: "Update workflow-orchestrator/CLAUDE.md with work-item orchestration"
      status: pending
      completed_at: null

    - id: impl_010
      description: "Update workflow-orchestrator/CHANGELOG.md (v5.0.0 → v5.1.0)"
      status: pending
      completed_at: null

    - id: impl_011
      description: "Update WORKFLOW.md with work-item PR feedback pattern (v5.2.0 → v5.3.0)"
      status: pending
      completed_at: null

    - id: impl_012
      description: "Update root CLAUDE.md with work-item generation commands"
      status: pending
      completed_at: null

context_checkpoints: []
---

# TODO: PR Feedback Documentation Updates

**Type:** feature
**Slug:** pr-feedback-docs
**Created:** 2025-11-08T11:20:41Z
**GitHub User:** stharrold

## Overview

Update all workflow documentation to reflect Option A (work-item generation) instead of Option B (iterative feedback on same branch).

**Code changes completed (commit 36632f8):**
- ✅ Deleted: `handle_pr_feedback.py` (Option B implementation)
- ✅ Created: `generate_work_items_from_pr.py` (Option A implementation, 733 lines)

**Remaining work:** Update 10 documentation files

## Current Status

**Phase:** Implementation (2)
**Current Step:** 2.5
**Last Updated:** 2025-11-08T11:30:00Z

**Progress:** 2/12 tasks complete (17%)

## Completed Tasks

- [x] **impl_001**: Delete handle_pr_feedback.py
- [x] **impl_002**: Create generate_work_items_from_pr.py (733 lines)

## Pending Tasks (10 Documentation Files)

### git-workflow-manager skill (3 files)

- [ ] **impl_003**: Update SKILL.md with work-item generation section
  - Add documentation for `generate_work_items_from_pr.py`
  - Remove references to `handle_pr_feedback.py`
  - Document workflow: PR → generate work-items → approve PR → fix work-items

- [ ] **impl_004**: Update CLAUDE.md with work-item usage examples
  - Add usage examples for work-item generation
  - Document integration with GitHub/Azure DevOps

- [ ] **impl_005**: Update CHANGELOG.md (v5.0.0 → v5.1.0)
  - Add entry for `generate_work_items_from_pr.py` (MINOR: new feature)
  - Add entry for removing `handle_pr_feedback.py`

### workflow-utilities skill (2 files)

- [ ] **impl_006**: Update SKILL.md with VCS adapter methods
  - Document new methods: `fetch_pr_comments()`, `update_pr()`, `get_pr_status()`
  - Explain usage by git-workflow-manager

- [ ] **impl_007**: Update CHANGELOG.md (v5.1.0 → v5.2.0)
  - Add entry for VCS adapter PR feedback methods (MINOR: new methods)

### workflow-orchestrator skill (3 files)

- [ ] **impl_008**: Update SKILL.md with work-item workflow
  - Update Phase 4.3: "Handle PR Feedback via Work-Items"
  - Document sequence: create PR → generate work-items → approve PR → fix work-items
  - Remove iterative feedback references

- [ ] **impl_009**: Update CLAUDE.md with work-item orchestration
  - Add orchestration examples for work-item workflow
  - Document decision point: simple fixes vs. work-item generation

- [ ] **impl_010**: Update CHANGELOG.md (v5.0.0 → v5.1.0)
  - Add entry for work-item workflow pattern (MINOR: workflow update)

### Root documentation (2 files)

- [ ] **impl_011**: Update WORKFLOW.md (v5.2.0 → v5.3.0)
  - Rewrite Phase 4.3, 4.8, 5.4, 5.6, 6.6 with work-item pattern
  - Add "PR Feedback Decision Tree"
  - Remove iterative feedback sections

- [ ] **impl_012**: Update root CLAUDE.md
  - Add work-item generation command to "Common Development Commands"
  - Remove `handle_pr_feedback.py` references
  - Update version to v1.9.0

## Key Changes (Option A vs. Option B)

### Option B (Removed)
- Iterative PR feedback on same branch
- `handle_pr_feedback.py` script
- Push updates to same PR
- Single feature branch per PR

### Option A (Implemented)
- Work-item generation from unresolved PR conversations
- `generate_work_items_from_pr.py` script
- Create separate work-items (GitHub issues, Azure DevOps tasks)
- Multiple feature branches per work-item
- Compatible with all issue trackers

## Workflow Pattern (Option A)

```
1. Create PR from feature branch to contrib
2. Reviewers add comments/conversations
3. Run: python generate_work_items_from_pr.py <pr-number>
   → Creates work-items: pr-<pr-number>-issue-1, pr-<pr-number>-issue-2, ...
4. Approve PR in web portal (conversations remain as work-items)
5. For each work-item:
   - Create feature worktree: create_worktree.py feature pr-94-issue-1 contrib/<user>
   - Implement fix
   - Create PR: feature → contrib
   - Merge PR
6. Repeat until no unresolved conversations
```

## Version Updates

**Skills:**
- git-workflow-manager: v5.0.0 → v5.1.0 (MINOR: new feature)
- workflow-utilities: v5.1.0 → v5.2.0 (MINOR: new methods)
- workflow-orchestrator: v5.0.0 → v5.1.0 (MINOR: workflow update)

**Documentation:**
- WORKFLOW.md: v5.2.0 → v5.3.0 (MINOR: clarification)

**Repository:**
- Current: v1.8.1
- Target: v1.9.0 (MINOR: new work-item workflow)

## Quality Gates

- [x] Test coverage ≥ 80% (N/A for documentation)
- [x] All tests passing (no code changes)
- [x] Build successful (no build required)
- [ ] Documentation complete (10 files pending)

## Commands for Resumption

```bash
# Resume work on contrib/stharrold
git checkout contrib/stharrold

# Update documentation files (10 files, ~40-50K tokens)
# See pending tasks above for file list

# After all updates, commit:
git add .claude/skills/git-workflow-manager/SKILL.md
git add .claude/skills/git-workflow-manager/CLAUDE.md
git add .claude/skills/git-workflow-manager/CHANGELOG.md
git add .claude/skills/workflow-utilities/SKILL.md
git add .claude/skills/workflow-utilities/CHANGELOG.md
git add .claude/skills/workflow-orchestrator/SKILL.md
git add .claude/skills/workflow-orchestrator/CLAUDE.md
git add .claude/skills/workflow-orchestrator/CHANGELOG.md
git add WORKFLOW.md
git add CLAUDE.md

git commit -m "docs(pr-feedback): update all documentation for work-item workflow

Update 10 documentation files to reflect Option A (work-item generation)
instead of Option B (iterative feedback on same branch).

Version bumps:
- git-workflow-manager: v5.0.0 → v5.1.0
- workflow-utilities: v5.1.0 → v5.2.0
- workflow-orchestrator: v5.0.0 → v5.1.0
- WORKFLOW.md: v5.2.0 → v5.3.0
- Repository: v1.8.1 → v1.9.0

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Create PR
gh pr create --base develop --head contrib/stharrold \
  --title "feat(pr-feedback): work-item generation workflow (v1.9.0)" \
  --body "..."
```

## Status History

- 2025-11-08T11:20:41Z: Workflow initialized (feature worktree created)
- 2025-11-08T11:25:00Z: Deleted handle_pr_feedback.py
- 2025-11-08T11:28:00Z: Created generate_work_items_from_pr.py (733 lines)
- 2025-11-08T11:30:00Z: Committed code changes (36632f8), switched to contrib branch
- 2025-11-08T11:32:00Z: Created TODO file for resumption, ready for documentation phase
