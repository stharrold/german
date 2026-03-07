# Vocabulary Expansion with CEFR Tagging — Design

**Issue:** #338
**Date:** 2026-03-07

## Problem

Current vocabulary files contain only ~70 words (all A1). Need comprehensive CEFR-tagged coverage across A1–C2.

## Approach: Script-Based Generation

Create `scripts/generate_vocabulary.py` that:
1. Contains vocabulary data organized by CEFR level and POS
2. Validates all entries through Pydantic before writing
3. Generates `nouns.json`, `verbs.json`, `adjectives.json`

## Cumulative Word Count Targets

| Level | Cumulative | New Words | Nouns (~55%) | Verbs (~25%) | Adj (~20%) |
|-------|-----------|-----------|-------------|-------------|-----------|
| A1    | ~500      | ~500      | ~275        | ~125        | ~100      |
| A2    | ~1,000    | ~500      | ~275        | ~125        | ~100      |
| B1    | ~2,000    | ~1,000    | ~550        | ~250        | ~200      |
| B2    | ~3,500    | ~1,500    | ~825        | ~375        | ~300      |
| C1    | ~5,000    | ~1,500    | ~825        | ~375        | ~300      |
| C2    | ~6,000+   | ~1,000    | ~550        | ~250        | ~200      |

## Schema (existing, unchanged)

```json
{
  "words": [
    {
      "german": "Haus",
      "english": "house",
      "part_of_speech": "noun",
      "gender": "neuter",
      "plural": "Häuser",
      "level": "A1"
    }
  ]
}
```

## Deliverables

1. `scripts/generate_vocabulary.py` — generation script with embedded vocabulary data
2. Updated `resources/vocabulary/{nouns,verbs,adjectives}.json` — expanded files
3. `tests/test_vocabulary_levels.py` — CEFR distribution validation tests
4. All existing tests continue to pass
