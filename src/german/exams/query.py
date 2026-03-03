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


def filter_by_skill(skill: str | ExamSkill, exercises: list[ExamExercise]) -> list[ExamExercise]:
    """Filter exercises by exam skill section.

    Args:
        skill: Exam skill to filter by (string or ExamSkill enum)
        exercises: List of exercises to filter

    Returns:
        List of exercises matching the specified skill
    """
    if isinstance(skill, str):
        skill = ExamSkill(skill)
    return [ex for ex in exercises if ex.skill == skill]


def filter_by_part(part: int, exercises: list[ExamExercise]) -> list[ExamExercise]:
    """Filter exercises by part number.

    For WritingExercise, matches on the ``task`` field instead of ``part``.

    Args:
        part: Part (or task) number to filter by
        exercises: List of exercises to filter

    Returns:
        List of exercises matching the specified part/task number
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


def filter_by_question_type(question_type: str | QuestionType, exercises: list[ExamExercise]) -> list[ExamExercise]:
    """Filter exercises that contain at least one question of the given type.

    Args:
        question_type: Question type to filter by (string or QuestionType enum)
        exercises: List of exercises to filter

    Returns:
        List of exercises that have at least one question of the specified type
    """
    if isinstance(question_type, str):
        question_type = QuestionType(question_type)
    result: list[ExamExercise] = []
    for ex in exercises:
        if isinstance(ex, (ListeningExercise, ReadingExercise)):
            if any(q.type == question_type for q in ex.questions):
                result.append(ex)
    return result
