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


class VerbForms(BaseModel):
    """Verb conjugation forms (e.g. from Goethe Wortliste)."""

    present_3p: Optional[str] = Field(None, description="3rd person present, e.g. 'holt ab'")
    past_participle: Optional[str] = Field(None, description="Past participle, e.g. 'abgeholt'")
    auxiliary: Optional[str] = Field(None, description="Auxiliary verb: 'hat' or 'ist'")

    model_config = ConfigDict(use_enum_values=True)


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

    # Enrichment fields (all optional for backward compatibility)
    source: Optional[str] = Field(None, description="Content provenance: ai-generated, goethe-wortliste, both")
    examples_de: Optional[list[str]] = Field(None, description="German example sentences")
    examples_en: Optional[list[str]] = Field(None, description="English translations of examples")
    verb_forms: Optional[VerbForms] = Field(None, description="Verb conjugation forms")
    thematic_group: Optional[str] = Field(None, description="Thematic group, e.g. Berufe, Familie")
    separable_prefix: Optional[bool] = Field(None, description="True for separable prefix verbs")

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def validate_noun_requirements(self) -> "VocabularyWord":
        """Validate that nouns have required gender field."""
        if self.part_of_speech == PartOfSpeech.NOUN and self.gender is None:
            raise ValueError(f"Noun '{self.german}' must have a gender (der/die/das)")
        return self
