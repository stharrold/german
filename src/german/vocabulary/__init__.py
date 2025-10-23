"""Vocabulary module for German language learning."""

from .loader import VocabularyLoadError, load_vocabulary
from .query import filter_by_gender, filter_by_pos, get_word

__all__ = [
    "load_vocabulary",
    "VocabularyLoadError",
    "get_word",
    "filter_by_pos",
    "filter_by_gender",
]
