"""Query functions for vocabulary data."""

from typing import List, Optional

from ..models import Gender, PartOfSpeech, VocabularyWord


def get_word(german_word: str, vocabulary: List[VocabularyWord]) -> Optional[VocabularyWord]:
    """
    Get a vocabulary word by its German term.

    Args:
        german_word: German word to find
        vocabulary: List of vocabulary words to search

    Returns:
        VocabularyWord if found, None otherwise
    """
    for word in vocabulary:
        if word.german.lower() == german_word.lower():
            return word
    return None


def filter_by_pos(
    part_of_speech: str | PartOfSpeech, vocabulary: List[VocabularyWord]
) -> List[VocabularyWord]:
    """
    Filter vocabulary by part of speech.

    Args:
        part_of_speech: Part of speech to filter by
        vocabulary: List of vocabulary words to filter

    Returns:
        List of matching words
    """
    if isinstance(part_of_speech, str):
        part_of_speech = PartOfSpeech(part_of_speech)

    return [word for word in vocabulary if word.part_of_speech == part_of_speech]


def filter_by_gender(
    gender: str | Gender, vocabulary: List[VocabularyWord]
) -> List[VocabularyWord]:
    """
    Filter nouns by grammatical gender.

    Args:
        gender: Gender to filter by (masculine, feminine, neuter)
        vocabulary: List of vocabulary words to filter

    Returns:
        List of nouns with the specified gender
    """
    if isinstance(gender, str):
        gender = Gender(gender)

    return [
        word
        for word in vocabulary
        if word.part_of_speech == PartOfSpeech.NOUN and word.gender == gender
    ]
