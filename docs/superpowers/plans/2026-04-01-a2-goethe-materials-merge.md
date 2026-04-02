# A2 Goethe-Institut Materials Merge — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge official Goethe-Institut A2 exam materials (2 PDFs, 1 Wortliste, 2 audio files) into the german repo — adding reference markdown exports, 26 new exercise JSONs, and enriched vocabulary with ~1,300 Goethe words.

**Architecture:** Four workstreams executed in dependency order: (1) schema extensions first (models), (2) audio transcription + PDF extraction in parallel, (3) vocabulary enrichment, (4) exercise conversion using extracted content. All new JSON follows existing conventions (`ensure_ascii=False`, `indent=2`, trailing newline, UTF-8).

**Tech Stack:** Python 3.12, Pydantic, pdfplumber (PDF extraction), faster-whisper (audio transcription via media-intelligence repo), uv, pytest, ruff

**Source files (all in `../library/docs/2026_Goethe-Institut_Deutsch-A2/`):**
- `A2_Modellsatz_Erwachsene.pdf` (44pp, 6 MB)
- `A2_Uebungssatz_Erwachsene.pdf` (44pp, 9 MB)
- `Goethe-Zertifikat_A2_Wortliste.pdf` (40pp, 400 KB)
- `pruefungstraining_1_hoeren_a2_erwachsene-v3.mp4` (14 MB)
- `pruefungstraining_2_hoeren_a2_erwachsene-v3.mp3` (35 MB)

---

## File Map

### New files to create
| File | Purpose |
|------|---------|
| `resources/reference/goethe-a2/modellsatz-erwachsene.md` | Markdown export of Modellsatz PDF |
| `resources/reference/goethe-a2/uebungssatz-erwachsene.md` | Markdown export of Übungssatz PDF |
| `resources/reference/goethe-a2/wortliste.md` | Markdown export of Wortliste PDF |
| `resources/exams/a2/{skill}/{teil}/uebung-06.json` | Modellsatz exercises (13 files) |
| `resources/exams/a2/{skill}/{teil}/uebung-07.json` | Übungssatz exercises (13 files) |
| `scripts/parse_wortliste.py` | Script to parse Wortliste PDF into vocabulary JSON |
| `scripts/extract_goethe_exercises.py` | Script to extract exercises from exam PDFs |

### Files to modify
| File | Change |
|------|--------|
| `src/german/models.py` | Add `VerbForms` model, extend `VocabularyWord` with new optional fields |
| `src/german/exams/models.py` | Add optional `source` field to all exercise models, `options_image_descriptions` to `Question` |
| `resources/vocabulary/nouns.json` | Add Goethe Wortliste nouns, enrich existing with examples |
| `resources/vocabulary/verbs.json` | Add Goethe Wortliste verbs, enrich existing with examples + verb forms |
| `resources/vocabulary/adjectives.json` | Add Goethe Wortliste adjectives, enrich existing with examples |
| `tests/test_models.py` | Add tests for `VerbForms`, new `VocabularyWord` fields |
| `tests/test_exam_models.py` | Add tests for `source` field, `options_image_descriptions` |
| `tests/test_a2_exercises.py` | Update exercise count 65 → 91, update per-teil counts 5 → 7 |
| `tests/test_vocabulary_levels.py` | Update minimum word count thresholds |

---

## Task 1: Extend Vocabulary Models

**Files:**
- Modify: `src/german/models.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: Write failing tests for VerbForms and new VocabularyWord fields**

Add to `tests/test_models.py`:

```python
from german.models import CEFRLevel, Gender, PartOfSpeech, VerbForms, VocabularyWord


def test_verb_forms_model():
    """Test VerbForms model for verb conjugation data."""
    forms = VerbForms(
        present_3p="holt ab",
        past_participle="abgeholt",
        auxiliary="hat",
    )
    assert forms.present_3p == "holt ab"
    assert forms.past_participle == "abgeholt"
    assert forms.auxiliary == "hat"


def test_verb_forms_partial():
    """Test VerbForms with only some fields."""
    forms = VerbForms(past_participle="gegangen", auxiliary="ist")
    assert forms.present_3p is None
    assert forms.past_participle == "gegangen"
    assert forms.auxiliary == "ist"


def test_vocabulary_word_with_examples():
    """Test VocabularyWord with example sentences."""
    word = VocabularyWord(
        german="kaufen",
        english="to buy",
        part_of_speech=PartOfSpeech.VERB,
        examples_de=["Tim kauft sich ein neues Auto.", "Ich habe das Buch gekauft."],
        examples_en=["Tim is buying a new car.", "I bought the book."],
    )
    assert len(word.examples_de) == 2
    assert len(word.examples_en) == 2


def test_vocabulary_word_with_verb_forms():
    """Test VocabularyWord with verb conjugation forms."""
    word = VocabularyWord(
        german="abholen",
        english="to pick up",
        part_of_speech=PartOfSpeech.VERB,
        verb_forms=VerbForms(
            present_3p="holt ab",
            past_participle="abgeholt",
            auxiliary="hat",
        ),
        separable_prefix=True,
    )
    assert word.verb_forms.present_3p == "holt ab"
    assert word.separable_prefix is True


def test_vocabulary_word_with_source():
    """Test VocabularyWord with source provenance."""
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.NEUTER,
        source="goethe-wortliste",
    )
    assert word.source == "goethe-wortliste"


def test_vocabulary_word_with_thematic_group():
    """Test VocabularyWord with thematic group."""
    word = VocabularyWord(
        german="Arzt",
        english="doctor",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.MASCULINE,
        thematic_group="Berufe",
    )
    assert word.thematic_group == "Berufe"


def test_vocabulary_word_backward_compatible():
    """Test that existing words without new fields still load."""
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.NEUTER,
        plural="Häuser",
        level="A1",
    )
    assert word.source is None
    assert word.examples_de is None
    assert word.verb_forms is None
    assert word.thematic_group is None
    assert word.separable_prefix is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_models.py -v -k "verb_forms or examples or source or thematic or backward_compatible"`
Expected: FAIL — `VerbForms` not defined, new fields not on `VocabularyWord`

- [ ] **Step 3: Implement VerbForms and extend VocabularyWord**

In `src/german/models.py`, add `VerbForms` class before `VocabularyWord` and extend `VocabularyWord`:

```python
class VerbForms(BaseModel):
    """Verb conjugation forms (e.g. from Goethe Wortliste)."""

    present_3p: Optional[str] = Field(None, description="3rd person present, e.g. 'holt ab'")
    past_participle: Optional[str] = Field(None, description="Past participle, e.g. 'abgeholt'")
    auxiliary: Optional[str] = Field(None, description="Auxiliary verb: 'hat' or 'ist'")

    model_config = ConfigDict(use_enum_values=True)
```

Add these fields to `VocabularyWord` (after existing fields, before `model_config`):

```python
    # Enrichment fields (all optional for backward compatibility)
    source: Optional[str] = Field(None, description="Content provenance: ai-generated, goethe-wortliste, both")
    examples_de: Optional[list[str]] = Field(None, description="German example sentences")
    examples_en: Optional[list[str]] = Field(None, description="English translations of examples")
    verb_forms: Optional[VerbForms] = Field(None, description="Verb conjugation forms")
    thematic_group: Optional[str] = Field(None, description="Thematic group, e.g. Berufe, Familie")
    separable_prefix: Optional[bool] = Field(None, description="True for separable prefix verbs")
```

Also add `VerbForms` to any `__all__` or re-exports if present.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_models.py -v`
Expected: ALL PASS (including existing tests — backward compatible)

- [ ] **Step 5: Run full test suite to verify no regressions**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS — existing vocabulary JSON loads fine since new fields are optional

- [ ] **Step 6: Commit**

```bash
git add src/german/models.py tests/test_models.py
git commit -m "feat: extend VocabularyWord with VerbForms, examples, source, thematic group"
```

---

## Task 2: Extend Exam Exercise Models

**Files:**
- Modify: `src/german/exams/models.py`
- Test: `tests/test_exam_models.py`

- [ ] **Step 1: Write failing tests for new exercise model fields**

Add to `tests/test_exam_models.py`:

```python
def test_question_with_image_descriptions():
    """Test Question with image-based answer options."""
    q = Question(
        number=11,
        type=QuestionType.MULTIPLE_CHOICE,
        text_de="Was hat das Mädchen gestern Abend gegessen?",
        correct_answer="a",
        options=["a", "b", "c"],
        options_image_descriptions=["Fisch auf Teller", "Hamburger", "Hähnchen mit Beilage"],
    )
    assert len(q.options_image_descriptions) == 3


def test_question_without_image_descriptions():
    """Test that options_image_descriptions is optional."""
    q = Question(
        number=1,
        type=QuestionType.MULTIPLE_CHOICE,
        text_de="Test?",
        correct_answer="a",
        options=["a) Ja", "b) Nein", "c) Vielleicht"],
    )
    assert q.options_image_descriptions is None


def test_listening_exercise_with_source():
    """Test ListeningExercise with source provenance field."""
    ex = ListeningExercise(
        id="a2-hoeren-teil-1-006",
        level="A2",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Test",
        instructions="Test instructions",
        time_minutes=8,
        transcript=[TranscriptLine(speaker="Test", text_de="Hallo", text_en="Hello")],
        questions=[Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="Test?", correct_answer="a", options=["a", "b", "c"])],
        source="goethe-modellsatz",
    )
    assert ex.source == "goethe-modellsatz"


def test_reading_exercise_with_source():
    """Test ReadingExercise with source provenance field."""
    ex = ReadingExercise(
        id="a2-lesen-teil-1-006",
        level="A2",
        skill=ExamSkill.LESEN,
        part=1,
        title="Test",
        instructions="Test instructions",
        time_minutes=8,
        passage=Passage(text_de="Text", text_en="Text", source="Zeitung", word_count=1),
        questions=[Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="Test?", correct_answer="a", options=["a", "b", "c"])],
        source="goethe-modellsatz",
    )
    assert ex.source == "goethe-modellsatz"


def test_exercise_source_optional():
    """Test that source field is optional (backward compatible)."""
    ex = ListeningExercise(
        id="a2-hoeren-teil-1-001",
        level="A2",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Test",
        instructions="Test",
        time_minutes=8,
        transcript=[TranscriptLine(speaker="Test", text_de="Hallo", text_en="Hello")],
        questions=[Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="Test?", correct_answer="a", options=["a", "b", "c"])],
    )
    assert ex.source is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_exam_models.py -v -k "image_descriptions or source"`
Expected: FAIL — fields don't exist

- [ ] **Step 3: Add optional fields to exam models**

In `src/german/exams/models.py`:

Add to `Question` (before `model_config`):
```python
    options_image_descriptions: Optional[list[str]] = Field(None, description="Textual descriptions of image-based answer options")
```

Add to each of `ListeningExercise`, `ReadingExercise`, `WritingExercise`, `SpeakingExercise` (before `model_config`):
```python
    source: Optional[str] = Field(None, description="Content provenance: ai-generated, goethe-modellsatz, goethe-uebungssatz")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_exam_models.py -v`
Expected: ALL PASS

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS — existing exercise JSON loads fine

- [ ] **Step 6: Commit**

```bash
git add src/german/exams/models.py tests/test_exam_models.py
git commit -m "feat: add source and options_image_descriptions to exam models"
```

---

## Task 3: Audio Transcription

**Files:**
- Output: `../media-intelligence/data/output/goethe-a2-modellsatz/` and `goethe-a2-uebungssatz/`

This task uses the media-intelligence repo to transcribe the audio files. The output is consumed by Task 6 (exercise conversion).

- [ ] **Step 1: Verify media-intelligence dependencies are installed**

```bash
cd /Users/stharrold/Documents/GitHub/media-intelligence && uv run python -c "import src.process_audio; print('OK')"
```

Expected: `OK`

- [ ] **Step 2: Create output directories**

```bash
mkdir -p /Users/stharrold/Documents/GitHub/media-intelligence/data/output/goethe-a2-modellsatz
mkdir -p /Users/stharrold/Documents/GitHub/media-intelligence/data/output/goethe-a2-uebungssatz
```

- [ ] **Step 3: Transcribe Modellsatz audio (MP4)**

```bash
cd /Users/stharrold/Documents/GitHub/media-intelligence
uv run python -m src.process_audio \
  /Users/stharrold/Documents/GitHub/library/docs/2026_Goethe-Institut_Deutsch-A2/pruefungstraining_1_hoeren_a2_erwachsene-v3.mp4 \
  -o data/output/goethe-a2-modellsatz/
```

Expected: `*_results.json` file with timestamped transcript segments in `data/output/goethe-a2-modellsatz/`

- [ ] **Step 4: Transcribe Übungssatz audio (MP3)**

```bash
cd /Users/stharrold/Documents/GitHub/media-intelligence
uv run python -m src.process_audio \
  /Users/stharrold/Documents/GitHub/library/docs/2026_Goethe-Institut_Deutsch-A2/pruefungstraining_2_hoeren_a2_erwachsene-v3.mp3 \
  -o data/output/goethe-a2-uebungssatz/
```

Expected: `*_results.json` file with timestamped transcript segments in `data/output/goethe-a2-uebungssatz/`

- [ ] **Step 5: Verify transcription output**

```bash
cd /Users/stharrold/Documents/GitHub/media-intelligence
ls -la data/output/goethe-a2-modellsatz/
ls -la data/output/goethe-a2-uebungssatz/
uv run python -c "
import json
for name in ['goethe-a2-modellsatz', 'goethe-a2-uebungssatz']:
    import glob
    files = glob.glob(f'data/output/{name}/**/*_results.json', recursive=True)
    for f in files:
        data = json.load(open(f))
        segments = data.get('transcription', {}).get('segments', [])
        print(f'{f}: {len(segments)} segments')
"
```

Expected: Both files have segments with German text

---

## Task 4: PDF Extraction to Markdown

**Files:**
- Create: `resources/reference/goethe-a2/modellsatz-erwachsene.md`
- Create: `resources/reference/goethe-a2/uebungssatz-erwachsene.md`
- Create: `resources/reference/goethe-a2/wortliste.md`

- [ ] **Step 1: Install pdfplumber in german repo if not present**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "import pdfplumber; print('OK')" 2>/dev/null || uv pip install pdfplumber
```

- [ ] **Step 2: Create reference directory**

```bash
mkdir -p /Users/stharrold/Documents/GitHub/german/resources/reference/goethe-a2
```

- [ ] **Step 3: Extract Modellsatz PDF to markdown**

Write a Python script that uses pdfplumber to extract text from all pages, then structure with section headers. Run it:

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "
import pdfplumber
from pathlib import Path

pdf_path = Path('../library/docs/2026_Goethe-Institut_Deutsch-A2/A2_Modellsatz_Erwachsene.pdf')
output_path = Path('resources/reference/goethe-a2/modellsatz-erwachsene.md')

lines = ['# Goethe-Zertifikat A2 — Modellsatz Erwachsene\n']
lines.append('> Source: A2_Modellsatz_Erwachsene.pdf, (C) Goethe-Institut 2016\n')

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines.append(f'\n---\n## Page {i+1}\n')
            lines.append(text + '\n')

output_path.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {len(lines)} lines to {output_path}')
"
```

- [ ] **Step 4: Extract Übungssatz PDF to markdown**

Same approach for the Übungssatz PDF:

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "
import pdfplumber
from pathlib import Path

pdf_path = Path('../library/docs/2026_Goethe-Institut_Deutsch-A2/A2_Uebungssatz_Erwachsene.pdf')
output_path = Path('resources/reference/goethe-a2/uebungssatz-erwachsene.md')

lines = ['# Goethe-Zertifikat A2 — Übungssatz 01 Erwachsene\n']
lines.append('> Source: A2_Uebungssatz_Erwachsene.pdf, (C) Goethe-Institut 2020\n')

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines.append(f'\n---\n## Page {i+1}\n')
            lines.append(text + '\n')

output_path.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {len(lines)} lines to {output_path}')
"
```

- [ ] **Step 5: Extract Wortliste PDF to markdown**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "
import pdfplumber
from pathlib import Path

pdf_path = Path('../library/docs/2026_Goethe-Institut_Deutsch-A2/Goethe-Zertifikat_A2_Wortliste.pdf')
output_path = Path('resources/reference/goethe-a2/wortliste.md')

lines = ['# Goethe-Zertifikat A2 — Wortliste\n']
lines.append('> Source: Goethe-Zertifikat_A2_Wortliste.pdf, (C) Goethe-Institut 2016\n')

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines.append(f'\n---\n## Page {i+1}\n')
            lines.append(text + '\n')

output_path.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {len(lines)} lines to {output_path}')
"
```

- [ ] **Step 6: Verify markdown files are readable**

```bash
wc -l resources/reference/goethe-a2/*.md
head -20 resources/reference/goethe-a2/modellsatz-erwachsene.md
```

Expected: Three markdown files with substantial content

- [ ] **Step 7: Commit**

```bash
git add resources/reference/goethe-a2/
git commit -m "docs: add markdown exports of Goethe A2 PDFs (Modellsatz, Übungssatz, Wortliste)"
```

---

## Task 5: Parse Wortliste and Enrich Vocabulary

**Files:**
- Create: `scripts/parse_wortliste.py`
- Modify: `resources/vocabulary/nouns.json`
- Modify: `resources/vocabulary/verbs.json`
- Modify: `resources/vocabulary/adjectives.json`
- Modify: `tests/test_vocabulary_levels.py`

This is the most complex task. The Wortliste PDF has ~1,300 entries in a two-column layout with entries like:
- `der Apfel, ¨-e` + example sentence (noun)
- `abholen, holt ab, hat abgeholt` + example sentence (verb)
- `billig` + example sentence (adjective)

- [ ] **Step 1: Write the Wortliste parser script**

Create `scripts/parse_wortliste.py`. This script:
1. Opens the Wortliste markdown (from Task 4) or PDF directly
2. Parses each entry into the enriched `VocabularyWord` schema
3. Detects part of speech from article/form patterns
4. Generates English translations for Goethe-only entries
5. Merges with existing vocabulary (dedup by german + part_of_speech)
6. Outputs updated `nouns.json`, `verbs.json`, `adjectives.json`

```python
#!/usr/bin/env python3
"""Parse Goethe A2 Wortliste and merge with existing vocabulary."""

import json
import re
from pathlib import Path


def parse_wortliste_markdown(md_path: Path) -> list[dict]:
    """Parse Wortliste markdown into raw vocabulary entries.
    
    Returns list of dicts with keys: german, gender, plural, verb_forms, 
    examples_de, thematic_group, separable_prefix, part_of_speech_hint.
    """
    text = md_path.read_text(encoding="utf-8")
    entries = []
    
    # Pattern for noun entries: "der/die/das Word, -plural"
    noun_pattern = re.compile(
        r"^(der|die|das)\s+(\w[\w\-]+)(?:,\s*(.+?))?$", re.MULTILINE
    )
    
    # Pattern for verb entries: "word, 3p present, past participle"
    verb_pattern = re.compile(
        r"^(\w+(?:\s*\(sich\))?),\s*(\w[\w\s]+),\s*(hat|ist)\s+(\w+)$", re.MULTILINE
    )
    
    # This is a starting point — the actual parser will need to handle
    # the two-column layout and various entry formats from the PDF.
    # Implementation should read the extracted markdown line by line
    # and classify each entry.
    
    return entries


def load_existing_vocab(vocab_dir: Path) -> dict[str, list[dict]]:
    """Load existing vocabulary JSON files."""
    result = {}
    for f in vocab_dir.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        result[f.stem] = data.get("words", [])
    return result


def merge_vocabularies(existing: list[dict], goethe: list[dict]) -> list[dict]:
    """Merge existing and Goethe vocabulary, deduplicating by german+POS."""
    seen = {}
    for word in existing:
        key = (word["german"].lower(), word["part_of_speech"])
        word.setdefault("source", "ai-generated")
        seen[key] = word
    
    for word in goethe:
        key = (word["german"].lower(), word["part_of_speech"])
        if key in seen:
            # Merge: add Goethe data to existing entry
            existing_word = seen[key]
            existing_word["source"] = "both"
            if word.get("examples_de"):
                existing_word["examples_de"] = word["examples_de"]
            if word.get("examples_en"):
                existing_word["examples_en"] = word["examples_en"]
            if word.get("verb_forms"):
                existing_word["verb_forms"] = word["verb_forms"]
            if word.get("thematic_group"):
                existing_word["thematic_group"] = word["thematic_group"]
            if word.get("separable_prefix") is not None:
                existing_word["separable_prefix"] = word["separable_prefix"]
        else:
            word.setdefault("source", "goethe-wortliste")
            seen[key] = word
    
    return sorted(seen.values(), key=lambda w: w["german"].lower())


def write_vocab_json(words: list[dict], output_path: Path):
    """Write vocabulary JSON with proper formatting."""
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump({"words": words}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    wortliste_md = repo_root / "resources" / "reference" / "goethe-a2" / "wortliste.md"
    vocab_dir = repo_root / "resources" / "vocabulary"
    
    # Parse Wortliste
    goethe_entries = parse_wortliste_markdown(wortliste_md)
    print(f"Parsed {len(goethe_entries)} Goethe Wortliste entries")
    
    # Load existing
    existing = load_existing_vocab(vocab_dir)
    
    # Merge and write
    for category in ["nouns", "verbs", "adjectives"]:
        goethe_cat = [e for e in goethe_entries if e.get("_category") == category]
        merged = merge_vocabularies(existing.get(category, []), goethe_cat)
        output = vocab_dir / f"{category}.json"
        write_vocab_json(merged, output)
        print(f"Wrote {len(merged)} words to {output}")
```

The parser implementation must handle the Wortliste's specific format. Key patterns:
- Nouns: `der/die/das Word, -plural` or `der/die/das Word (Sg.)` (uncountable)
- Verbs: `infinitive, 3p present, hat/ist past_participle`
- Adjectives/adverbs: bare word with example sentences
- Separable prefix verbs: `(ab)fahren, fährt (ab), ist (ab)gefahren`
- Thematic groups appear as section headers in Wortgruppen (pp.5-7)

- [ ] **Step 2: Run the parser and inspect output**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python scripts/parse_wortliste.py
```

Expected: Prints counts of parsed and merged words

- [ ] **Step 3: Validate merged vocabulary loads through Pydantic**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "
from german.vocabulary import load_vocabulary
vocab = load_vocabulary()
print(f'Total words: {len(vocab)}')
sources = {}
for w in vocab:
    s = getattr(w, 'source', None) or 'unknown'
    sources[s] = sources.get(s, 0) + 1
for s, c in sorted(sources.items()):
    print(f'  {s}: {c}')
"
```

Expected: Total significantly higher than 960, with ai-generated + goethe-wortliste + both sources

- [ ] **Step 4: Update vocabulary test thresholds**

In `tests/test_vocabulary_levels.py`, update minimum counts:

```python
def test_noun_count_minimum():
    """Test minimum noun count across levels."""
    nouns = load_vocabulary(category="nouns")
    assert len(nouns) >= 600, f"Expected >= 600 nouns, got {len(nouns)}"


def test_verb_count_minimum():
    """Test minimum verb count across levels."""
    verbs = load_vocabulary(category="verbs")
    assert len(verbs) >= 400, f"Expected >= 400 verbs, got {len(verbs)}"


def test_adjective_count_minimum():
    """Test minimum adjective count across levels."""
    adjectives = load_vocabulary(category="adjectives")
    assert len(adjectives) >= 300, f"Expected >= 300 adjectives, got {len(adjectives)}"


def test_total_vocabulary_minimum():
    """Test total vocabulary meets minimum threshold."""
    vocab = load_vocabulary()
    assert len(vocab) >= 1200, f"Expected >= 1200 total words, got {len(vocab)}"
```

Note: Exact thresholds depend on actual parsing results. Adjust after Step 3.

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/parse_wortliste.py resources/vocabulary/ tests/test_vocabulary_levels.py
git commit -m "feat: parse Goethe A2 Wortliste and merge with existing vocabulary"
```

---

## Task 6: Convert Modellsatz Exercises to JSON

**Files:**
- Create: 13 new `uebung-06.json` files across `resources/exams/a2/`
- Create: `scripts/extract_goethe_exercises.py`

This task converts the Modellsatz PDF content (already extracted to markdown in Task 4) into JSON exercise files following the existing schema. Uses answer keys from p.32 and transcripts from pp.33-36 of the PDF (cross-referenced with Whisper output from Task 3).

- [ ] **Step 1: Create the exercise extraction script**

Create `scripts/extract_goethe_exercises.py`. This script reads the markdown exports and creates JSON exercise files. Due to the complexity of parsing PDFs with mixed text/images, this script will be a structured template that the implementer fills in with the actual content from the PDFs.

For each exercise, the script must:
1. Extract the passage/transcript/situation text
2. Extract questions with options
3. Map answer keys from the Lösungen page
4. Generate English translations for all German text
5. Write JSON files with `ensure_ascii=False, indent=2` + trailing newline

- [ ] **Step 2: Create Lesen exercises (4 files)**

Create `uebung-06.json` for each Lesen teil:

**teil-1** (p.6-7): Newspaper article about Stefan Berger + 5 multiple choice questions
**teil-2** (p.8-9): Kaufhaus Alexa information board + 5 matching questions (Zuordnen)
**teil-3** (p.10-11): Email from Gülcan + 5 multiple choice questions
**teil-4** (p.12-13): 6 restaurant ads matched to 5 people + 5 matching questions

Each file follows the `ReadingExercise` schema. Example ID format: `a2-lesen-teil-1-006`.

- [ ] **Step 3: Create Hören exercises (4 files)**

Create `uebung-06.json` for each Hören teil, using transcripts from p.33-36 cross-referenced with Whisper output:

**teil-1** (p.16, transcript p.33): 5 short radio announcements → 5 multiple choice
**teil-2** (p.17, transcript p.34): Weekly planning conversation → 5 picture matching (use `options_image_descriptions`)
**teil-3** (p.18, transcript p.35): 5 short conversations → 5 picture-based multiple choice (use `options_image_descriptions`)
**teil-4** (p.19, transcript p.36): Interview with Sarah → 5 Richtig/Falsch (true/false)

- [ ] **Step 4: Create Schreiben exercises (2 files)**

Create `uebung-06.json` for each Schreiben aufgabe:

**aufgabe-1** (p.22 top): SMS to friend Ekaterini — 3 required points, 20-30 words
**aufgabe-2** (p.22 bottom): Email to boss Herr Lehmann — 3 required points, 30-40 words

Include model answers and scoring criteria from p.37-40.

- [ ] **Step 5: Create Sprechen exercises (3 files)**

Create `uebung-06.json` for each Sprechen teil:

**teil-1** (p.24): Question cards — Geburtstag? Wohnort? Beruf? Hobby?
**teil-2** (p.25): Theme cards — "Was machen Sie mit Ihrem Geld?" / "Was machen Sie oft am Wochenende?"
**teil-3** (p.26-27): Schedule planning — buy birthday present for Patrick

Include model dialogues and evaluation criteria from p.41-42.

- [ ] **Step 6: Validate all 13 new Modellsatz exercises load**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "
from pathlib import Path
from german.exams.loader import load_exercise
from german.exams.models import ListeningExercise, ReadingExercise, WritingExercise, SpeakingExercise

a2_dir = Path('resources/exams/a2')
errors = []
count = 0

for teil in range(1, 5):
    f = a2_dir / 'lesen' / f'teil-{teil}' / 'uebung-06.json'
    try:
        load_exercise(f, ReadingExercise)
        count += 1
    except Exception as e:
        errors.append(f'{f}: {e}')

for teil in range(1, 5):
    f = a2_dir / 'hoeren' / f'teil-{teil}' / 'uebung-06.json'
    try:
        load_exercise(f, ListeningExercise)
        count += 1
    except Exception as e:
        errors.append(f'{f}: {e}')

for aufgabe in range(1, 3):
    f = a2_dir / 'schreiben' / f'aufgabe-{aufgabe}' / 'uebung-06.json'
    try:
        load_exercise(f, WritingExercise)
        count += 1
    except Exception as e:
        errors.append(f'{f}: {e}')

for teil in range(1, 4):
    f = a2_dir / 'sprechen' / f'teil-{teil}' / 'uebung-06.json'
    try:
        load_exercise(f, SpeakingExercise)
        count += 1
    except Exception as e:
        errors.append(f'{f}: {e}')

print(f'Loaded {count}/13 exercises')
for e in errors:
    print(f'  ERROR: {e}')
"
```

Expected: `Loaded 13/13 exercises`

- [ ] **Step 7: Commit**

```bash
git add resources/exams/a2/*/uebung-06.json scripts/extract_goethe_exercises.py
git commit -m "feat: add Goethe A2 Modellsatz exercises (13 exercises, uebung-06)"
```

---

## Task 7: Convert Übungssatz Exercises to JSON

**Files:**
- Create: 13 new `uebung-07.json` files across `resources/exams/a2/`

Same structure as Task 6, but using Übungssatz PDF content. The Übungssatz has identical structure (confirmed from TOC on p.1): Lesen p.5, Hören p.15, Schreiben p.21, Sprechen p.23, Lösungen p.32, Transkripte p.33.

- [ ] **Step 1: Read Übungssatz PDF to extract all content**

Read all pages of the Übungssatz PDF to extract questions, passages, transcripts, and answer keys. The structure mirrors the Modellsatz exactly.

- [ ] **Step 2: Create all 13 Übungssatz exercise JSON files**

Create `uebung-07.json` for every teil/aufgabe, following the same patterns as Task 6. Exercise IDs use format `a2-{skill}-teil-{N}-007`.

Set `"source": "goethe-uebungssatz"` on all exercises.

- [ ] **Step 3: Validate all 13 new Übungssatz exercises load**

Same validation script as Task 6 Step 6, but checking `uebung-07.json` files.

- [ ] **Step 4: Commit**

```bash
git add resources/exams/a2/*/uebung-07.json
git commit -m "feat: add Goethe A2 Übungssatz exercises (13 exercises, uebung-07)"
```

---

## Task 8: Update Tests and Counts

**Files:**
- Modify: `tests/test_a2_exercises.py`

- [ ] **Step 1: Update exercise count assertions**

In `tests/test_a2_exercises.py`, update all count assertions:

Change `test_a2_hoeren_exercises_exist`:
```python
    assert len(exercises) == 7, f"Expected 7 exercises in teil-{teil}, found {len(exercises)}"
```

Change `test_a2_hoeren_exercises_valid`:
```python
    assert len(exercises) == 7
```

Change `test_a2_lesen_exercises_exist`:
```python
    assert len(exercises) == 7, f"Expected 7 exercises in teil-{teil}, found {len(exercises)}"
```

Change `test_a2_lesen_exercises_valid`:
```python
    assert len(exercises) == 7
```

Change `test_a2_schreiben_exercises_exist`:
```python
    assert len(exercises) == 7, f"Expected 7 exercises in aufgabe-{aufgabe}, found {len(exercises)}"
```

Change `test_a2_schreiben_exercises_valid`:
```python
    assert len(exercises) == 7
```

Change `test_a2_sprechen_exercises_exist`:
```python
    assert len(exercises) == 7, f"Expected 7 exercises in teil-{teil}, found {len(exercises)}"
```

Change `test_a2_sprechen_exercises_valid`:
```python
    assert len(exercises) == 7
```

Change `test_a2_total_exercise_count`:
```python
    assert count == 91, f"Expected 91 exercises, found {count}"
```

- [ ] **Step 2: Add test for source field on Goethe exercises**

Add to `tests/test_a2_exercises.py`:

```python
def test_a2_goethe_exercises_have_source():
    """Test that Goethe exercises have source field set."""
    import json
    for f in A2_DIR.glob("**/uebung-06.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("source") == "goethe-modellsatz", f"Missing source in {f}"
    for f in A2_DIR.glob("**/uebung-07.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("source") == "goethe-uebungssatz", f"Missing source in {f}"
```

- [ ] **Step 3: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 4: Run linting**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: Clean

- [ ] **Step 5: Commit**

```bash
git add tests/test_a2_exercises.py
git commit -m "test: update A2 exercise counts 65->91, add Goethe source validation"
```

---

## Task 9: Version Bump and Finalize

**Files:**
- Modify: `pyproject.toml`
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Bump version to v2.9.0**

In `pyproject.toml`, change `version = "2.8.0"` to `version = "2.9.0"`.

- [ ] **Step 2: Update CHANGELOG.md**

Add entry at top of changelog:

```markdown
## [v2.9.0] - 2026-04-01

### Added
- Official Goethe-Institut A2 materials integration
  - 26 new exercises from Modellsatz + Übungssatz (A2 total: 65 → 91)
  - Markdown reference exports of all 3 Goethe PDFs
  - Audio transcription of Hören practice files via faster-whisper
- Enriched vocabulary schema with example sentences, verb forms, thematic groups
  - `VerbForms` model for German verb conjugation patterns
  - Merged ~1,300 Goethe Wortliste entries with existing 960-word collection
  - `source` provenance tracking on all vocabulary entries
- `source` field on all exam exercise models for content provenance
- `options_image_descriptions` field for image-based answer options
```

- [ ] **Step 3: Update CLAUDE.md status section**

Update the Status section to reflect the new state.

- [ ] **Step 4: Commit uv.lock if changed**

```bash
cd /Users/stharrold/Documents/GitHub/german
uv run python -c "pass"  # triggers uv.lock update
git add pyproject.toml uv.lock CHANGELOG.md CLAUDE.md
git commit -m "chore: bump version to v2.9.0, update CHANGELOG and CLAUDE.md"
```

- [ ] **Step 5: Final full test run**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

---

## Dependencies Between Tasks

```
Task 1 (Vocab models)  ──→  Task 5 (Wortliste parse)
Task 2 (Exam models)   ──→  Task 6 (Modellsatz exercises)  ──→  Task 8 (Update tests)
Task 3 (Audio)         ──→  Task 6 (Modellsatz exercises)
Task 4 (PDF extract)   ──→  Task 5 (Wortliste parse)
Task 4 (PDF extract)   ──→  Task 6 (Modellsatz exercises)
Task 6 (Modellsatz)    ──→  Task 7 (Übungssatz exercises)   ──→  Task 8 (Update tests)
Task 8 (Update tests)  ──→  Task 9 (Version bump)
```

**Parallelizable:** Tasks 1+2 (models), Tasks 3+4 (extraction), Tasks 6+7 (exercises, if content available)
