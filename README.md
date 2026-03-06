# German Language Learning Repository

A Python-based repository for German language learning resources, featuring A1, A2, B1, B2, and C1 exam practice exercises in Goethe-Institut format.

## Purpose

This repository contains:
- **A1 exam practice exercises** — 60 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **A2 exam practice exercises** — 65 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **B1 exam practice exercises** — 75 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **B2 exam practice exercises** — 65 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **C1 exam practice exercises** — 65 structured exercises across all 4 skills (Hören, Lesen, Schreiben, Sprechen) in Goethe-Institut format
- **Supplementary listening topics** — 20 bilingual prose topics (~2,250 words each) for B1 listening practice
- **Vocabulary data** — German nouns, verbs, and adjectives with Pydantic validation
- **Certificate guides** — Reference materials for CEFR levels A1–C2
- **Python tools** — Loader and query modules for vocabulary and exam data

## Exam Practice Content

### A1 (60 exercises)

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–3 | 15 | Multiple-choice, true/false |
| **Lesen** (Reading) | Teil 1–4 | 20 | Multiple-choice, true/false, matching |
| **Schreiben** (Writing) | Aufgabe 1–2 | 10 | Form filling, short messages |
| **Sprechen** (Speaking) | Teil 1–3 | 15 | Introductions, requests, planning |

### A2 (65 exercises)

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–4 | 20 | Multiple-choice, true/false, matching |
| **Lesen** (Reading) | Teil 1–4 | 20 | Multiple-choice, true/false, matching |
| **Schreiben** (Writing) | Aufgabe 1–2 | 10 | Informal messages, form filling |
| **Sprechen** (Speaking) | Teil 1–3 | 15 | Topic cards, planning, discussions |

### B1 (75 exercises)

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–4 | 20 | Multiple-choice, true/false, matching |
| **Lesen** (Reading) | Teil 1–5 | 25 | Multiple-choice, true/false, matching |
| **Schreiben** (Writing) | Aufgabe 1–3 | 15 | Informal/formal emails, opinion pieces |
| **Sprechen** (Speaking) | Teil 1–3 | 15 | Planning, presentations, discussions |

### B2 (65 exercises)

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–4 | 20 | Multiple-choice, interviews, lectures |
| **Lesen** (Reading) | Teil 1–5 | 25 | Multiple-choice, opinions, academic texts |
| **Schreiben** (Writing) | Aufgabe 1–2 | 10 | Formal letters, argumentative essays |
| **Sprechen** (Speaking) | Teil 1–2 | 10 | Presentations, discussions, negotiations |

### C1 (65 exercises)

| Skill | Parts | Exercises | Format |
|-------|-------|-----------|--------|
| **Hören** (Listening) | Teil 1–4 | 20 | Academic lectures, debates, professional conversations |
| **Lesen** (Reading) | Teil 1–5 | 25 | Academic articles, essays, reports, literary analysis |
| **Schreiben** (Writing) | Aufgabe 1–2 | 10 | Professional texts, argumentative essays |
| **Sprechen** (Speaking) | Teil 1–2 | 10 | Academic presentations, collaborative negotiation |

### How to Practice

Each exercise is a JSON file. To practice:

1. **Open any exercise file** (e.g., `resources/exams/b1/lesen/teil-1/uebung-01.json`)
2. **Read the instructions** (`instructions`) and, where present, the situational context (`situation_de` for Schreiben/Sprechen)
3. **Do the exercise:**
   - *Lesen:* Read the passage (`passage.text_de`), answer the questions, then check against `correct_answer`
   - *Hören:* Read the transcript (`transcript.text_de`), answer the questions, then check against `correct_answer`
   - *Schreiben:* Write a response following the `required_points`, then compare with `model_answer.text_de`
   - *Sprechen:* Prepare a response using `discussion_points`, then review the `model_dialogue` and `evaluation_criteria`
4. **Use the English fields** (`text_en`, `situation_en`) if you need help understanding

Or use the Python API to load exercises programmatically:

```python
from pathlib import Path
from german.exams.loader import load_exercises
from german.exams.models import ReadingExercise

lesen = load_exercises(Path("resources/exams/b1/lesen"), ReadingExercise)
```

### Exercise Files

```
resources/exams/a2/
├── hoeren/teil-{1-4}/uebung-{01-05}.json
├── lesen/teil-{1-4}/uebung-{01-05}.json
├── schreiben/aufgabe-{1-2}/uebung-{01-05}.json
└── sprechen/teil-{1-3}/uebung-{01-05}.json

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
