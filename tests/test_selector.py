"""Tests for adaptive exercise selector."""

from datetime import datetime, timedelta

import pytest

from german.adaptive.selector import AdaptiveSelector
from german.adaptive.profiler import StudentProfile


@pytest.fixture
def tmp_profile(tmp_path):
    path = tmp_path / "profile.json"
    profile = StudentProfile.load(path, student_name="Test")
    profile.active_levels = ["a2"]
    return profile


def test_pick_next_cold_start(tmp_profile):
    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    exercise, concept_id = result
    assert concept_id in ["a2-hoeren-teil-1", "a2-lesen-teil-1"]


def test_pick_next_returns_exercise(tmp_profile):
    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    exercise, concept_id = result
    assert hasattr(exercise, "questions")
    assert hasattr(exercise, "id")


def test_pick_next_prioritizes_weak_concepts(tmp_profile):
    for teil in range(1, 5):
        for skill in ["lesen", "hoeren"]:
            cid = f"a2-{skill}-teil-{teil}"
            tmp_profile.concepts[cid] = {
                "proficiency": 0.95, "total_attempts": 50, "correct_attempts": 48,
                "mastered": True, "last_attempt": datetime.now().isoformat(),
                "next_review": (datetime.now() + timedelta(days=7)).isoformat(),
                "attempt_history": [],
            }
    tmp_profile.concepts["a2-lesen-teil-3"]["proficiency"] = 0.2
    tmp_profile.concepts["a2-lesen-teil-3"]["mastered"] = False

    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    _, concept_id = result
    assert concept_id == "a2-lesen-teil-3"


def test_pick_next_none_when_no_exercises(tmp_profile):
    selector = AdaptiveSelector(tmp_profile, "z9")
    result = selector.pick_next()
    assert result is None


def test_get_concept_order(tmp_profile):
    selector = AdaptiveSelector(tmp_profile, "a2")
    order = selector.get_concept_order()
    assert len(order) == 8
    for cid in order:
        assert cid.startswith("a2-")
