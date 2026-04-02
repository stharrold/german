# A2 Goethe-Institut Materials Merge — Design Spec

**Date**: 2026-04-01
**Status**: Approved
**Scope**: Merge official Goethe-Institut A2 exam materials into the german repo

## Overview

Integrate five Goethe-Institut A2 source files from `../library/docs/2026_Goethe-Institut_Deutsch-A2/` into this repo across four workstreams: reference storage, exercise conversion, vocabulary enrichment, and audio transcription.

## Source Materials

| File | Size | Content |
|------|------|---------|
| `A2_Modellsatz_Erwachsene.pdf` | 6 MB, 44pp | Complete model exam (Lesen 4T, Hören 4T, Schreiben 2T, Sprechen 3T) + answer keys, transcripts, scoring rubrics |
| `A2_Uebungssatz_Erwachsene.pdf` | 9 MB | Second complete practice exam (same structure, different content) |
| `Goethe-Zertifikat_A2_Wortliste.pdf` | 400 KB | ~1,300 lexical entries with example sentences, thematic groupings |
| `pruefungstraining_1_hoeren_a2_erwachsene-v3.mp4` | 14 MB | Audio for Modellsatz Hören |
| `pruefungstraining_2_hoeren_a2_erwachsene-v3.mp3` | 35 MB | Audio for Übungssatz Hören |

## Workstream 1: Reference Storage

Store markdown exports of all three PDFs for programmatic access. PDFs stay in `../library/` (copyrighted binaries not committed).

### Output

```
resources/reference/goethe-a2/
├── modellsatz-erwachsene.md
├── uebungssatz-erwachsene.md
└── wortliste.md
```

### Tooling

Use the `library` repo's `pipe_01_extract.py` (PDF text extraction) to convert PDFs to clean text, then structure into markdown with section headers matching the PDF's table of contents.

## Workstream 2: Exercise Conversion

Convert both exam sets into the existing JSON exercise format. Files are named `uebung-06.json` (Modellsatz) and `uebung-07.json` (Übungssatz) — continuing the numbering from the existing 5 AI-generated exercises per teil.

### Output Structure

```
resources/exams/a2/
├── hoeren/teil-{1-4}/uebung-06.json    # Modellsatz
├── hoeren/teil-{1-4}/uebung-07.json    # Übungssatz
├── lesen/teil-{1-4}/uebung-06.json
├── lesen/teil-{1-4}/uebung-07.json
├── schreiben/aufgabe-{1-2}/uebung-06.json
├── schreiben/aufgabe-{1-2}/uebung-07.json
├── sprechen/teil-{1-3}/uebung-06.json
└── sprechen/teil-{1-3}/uebung-07.json
```

### Exercise Count

- Existing: 65 AI-generated exercises (5 per teil)
- Modellsatz: 13 exercises (4 Lesen + 4 Hören + 2 Schreiben + 3 Sprechen)
- Übungssatz: 13 exercises (same structure)
- **Total: 91 A2 exercises**

### New JSON Fields

Added to exercise JSON (backward-compatible, optional):

- `"source": "goethe-modellsatz"` or `"goethe-uebungssatz"` — provenance tracking
- Existing AI-generated exercises get `"source": "ai-generated"` backfilled

### Answer Keys

Extracted from the Lösungen pages in each PDF (filled answer sheet scans).

### Hören Transcripts

Transcripts come from two sources and are cross-referenced:
1. PDF transcripts (Modellsatz pp.33-36)
2. Audio transcripts from media-intelligence Whisper pipeline (Workstream 4)

## Workstream 3: Vocabulary Enrichment

Extend the vocabulary schema to accommodate both the existing AI-generated words and the Goethe Wortliste, then merge into unified JSON files.

### Schema Extension

New Pydantic model in `src/german/models.py`:

```python
class VerbForms(BaseModel):
    """Verb conjugation forms from Goethe Wortliste."""
    present_3p: str | None = None      # 3rd person present, e.g. "holt ab"
    past_participle: str | None = None  # e.g. "hat abgeholt"
    auxiliary: str | None = None        # "hat" or "ist"

class VocabularyWord(BaseModel):
    # --- existing fields (unchanged) ---
    german: str
    english: str
    part_of_speech: PartOfSpeech
    gender: Gender | None = None
    plural: str | None = None
    cefr_level: str | None = None
    # --- new fields (all optional for backward compatibility) ---
    source: str | None = None              # "ai-generated" | "goethe-wortliste" | "both"
    examples_de: list[str] | None = None   # German example sentences
    examples_en: list[str] | None = None   # English translations of examples
    verb_forms: VerbForms | None = None    # Verb conjugation forms
    thematic_group: str | None = None      # "Berufe", "Familie", "Farben", etc.
    separable_prefix: bool | None = None   # True for verbs like abholen, anfangen
```

All new fields default to `None` — existing JSON files load without changes.

### Merge Strategy

Three cases:

1. **Words in both sources**: Merge fields from both, set `source: "both"`. Goethe provides example sentences and verb forms; AI provides English translations.
2. **Words only in AI set** (960 existing): Enrich with generated example sentences and verb forms, set `source: "ai-generated"`.
3. **Words only in Goethe** (~1,300 minus overlap): Generate English translations and classify part of speech, set `source: "goethe-wortliste"`.

### Wortliste Parsing

The Goethe Wortliste PDF has two sections:
- **Wortgruppen** (pp.5-7): Thematic groups (Berufe, Familienmitglieder, Farben, Himmelsrichtungen, Länder, Schulfächer, Währungen, Zeitangaben, Zahlen)
- **Alphabetischer Wortschatz** (pp.8+): Alphabetical entries with example sentences

Each alphabetical entry follows the pattern:
```
der Apfel, ¨-e    Ein Kilo Äpfel, bitte.
abholen, holt ab, hat abgeholt    Wann kann ich die Sachen bei dir abholen?
```

Parsing rules:
- Article prefix (`der/die/das`) → gender
- Plural suffix (e.g., `-e`, `-en`, `¨-er`) → plural form
- Verb with 3 forms → `VerbForms`
- No article, no verb forms → adjective/adverb/other
- Separable prefix verbs identified by `prefix ab/an/auf/aus/ein/mit/vor/zu/...` pattern

## Workstream 4: Audio Transcription

Use media-intelligence pipeline (faster-whisper, local CPU) to transcribe both audio files.

### Commands

```bash
cd /Users/stharrold/Documents/GitHub/media-intelligence

# Modellsatz audio (MP4, 14 MB)
uv run python -m src.process_audio \
  /Users/stharrold/Documents/GitHub/library/docs/2026_Goethe-Institut_Deutsch-A2/pruefungstraining_1_hoeren_a2_erwachsene-v3.mp4 \
  -o data/output/goethe-a2-modellsatz/

# Übungssatz audio (MP3, 35 MB)
uv run python -m src.process_audio \
  /Users/stharrold/Documents/GitHub/library/docs/2026_Goethe-Institut_Deutsch-A2/pruefungstraining_2_hoeren_a2_erwachsene-v3.mp3 \
  -o data/output/goethe-a2-uebungssatz/
```

### Output

Each produces a `*_results.json` with:
- Timestamped transcript segments
- Speaker diarization (who speaks when)
- Language detection confirmation

### Cross-Validation

Diff Whisper transcripts against PDF transcripts (Modellsatz pp.33-36) to:
- Catch OCR errors in PDF extraction
- Identify Whisper hallucinations
- Produce final verified transcripts for the exercise JSON files

## Execution Order

1. **Audio transcription** (Workstream 4) — longest running, start first
2. **PDF extraction to markdown** (Workstream 1) — can run in parallel with audio
3. **Vocabulary schema extension + Wortliste parsing + merge** (Workstream 3)
4. **Exercise conversion** (Workstream 2) — depends on transcripts from step 1 and content from step 2
5. **Tests** — update test counts, validate all new JSON, run full suite
6. **Version bump** to v2.9.0 + CHANGELOG update

## Test Updates

- Update A2 exercise count assertions: 65 → 91
- Add tests for new `VerbForms` model
- Add tests for new vocabulary fields (`examples_de`, `examples_en`, `thematic_group`, `separable_prefix`)
- Validate all new JSON files load through Pydantic models
- Verify `source` field present on all vocabulary entries

## Model Adjustments

### Exam Exercise Models

All four exercise models (`ListeningExercise`, `ReadingExercise`, `WritingExercise`, `SpeakingExercise`) get a new optional field:

```python
source: str | None = Field(None, description="Content provenance: ai-generated, goethe-modellsatz, goethe-uebungssatz")
```

### Image-Based Answer Options

Goethe A2 Hören Teil 2 uses picture-matching (9 images labeled a-i, matched to days of the week) and Teil 3 uses picture-based multiple choice (3 images per question). Since `Question.options` is `list[str]`, describe images textually:

- Teil 2: `["a) Paar tanzt", "b) Kinobesuch", "c) Schwimmbad", ...]`
- Teil 3: `["a) Fisch auf Teller", "b) Hamburger", "c) Hähnchen"]`

Add an optional field to `Question` for image descriptions:

```python
options_image_descriptions: list[str] | None = Field(None, description="Textual descriptions of image-based answer options")
```

### TranscriptLine.text_en

`TranscriptLine.text_en` is currently required (`str`, not `Optional`). Goethe transcripts are German-only. For Goethe exercises, generate English translations of all transcript lines to satisfy the schema.

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Whisper misrecognizes German audio | Cross-validate with PDF transcripts |
| Wortliste PDF parsing errors (multi-column layout) | Use pdfplumber with layout-aware extraction |
| Goethe Hören Teil 2/3 use images as answer options | Describe images textually in JSON (`options_description` field) |
| Vocabulary overlap detection misses near-matches | Normalize German words (lowercase, strip articles) before matching |
| Test count changes break CI | Update all assertion counts in a single commit |

## Attribution

All Goethe-Institut materials are © Goethe-Institut 2016. The `source` field on exercises and vocabulary entries provides clear provenance tracking. Markdown reference files include the original Impressum.
