# Adaptive Learning Engine — Design Spec

**Date**: 2026-04-02
**Status**: Approved
**Issue**: [#363](https://github.com/stharrold/german/issues/363)
**Scope**: Adaptive drill engine for Lesen + Hören exercises with CLI interface

## Overview

Add an adaptive learning engine that tracks student proficiency per exam concept, selects exercises based on mastery gaps, and provides an interactive CLI drill session. The UI is both a standalone Python CLI and conversational use within Claude Code.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Skills covered | Lesen + Hören only (v1) | Objective answers, auto-scorable. Schreiben/Sprechen need subjective evaluation. |
| Concept taxonomy | Exam-structure-centric | Zero manual tagging — concepts auto-derived from `{level}-{skill}-teil-{N}` |
| Persistence | JSON file at `~/.german/profile.json` | Simple, human-readable, zero dependencies. ~48 concepts is tiny. |
| CLI approach | Library + standalone script + Claude Code | Core engine is a pure Python library. Standalone CLI proves it works. Claude Code provides richer interaction. |

## Concept Model

Each concept is auto-derived from exercise fields: `f"{level.lower()}-{skill}-teil-{part}"`.

**A2 example** (8 concepts):

| Concept ID | Description | Difficulty |
|------------|-------------|------------|
| `a2-lesen-teil-1` | Medientexte verstehen (newspaper/magazine articles) | 0.3 |
| `a2-lesen-teil-2` | Informationstafeln verstehen (information boards) | 0.5 |
| `a2-lesen-teil-3` | Korrespondenz verstehen (emails, letters) | 0.7 |
| `a2-lesen-teil-4` | Anzeigen verstehen (classified ads, matching) | 0.9 |
| `a2-hoeren-teil-1` | Radio/Anrufbeantworter (short announcements) | 0.3 |
| `a2-hoeren-teil-2` | Zusammenhängendes Gespräch (extended conversation) | 0.5 |
| `a2-hoeren-teil-3` | Einzelgespräche (short dialogues) | 0.7 |
| `a2-hoeren-teil-4` | Radiointerview (interview, true/false) | 0.9 |

Extends to all 6 CEFR levels: ~48 total concepts (8 per level for levels with 4+4 Teile, varies by level).

Concept IDs are derived, not stored — `derive_concept_id(exercise)` computes them from exercise fields.

**Difficulty mapping** by Teil number within each skill:
- Teil 1: 0.3
- Teil 2: 0.5
- Teil 3: 0.7
- Teil 4: 0.9
- Teil 5: 0.9 (for levels like B1 Lesen that have 5 Teile)

## Proficiency Tracker

Adapted from chimeu's `ConceptProfiler`.

### Update Formulas

- **Correct answer**: `proficiency += (1 - proficiency) * difficulty * 0.3`
- **Incorrect answer**: `proficiency *= 0.7`
- Clamped to [0.0, 1.0]
- **Mastery threshold**: 0.85

### Review Scheduling

`next_review = now + timedelta(days = 1 + (proficiency * 6))`

Mastered concepts (0.85+) get reviewed every ~6-7 days. Weak concepts (< 0.3) get reviewed daily.

### Proficiency Updates Per Question

Each question answered updates the concept proficiency individually. An exercise with 5 questions produces 5 proficiency updates to the same concept.

### Profile Schema

Stored at `~/.german/profile.json`:

```json
{
  "student_name": "Samuel",
  "active_levels": ["a2"],
  "created": "2026-04-02T10:00:00",
  "last_session": "2026-04-02T14:30:00",
  "concepts": {
    "a2-lesen-teil-1": {
      "proficiency": 0.72,
      "total_attempts": 8,
      "correct_attempts": 6,
      "mastered": false,
      "last_attempt": "2026-04-02T14:30:00",
      "next_review": "2026-04-05T14:30:00",
      "attempt_history": [
        {
          "timestamp": "2026-04-02T14:30:00",
          "exercise_id": "a2-lesen-teil-1-003",
          "question": 2,
          "is_correct": true,
          "old_proficiency": 0.65,
          "new_proficiency": 0.72
        }
      ]
    }
  }
}
```

## Adaptive Selector

### Concept Selection

```
priority = (1 - proficiency) * days_since_review
```

Highest priority concept is selected. Ties broken randomly.

### Exercise Selection Within Concept

1. Filter all exercises for the selected concept (e.g., all `a2-lesen-teil-1` exercises)
2. Exclude exercises attempted in the last 24 hours
3. If all excluded (small exercise pool), pick least-recently-attempted
4. Random from remaining candidates

### Level Scoping

The selector only considers concepts at the student's active level(s). On first run, the student picks a level. Additional levels can be added via `--level`.

### Cold Start

New student with no history — concepts are presented in order: Lesen Teil 1 → 2 → 3 → 4, then Hören Teil 1 → 2 → 3 → 4. After the first pass through all concepts, the priority formula takes over.

## Scorer

Handles the different question types present in Lesen and Hören exercises:

| Question Type | Scoring Logic |
|---------------|---------------|
| `multiple_choice` | `answer.lower().strip() == correct_answer.lower().strip()` |
| `true_false` | `answer.lower() in ("ja", "true", "richtig")` compared to bool `correct_answer` |
| `matching` | Letter comparison: `answer.lower().strip() == correct_answer.lower().strip()` |

Returns a `ScoreResult` with: `is_correct: bool`, `correct_answer: str`, `explanation_de: str | None`, `explanation_en: str | None`.

## Architecture & File Layout

### New Module

```
src/german/adaptive/
├── __init__.py          # Public API exports
├── concepts.py          # derive_concept_id(), DIFFICULTY_MAP, CONCEPT_DESCRIPTIONS
├── profiler.py          # StudentProfile — load/save JSON, update proficiency
├── selector.py          # AdaptiveSelector — pick next concept + exercise
├── scorer.py            # score_answer() for MC, true/false, matching
└── cli.py               # Standalone drill: `python -m german.adaptive`
```

### Module Responsibilities

**`concepts.py`** — Standalone, no imports from other adaptive modules.
- `derive_concept_id(exercise) -> str` — computes `{level}-{skill}-teil-{part}`
- `DIFFICULTY_MAP: dict[int, float]` — Teil number to difficulty
- `CONCEPT_DESCRIPTIONS: dict[str, str]` — human-readable concept names (e.g., "Medientexte verstehen")
- `get_scorable_skills() -> list[str]` — returns `["hoeren", "lesen"]`

**`profiler.py`** — Imports `concepts.py`.
- `StudentProfile` class:
  - `load(path) -> StudentProfile` — reads JSON, creates if missing
  - `save()` — writes JSON with `ensure_ascii=False, indent=2`
  - `update(concept_id, is_correct, difficulty, exercise_id, question_number)` — applies gain/decay formula
  - `get_proficiency(concept_id) -> float` — returns 0.0 for unseen concepts
  - `get_priority(concept_id) -> float` — computes `(1 - proficiency) * days_since_review`
  - `get_stats() -> dict` — summary statistics for dashboard

**`selector.py`** — Imports `profiler.py`, `concepts.py`, exam loader.
- `AdaptiveSelector` class:
  - `__init__(profile, level)` — loads exercises for the level
  - `pick_next() -> Exercise | None` — selects highest-priority concept, then exercise within it
  - `get_concept_order() -> list[str]` — cold-start ordering

**`scorer.py`** — Imports exam models only.
- `ScoreResult` dataclass: `is_correct`, `correct_answer`, `explanation_de`, `explanation_en`
- `score_answer(question, user_answer) -> ScoreResult`

**`cli.py`** — Imports everything, orchestrates the drill loop.
- `DrillSession` class:
  - `__init__(level, num_questions, profile_path)` — sets up session
  - `run()` — main loop: select → present → answer → score → update → repeat
  - `show_stats()` — progress dashboard
- `main()` — argument parsing, entry point for `python -m german.adaptive`

### Data Flow

```
Student launches drill
  → cli creates DrillSession(level, num_questions)
  → selector.pick_next() queries profiler for highest-priority concept
  → selector loads exercises for that concept via exam loader
  → cli presents exercise questions one at a time (prints passage/transcript + question)
  → user types answer
  → scorer.score_answer() checks correctness
  → cli displays result + explanation
  → profiler.update() adjusts mastery
  → profiler.save() writes to ~/.german/profile.json
  → repeat until num_questions reached or user quits
  → cli shows session summary
```

## CLI Interface

### Standalone Drill

```
$ uv run python -m german.adaptive --level a2 --questions 10

=== German Adaptive Drill — A2 ===
Student: Samuel | Mastered: 2/8 concepts | Session: 0/10

─── Lesen Teil 1: Medientexte verstehen ───
[Proficiency: 0.45 ▓▓▓▓░░░░░░ | Priority: HIGH]

Sie lesen in einer Zeitung diesen Text.
[passage displayed]

Frage 1/5: Bei Stefan Berger können Gäste ...
  a) bekannte Gerichte essen.
  b) interessante Getränke bestellen.
  c) neue Speisen probieren.

Your answer: c

✓ Richtig! (0.45 → 0.57)

[... remaining questions ...]

─── Exercise Summary ───
a2-lesen-teil-1: 4/5 correct (0.45 → 0.78)

Continue? [Y/n]:
```

### Progress Dashboard

```
$ uv run python -m german.adaptive --stats

=== A2 Progress ===
Concept                    Prof.  Mastered  Last      Next Review
─────────────────────────────────────────────────────────────────
Lesen Teil 1 (Medientexte) 0.87   ✓         today     Apr 08
Lesen Teil 2 (Info-tafeln) 0.72   ·         yesterday Apr 04
Lesen Teil 3 (Korrespond.) 0.45   ·         2d ago    overdue!
Lesen Teil 4 (Anzeigen)    0.31   ·         3d ago    overdue!
Hören Teil 1 (Radio)       0.91   ✓         today     Apr 09
Hören Teil 2 (Gespräch)    0.00   ·         never     —
Hören Teil 3 (Einzelgespr) 0.00   ·         never     —
Hören Teil 4 (Interview)   0.00   ·         never     —

Overall: 2/8 mastered | 156 questions answered | 68% accuracy
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--level {a1,a2,b1,b2,c1,c2}` | CEFR level to drill | Required on first run, remembered after |
| `--questions N` | Questions per session | 10 |
| `--stats` | Show progress dashboard only | — |
| `--reset` | Clear profile and start over | — |
| `--profile PATH` | Custom profile path | `~/.german/profile.json` |

## Testing Strategy

- **`concepts.py`**: Test `derive_concept_id()` with exercises from each level/skill
- **`profiler.py`**: Test gain/decay formulas, mastery threshold, review scheduling, JSON persistence (round-trip load/save), cold-start defaults
- **`selector.py`**: Test priority-based selection, exercise exclusion (24h rule), cold-start ordering, empty pool handling
- **`scorer.py`**: Test each question type (MC, true/false, matching), case insensitivity, whitespace handling
- **`cli.py`**: Integration test with mock stdin/stdout — run a 3-question session, verify profile updated

## Out of Scope (v1)

- Schreiben and Sprechen exercises (need subjective evaluation)
- Vocabulary-only drill mode
- Web UI, Marimo notebooks, or any GUI
- Audio playback for Hören exercises
- Multi-student profiles in a single file
- Spaced repetition with configurable intervals
- Concept dependencies (e.g., "must master Teil 1 before Teil 3")
