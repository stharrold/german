"""Data models for German B1 exam exercises."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class QuestionType(str, Enum):
    """Types of exam questions."""

    TRUE_FALSE = "true_false"
    MULTIPLE_CHOICE = "multiple_choice"
    MATCHING = "matching"


class ExamSkill(str, Enum):
    """Exam skill sections (Goethe-Institut B1 format)."""

    HOEREN = "hoeren"
    LESEN = "lesen"
    SCHREIBEN = "schreiben"
    SPRECHEN = "sprechen"


class ExamMeta(BaseModel):
    """Metadata for an exam configuration."""

    level: str = Field(..., description="CEFR level (e.g. B1)")
    provider: str = Field(..., description="Exam provider (e.g. Goethe-Institut)")
    total_time_minutes: int = Field(..., description="Total exam time in minutes")
    passing_score_percent: int = Field(..., description="Minimum passing score percentage")

    model_config = ConfigDict(use_enum_values=True)


class Question(BaseModel):
    """A single exam question."""

    number: int = Field(..., description="Question number")
    type: QuestionType = Field(..., description="Question type")
    text_de: str = Field(..., description="Question text in German")
    text_en: Optional[str] = Field(None, description="Question text in English")
    correct_answer: bool | str = Field(..., description="Correct answer (bool for true/false, str for others)")
    options: Optional[list[str]] = Field(None, description="Answer options for multiple choice")
    explanation_de: Optional[str] = Field(None, description="Explanation in German")
    explanation_en: Optional[str] = Field(None, description="Explanation in English")

    model_config = ConfigDict(use_enum_values=True)


class TranscriptLine(BaseModel):
    """A single line of dialogue in a listening transcript."""

    speaker: str = Field(..., description="Speaker name or role")
    text_de: str = Field(..., description="Spoken text in German")
    text_en: str = Field(..., description="Spoken text in English")

    model_config = ConfigDict(use_enum_values=True)


class Passage(BaseModel):
    """A reading passage for a reading exercise."""

    text_de: str = Field(..., description="Passage text in German")
    text_en: str = Field(..., description="Passage text in English")
    source: str = Field(..., description="Source attribution")
    word_count: int = Field(..., description="Word count of the German text")

    model_config = ConfigDict(use_enum_values=True)


class ModelAnswer(BaseModel):
    """A model answer for a writing or speaking exercise."""

    text_de: str = Field(..., description="Model answer in German")
    text_en: str = Field(..., description="Model answer in English")

    model_config = ConfigDict(use_enum_values=True)


class ListeningExercise(BaseModel):
    """A listening comprehension exercise (Hoeren)."""

    id: str = Field(..., description="Unique exercise identifier")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill section")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Exercise instructions")
    time_minutes: int = Field(..., description="Time allowed in minutes")
    transcript: list[TranscriptLine] = Field(..., min_length=1, description="Listening transcript lines")
    questions: list[Question] = Field(..., min_length=1, description="Exercise questions")

    model_config = ConfigDict(use_enum_values=True)


class ReadingExercise(BaseModel):
    """A reading comprehension exercise (Lesen)."""

    id: str = Field(..., description="Unique exercise identifier")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill section")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Exercise instructions")
    time_minutes: int = Field(..., description="Time allowed in minutes")
    passage: Passage = Field(..., description="Reading passage")
    questions: list[Question] = Field(..., min_length=1, description="Exercise questions")

    model_config = ConfigDict(use_enum_values=True)


class WritingExercise(BaseModel):
    """A writing exercise (Schreiben)."""

    id: str = Field(..., description="Unique exercise identifier")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    task: int = Field(..., description="Task number within the skill section")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Exercise instructions")
    situation_de: str = Field(..., description="Situation description in German")
    situation_en: str = Field(..., description="Situation description in English")
    target_word_count: int = Field(..., description="Target word count for the response")
    required_points: list[str] = Field(..., min_length=1, description="Required content points to address")
    model_answer: ModelAnswer = Field(..., description="Model answer")
    scoring_criteria: list[str] = Field(..., min_length=1, description="Scoring criteria")

    model_config = ConfigDict(use_enum_values=True)


class SpeakingExercise(BaseModel):
    """A speaking exercise (Sprechen)."""

    id: str = Field(..., description="Unique exercise identifier")
    level: str = Field(..., description="CEFR level")
    skill: ExamSkill = Field(..., description="Exam skill section")
    part: int = Field(..., description="Part number within the skill section")
    title: str = Field(..., description="Exercise title")
    instructions: str = Field(..., description="Exercise instructions")
    situation_de: str = Field(..., description="Situation description in German")
    situation_en: str = Field(..., description="Situation description in English")
    discussion_points: list[str] = Field(..., min_length=1, description="Discussion points to cover")
    model_dialogue: list[TranscriptLine] = Field(..., description="Model dialogue lines")
    evaluation_criteria: list[str] = Field(..., min_length=1, description="Evaluation criteria")

    model_config = ConfigDict(use_enum_values=True)
