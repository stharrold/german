"""Tests for adaptive learning proficiency tracker."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from german.adaptive.profiler import StudentProfile


@pytest.fixture
def tmp_profile(tmp_path):
    """Create a temporary profile path."""
    return tmp_path / "profile.json"


def test_create_new_profile(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    assert profile.student_name == "Test"
    assert profile.concepts == {}
    assert profile.active_levels == []


def test_save_and_load_roundtrip(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.active_levels = ["a2"]
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="a2-lesen-teil-1-001", question_number=1)
    profile.save()
    loaded = StudentProfile.load(tmp_profile)
    assert loaded.student_name == "Test"
    assert loaded.active_levels == ["a2"]
    assert "a2-lesen-teil-1" in loaded.concepts


def test_update_correct_answer(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    concept = profile.concepts["a2-lesen-teil-1"]
    assert abs(concept["proficiency"] - 0.09) < 0.01
    assert concept["total_attempts"] == 1
    assert concept["correct_attempts"] == 1
    assert concept["mastered"] is False


def test_update_incorrect_answer(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    old_prof = profile.concepts["a2-lesen-teil-1"]["proficiency"]
    profile.update("a2-lesen-teil-1", is_correct=False, difficulty=0.3, exercise_id="ex1", question_number=2)
    new_prof = profile.concepts["a2-lesen-teil-1"]["proficiency"]
    assert abs(new_prof - old_prof * 0.7) < 0.01


def test_mastery_threshold(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.concepts["a2-lesen-teil-1"] = {
        "proficiency": 0.84, "total_attempts": 20, "correct_attempts": 18,
        "mastered": False, "last_attempt": datetime.now().isoformat(),
        "next_review": datetime.now().isoformat(), "attempt_history": [],
    }
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.9, exercise_id="ex1", question_number=1)
    assert profile.concepts["a2-lesen-teil-1"]["mastered"] is True


def test_proficiency_clamped(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    for i in range(50):
        profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.9, exercise_id="ex1", question_number=i)
    assert profile.concepts["a2-lesen-teil-1"]["proficiency"] <= 1.0


def test_get_proficiency_unseen(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    assert profile.get_proficiency("a2-lesen-teil-1") == 0.0


def test_get_proficiency_existing(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    assert profile.get_proficiency("a2-lesen-teil-1") > 0.0


def test_get_priority_unseen(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    priority = profile.get_priority("a2-lesen-teil-1")
    assert priority > 0


def test_get_priority_mastered(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.concepts["a2-lesen-teil-1"] = {
        "proficiency": 0.95, "total_attempts": 50, "correct_attempts": 48,
        "mastered": True, "last_attempt": datetime.now().isoformat(),
        "next_review": (datetime.now() + timedelta(days=7)).isoformat(),
        "attempt_history": [],
    }
    priority = profile.get_priority("a2-lesen-teil-1")
    assert priority < 0.1


def test_review_scheduling(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    concept = profile.concepts["a2-lesen-teil-1"]
    next_review = datetime.fromisoformat(concept["next_review"])
    now = datetime.now()
    assert next_review - now < timedelta(days=3)


def test_attempt_history_recorded(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="a2-lesen-teil-1-001", question_number=3)
    history = profile.concepts["a2-lesen-teil-1"]["attempt_history"]
    assert len(history) == 1
    assert history[0]["exercise_id"] == "a2-lesen-teil-1-001"
    assert history[0]["question"] == 3
    assert history[0]["is_correct"] is True
    assert "old_proficiency" in history[0]
    assert "new_proficiency" in history[0]


def test_get_stats(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    profile.update("a2-lesen-teil-1", is_correct=False, difficulty=0.3, exercise_id="ex1", question_number=2)
    stats = profile.get_stats()
    assert stats["total_attempts"] == 2
    assert stats["total_correct"] == 1
    assert stats["accuracy"] == 0.5
    assert stats["concepts_studied"] == 1
    assert stats["concepts_mastered"] == 0


def test_json_format(tmp_profile):
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    profile.save()
    content = tmp_profile.read_text(encoding="utf-8")
    assert content.endswith("\n")
    data = json.loads(content)
    assert data["student_name"] == "Test"
