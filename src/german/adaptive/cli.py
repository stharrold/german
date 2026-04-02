"""Interactive CLI drill session for adaptive German exam practice.

Usage:
    uv run python -m german.adaptive --level a2 --questions 10
    uv run python -m german.adaptive --stats
    uv run python -m german.adaptive --reset
"""

import sys
from datetime import datetime
from pathlib import Path

from german.exams.models import ListeningExercise, ReadingExercise

from .concepts import CONCEPT_DESCRIPTIONS, get_concepts_for_level, get_difficulty
from .profiler import StudentProfile
from .scorer import score_answer
from .selector import AdaptiveSelector

DEFAULT_PROFILE_PATH = Path.home() / ".german" / "profile.json"


class DrillSession:
    """Interactive adaptive drill session."""

    def __init__(self, level: str, num_questions: int = 10, profile_path: Path = DEFAULT_PROFILE_PATH):
        self.level = level.lower()
        self.num_questions = num_questions
        self.profile = StudentProfile.load(profile_path, student_name="Student")
        if self.level not in self.profile.active_levels:
            self.profile.active_levels.append(self.level)
        self.selector = AdaptiveSelector(self.profile, self.level)
        self._questions_answered = 0
        self._session_correct = 0

    def run(self) -> None:
        """Run the interactive drill session."""
        print(f"\n=== German Adaptive Drill — {self.level.upper()} ===")
        concepts = get_concepts_for_level(self.level)
        mastered = sum(
            1 for c in concepts
            if c in self.profile.concepts and self.profile.concepts[c].get("mastered", False)
        )
        print(f"Student: {self.profile.student_name} | Mastered: {mastered}/{len(concepts)} concepts | Session: 0/{self.num_questions}\n")

        while self._questions_answered < self.num_questions:
            result = self.selector.pick_next()
            if result is None:
                print("No exercises available for this level.")
                break

            exercise, concept_id = result
            self._run_exercise(exercise, concept_id)

            if self._questions_answered >= self.num_questions:
                break

            try:
                cont = input("\nContinue? [Y/n]: ").strip().lower()
                if cont == "n":
                    break
            except (EOFError, KeyboardInterrupt):
                break

        self._show_session_summary()
        self.profile.save()

    def _run_exercise(self, exercise, concept_id: str) -> None:
        """Run a single exercise — present all questions."""
        desc = CONCEPT_DESCRIPTIONS.get(concept_id, concept_id)
        prof = self.profile.get_proficiency(concept_id)
        bar = self._proficiency_bar(prof)
        priority = "HIGH" if prof < 0.5 else "MED" if prof < 0.85 else "LOW"

        print(f"\n{'─' * 50}")
        teil_num = int(concept_id.split("-")[-1])
        skill_name = "Lesen" if "lesen" in concept_id else "Hören"
        print(f"{skill_name} Teil {teil_num}: {desc}")
        print(f"[Proficiency: {prof:.2f} {bar} | Priority: {priority}]")
        print()

        # Show passage or transcript context
        if isinstance(exercise, ReadingExercise):
            print(exercise.instructions)
            print()
            print(exercise.passage.text_de)
            print()
        elif isinstance(exercise, ListeningExercise):
            print(exercise.instructions)
            print()
            print("[Transcript]")
            for line in exercise.transcript:
                print(f"  {line.speaker}: {line.text_de}")
            print()

        difficulty = get_difficulty(teil_num)

        for i, question in enumerate(exercise.questions):
            if self._questions_answered >= self.num_questions:
                break

            print(f"Frage {i + 1}/{len(exercise.questions)}: {question.text_de}")
            if question.options:
                for opt in question.options:
                    print(f"  {opt}")

            try:
                user_answer = input("\nYour answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_answer:
                continue

            result = score_answer(question, user_answer)
            self.profile.update(concept_id, result.is_correct, difficulty, exercise.id, question.number)

            self._questions_answered += 1
            if result.is_correct:
                self._session_correct += 1
                new_prof = self.profile.get_proficiency(concept_id)
                print(f"✓ Richtig! ({prof:.2f} → {new_prof:.2f})")
            else:
                new_prof = self.profile.get_proficiency(concept_id)
                print(f"✗ Falsch. Richtige Antwort: {result.correct_answer} ({prof:.2f} → {new_prof:.2f})")

            if result.explanation_de:
                print(f"  {result.explanation_de}")

            prof = new_prof
            print()

    def _show_session_summary(self) -> None:
        """Show end-of-session summary."""
        print(f"\n{'═' * 50}")
        print(f"Session complete: {self._session_correct}/{self._questions_answered} correct")
        if self._questions_answered > 0:
            print(f"Accuracy: {self._session_correct / self._questions_answered:.0%}")
        print()

    def show_stats(self) -> None:
        """Show progress dashboard."""
        concepts = get_concepts_for_level(self.level)
        print(f"\n=== {self.level.upper()} Progress ===")
        print(f"{'Concept':<30} {'Prof.':>6} {'Mastered':>8}  {'Last':<12} {'Next Review':<12}")
        print("─" * 75)

        for cid in concepts:
            desc = CONCEPT_DESCRIPTIONS.get(cid, cid)
            short_desc = desc[:25] if len(desc) > 25 else desc

            teil = cid.split("-")[-1]
            skill = "Lesen" if "lesen" in cid else "Hören"
            label = f"{skill} Teil {teil} ({short_desc})"

            if cid in self.profile.concepts:
                c = self.profile.concepts[cid]
                prof = c["proficiency"]
                mastered = "✓" if c["mastered"] else "·"
                last = self._format_relative_date(c.get("last_attempt"))
                next_rev = self._format_date(c.get("next_review"))
                if c.get("next_review"):
                    if datetime.fromisoformat(c["next_review"]) < datetime.now():
                        next_rev += " !"
            else:
                prof = 0.0
                mastered = "·"
                last = "never"
                next_rev = "—"

            print(f"{label:<30} {prof:>5.2f} {mastered:>8}  {last:<12} {next_rev:<12}")

        stats = self.profile.get_stats()
        print()
        total_mastered = sum(
            1 for c in concepts
            if c in self.profile.concepts and self.profile.concepts[c].get("mastered", False)
        )
        print(f"Overall: {total_mastered}/{len(concepts)} mastered | {stats['total_attempts']} questions answered | {stats['accuracy']:.0%} accuracy")

    @staticmethod
    def _proficiency_bar(prof: float, width: int = 10) -> str:
        filled = int(prof * width)
        return "▓" * filled + "░" * (width - filled)

    @staticmethod
    def _format_relative_date(iso_str: str | None) -> str:
        if not iso_str:
            return "never"
        dt = datetime.fromisoformat(iso_str)
        days = (datetime.now() - dt).days
        if days == 0:
            return "today"
        elif days == 1:
            return "yesterday"
        else:
            return f"{days}d ago"

    @staticmethod
    def _format_date(iso_str: str | None) -> str:
        if not iso_str:
            return "—"
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%b %d")


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="German Adaptive Drill")
    parser.add_argument("--level", choices=["a1", "a2", "b1", "b2", "c1", "c2"], help="CEFR level to drill")
    parser.add_argument("--questions", type=int, default=10, help="Questions per session (default: 10)")
    parser.add_argument("--stats", action="store_true", help="Show progress dashboard")
    parser.add_argument("--reset", action="store_true", help="Reset profile")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE_PATH, help="Profile path")
    args = parser.parse_args()

    if args.reset:
        if args.profile.exists():
            args.profile.unlink()
            print("Profile reset.")
        else:
            print("No profile to reset.")
        return

    if args.stats:
        if not args.level:
            # Try to get level from existing profile
            if args.profile.exists():
                profile = StudentProfile.load(args.profile)
                if profile.active_levels:
                    args.level = profile.active_levels[0]
                else:
                    print("No active level. Use --level to set one.")
                    sys.exit(1)
            else:
                print("No profile found. Start a drill session first.")
                sys.exit(1)
        session = DrillSession(level=args.level, num_questions=0, profile_path=args.profile)
        session.show_stats()
        return

    if not args.level:
        # Try existing profile
        if args.profile.exists():
            profile = StudentProfile.load(args.profile)
            if profile.active_levels:
                args.level = profile.active_levels[0]
                print(f"Continuing with level {args.level.upper()}")
            else:
                print("No active level. Use --level to set one.")
                sys.exit(1)
        else:
            print("First run — use --level to set your CEFR level (e.g., --level a2)")
            sys.exit(1)

    session = DrillSession(level=args.level, num_questions=args.questions, profile_path=args.profile)
    session.run()
