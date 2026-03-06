"""Tests for B2 exam exercise content validation."""

import json
import re
from pathlib import Path

import pytest

from german.exams.loader import load_exam_meta, load_exercises
from german.exams.models import (
    ExamMeta,
    ExamSkill,
    ListeningExercise,
    ReadingExercise,
    SpeakingExercise,
    WritingExercise,
)

B2_DIR = Path(__file__).parent.parent / "resources" / "exams" / "b2"
EXERCISE_ID_PATTERN = re.compile(r"^b2-(hoeren|lesen|schreiben|sprechen)-(teil|aufgabe)-\d+-\d{3}$")


def test_b2_meta_json_exists():
    """Test that meta.json exists for B2 exam."""
    assert (B2_DIR / "meta.json").exists()


def test_b2_meta_json_valid():
    """Test that B2 meta.json validates against ExamMeta model."""
    meta = load_exam_meta("b2")
    assert isinstance(meta, ExamMeta)
    assert meta.level == "B2"
    assert meta.provider == "Goethe-Institut"


def test_b2_directory_structure():
    """Test that all expected B2 exam directories exist."""
    expected_dirs = [
        "hoeren/teil-1", "hoeren/teil-2", "hoeren/teil-3", "hoeren/teil-4",
        "lesen/teil-1", "lesen/teil-2", "lesen/teil-3", "lesen/teil-4", "lesen/teil-5",
        "schreiben/aufgabe-1", "schreiben/aufgabe-2",
        "sprechen/teil-1", "sprechen/teil-2",
    ]
    for subdir in expected_dirs:
        assert (B2_DIR / subdir).is_dir(), f"Missing directory: {B2_DIR / subdir}"


# --- Hören ---

@pytest.mark.parametrize("teil", [1, 2, 3, 4])
def test_b2_hoeren_exercises_exist(teil):
    """Test that each Hören teil has 5 exercises."""
    teil_dir = B2_DIR / "hoeren" / f"teil-{teil}"
    exercises = sorted(teil_dir.glob("uebung-*.json"))
    assert len(exercises) == 5, f"Expected 5 exercises in teil-{teil}, found {len(exercises)}"


@pytest.mark.parametrize("teil", [1, 2, 3, 4])
def test_b2_hoeren_exercises_valid(teil):
    """Test that all Hören exercises pass Pydantic validation."""
    teil_dir = B2_DIR / "hoeren" / f"teil-{teil}"
    exercises = load_exercises(teil_dir, ListeningExercise)
    assert len(exercises) == 5
    for ex in exercises:
        assert ex.level == "B2"
        assert ex.skill == ExamSkill.HOEREN
        assert ex.part == teil
        assert EXERCISE_ID_PATTERN.match(ex.id), f"Bad ID: {ex.id}"
        assert len(ex.transcript) >= 1
        assert len(ex.questions) >= 1


# --- Lesen ---

@pytest.mark.parametrize("teil", [1, 2, 3, 4, 5])
def test_b2_lesen_exercises_exist(teil):
    """Test that each Lesen teil has 5 exercises."""
    teil_dir = B2_DIR / "lesen" / f"teil-{teil}"
    exercises = sorted(teil_dir.glob("uebung-*.json"))
    assert len(exercises) == 5, f"Expected 5 exercises in teil-{teil}, found {len(exercises)}"


@pytest.mark.parametrize("teil", [1, 2, 3, 4, 5])
def test_b2_lesen_exercises_valid(teil):
    """Test that all Lesen exercises pass Pydantic validation."""
    teil_dir = B2_DIR / "lesen" / f"teil-{teil}"
    exercises = load_exercises(teil_dir, ReadingExercise)
    assert len(exercises) == 5
    for ex in exercises:
        assert ex.level == "B2"
        assert ex.skill == ExamSkill.LESEN
        assert ex.part == teil
        assert EXERCISE_ID_PATTERN.match(ex.id), f"Bad ID: {ex.id}"
        assert ex.passage is not None
        assert len(ex.questions) >= 1


# --- Schreiben ---

@pytest.mark.parametrize("aufgabe", [1, 2])
def test_b2_schreiben_exercises_exist(aufgabe):
    """Test that each Schreiben aufgabe has 5 exercises."""
    aufgabe_dir = B2_DIR / "schreiben" / f"aufgabe-{aufgabe}"
    exercises = sorted(aufgabe_dir.glob("uebung-*.json"))
    assert len(exercises) == 5, f"Expected 5 exercises in aufgabe-{aufgabe}, found {len(exercises)}"


@pytest.mark.parametrize("aufgabe", [1, 2])
def test_b2_schreiben_exercises_valid(aufgabe):
    """Test that all Schreiben exercises pass Pydantic validation."""
    aufgabe_dir = B2_DIR / "schreiben" / f"aufgabe-{aufgabe}"
    exercises = load_exercises(aufgabe_dir, WritingExercise)
    assert len(exercises) == 5
    for ex in exercises:
        assert ex.level == "B2"
        assert ex.skill == ExamSkill.SCHREIBEN
        assert ex.task == aufgabe
        assert EXERCISE_ID_PATTERN.match(ex.id), f"Bad ID: {ex.id}"
        assert ex.model_answer.text_de
        assert len(ex.required_points) >= 1


@pytest.mark.parametrize("aufgabe", [1, 2])
def test_b2_schreiben_word_count(aufgabe):
    """Test that target_word_count matches model answer word count (±2)."""
    aufgabe_dir = B2_DIR / "schreiben" / f"aufgabe-{aufgabe}"
    exercises = load_exercises(aufgabe_dir, WritingExercise)
    for ex in exercises:
        actual = len(ex.model_answer.text_de.split())
        assert abs(actual - ex.target_word_count) <= 2, (
            f"{ex.id}: target_word_count={ex.target_word_count}, actual={actual}"
        )


# --- Sprechen ---

@pytest.mark.parametrize("teil", [1, 2])
def test_b2_sprechen_exercises_exist(teil):
    """Test that each Sprechen teil has 5 exercises."""
    teil_dir = B2_DIR / "sprechen" / f"teil-{teil}"
    exercises = sorted(teil_dir.glob("uebung-*.json"))
    assert len(exercises) == 5, f"Expected 5 exercises in teil-{teil}, found {len(exercises)}"


@pytest.mark.parametrize("teil", [1, 2])
def test_b2_sprechen_exercises_valid(teil):
    """Test that all Sprechen exercises pass Pydantic validation."""
    teil_dir = B2_DIR / "sprechen" / f"teil-{teil}"
    exercises = load_exercises(teil_dir, SpeakingExercise)
    assert len(exercises) == 5
    for ex in exercises:
        assert ex.level == "B2"
        assert ex.skill == ExamSkill.SPRECHEN
        assert ex.part == teil
        assert EXERCISE_ID_PATTERN.match(ex.id), f"Bad ID: {ex.id}"
        assert len(ex.discussion_points) >= 1
        assert len(ex.model_dialogue) >= 1


# --- Cross-cutting ---

def test_b2_total_exercise_count():
    """Test that exactly 65 B2 exercises exist."""
    count = len(list(B2_DIR.glob("**/uebung-*.json")))
    assert count == 65, f"Expected 65 exercises, found {count}"


def test_b2_no_unicode_escapes():
    """Test that JSON files use native UTF-8, not unicode escapes."""
    for f in B2_DIR.glob("**/uebung-*.json"):
        content = f.read_text(encoding="utf-8")
        assert not re.search(r"\\u[0-9a-fA-F]{4}", content), f"Unicode escape found in {f}"


def test_b2_all_ids_unique():
    """Test that all exercise IDs are unique across B2."""
    ids = []
    for f in B2_DIR.glob("**/uebung-*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        ids.append(data["id"])
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[x for x in ids if ids.count(x) > 1]}"


def test_b2_all_bilingual():
    """Test that all exercises have bilingual content where expected."""
    def check_fields(obj, filepath):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.endswith("_de"):
                    en_key = key[:-3] + "_en"
                    assert en_key in obj, f"Missing '{en_key}' for '{key}' in {filepath}"
                elif key.endswith("_en"):
                    de_key = key[:-3] + "_de"
                    assert de_key in obj, f"Missing '{de_key}' for '{key}' in {filepath}"
                check_fields(value, filepath)
        elif isinstance(obj, list):
            for item in obj:
                check_fields(item, filepath)

    for f in B2_DIR.glob("**/uebung-*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        check_fields(data, f)
