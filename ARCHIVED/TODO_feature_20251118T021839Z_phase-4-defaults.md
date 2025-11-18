---
type: workflow-manifest
workflow_type: feature
slug: phase-4-defaults
timestamp: 20251118T021839Z
github_user: stharrold

workflow_progress:
  phase: 4
  current_step: "4.4"
  last_task: quality_001

quality_gates:
  test_coverage: 100
  tests_passing: true
  semantic_version: "1.13.0"

tasks:
  setup:
    - id: setup_001
      description: "Create TODO workflow file and register in TODO.md"
      status: completed
      started_at: "2025-11-18T02:18:39Z"
      completed_at: "2025-11-17T21:29:30Z"

  implementation:
    - id: impl_001
      description: "Implement default_synchronizations.sql with 7+ rules (4 normal flow + 3 error recovery)"
      status: completed
      started_at: "2025-11-17T20:00:00Z"
      completed_at: "2025-11-17T21:00:00Z"
    - id: impl_002
      description: "Create test script to validate SQL insertion"
      status: completed
      started_at: "2025-11-17T21:00:00Z"
      completed_at: "2025-11-17T21:15:00Z"
    - id: impl_003
      description: "Document rule design rationale"
      status: completed
      started_at: "2025-11-17T21:15:00Z"
      completed_at: "2025-11-17T21:25:00Z"

  quality:
    - id: quality_001
      description: "Run quality gates (≥80% coverage, tests passing)"
      status: completed
      started_at: "2025-11-17T21:25:00Z"
      completed_at: "2025-11-17T21:29:30Z"

  integration:
    - id: integration_001
      description: "Create PR: contrib/stharrold → develop"
      status: completed
      started_at: "2025-11-17T21:29:30Z"
      completed_at: "2025-11-17T21:35:00Z"
---

# TODO: Phase 4 Default Synchronization Rules Implementation

**Issue:** #162
**Branch:** contrib/stharrold
**Workflow Type:** feature
**Created:** 2025-11-18T02:18:39Z

## Objective

Define default synchronization rules for documented 4-tier workflow (Orchestrate → Develop → Assess → Research).

## Dependencies

- ✅ Phase 2 (#160): Synchronization Engine (completed in v1.11.0)
- ✅ Phase 3 (#161): Integration Layer (completed in v1.12.0)

## Deliverables

- [x] `.claude/skills/agentdb-state-manager/templates/default_synchronizations.sql`
  - 4 normal flow synchronizations (tier-to-tier handoffs)
  - 3+ error recovery synchronizations (failures → recovery)
  - Priority ordering (errors > normal flow)
  - Documentation in SQL comments
- [x] Rule testing script: validate all rules insertable
- [x] Documentation of rule design rationale

## Progress Tracking

### Setup (Phase 2.1)
- [x] Create TODO workflow file
- [x] Register in TODO.md manifest

### Implementation (Phase 2.4)
- [x] Create templates/ directory
- [x] Implement 4 normal flow rules
- [x] Implement 3+ error recovery rules
- [x] Add SQL documentation comments

### Testing (Phase 3)
- [x] Create test_default_syncs.py
- [x] Validate SQL insertion
- [x] Validate JSONPath syntax
- [x] Run quality gates

### Integration (Phase 4)
- [x] Create PR to develop
- [x] Address review feedback
- [x] Merge PR

## 4-Tier Workflow Overview

```
┌──────────────┐
│ Orchestrate  │  Planning phase (BMAD)
│   Agent      │
└──────┬───────┘
       │ planning_complete
       ▼
┌──────────────┐
│   Develop    │  Implementation phase (code + tests)
│   Agent      │
└──────┬───────┘
       │ commit_complete
       ▼
┌──────────────┐
│   Assess     │  Quality validation (coverage, tests)
│   Agent      │
└──────┬───────┘
       │ assessment_complete
       ▼
┌──────────────┐
│  Research    │  Documentation generation
│   Agent      │
└──────────────┘
```

## Synchronization Rules to Implement

### Normal Flow Rules (4 total)

1. **Orchestrate → Develop**: Planning complete → Initialize worktree
2. **Develop → Assess**: Commit complete → Run test suite
3. **Assess → Research**: Assessment complete → Generate documentation
4. **Research → Orchestrate**: Documentation complete → Create PR

### Error Recovery Rules (3+ total)

5. **Test Failure → Add Tests**: Assessment failed → Add missing tests
6. **Lint Failure → Fix Linting**: Commit incomplete → Fix linting errors
7. **Coverage Gap → Identify Untested**: Coverage < 80% → Identify untested modules

## Rule Design Principles

- **Single Responsibility**: Each sync rule has ONE purpose
- **Explicit Error Handling**: Dedicated rules for each error type
- **Priority Ordering**: Errors (200) > Normal (100) > Background (1-99)
- **Minimize Cascading**: Avoid Rule A → Rule B → Rule C chains
- **Idempotency**: Same trigger state → same provenance hash → executes once

## Success Criteria

- [x] All rules insertable without SQL errors
- [x] Rule testing script validates each rule
- [x] Documentation explains each rule's purpose
- [x] Priority ordering prevents conflicts
- [x] Coverage of all 4 workflow tiers
- [x] Coverage of all documented error scenarios

## Estimated Effort

6-10 hours

## Notes

- DuckDB syntax required (no PostgreSQL-specific syntax)
- JSONPath validation required
- Healthcare compliance: All sync rules must preserve audit trail
