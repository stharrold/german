# German Language Learning Repository

A Python-based repository for German language learning resources, featuring B1 exam practice exercises in Goethe-Institut format.

## Purpose

This repository contains:
- **B1 exam practice exercises** — 80 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **Supplementary listening topics** — 20 bilingual prose topics (~2,250 words each) for B1 listening practice
- **Vocabulary data** — German nouns, verbs, and adjectives with Pydantic validation
- **Certificate guides** — Reference materials for CEFR levels A1–C2
- **Python tools** — Loader and query modules for vocabulary and exam data

## B1 Exam Practice Content

80 exercises following the Goethe-Institut B1 exam format, with bilingual instructions (DE/EN):

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–4 | 20 | Multiple-choice, true/false, matching |
| **Lesen** (Reading) | Teil 1–5 | 25 | Multiple-choice, true/false, matching |
| **Schreiben** (Writing) | Aufgabe 1–3 | 15 | Informal/formal emails, opinion pieces |
| **Sprechen** (Speaking) | Teil 1–3 | 15 | Planning, presentations, discussions |

### How to Practice

Each exercise is a JSON file with bilingual content. To practice:

1. **Open any exercise file** (e.g., `resources/exams/b1/lesen/teil-1/uebung-01.json`)
2. **Read the situation** (`situation_de`) and instructions (`instructions`)
3. **Do the exercise:**
   - *Lesen/Hören:* Read the passage (`passage.text_de`), answer the questions (`questions`), then check against `correct_answer`
   - *Schreiben:* Write a response following the `required_points`, then compare with `model_answer.text_de`
   - *Sprechen:* Prepare a response using the prompts, then review the `model_answer` and `scoring_criteria`
4. **Use the English translations** (`text_en`, `situation_en`) if you need help understanding

Or use the Python API to load exercises programmatically:

```python
from german.exams.loader import load_exercises
from german.exams.query import filter_by_skill

exercises = load_exercises()
lesen = filter_by_skill(exercises, "lesen")
```

### Exercise Files

```
resources/exams/b1/
├── hoeren/teil-{1-4}/uebung-{01-05}.json
├── lesen/teil-{1-5}/uebung-{01-05}.json
├── schreiben/aufgabe-{1-3}/uebung-{01-05}.json
└── sprechen/teil-{1-3}/uebung-{01-05}.json
```

## Quick Start

```bash
# Install dependencies
uv sync

# Authenticate with your VCS provider
gh auth login              # For GitHub

# Start development workflow
/workflow:v7x1_1-worktree "feature description"
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide
- **[WORKFLOW.md](WORKFLOW.md)** - v7x1 workflow guide (4-step)

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **Testing:** pytest with coverage
- **Linting:** ruff
- **Type Checking:** mypy
- **Containerization:** Podman (optional)
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees
- **CI:** GitHub Actions (tests, Claude Code review)

**Protected Branches:** `main` and `develop` are permanent. Never delete or commit directly. All changes via PRs only.

## v7x1 Workflow

```
/workflow:v7x1_1-worktree "description"  → Create worktree + implement
/workflow:v7x1_2-integrate "branch"      → PR feature → contrib → develop
/workflow:v7x1_3-release [version]       → Release → main, tag
/workflow:v7x1_4-backmerge               → Sync release → develop
```

See [WORKFLOW.md](WORKFLOW.md) for full details.

## Development Commands

```bash
# Create feature worktree
/workflow:v7x1_1-worktree "add new vocabulary category"

# Run tests with coverage
uv run pytest --cov=src --cov-report=term

# Run linting
uv run ruff check .

# Run type checking
uv run mypy src/
```

## Using This Workflow in Other Projects

This repository's workflow can be applied to other projects using the bundle system from `stharrold-templates`:

```bash
# Clone templates
git clone https://github.com/stharrold/stharrold-templates.git .tmp/stharrold-templates

# Apply git workflow bundle
python .tmp/stharrold-templates/scripts/apply_bundle.py .tmp/stharrold-templates . --bundle git

# Cleanup
rm -rf .tmp/stharrold-templates
```

## Contributing

This repository uses `contrib/<gh-user>` branches for personal contributions. See [WORKFLOW.md](WORKFLOW.md) for the complete integration process.

## License

[Add license information]
