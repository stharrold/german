"""Tests for exam exercise loader."""

import json

import pytest

from german.exams.loader import ExamLoadError, load_exam_meta, load_exercise, load_exercises
from german.exams.models import ExamMeta, ListeningExercise


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


def test_load_exam_meta_path_traversal():
    """Test that path traversal in level is rejected."""
    with pytest.raises(ExamLoadError, match="Invalid level"):
        load_exam_meta("../../etc")


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
    bad_data = {"id": "bad", "level": "B1"}
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
