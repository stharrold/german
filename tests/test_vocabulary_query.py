"""Tests for vocabulary query functions."""

from german.models import Gender, PartOfSpeech
from german.vocabulary import filter_by_gender, filter_by_pos, get_word, load_vocabulary


def test_get_word_found():
    """Test getting an existing word."""
    vocab = load_vocabulary()
    word = get_word("Haus", vocab)
    assert word is not None
    assert word.german == "Haus"
    assert word.english == "house"


def test_get_word_not_found():
    """Test getting a non-existent word returns None."""
    vocab = load_vocabulary()
    word = get_word("nonexistent", vocab)
    assert word is None


def test_get_word_case_insensitive():
    """Test that word lookup is case-insensitive."""
    vocab = load_vocabulary()
    word1 = get_word("haus", vocab)
    word2 = get_word("Haus", vocab)
    word3 = get_word("HAUS", vocab)
    assert word1 is not None
    assert word2 is not None
    assert word3 is not None
    assert word1.german == word2.german == word3.german


def test_filter_by_pos_nouns():
    """Test filtering by noun part of speech."""
    vocab = load_vocabulary()
    nouns = filter_by_pos(PartOfSpeech.NOUN, vocab)
    assert len(nouns) > 0
    assert all(word.part_of_speech == PartOfSpeech.NOUN for word in nouns)
    assert all(word.gender is not None for word in nouns)


def test_filter_by_pos_verbs():
    """Test filtering by verb part of speech."""
    vocab = load_vocabulary()
    verbs = filter_by_pos(PartOfSpeech.VERB, vocab)
    assert len(verbs) > 0
    assert all(word.part_of_speech == PartOfSpeech.VERB for word in verbs)


def test_filter_by_pos_adjectives():
    """Test filtering by adjective part of speech."""
    vocab = load_vocabulary()
    adjectives = filter_by_pos(PartOfSpeech.ADJECTIVE, vocab)
    assert len(adjectives) > 0
    assert all(word.part_of_speech == PartOfSpeech.ADJECTIVE for word in adjectives)


def test_filter_by_pos_string():
    """Test filtering by part of speech using string."""
    vocab = load_vocabulary()
    nouns = filter_by_pos("noun", vocab)
    assert len(nouns) > 0
    assert all(word.part_of_speech == PartOfSpeech.NOUN for word in nouns)


def test_filter_by_gender_masculine():
    """Test filtering by masculine gender."""
    vocab = load_vocabulary()
    masculine = filter_by_gender(Gender.MASCULINE, vocab)
    assert len(masculine) > 0
    assert all(word.gender == Gender.MASCULINE for word in masculine)
    assert all(word.part_of_speech == PartOfSpeech.NOUN for word in masculine)


def test_filter_by_gender_feminine():
    """Test filtering by feminine gender."""
    vocab = load_vocabulary()
    feminine = filter_by_gender(Gender.FEMININE, vocab)
    assert len(feminine) > 0
    assert all(word.gender == Gender.FEMININE for word in feminine)


def test_filter_by_gender_neuter():
    """Test filtering by neuter gender."""
    vocab = load_vocabulary()
    neuter = filter_by_gender(Gender.NEUTER, vocab)
    assert len(neuter) > 0
    assert all(word.gender == Gender.NEUTER for word in neuter)


def test_filter_by_gender_string():
    """Test filtering by gender using string."""
    vocab = load_vocabulary()
    masculine = filter_by_gender("masculine", vocab)
    assert len(masculine) > 0
    assert all(word.gender == Gender.MASCULINE for word in masculine)


def test_filter_operations_combined():
    """Test combining filter operations."""
    vocab = load_vocabulary()
    nouns = filter_by_pos(PartOfSpeech.NOUN, vocab)
    masculine_nouns = filter_by_gender(Gender.MASCULINE, nouns)
    assert len(masculine_nouns) > 0
    assert all(word.part_of_speech == PartOfSpeech.NOUN for word in masculine_nouns)
    assert all(word.gender == Gender.MASCULINE for word in masculine_nouns)
