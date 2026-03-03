# B1 Exam Practice Content — Design

**Date:** 2026-03-03
**Status:** Approved
**Approach:** Exam-Mirrored Content Structure (Approach A)

## Goal

Transform this repo from a reference-link collection into a comprehensive CEFR exam practice resource. Start with B1 (Goethe-Institut format), then replicate the pattern for A1-C2.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Exam components | All 4 skills (Hören, Lesen, Schreiben, Sprechen) | Full exam coverage |
| First level | B1 | Existing content (20 listening topics), most detailed certificate guide |
| Content format | Structured JSON + Markdown | Machine-readable for apps/quizzes, human-readable companions |
| Content structure | Mirror Goethe-Institut B1 exam exactly | Learners practice what they'll face |
| Work tracking | GitHub Issues with milestone | Assignment, PR linking, public visibility |

## Directory Structure

```
resources/exams/b1/
├── meta.json                    # Exam metadata (provider, timing, passing score)
│
├── hoeren/                      # Hören — 4 parts, ~40 min, 30 items
│   ├── teil-1/                  # Part 1: short messages/announcements
│   │   ├── uebung-01.json
│   │   └── ...
│   ├── teil-2/                  # Part 2: radio interview/discussion
│   ├── teil-3/                  # Part 3: everyday conversations
│   └── teil-4/                  # Part 4: public announcements
│
├── lesen/                       # Lesen — 5 parts, 65 min, 30 items
│   ├── teil-1/                  # Part 1: blog entries (true/false)
│   ├── teil-2/                  # Part 2: press report (multiple choice)
│   ├── teil-3/                  # Part 3: ads/classifieds (matching)
│   ├── teil-4/                  # Part 4: reader comments (matching opinions)
│   └── teil-5/                  # Part 5: instructions/rules (multiple choice)
│
├── schreiben/                   # Schreiben — 3 tasks, 60 min
│   ├── aufgabe-1/               # Task 1: informal email (~80 words)
│   ├── aufgabe-2/               # Task 2: opinion piece (~80 words)
│   └── aufgabe-3/               # Task 3: formal email (~40 words)
│
└── sprechen/                    # Sprechen — 3 parts, ~15 min (pair exam)
    ├── teil-1/                  # Part 1: collaborative planning
    ├── teil-2/                  # Part 2: topic presentation
    └── teil-3/                  # Part 3: Q&A discussion
```

## JSON Schemas

### Listening Exercise (`hoeren/teil-X/uebung-XX.json`)

```json
{
  "id": "b1-hoeren-teil1-001",
  "level": "B1",
  "skill": "hoeren",
  "part": 1,
  "title": "Telefonische Nachrichten",
  "instructions": "Sie hören fünf kurze Texte. Sie hören jeden Text zweimal.",
  "time_minutes": 10,
  "transcript": [
    {
      "speaker": "narrator",
      "text_de": "...",
      "text_en": "..."
    }
  ],
  "questions": [
    {
      "number": 1,
      "type": "true_false",
      "text_de": "...",
      "text_en": "...",
      "correct_answer": true,
      "explanation_de": "...",
      "explanation_en": "..."
    }
  ]
}
```

### Reading Exercise (`lesen/teil-X/uebung-XX.json`)

```json
{
  "id": "b1-lesen-teil1-001",
  "level": "B1",
  "skill": "lesen",
  "part": 1,
  "title": "Blog: Mein erster Tag im neuen Job",
  "instructions": "Lesen Sie den Text und die Aufgaben 1 bis 6.",
  "time_minutes": 13,
  "passage": {
    "text_de": "...",
    "text_en": "...",
    "source": "Blog post",
    "word_count": 350
  },
  "questions": [
    {
      "number": 1,
      "type": "true_false",
      "text_de": "...",
      "correct_answer": true,
      "explanation_de": "..."
    }
  ]
}
```

### Writing Exercise (`schreiben/aufgabe-X/uebung-XX.json`)

```json
{
  "id": "b1-schreiben-aufgabe1-001",
  "level": "B1",
  "skill": "schreiben",
  "task": 1,
  "title": "E-Mail an einen Freund",
  "instructions": "...",
  "situation_de": "...",
  "situation_en": "...",
  "target_word_count": 80,
  "required_points": ["react to news", "describe the apartment", "suggest meeting"],
  "model_answer": {
    "text_de": "...",
    "text_en": "..."
  },
  "scoring_criteria": ["task fulfillment", "coherence", "vocabulary range", "grammar accuracy"]
}
```

### Speaking Exercise (`sprechen/teil-X/uebung-XX.json`)

```json
{
  "id": "b1-sprechen-teil1-001",
  "level": "B1",
  "skill": "sprechen",
  "part": 1,
  "title": "Gemeinsam etwas planen",
  "instructions": "...",
  "situation_de": "...",
  "situation_en": "...",
  "discussion_points": ["Wann?", "Wo?", "Essen?", "Geschenk?"],
  "model_dialogue": [
    {"speaker": "A", "text_de": "...", "text_en": "..."},
    {"speaker": "B", "text_de": "...", "text_en": "..."}
  ],
  "evaluation_criteria": ["task fulfillment", "fluency", "interaction", "pronunciation"]
}
```

## Python Models

New Pydantic models in `src/german/exams/`:

- `ExamMeta` — level, provider, timing, passing score
- `Question` — number, type (true_false/multiple_choice/matching), correct_answer, explanation
- `ListeningExercise` — transcript lines, questions
- `ReadingExercise` — passage, questions
- `WritingExercise` — prompt, situation, model answer, criteria
- `SpeakingExercise` — situation, discussion points, model dialogue, criteria

New loader: `src/german/exams/loader.py` (load JSON, validate, query by skill/part).

## GitHub Issues — Milestone: "B1 Exam Practice Content"

### Foundation (4 issues)

1. Define Pydantic models for exam exercises
2. Create exam exercise loader + query module
3. Set up `resources/exams/b1/` directory structure + `meta.json`
4. Add JSON schema validation tests

### Content — Hören (4 issues, 5 exercises each)

5. B1 Hören Teil 1 — short messages (5 exercises)
6. B1 Hören Teil 2 — radio discussions (5 exercises)
7. B1 Hören Teil 3 — conversations (5 exercises)
8. B1 Hören Teil 4 — announcements (5 exercises)

### Content — Lesen (5 issues, 5 exercises each)

9. B1 Lesen Teil 1 — blog entries (5 exercises)
10. B1 Lesen Teil 2 — press reports (5 exercises)
11. B1 Lesen Teil 3 — classifieds (5 exercises)
12. B1 Lesen Teil 4 — reader comments (5 exercises)
13. B1 Lesen Teil 5 — instructions/rules (5 exercises)

### Content — Schreiben (3 issues, 5 exercises each)

14. B1 Schreiben Aufgabe 1 — informal email (5 exercises)
15. B1 Schreiben Aufgabe 2 — opinion piece (5 exercises)
16. B1 Schreiben Aufgabe 3 — formal email (5 exercises)

### Content — Sprechen (3 issues, 5 exercises each)

17. B1 Sprechen Teil 1 — collaborative planning (5 exercises)
18. B1 Sprechen Teil 2 — topic presentation (5 exercises)
19. B1 Sprechen Teil 3 — Q&A discussion (5 exercises)

### Integration (2 issues)

20. Migrate existing B1 listening topics to new structure
21. Update CLAUDE.md and README.md for exam content

**Total: 21 issues, 80 exercises for complete B1 coverage.**

## Scope for Later

- Replicate B1 pattern for A1, A2, B2, C1, C2
- CEFR-tag existing vocabulary JSON files
- Add `separable` field to verb schema
- Build quiz/app interface on top of JSON data
- Add Sprachbausteine section (telc-specific)
