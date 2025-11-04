---
type: workflow-manifest
workflow_type: feature
slug: protect-main-develop
github_user: stharrold
timestamp: 20251104T170000Z
title: "Branch Protection Documentation"

workflow_progress:
  phase: 3
  current_step: "3.5"
  last_task: quality_005
  created_at: "2025-11-04T17:00:00Z"
  completed_at: "2025-11-04T18:30:00Z"

quality_gates:
  test_coverage: 88.1
  tests_passing: true
  semantic_version: "1.6.0"
  linting_clean: true

tasks:
  documentation:
    - id: doc_001
      description: "Add 'Branch Protection Policy' section to WORKFLOW.md after line 93"
      status: pending
      priority: high
      estimated_time: "30min"
      details: |
        Add comprehensive section explaining:
        - Main and develop are permanent branches (never delete)
        - Never commit directly to main or develop
        - All changes via pull requests only
        - Quality gates required before merge
        - Exception: backmerge_release.py (document why)

    - id: doc_002
      description: "Update CLAUDE.md 'Git Branch Structure' section"
      status: pending
      priority: high
      estimated_time: "15min"
      details: |
        Add explicit statement in line ~240 area:
        - Protected branches: main, develop
        - Never delete, never commit directly
        - PR-only merge policy

    - id: doc_003
      description: "Update CONTRIBUTING.md with 'Protected Branches' section"
      status: pending
      priority: high
      estimated_time: "20min"
      details: |
        Add to "Development Workflow" section:
        - Protected branch rules
        - What happens if you violate them
        - How to fix if you accidentally commit to protected branch

    - id: doc_004
      description: "Update README.md with protected branches quick reference"
      status: pending
      priority: medium
      estimated_time: "10min"
      details: |
        Add after "Technology Stack" section:
        - Quick note about main/develop protection
        - Link to WORKFLOW.md for details

    - id: doc_005
      description: "Update git-workflow-manager/SKILL.md with protected branch policy"
      status: pending
      priority: high
      estimated_time: "20min"
      details: |
        Add to skill documentation:
        - Branch protection as core responsibility
        - Scripts must never commit to main/develop
        - Validation that protection is enforced

    - id: doc_006
      description: "Update initialize-repository/SKILL.md with GitHub setup steps"
      status: pending
      priority: high
      estimated_time: "25min"
      details: |
        Add "Post-Application Steps" section:
        - GitHub branch protection configuration
        - Pre-push hook installation
        - Link to .github/BRANCH_PROTECTION.md guide

  github_setup:
    - id: github_001
      description: "Create .github/BRANCH_PROTECTION.md configuration guide"
      status: pending
      priority: high
      estimated_time: "30min"
      details: |
        Step-by-step guide for configuring GitHub:
        - Branch protection rules for main (screenshots if possible)
        - Branch protection rules for develop
        - Recommended settings (require PR, status checks, etc.)
        - How to verify protection is active
        - Troubleshooting common issues

    - id: github_002
      description: "Create .github/ directory structure"
      status: pending
      priority: medium
      estimated_time: "5min"
      details: |
        Create .github/ directory with:
        - BRANCH_PROTECTION.md
        - README.md explaining directory purpose

  safety_hooks:
    - id: hook_001
      description: "Create .git-hooks/pre-push hook template"
      status: pending
      priority: medium
      estimated_time: "20min"
      details: |
        Create pre-push hook that prevents:
        - Direct pushes to main
        - Direct pushes to develop
        - Provides helpful error message
        - Instructions to create PR instead

    - id: hook_002
      description: "Document pre-push hook installation in WORKFLOW.md Phase 0"
      status: pending
      priority: medium
      estimated_time: "15min"
      details: |
        Add to Phase 0 (Initial Setup):
        - How to install pre-push hook
        - What it does
        - How to test it
        - How to bypass (only if absolutely necessary)

  exception_documentation:
    - id: except_001
      description: "Document backmerge_release.py as allowed exception"
      status: pending
      priority: high
      estimated_time: "20min"
      details: |
        In multiple locations (WORKFLOW.md, git-workflow-manager/SKILL.md):
        - Explain why backmerge_release.py commits to develop
        - This is the ONLY exception to the rule
        - How it maintains integrity (always from release branch)
        - Why it's safe (no code changes, just merge commits)

    - id: except_002
      description: "Add warning comment to backmerge_release.py script"
      status: pending
      priority: medium
      estimated_time: "10min"
      details: |
        Add prominent comment at top of script:
        # WARNING: This script commits directly to develop
        # This is an EXCEPTION to branch protection policy
        # Only used for back-merging releases (Phase 5)
        # See WORKFLOW.md "Branch Protection Policy" for details

  testing:
    - id: test_001
      description: "Create test_branch_protection.py to verify script compliance"
      status: pending
      priority: medium
      estimated_time: "30min"
      details: |
        Create test that verifies:
        - All workflow scripts are scanned
        - No script has hardcoded commits to main
        - Only backmerge_release.py commits to develop
        - Tag operations on main are allowed (read-only + tag)

    - id: test_002
      description: "Add branch protection validation to quality-enforcer"
      status: pending
      priority: low
      estimated_time: "20min"
      details: |
        Add quality gate check:
        - Scans all Python scripts in .claude/skills/
        - Flags any that commit to main or develop (except exceptions)
        - Runs during Phase 3 quality gates

  quality:
    - id: quality_001
      description: "Run all tests with coverage"
      status: pending
      priority: high
      estimated_time: "5min"
      dependencies: ["test_001"]

    - id: quality_002
      description: "Validate version consistency across all updated files"
      status: pending
      priority: high
      estimated_time: "5min"
      details: |
        Run: python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose

    - id: quality_003
      description: "Verify cross-references in documentation"
      status: pending
      priority: medium
      estimated_time: "15min"
      details: |
        Check that:
        - All references to "Branch Protection Policy" are correct
        - Links to .github/BRANCH_PROTECTION.md work
        - Section references are accurate

    - id: quality_004
      description: "Update CHANGELOG.md with changes"
      status: pending
      priority: high
      estimated_time: "10min"
      details: |
        Add entry for this feature:
        - Type: MINOR (new feature - branch protection documentation)
        - Document all files changed
        - Note impact on workflow

    - id: quality_005
      description: "Calculate semantic version"
      status: pending
      priority: high
      estimated_time: "5min"
      dependencies: ["quality_001", "quality_004"]
      details: |
        Run: python .claude/skills/git-workflow-manager/scripts/semantic_version.py develop v1.5.1
        Expected: v1.6.0 (MINOR - new documentation feature)

  workflow_management:
    - id: workflow_001
      description: "Register workflow in TODO.md"
      status: pending
      priority: high
      estimated_time: "5min"
      details: |
        Run: python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
          TODO_feature_20251104T170000Z_protect-main-develop.md feature protect-main-develop \
          --title "Branch Protection Documentation"

dependencies:
  test_001:
    depends_on: ["doc_005"]  # Need git-workflow-manager docs first
  quality_001:
    depends_on: ["test_001"]
  quality_005:
    depends_on: ["quality_001", "quality_004"]

blocked_tasks: []

notes:
  - "This is DOCUMENTATION only - no code changes to scripts themselves"
  - "Current risk level: MEDIUM (protection is procedural, not technical)"
  - "Priority: HIGH (foundational best practice for repository replication)"
  - "Gap: Repository has NO GitHub branch protection configured (only procedural)"
  - "Impact: Prevents accidental corruption of main/develop branches"
  - "Token savings: N/A (documentation feature)"
  - "Related: initialize-repository skill will gain GitHub setup steps"

research_findings:
  current_state:
    - "Branch protection is IMPLICIT through workflow patterns"
    - "No .github/ directory exists"
    - "No GitHub branch protection rules configured"
    - "No pre-push hooks active"
    - "All scripts follow good practices (no main commits except initialize)"
    - "One undocumented exception: backmerge_release.py commits to develop"

  files_mentioning_protection:
    - "WORKFLOW.md:1644-1647 - 'Main only updated via merged PRs'"
    - "CLAUDE.md:287-290 - 'Main branch protection' section (4 lines)"
    - "CONTRIBUTING.md:474 - 'Push fixes as new commits (don't force push)'"

  files_needing_updates:
    - "WORKFLOW.md - Add 'Branch Protection Policy' section"
    - "CLAUDE.md - Expand protection documentation"
    - "CONTRIBUTING.md - Add 'Protected Branches' section"
    - "README.md - Add quick reference"
    - "git-workflow-manager/SKILL.md - Add policy"
    - "initialize-repository/SKILL.md - Add GitHub setup"

  scripts_interacting_with_main_develop:
    - "initialize_repository.py - Commits to main (one-time setup only)"
    - "tag_release.py - Checks out main to tag (read + tag operation)"
    - "backmerge_release.py - Commits to develop (documented exception)"
    - "daily_rebase.py - Rebases onto develop (read-only)"

expected_outcomes:
  - "Explicit 'never delete, never commit directly' statement in 6 files"
  - "GitHub setup guide for branch protection rules"
  - "Pre-push hook template to prevent accidents"
  - "Documented exception for backmerge_release.py"
  - "Tests to verify script compliance"
  - "Foundation for future CI/CD enforcement"

version_impact:
  type: "MINOR"
  rationale: "New feature (comprehensive branch protection documentation)"
  current_version: "v1.5.1"
  expected_version: "v1.6.0"

---

# TODO: Branch Protection Documentation

**Status:** In Progress
**Phase:** 2 (Implementation)
**Current Step:** 2.1 (Create TODO file)

## Overview

Document that `main` and `develop` are **protected branches** with explicit rules:

1. **Never delete** main or develop
2. **Never commit directly** to main or develop
3. **Only merge via pull requests**

**Current State:** Branch protection is IMPLICIT (workflow patterns) but not EXPLICIT (documented policy)

**Risk:** New contributors could accidentally commit/delete protected branches

**Solution:** Comprehensive documentation across 6 core files + GitHub setup guide + safety hooks

---

## Research Summary

### What We Found

**Strengths:**
- ✅ Clear branch hierarchy diagram
- ✅ Consistent PR-based workflow patterns
- ✅ Worktree isolation prevents accidents
- ✅ Scripts follow good practices

**Gaps:**
- ❌ No explicit "never delete/commit" statement
- ❌ No GitHub branch protection setup guide
- ❌ No pre-push hooks
- ❌ Undocumented exception (backmerge_release.py)

**Current Protection Mechanism:** Procedural discipline (not technical enforcement)

---

## Implementation Plan

### Phase 1: Core Documentation (6 files)

1. **WORKFLOW.md** - Add "Branch Protection Policy" section
2. **CLAUDE.md** - Expand Git Branch Structure section
3. **CONTRIBUTING.md** - Add "Protected Branches" to Development Workflow
4. **README.md** - Add quick reference
5. **git-workflow-manager/SKILL.md** - Add protected branch policy
6. **initialize-repository/SKILL.md** - Add GitHub setup steps

### Phase 2: GitHub Setup Guide

7. **.github/BRANCH_PROTECTION.md** - Step-by-step configuration guide
8. **.github/README.md** - Explain directory purpose

### Phase 3: Safety Hooks (Optional)

9. **.git-hooks/pre-push** - Template to prevent accidental direct pushes
10. **WORKFLOW.md Phase 0** - Document hook installation

### Phase 4: Exception Documentation

11. **backmerge_release.py** - Add warning comment
12. **WORKFLOW.md + git-workflow-manager** - Document exception

### Phase 5: Testing & Quality

13. **test_branch_protection.py** - Verify script compliance
14. **quality-enforcer** - Add branch protection validation
15. **CHANGELOG.md** - Document changes
16. **Semantic versioning** - Calculate v1.6.0

### Phase 6: Workflow Management

17. **Register in TODO.md** - Add to active workflows

---

## Task Progress

**Total Tasks:** 21
**Completed:** 0
**In Progress:** 1 (Creating TODO file)
**Blocked:** 0

### Documentation (6 tasks)
- [ ] doc_001 - WORKFLOW.md (HIGH, 30min)
- [ ] doc_002 - CLAUDE.md (HIGH, 15min)
- [ ] doc_003 - CONTRIBUTING.md (HIGH, 20min)
- [ ] doc_004 - README.md (MEDIUM, 10min)
- [ ] doc_005 - git-workflow-manager/SKILL.md (HIGH, 20min)
- [ ] doc_006 - initialize-repository/SKILL.md (HIGH, 25min)

### GitHub Setup (2 tasks)
- [ ] github_001 - BRANCH_PROTECTION.md guide (HIGH, 30min)
- [ ] github_002 - .github/ directory (MEDIUM, 5min)

### Safety Hooks (2 tasks)
- [ ] hook_001 - pre-push template (MEDIUM, 20min)
- [ ] hook_002 - Document installation (MEDIUM, 15min)

### Exception Documentation (2 tasks)
- [ ] except_001 - Document backmerge exception (HIGH, 20min)
- [ ] except_002 - Add warning to script (MEDIUM, 10min)

### Testing (2 tasks)
- [ ] test_001 - test_branch_protection.py (MEDIUM, 30min)
- [ ] test_002 - Add to quality-enforcer (LOW, 20min)

### Quality (5 tasks)
- [ ] quality_001 - Run tests with coverage (HIGH, 5min)
- [ ] quality_002 - Validate versions (HIGH, 5min)
- [ ] quality_003 - Verify cross-references (MEDIUM, 15min)
- [ ] quality_004 - Update CHANGELOG (HIGH, 10min)
- [ ] quality_005 - Calculate semantic version (HIGH, 5min)

### Workflow Management (1 task)
- [ ] workflow_001 - Register in TODO.md (HIGH, 5min)

---

## Key Decisions

### 1. Protection Mechanism: Documentation First, Technical Later

**Decision:** Start with comprehensive documentation, add technical enforcement (GitHub rules, hooks) as optional

**Rationale:**
- Current risk is MEDIUM (not critical)
- Documentation provides immediate value
- Technical enforcement requires GitHub admin access
- Pre-push hooks are optional (can bypass if needed)

### 2. Document Exception: backmerge_release.py

**Decision:** Explicitly document that backmerge_release.py commits to develop (only exception)

**Rationale:**
- Current behavior is correct (back-merges are safe)
- Undocumented exception creates confusion
- Transparency prevents copy-paste errors

### 3. No Code Changes to Scripts

**Decision:** Documentation only, no changes to script behavior

**Rationale:**
- Scripts already follow best practices
- Only backmerge_release.py commits to develop (intentional)
- No bugs to fix, only documentation gaps

---

## Success Criteria

✅ **Documentation:**
- [ ] "Branch Protection Policy" section in WORKFLOW.md
- [ ] Explicit rules in CLAUDE.md, CONTRIBUTING.md, README.md
- [ ] All 6 core files updated consistently
- [ ] Cross-references accurate

✅ **GitHub Setup:**
- [ ] .github/BRANCH_PROTECTION.md guide created
- [ ] Step-by-step configuration instructions
- [ ] Screenshots or clear text instructions

✅ **Safety:**
- [ ] Pre-push hook template created
- [ ] Installation documented in WORKFLOW.md Phase 0
- [ ] Explains how to test and bypass if needed

✅ **Exception:**
- [ ] backmerge_release.py exception documented in 3 places
- [ ] Warning comment added to script
- [ ] Explains why it's safe

✅ **Testing:**
- [ ] test_branch_protection.py verifies script compliance
- [ ] Quality gate checks for violations
- [ ] All tests passing with ≥80% coverage

✅ **Quality:**
- [ ] CHANGELOG.md updated
- [ ] Version validation passes
- [ ] Semantic version = v1.6.0 (MINOR)

✅ **Workflow:**
- [ ] Registered in TODO.md active workflows
- [ ] Ready for feature branch creation

---

## Timeline

**Estimated Total Time:** 4-5 hours

**Breakdown:**
- Documentation (6 tasks): ~2 hours
- GitHub setup (2 tasks): ~35 minutes
- Safety hooks (2 tasks): ~35 minutes
- Exception docs (2 tasks): ~30 minutes
- Testing (2 tasks): ~50 minutes
- Quality (5 tasks): ~40 minutes
- Workflow mgmt (1 task): ~5 minutes

**Target Completion:** Same session (2025-11-04)

---

## Next Steps

1. ✅ Create this TODO file
2. ⏭️ Register in TODO.md (workflow_001)
3. ⏭️ Start documentation updates (doc_001-006)
4. ⏭️ Create GitHub setup guide (github_001-002)
5. ⏭️ Add safety hooks (hook_001-002)
6. ⏭️ Document exception (except_001-002)
7. ⏭️ Add tests (test_001-002)
8. ⏭️ Run quality gates (quality_001-005)

---

## Questions for User

None at this time. Plan is comprehensive and scope is clear.

---

## References

- **Research Report:** Comprehensive gap analysis completed
- **WORKFLOW.md:** Lines 79-92 (branch structure), 1644-1647 (main protection)
- **CLAUDE.md:** Lines 287-290 (main branch protection)
- **CONTRIBUTING.md:** Line 474 (no force push)
- **Affected Skills:** git-workflow-manager, initialize-repository
- **Exception Script:** .claude/skills/git-workflow-manager/scripts/backmerge_release.py

---

**Last Updated:** 2025-11-04T17:00:00Z
**Next Checkpoint:** After completing documentation updates (doc_001-006)
