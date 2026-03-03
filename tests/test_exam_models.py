"""Tests for German B1 exam exercise models."""

import json
import re
from pathlib import Path

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
        total_time_minutes=190,
        passing_score_percent=60,
    )
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"
    assert meta.total_time_minutes == 190
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
    assert line.text_de == "Ich möchte gern fünf Brötchen."


def test_listening_exercise_valid():
    """Test creating a full listening exercise."""
    exercise = ListeningExercise(
        id="b1-hoeren-teil-1-001",
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
    assert exercise.id == "b1-hoeren-teil-1-001"
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
            id="b1-hoeren-teil-1-001",
            level="B1",
            skill=ExamSkill.HOEREN,
            part=1,
            title="Test",
            instructions="Test instructions",
            time_minutes=8,
            transcript=[],
            questions=[
                Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Test?", correct_answer=True),
            ],
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
        id="b1-lesen-teil-1-001",
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
    assert exercise.id == "b1-lesen-teil-1-001"
    assert exercise.skill == ExamSkill.LESEN
    assert exercise.passage.source == "Süddeutsche Zeitung"
    assert len(exercise.questions) == 1


def test_reading_exercise_missing_passage():
    """Test that missing passage raises ValidationError."""
    with pytest.raises(ValidationError, match="passage"):
        ReadingExercise(
            id="b1-lesen-teil-1-001",
            level="B1",
            skill=ExamSkill.LESEN,
            part=1,
            title="Test",
            instructions="Test instructions",
            time_minutes=10,
            questions=[
                Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Test?", correct_answer=True),
            ],
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
        id="b1-schreiben-aufgabe-1-001",
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
    assert exercise.id == "b1-schreiben-aufgabe-1-001"
    assert exercise.skill == ExamSkill.SCHREIBEN
    assert exercise.task == 1
    assert exercise.target_word_count == 120
    assert len(exercise.required_points) == 3
    assert len(exercise.scoring_criteria) == 3
    assert exercise.model_answer.text_de.startswith("Sehr geehrte")


def test_speaking_exercise_valid():
    """Test creating a full speaking exercise."""
    exercise = SpeakingExercise(
        id="b1-sprechen-teil-1-001",
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
    assert exercise.id == "b1-sprechen-teil-1-001"
    assert exercise.skill == ExamSkill.SPRECHEN
    assert exercise.part == 1
    assert len(exercise.discussion_points) == 3
    assert len(exercise.model_dialogue) == 2
    assert len(exercise.evaluation_criteria) == 4


def test_speaking_exercise_missing_discussion_points():
    """Test that empty discussion_points raises ValidationError (min_length=1)."""
    with pytest.raises(ValidationError, match="discussion_points"):
        SpeakingExercise(
            id="b1-sprechen-teil-1-001",
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


def test_meta_json_exists():
    """Test that meta.json exists for B1 exam."""
    meta_path = Path(__file__).parent.parent / "resources" / "exams" / "b1" / "meta.json"
    assert meta_path.exists(), f"meta.json not found at {meta_path}"


def test_meta_json_valid():
    """Test that meta.json validates against ExamMeta model."""
    meta_path = Path(__file__).parent.parent / "resources" / "exams" / "b1" / "meta.json"
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = ExamMeta(**data)
    assert meta.level == "B1"
    assert meta.provider == "Goethe-Institut"


def test_b1_directory_structure():
    """Test that all expected B1 exam directories exist."""
    b1_dir = Path(__file__).parent.parent / "resources" / "exams" / "b1"
    expected_dirs = [
        "hoeren/teil-1", "hoeren/teil-2", "hoeren/teil-3", "hoeren/teil-4",
        "lesen/teil-1", "lesen/teil-2", "lesen/teil-3", "lesen/teil-4", "lesen/teil-5",
        "schreiben/aufgabe-1", "schreiben/aufgabe-2", "schreiben/aufgabe-3",
        "sprechen/teil-1", "sprechen/teil-2", "sprechen/teil-3",
    ]
    for subdir in expected_dirs:
        assert (b1_dir / subdir).is_dir(), f"Missing directory: {b1_dir / subdir}"


def test_listening_exercise_roundtrip_json():
    """Test that a listening exercise survives JSON round-trip."""
    exercise = ListeningExercise(
        id="b1-hoeren-teil-1-001",
        level="B1",
        skill=ExamSkill.HOEREN,
        part=1,
        title="Ansagen am Bahnhof",
        instructions="Sie hören fünf kurze Texte. Sie hören jeden Text zweimal.",
        time_minutes=10,
        transcript=[
            TranscriptLine(
                speaker="Sprecher",
                text_de="Achtung auf Gleis drei: Der Zug nach München fährt in fünf Minuten ab.",
                text_en="Attention on platform three: The train to Munich departs in five minutes.",
            )
        ],
        questions=[
            Question(
                number=1,
                type=QuestionType.TRUE_FALSE,
                text_de="Der Zug fährt nach München.",
                text_en="The train goes to Munich.",
                correct_answer=True,
                explanation_de="Die Durchsage sagt 'Zug nach München'.",
                explanation_en="The announcement says 'train to Munich'.",
            )
        ],
    )
    json_str = exercise.model_dump_json()
    reloaded = ListeningExercise.model_validate_json(json_str)
    assert reloaded.id == exercise.id
    assert reloaded.transcript[0].text_de == exercise.transcript[0].text_de
    assert reloaded.questions[0].correct_answer == exercise.questions[0].correct_answer


def test_writing_exercise_roundtrip_json():
    """Test that a writing exercise survives JSON round-trip."""
    exercise = WritingExercise(
        id="b1-schreiben-aufgabe-1-001",
        level="B1",
        skill=ExamSkill.SCHREIBEN,
        task=1,
        title="E-Mail an einen Freund",
        instructions="Schreiben Sie eine E-Mail.",
        situation_de="Ihr Freund hat eine neue Wohnung gefunden.",
        situation_en="Your friend found a new apartment.",
        target_word_count=80,
        required_points=["react to news", "ask about the apartment", "suggest a visit"],
        model_answer=ModelAnswer(
            text_de="Lieber Max, ich freue mich sehr über deine neue Wohnung!",
            text_en="Dear Max, I am very happy about your new apartment!",
        ),
        scoring_criteria=["task fulfillment", "coherence", "vocabulary range", "grammar accuracy"],
    )
    json_str = exercise.model_dump_json()
    reloaded = WritingExercise.model_validate_json(json_str)
    assert reloaded.task == exercise.task
    assert reloaded.model_answer.text_de == exercise.model_answer.text_de


EXERCISE_ID_PATTERN = re.compile(r"^b1-(hoeren|lesen|schreiben|sprechen)-(teil|aufgabe)-\d+-\d{3}$")


def test_exercise_id_format():
    """Test that exercise IDs follow the naming convention."""
    exercises = [
        ListeningExercise(
            id="b1-hoeren-teil-1-001",
            level="B1",
            skill=ExamSkill.HOEREN,
            part=1,
            title="T",
            instructions="I",
            time_minutes=10,
            transcript=[TranscriptLine(speaker="n", text_de="D.", text_en="E.")],
            questions=[Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Q?", correct_answer=True)],
        ),
        ReadingExercise(
            id="b1-lesen-teil-2-003",
            level="B1",
            skill=ExamSkill.LESEN,
            part=2,
            title="T",
            instructions="I",
            time_minutes=13,
            passage=Passage(text_de="T.", text_en="T.", source="Blog", word_count=100),
            questions=[Question(number=1, type=QuestionType.TRUE_FALSE, text_de="Q?", correct_answer=True)],
        ),
        WritingExercise(
            id="b1-schreiben-aufgabe-1-001",
            level="B1",
            skill=ExamSkill.SCHREIBEN,
            task=1,
            title="T",
            instructions="I",
            situation_de="S.",
            situation_en="S.",
            target_word_count=80,
            required_points=["p1"],
            model_answer=ModelAnswer(text_de="A.", text_en="A."),
            scoring_criteria=["c1"],
        ),
        SpeakingExercise(
            id="b1-sprechen-teil-3-001",
            level="B1",
            skill=ExamSkill.SPRECHEN,
            part=3,
            title="T",
            instructions="I",
            situation_de="S.",
            situation_en="S.",
            discussion_points=["p1"],
            model_dialogue=[TranscriptLine(speaker="A", text_de="D.", text_en="E.")],
            evaluation_criteria=["c1"],
        ),
    ]
    for ex in exercises:
        assert EXERCISE_ID_PATTERN.match(ex.id), f"ID '{ex.id}' doesn't match expected format"


def test_umlaut_preservation_in_models():
    """Test that German umlauts and ß survive model creation."""
    line = TranscriptLine(
        speaker="Prüfer",
        text_de="Möchten Sie über Ihre Erfahrungen in der Großstadt erzählen?",
        text_en="Would you like to talk about your experiences in the big city?",
    )
    assert "ü" in line.speaker
    assert "ö" in line.text_de
    assert "ß" in line.text_de
    assert "ä" in line.text_de
