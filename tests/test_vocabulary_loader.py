"""Tests for vocabulary loader."""

import pytest

from german.models import Gender, PartOfSpeech
from german.vocabulary import VocabularyLoadError, load_vocabulary


def test_load_all_vocabulary():
    """Test loading all vocabulary files."""
    vocab = load_vocabulary()
    assert len(vocab) > 0
    assert all(hasattr(word, "german") for word in vocab)
    assert all(hasattr(word, "english") for word in vocab)


def test_load_vocabulary_has_nouns():
    """Test that loaded vocabulary includes nouns."""
    vocab = load_vocabulary()
    nouns = [word for word in vocab if word.part_of_speech == PartOfSpeech.NOUN]
    assert len(nouns) > 0
    # All nouns should have gender
    assert all(noun.gender is not None for noun in nouns)


def test_load_vocabulary_has_verbs():
    """Test that loaded vocabulary includes verbs."""
    vocab = load_vocabulary()
    verbs = [word for word in vocab if word.part_of_speech == PartOfSpeech.VERB]
    assert len(verbs) > 0


def test_load_vocabulary_has_adjectives():
    """Test that loaded vocabulary includes adjectives."""
    vocab = load_vocabulary()
    adjectives = [word for word in vocab if word.part_of_speech == PartOfSpeech.ADJECTIVE]
    assert len(adjectives) > 0


def test_load_nouns_category():
    """Test loading only nouns category."""
    nouns = load_vocabulary(category="nouns")
    assert len(nouns) > 0
    assert all(word.part_of_speech == PartOfSpeech.NOUN for word in nouns)


def test_load_verbs_category():
    """Test loading only verbs category."""
    verbs = load_vocabulary(category="verbs")
    assert len(verbs) > 0
    assert all(word.part_of_speech == PartOfSpeech.VERB for word in verbs)


def test_load_adjectives_category():
    """Test loading only adjectives category."""
    adjectives = load_vocabulary(category="adjectives")
    assert len(adjectives) > 0
    assert all(word.part_of_speech == PartOfSpeech.ADJECTIVE for word in adjectives)


def test_vocabulary_has_umlauts():
    """Test that vocabulary includes German umlauts."""
    vocab = load_vocabulary()
    german_words = [word.german for word in vocab]
    all_text = " ".join(german_words)

    # Check for umlauts and eszett
    assert any(char in all_text for char in ["ä", "ö", "ü", "Ä", "Ö", "Ü", "ß"])


def test_vocabulary_has_all_genders():
    """Test that vocabulary includes all three genders."""
    vocab = load_vocabulary()
    nouns = [word for word in vocab if word.part_of_speech == PartOfSpeech.NOUN]

    genders = {noun.gender for noun in nouns}
    assert Gender.MASCULINE in genders
    assert Gender.FEMININE in genders
    assert Gender.NEUTER in genders


def test_vocabulary_count():
    """Test that we have a reasonable amount of vocabulary."""
    vocab = load_vocabulary()
    assert len(vocab) >= 50, "Should have at least 50 vocabulary words"


def test_load_nonexistent_category_raises_error():
    """Test that loading a nonexistent category raises an error."""
    with pytest.raises(VocabularyLoadError):
        load_vocabulary(category="nonexistent")
