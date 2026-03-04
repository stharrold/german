"""Data models for German vocabulary."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CEFRLevel(str, Enum):
    """CEFR proficiency levels for vocabulary."""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class PartOfSpeech(str, Enum):
    """Part of speech categories."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"


class Gender(str, Enum):
    """Grammatical gender for German nouns."""

    MASCULINE = "masculine"  # der
    FEMININE = "feminine"  # die
    NEUTER = "neuter"  # das


class VocabularyWord(BaseModel):
    """A German vocabulary word with linguistic metadata."""

    german: str = Field(..., description="German word")
    english: str = Field(..., description="English translation")
    part_of_speech: PartOfSpeech

    # CEFR level
    level: Optional[CEFRLevel] = Field(None, description="CEFR proficiency level (A1-C2)")

    # Noun-specific fields
    gender: Optional[Gender] = Field(None, description="Grammatical gender (nouns only)")
    plural: Optional[str] = Field(None, description="Plural form (nouns only)")

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def validate_noun_requirements(self) -> "VocabularyWord":
        """Validate that nouns have required gender field."""
        if self.part_of_speech == PartOfSpeech.NOUN and self.gender is None:
            raise ValueError(f"Noun '{self.german}' must have a gender (der/die/das)")
        return self
