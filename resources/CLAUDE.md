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
├── vocabulary/              # JSON word lists (nouns, verbs, adjectives)
├── exams/b1/                # B1 exam practice exercises (Goethe-Institut format)
│   ├── hoeren/teil-{1-4}/   # Listening (20 exercises)
│   ├── lesen/teil-{1-5}/    # Reading (25 exercises)
│   ├── schreiben/aufgabe-{1-3}/  # Writing (15 exercises)
│   └── sprechen/teil-{1-3}/      # Speaking (15 exercises)
└── supplementary/           # B1 listening topics (20 bilingual prose files)
```

## Conventions

- All JSON files must be UTF-8 encoded (for umlauts: ä, ö, ü, ß)
- Use `json.dump(data, fh, ensure_ascii=False, indent=2)` — no unicode escapes
- Exercise ID format: `b1-{skill}-{teil|aufgabe}-{N}-{NNN}`
- Exercise files: `uebung-{01-05}.json` (zero-padded)
- Model answers must match `target_word_count` (±2 words)
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