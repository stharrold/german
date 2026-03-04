# B1 Exam Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Pydantic models, loader/query modules, directory structure, and validation tests for B1 exam practice exercises (issues #278-281).

**Architecture:** Mirror the existing `src/german/vocabulary/` pattern — models define schemas, loader deserializes JSON, query filters collections. The new `src/german/exams/` package sits alongside `vocabulary/` under the `german` namespace. Resources live in `resources/exams/b1/` with one JSON file per exercise.

**Tech Stack:** Python 3.11+, Pydantic v2, pytest, ruff, uv

---

## Task 1: Create Pydantic exam models (#278)

**Files:**
- Create: `src/german/exams/__init__.py`
- Create: `src/german/exams/models.py`
- Test: `tests/test_exam_models.py`

### Step 1: Write failing tests for exam models

Create `tests/test_exam_models.py` with tests for every model. Follow the pattern from `tests/test_models.py` — one test per model, one test per validation rule.

```python
"""Tests for B1 exam exercise models."""

import pytest
from pydantic import ValidationError

from german.exams.models import (
    ExamMeta,
    ExamSkill,
    ListeningExercise,
    ModelAnswer,
    Passage,
    Question,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    TranscriptLine,
    WritingExercise,
)


# --- ExamMeta ---


def test_exam_meta_valid():
    """Test creating valid exam metadata."""
    meta = ExamMeta(
        level="B1",
        provider="Goethe-Institut",
        total_time_minutes=190,
        passing_score_percent=60,
    )
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"
    assert meta.total_time_minutes == 190
    assert meta.passing_score_percent == 60


def test_exam_meta_missing_level():
    """Test that level is required."""
    with pytest.raises(ValidationError):
        ExamMeta(
            provider="Goethe-Institut",
            total_time_minutes=190,
            passing_score_percent=60,
        )


# --- QuestionType enum ---


def test_question_type_values():
    """Test all question type enum values."""
    assert QuestionType.TRUE_FALSE == "true_false"
    assert QuestionType.MULTIPLE_CHOICE == "multiple_choice"
    assert QuestionType.MATCHING == "matching"


# --- ExamSkill enum ---


def test_exam_skill_values():
    """Test all exam skill enum values."""
    assert ExamSkill.HOEREN == "hoeren"
    assert ExamSkill.LESEN == "lesen"
    assert ExamSkill.SCHREIBEN == "schreiben"
    assert ExamSkill.SPRECHEN == "sprechen"


# --- Question ---


def test_question_true_false():
    """Test creating a true/false question."""
    q = Question(
        number=1,
        type=QuestionType.TRUE_FALSE,
        text_de="Der Mann arbeitet in Berlin.",
        text_en="The man works in Berlin.",
        correct_answer=True,
        explanation_de="Im Text steht, dass er in Berlin arbeitet.",
        explanation_en="The text states that he works in Berlin.",
    )
    assert q.number == 1
    assert q.type == QuestionType.TRUE_FALSE
    assert q.correct_answer is True


def test_question_multiple_choice():
    """Test creating a multiple choice question."""
    q = Question(
        number=1,
        type=QuestionType.MULTIPLE_CHOICE,
        text_de="Was macht der Mann?",
        text_en="What does the man do?",
        correct_answer="a",
        options=["a) Er arbeitet.", "b) Er schläft.", "c) Er isst."],
        explanation_de="Er arbeitet in einem Büro.",
        explanation_en="He works in an office.",
    )
    assert q.correct_answer == "a"
    assert len(q.options) == 3


def test_question_missing_number():
    """Test that question number is required."""
    with pytest.raises(ValidationError):
        Question(
            type=QuestionType.TRUE_FALSE,
            text_de="Test",
            correct_answer=True,
        )


# --- TranscriptLine ---


def test_transcript_line():
    """Test creating a transcript line."""
    line = TranscriptLine(
        speaker="narrator",
        text_de="Guten Tag, meine Damen und Herren.",
        text_en="Good day, ladies and gentlemen.",
    )
    assert line.speaker == "narrator"
    assert "Guten Tag" in line.text_de


def test_transcript_line_umlaut():
    """Test transcript line with umlauts."""
    line = TranscriptLine(
        speaker="Sprecher",
        text_de="Ich möchte über die Prüfung sprechen.",
        text_en="I would like to talk about the exam.",
    )
    assert "ö" in line.text_de
    assert "ü" in line.text_de


# --- ListeningExercise ---


def test_listening_exercise_valid():
    """Test creating a valid listening exercise."""
    exercise = ListeningExercise(
        id="b1-hoeren-teil-1-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Telefonische Nachrichten",
        instructions="Sie hören fünf kurze Texte. Sie hören jeden Text zweimal.",
        time_minutes=10,
        transcript=[
            TranscriptLine(
                speaker="narrator",
                text_de="Nachricht eins.",
                text_en="Message one.",
            )
        ],
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="Der Anrufer möchte einen Termin.",
                text_en="The caller wants an appointment.",
                correct_answer=True,
                explanation_de="Er sagt, er braucht einen Termin.",
                explanation_en="He says he needs an appointment.",
            )
        ],
    )
    assert exercise.id == "b1-hoeren-teil-1-001"
    assert exercise.skill == ExamSkill.HOEREN
    assert exercise.part == 1
    assert len(exercise.transcript) == 1
    assert len(exercise.questions) == 1


def test_listening_exercise_missing_transcript():
    """Test that transcript is required for listening."""
    with pytest.raises(ValidationError):
        ListeningExercise(
            id="b1-hoeren-teil-1-001",
            level="B1",
            skill=ExamSkill.HOEREN,
            part=1,
            title="Test",
            instructions="Test",
            time_minutes=10,
            questions=[],
        )


# --- Passage & ReadingExercise ---


def test_passage():
    """Test creating a passage."""
    p = Passage(
        text_de="Ich bin heute in die Stadt gegangen.",
        text_en="I went to the city today.",
        source="Blog post",
        word_count=350,
    )
    assert p.source == "Blog post"
    assert p.word_count == 350


def test_reading_exercise_valid():
    """Test creating a valid reading exercise."""
    exercise = ReadingExercise(
        id="b1-lesen-teil-1-001",
        level="B1",
        skill=ExamSkill.LESEN,
        part=1,
        title="Blog: Mein erster Tag",
        instructions="Lesen Sie den Text und die Aufgaben 1 bis 6.",
        time_minutes=13,
        passage=Passage(
            text_de="Ein langer Text...",
            text_en="A long text...",
            source="Blog post",
            word_count=350,
        ),
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="Der Autor ist nervös.",
                correct_answer=True,
                explanation_de="Er schreibt, dass er aufgeregt war.",
            )
        ],
    )
    assert exercise.id == "b1-lesen-teil-1-001"
    assert exercise.passage.word_count == 350


def test_reading_exercise_missing_passage():
    """Test that passage is required for reading."""
    with pytest.raises(ValidationError):
        ReadingExercise(
            id="b1-lesen-teil-1-001",
            level="B1",
            skill=ExamSkill.LESEN,
            part=1,
            title="Test",
            instructions="Test",
            time_minutes=13,
            questions=[],
        )


# --- ModelAnswer & WritingExercise ---


def test_model_answer():
    """Test creating a model answer."""
    ma = ModelAnswer(
        text_de="Liebe Maria, vielen Dank für deine Nachricht.",
        text_en="Dear Maria, thank you for your message.",
    )
    assert "Liebe Maria" in ma.text_de


def test_writing_exercise_valid():
    """Test creating a valid writing exercise."""
    exercise = WritingExercise(
        id="b1-schreiben-aufgabe-1-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=1,
        title="E-Mail an einen Freund",
        instructions="Schreiben Sie eine E-Mail an Ihren Freund.",
        situation_de="Ihr Freund hat eine neue Wohnung.",
        situation_en="Your friend has a new apartment.",
        target_word_count=80,
        required_points=["react to news", "describe the apartment", "suggest meeting"],
        model_answer=ModelAnswer(
            text_de="Lieber Tom, ich habe gehört...",
            text_en="Dear Tom, I heard...",
        ),
        scoring_criteria=["task fulfillment", "coherence", "vocabulary range", "grammar accuracy"],
    )
    assert exercise.task == 1
    assert exercise.target_word_count == 80
    assert len(exercise.required_points) == 3
    assert len(exercise.scoring_criteria) == 4


# --- SpeakingExercise ---


def test_speaking_exercise_valid():
    """Test creating a valid speaking exercise."""
    exercise = SpeakingExercise(
        id="b1-sprechen-teil-1-001",
        level="B1",
        skill=ExamSkill.SPRECHEN,
        part=1,
        title="Gemeinsam etwas planen",
        instructions="Sie sollen gemeinsam etwas planen.",
        situation_de="Sie möchten ein Fest organisieren.",
        situation_en="You want to organize a party.",
        discussion_points=["Wann?", "Wo?", "Essen?", "Geschenk?"],
        model_dialogue=[
            TranscriptLine(speaker="A", text_de="Wann sollen wir feiern?", text_en="When should we celebrate?"),
            TranscriptLine(speaker="B", text_de="Am Samstag vielleicht?", text_en="On Saturday maybe?"),
        ],
        evaluation_criteria=["task fulfillment", "fluency", "interaction", "pronunciation"],
    )
    assert exercise.part == 1
    assert len(exercise.discussion_points) == 4
    assert len(exercise.model_dialogue) == 2
    assert len(exercise.evaluation_criteria) == 4


def test_speaking_exercise_missing_discussion_points():
    """Test that discussion points are required for speaking."""
    with pytest.raises(ValidationError):
        SpeakingExercise(
            id="b1-sprechen-teil-1-001",
            level="B1",
            skill=ExamSkill.SPRECHEN,
            part=1,
            title="Test",
            instructions="Test",
            situation_de="Test",
            situation_en="Test",
            model_dialogue=[],
            evaluation_criteria=[],
        )
```

### Step 2: Run tests to verify they fail

Run: `uv run pytest tests/test_exam_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.exams'`

### Step 3: Create `src/german/exams/__init__.py`

```python
"""Exam exercise models and utilities for German language certification practice."""
```

### Step 4: Implement `src/german/exams/models.py`

Follow the style of `src/german/models.py` — use `str, Enum` for enums, `BaseModel` with `ConfigDict(use_enum_values=True)`, `Field(...)` for required fields.

```python
"""Data models for German exam exercises."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class QuestionType(str, Enum):
    """Question format types used in exam exercises."""

    TRUE_FALSE = "true_false"
    MULTIPLE_CHOICE = "multiple_choice"
    MATCHING = "matching"


class ExamSkill(str, Enum):
    """The four exam skill sections (German names for directory mapping)."""

    HOEREN = "hoeren"
    LESEN = "lesen"
    SCHREIBEN = "schreiben"
    SPRECHEN = "sprechen"


class ExamMeta(BaseModel):
    """Exam-level metadata (one per exam level, stored in meta.json)."""

    level: str = Field(..., description="CEFR level (e.g. B1)")
    provider: str = Field(..., description="Exam provider (e.g. Goethe-Institut)")
    total_time_minutes: int = Field(..., description="Total exam time in minutes")
    passing_score_percent: int = Field(..., description="Minimum passing score percentage")

    model_config = ConfigDict(use_enum_values=True)


class Question(BaseModel):
    """A single exam question."""

    number: int = Field(..., description="Question number within the exercise")
    type: QuestionType = Field(..., description="Question format")
    text_de: str = Field(..., description="Question text in German")
    text_en: Optional[str] = Field(None, description="Question text in English")
    correct_answer: bool | str = Field(..., description="Correct answer (bool for true/false, str for MC/matching)")
    options: Optional[list[str]] = Field(None, description="Answer options (multiple choice only)")
    explanation_de: Optional[str] = Field(None, description="Explanation in German")
    explanation_en: Optional[str] = Field(None, description="Explanation in English")

    model_config = ConfigDict(use_enum_values=True)


class TranscriptLine(BaseModel):
    """A single line of a listening transcript or speaking dialogue."""

    speaker: str = Field(..., description="Speaker identifier (e.g. narrator, A, B)")
    text_de: str = Field(..., description="Spoken text in German")
    text_en: str = Field(..., description="Spoken text in English")

    model_config = ConfigDict(use_enum_values=True)


class Passage(BaseModel):
    """A reading passage with metadata."""

    text_de: str = Field(..., description="Passage text in German")
    text_en: str = Field(..., description="Passage text in English")
    source: str = Field(..., description="Source type (e.g. Blog post, Newspaper)")
    word_count: int = Field(..., description="Approximate word count")

    model_config = ConfigDict(use_enum_values=True)


class ModelAnswer(BaseModel):
    """A bilingual model answer for writing exercises."""

    text_de: str = Field(..., description="Model answer in German")
    text_en: str = Field(..., description="Model answer in English")

    model_config = ConfigDict(use_enum_values=True)


class ListeningExercise(BaseModel):
    """A Hören (listening) exercise with transcript and questions."""

    id: str = Field(..., description="Exercise ID (e.g. b1-hoeren-teil-1-001)")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Instructions for the exercise")
    time_minutes: int = Field(..., description="Time allotted in minutes")
    transcript: list[TranscriptLine] = Field(..., description="Listening transcript lines", min_length=1)
    questions: list[Question] = Field(..., description="Exercise questions")

    model_config = ConfigDict(use_enum_values=True)


class ReadingExercise(BaseModel):
    """A Lesen (reading) exercise with passage and questions."""

    id: str = Field(..., description="Exercise ID (e.g. b1-lesen-teil-1-001)")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Instructions for the exercise")
    time_minutes: int = Field(..., description="Time allotted in minutes")
    passage: Passage = Field(..., description="Reading passage")
    questions: list[Question] = Field(..., description="Exercise questions")

    model_config = ConfigDict(use_enum_values=True)


class WritingExercise(BaseModel):
    """A Schreiben (writing) exercise with prompt and model answer."""

    id: str = Field(..., description="Exercise ID (e.g. b1-schreiben-aufgabe-1-001)")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    task: int = Field(..., description="Task number (Aufgabe)")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Instructions for the exercise")
    situation_de: str = Field(..., description="Situation description in German")
    situation_en: str = Field(..., description="Situation description in English")
    target_word_count: int = Field(..., description="Target word count")
    required_points: list[str] = Field(..., description="Points that must be addressed", min_length=1)
    model_answer: ModelAnswer = Field(..., description="Model answer")
    scoring_criteria: list[str] = Field(..., description="Scoring criteria", min_length=1)

    model_config = ConfigDict(use_enum_values=True)


class SpeakingExercise(BaseModel):
    """A Sprechen (speaking) exercise with dialogue and evaluation criteria."""

    id: str = Field(..., description="Exercise ID (e.g. b1-sprechen-teil-1-001)")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Instructions for the exercise")
    situation_de: str = Field(..., description="Situation description in German")
    situation_en: str = Field(..., description="Situation description in English")
    discussion_points: list[str] = Field(..., description="Discussion points / prompts", min_length=1)
    model_dialogue: list[TranscriptLine] = Field(..., description="Model dialogue lines")
    evaluation_criteria: list[str] = Field(..., description="Evaluation criteria", min_length=1)

    model_config = ConfigDict(use_enum_values=True)
```

### Step 5: Run tests to verify they pass

Run: `uv run pytest tests/test_exam_models.py -v`
Expected: All tests PASS

### Step 6: Update `src/german/exams/__init__.py` with exports

```python
"""Exam exercise models and utilities for German language certification practice."""

from .models import (
    ExamMeta,
    ExamSkill,
    ListeningExercise,
    ModelAnswer,
    Passage,
    Question,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    TranscriptLine,
    WritingExercise,
)

__all__ = [
    "ExamMeta",
    "ExamSkill",
    "ListeningExercise",
    "ModelAnswer",
    "Passage",
    "Question",
    "QuestionType",
    "ReadingExercise",
    "SpeakingExercise",
    "TranscriptLine",
    "WritingExercise",
]
```

### Step 7: Run full test suite

Run: `uv run pytest -v`
Expected: All tests PASS (existing 30 + new exam model tests)

### Step 8: Lint

Run: `uv run ruff check src/german/exams/ tests/test_exam_models.py`
Expected: Clean

### Step 9: Commit

```bash
git add src/german/exams/__init__.py src/german/exams/models.py tests/test_exam_models.py
git commit -m "feat(exams): add Pydantic models for B1 exam exercises (#278)"
```

---

## Task 2: Set up directory structure and meta.json (#280)

**Files:**
- Create: `resources/exams/b1/meta.json`
- Create: 15 subdirectories with `.gitkeep` files

### Step 1: Write failing test for meta.json loading

Append to `tests/test_exam_models.py`:

```python
import json
from pathlib import Path


def test_meta_json_exists():
    """Test that meta.json exists for B1 exam."""
    meta_path = Path(__file__).parent.parent / "resources" / "exams" / "b1" / "meta.json"
    assert meta_path.exists(), f"meta.json not found at {meta_path}"


def test_meta_json_valid():
    """Test that meta.json validates against ExamMeta model."""
    meta_path = Path(__file__).parent.parent / "resources" / "exams" / "b1" / "meta.json"
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = ExamMeta(**data)
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"


def test_b1_directory_structure():
    """Test that all expected B1 exam directories exist."""
    b1_dir = Path(__file__).parent.parent / "resources" / "exams" / "b1"
    expected_dirs = [
        "hoeren/teil-1", "hoeren/teil-2", "hoeren/teil-3", "hoeren/teil-4",
        "lesen/teil-1", "lesen/teil-2", "lesen/teil-3", "lesen/teil-4", "lesen/teil-5",
        "schreiben/aufgabe-1", "schreiben/aufgabe-2", "schreiben/aufgabe-3",
        "sprechen/teil-1", "sprechen/teil-2", "sprechen/teil-3",
    ]
    for subdir in expected_dirs:
        assert (b1_dir / subdir).is_dir(), f"Missing directory: {b1_dir / subdir}"
```

### Step 2: Run tests to verify they fail

Run: `uv run pytest tests/test_exam_models.py::test_meta_json_exists -v`
Expected: FAIL — `AssertionError: meta.json not found`

### Step 3: Create directory structure and meta.json

Create `resources/exams/b1/meta.json`:

```json
{
  "level": "B1",
  "provider": "Goethe-Institut",
  "total_time_minutes": 190,
  "passing_score_percent": 60
}
```

Create directories (with `.gitkeep` so git tracks them):

```bash
mkdir -p resources/exams/b1/hoeren/teil-{1,2,3,4}
mkdir -p resources/exams/b1/lesen/teil-{1,2,3,4,5}
mkdir -p resources/exams/b1/schreiben/aufgabe-{1,2,3}
mkdir -p resources/exams/b1/sprechen/teil-{1,2,3}
touch resources/exams/b1/hoeren/teil-{1,2,3,4}/.gitkeep
touch resources/exams/b1/lesen/teil-{1,2,3,4,5}/.gitkeep
touch resources/exams/b1/schreiben/aufgabe-{1,2,3}/.gitkeep
touch resources/exams/b1/sprechen/teil-{1,2,3}/.gitkeep
```

### Step 4: Run tests to verify they pass

Run: `uv run pytest tests/test_exam_models.py::test_meta_json_exists tests/test_exam_models.py::test_meta_json_valid tests/test_exam_models.py::test_b1_directory_structure -v`
Expected: All PASS

### Step 5: Commit

```bash
git add resources/exams/
git commit -m "feat(exams): set up B1 directory structure and meta.json (#280)"
```

---

## Task 3: Create exam exercise loader and query module (#279)

**Files:**
- Create: `src/german/exams/loader.py`
- Create: `src/german/exams/query.py`
- Test: `tests/test_exam_loader.py`
- Test: `tests/test_exam_query.py`
- Modify: `src/german/exams/__init__.py` (add exports)

### Step 1: Write failing tests for loader

Create `tests/test_exam_loader.py`:

```python
"""Tests for exam exercise loader."""

import json
from pathlib import Path

import pytest

from german.exams.loader import ExamLoadError, load_exam_meta, load_exercise, load_exercises
from german.exams.models import ExamMeta, ExamSkill, ListeningExercise


def test_load_exam_meta():
    """Test loading exam metadata from meta.json."""
    meta = load_exam_meta("b1")
    assert isinstance(meta, ExamMeta)
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"


def test_load_exam_meta_nonexistent():
    """Test loading metadata for nonexistent level raises error."""
    with pytest.raises(ExamLoadError, match="not found"):
        load_exam_meta("c3")


def test_load_exercise_from_file(tmp_path):
    """Test loading a single exercise from a JSON file."""
    exercise_data = {
        "id": "b1-hoeren-teil-1-001",
        "level": "B1",
        "skill": "hoeren",
        "part": 1,
        "title": "Telefonische Nachrichten",
        "instructions": "Sie hören fünf kurze Texte.",
        "time_minutes": 10,
        "transcript": [
            {"speaker": "narrator", "text_de": "Nachricht eins.", "text_en": "Message one."}
        ],
        "questions": [
            {
                "number": 1,
                "type": "true_false",
                "text_de": "Der Anrufer möchte einen Termin.",
                "text_en": "The caller wants an appointment.",
                "correct_answer": True,
                "explanation_de": "Er sagt, er braucht einen Termin.",
                "explanation_en": "He says he needs an appointment.",
            }
        ],
    }
    exercise_file = tmp_path / "uebung-01.json"
    exercise_file.write_text(json.dumps(exercise_data), encoding="utf-8")

    exercise = load_exercise(exercise_file, ListeningExercise)
    assert exercise.id == "b1-hoeren-teil-1-001"
    assert len(exercise.transcript) == 1
    assert len(exercise.questions) == 1


def test_load_exercise_invalid_json(tmp_path):
    """Test that invalid JSON raises ExamLoadError."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid json", encoding="utf-8")
    with pytest.raises(ExamLoadError, match="Invalid JSON"):
        load_exercise(bad_file, ListeningExercise)


def test_load_exercise_validation_failure(tmp_path):
    """Test that schema validation failure raises ExamLoadError."""
    bad_data = {"id": "bad", "level": "B1"}  # missing required fields
    bad_file = tmp_path / "bad.json"
    bad_file.write_text(json.dumps(bad_data), encoding="utf-8")
    with pytest.raises(ExamLoadError, match="Validation error"):
        load_exercise(bad_file, ListeningExercise)


def test_load_exercises_empty_directory(tmp_path):
    """Test loading exercises from empty directory returns empty list."""
    exercises = load_exercises(tmp_path, ListeningExercise)
    assert exercises == []


def test_load_exercises_skips_non_json(tmp_path):
    """Test that non-JSON files are skipped."""
    (tmp_path / "readme.txt").write_text("not json")
    (tmp_path / ".gitkeep").write_text("")
    exercises = load_exercises(tmp_path, ListeningExercise)
    assert exercises == []
```

### Step 2: Run tests to verify they fail

Run: `uv run pytest tests/test_exam_loader.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.exams.loader'`

### Step 3: Implement `src/german/exams/loader.py`

```python
"""Load exam exercises from JSON files."""

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .models import ExamMeta

T = TypeVar("T", bound=BaseModel)


class ExamLoadError(Exception):
    """Exception raised when exam exercise loading fails."""

    pass


def _resources_dir() -> Path:
    """Return the resources/exams/ directory path."""
    return Path(__file__).parent.parent.parent.parent / "resources" / "exams"


def load_exam_meta(level: str) -> ExamMeta:
    """
    Load exam metadata for a given CEFR level.

    Args:
        level: CEFR level code (e.g. "b1")

    Returns:
        ExamMeta object

    Raises:
        ExamLoadError: If meta.json not found or invalid
    """
    meta_path = _resources_dir() / level / "meta.json"
    if not meta_path.exists():
        raise ExamLoadError(f"Exam metadata not found: {meta_path}")

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ExamMeta(**data)
    except json.JSONDecodeError as e:
        raise ExamLoadError(f"Invalid JSON in {meta_path.name}: {e}")
    except ValidationError as e:
        raise ExamLoadError(f"Validation error in {meta_path.name}: {e}")


def load_exercise(path: Path, model_class: type[T]) -> T:
    """
    Load a single exercise from a JSON file.

    Args:
        path: Path to the exercise JSON file
        model_class: Pydantic model class to validate against

    Returns:
        Validated exercise object

    Raises:
        ExamLoadError: If file not found, invalid JSON, or validation fails
    """
    if not path.exists():
        raise ExamLoadError(f"Exercise file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ExamLoadError(f"Invalid JSON in {path.name}: {e}")
    except UnicodeDecodeError as e:
        raise ExamLoadError(f"Encoding error in {path.name}: {e}. Must be UTF-8.")

    try:
        return model_class(**data)
    except ValidationError as e:
        raise ExamLoadError(f"Validation error in {path.name}: {e}")


def load_exercises(directory: Path, model_class: type[T]) -> list[T]:
    """
    Load all exercises from a directory.

    Args:
        directory: Directory containing exercise JSON files
        model_class: Pydantic model class to validate against

    Returns:
        List of validated exercise objects (sorted by filename)

    Raises:
        ExamLoadError: If any file fails to load or validate
    """
    if not directory.exists():
        return []

    exercises: list[T] = []
    for json_file in sorted(directory.glob("*.json")):
        exercises.append(load_exercise(json_file, model_class))

    return exercises
```

### Step 4: Run loader tests to verify they pass

Run: `uv run pytest tests/test_exam_loader.py -v`
Expected: All PASS

### Step 5: Write failing tests for query module

Create `tests/test_exam_query.py`:

```python
"""Tests for exam exercise query functions."""

from german.exams.models import (
    ExamSkill,
    ListeningExercise,
    ModelAnswer,
    Passage,
    Question,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    TranscriptLine,
    WritingExercise,
)
from german.exams.query import filter_by_part, filter_by_skill, filter_by_question_type


def _make_listening(part: int = 1) -> ListeningExercise:
    """Helper to create a listening exercise."""
    return ListeningExercise(
        id=f"b1-hoeren-teil{part}-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=part,
        title="Test",
        instructions="Test",
        time_minutes=10,
        transcript=[TranscriptLine(speaker="narrator", text_de="Test.", text_en="Test.")],
        questions=[
            Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Test?", correct_answer=True)
        ],
    )


def _make_reading(part: int = 1) -> ReadingExercise:
    """Helper to create a reading exercise."""
    return ReadingExercise(
        id=f"b1-lesen-teil{part}-001",
        level="B1",
        skill=ExamSkill.LESEN,
        part=part,
        title="Test",
        instructions="Test",
        time_minutes=13,
        passage=Passage(text_de="Text.", text_en="Text.", source="Blog", word_count=100),
        questions=[
            Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="Was?", correct_answer="a",
                     options=["a) X", "b) Y", "c) Z"])
        ],
    )


def _make_writing(task: int = 1) -> WritingExercise:
    """Helper to create a writing exercise."""
    return WritingExercise(
        id=f"b1-schreiben-aufgabe{task}-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=task,
        title="Test",
        instructions="Test",
        situation_de="Test.",
        situation_en="Test.",
        target_word_count=80,
        required_points=["point 1"],
        model_answer=ModelAnswer(text_de="Antwort.", text_en="Answer."),
        scoring_criteria=["criterion 1"],
    )


def _make_speaking(part: int = 1) -> SpeakingExercise:
    """Helper to create a speaking exercise."""
    return SpeakingExercise(
        id=f"b1-sprechen-teil{part}-001",
        level="B1",
        skill=ExamSkill.SPRECHEN,
        part=part,
        title="Test",
        instructions="Test",
        situation_de="Test.",
        situation_en="Test.",
        discussion_points=["Punkt 1"],
        model_dialogue=[TranscriptLine(speaker="A", text_de="Test.", text_en="Test.")],
        evaluation_criteria=["criterion 1"],
    )


# -- filter_by_skill --


def test_filter_by_skill_hoeren():
    """Test filtering exercises by listening skill."""
    exercises = [_make_listening(), _make_reading(), _make_writing(), _make_speaking()]
    result = filter_by_skill(ExamSkill.HOEREN, exercises)
    assert len(result) == 1
    assert all(e.skill == ExamSkill.HOEREN for e in result)


def test_filter_by_skill_string():
    """Test filtering by skill using string value."""
    exercises = [_make_listening(), _make_reading()]
    result = filter_by_skill("lesen", exercises)
    assert len(result) == 1


def test_filter_by_skill_empty():
    """Test filtering with no matches returns empty list."""
    exercises = [_make_listening()]
    result = filter_by_skill(ExamSkill.SPRECHEN, exercises)
    assert result == []


# -- filter_by_part --


def test_filter_by_part():
    """Test filtering exercises by part number."""
    exercises = [_make_listening(part=1), _make_listening(part=2), _make_listening(part=3)]
    result = filter_by_part(2, exercises)
    assert len(result) == 1
    assert result[0].part == 2


def test_filter_by_part_writing_uses_task():
    """Test that writing exercises match on task field."""
    exercises = [_make_writing(task=1), _make_writing(task=2)]
    result = filter_by_part(2, exercises)
    assert len(result) == 1


# -- filter_by_question_type --


def test_filter_by_question_type():
    """Test filtering exercises by question type."""
    listening = _make_listening()  # has true_false questions
    reading = _make_reading()  # has multiple_choice questions
    exercises = [listening, reading]
    result = filter_by_question_type(QuestionType.TRUE_FALSE, exercises)
    assert len(result) == 1


def test_filter_by_question_type_string():
    """Test filtering by question type using string."""
    exercises = [_make_listening()]
    result = filter_by_question_type("true_false", exercises)
    assert len(result) == 1
```

### Step 6: Run query tests to verify they fail

Run: `uv run pytest tests/test_exam_query.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.exams.query'`

### Step 7: Implement `src/german/exams/query.py`

```python
"""Query functions for exam exercise data."""

from typing import Union

from .models import (
    ExamSkill,
    ListeningExercise,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    WritingExercise,
)

ExamExercise = Union[ListeningExercise, ReadingExercise, WritingExercise, SpeakingExercise]


def filter_by_skill(
    skill: str | ExamSkill, exercises: list[ExamExercise]
) -> list[ExamExercise]:
    """
    Filter exercises by exam skill section.

    Args:
        skill: Exam skill to filter by (hoeren, lesen, schreiben, sprechen)
        exercises: List of exercises to filter

    Returns:
        List of matching exercises
    """
    if isinstance(skill, str):
        skill = ExamSkill(skill)

    return [ex for ex in exercises if ex.skill == skill]


def filter_by_part(
    part: int, exercises: list[ExamExercise]
) -> list[ExamExercise]:
    """
    Filter exercises by part/task number.

    For writing exercises, matches on the 'task' field.
    For all others, matches on the 'part' field.

    Args:
        part: Part or task number to filter by
        exercises: List of exercises to filter

    Returns:
        List of matching exercises
    """
    result: list[ExamExercise] = []
    for ex in exercises:
        if isinstance(ex, WritingExercise):
            if ex.task == part:
                result.append(ex)
        else:
            if ex.part == part:
                result.append(ex)
    return result


def filter_by_question_type(
    question_type: str | QuestionType, exercises: list[ExamExercise]
) -> list[ExamExercise]:
    """
    Filter exercises that contain at least one question of the given type.

    Args:
        question_type: Question type to filter by
        exercises: List of exercises to filter

    Returns:
        List of exercises containing matching questions
    """
    if isinstance(question_type, str):
        question_type = QuestionType(question_type)

    result: list[ExamExercise] = []
    for ex in exercises:
        if hasattr(ex, "questions"):
            if any(q.type == question_type for q in ex.questions):
                result.append(ex)
    return result
```

### Step 8: Run query tests to verify they pass

Run: `uv run pytest tests/test_exam_query.py -v`
Expected: All PASS

### Step 9: Update `src/german/exams/__init__.py` with loader and query exports

```python
"""Exam exercise models and utilities for German language certification practice."""

from .loader import ExamLoadError, load_exam_meta, load_exercise, load_exercises
from .models import (
    ExamMeta,
    ExamSkill,
    ListeningExercise,
    ModelAnswer,
    Passage,
    Question,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    TranscriptLine,
    WritingExercise,
)
from .query import filter_by_part, filter_by_question_type, filter_by_skill

__all__ = [
    "ExamLoadError",
    "ExamMeta",
    "ExamSkill",
    "ListeningExercise",
    "ModelAnswer",
    "Passage",
    "Question",
    "QuestionType",
    "ReadingExercise",
    "SpeakingExercise",
    "TranscriptLine",
    "WritingExercise",
    "filter_by_part",
    "filter_by_question_type",
    "filter_by_skill",
    "load_exam_meta",
    "load_exercise",
    "load_exercises",
]
```

### Step 10: Run full test suite and lint

Run: `uv run pytest -v && uv run ruff check src/german/exams/ tests/test_exam_loader.py tests/test_exam_query.py`
Expected: All PASS, no lint errors

### Step 11: Commit

```bash
git add src/german/exams/loader.py src/german/exams/query.py src/german/exams/__init__.py tests/test_exam_loader.py tests/test_exam_query.py
git commit -m "feat(exams): add exam exercise loader and query module (#279)"
```

---

## Task 4: Add comprehensive JSON schema validation tests (#281)

**Files:**
- Modify: `tests/test_exam_models.py` (add integration-style validation tests)

### Step 1: Add integration validation tests

Append to `tests/test_exam_models.py` (these go beyond unit tests to validate full round-trip JSON → model → assertions):

```python
def test_listening_exercise_roundtrip_json():
    """Test that a listening exercise survives JSON round-trip."""
    exercise = ListeningExercise(
        id="b1-hoeren-teil-1-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Ansagen am Bahnhof",
        instructions="Sie hören fünf kurze Texte. Sie hören jeden Text zweimal.",
        time_minutes=10,
        transcript=[
            TranscriptLine(
                speaker="Sprecher",
                text_de="Achtung auf Gleis drei: Der Zug nach München fährt in fünf Minuten ab.",
                text_en="Attention on platform three: The train to Munich departs in five minutes.",
            )
        ],
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="Der Zug fährt nach München.",
                text_en="The train goes to Munich.",
                correct_answer=True,
                explanation_de="Die Durchsage sagt 'Zug nach München'.",
                explanation_en="The announcement says 'train to Munich'.",
            )
        ],
    )
    json_str = exercise.model_dump_json()
    reloaded = ListeningExercise.model_validate_json(json_str)
    assert reloaded.id == exercise.id
    assert reloaded.transcript[0].text_de == exercise.transcript[0].text_de
    assert reloaded.questions[0].correct_answer == exercise.questions[0].correct_answer


def test_writing_exercise_roundtrip_json():
    """Test that a writing exercise survives JSON round-trip."""
    exercise = WritingExercise(
        id="b1-schreiben-aufgabe-1-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=1,
        title="E-Mail an einen Freund",
        instructions="Schreiben Sie eine E-Mail.",
        situation_de="Ihr Freund hat eine neue Wohnung gefunden.",
        situation_en="Your friend found a new apartment.",
        target_word_count=80,
        required_points=["react to news", "ask about the apartment", "suggest a visit"],
        model_answer=ModelAnswer(
            text_de="Lieber Max, ich freue mich sehr über deine neue Wohnung!",
            text_en="Dear Max, I am very happy about your new apartment!",
        ),
        scoring_criteria=["task fulfillment", "coherence", "vocabulary range", "grammar accuracy"],
    )
    json_str = exercise.model_dump_json()
    reloaded = WritingExercise.model_validate_json(json_str)
    assert reloaded.task == exercise.task
    assert reloaded.model_answer.text_de == exercise.model_answer.text_de


def test_exercise_id_format():
    """Test that exercise IDs follow the naming convention."""
    exercises = [
        ListeningExercise(
            id="b1-hoeren-teil-1-001", level="B1", skill=ExamSkill.HOEREN, part=1,
            title="T", instructions="I", time_minutes=10,
            transcript=[TranscriptLine(speaker="n", text_de="D.", text_en="E.")],
            questions=[Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Q?", correct_answer=True)],
        ),
        ReadingExercise(
            id="b1-lesen-teil-2-003", level="B1", skill=ExamSkill.LESEN, part=2,
            title="T", instructions="I", time_minutes=13,
            passage=Passage(text_de="T.", text_en="T.", source="Blog", word_count=100),
            questions=[Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Q?", correct_answer=True)],
        ),
    ]
    import re
    pattern = r"^b1-(hoeren|lesen|schreiben|sprechen)-(teil|aufgabe)-\d+-\d{3}$"
    for ex in exercises:
        assert re.match(pattern, ex.id), f"ID '{ex.id}' doesn't match expected format"


def test_umlaut_preservation_in_models():
    """Test that German umlauts and ß survive model creation."""
    line = TranscriptLine(
        speaker="Prüfer",
        text_de="Möchten Sie über Ihre Erfahrungen in der Großstadt erzählen?",
        text_en="Would you like to talk about your experiences in the big city?",
    )
    assert "ü" in line.speaker
    assert "ö" in line.text_de
    assert "ß" in line.text_de
    assert "ä" in line.text_de
```

### Step 2: Run all tests

Run: `uv run pytest -v`
Expected: All tests PASS

### Step 3: Check coverage

Run: `uv run pytest --cov=german.exams --cov-report=term-missing tests/test_exam_models.py tests/test_exam_loader.py tests/test_exam_query.py`
Expected: Coverage >= 80% for `german.exams` modules

### Step 4: Final lint check

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: Clean

### Step 5: Commit

```bash
git add tests/test_exam_models.py
git commit -m "test(exams): add JSON schema validation and round-trip tests (#281)"
```

---

## Summary

| Task | Issue | Files created | Tests added |
|------|-------|---------------|-------------|
| 1 | #278 | `src/german/exams/{__init__,models}.py` | ~20 model tests |
| 2 | #280 | `resources/exams/b1/meta.json` + 15 dirs | 3 structure tests |
| 3 | #279 | `src/german/exams/{loader,query}.py` | ~15 loader/query tests |
| 4 | #281 | — (extends test file) | 4 validation tests |

**Total: 7 new files, ~42 tests, 4 commits**
