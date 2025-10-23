# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Python-based repository for German language learning resources and content. It contains:
- German language reference materials (vocabulary, grammar, etc.)
- Python scripts and tools for language processing and learning
- Structured data for German language content
- **Workflow v5.0 skill-based architecture** for managing development workflow

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv (preferred) or pip
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees
- **Workflow System:** Skill-based architecture (7 specialized skills)
- **Containerization:** Podman + podman-compose

## Workflow v5.0 Architecture

This repository uses a **skill-based workflow system** located in `.claude/skills/`. The system provides progressive skill loading - only load what's needed for the current phase.

### Available Skills

**Location:** `.claude/skills/<skill-name>/SKILL.md`

1. **workflow-orchestrator** - Main coordinator for workflow phases
2. **tech-stack-adapter** - Detects Python/uv project configuration
3. **git-workflow-manager** - Git operations, worktrees, semantic versioning
4. **bmad-planner** - Creates BMAD planning documents (requirements, architecture)
5. **speckit-author** - Creates detailed specifications and implementation plans
6. **quality-enforcer** - Enforces quality gates (≥80% coverage, tests, linting)
7. **workflow-utilities** - Shared utilities for file management and TODO updates

### Using the Workflow

**Start workflow:** Say **"next step?"**

The orchestrator will:
- Detect current context (main repo vs worktree, current branch)
- Load only relevant skills for current phase
- Prompt for confirmation before each action
- Update TODO file with progress
- Guide through: planning → specification → implementation → quality → PR

**Monitor context usage:** Run `/context` periodically. When >50%, orchestrator will save state and prompt you to run `/init` to reset.

### Workflow Phases

**Phase 1: Planning** (main repo, `contrib/<gh-user>` branch)
- Create requirements.md and architecture.md
- Skills: bmad-planner

**Phase 2: Implementation** (feature worktree)
- Create spec.md and plan.md
- Implement features
- Write tests
- Skills: speckit-author, git-workflow-manager

**Phase 3: Quality** (feature worktree)
- Run quality gates (≥80% coverage, all tests passing)
- Calculate semantic version
- Skills: quality-enforcer

**Phase 4: Integration**
- Create PR: feature → contrib/<gh-user>
- Merge in GitHub UI
- Rebase contrib onto develop
- Create PR: contrib/<gh-user> → develop
- Skills: git-workflow-manager

## Git Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑
release/vX.Y.Z                ← Release candidate
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution (contrib/stharrold)
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
```

**Current contrib branch:** `contrib/stharrold`

## Common Development Commands

### Workflow Commands

```bash
# Detect project stack (run once per session)
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# Create feature worktree
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/stharrold

# Update TODO task status
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_*.md <task_id> <complete|pending|blocked>

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Calculate semantic version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.0.0
```

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
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term

# Coverage with threshold check
uv run pytest --cov=src --cov-fail-under=80

# Lint code
uv run ruff check src/ tests/

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
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` - Subdirectory for deprecated files (except in ARCHIVED itself)

Use `workflow-utilities/scripts/directory_structure.py` to create compliant directories.

## Quality Gates (Enforced Before PR)

- ✓ Test coverage ≥ 80%
- ✓ All tests passing
- ✓ Build successful
- ✓ Linting clean (ruff)
- ✓ Type checking clean (mypy)
- ✓ Container healthy (if applicable)

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

3. **Exercises:**
   - Store as JSON with correct answers
   - Tag by difficulty and topic

### Data Quality

- Validate umlauts (ä, ö, ü) and eszett (ß) encoding (UTF-8)
- Cross-check translations for accuracy
- Cite sources when possible

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

## Semantic Versioning

Automatic version calculation based on changes:
- **MAJOR**: Breaking changes (API changes, removed features)
- **MINOR**: New features (new files, new endpoints)
- **PATCH**: Bug fixes, refactoring, docs, tests

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
✓ Monitor context via `/context` - save state and `/init` when >50%
✓ Update TODO file after each step
✓ Use workflow-utilities for shared utilities
✓ Enforce quality gates before PR creation
