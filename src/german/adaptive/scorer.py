"""Answer scorer for adaptive learning.

Scores student answers against correct answers for multiple choice,
true/false, and matching question types.
"""

from dataclasses import dataclass

from german.exams.models import Question, QuestionType


@dataclass
class ScoreResult:
    """Result of scoring a student's answer."""

    is_correct: bool
    correct_answer: str
    explanation_de: str | None = None
    explanation_en: str | None = None


def score_answer(question: Question, user_answer: str) -> ScoreResult:
    """Score a student's answer against the correct answer."""
    user_clean = user_answer.strip().lower()

    if question.type == QuestionType.TRUE_FALSE:
        user_bool = user_clean in ("ja", "true", "richtig")
        correct_bool = question.correct_answer if isinstance(question.correct_answer, bool) else str(question.correct_answer).lower() in ("ja", "true", "richtig")
        is_correct = user_bool == correct_bool
        correct_display = "Ja" if correct_bool else "Nein"
    else:
        correct_clean = str(question.correct_answer).strip().lower()
        is_correct = user_clean == correct_clean
        correct_display = str(question.correct_answer)

    return ScoreResult(
        is_correct=is_correct,
        correct_answer=correct_display,
        explanation_de=getattr(question, "explanation_de", None),
        explanation_en=getattr(question, "explanation_en", None),
    )
