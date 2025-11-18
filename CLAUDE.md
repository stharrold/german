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
  - planning/CLAUDE.md
  - resources/CLAUDE.md
  - specs/CLAUDE.md
  - src/CLAUDE.md
  - tests/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Python-based repository for German language learning resources and content. It contains:
- German language reference materials (vocabulary, grammar, etc.)
- Python scripts and tools for language processing and learning
- Structured data for German language content
- **Workflow v5.3 skill-based architecture** for managing development workflow
- **Active Development:** MIT Agent Synchronization Pattern (Issues #158-#172)
  - Phase 1: Database Schema (✅ Completed in v1.10.0 - PRs #165, #173, #179 merged)
  - Phases 2-6: Ready for implementation (Issues #160-#164)
  - See Issue #158 for 6-phase implementation plan

## Quick Start for New Claude Instances

**First commands to run:**
```bash
# 1. Detect project stack (run once per session)
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# 2. Check current context
git status
cat TODO.md  # See active workflows

# 3. Start workflow
# Say: "next step?"
```

**Critical architecture concepts:**
- **Progressive skill loading**: Load 1-3 skills per phase (not all 9)
- **TODO files live in main repo**: Worktrees reference `../TODO_*.md`
- **Callable tools reduce tokens by 75-92%**: BMAD/SpecKit are interactive scripts
- **Context checkpoint at 100K tokens**: System auto-saves, you run `/init` then `/compact`

## Current Active Work

**MIT Agent Synchronization Pattern (Issue #158):**
- **Phase 1 (Issue #159): ✅ COMPLETED in v1.10.0**
  - Database schema implemented (agentdb_sync_schema.sql, 458 lines)
  - HIPAA/FDA/IRB-compliant audit trail design
  - Test suite with 557 test cases (test_schema_migration.py, 706 lines)
  - PRs #165, #173, #179 merged to main
  - All phase-1-schema issues resolved (including #167-172 closed in v1.10.1)
  - Post-release cleanup completed in v1.10.1

- **Phase 2 (Issue #160): ✅ COMPLETED in v1.11.0**
  - Synchronization engine implemented (sync_engine.py, 559 lines)
  - Declarative coordination with pattern matching and idempotency
  - SHA-256 content-addressed hashing for provenance tracking
  - Phase 2 database migration (phase2_migration.sql, 215 lines)
  - Comprehensive test suite (test_sync_engine.py, 689 lines, 22 tests)
  - Integration guide (phase2_integration_guide.md, 394 lines)
  - PR #198 merged to contrib, PR #202 merged to develop
  - v1.11.0 released and tagged

- **Phase 3 (Issue #161): ✅ COMPLETED in v1.12.0**
  - Integration layer implemented (worktree_agent_integration.py, 594 lines)
  - Agent hooks added to 3 existing scripts (bmad-planner, quality-enforcer, speckit-author)
  - FlowTokenManager, PHIDetector, ComplianceWrapper, SyncEngineFactory, trigger_sync_completion()
  - Test suite with 34 tests, 96% coverage (test_worktree_integration.py, 563 lines)
  - Feature flag control (SYNC_ENGINE_ENABLED, disabled by default)
  - Graceful degradation on errors
  - Non-invasive integration (<10 lines per agent script)
  - PR #217 merged to contrib, PR #226 merged to develop
  - v1.12.0 released and tagged
  - Linting fixes applied (Issues #218-#221 closed)

- **Phase 4 (Issue #162): ✅ COMPLETED** (pending v1.13.0 release)
  - Default synchronization rules implemented (default_synchronizations.sql, 456 lines)
  - 8 synchronization rules (4 normal flow + 4 error recovery)
  - Comprehensive test suite (test_default_syncs.py, 389 lines, 12 tests)
  - Design rationale documentation (phase4_default_rules_rationale.md, 700+ lines)
  - 4-tier workflow coverage (Orchestrate → Develop → Assess → Research)
  - Priority-based rule execution (200 for errors > 100 for normal flow)
  - PR #241 merged to contrib
  - 7 PR review issues resolved (Issues #242-248):
    - #242: Coverage range matching documentation (PR #250)
    - #243: TODO status updates (PR #254)
    - #244: Generic worktree paths (PR #253)
    - #245: Idempotent SQL loading (PR #251)
    - #246: Security validation docs (PR #249)
    - #247: Version clarity (PR #255)
    - #248: Test logic strengthening (PR #252)
  - All 7 PRs merged to contrib
  - Atomic cleanup script implemented (cleanup_feature.py)

**Next phases ready for implementation:**
- Phase 5 (Issue #163): Testing & Compliance (ready to start)
- Phase 6 (Issue #164): Performance & Docs (blocked by Phase 5)

Check for new work: `gh issue list --state open`

## Workflow Execution Flow

```
User: "next step?"
    ↓
workflow-orchestrator: Detect context
    ├─ Main repo + contrib branch → Phase 1 (BMAD planning)
    ├─ Feature worktree → Phase 2-3 (SpecKit + implementation)
    └─ PR merged → Phase 4 (PR feedback, archival)
    ↓
Load relevant skills (1-3, not all 9)
    ├─ Phase 1: tech-stack-adapter + bmad-planner
    ├─ Phase 2: speckit-author + git-workflow-manager
    ├─ Phase 3: quality-enforcer
    └─ Phase 4: git-workflow-manager + workflow-utilities
    ↓
Execute callable tool or perform operation
    ├─ BMAD: Interactive Q&A → planning/ files
    ├─ SpecKit: Auto-detect BMAD → specs/ files
    └─ Git ops: Create worktree, PR, merge
    ↓
Update TODO_*.md with progress
    ↓
Check context usage (checkpoint at 100K)
```

## Parallel Agent Execution Patterns

**When multiple independent issues exist, use parallel agents for efficiency.**

**Example: MIT Agent Synchronization Pattern (Issue #158)**

**Stage 1 (Sequential):** Issue #159 - Database Schema (8-12h)
- MUST complete first (foundational)
- Blocks all other phases

**Stage 2 (Parallel - 2 agents):** Issues #160 + #161 (12-16h parallel vs 22-30h sequential)
- Agent 1: #160 (Sync Engine) - creates `sync_engine.py`
- Agent 2: #161 (Integration Layer) - creates `worktree_agent_integration.py`
- Safe to parallelize: No file conflicts, different scopes
- Time savings: 40-47% reduction

**Stage 3 (Sequential):** Issue #162 - Default Rules (6-10h)
- Requires both #160 AND #161 complete
- Cannot parallelize

**Stage 4 (Parallel - 2 agents):** Issues #163 + #164 (14-18h parallel vs 26-34h sequential)
- Agent 1: #163 (Testing & Compliance)
- Agent 2: #164 (Performance & Docs)
- Safe to parallelize: Completely separate directories
- Time savings: 46-47% reduction

**Parallelization Decision Tree:**
1. Check dependencies: Do tasks depend on each other?
2. Check file conflicts: Do tasks modify same files?
3. Check scope: Are tasks truly independent?
4. If all clear: Execute in parallel for time savings

**Total time:** 40-56 hours parallel vs 62-86 hours sequential (35-47% faster)

## Code Architecture

**Package Structure:**
```
src/german/
├── __init__.py           # Package initialization
├── models.py             # Pydantic models: VocabularyWord, Gender, PartOfSpeech
└── vocabulary/
    ├── __init__.py
    ├── loader.py         # Load JSON vocabulary files → VocabularyWord objects
    └── query.py          # Query/filter vocabulary (by POS, gender, etc.)

resources/vocabulary/
├── nouns.json            # German nouns with gender, plural
├── verbs.json            # German verbs
└── adjectives.json       # German adjectives
```

**Data Flow:**
```
JSON files → loader.py → VocabularyWord (Pydantic) → query.py → Application
```

**German Language Constraints:**
- All nouns MUST have gender (der/die/das) - enforced by Pydantic `@model_validator`
- JSON files MUST be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- Vocabulary schema: `{"words": [{"german": "...", "english": "...", "part_of_speech": "...", "gender": "..."}]}`

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv (preferred) or pip
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees
- **Workflow System:** Skill-based architecture (9 specialized skills)
- **Containerization:** Podman + podman-compose

## Workflow v5.3 Architecture

This repository uses a **skill-based workflow system** located in `.claude/skills/`. The system provides progressive skill loading - only load what's needed for the current phase.

**Current workflow version:** 5.3.0

**Quick start:** See [WORKFLOW-INIT-PROMPT.md](WORKFLOW-INIT-PROMPT.md) for navigation guide to workflow system (DRY reference-based, ~500 tokens)

**Complete documentation:** See [WORKFLOW.md](WORKFLOW.md) for full 6-phase workflow guide (~4,000 tokens, 2000+ lines)

**Architecture deep-dive:** See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architectural analysis including:
- Token efficiency patterns (progressive loading saves 50%, callable tools save 75-92%)
- Skill integration patterns and when to use each skill
- Critical design decisions and rationale
- Complete constants reference with explanations

## Critical Pitfalls (Not Obvious from Individual Files)

**Branch Protection:**
- ❌ Never commit directly to `main` or `develop`
- ✅ All changes via PRs (self-merge enabled as of v1.8.1)
- Scripts validate branch before operations

**TODO Lifecycle:**
- ❌ Never delete TODO files directly
- ✅ Use `workflow_registrar.py` to add to TODO.md manifest
- ✅ Use `workflow_archiver.py` to move to ARCHIVED/ after completion
- ✅ TODO files must be committed to feature branches (part of PR)

**Context Management:**
- At 100K tokens: System auto-saves to TODO_*.md
- You must then: `/init` → `/compact` → continue
- Effective capacity: 136K tokens (200K total - 64K overhead)

**Worktree Pattern:**
- Main repo: Where TODO files live
- Worktrees: Reference `../TODO_*.md`
- After PR merge: Delete worktree + branch, archive TODO

**When to Use Which Skill:**
- Complex feature needing alignment → Use BMAD (Phase 1)
- Simple bug fix → Skip BMAD, use SpecKit standalone (Phase 2)
- Need dependency queries → Use AgentDB (89% token savings)
- Simple file read → Just read the file directly
- Need to resolve PR review feedback → Use `generate_work_items_from_pr.py` (Phase 4.3)
- Healthcare/medical project → Check HIPAA compliance requirements first
- Working with DuckDB → Verify syntax compatibility (no PostgreSQL-specific code)

### Available Skills (9 Total)

**Location:** `.claude/skills/<skill-name>/SKILL.md`

1. **workflow-orchestrator** - Main coordinator for workflow phases
2. **tech-stack-adapter** - Detects Python/uv project configuration
3. **git-workflow-manager** (v5.2.2) - Git operations, worktrees, semantic versioning, pre-PR rebase
4. **bmad-planner** - Creates BMAD planning documents (requirements, architecture)
5. **speckit-author** - Creates detailed specifications and implementation plans
6. **quality-enforcer** - Enforces quality gates (≥80% coverage, tests, linting)
7. **workflow-utilities** - Shared utilities for file management and TODO updates
8. **initialize-repository** - Meta-skill (Phase 0) for bootstrapping new repositories
9. **agentdb-state-manager** - AgentDB persistent state tracking and analytics

### Official Claude Code Documentation

This workflow system extends official Claude Code patterns. For official documentation:

**Claude Code Skills:**
- **Specification:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- **Building Agents:** https://docs.claude.com/en/docs/agents-and-tools/building-agents
- **Getting Started:** https://docs.claude.com/en/docs/claude-code/getting-started
- **Docs Map:** https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md

**Relationship to official patterns:** This workflow uses extended patterns (SKILL.md vs skill.md, additional files for context/versioning, phase-based coordination) optimized for multi-phase development. Both patterns are valid. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed comparison.

**When creating new skills:** Use `python .claude/skills/workflow-utilities/scripts/create_skill.py <skill-name>` - the script automatically fetches official docs, compares patterns, and alerts you to discrepancies with citations.

### Using the Workflow

**Start workflow:** Say **"next step?"**

The orchestrator will:
- Detect current context (main repo vs worktree, current branch)
- Load only relevant skills for current phase
- Prompt for confirmation before each action
- Update TODO file with progress
- Guide through: planning → specification → implementation → quality → PR

**Monitor context usage:** Run `/context` periodically. At 100K tokens, orchestrator saves state to TODO_*.md and prompts you to run `/init` (updates memory files) then `/compact` (compresses memory buffer).

### Workflow Phases (Bidirectional BMAD ↔ SpecKit Flow)

**Phase 1: Planning (BMAD - Callable Tool)** (main repo, `contrib/<gh-user>` branch)
- **Callable script:** `python .claude/skills/bmad-planner/scripts/create_planning.py`
- **Interactive Q&A:** 3 personas (Analyst, Architect, PM) gather requirements
- **Output:** planning/<feature>/ with requirements.md, architecture.md, epics.md
- **Skills:** bmad-planner (callable)
- **Token savings:** ~2,300 tokens per feature (92% reduction vs manual)

**Phase 2: Implementation (SpecKit - Callable Tool)** (feature worktree)
- **Call SpecKit script:** `python .claude/skills/speckit-author/scripts/create_specifications.py`
- **Script auto-detects** BMAD context from ../planning/<feature>/
- **Interactive Q&A:** 5-8 questions (with BMAD) or 10-15 (without)
- **Output:** specs/<feature>/ with spec.md, plan.md, TODO_*.md updated
- **Skills:** speckit-author (callable), git-workflow-manager
- **Token savings:** ~1,700-2,700 tokens per feature (vs manual reproduction)

**Phase 3: Quality** (feature worktree)
- Run quality gates (≥80% coverage, all tests passing)
- Calculate semantic version
- **Skills:** quality-enforcer

**Phase 4: Integration + Feedback** (9 steps)
- Create PR: feature → contrib/<gh-user>
- Reviewers add comments
- **Phase 4.3: PR Feedback Handling (Optional)**
  - Generate work-items from unresolved PR conversations
  - Decision tree: simple fixes (same branch) vs. substantive changes (work-items)
  - Each work-item follows Phase 2-4 workflow
  - Enables PR approval without blocking on follow-up work
- Approve and merge PR in GitHub/Azure DevOps UI
- Archive workflow and delete worktree
- **Update BMAD with as-built:** `python .claude/skills/speckit-author/scripts/update_asbuilt.py`
- Script analyzes deviations, gathers metrics, updates planning/
- Rebase contrib onto develop
- Create PR: contrib/<gh-user> → develop
- **Skills:** git-workflow-manager, speckit-author (update_asbuilt.py)

**Phase 5: Release** (main repo)
- Create release branch from develop
- Final QA and documentation
- Create PR: release/vX.Y.Z → main
- Tag release after merge
- Back-merge to develop
- Cleanup release branch
- **Skills:** git-workflow-manager, quality-enforcer
- **SpecKit:** Not used (packages existing features)

**Phase 6: Hotfix** (hotfix worktree from main)
- Create hotfix worktree from main (not contrib)
- **SpecKit optional:** Use only for complex fixes requiring planning
- Implement minimal fix (keep scope tight)
- Run quality gates (≥80% coverage required)
- Merge to main → tag → back-merge to develop
- **Skills:** git-workflow-manager, speckit-author (optional), quality-enforcer
- **Versioning:** vX.Y.Z-hotfix.N

### Key Workflow Features

**Interactive Planning (BMAD - Callable Tool):**
- **Run script:** `create_planning.py` in main repo on contrib branch
- 🧠 Analyst: Q&A for requirements (5-10 questions)
- 🏗️ Architect: Q&A for architecture (5-8 questions)
- 📋 PM: Automatic epic breakdown
- Generates requirements.md, architecture.md, epics.md from templates
- Commits changes automatically
- **Token savings:** ~2,300 tokens per feature (92% reduction)

**Interactive Specifications (SpecKit - Callable Tool):**
- **Run script:** `create_specifications.py` in feature/hotfix worktrees
- Auto-detects BMAD planning from Phase 1
- Adaptive Q&A: 5-8 questions (with BMAD) or 10-15 (without BMAD)
- Generates spec.md and plan.md from templates
- Parses tasks from plan.md → updates TODO_*.md YAML frontmatter
- Commits changes automatically
- **When to use:** Standard for features, optional for complex hotfixes

**Feedback Loop (SpecKit → BMAD - Callable Tool):**
- **Run script:** `update_asbuilt.py` after PR merge (Phase 4)
- Compares as-built specs with original BMAD planning
- Auto-detects technology deviations
- Interactive Q&A for metrics and lessons learned
- Updates planning/ files with "As-Built" sections
- Improves future planning accuracy

**PR Feedback via Work-Items (git-workflow-manager - Callable Tool):**
- **Run script:** `generate_work_items_from_pr.py` after PR review (Phase 4.3)
- Auto-detects VCS provider (GitHub/Azure DevOps)
- Extracts unresolved PR conversations (GitHub: isResolved==false, Azure: status==active)
- Creates work-items with slug pattern: pr-{pr_number}-issue-{sequence}
- Compatible with all issue trackers
- **When to use:** Standard for substantive PR feedback, skip for simple fixes
- **Token savings:** No additional cost (pure CLI operations)

## Critical Skill Integration Patterns

Understanding how skills interact is essential for maximizing token efficiency and workflow effectiveness.

### BMAD → SpecKit Context Reuse (Token Efficiency)

**Token savings through context flow:**
- **BMAD** (Phase 1) creates `planning/<slug>/` with requirements.md and architecture.md
- **SpecKit** (Phase 2) auto-detects `../planning/<slug>/` from feature worktrees
- Context reuse reduces SpecKit Q&A from 10-15 questions (without BMAD) to 5-8 questions (with BMAD)
- **Token savings: 1,700-2,700 tokens per feature** by reusing planning context

**Implementation:** SpecKit's `create_specifications.py` checks for `../planning/<slug>/` and loads requirements/architecture to pre-populate spec.md and plan.md templates, skipping redundant questions.

**When to use BMAD:**
- Complex features requiring stakeholder alignment → Use BMAD
- Simple bug fixes or small refactors → Skip BMAD, use SpecKit standalone

### Shared TODO File Manipulation (Consistency)

**All callable tools follow consistent TODO patterns:**
- BMAD, SpecKit, and workflow utilities all write YAML frontmatter to TODO_*.md
- workflow-utilities provides shared YAML parsing/writing functions (used by all skills)
- **Registration pattern:** Create TODO_*.md → call `workflow_registrar.py` → update TODO.md manifest
- **Archival pattern:** Move to ARCHIVED/ → call `workflow_archiver.py` → update TODO.md manifest

**Benefits:**
- Consistent YAML structure enables AgentDB synchronization
- Cross-phase queries work reliably (e.g., "what tasks are blocked?")
- Single source of truth for workflow state

### AgentDB Dual-Write Architecture (Analytics Cache)

**Source of truth vs. analytics cache:**
- **TODO_*.md files** remain the source of truth (human-editable, git-tracked)
- **AgentDB** is a read-only analytics cache (DuckDB, 24-hour session lifetime)
- **Sync pattern:** Modify TODO_*.md → run `sync_todo_to_db.py` → query AgentDB

**When to use AgentDB:**
- Complex queries (dependencies, blocked tasks, progress analytics) → 89% token reduction
- Simple file reads (single TODO file) → Just read the file directly
- Cross-workflow queries → AgentDB shines (e.g., "all blocked tasks across all features")

### Quality + Versioning Integration (Automation)

**Automated semantic versioning from test results:**
1. **quality-enforcer** runs pytest with coverage (Phase 3)
2. **semantic_version.py** analyzes git diff for breaking changes, features, fixes
3. Both outputs merged into TODO_*.md `quality_gates` section:
   ```yaml
   quality_gates:
     test_coverage: 85
     tests_passing: true
     semantic_version: "1.5.0"
   ```
4. Version propagates to PR title, git tags, CHANGELOG.md

**Benefits:**
- No manual version calculation - automated from code changes + test quality
- Quality gates enforced before PR creation (≥80% coverage required)
- Version history correlates with actual changes (not arbitrary bumps)

## Git Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑                             ↑
release/vX.Y.Z                hotfix/vX.Y.Z-hotfix.N (worktree)
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution (contrib/stharrold)
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
```

**Current contrib branch:** `contrib/stharrold`

### Protected Branches

**CRITICAL:** `main` and `develop` are **protected and permanent** branches.

**Rules:**
1. ❌ **Never delete** `main` or `develop`
2. ❌ **Never commit directly** to `main` or `develop`
3. ✅ **Only merge via pull requests** (approval optional, self-merge enabled as of v1.8.1)

**No exceptions:** All scripts create PRs (including `backmerge_release.py` which creates PR for release → develop)

**Technical enforcement:**
- Configure GitHub branch protection (see `.github/BRANCH_PROTECTION.md`)
- Configure Azure DevOps branch policies (see `.github/AZURE_DEVOPS_POLICIES.md`)
- Install pre-push hook: `cp .git-hooks/pre-push .git/hooks/pre-push && chmod +x .git/hooks/pre-push`

**If you violate protection:** See WORKFLOW.md "Branch Protection Policy" section for recovery procedures.

### Merge Method Configuration

⚠️ **CRITICAL**: Configure GitHub account to use "Create a merge commit" instead of squash merge.

**Why squash merge breaks workflow:**
- Loses individual commit messages (combines all into one)
- Breaks auto-close functionality ("Closes #N" references lost)
- Reduces git history traceability
- Complicates debugging and bisecting

**Configure merge method:**
1. **Account default:** https://github.com/settings/merge-preferences
   - Set default to "Create a merge commit"
2. **Per-PR override:** Select "Create a merge commit" in PR UI before merging

**If issues didn't auto-close after PR merge:**
```bash
# Manually close issues with reference to merged PR
gh issue close <issue-number> --comment "Fixed in PR #<pr-number>"
```

**Check current account default:**
```bash
gh api graphql -f query='query { viewer { login defaultMergeMethod } }'
# Should show: "MERGE" (not "SQUASH")
```

**Branch workflows:**
- **Features:** contrib → feature worktree → contrib → develop → release → main
- **Hotfixes:** main → hotfix worktree → main (tagged) → back-merge to develop
- **Releases:** develop → release branch → main (tagged) → back-merge to develop

## Production Safety & Rollback

**Critical principle:** Deploy from **tags** (v1.5.1), never branch heads. Tags are immutable and enable instant rollback.

### Emergency Rollback (if production breaks)

**Fastest rollback (2 minutes):**
```bash
git checkout v1.5.0  # Last known good tag
# Deploy this tag to production
```

**Remove bad release from main:**
```bash
git revert <merge-commit-sha> -m 1
git tag -a v1.5.2 -m "Revert broken v1.5.1"
git push origin v1.5.2
```

**If hotfix takes too long:**
- Keep production on v1.5.0 (stable)
- Don't rush the hotfix - do it properly with quality gates
- Production stability > speed

**Why tag-based deployment:**
- v1.5.1 never changes (immutable)
- Can reproduce exact deployment anytime
- Instant rollback (no code changes)
- Clear version in production

**Main branch protection:**
- Hotfix work isolated in separate worktree (main untouched)
- Main only updated via merged PRs
- Tagged releases are immutable (can always rollback)

**See WORKFLOW.md "Production Safety & Rollback" section for:**
- Complete rollback procedures (3 scenarios)
- Rollback decision tree
- Timeline estimates (10 min rollback, 20 min cleanup)

## Common Development Commands

### Workflow Commands

```bash
# Detect project stack (run once per session)
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# Create BMAD planning (Phase 1: in main repo, contrib branch)
python .claude/skills/bmad-planner/scripts/create_planning.py \
  <slug> stharrold

# Create feature worktree (Phase 2)
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/stharrold

# Create hotfix worktree (from main for production fixes)
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix <slug> main

# Create SpecKit specifications (Phase 2: in worktree)
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature <slug> stharrold --todo-file ../TODO_feature_*.md

# Update BMAD planning with as-built details (Phase 4: after PR merge)
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/<slug> specs/<slug>

# Generate work-items from PR feedback (Phase 4: optional, for substantive changes)
python .claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py \
  <pr-number>

# Daily rebase contrib onto develop
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold

# Update TODO task status
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_*.md <task_id> <complete|pending|blocked>

# Register workflow in TODO.md (Phase 1/2)
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  TODO_feature_*.md <workflow_type> <slug> --title "Feature Title"

# Atomic cleanup: archive + delete worktree + delete branches (Phase 4.6: RECOMMENDED)
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  <slug> \
  --summary "What was completed" \
  --version "1.9.0"

# Manual cleanup (NOT RECOMMENDED - use atomic cleanup above)
# Archive workflow first
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_*.md --summary "What was completed" --version "1.9.0"
# Then delete worktree and branches
git worktree remove ../german_feature_<slug>
git branch -D feature/<timestamp>_<slug>
git push origin --delete feature/<timestamp>_<slug>

# Sync TODO.md with filesystem (recovery)
python .claude/skills/workflow-utilities/scripts/sync_manifest.py

# Run quality gates (Phase 3)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Calculate semantic version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.0.0
```

### AgentDB State Management

```bash
# Initialize AgentDB (run once per session)
python .claude/skills/agentdb-state-manager/scripts/init_database.py

# Sync TODO files to AgentDB (after TODO updates)
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py --all

# Query current workflow state
python .claude/skills/agentdb-state-manager/scripts/query_state.py

# Query task dependencies
python .claude/skills/agentdb-state-manager/scripts/query_state.py \
  --dependencies --task <task_id>

# Analyze workflow metrics
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py --trends

# Store context checkpoint (at 100K tokens)
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py \
  store --todo TODO_feature_*.md

# List checkpoints
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py list
```

### Release Management

```bash
# Create release branch from develop
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.1.0 develop

# Tag release on main after merge
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.1.0 main

# Back-merge release to develop (v5.2.0+: includes pre-PR rebase)
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.1.0 develop

# Cleanup release branch after completion
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.1.0
```

**Pre-PR Rebase Feature (git-workflow-manager v5.2.0+):**
- `backmerge_release.py` now rebases release branch onto target before creating PR
- Ensures clean linear history and prevents "branch out-of-date" warnings
- Automatically detects conflicts and provides clear error messages
- Uses `--force-with-lease` for safe force push after rebase

### Repository Initialization (Phase 0)

```bash
# Bootstrap new repository with complete workflow system (run once per repo)
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  <source-repo> <target-repo>

# Example: Replicate workflow from current repo to new project
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project

# For existing repositories: See detailed guidance
cat .claude/skills/initialize-repository/SKILL.md
# Read "Applying to Existing Repositories" section for safety guidelines
```

**What gets copied:**
- ✓ 9 workflow skills (BMAD, SpecKit, quality gates, git automation, etc.)
- ✓ Workflow documentation (WORKFLOW.md, CONTRIBUTING.md, quality configs)
- ✗ Your code remains untouched (unless you choose to copy domain content)

**⚠️ Caution for existing repos:** Overwrites README.md, CLAUDE.md, pyproject.toml, .gitignore. Use test-copy approach or backup before applying.

**When to use:** Phase 0 (bootstrapping). Run once per repository, NOT part of Phases 1-6 workflow.

### Package Management

```bash
# Install/sync dependencies
uv sync

# Add a dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Testing & Quality

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term

# Coverage with threshold check (required ≥80%)
uv run pytest --cov=src --cov-fail-under=80

# Run single test file
uv run pytest tests/test_models.py

# Run specific test
uv run pytest tests/test_models.py::test_vocabulary_word_noun_with_gender

# Run tests matching pattern
uv run pytest -k "noun"

# Verbose output
uv run pytest -v

# Lint code
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Type checking
uv run mypy src/

# Format code
uv run ruff format src/
```

### Container Operations

```bash
# Build container
podman build -t german:latest .

# Run container
podman run --rm -p 8000:8000 german:latest

# Run with compose
podman-compose up -d
podman-compose ps
podman-compose logs
podman-compose down
```

## Directory Standards

**Every directory** created by workflow must have:
- `CLAUDE.md` - Context-specific guidance with YAML frontmatter
  - References: sibling README.md, parent CLAUDE.md, children CLAUDE.md
- `README.md` - Human-readable documentation with YAML frontmatter
  - References: sibling CLAUDE.md, parent README.md, children README.md
- `ARCHIVED/` - Subdirectory for deprecated files (except in ARCHIVED itself)

**YAML Frontmatter (CLAUDE.md):**
```yaml
---
type: claude-context
directory: path/to/dir
purpose: Brief purpose description
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - subdir/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---
```

**YAML Frontmatter (README.md):**
```yaml
---
type: directory-documentation
directory: path/to/dir
title: Directory Title
sibling_claude: CLAUDE.md
parent: ../README.md
children:
  - ARCHIVED/README.md
  - subdir/README.md
---
```

**Create compliant directories:**
```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py <directory>
```

**Migrate existing directories:**
```bash
# Preview changes
python .claude/skills/workflow-utilities/scripts/migrate_directory_frontmatter.py --dry-run

# Apply migration
python .claude/skills/workflow-utilities/scripts/migrate_directory_frontmatter.py
```

## Quality Gates (Enforced Before PR)

- ✓ Test coverage ≥ 80%
- ✓ All tests passing
- ✓ Build successful
- ✓ Linting clean (ruff)
- ✓ Type checking clean (mypy)
- ✓ Container healthy (if applicable)
- ✓ DuckDB compatibility (no PostgreSQL-specific syntax)
- ✓ Healthcare compliance (HIPAA/FDA/IRB if applicable)
- ✓ APPEND-ONLY enforcement for audit trails (where applicable)

## GitHub Issue Management

**Issue Sources:**
- GitHub Copilot code reviews (automated static analysis)
- Manual issue creation by contributors
- Dependency security alerts

**Issue Workflow:**
1. **On contrib branch:** Fix issues locally while working on features
2. **Create commits:** Reference issue numbers in commit messages
   ```bash
   git commit -m "fix(quality): resolve unused variable (Issue #44)"
   ```
3. **Batch fixes:** Multiple related issues can be fixed in one commit
   ```bash
   git commit -m "fix(quality): resolve all GitHub Copilot code review issues

   Fixed 11 code quality issues identified by Copilot code reviews:
   - Issues #44-47: Remove unused variables
   - Issue #49: Fix bare except blocks
   - Issue #48: Fix Python 3 syntax error
   ..."
   ```
4. **PR to develop:** Include issue references in PR description with exact keywords
5. **Close issues:** Issues auto-close when PR merges if commit message uses **exact keywords** followed by `#N`:
   - **Closes #N** (recommended - most explicit)
   - **Fixes #N** (for bug fixes)
   - **Resolves #N** (for general issues)

   **Multiple issues:** Use one keyword per line:
   ```bash
   git commit -m "fix(quality): add explicit UTF-8 encoding to file operations

   Add encoding='utf-8' parameter to all open() calls for cross-platform compatibility.

   Closes #60
   Closes #61
   Closes #62"
   ```

   **IMPORTANT:** The format must be **exactly** `Closes #N` (not "Issues #N" or "Issue #N")

**Troubleshooting - Issues Not Auto-Closing:**

If issues remain open after PR merge:
1. Check commit messages for exact keyword format (`Closes #N`)
2. **Manual close:** `gh issue close <number> --comment "Fixed in vX.Y.Z"`
3. **Proper commit (future PRs):** Use exact keywords listed above

**Common Issue Types:**
- **Unused variables/imports:** Remove or use the variable
- **Bare except blocks:** Replace `except:` with specific exceptions (e.g., `except (ValueError, TypeError):`)
- **Line too long (>100 chars):** Break into multiple lines (acceptable in some cases)
- **Syntax errors:** Fix immediately (blocking)
- **Security issues:** Address with highest priority

**Quality Commands:**
```bash
# Check for linting issues (pyflakes only)
uv run ruff check . --select F

# Check all linting rules
uv run ruff check .

# Auto-fix safe issues
uv run ruff check --fix .

# Run tests to verify fixes
uv run pytest -v
```

**Best Practices:**
- Fix issues on feature/contrib branches, not directly on develop/main
- Group related fixes in single commits (e.g., all unused variables together)
- Always run tests after fixes to ensure no regressions
- Reference issue numbers in commit messages for traceability

## Healthcare Compliance (For Medical/Research Projects)

**If working with Protected Health Information (PHI) or medical research:**

**HIPAA Requirements:**
- All PHI access MUST be logged with justification
- Audit trails MUST be immutable (APPEND-ONLY)
- Actor/role tracking required for all operations
- Compliance gaps must be documented and mitigated

**Implementation Patterns:**
```python
# Use compliance enforcement decorators
from compliance_enforcer import enforce_append_only, validate_phi_access

@enforce_append_only('sync_audit_trail')
def insert_audit_log(conn, data):
    return conn.execute("INSERT INTO sync_audit_trail ...")

# Validate PHI access
validate_phi_access(
    phi_accessed=True,
    phi_justification="Clinical research analysis per IRB protocol #12345"
)
```

**Compliance Documentation:**
- See `.claude/skills/agentdb-state-manager/docs/phase1_hipaa_compliance.md` for detailed compliance validation
- GAP analysis required for all healthcare-related features
- FDA 21 CFR Part 11 requirements for electronic records

**Testing:**
```bash
# Test APPEND-ONLY enforcement
python -c "from compliance_enforcer import enforce_append_only; ..."

# Run compliance validation
python .claude/skills/agentdb-state-manager/scripts/test_schema_migration.py
```

## Project Configuration

**.gitignore:** Excludes `__pycache__/`, `.coverage`, `*.pyc`, `.venv/`, and IDE/OS files. Do not commit generated files.

## DuckDB Development Guidelines

**This project uses DuckDB (≥1.4.2) for AgentDB state management.**

**Critical Syntax Differences from PostgreSQL:**

**❌ Don't use PostgreSQL syntax:**
```sql
-- WRONG: PostgreSQL (not valid in DuckDB)
NOW() - INTERVAL '30 days'  -- ❌ Uses quoted interval and plural 'days'
EXTRACT(EPOCH FROM (timestamp1 - timestamp2))  -- ❌ EXTRACT(EPOCH) not supported
```

**✅ Use DuckDB syntax:**
```sql
-- CORRECT: DuckDB interval syntax
CURRENT_TIMESTAMP - INTERVAL 30 DAY

-- CORRECT: DuckDB date/time functions
datediff('millisecond', timestamp1, timestamp2)
```

**Foreign Key Support:**
- DuckDB DOES support ON DELETE actions (CASCADE, RESTRICT, SET NULL, SET DEFAULT, NO ACTION)
- Always use explicit `ON DELETE RESTRICT` for audit trail immutability
- Example: `REFERENCES parent(id) ON DELETE RESTRICT`

**Testing DuckDB Queries:**
```bash
# Test query directly in DuckDB
duckdb -c "SELECT your_query_here;"

# Load schema and test
duckdb < .claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql
```

**DuckDB Resources:**
- Official Docs: https://duckdb.org/docs/
- SQL Reference: https://duckdb.org/docs/sql/introduction

## German Language Content Guidelines

### Data Structure

When working with German language content:
- Nouns have grammatical gender (der/die/das) - always include this
- Verbs have separable prefixes - track this attribute
- Adjectives have declension - may need tables
- Cases (Nominativ, Akkusativ, Dativ, Genitiv) affect articles and adjectives

### Content Organization

1. **Vocabulary:**
   - Store in `resources/vocabulary/` as JSON/YAML
   - Schema: German word, English translation, gender, plural forms

2. **Grammar Rules:**
   - Document in `resources/grammar/` as Markdown
   - Include examples with explanations

3. **Listening Practice:**
   - B1-level content in `output/topic-*.md`
   - Format: `<German> . <English> . <German> . <English> .`
   - 150 words per minute speech rate
   - 15 minutes per topic (~2,250 words)
   - 20 topics covering all B1 exam areas

4. **Exam Resources:**
   - Certificate guides in `input/german-certificate-*.md`
   - Covers all CEFR levels (A1, A2, B1, B2, C1, C2)
   - Free practice materials, exam structure, official resources
   - Aligned with Goethe-Institut, telc, and ÖSD standards

### Data Quality

- Validate umlauts (ä, ö, ü) and eszett (ß) encoding (UTF-8)
- Cross-check translations for accuracy
- Cite sources when possible
- **B1 Listening Content Standards:**
  - Grammar: Authentic B1 structures (Perfekt, Präteritum, Konjunktiv II, subordinate clauses)
  - Vocabulary: 2,400-3,000 active words (B1 CEFR level)
  - Sentence complexity: 12-20 words average, mix of simple and complex
  - Topics: Match official Goethe, telc, ÖSD B1 exam requirements

## File Deprecation

**Never delete files directly.** Use deprecation:

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_*.md "description" old_file1.py old_file2.py
```

This creates `ARCHIVED/<timestamp>_description.zip` and removes originals.

**List archives:**
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py list
```

**Extract archive:**
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract ARCHIVED/<archive>.zip restored/
```

## Documentation Maintenance

**CRITICAL: When updating skills, all related documentation must be updated.**

### Quick Update Process

**Use the update checklist:**
```bash
cat .claude/skills/UPDATE_CHECKLIST.md
```

**Validate version consistency:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose
```

**Semi-automated sync (after modifying a skill):**
```bash
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  <skill-name> <new-version>
```

### Files to Update When Modifying a Skill

1. **`.claude/skills/<skill-name>/SKILL.md`** - Version in frontmatter, documentation
2. **`.claude/skills/<skill-name>/CLAUDE.md`** - Usage examples
3. **`.claude/skills/<skill-name>/CHANGELOG.md`** - Version history
4. **`WORKFLOW.md`** - Phase sections, commands, token metrics
5. **`CLAUDE.md`** (this file) - Command reference if changed
6. **Integration files** - Other skills that depend on the updated skill

### Version Numbering (Semantic Versioning)

Skills and WORKFLOW.md use `MAJOR.MINOR.PATCH`:

- **MAJOR:** Breaking changes, removed features
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes, documentation improvements

**Example:** bmad-planner v5.0.0 → v5.1.0 (added migration Q&A feature)

### Validation Tools

**Check version consistency:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py
```

**View skill versions:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose
```

### Related Documentation

- **[UPDATE_CHECKLIST.md](.claude/skills/UPDATE_CHECKLIST.md)** - Complete update checklist
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Repository changelog
- **Skill CHANGELOGs:** `.claude/skills/<skill-name>/CHANGELOG.md`

## TODO File Format

Workflow uses TODO files with YAML frontmatter:

```yaml
---
type: workflow-manifest
workflow_type: feature
slug: feature-name
github_user: stharrold

workflow_progress:
  phase: 2
  current_step: "2.3"
  last_task: impl_002

quality_gates:
  test_coverage: 80
  tests_passing: true
  semantic_version: "1.1.0"

tasks:
  implementation:
    - id: impl_001
      status: complete
      completed_at: "2025-10-23T10:00:00Z"
---

# TODO body content
```

## TODO.md Master Manifest Format

The root `TODO.md` file is a master registry tracking all workflow files. It uses YAML frontmatter with two arrays: `workflows.active[]` (in-progress) and `workflows.archived[]` (completed).

**Master manifest structure:**

```yaml
---
type: workflow-master-manifest
version: 5.0.0
last_update: "2025-11-03T17:07:21Z"

workflows:
  active:                    # In-progress workflows
    - slug: auth-system
      timestamp: 20251103T143000Z
      title: "User Authentication System"
      status: in_progress
      file: "TODO_feature_20251103T143000Z_auth-system.md"

  archived:                  # Completed workflows
    - slug: workflow
      timestamp: 20251023T123254Z
      title: "Release Workflow Automation"
      status: completed
      completed_at: "2025-10-23T19:30:00Z"
      semantic_version: "1.2.0"
      file: "ARCHIVED/TODO_feature_20251023T123254Z_workflow.md"
      summary: "Brief description of what was accomplished"

context_stats:
  total_workflows_completed: 1
  current_token_usage: 55000
  last_checkpoint: "2025-11-03T17:07:21Z"
  recent_improvements: "Summary of recent direct improvements"
---

# Master TODO Manifest

Body content with human-readable summaries...
```

**Lifecycle management:**

1. **Phase 1/2 (Registration):** After creating TODO_feature_*.md, register in active list:
   ```bash
   python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
     TODO_feature_*.md <workflow_type> <slug> --title "Feature Title"
   ```

2. **During workflow:** TODO_feature_*.md tracks individual task progress

3. **Phase 4.4 (Archival):** After PR merge, move to archived list:
   ```bash
   python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
     TODO_feature_*.md --summary "What was completed" --version "1.5.0"
   ```
   This moves file to ARCHIVED/ and updates TODO.md manifest

4. **Phase 4.5 (Cleanup):** Delete worktree and feature branch:
   ```bash
   git worktree remove ../german_feature_<slug>
   git branch -D feature/<timestamp>_<slug>
   git push origin --delete feature/<timestamp>_<slug>
   ```
   Removes local worktree, local branch, and remote branch

5. **Recovery (if needed):** Rebuild manifest from filesystem:
   ```bash
   python .claude/skills/workflow-utilities/scripts/sync_manifest.py
   ```

**Key distinction:**
- **TODO.md** = Master registry of ALL workflows (one file, tracks everything)
- **TODO_feature_*.md** = Individual workflow tracking (one per feature/hotfix)

## Semantic Versioning

Automatic version calculation based on changes:
- **MAJOR**: Breaking changes (API changes, removed features)
- **MINOR**: New features (new files, new endpoints)
- **PATCH**: Bug fixes, refactoring, docs, tests

**Current version:** v1.12.0 (latest stable)

**Recent releases:**
- v1.12.0: MIT Agent Synchronization Pattern (Phase 3: Integration Layer) (MINOR)
- v1.11.0: MIT Agent Synchronization Pattern (Phase 2: Synchronization Engine) (MINOR)
- v1.10.1: Post-v1.10.0 documentation cleanup and issue resolution (PATCH)
- v1.10.0: MIT Agent Synchronization Pattern (Phase 1) + DuckDB compatibility fixes (MINOR)
- v1.9.1: ARCHITECTURE.md documentation clarity improvements (PATCH)
- v1.9.0: PR feedback work-item generation workflow (MINOR)
- v1.8.1: Branch protection updates + self-merge enabled (PATCH)
- v1.8.0: CI/CD replication + DRY navigation guide (MINOR)
- v1.7.0: Cross-platform CI/CD infrastructure (MINOR)
- v1.6.0: Branch protection + GitHub issue management (MINOR)
- v1.5.1: Bug fixes + comprehensive skill documentation (PATCH)
- v1.5.0: Azure DevOps CLI support with VCS abstraction layer (MINOR)
- v1.4.0: BMAD and SpecKit callable tools with token reduction (MINOR)
- v1.3.0: Complete B1 German listening practice library (MINOR)
- v1.2.0: Release automation scripts + workflow v5.0 architecture (MINOR)

**Included in v1.12.0:**
- MIT Agent Synchronization Pattern Phase 3 (integration layer)
- 594-line worktree_agent_integration.py with FlowTokenManager, PHIDetector, ComplianceWrapper
- Agent hooks for bmad-planner, quality-enforcer, speckit-author (<10 lines each)
- 563-line test suite with 34 tests (96% coverage)
- Feature flag control (SYNC_ENGINE_ENABLED, disabled by default)
- Graceful degradation on errors
- Non-invasive integration pattern
- PR #226 merged to develop
- Linting fixes (Issues #218-221 closed)

**Included in v1.11.0:**
- MIT Agent Synchronization Pattern Phase 2 (synchronization engine)
- 559-line sync_engine.py with declarative coordination and pattern matching
- SHA-256 content-addressed hashing for idempotency enforcement
- 689-line test suite with 22 comprehensive tests (88% coverage)
- 215-line Phase 2 database migration (extends Phase 1 schema)
- 394-line integration guide for engine usage
- 1,720-line workflow tracking documentation
- N999 linting exception for .claude directory
- Code quality improvements (issues #199-201, #203 fixed)

**Included in v1.10.1:**
- Post-release documentation cleanup (ARCHIVED directories, compliance docs)
- Closed duplicate issues from Phase 1 (#167-172)
- APPEND-ONLY terminology standardization
- YAML frontmatter spacing fixes
- Updated CLAUDE.md for v1.10.0 completion status

**Included in v1.10.0:**
- MIT Agent Synchronization Pattern Phase 1 (database schema, HIPAA/FDA/IRB compliance)
- DuckDB schema with 458 lines, 3 core tables, 20+ indexes
- Healthcare compliance documentation (511 lines) and integration guide (1068 lines)
- Test suite with 557 test cases (706 lines)
- Directory structure improvements (docs/, benchmarks/ with ARCHIVED/ subdirectories)
- DuckDB development guidelines in CLAUDE.md

**Included in v1.9.0 and earlier:**
- Work-item generation workflow from PR feedback (v1.9.0)
- Branch protection compliance (PR workflow enforced, approval optional since v1.8.1)
- Azure DevOps branch policies documentation (644 lines comprehensive guide)
- Documentation maintenance system (UPDATE_CHECKLIST.md, validate_versions.py, sync_skill_docs.py)
- CHANGELOG system for all skills
- CONTRIBUTING.md with contributor guidelines
- initialize-repository meta-skill (Phase 0 bootstrapping for new repositories)
- agentdb-state-manager skill (persistent state tracking and analytics with 89-92% token reduction)
- Official Claude Code docs integration with skill creation workflow
- TODO.md lifecycle management (workflow_registrar.py, workflow_archiver.py, sync_manifest.py in workflow-utilities v5.1.0)

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

Implements: <task_id>
Spec: <spec_file>
Tests: <test_file>
Coverage: <percentage>

Refs: TODO_<workflow>_<timestamp>_<slug>.md

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** feat, fix, docs, style, refactor, test, chore

## Key Workflow Behaviors

✓ Load orchestrator first, then skills per phase (token efficient)
✓ Always wait for "Y" confirmation before actions
✓ Monitor context - automatic checkpoint at 100K tokens
✓ Update TODO file after each step
✓ Use workflow-utilities for shared utilities
✓ Enforce quality gates before PR creation

## Context Monitoring (CRITICAL)

**Token Threshold: 100K tokens**

System will show token usage after each tool use:
```
Token usage: 98543/200000; 101457 remaining
```

**At 100K tokens (~73% of 136K effective capacity):**

✅ **Claude automatically:**
1. Updates TODO_*.md with current state
2. Commits checkpoint
3. Displays: "✓ State saved to TODO file"

⚠️ **You must then:**
1. Run `/init` (updates CLAUDE.md memory files)
2. Run `/compact` (compresses memory buffer)
3. Continue working - context preserved in TODO_*.md

**Warning at 80K tokens:**
- Complete current task before checkpoint
- Checkpoint at 100K ensures clean resume

**Effective context breakdown:**
- Total capacity: 200K tokens
- System overhead: 64K tokens (prompt, tools, memory, buffer)
- Usable context: 136K tokens
- Checkpoint at: 100K tokens (73% of usable)
- Safety margin: 36K tokens for wrap-up

**Why 100K tokens?**
- Ensures enough remaining context to:
  - Save complete state to TODO_*.md
  - Commit changes properly
  - Provide clear resume instructions
- Prevents hitting hard limits mid-task
- Allows current task completion before reset

## Critical Architectural Notes

**TODO File Location:**
- `TODO_*.md` files live in **main repo**, NOT in worktrees
- Worktrees reference via `../TODO_*.md`
- `TODO.md` is master manifest with YAML frontmatter listing all active/archived workflows

**Timestamp Format:**
- Use `YYYYMMDDTHHMMSSZ` (compact ISO8601)
- Rationale: Remains intact when parsed by underscores/hyphens
- Example: `feature/20251023T143000Z_my-feature`

**Version Field in Frontmatter:**
- All SKILL.md files include `version: 5.0.0` in frontmatter
- Purpose: Quality control for file format consistency and inter-file compatibility

**Best Practices Compliance:**
- Error handling: Try/except with helpful messages
- Input validation: Before all operations
- Constants documented: Inline with rationale
- Cleanup on failure: Remove artifacts if operation fails

**Reference Documentation:**
- Complete workflow: `WORKFLOW.md` (6 phases including hotfix, 2000+ lines)
- Detailed planning: `TODO_feature_*.md` files
- SpecKit implementation: `.claude/skills/speckit-author/` (callable tools)
- Original spec: `ARCHIVED/Workflow-v5x2.md`
- Update process: `.claude/skills/UPDATE_CHECKLIST.md` (12-step skill update guide)

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[WORKFLOW.md](WORKFLOW.md)** - Complete 6-phase workflow guide (2000+ lines)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[benchmarks/CLAUDE.md](benchmarks/CLAUDE.md)** - Benchmarks
- **[docs/CLAUDE.md](docs/CLAUDE.md)** - Docs
- **[planning/CLAUDE.md](planning/CLAUDE.md)** - Planning
- **[resources/CLAUDE.md](resources/CLAUDE.md)** - Resources
- **[specs/CLAUDE.md](specs/CLAUDE.md)** - Specifications
- **[src/CLAUDE.md](src/CLAUDE.md)** - Src
- **[tests/CLAUDE.md](tests/CLAUDE.md)** - Tests
