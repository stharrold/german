"""Student proficiency tracker for adaptive learning.

Tracks per-concept mastery scores using gain/decay formulas adapted
from the chimeu ConceptProfiler. Persists state as JSON.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


class StudentProfile:
    """Tracks student proficiency across exam concepts."""

    MASTERY_THRESHOLD = 0.85
    GAIN_MULTIPLIER = 0.3
    DECAY_MULTIPLIER = 0.7

    def __init__(self, path: Path, student_name: str, active_levels: list[str], concepts: dict, created: str, last_session: str | None):
        self._path = path
        self.student_name = student_name
        self.active_levels = active_levels
        self.concepts = concepts
        self.created = created
        self.last_session = last_session

    @classmethod
    def load(cls, path: Path, student_name: str = "Student") -> "StudentProfile":
        """Load profile from JSON file, or create new if not found."""
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls(
                path=path,
                student_name=data.get("student_name", student_name),
                active_levels=data.get("active_levels", []),
                concepts=data.get("concepts", {}),
                created=data.get("created", datetime.now().isoformat()),
                last_session=data.get("last_session"),
            )
        return cls(
            path=path,
            student_name=student_name,
            active_levels=[],
            concepts={},
            created=datetime.now().isoformat(),
            last_session=None,
        )

    def save(self) -> None:
        """Save profile to JSON file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "student_name": self.student_name,
            "active_levels": self.active_levels,
            "created": self.created,
            "last_session": self.last_session,
            "concepts": self.concepts,
        }
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    def update(self, concept_id: str, is_correct: bool, difficulty: float, exercise_id: str, question_number: int) -> None:
        """Update proficiency for a concept based on answer correctness."""
        now = datetime.now()

        if concept_id not in self.concepts:
            self.concepts[concept_id] = {
                "proficiency": 0.0,
                "total_attempts": 0,
                "correct_attempts": 0,
                "mastered": False,
                "last_attempt": None,
                "next_review": None,
                "attempt_history": [],
            }

        concept = self.concepts[concept_id]
        old_proficiency = concept["proficiency"]

        if is_correct:
            concept["proficiency"] += (1.0 - concept["proficiency"]) * difficulty * self.GAIN_MULTIPLIER
            concept["correct_attempts"] += 1
        else:
            concept["proficiency"] *= self.DECAY_MULTIPLIER

        # Clamp to [0, 1]
        concept["proficiency"] = max(0.0, min(1.0, concept["proficiency"]))

        concept["total_attempts"] += 1
        concept["mastered"] = concept["proficiency"] >= self.MASTERY_THRESHOLD
        concept["last_attempt"] = now.isoformat()

        # Review scheduling: 1 + (proficiency * 6) days
        review_days = 1 + (concept["proficiency"] * 6)
        concept["next_review"] = (now + timedelta(days=review_days)).isoformat()

        concept["attempt_history"].append({
            "timestamp": now.isoformat(),
            "exercise_id": exercise_id,
            "question": question_number,
            "is_correct": is_correct,
            "old_proficiency": round(old_proficiency, 4),
            "new_proficiency": round(concept["proficiency"], 4),
        })

        self.last_session = now.isoformat()

    def get_proficiency(self, concept_id: str) -> float:
        """Get proficiency for a concept. Returns 0.0 if unseen."""
        if concept_id not in self.concepts:
            return 0.0
        return self.concepts[concept_id]["proficiency"]

    def get_priority(self, concept_id: str) -> float:
        """Get review priority for a concept. Higher = needs more review."""
        proficiency = self.get_proficiency(concept_id)
        if concept_id not in self.concepts or self.concepts[concept_id]["last_attempt"] is None:
            # Never attempted — high priority
            return (1.0 - proficiency) * 30.0
        last = datetime.fromisoformat(self.concepts[concept_id]["last_attempt"])
        days_since = max(0.0, (datetime.now() - last).total_seconds() / 86400)
        return (1.0 - proficiency) * days_since

    def get_stats(self) -> dict:
        """Get summary statistics."""
        total_attempts = sum(c["total_attempts"] for c in self.concepts.values())
        total_correct = sum(c["correct_attempts"] for c in self.concepts.values())
        return {
            "total_attempts": total_attempts,
            "total_correct": total_correct,
            "accuracy": total_correct / total_attempts if total_attempts > 0 else 0.0,
            "concepts_studied": len(self.concepts),
            "concepts_mastered": sum(1 for c in self.concepts.values() if c["mastered"]),
        }
