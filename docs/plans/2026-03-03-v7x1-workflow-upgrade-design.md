# Design: Upgrade to v7x1 Workflow

**Date:** 2026-03-03
**Status:** Approved
**Version:** v2.0.0 (major: workflow architecture change)

## Context

The german repo currently uses Workflow v5.3 with a 6-phase, document-driven development cycle powered by 9 skills (including BMAD planner, SpecKit author, and quality-enforcer). Experience has shown that Claude's built-in planning produces better results than the BMAD/SpecKit combination, making those skills unnecessary overhead.

The `stharrold-templates` repo (v8.7.0) provides a streamlined 4-step v7x1 workflow via the bundle distribution system (`apply_bundle.py`). This design migrates german to v7x1.

## Decision

Upgrade from v5.3 (6-phase, 9 skills) to v7x1 (4-step, 6 skills) using the `git` and `ci` bundles from stharrold-templates.

## What Changes

### Removed (archived)

| Component | Reason |
|-----------|--------|
| `bmad-planner` skill | Claude's planning replaces structured BMAD Q&A |
| `speckit-author` skill | Claude's planning replaces SpecKit specifications |
| `quality-enforcer` skill | Replaced by GitHub Actions CI (claude-code-review.yml, tests.yml) |
| `planning/` directory | BMAD output — historical reference only |
| `specs/` directory | SpecKit output — historical reference only |
| `UPDATE_CHECKLIST.md` | v5.3-specific skill update process |
| Tests for removed skills | Archive alongside their skills |

### Replaced by bundle

| Component | Action |
|-----------|--------|
| `git-workflow-manager` skill | Replaced by stharrold-templates v8.7.0 version |
| `workflow-orchestrator` skill | Replaced by stharrold-templates v8.7.0 version |
| `workflow-utilities` skill | Replaced by stharrold-templates v8.7.0 version |
| `WORKFLOW.md` | Replaced by v7x1 workflow docs |
| `CONTRIBUTING.md` | Replaced by stharrold-templates version |

### Added

| Component | Source |
|-----------|--------|
| `.claude/commands/workflow/v7x1_1-worktree.md` | git bundle |
| `.claude/commands/workflow/v7x1_2-integrate.md` | git bundle |
| `.claude/commands/workflow/v7x1_3-release.md` | git bundle |
| `.claude/commands/workflow/v7x1_4-backmerge.md` | git bundle |
| `.claude/commands/workflow/status.md` | git bundle |
| `.github/workflows/tests.yml` | ci bundle |
| `.github/workflows/claude-code-review.yml` | ci bundle |
| `.github/workflows/secrets-example.yml` | ci bundle |
| `Containerfile` | ci bundle |
| `podman-compose.yml` | ci bundle |

### Kept unchanged

| Component | Reason |
|-----------|--------|
| `tech-stack-adapter` skill | Still useful for project detection |
| `agentdb-state-manager` skill | MIT sync pattern (v1.15.0, production-approved) |
| `initialize-repository` skill | Bootstrap utility for new repos |
| `src/german/` | Domain code unaffected |
| `resources/` | Language content unaffected |
| `input/`, `output/` | Learning materials unaffected |
| `tests/` (domain tests) | test_models.py, test_vocabulary_*.py unaffected |
| Git branch structure | Same: main ← develop ← contrib ← feature |

### Modified

| File | Change |
|------|--------|
| `CLAUDE.md` | Full rewrite: remove v5.3 references, add v7x1 workflow |
| `CHANGELOG.md` | Add v2.0.0 entry |
| `TODO.md` | Note migration |
| `.gitignore` | Merge: append workflow patterns |
| `pyproject.toml` | Merge: add missing dev deps |

## Execution Plan

### Step 1: Dry run bundle application

```bash
python .tmp/stharrold-templates/scripts/apply_bundle.py \
  .tmp/stharrold-templates . --bundle git --bundle ci --dry-run
```

### Step 2: Apply bundles

```bash
python .tmp/stharrold-templates/scripts/apply_bundle.py \
  .tmp/stharrold-templates . --bundle git --bundle ci
```

### Step 3: Archive removed skills

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3 bmad-planner archived for v7x1 upgrade" \
  .claude/skills/bmad-planner

python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3 speckit-author archived for v7x1 upgrade" \
  .claude/skills/speckit-author

python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3 quality-enforcer archived for v7x1 upgrade" \
  .claude/skills/quality-enforcer
```

### Step 4: Archive historical directories

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3 BMAD planning output archived for v7x1 upgrade" \
  planning

python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3 SpecKit specs output archived for v7x1 upgrade" \
  specs
```

### Step 5: Archive removed skill tests

Archive test files for bmad-planner, speckit-author, quality-enforcer from tests/skills/.

### Step 6: Rewrite CLAUDE.md

Full rewrite keeping german-specific content (code architecture, language guidelines, branch structure) and replacing v5.3 workflow with v7x1.

### Step 7: Update CHANGELOG.md and TODO.md

Add v2.0.0 entry to CHANGELOG. Update TODO.md to note migration.

### Step 8: Review and commit

```bash
git diff
git add <specific files>
git commit
```

## Risks

| Risk | Mitigation |
|------|------------|
| Bundle overwrites customized skill files | Skills are template-owned; german's customizations are in CLAUDE.md (rewritten separately) |
| CI workflows may need german-specific adjustments | Review tests.yml and claude-code-review.yml after apply |
| Containerfile/podman-compose.yml may conflict | Review diff; german has specific container needs |
| AgentDB tests reference removed skills | Archive only tests for removed skills; AgentDB tests stay |
| deprecate_files.py may have been replaced by bundle | Run archival before bundle if needed, or manually zip |

## Success Criteria

- [ ] `/workflow:v7x1_1-worktree "test"` creates a worktree correctly
- [ ] `/workflow:v7x1_2-integrate` creates PRs correctly
- [ ] `/workflow:status` shows workflow state
- [ ] No references to BMAD/SpecKit/quality-enforcer in CLAUDE.md
- [ ] Removed skills archived in ARCHIVED/
- [ ] Domain tests still pass (`uv run pytest tests/test_models.py tests/test_vocabulary_*.py`)
- [ ] Git branch structure preserved
