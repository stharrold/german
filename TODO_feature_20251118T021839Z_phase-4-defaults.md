---
type: workflow-manifest
workflow_type: feature
slug: phase-4-defaults
timestamp: 20251118T021839Z
github_user: stharrold

workflow_progress:
  phase: 2
  current_step: "2.1"
  last_task: setup_001

quality_gates:
  test_coverage: null
  tests_passing: null
  semantic_version: null

tasks:
  setup:
    - id: setup_001
      description: "Create TODO workflow file and register in TODO.md"
      status: in_progress
      started_at: "2025-11-18T02:18:39Z"
      completed_at: null

  implementation:
    - id: impl_001
      description: "Implement default_synchronizations.sql with 7+ rules (4 normal flow + 3 error recovery)"
      status: pending
      started_at: null
      completed_at: null
    - id: impl_002
      description: "Create test script to validate SQL insertion"
      status: pending
      started_at: null
      completed_at: null
    - id: impl_003
      description: "Document rule design rationale"
      status: pending
      started_at: null
      completed_at: null

  quality:
    - id: quality_001
      description: "Run quality gates (≥80% coverage, tests passing)"
      status: pending
      started_at: null
      completed_at: null

  integration:
    - id: integration_001
      description: "Create PR: contrib/stharrold → develop"
      status: pending
      started_at: null
      completed_at: null
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

- [ ] `.claude/skills/agentdb-state-manager/templates/default_synchronizations.sql`
  - 4 normal flow synchronizations (tier-to-tier handoffs)
  - 3+ error recovery synchronizations (failures → recovery)
  - Priority ordering (errors > normal flow)
  - Documentation in SQL comments
- [ ] Rule testing script: validate all rules insertable
- [ ] Documentation of rule design rationale

## Progress Tracking

### Setup (Phase 2.1)
- [x] Create TODO workflow file
- [ ] Register in TODO.md manifest

### Implementation (Phase 2.4)
- [ ] Create templates/ directory
- [ ] Implement 4 normal flow rules
- [ ] Implement 3+ error recovery rules
- [ ] Add SQL documentation comments

### Testing (Phase 3)
- [ ] Create test_default_syncs.py
- [ ] Validate SQL insertion
- [ ] Validate JSONPath syntax
- [ ] Run quality gates

### Integration (Phase 4)
- [ ] Create PR to develop
- [ ] Address review feedback
- [ ] Merge PR

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

- [ ] All rules insertable without SQL errors
- [ ] Rule testing script validates each rule
- [ ] Documentation explains each rule's purpose
- [ ] Priority ordering prevents conflicts
- [ ] Coverage of all 4 workflow tiers
- [ ] Coverage of all documented error scenarios

## Estimated Effort

6-10 hours

## Notes

- DuckDB syntax required (no PostgreSQL-specific syntax)
- JSONPath validation required
- Healthcare compliance: All sync rules must preserve audit trail
