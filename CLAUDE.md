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
- B1 exam practice content: complete (21/21 closed), milestone [#299](https://github.com/stharrold/german/issues/299)
- B1 foundation complete: Pydantic models, loader/query, directory structure, validation tests (#278-281)
- B1 Hören complete: 20 exercises across teil-1 to teil-4 (#282-285)
- B1 Lesen complete: 25 exercises across teil-1 to teil-5 (#286-290)
- B1 Schreiben complete: 15 exercises across aufgabe-1 to aufgabe-3 (#291-293)
- B1 Sprechen complete: 15 exercises across teil-1 to teil-3 (#294-296)
- A2 exam practice content: complete (#321), v2.3.0
- A2: 65 exercises — Hören (4×5), Lesen (4×5), Schreiben (2×5), Sprechen (3×5)
- A1 exam practice content: complete (#334), v2.4.0
- A1: 60 exercises — Hören (3×5), Lesen (4×5), Schreiben (2×5), Sprechen (3×5)
- B2 exam practice content: complete (#335), v2.5.0
- B2: 65 exercises — Hören (4×5), Lesen (5×5), Schreiben (2×5), Sprechen (2×5)
- C1 exam practice content: complete (#336)
- C1: 65 exercises — Hören (4×5), Lesen (5×5), Schreiben (2×5), Sprechen (2×5)

## Repository Purpose

Python-based German language learning resources and content:
- German vocabulary data (nouns, verbs, adjectives) with Pydantic validation
- B1-level listening comprehension topics (20 topics, bilingual format)
- Certificate guides for CEFR levels (A1-C2)
- Python tools for loading and querying vocabulary data
- B1 exam practice exercises (75 exercises, Goethe-Institut format — see [#299](https://github.com/stharrold/german/issues/299))
- A2 exam practice exercises (65 exercises, Goethe-Institut format — #321)
- A1 exam practice exercises (60 exercises, Goethe-Institut format — #334)
- B2 exam practice exercises (65 exercises, Goethe-Institut format — #335)
- C1 exam practice exercises (65 exercises, Goethe-Institut format — #336)

## Gotchas

- `.claude/settings.local.json` is gitignored — do not commit (restrictive Bash allowlists break CI `claude-code-action` which needs unrestricted `gh` access)
- `release_workflow.py create-release` auto-calculates version from last git tag — override manually for major bumps
- Ruff auto-fixes import ordering on commit — re-stage if pre-commit hook modifies files
- `backmerge_workflow.py cleanup-release` only prints instructions — run `git branch -d release/vX.Y.Z && git push origin --delete release/vX.Y.Z` manually
- `cleanup_feature.py` may miss worktree cleanup — verify with `git worktree list`, then `git worktree remove <path>`, `git branch -d <branch>`, `git push origin --delete <branch>`
- Backmerge: always try `backmerge_workflow.py pr-develop` (release → develop) first — only fall back to PR `main` → `develop` if `gh pr create` returns "No commits between develop and release"
- `claude-code-review.yml` requires `claude_args: "--allowedTools Bash,WebFetch,WebSearch,Skill,Task"` (not `allowed_tools`), `id-token: write` (for OIDC auth), and `fetch-depth: 0` — without these, tool calls are denied and git diff can't reach the base branch
- `uv run` modifies `uv.lock` when `pyproject.toml` version changes — commit `uv.lock` after version bumps or rebase-contrib will fail with "Uncommitted changes detected"
- Git worktrees use a `.git` file (not directory) — use `.exists()` not `.is_dir()` when checking for git repos
- Can't `git checkout` a branch that's checked out in a worktree — work from the worktree path or `git worktree remove` first
- All nouns MUST have gender (der/die/das) — enforced by Pydantic `@model_validator`
- JSON vocabulary files MUST be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- German direct speech in JSON: avoid unescaped ASCII double quotes inside strings — either escape inner quotes (`\"...\"`) or use single quotes for the speech (`'...'`). Typographic quotes like `„..."` are fine as long as any ASCII `"` is escaped
- WritingExercise uses `task` field (not `part`) — `filter_by_part()` handles this, but new query code must too
- VCS supports GitHub (`gh`) and Azure DevOps (`az`) — auto-detected from `git remote.origin.url`
- After deleting/renaming Python modules, grep all `*.md` files under `.claude/skills/` for stale references
- After deleting/renaming Python modules, also grep `tests/` for stale imports — stale test files cause pytest collection errors (exit code 2) that block ALL tests
- `gh issue create --label X` fails if label doesn't exist — run `gh label create` first
- `record_sync.py` (AgentDB state tracking) doesn't exist in this repo — worktree/integrate skills reference it but failure is non-blocking
- `git branch -d` fails on feature branches merged via PR (not merged to local HEAD) — use `git branch -D` after confirming the PR is merged
- Contrib→develop PR shows "out of date with base branch" — run `git fetch origin && git merge origin/develop --no-edit && git push` on contrib branch
- Exam exercise `target_word_count` must match the model answer word count (±2 words) — Copilot CI flags mismatches
- Always use `json.dump(data, fh, ensure_ascii=False, indent=2)` when writing exam JSON to avoid `\u00xx` unicode escapes for German characters
- Reply to PR inline comments via `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies` — not top-level PR comments
- `Closes #N` in PR body doesn't auto-close issues when PRs go through contrib→develop (two-hop merge) — close issues manually with `gh issue close`
- `claude-code-review.yml` workflow validation fails until the file exists on `main` (the default branch) — do a release to fix
- Never cherry-pick commits between branches — causes duplicate commits and test failures. If a PR was closed (not merged), recreate the source branch and reopen the PR instead
- Can't reopen a GitHub PR if its head branch was deleted — recreate the branch at the original SHA first, then `gh pr reopen`
- `gh pr view --json state,mergeCommit` distinguishes merged (`mergeCommit` present) from closed-without-merge (`mergeCommit: null`)
- When creating new exam level content, generate PDFs (`uv run --extra pdf python scripts/make_pdfs.py --level {level}`) and commit them — they're not auto-generated
- JSON files written by agents/Write tool lack trailing newlines — always add `fh.write("\n")` after `json.dump` or reformat with `jq`
- Bump `pyproject.toml` version on every release — `__init__.py` reads it dynamically via `importlib.metadata.version()`
- A1 Hören Teil-2 has 4 questions (not 5) matching the 4-dialogue Goethe format — test assertions must reflect per-teil question counts
- Agent-generated JSON files may have CRLF line endings — check with `grep -rl $'\r'` and normalize before committing
- AI-generated exam exercises bias correct_answer to one option — redistribute using deterministic hash: `md5(exercise_id + question_number) % num_options`
- `release_workflow.py tag-release` creates git tags but NOT GitHub Releases — run `gh release create vX.Y.Z` separately after tagging

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
├── vocabulary/
│   ├── loader.py          # JSON → VocabularyWord objects (UTF-8)
│   └── query.py           # Filter by POS, gender, lookup
└── exams/
    ├── models.py          # Pydantic: ListeningExercise, ReadingExercise, WritingExercise, SpeakingExercise
    ├── loader.py          # JSON → Exercise objects (generic TypeVar loader)
    └── query.py           # Filter by skill, part, question type

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
resources/supplementary/         # B1 listening topics (20 topics, bilingual prose)
resources/vocabulary/            # JSON word lists (nouns, verbs, adjectives)
resources/exams/a1/              # A1 exam practice exercises (60, Goethe-Institut format)
├── hoeren/teil-{1-3}/          # Listening (3 parts, 5 exercises each)
├── lesen/teil-{1-4}/           # Reading (4 parts, 5 exercises each)
├── schreiben/aufgabe-{1-2}/    # Writing (2 tasks, 5 exercises each)
└── sprechen/teil-{1-3}/        # Speaking (3 parts, 5 exercises each)
resources/exams/a2/              # A2 exam practice exercises (65, Goethe-Institut format)
├── hoeren/teil-{1-4}/          # Listening (4 parts, 5 exercises each)
├── lesen/teil-{1-4}/           # Reading (4 parts, 5 exercises each)
├── schreiben/aufgabe-{1-2}/    # Writing (2 tasks, 5 exercises each)
└── sprechen/teil-{1-3}/        # Speaking (3 parts, 5 exercises each)
resources/exams/b1/              # B1 exam practice exercises (75, Goethe-Institut format)
├── hoeren/teil-{1-4}/          # Listening (4 parts, 5 exercises each)
├── lesen/teil-{1-5}/           # Reading (5 parts, 5 exercises each)
├── schreiben/aufgabe-{1-3}/    # Writing (3 tasks, 5 exercises each)
└── sprechen/teil-{1-3}/        # Speaking (3 parts, 5 exercises each)
resources/exams/b2/              # B2 exam practice exercises (65, Goethe-Institut format)
├── hoeren/teil-{1-4}/          # Listening (4 parts, 5 exercises each)
├── lesen/teil-{1-5}/           # Reading (5 parts, 5 exercises each)
├── schreiben/aufgabe-{1-2}/    # Writing (2 tasks, 5 exercises each)
└── sprechen/teil-{1-2}/        # Speaking (2 parts, 5 exercises each)
resources/exams/c1/              # C1 exam practice exercises (65, Goethe-Institut format)
├── hoeren/teil-{1-4}/          # Listening (4 parts, 5 exercises each)
├── lesen/teil-{1-5}/           # Reading (5 parts, 5 exercises each)
├── schreiben/aufgabe-{1-2}/    # Writing (2 tasks, 5 exercises each)
└── sprechen/teil-{1-2}/        # Speaking (2 parts, 5 exercises each)
```

**Exam exercise schema:** Structured JSON validated by Pydantic models in `src/german/exams/`. Key fields differ by skill:
- *Hören:* `transcript`, `questions` (with `correct_answer`)
- *Lesen:* `passage`, `questions` (with `correct_answer`)
- *Schreiben:* `situation_de`, `required_points`, `model_answer`, `scoring_criteria`
- *Sprechen:* `situation_de`, `discussion_points`, `model_dialogue`, `evaluation_criteria`

**Exercise ID format:** `{level}-{skill}-{teil|aufgabe}-{N}-{NNN}` — hyphens must match directory names (e.g., `teil-1`, not `teil1`)

`scripts/make_pdfs.py` supports `--level {a1,a2,b1,b2}` for multi-level PDF generation

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

- **v2.5.0** (2026-03-06): B2 exam practice content (65 exercises), subscript digit PDF support
- **v2.4.0** (2026-03-06): A1 exam practice content (60 exercises), version bump alignment
- **v2.3.0** (2026-03-05): A2 exam practice content (65 exercises), multi-level PDF generation
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
