"""Tests for German vocabulary models."""

import pytest
from pydantic import ValidationError

from german.models import CEFRLevel, Gender, PartOfSpeech, VocabularyWord


def test_vocabulary_word_noun_with_gender():
    """Test creating a noun with all required fields."""
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.NEUTER,
        plural="Häuser",
    )
    assert word.german == "Haus"
    assert word.english == "house"
    assert word.part_of_speech == PartOfSpeech.NOUN
    assert word.gender == Gender.NEUTER
    assert word.plural == "Häuser"


def test_vocabulary_word_verb():
    """Test creating a verb (no gender required)."""
    word = VocabularyWord(
        german="lernen",
        english="to learn",
        part_of_speech=PartOfSpeech.VERB,
    )
    assert word.german == "lernen"
    assert word.english == "to learn"
    assert word.part_of_speech == PartOfSpeech.VERB
    assert word.gender is None
    assert word.plural is None


def test_vocabulary_word_adjective():
    """Test creating an adjective."""
    word = VocabularyWord(
        german="schön",
        english="beautiful",
        part_of_speech=PartOfSpeech.ADJECTIVE,
    )
    assert word.german == "schön"
    assert word.part_of_speech == PartOfSpeech.ADJECTIVE


def test_noun_without_gender_raises_error():
    """Test that nouns require a gender."""
    with pytest.raises(ValidationError, match="must have a gender"):
        VocabularyWord(
            german="Haus",
            english="house",
            part_of_speech=PartOfSpeech.NOUN,
        )


def test_noun_with_umlaut():
    """Test that umlauts are handled correctly."""
    word = VocabularyWord(
        german="Tür",
        english="door",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.FEMININE,
        plural="Türen",
    )
    assert word.german == "Tür"
    assert "ü" in word.german


def test_all_gender_types():
    """Test all grammatical genders."""
    masculine = VocabularyWord(
        german="Mann", english="man", part_of_speech=PartOfSpeech.NOUN, gender=Gender.MASCULINE
    )
    feminine = VocabularyWord(
        german="Frau", english="woman", part_of_speech=PartOfSpeech.NOUN, gender=Gender.FEMININE
    )
    neuter = VocabularyWord(
        german="Kind", english="child", part_of_speech=PartOfSpeech.NOUN, gender=Gender.NEUTER
    )

    assert masculine.gender == Gender.MASCULINE
    assert feminine.gender == Gender.FEMININE
    assert neuter.gender == Gender.NEUTER


def test_all_part_of_speech_types():
    """Test all parts of speech."""
    noun = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.NEUTER,
    )
    verb = VocabularyWord(german="gehen", english="to go", part_of_speech=PartOfSpeech.VERB)
    adjective = VocabularyWord(
        german="groß", english="big", part_of_speech=PartOfSpeech.ADJECTIVE
    )
    adverb = VocabularyWord(german="schnell", english="quickly", part_of_speech=PartOfSpeech.ADVERB)

    assert noun.part_of_speech == PartOfSpeech.NOUN
    assert verb.part_of_speech == PartOfSpeech.VERB
    assert adjective.part_of_speech == PartOfSpeech.ADJECTIVE
    assert adverb.part_of_speech == PartOfSpeech.ADVERB


def test_vocabulary_word_with_level():
    """Test creating a word with CEFR level."""
    word = VocabularyWord(
        german="Haus",
        english="house",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.NEUTER,
        level=CEFRLevel.A1,
    )
    assert word.level == CEFRLevel.A1


def test_vocabulary_word_without_level():
    """Test that level is optional (backward compatible)."""
    word = VocabularyWord(
        german="lernen",
        english="to learn",
        part_of_speech=PartOfSpeech.VERB,
    )
    assert word.level is None


def test_all_cefr_levels():
    """Test all CEFR levels are valid."""
    for level in CEFRLevel:
        word = VocabularyWord(
            german="test",
            english="test",
            part_of_speech=PartOfSpeech.VERB,
            level=level,
        )
        assert word.level == level

    assert len(CEFRLevel) == 6


def test_cefr_level_from_string():
    """Test creating a word with level as string."""
    word = VocabularyWord(
        german="gehen",
        english="to go",
        part_of_speech=PartOfSpeech.VERB,
        level="B1",
    )
    assert word.level == CEFRLevel.B1
