"""Tests for exam exercise query functions."""

from german.exams.models import (
    ExamSkill,
    ListeningExercise,
    ModelAnswer,
    Passage,
    Question,
    QuestionType,
    ReadingExercise,
    SpeakingExercise,
    TranscriptLine,
    WritingExercise,
)
from german.exams.query import filter_by_part, filter_by_question_type, filter_by_skill


def _make_listening(part: int = 1) -> ListeningExercise:
    return ListeningExercise(
        id=f"b1-hoeren-teil-{part}-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=part,
        title="Test",
        instructions="Test",
        time_minutes=10,
        transcript=[TranscriptLine(speaker="narrator", text_de="Test.", text_en="Test.")],
        questions=[Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Test?", correct_answer=True)],
    )


def _make_reading(part: int = 1) -> ReadingExercise:
    return ReadingExercise(
        id=f"b1-lesen-teil-{part}-001",
        level="B1",
        skill=ExamSkill.LESEN,
        part=part,
        title="Test",
        instructions="Test",
        time_minutes=13,
        passage=Passage(text_de="Text.", text_en="Text.", source="Blog", word_count=100),
        questions=[Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="Was?", correct_answer="a", options=["a) X", "b) Y", "c) Z"])],
    )


def _make_writing(task: int = 1) -> WritingExercise:
    return WritingExercise(
        id=f"b1-schreiben-aufgabe-{task}-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=task,
        title="Test",
        instructions="Test",
        situation_de="Test.",
        situation_en="Test.",
        target_word_count=80,
        required_points=["point 1"],
        model_answer=ModelAnswer(text_de="Antwort.", text_en="Answer."),
        scoring_criteria=["criterion 1"],
    )


def _make_speaking(part: int = 1) -> SpeakingExercise:
    return SpeakingExercise(
        id=f"b1-sprechen-teil-{part}-001",
        level="B1",
        skill=ExamSkill.SPRECHEN,
        part=part,
        title="Test",
        instructions="Test",
        situation_de="Test.",
        situation_en="Test.",
        discussion_points=["Punkt 1"],
        model_dialogue=[TranscriptLine(speaker="A", text_de="Test.", text_en="Test.")],
        evaluation_criteria=["criterion 1"],
    )


def test_filter_by_skill_hoeren():
    exercises = [_make_listening(), _make_reading(), _make_writing(), _make_speaking()]
    result = filter_by_skill(ExamSkill.HOEREN, exercises)
    assert len(result) == 1
    assert all(e.skill == ExamSkill.HOEREN for e in result)


def test_filter_by_skill_string():
    exercises = [_make_listening(), _make_reading()]
    result = filter_by_skill("lesen", exercises)
    assert len(result) == 1


def test_filter_by_skill_empty():
    exercises = [_make_listening()]
    result = filter_by_skill(ExamSkill.SPRECHEN, exercises)
    assert result == []


def test_filter_by_part():
    exercises = [_make_listening(part=1), _make_listening(part=2), _make_listening(part=3)]
    result = filter_by_part(2, exercises)
    assert len(result) == 1
    assert result[0].part == 2


def test_filter_by_part_writing_uses_task():
    exercises = [_make_writing(task=1), _make_writing(task=2)]
    result = filter_by_part(2, exercises)
    assert len(result) == 1


def test_filter_by_question_type():
    listening = _make_listening()
    reading = _make_reading()
    exercises = [listening, reading]
    result = filter_by_question_type(QuestionType.TRUE_FALSE, exercises)
    assert len(result) == 1


def test_filter_by_question_type_string():
    exercises = [_make_listening()]
    result = filter_by_question_type("true_false", exercises)
    assert len(result) == 1
