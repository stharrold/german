"""Integration tests for adaptive drill CLI."""

from io import StringIO
from unittest.mock import patch

import pytest

from german.adaptive.cli import DrillSession


@pytest.fixture
def tmp_profile_path(tmp_path):
    return tmp_path / "profile.json"


def test_drill_session_creates_profile(tmp_profile_path):
    """Test that DrillSession creates a profile on first run."""
    session = DrillSession(level="a2", num_questions=1, profile_path=tmp_profile_path)
    assert session.profile.student_name is not None
    assert session.profile.active_levels == ["a2"]


def test_drill_session_selects_exercise(tmp_profile_path):
    """Test that DrillSession can select an exercise."""
    session = DrillSession(level="a2", num_questions=1, profile_path=tmp_profile_path)
    result = session.selector.pick_next()
    assert result is not None


def test_drill_session_run_with_input(tmp_profile_path):
    """Test running a 2-question drill session with simulated input."""
    session = DrillSession(level="a2", num_questions=2, profile_path=tmp_profile_path)
    # Simulate user answering "b" for every question, then "n" to not continue
    answers = "b\n" * 20 + "n\n"  # Enough answers for any exercise
    with patch("builtins.input", side_effect=answers.split("\n")):
        with patch("sys.stdout", new_callable=StringIO):
            try:
                session.run()
            except (StopIteration, EOFError):
                pass  # Expected when input runs out

    # Profile should have been updated
    assert session.profile.get_stats()["total_attempts"] > 0


def test_drill_session_stats(tmp_profile_path):
    """Test stats display doesn't crash."""
    session = DrillSession(level="a2", num_questions=0, profile_path=tmp_profile_path)
    # Just verify show_stats doesn't raise
    output = StringIO()
    with patch("sys.stdout", output):
        session.show_stats()
    assert "A2" in output.getvalue() or "a2" in output.getvalue()
