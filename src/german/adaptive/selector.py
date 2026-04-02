"""Adaptive exercise selector.

Picks the next exercise based on student proficiency gaps,
prioritizing concepts that need the most review.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from german.exams.loader import load_exercises
from german.exams.models import ListeningExercise, ReadingExercise

from .concepts import SCORABLE_SKILLS, get_concepts_for_level
from .profiler import StudentProfile

Exercise = Union[ListeningExercise, ReadingExercise]


class AdaptiveSelector:
    """Selects exercises adaptively based on student proficiency."""

    def __init__(self, profile: StudentProfile, level: str):
        self._profile = profile
        self._level = level.lower()
        self._exercises: dict[str, list[Exercise]] = {}
        self._load_exercises()

    def _load_exercises(self) -> None:
        """Load all scorable exercises for the level."""
        resources_dir = Path(__file__).parent.parent.parent.parent / "resources" / "exams" / self._level
        if not resources_dir.exists():
            return
        for skill in SCORABLE_SKILLS:
            skill_dir = resources_dir / skill
            if not skill_dir.exists():
                continue
            model_class = ListeningExercise if skill == "hoeren" else ReadingExercise
            for teil_dir in sorted(skill_dir.iterdir()):
                if not teil_dir.is_dir() or not teil_dir.name.startswith("teil-"):
                    continue
                teil_num = int(teil_dir.name.split("-")[1])
                concept_id = f"{self._level}-{skill}-teil-{teil_num}"
                exercises = load_exercises(teil_dir, model_class)
                if exercises:
                    self._exercises[concept_id] = exercises

    def pick_next(self) -> tuple[Exercise, str] | None:
        """Pick the next exercise based on proficiency gaps."""
        concepts = self.get_concept_order()
        if not concepts:
            return None
        concepts_with_priority = [
            (cid, self._profile.get_priority(cid))
            for cid in concepts
            if cid in self._exercises
        ]
        if not concepts_with_priority:
            return None
        concepts_with_priority.sort(key=lambda x: x[1], reverse=True)
        selected_concept = concepts_with_priority[0][0]
        exercises = self._exercises[selected_concept]
        exercise = self._pick_exercise(selected_concept, exercises)
        return exercise, selected_concept

    def _pick_exercise(self, concept_id: str, exercises: list[Exercise]) -> Exercise:
        """Pick an exercise, avoiding recently attempted ones."""
        now = datetime.now()
        cutoff = now - timedelta(hours=24)
        recent_ids = set()
        if concept_id in self._profile.concepts:
            for attempt in self._profile.concepts[concept_id].get("attempt_history", []):
                attempt_time = datetime.fromisoformat(attempt["timestamp"])
                if attempt_time > cutoff:
                    recent_ids.add(attempt["exercise_id"])
        available = [ex for ex in exercises if ex.id not in recent_ids]
        if not available:
            available = exercises
        return random.choice(available)

    def get_concept_order(self) -> list[str]:
        """Get ordered list of concepts for the level."""
        return get_concepts_for_level(self._level)
