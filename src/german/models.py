"""Data models for German vocabulary."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


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

    # Noun-specific fields
    gender: Optional[Gender] = Field(None, description="Grammatical gender (nouns only)")
    plural: Optional[str] = Field(None, description="Plural form (nouns only)")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True

    @model_validator(mode="after")
    def validate_noun_requirements(self) -> "VocabularyWord":
        """Validate that nouns have required gender field."""
        if self.part_of_speech == PartOfSpeech.NOUN and self.gender is None:
            raise ValueError(f"Noun '{self.german}' must have a gender (der/die/das)")
        return self
