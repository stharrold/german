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

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Workflow v7x1 upgrade complete (v2.0.0).
- v5.3 skills (bmad-planner, speckit-author, quality-enforcer) archived
- v7x1 slash commands installed
- CI: GitHub Actions (tests.yml, claude-code-review.yml)
- B1 exam practice content: 21 issues created, milestone [#299](https://github.com/stharrold/german/issues/299)

## Repository Purpose

Python-based German language learning resources and content:
- German vocabulary data (nouns, verbs, adjectives) with Pydantic validation
- B1-level listening comprehension topics (20 topics, bilingual format)
- Certificate guides for CEFR levels (A1-C2)
- Python tools for loading and querying vocabulary data
- B1 exam practice exercises (in progress — see [#299](https://github.com/stharrold/german/issues/299))

## Gotchas

- `.claude/settings.local.json` is gitignored — do not commit (restrictive Bash allowlists break CI `claude-code-action` which needs unrestricted `gh` access)
- `release_workflow.py create-release` auto-calculates version from last git tag — override manually for major bumps
- Ruff auto-fixes import ordering on commit — re-stage if pre-commit hook modifies files
- `backmerge_workflow.py cleanup-release` only prints instructions — run `git branch -d release/vX.Y.Z && git push origin --delete release/vX.Y.Z` manually
- Backmerge: always try `backmerge_workflow.py pr-develop` (release → develop) first — only fall back to PR `main` → `develop` if `gh pr create` returns "No commits between develop and release"
- `claude-code-review.yml` requires `claude_args: "--allowedTools Bash,WebFetch,WebSearch,Skill,Task"` (not `allowed_tools`), `id-token: write` (for OIDC auth), and `fetch-depth: 0` — without these, tool calls are denied and git diff can't reach the base branch
- `uv run` modifies `uv.lock` when `pyproject.toml` version changes — commit `uv.lock` after version bumps or rebase-contrib will fail with "Uncommitted changes detected"
- Git worktrees use a `.git` file (not directory) — use `.exists()` not `.is_dir()` when checking for git repos
- All nouns MUST have gender (der/die/das) — enforced by Pydantic `@model_validator`
- JSON vocabulary files MUST be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- VCS supports GitHub (`gh`) and Azure DevOps (`az`) — auto-detected from `git remote.origin.url`
- After deleting/renaming Python modules, grep all `*.md` files under `.claude/skills/` for stale references
- `gh issue create --label X` fails if label doesn't exist — run `gh label create` first

## Branch Structure

`main` ← `develop` ← `contrib/stharrold` ← `feature/*`

**Protected branches:** `main` and `develop` (PR-only, no direct commits, no squash merge).

## v7x1 Workflow

```
/workflow:v7x1_1-worktree "feature description"  → creates worktree
    Implementation in worktree with Claude Code
/workflow:v7x1_2-integrate "feature/branch"       → PR feature→contrib→develop
/workflow:v7x1_3-release [version]                 → release→main, tag
/workflow:v7x1_4-backmerge                         → release→develop, rebase contrib
```

See [WORKFLOW.md](WORKFLOW.md) for full details.

## Commands

```bash
uv run pytest                              # All tests
uv run ruff check .                        # Lint
uv run pre-commit run --all-files          # Pre-commit hooks
uv run mypy src/                           # Type checking
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

**Data flow:** `JSON → loader.py → VocabularyWord (Pydantic) → query.py → Application`

**Vocabulary schema:**
```json
{"words": [{"german": "...", "english": "...", "part_of_speech": "...", "gender": "..."}]}
```

## Content Architecture

```
input/                          # Certificate guides (A1-C2, resource links)
output/                         # B1 listening topics (20 topics, bilingual prose)
resources/vocabulary/            # JSON word lists (nouns, verbs, adjectives)
resources/exams/b1/              # Exam practice exercises (Goethe-Institut format)
├── hoeren/teil-{1-4}/          # Listening (4 parts, 5 exercises each)
├── lesen/teil-{1-5}/           # Reading (5 parts, 5 exercises each)
├── schreiben/aufgabe-{1-3}/    # Writing (3 tasks, 5 exercises each)
└── sprechen/teil-{1-3}/        # Speaking (3 parts, 5 exercises each)
```

**Exam exercise schema:** Structured JSON with bilingual fields (`text_de`/`text_en`), questions, model answers, and scoring criteria. Validated by Pydantic models in `src/german/exams/`.

**Design:** `docs/plans/2026-03-03-b1-exam-practice-content-design.md`

## German Language Content Guidelines

- Nouns have grammatical gender (der/die/das) — always include
- Verbs may have separable prefixes — track this attribute
- B1 listening format: `<German> . <English> . <German> . <English> .`
- 150 words per minute speech rate, 15 minutes per topic (~2,250 words)
- Validate umlauts (ä, ö, ü) and eszett (ß) encoding (UTF-8)

## Skills (6)

| Skill | Purpose |
|-------|---------|
| `git-workflow-manager` | Worktrees, PRs, semantic versioning, releases |
| `workflow-orchestrator` | Workflow coordination |
| `workflow-utilities` | Shared utilities, deprecation, VCS abstraction |
| `tech-stack-adapter` | Python/uv project detection |
| `agentdb-state-manager` | DuckDB analytics, state tracking |
| `initialize-repository` | Bootstrap workflow in new repos |

## What NOT to Do

- Never commit directly to `main` or `develop` (use PRs only)
- Never delete `main` or `develop` branches
- Never squash merge PRs (breaks auto-close, loses commit history)
- Never push force to main/develop (only use `--force-with-lease` on feature branches)
- Never delete files directly — use `deprecate_files.py` to archive

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

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[benchmarks/CLAUDE.md](benchmarks/CLAUDE.md)** - Benchmarks
- **[docs/CLAUDE.md](docs/CLAUDE.md)** - Docs
- **[resources/CLAUDE.md](resources/CLAUDE.md)** - Resources
- **[src/CLAUDE.md](src/CLAUDE.md)** - Src
- **[tests/CLAUDE.md](tests/CLAUDE.md)** - Tests
