# Vocabulary Expansion with CEFR Tagging — Implementation Plan

**Goal:** Expand vocabulary files from ~70 words to ~6,000+ words with CEFR level tagging (A1–C2).

**Architecture:** A Python generation script (`scripts/generate_vocabulary.py`) contains all vocabulary data organized by CEFR level and POS. It validates every entry through the existing Pydantic `VocabularyWord` model before writing JSON files. A new test file validates CEFR distribution across the generated vocabulary.

**Tech Stack:** Python >=3.11, Pydantic, uv, pytest

---

### Task 1: Write CEFR Distribution Tests

**Files:**
- Create: `tests/test_vocabulary_levels.py`

**Step 1: Write the test file**

```python
"""Tests for CEFR level distribution in vocabulary data."""

from german.models import CEFRLevel
from german.vocabulary import load_vocabulary


def test_all_levels_present():
    """Test that vocabulary contains words at every CEFR level."""
    vocab = load_vocabulary()
    levels = {word.level for word in vocab}
    for level in CEFRLevel:
        assert level in levels, f"Missing CEFR level: {level}"


def test_all_words_have_level():
    """Test that every word has a CEFR level assigned."""
    vocab = load_vocabulary()
    for word in vocab:
        assert word.level is not None, f"Word '{word.german}' missing CEFR level"


def test_no_duplicate_words():
    """Test that there are no duplicate German words within same POS."""
    vocab = load_vocabulary()
    seen = set()
    for word in vocab:
        key = (word.german.lower(), word.part_of_speech)
        assert key not in seen, f"Duplicate: {word.german} ({word.part_of_speech})"
        seen.add(key)


def test_noun_count_minimum():
    """Test minimum noun count across levels."""
    nouns = load_vocabulary(category="nouns")
    assert len(nouns) >= 400, f"Expected >= 400 nouns, got {len(nouns)}"


def test_verb_count_minimum():
    """Test minimum verb count across levels."""
    verbs = load_vocabulary(category="verbs")
    assert len(verbs) >= 200, f"Expected >= 200 verbs, got {len(verbs)}"


def test_adjective_count_minimum():
    """Test minimum adjective count across levels."""
    adjectives = load_vocabulary(category="adjectives")
    assert len(adjectives) >= 200, f"Expected >= 200 adjectives, got {len(adjectives)}"


def test_level_distribution_nouns():
    """Test that nouns are distributed across levels."""
    nouns = load_vocabulary(category="nouns")
    for level in CEFRLevel:
        level_nouns = [n for n in nouns if n.level == level]
        assert len(level_nouns) >= 10, f"Nouns at {level}: {len(level_nouns)} (need >= 10)"


def test_level_distribution_verbs():
    """Test that verbs are distributed across levels."""
    verbs = load_vocabulary(category="verbs")
    for level in CEFRLevel:
        level_verbs = [v for v in verbs if v.level == level]
        assert len(level_verbs) >= 10, f"Verbs at {level}: {len(level_verbs)} (need >= 10)"


def test_level_distribution_adjectives():
    """Test that adjectives are distributed across levels."""
    adjectives = load_vocabulary(category="adjectives")
    for level in CEFRLevel:
        level_adjs = [a for a in adjectives if a.level == level]
        assert len(level_adjs) >= 10, f"Adjectives at {level}: {len(level_adjs)} (need >= 10)"


def test_total_vocabulary_minimum():
    """Test total vocabulary meets minimum threshold."""
    vocab = load_vocabulary()
    assert len(vocab) >= 500, f"Expected >= 500 total words, got {len(vocab)}"
```

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_vocabulary_levels.py -v`
Expected: FAIL — current 70 words are all A1, so `test_all_levels_present` and distribution tests fail.

**Step 3: Commit the failing tests**

```bash
git add tests/test_vocabulary_levels.py
git commit -m "test: add CEFR level distribution tests for vocabulary"
```

---

### Task 2: Create Generation Script Skeleton

**Files:**
- Create: `scripts/generate_vocabulary.py`

**Step 1: Write the script skeleton**

Create `scripts/generate_vocabulary.py` with:
- Imports for `VocabularyWord`, `json`, `pathlib`
- A `generate_nouns()` function returning `list[dict]` of noun entries
- A `generate_verbs()` function returning `list[dict]` of verb entries
- A `generate_adjectives()` function returning `list[dict]` of adjective entries
- A `validate_and_write(words, filepath)` function that:
  - Validates each dict through `VocabularyWord(**entry)`
  - Checks for duplicates (same `german` value)
  - Writes JSON with `json.dump(data, fh, ensure_ascii=False, indent=2)` + trailing newline
  - Prints summary (count per level)
- A `main()` function that calls all three generators and writes the files
- Argparse with `--dry-run` flag (validate only, don't write)

Start with just the existing ~70 words to verify the pipeline works.

**Step 2: Run the script in dry-run mode**

Run: `uv run python scripts/generate_vocabulary.py --dry-run`
Expected: Validation passes for all 70 words, summary printed.

**Step 3: Run the script to generate files**

Run: `uv run python scripts/generate_vocabulary.py`
Expected: Files written, existing tests still pass.

**Step 4: Run all tests**

Run: `uv run pytest tests/ -v`
Expected: All existing tests pass. New distribution tests still fail (only A1 words).

**Step 5: Commit**

```bash
git add scripts/generate_vocabulary.py
git commit -m "feat: add vocabulary generation script skeleton"
```

---

### Task 3: Populate A1 and A2 Vocabulary

**Files:**
- Modify: `scripts/generate_vocabulary.py`

**Step 1: Expand A1 vocabulary data**

Add words to reach A1 targets (~275 nouns, ~125 verbs, ~100 adjectives).
Organize by semantic categories: family, food, home, body, numbers, colors, daily life, etc.
Every noun MUST have `gender` and `plural`. All entries MUST have `level: "A1"`.

**Step 2: Add A2 vocabulary data**

Add words to reach A2 targets (~275 nouns, ~125 verbs, ~100 adjectives).
Categories: work, travel, health, shopping, emotions, weather, media, etc.

**Step 3: Run generation and validate**

Run: `uv run python scripts/generate_vocabulary.py`
Then: `uv run pytest tests/ -v`
Expected: A1/A2 distribution tests should now pass.

**Step 4: Commit**

```bash
git add scripts/generate_vocabulary.py resources/vocabulary/
git commit -m "feat: add A1 and A2 vocabulary (~1,000 words)"
```

---

### Task 4: Populate B1 and B2 Vocabulary

**Files:**
- Modify: `scripts/generate_vocabulary.py`

**Step 1: Add B1 vocabulary data**

~550 nouns, ~250 verbs, ~200 adjectives.
Categories: politics, education, environment, culture, technology, abstract concepts, etc.

**Step 2: Add B2 vocabulary data**

~825 nouns, ~375 verbs, ~300 adjectives.
Categories: science, law, economics, philosophy, specialized professions, academic, etc.

**Step 3: Run generation and validate**

Run: `uv run python scripts/generate_vocabulary.py`
Then: `uv run pytest tests/ -v`

**Step 4: Commit**

```bash
git add scripts/generate_vocabulary.py resources/vocabulary/
git commit -m "feat: add B1 and B2 vocabulary (~2,500 words)"
```

---

### Task 5: Populate C1 and C2 Vocabulary

**Files:**
- Modify: `scripts/generate_vocabulary.py`

**Step 1: Add C1 vocabulary data**

~825 nouns, ~375 verbs, ~300 adjectives.
Categories: advanced academic, literary, technical, formal register, etc.

**Step 2: Add C2 vocabulary data**

~550 nouns, ~250 verbs, ~200 adjectives.
Categories: archaic/literary, highly specialized, idiomatic, regional, scholarly, etc.

**Step 3: Run generation and validate**

Run: `uv run python scripts/generate_vocabulary.py`
Then: `uv run pytest tests/ -v`
Expected: ALL tests pass including distribution tests.

**Step 4: Commit**

```bash
git add scripts/generate_vocabulary.py resources/vocabulary/
git commit -m "feat: add C1 and C2 vocabulary (~2,500 words)"
```

---

### Task 6: Final Validation and Cleanup

**Step 1: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL tests pass.

**Step 2: Run linting**

Run: `uv run ruff check .`
Then: `uv run ruff format .`

**Step 3: Verify JSON formatting**

Run: `uv run python -c "import json; [json.load(open(f'resources/vocabulary/{c}.json')) for c in ['nouns','verbs','adjectives']]"`
Expected: No errors.

**Step 4: Print final summary**

Run: `uv run python scripts/generate_vocabulary.py --dry-run`
Expected: Summary showing word counts per level per POS.

**Step 5: Commit any cleanup**

```bash
git add -A
git commit -m "chore: lint and format vocabulary expansion"
```
