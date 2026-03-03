"""Tests for German B1 exam exercise models."""

import pytest
from pydantic import ValidationError

from german.exams.models import (
    ExamMeta,
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


def test_exam_meta_valid():
    """Test creating a valid ExamMeta instance."""
    meta = ExamMeta(
        level="B1",
        provider="Goethe-Institut",
        total_time_minutes=165,
        passing_score_percent=60,
    )
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"
    assert meta.total_time_minutes == 165
    assert meta.passing_score_percent == 60


def test_exam_meta_missing_level():
    """Test that missing level raises ValidationError."""
    with pytest.raises(ValidationError, match="level"):
        ExamMeta(
            provider="Goethe-Institut",
            total_time_minutes=165,
            passing_score_percent=60,
        )


def test_question_type_values():
    """Test all QuestionType enum values."""
    assert QuestionType.TRUE_FALSE == "true_false"
    assert QuestionType.MULTIPLE_CHOICE == "multiple_choice"
    assert QuestionType.MATCHING == "matching"
    assert len(QuestionType) == 3


def test_exam_skill_values():
    """Test all ExamSkill enum values."""
    assert ExamSkill.HOEREN == "hoeren"
    assert ExamSkill.LESEN == "lesen"
    assert ExamSkill.SCHREIBEN == "schreiben"
    assert ExamSkill.SPRECHEN == "sprechen"
    assert len(ExamSkill) == 4


def test_question_true_false():
    """Test creating a true/false question with all fields."""
    question = Question(
        number=1,
        type=QuestionType.TRUE_FALSE,
        text_de="Die Frau geht zum Markt.",
        text_en="The woman goes to the market.",
        correct_answer=True,
        options=None,
        explanation_de="Im Text steht, dass die Frau zum Markt geht.",
        explanation_en="The text states that the woman goes to the market.",
    )
    assert question.number == 1
    assert question.type == QuestionType.TRUE_FALSE
    assert question.text_de == "Die Frau geht zum Markt."
    assert question.text_en == "The woman goes to the market."
    assert question.correct_answer is True
    assert question.options is None
    assert question.explanation_de == "Im Text steht, dass die Frau zum Markt geht."
    assert question.explanation_en == "The text states that the woman goes to the market."


def test_question_multiple_choice():
    """Test creating a multiple choice question with options."""
    question = Question(
        number=2,
        type=QuestionType.MULTIPLE_CHOICE,
        text_de="Was kauft der Mann?",
        text_en="What does the man buy?",
        correct_answer="b",
        options=["a) Brot", "b) Milch", "c) Eier"],
    )
    assert question.number == 2
    assert question.type == QuestionType.MULTIPLE_CHOICE
    assert question.correct_answer == "b"
    assert question.options == ["a) Brot", "b) Milch", "c) Eier"]
    assert len(question.options) == 3


def test_question_missing_number():
    """Test that missing number raises ValidationError."""
    with pytest.raises(ValidationError, match="number"):
        Question(
            type=QuestionType.TRUE_FALSE,
            text_de="Eine Frage.",
            correct_answer=True,
        )


def test_transcript_line():
    """Test creating a transcript line."""
    line = TranscriptLine(
        speaker="Moderator",
        text_de="Willkommen zum Programm.",
        text_en="Welcome to the program.",
    )
    assert line.speaker == "Moderator"
    assert line.text_de == "Willkommen zum Programm."
    assert line.text_en == "Welcome to the program."


def test_transcript_line_umlaut():
    """Test that umlauts are preserved in transcript lines."""
    line = TranscriptLine(
        speaker="Sprecher",
        text_de="Ich möchte gern fünf Brötchen.",
        text_en="I would like five bread rolls.",
    )
    assert "ö" in line.text_de
    assert "ü" in line.text_de
    assert "ö" in line.text_de


def test_listening_exercise_valid():
    """Test creating a full listening exercise."""
    exercise = ListeningExercise(
        id="b1-hoeren-teil1-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Telefonansage verstehen",
        instructions="Sie hören eine Telefonansage. Lesen Sie die Aufgabe und kreuzen Sie an.",
        time_minutes=8,
        transcript=[
            TranscriptLine(
                speaker="Ansage",
                text_de="Herzlich willkommen bei der Volkshochschule Berlin.",
                text_en="Welcome to the Berlin Adult Education Center.",
            ),
            TranscriptLine(
                speaker="Ansage",
                text_de="Unsere Öffnungszeiten sind Montag bis Freitag von 9 bis 17 Uhr.",
                text_en="Our opening hours are Monday to Friday from 9 to 5.",
            ),
        ],
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="Die Volkshochschule ist am Samstag geöffnet.",
                text_en="The adult education center is open on Saturday.",
                correct_answer=False,
            ),
        ],
    )
    assert exercise.id == "b1-hoeren-teil1-001"
    assert exercise.level == "B1"
    assert exercise.skill == ExamSkill.HOEREN
    assert exercise.part == 1
    assert exercise.time_minutes == 8
    assert len(exercise.transcript) == 2
    assert len(exercise.questions) == 1


def test_listening_exercise_missing_transcript():
    """Test that empty transcript raises ValidationError (min_length=1)."""
    with pytest.raises(ValidationError, match="transcript"):
        ListeningExercise(
            id="b1-hoeren-teil1-001",
            level="B1",
            skill=ExamSkill.HOEREN,
            part=1,
            title="Test",
            instructions="Test instructions",
            time_minutes=8,
            transcript=[],
            questions=[],
        )


def test_passage():
    """Test creating a passage."""
    passage = Passage(
        text_de="Berlin ist die Hauptstadt von Deutschland.",
        text_en="Berlin is the capital of Germany.",
        source="Berliner Zeitung",
        word_count=7,
    )
    assert passage.text_de == "Berlin ist die Hauptstadt von Deutschland."
    assert passage.text_en == "Berlin is the capital of Germany."
    assert passage.source == "Berliner Zeitung"
    assert passage.word_count == 7


def test_reading_exercise_valid():
    """Test creating a full reading exercise."""
    exercise = ReadingExercise(
        id="b1-lesen-teil1-001",
        level="B1",
        skill=ExamSkill.LESEN,
        part=1,
        title="Zeitungsartikel verstehen",
        instructions="Lesen Sie den Text und die Aufgaben. Kreuzen Sie an: richtig oder falsch.",
        time_minutes=10,
        passage=Passage(
            text_de="Die Stadt München plant einen neuen Park im Zentrum.",
            text_en="The city of Munich is planning a new park in the center.",
            source="Süddeutsche Zeitung",
            word_count=9,
        ),
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="München baut einen Park.",
                text_en="Munich is building a park.",
                correct_answer=True,
            ),
        ],
    )
    assert exercise.id == "b1-lesen-teil1-001"
    assert exercise.skill == ExamSkill.LESEN
    assert exercise.passage.source == "Süddeutsche Zeitung"
    assert len(exercise.questions) == 1


def test_reading_exercise_missing_passage():
    """Test that missing passage raises ValidationError."""
    with pytest.raises(ValidationError, match="passage"):
        ReadingExercise(
            id="b1-lesen-teil1-001",
            level="B1",
            skill=ExamSkill.LESEN,
            part=1,
            title="Test",
            instructions="Test instructions",
            time_minutes=10,
            questions=[],
        )


def test_model_answer():
    """Test creating a model answer."""
    answer = ModelAnswer(
        text_de="Sehr geehrte Damen und Herren, ich schreibe Ihnen wegen...",
        text_en="Dear Sir or Madam, I am writing to you regarding...",
    )
    assert answer.text_de == "Sehr geehrte Damen und Herren, ich schreibe Ihnen wegen..."
    assert answer.text_en == "Dear Sir or Madam, I am writing to you regarding..."


def test_writing_exercise_valid():
    """Test creating a full writing exercise."""
    exercise = WritingExercise(
        id="b1-schreiben-aufgabe1-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=1,
        title="Formeller Brief",
        instructions="Schreiben Sie einen formellen Brief.",
        situation_de="Sie haben eine Anzeige für einen Sprachkurs gelesen.",
        situation_en="You have read an advertisement for a language course.",
        target_word_count=120,
        required_points=[
            "Grund für das Schreiben",
            "Informationen über den Kurs",
            "Ihre Verfügbarkeit",
        ],
        model_answer=ModelAnswer(
            text_de="Sehr geehrte Damen und Herren, ich habe Ihre Anzeige gelesen...",
            text_en="Dear Sir or Madam, I have read your advertisement...",
        ),
        scoring_criteria=[
            "Aufgabenerfüllung (Inhalt)",
            "Kommunikative Gestaltung",
            "Formale Richtigkeit",
        ],
    )
    assert exercise.id == "b1-schreiben-aufgabe1-001"
    assert exercise.skill == ExamSkill.SCHREIBEN
    assert exercise.task == 1
    assert exercise.target_word_count == 120
    assert len(exercise.required_points) == 3
    assert len(exercise.scoring_criteria) == 3
    assert exercise.model_answer.text_de.startswith("Sehr geehrte")


def test_speaking_exercise_valid():
    """Test creating a full speaking exercise."""
    exercise = SpeakingExercise(
        id="b1-sprechen-teil1-001",
        level="B1",
        skill=ExamSkill.SPRECHEN,
        part=1,
        title="Gemeinsam etwas planen",
        instructions="Sie und Ihr Partner planen zusammen ein Fest.",
        situation_de="Sie möchten ein Sommerfest organisieren.",
        situation_en="You want to organize a summer party.",
        discussion_points=[
            "Wann soll das Fest stattfinden?",
            "Wo soll das Fest stattfinden?",
            "Was soll es zu essen geben?",
        ],
        model_dialogue=[
            TranscriptLine(
                speaker="Teilnehmer A",
                text_de="Ich schlage vor, dass wir das Fest am Samstag machen.",
                text_en="I suggest we have the party on Saturday.",
            ),
            TranscriptLine(
                speaker="Teilnehmer B",
                text_de="Gute Idee! Und wo sollen wir feiern?",
                text_en="Good idea! And where should we celebrate?",
            ),
        ],
        evaluation_criteria=[
            "Aufgabenerfüllung",
            "Interaktion",
            "Wortschatz und Strukturen",
            "Aussprache und Intonation",
        ],
    )
    assert exercise.id == "b1-sprechen-teil1-001"
    assert exercise.skill == ExamSkill.SPRECHEN
    assert exercise.part == 1
    assert len(exercise.discussion_points) == 3
    assert len(exercise.model_dialogue) == 2
    assert len(exercise.evaluation_criteria) == 4


def test_speaking_exercise_missing_discussion_points():
    """Test that empty discussion_points raises ValidationError (min_length=1)."""
    with pytest.raises(ValidationError, match="discussion_points"):
        SpeakingExercise(
            id="b1-sprechen-teil1-001",
            level="B1",
            skill=ExamSkill.SPRECHEN,
            part=1,
            title="Test",
            instructions="Test instructions",
            situation_de="Test Situation",
            situation_en="Test situation",
            discussion_points=[],
            model_dialogue=[],
            evaluation_criteria=["Criterion 1"],
        )
