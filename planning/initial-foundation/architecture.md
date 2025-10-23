# Architecture: Initial Foundation

**Date:** 2025-10-23
**Author:** stharrold
**Status:** Draft

## System Overview

### High-Level Architecture

```
┌─────────────────┐
│  Python Client  │
│   Application   │
└────────┬────────┘
         │ import
         ▼
┌─────────────────┐         ┌──────────────────┐
│  german Package │────────>│  Vocabulary Data │
│  (src/german)   │  loads  │  (JSON files)    │
└─────────────────┘         └──────────────────┘
```

The initial foundation is a simple Python library that loads and validates German vocabulary data from JSON files.

### Components

1. **german Package** (Python library)
   - Core vocabulary data models (Pydantic)
   - Vocabulary loader and validator
   - Query functions for retrieving words
   - Utility functions

2. **Vocabulary Data** (JSON files)
   - Structured vocabulary files in `resources/vocabulary/`
   - Nouns, verbs, adjectives separated by file
   - UTF-8 encoded with German characters

3. **Testing Framework** (pytest)
   - Unit tests for models and loaders
   - Integration tests for end-to-end workflows
   - Test coverage reporting

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **Data Format:** JSON
- **Validation:** Pydantic v2
- **Testing:** pytest, pytest-cov
- **Linting:** ruff
- **Type Checking:** mypy
- **Build System:** hatchling

### Technology Justification

**Why Python 3.11+?**
- Modern Python with better performance
- Excellent type hints support
- Great ecosystem for language processing
- Easy for contributors to work with

**Why JSON?**
- Human-readable and editable
- Git-friendly (easy diffs)
- Simple parsing in Python
- No database overhead for v1.0.0
- Easy migration path to database later

**Why Pydantic?**
- Automatic validation with type hints
- Clear error messages
- JSON serialization built-in
- Well-documented and widely used

## Data Model

### Vocabulary Models

```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class PartOfSpeech(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"

class Gender(str, Enum):
    MASCULINE = "masculine"  # der
    FEMININE = "feminine"    # die
    NEUTER = "neuter"        # das

class VocabularyWord(BaseModel):
    german: str = Field(..., description="German word")
    english: str = Field(..., description="English translation")
    part_of_speech: PartOfSpeech

    # Noun-specific fields
    gender: Optional[Gender] = Field(None, description="Grammatical gender (nouns only)")
    plural: Optional[str] = Field(None, description="Plural form (nouns only)")

    class Config:
        use_enum_values = True

    def model_post_init(self, __context):
        # Validate: nouns must have gender
        if self.part_of_speech == PartOfSpeech.NOUN and self.gender is None:
            raise ValueError(f"Noun '{self.german}' must have a gender")
```

### Data File Structure

```json
{
  "words": [
    {
      "german": "Haus",
      "english": "house",
      "part_of_speech": "noun",
      "gender": "neuter",
      "plural": "Häuser"
    },
    {
      "german": "lernen",
      "english": "to learn",
      "part_of_speech": "verb"
    },
    {
      "german": "schön",
      "english": "beautiful",
      "part_of_speech": "adjective"
    }
  ]
}
```

## Package Structure

```
german/
├── src/
│   └── german/
│       ├── __init__.py           # Package initialization, exports
│       ├── models.py             # Pydantic models (VocabularyWord, etc.)
│       ├── vocabulary/
│       │   ├── __init__.py
│       │   ├── loader.py         # Load vocabulary from JSON
│       │   └── query.py          # Query vocabulary data
│       ├── grammar/              # Grammar module (future)
│       │   └── __init__.py
│       └── utils/
│           ├── __init__.py
│           └── validation.py     # Validation utilities
├── resources/
│   └── vocabulary/
│       ├── nouns.json            # German nouns
│       ├── verbs.json            # German verbs
│       └── adjectives.json       # German adjectives
├── tests/
│   ├── __init__.py
│   ├── test_models.py            # Test Pydantic models
│   ├── test_vocabulary_loader.py # Test vocabulary loading
│   └── test_vocabulary_query.py  # Test query functions
├── pyproject.toml                # Project configuration
└── README.md                     # Usage documentation
```

## API Design

### Vocabulary Loader

```python
from german.vocabulary import load_vocabulary

# Load all vocabulary
vocab = load_vocabulary()  # Returns List[VocabularyWord]

# Load specific category
nouns = load_vocabulary(category="nouns")
```

### Query Functions

```python
from german.vocabulary import get_word, filter_by_pos, filter_by_gender

# Get specific word
word = get_word("Haus")  # Returns VocabularyWord or None

# Filter by part of speech
verbs = filter_by_pos("verb")  # Returns List[VocabularyWord]

# Filter nouns by gender
masculine_nouns = filter_by_gender("masculine")  # Returns List[VocabularyWord]
```

## Error Handling Strategy

### Validation Errors

```python
from pydantic import ValidationError

try:
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech="noun"
        # Missing gender!
    )
except ValidationError as e:
    print(f"Validation error: {e}")
    # Output: "Noun 'Haus' must have a gender"
```

### File Loading Errors

```python
from german.vocabulary import load_vocabulary, VocabularyLoadError

try:
    vocab = load_vocabulary()
except VocabularyLoadError as e:
    print(f"Failed to load vocabulary: {e}")
    # Provides clear error with file name and issue
```

### Logging

- Use Python's `logging` module
- Default level: WARNING
- Users can configure via `logging.basicConfig()`

## Testing Strategy

### Unit Tests

**Target Coverage:** 85%+

```python
# tests/test_models.py
def test_vocabulary_word_with_gender():
    """Test noun with gender."""
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech="noun",
        gender="neuter",
        plural="Häuser"
    )
    assert word.german == "Haus"
    assert word.gender == "neuter"

def test_noun_without_gender_raises_error():
    """Test that nouns require gender."""
    with pytest.raises(ValueError, match="must have a gender"):
        VocabularyWord(
            german="Haus",
            english="house",
            part_of_speech="noun"
        )

def test_verb_does_not_need_gender():
    """Test that verbs don't require gender."""
    word = VocabularyWord(
        german="lernen",
        english="to learn",
        part_of_speech="verb"
    )
    assert word.gender is None
```

### Integration Tests

```python
# tests/test_vocabulary_loader.py
def test_load_vocabulary_from_json():
    """Test loading vocabulary from JSON files."""
    vocab = load_vocabulary()
    assert len(vocab) > 0
    assert all(isinstance(w, VocabularyWord) for w in vocab)

def test_vocabulary_files_are_utf8():
    """Test that vocabulary files have proper encoding."""
    vocab = load_vocabulary()
    # Check for umlauts
    has_umlauts = any('ä' in w.german or 'ö' in w.german or 'ü' in w.german
                      for w in vocab)
    assert has_umlauts, "Vocabulary should include words with umlauts"
```

### Test Data

- Use small test JSON files in `tests/data/`
- Separate from production vocabulary in `resources/`
- Include edge cases: umlauts, eszett, various genders

## Security Considerations

### Input Validation

- All external data validated via Pydantic models
- Type checking prevents invalid data types
- Enum validation for part_of_speech and gender

### No External Dependencies

- No network calls
- No database connections
- File system access limited to known directories

### Data Integrity

- UTF-8 encoding enforced
- Schema validation before loading
- Immutable data structures where possible

## Deployment

### Installation

```bash
# From source
git clone https://github.com/stharrold/german.git
cd german
uv sync

# Development installation
uv sync --all-extras
```

### Usage

```python
import german
from german.vocabulary import load_vocabulary

vocab = load_vocabulary()
for word in vocab[:5]:
    print(f"{word.german} ({word.english})")
```

## Monitoring & Observability

Not applicable for v1.0.0 - this is a library, not a service.

## Scalability Plan

### Current Scale

- Target: 50-100 words in v1.0.0
- Expected: 1000+ words in future releases

### Future Scaling

**When to migrate from JSON:**
- \> 10,000 words
- Need for complex queries
- Performance becomes an issue

**Migration path:**
- SQLite for local storage
- PostgreSQL for multi-user applications
- Keep JSON as import/export format

## Disaster Recovery

### Backup Strategy

- All data in git repository
- Git history provides full backup
- No separate backup needed

## Design Trade-offs

### Decision: JSON vs Database

**Chosen:** JSON files

**Reasoning:**
- Pro: Simple, human-editable
- Pro: Git-friendly for versioning
- Pro: No setup overhead
- Pro: Easy for contributors
- Con: Not suitable for large datasets
- Con: Limited query capabilities

**Alternative Considered:** SQLite
- Why not chosen: Overkill for v1.0.0, adds complexity

### Decision: Pydantic vs dataclasses

**Chosen:** Pydantic

**Reasoning:**
- Pro: Automatic validation
- Pro: JSON serialization
- Pro: Great error messages
- Con: External dependency

**Alternative Considered:** Python dataclasses
- Why not chosen: Need validation, JSON handling

## Open Technical Questions

- [ ] Should we cache loaded vocabulary in memory?
- [ ] Include example sentences in data model?
- [ ] Support for compound words?

## References

- [Pydantic documentation](https://docs.pydantic.dev/)
- [German grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender_in_German)
- [Python packaging with uv](https://github.com/astral-sh/uv)
