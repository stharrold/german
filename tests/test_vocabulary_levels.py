"""Tests for CEFR level distribution in vocabulary data."""

from german.models import CEFRLevel, PartOfSpeech
from german.vocabulary import load_vocabulary


def test_all_levels_present():
    """Test that vocabulary contains words at every CEFR level."""
    vocab = load_vocabulary()
    levels = {word.level for word in vocab}
    for level in CEFRLevel:
        assert level in levels, f"Missing CEFR level: {level}"


def test_all_words_have_level():
    """Test that every word has a CEFR level assigned."""
    vocab = load_vocabulary()
    for word in vocab:
        assert word.level is not None, f"Word '{word.german}' missing CEFR level"


def test_no_duplicate_words():
    """Test that there are no duplicate German words within same POS."""
    vocab = load_vocabulary()
    seen = set()
    for word in vocab:
        key = (word.german.lower(), word.part_of_speech)
        assert key not in seen, f"Duplicate: {word.german} ({word.part_of_speech})"
        seen.add(key)


def test_noun_count_minimum():
    """Test minimum noun count across levels."""
    nouns = load_vocabulary(category="nouns")
    assert len(nouns) >= 200, f"Expected >= 200 nouns, got {len(nouns)}"


def test_verb_count_minimum():
    """Test minimum verb count across levels."""
    verbs = load_vocabulary(category="verbs")
    assert len(verbs) >= 100, f"Expected >= 100 verbs, got {len(verbs)}"


def test_adjective_count_minimum():
    """Test minimum adjective count across levels."""
    adjectives = load_vocabulary(category="adjectives")
    assert len(adjectives) >= 80, f"Expected >= 80 adjectives, got {len(adjectives)}"


def test_level_distribution_nouns():
    """Test that nouns are distributed across levels."""
    nouns = load_vocabulary(category="nouns")
    for level in CEFRLevel:
        level_nouns = [n for n in nouns if n.level == level]
        assert len(level_nouns) >= 10, f"Nouns at {level}: {len(level_nouns)} (need >= 10)"


def test_level_distribution_verbs():
    """Test that verbs are distributed across levels."""
    verbs = load_vocabulary(category="verbs")
    for level in CEFRLevel:
        level_verbs = [v for v in verbs if v.level == level]
        assert len(level_verbs) >= 10, f"Verbs at {level}: {len(level_verbs)} (need >= 10)"


def test_level_distribution_adjectives():
    """Test that adjectives are distributed across levels."""
    adjectives = load_vocabulary(category="adjectives")
    for level in CEFRLevel:
        level_adjs = [a for a in adjectives if a.level == level]
        assert len(level_adjs) >= 10, f"Adjectives at {level}: {len(level_adjs)} (need >= 10)"


def test_total_vocabulary_minimum():
    """Test total vocabulary meets minimum threshold."""
    vocab = load_vocabulary()
    assert len(vocab) >= 500, f"Expected >= 500 total words, got {len(vocab)}"
