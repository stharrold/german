---
type: claude-context
directory: resources
purpose: Context-specific guidance for resources
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - vocabulary/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---

# Claude Code Context: resources

## Purpose

Context-specific guidance for resources

## Directory Structure

```
resources/
├── vocabulary/                   # JSON word lists (nouns, verbs, adjectives)
├── exams/a1/                     # A1 exam practice exercises (60, Goethe-Institut format)
│   ├── hoeren/teil-{1-3}/        # Listening (15 exercises)
│   ├── lesen/teil-{1-4}/         # Reading (20 exercises)
│   ├── schreiben/aufgabe-{1-2}/  # Writing (10 exercises)
│   └── sprechen/teil-{1-3}/      # Speaking (15 exercises)
├── exams/a2/                     # A2 exam practice exercises (65, Goethe-Institut format)
│   ├── hoeren/teil-{1-4}/        # Listening (20 exercises)
│   ├── lesen/teil-{1-4}/         # Reading (20 exercises)
│   ├── schreiben/aufgabe-{1-2}/  # Writing (10 exercises)
│   └── sprechen/teil-{1-3}/      # Speaking (15 exercises)
├── exams/b1/                     # B1 exam practice exercises (75, Goethe-Institut format)
│   ├── hoeren/teil-{1-4}/        # Listening (20 exercises)
│   ├── lesen/teil-{1-5}/         # Reading (25 exercises)
│   ├── schreiben/aufgabe-{1-3}/  # Writing (15 exercises)
│   └── sprechen/teil-{1-3}/      # Speaking (15 exercises)
├── exams/b2/                     # B2 exam practice exercises (65, Goethe-Institut format)
│   ├── hoeren/teil-{1-4}/        # Listening (20 exercises)
│   ├── lesen/teil-{1-5}/         # Reading (25 exercises)
│   ├── schreiben/aufgabe-{1-2}/  # Writing (10 exercises)
│   └── sprechen/teil-{1-2}/      # Speaking (10 exercises)
└── supplementary/                # Supplementary teaching resources
    └── b1-listening-topics/      # B1 listening topics (20 bilingual prose files)
```

## Conventions

- All JSON files must be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- Use `json.dump(data, fh, ensure_ascii=False, indent=2)` — no unicode escapes
- Exercise ID format: `{level}-{skill}-{teil|aufgabe}-{N}-{NNN}`
- Exercise files: `uebung-{01-05}.json` (zero-padded)
- Model answers should aim to match `target_word_count` (±2 words) — manual guideline, not enforced by validators
- All exam exercises validated by Pydantic models in `src/german/exams/models.py`


## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[vocabulary/CLAUDE.md](vocabulary/CLAUDE.md)** - Vocabulary

## Related Skills

- workflow-orchestrator
- workflow-utilities