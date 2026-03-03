# v7x1 Workflow Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate german repo from Workflow v5.3 (6-phase, 9 skills) to v7x1 (4-step, 6 skills) using stharrold-templates bundles.

**Architecture:** Apply `git` and `ci` bundles from `.tmp/stharrold-templates` to replace 3 skills and add v7x1 slash commands + GitHub Actions. Archive 3 removed skills (bmad-planner, speckit-author, quality-enforcer) and their historical output directories. Full CLAUDE.md rewrite.

**Tech Stack:** Python 3.11+, uv, git, apply_bundle.py, deprecate_files.py

---

### Task 1: Archive removed skills

Archive bmad-planner, speckit-author, and quality-enforcer before the bundle replaces workflow-utilities (which contains the archival script).

**Files:**
- Archive: `.claude/skills/bmad-planner/` → `ARCHIVED/`
- Archive: `.claude/skills/speckit-author/` → `ARCHIVED/`
- Archive: `.claude/skills/quality-enforcer/` → `ARCHIVED/`

**Step 1: Archive bmad-planner**

Run:
```bash
cd /Users/stharrold/Documents/GitHub/german
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3-bmad-planner" .claude/skills/bmad-planner
```

If the script fails (it expects a TODO_feature_* filename), fall back to manual archival:
```bash
cd /Users/stharrold/Documents/GitHub/german
mkdir -p ARCHIVED
zip -r ARCHIVED/20260303T000000Z_v5.3-bmad-planner.zip .claude/skills/bmad-planner/
rm -rf .claude/skills/bmad-planner/
```

**Step 2: Archive speckit-author**

Run:
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3-speckit-author" .claude/skills/speckit-author
```

Fallback:
```bash
zip -r ARCHIVED/20260303T000000Z_v5.3-speckit-author.zip .claude/skills/speckit-author/
rm -rf .claude/skills/speckit-author/
```

**Step 3: Archive quality-enforcer**

Run:
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO.md "v5.3-quality-enforcer" .claude/skills/quality-enforcer
```

Fallback:
```bash
zip -r ARCHIVED/20260303T000000Z_v5.3-quality-enforcer.zip .claude/skills/quality-enforcer/
rm -rf .claude/skills/quality-enforcer/
```

**Step 4: Verify archives exist**

Run:
```bash
ls -la ARCHIVED/*.zip | grep v5.3
ls .claude/skills/ | sort
```

Expected: 3 zip files in ARCHIVED/. Skills directory should NOT contain bmad-planner, speckit-author, or quality-enforcer.

---

### Task 2: Archive historical directories

Archive planning/ and specs/ directories (BMAD/SpecKit output, historical reference only).

**Files:**
- Archive: `planning/` → `ARCHIVED/`
- Archive: `specs/` → `ARCHIVED/`

**Step 1: Archive planning/**

```bash
cd /Users/stharrold/Documents/GitHub/german
zip -r ARCHIVED/20260303T000000Z_v5.3-planning.zip planning/
rm -rf planning/
```

**Step 2: Archive specs/**

```bash
zip -r ARCHIVED/20260303T000000Z_v5.3-specs.zip specs/
rm -rf specs/
```

**Step 3: Archive UPDATE_CHECKLIST.md**

```bash
zip -r ARCHIVED/20260303T000000Z_v5.3-update-checklist.zip .claude/skills/UPDATE_CHECKLIST.md
rm -f .claude/skills/UPDATE_CHECKLIST.md
```

**Step 4: Verify**

```bash
ls ARCHIVED/*v5.3*.zip
test ! -d planning && echo "planning/ removed" || echo "ERROR: planning/ still exists"
test ! -d specs && echo "specs/ removed" || echo "ERROR: specs/ still exists"
```

---

### Task 3: Apply git + ci bundles

Apply the stharrold-templates bundles to install v7x1 workflow.

**Files:**
- Replace: `.claude/skills/git-workflow-manager/`
- Replace: `.claude/skills/workflow-orchestrator/`
- Replace: `.claude/skills/workflow-utilities/`
- Create: `.claude/commands/workflow/` (5 command files)
- Replace: `WORKFLOW.md`
- Replace: `CONTRIBUTING.md`
- Merge: `.gitignore`
- Replace: `.github/workflows/tests.yml`
- Create: `.github/workflows/claude-code-review.yml`
- Create: `.github/workflows/secrets-example.yml`
- Create: `Containerfile`
- Create: `podman-compose.yml`
- Create: `.pre-commit-config.yaml`
- Merge: `pyproject.toml`

**Step 1: Apply bundles**

```bash
cd /Users/stharrold/Documents/GitHub/german
python .tmp/stharrold-templates/scripts/apply_bundle.py \
  .tmp/stharrold-templates . --bundle git --bundle ci
```

Expected output:
```
Applying bundle: git
  REPLACE .claude/skills/git-workflow-manager/
  REPLACE .claude/skills/workflow-orchestrator/
  REPLACE .claude/skills/workflow-utilities/
  COPY .claude/commands/workflow/
  REPLACE WORKFLOW.md
  REPLACE CONTRIBUTING.md
  MERGE .gitignore (N patterns added)
Applied: git (7 items)

Applying bundle: ci
  REPLACE .github/workflows/tests.yml
  COPY .github/workflows/claude-code-review.yml
  COPY .github/workflows/secrets-example.yml
  COPY Containerfile
  COPY podman-compose.yml
  COPY .pre-commit-config.yaml
  MERGE pyproject.toml (N deps added)
Applied: ci (7 items)
```

**Step 2: Verify slash commands installed**

```bash
ls .claude/commands/workflow/
```

Expected: `v7x1_1-worktree.md  v7x1_2-integrate.md  v7x1_3-release.md  v7x1_4-backmerge.md  status.md`

**Step 3: Verify skills replaced**

```bash
ls .claude/skills/ | sort
```

Expected: `agentdb-state-manager  git-workflow-manager  initialize-repository  tech-stack-adapter  workflow-orchestrator  workflow-utilities  __init__.py`

(6 skills + __init__.py, NO bmad-planner, speckit-author, quality-enforcer)

**Step 4: Review CI workflows**

Read `.github/workflows/tests.yml` and `.github/workflows/claude-code-review.yml` to verify they are compatible with german's setup. The tests.yml may need adjustment for:
- Branch triggers (main, develop)
- Python version (3.11)
- Coverage threshold (may not have --cov-fail-under since quality-enforcer is removed)

If tests.yml removes coverage enforcement, that is expected (quality gates now handled by Claude Code Review action).

**Step 5: Review Containerfile and podman-compose.yml**

Read both files. If they reference stharrold-templates-specific paths or services, adjust for german's layout (src/german/, resources/, etc.).

---

### Task 4: Review and fix bundle artifacts

Review files installed by bundles and fix any stharrold-templates-specific references.

**Files:**
- Modify: `.github/workflows/tests.yml` (if needed)
- Modify: `.github/workflows/claude-code-review.yml` (if needed)
- Modify: `Containerfile` (if needed)
- Modify: `podman-compose.yml` (if needed)
- Modify: `.pre-commit-config.yaml` (if needed)

**Step 1: Check tests.yml references**

Read `.github/workflows/tests.yml`. Ensure:
- Triggers on `main` and `develop` branches
- Uses Python 3.11
- Runs `uv sync --frozen`
- Runs `uv run pytest` (coverage optional since quality-enforcer removed)
- Runs `uv run ruff check .`

If the file references stharrold-templates paths, fix them.

**Step 2: Check claude-code-review.yml**

Read `.github/workflows/claude-code-review.yml`. Important gotchas from stharrold-templates CLAUDE.md:
- Requires `claude_args: "--allowedTools Bash,WebFetch,WebSearch,Skill,Task"` (not `allowed_tools`)
- Requires `id-token: write` (for OIDC auth)
- Requires `fetch-depth: 0`
- Changes require reaching `main` before OIDC validates them

No changes needed on first install — just review for compatibility.

**Step 3: Check Containerfile**

Read `Containerfile`. If it references `stharrold-templates` or paths not in german, adjust to use `src/german/`.

**Step 4: Check podman-compose.yml**

Read `podman-compose.yml`. Adjust service names and volume mounts if they reference stharrold-templates paths.

**Step 5: Check .pre-commit-config.yaml**

Read `.pre-commit-config.yaml`. Note the SPDX header enforcement mentioned in stharrold-templates gotchas. Decide whether to keep or adjust.

---

### Task 5: Rewrite CLAUDE.md

Full rewrite removing all v5.3 references and adding v7x1 workflow.

**Files:**
- Modify: `CLAUDE.md` (full rewrite)

**Step 1: Write new CLAUDE.md**

The new CLAUDE.md should contain these sections (in order):

```markdown
---
type: claude-context
directory: .
purpose: Context-specific guidance for german
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - benchmarks/CLAUDE.md
  - docs/CLAUDE.md
  - resources/CLAUDE.md
  - src/CLAUDE.md
  - tests/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---

# CLAUDE.md

## Status

Workflow v7x1 upgrade complete (v2.0.0).
- v5.3 skills (bmad-planner, speckit-author, quality-enforcer) archived
- v7x1 slash commands installed
- CI: GitHub Actions (tests.yml, claude-code-review.yml)
- pyproject.toml version: 2.0.0

## Repository Purpose

Python-based German language learning resources and content:
- German vocabulary (nouns, verbs, adjectives) with Pydantic validation
- B1-level listening comprehension topics (20 topics, bilingual format)
- Certificate guides for CEFR levels (A1-C2)
- Python tools for loading and querying vocabulary data

## Gotchas

[Adapted from stharrold-templates CLAUDE.md - keep relevant items:]
- `.claude/settings.local.json` is gitignored — do not commit
- `release_workflow.py create-release` auto-calculates version from last git tag — override manually for major bumps
- Ruff auto-fixes import ordering on commit — re-stage if pre-commit hook modifies files
- `backmerge_workflow.py cleanup-release` only prints instructions — run cleanup commands manually
- Backmerge: always try `backmerge_workflow.py pr-develop` (release → develop) first — only fall back to PR `main` → `develop` if "No commits between"
- `claude-code-review.yml` requires `claude_args`, `id-token: write`, and `fetch-depth: 0`
- `uv run` modifies `uv.lock` when `pyproject.toml` version changes — commit `uv.lock` after version bumps
- Git worktrees use a `.git` file (not directory) — use `.exists()` not `.is_dir()`
- All nouns MUST have gender (der/die/das) — enforced by Pydantic `@model_validator`
- JSON vocabulary files MUST be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- VCS supports GitHub (`gh`) and Azure DevOps (`az`) — auto-detected from remote URL

## Branch Structure

`main` ← `develop` ← `contrib/stharrold` ← `feature/*`

Protected branches: `main` and `develop` (PR-only, no direct commits).

## v7x1 Workflow

```
/workflow:v7x1_1-worktree "feature description"  → creates worktree
    Implementation in worktree with Claude Code
/workflow:v7x1_2-integrate "feature/branch"       → PR feature→contrib→develop
/workflow:v7x1_3-release [version]                 → release→main, tag
/workflow:v7x1_4-backmerge                         → release→develop, rebase contrib
```

See `WORKFLOW.md` for full details.

## Commands

```bash
uv run pytest                              # All tests
uv run ruff check .                        # Lint
uv run pre-commit run --all-files          # Pre-commit hooks
```

## Code Architecture

```
src/german/
├── __init__.py
├── models.py             # Pydantic: VocabularyWord, Gender, PartOfSpeech
└── vocabulary/
    ├── loader.py          # JSON → VocabularyWord objects (UTF-8)
    └── query.py           # Filter by POS, gender, lookup

resources/vocabulary/
├── nouns.json             # German nouns with gender, plural
├── verbs.json             # German verbs
└── adjectives.json        # German adjectives
```

Data flow: `JSON → loader.py → VocabularyWord (Pydantic) → query.py → Application`

## German Language Content Guidelines

- Nouns have grammatical gender (der/die/das) — always include
- Verbs may have separable prefixes — track this attribute
- Vocabulary schema: `{"words": [{"german": "...", "english": "...", "part_of_speech": "...", "gender": "..."}]}`
- B1 listening format: `<German> . <English> . <German> . <English> .`
- Validate umlauts (ä, ö, ü) and eszett (ß) encoding (UTF-8)

## Skills (6)

| Skill | Purpose |
|-------|---------|
| git-workflow-manager | Worktrees, PRs, semantic versioning, releases |
| workflow-orchestrator | Workflow coordination |
| workflow-utilities | Shared utilities, deprecation, VCS abstraction |
| tech-stack-adapter | Python/uv project detection |
| agentdb-state-manager | DuckDB analytics, state tracking |
| initialize-repository | Bootstrap workflow in new repos |

## Version History

- **v2.0.0** (2026-03-03): Workflow v7x1 upgrade (BREAKING: removed BMAD/SpecKit/quality-enforcer)
- **v1.15.1** (2025-11-18): CLAUDE.md improvements, worktree cleanup guide
- **v1.15.0** (2025-11-18): MIT Agent Sync Pattern complete (all 6 phases)

See [CHANGELOG.md](CHANGELOG.md) for full history.

## Related Documentation

- **[README.md](README.md)** - Human-readable project documentation
- **[WORKFLOW.md](WORKFLOW.md)** - v7x1 workflow guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
```

**Step 2: Verify no stale references**

```bash
grep -r "bmad-planner\|speckit-author\|quality-enforcer\|v5\.3\|Phase 1.*BMAD\|Phase 2.*SpecKit" CLAUDE.md
```

Expected: No matches.

---

### Task 6: Update CHANGELOG.md

Add v2.0.0 entry documenting the workflow upgrade.

**Files:**
- Modify: `CHANGELOG.md`

**Step 1: Add v2.0.0 entry**

Insert after `## [Unreleased]` line:

```markdown
## [2.0.0] - 2026-03-03

### Changed
- **BREAKING: Workflow upgraded from v5.3 to v7x1** - 6-phase document-driven workflow replaced with 4-step autonomous workflow
  - Removed bmad-planner skill (Claude's planning replaces BMAD Q&A)
  - Removed speckit-author skill (Claude's planning replaces SpecKit specifications)
  - Removed quality-enforcer skill (GitHub Actions CI replaces manual quality gates)
  - Replaced git-workflow-manager, workflow-orchestrator, workflow-utilities with stharrold-templates v8.7.0 versions
  - Added v7x1 slash commands: `/workflow:v7x1_1-worktree`, `/workflow:v7x1_2-integrate`, `/workflow:v7x1_3-release`, `/workflow:v7x1_4-backmerge`

### Added
- `.claude/commands/workflow/` - v7x1 slash commands (5 files)
- `.github/workflows/claude-code-review.yml` - Automated Claude Code review
- `.github/workflows/secrets-example.yml` - Secrets workflow example
- `Containerfile` - Container definition
- `podman-compose.yml` - Container orchestration
- `.pre-commit-config.yaml` - Pre-commit hooks

### Removed
- `planning/` directory (archived)
- `specs/` directory (archived)
- `.claude/skills/bmad-planner/` (archived)
- `.claude/skills/speckit-author/` (archived)
- `.claude/skills/quality-enforcer/` (archived)
- `.claude/skills/UPDATE_CHECKLIST.md` (archived)
```

---

### Task 7: Update TODO.md and pyproject.toml version

Update manifest and project version.

**Files:**
- Modify: `TODO.md` (update version field)
- Modify: `pyproject.toml` (update version to 2.0.0)

**Step 1: Update TODO.md version**

Change `version: 5.0.0` to `version: 7.0.0` in the YAML frontmatter.

**Step 2: Update pyproject.toml version**

Change `version = "1.15.1"` (or current) to `version = "2.0.0"`.

**Step 3: Update CLAUDE.md frontmatter**

Remove children references to archived directories (planning/CLAUDE.md, specs/CLAUDE.md).

---

### Task 8: Clean up stale references

Find and fix any remaining references to removed skills across the codebase.

**Files:**
- Scan: All `.md` files for stale references

**Step 1: Search for stale references**

```bash
grep -r "bmad-planner\|speckit-author\|quality-enforcer\|v5\.3\|Phase 1.*BMAD\|Phase 2.*SpecKit\|create_planning\|create_specifications\|run_quality_gates\|update_asbuilt" \
  --include="*.md" --include="*.py" \
  --exclude-dir=ARCHIVED --exclude-dir=.tmp --exclude-dir=.git \
  .
```

**Step 2: Fix any found references**

For each match:
- If in a kept file (CLAUDE.md, README.md, etc.): update or remove the reference
- If in a test file: verify it's testing kept functionality
- If in a skill file: verify the bundle replacement doesn't reference removed skills

**Step 3: Search for stale WORKFLOW-INIT-PROMPT.md**

```bash
test -f WORKFLOW-INIT-PROMPT.md && echo "EXISTS - review for v7x1 compatibility" || echo "not found"
```

If exists, archive it (it was a v5.3 navigation guide).

---

### Task 9: Run domain tests

Verify nothing broke in the actual German language code.

**Files:**
- Test: `tests/test_models.py`
- Test: `tests/test_vocabulary_loader.py`
- Test: `tests/test_vocabulary_query.py`

**Step 1: Run domain tests**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run pytest tests/test_models.py tests/test_vocabulary_loader.py tests/test_vocabulary_query.py -v
```

Expected: All tests pass.

**Step 2: Run full test suite**

```bash
uv run pytest -v
```

Note: Some skill tests may fail if they reference scripts/imports that changed in the bundle replacement. This is expected — those tests test the OLD skill versions. Document any failures.

**Step 3: Run linting**

```bash
uv run ruff check .
```

Fix any linting issues in modified files.

---

### Task 10: Review all changes and commit

Review the complete diff and create a single commit.

**Step 1: Review diff**

```bash
git diff --stat
git diff
```

**Step 2: Stage specific files**

```bash
git add \
  ARCHIVED/ \
  .claude/commands/ \
  .claude/skills/ \
  .github/workflows/ \
  CLAUDE.md \
  CHANGELOG.md \
  CONTRIBUTING.md \
  WORKFLOW.md \
  TODO.md \
  pyproject.toml \
  .gitignore \
  Containerfile \
  podman-compose.yml \
  .pre-commit-config.yaml \
  docs/plans/
```

Also stage any deleted files (planning/, specs/):
```bash
git add -u planning/ specs/
```

**Step 3: Commit**

```bash
git commit -m "feat!: upgrade workflow from v5.3 to v7x1

BREAKING CHANGE: Replaced 6-phase document-driven workflow with 4-step
autonomous v7x1 workflow from stharrold-templates v8.7.0.

- Removed: bmad-planner, speckit-author, quality-enforcer (archived)
- Removed: planning/, specs/ directories (archived)
- Replaced: git-workflow-manager, workflow-orchestrator, workflow-utilities
- Added: v7x1 slash commands, GitHub Actions CI, Containerfile, pre-commit
- Rewritten: CLAUDE.md for v7x1

Co-Authored-By: Claude <noreply@anthropic.com>"
```
