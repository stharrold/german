"""Tests for adaptive learning answer scorer."""

from german.adaptive.scorer import score_answer
from german.exams.models import Question, QuestionType


def _make_mc_question(correct: str = "b") -> Question:
    return Question(
        number=1, type=QuestionType.MULTIPLE_CHOICE,
        text_de="Was ist richtig?", correct_answer=correct,
        options=["a) Ja", "b) Nein", "c) Vielleicht"],
        explanation_de="Erklärung", explanation_en="Explanation",
    )


def _make_tf_question(correct: bool = True) -> Question:
    return Question(
        number=1, type=QuestionType.TRUE_FALSE,
        text_de="Sarah ist in Afrika geboren.", correct_answer=correct,
    )


def _make_matching_question(correct: str = "c") -> Question:
    return Question(
        number=6, type=QuestionType.MATCHING,
        text_de="Sie möchten Rosen schenken.", correct_answer=correct,
        options=["a", "b", "c"],
    )


def test_score_mc_correct():
    result = score_answer(_make_mc_question("b"), "b")
    assert result.is_correct is True
    assert result.correct_answer == "b"


def test_score_mc_incorrect():
    result = score_answer(_make_mc_question("b"), "a")
    assert result.is_correct is False
    assert result.correct_answer == "b"


def test_score_mc_case_insensitive():
    result = score_answer(_make_mc_question("b"), "B")
    assert result.is_correct is True


def test_score_mc_whitespace():
    result = score_answer(_make_mc_question("b"), " b ")
    assert result.is_correct is True


def test_score_tf_correct_ja():
    result = score_answer(_make_tf_question(True), "ja")
    assert result.is_correct is True


def test_score_tf_correct_nein():
    result = score_answer(_make_tf_question(False), "nein")
    assert result.is_correct is True


def test_score_tf_incorrect():
    result = score_answer(_make_tf_question(True), "nein")
    assert result.is_correct is False


def test_score_tf_richtig_falsch():
    assert score_answer(_make_tf_question(True), "richtig").is_correct is True
    assert score_answer(_make_tf_question(False), "falsch").is_correct is True


def test_score_matching_correct():
    result = score_answer(_make_matching_question("c"), "c")
    assert result.is_correct is True


def test_score_matching_incorrect():
    result = score_answer(_make_matching_question("c"), "a")
    assert result.is_correct is False


def test_score_matching_x():
    q = _make_matching_question("x")
    result = score_answer(q, "x")
    assert result.is_correct is True


def test_score_result_has_explanation():
    result = score_answer(_make_mc_question("b"), "a")
    assert result.explanation_de == "Erklärung"
    assert result.explanation_en == "Explanation"


def test_score_result_no_explanation():
    q = Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="?", correct_answer="a", options=["a", "b"])
    result = score_answer(q, "b")
    assert result.explanation_de is None
