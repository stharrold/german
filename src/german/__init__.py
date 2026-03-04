"""German language learning resources and tools."""

from importlib.metadata import version

__version__ = version("german")

from .models import CEFRLevel, Gender, PartOfSpeech, VocabularyWord
from .vocabulary import (
    VocabularyLoadError,
    filter_by_gender,
    filter_by_level,
    filter_by_pos,
    get_word,
    load_vocabulary,
)

__all__ = [
    "__version__",
    "VocabularyWord",
    "PartOfSpeech",
    "Gender",
    "CEFRLevel",
    "load_vocabulary",
    "VocabularyLoadError",
    "get_word",
    "filter_by_pos",
    "filter_by_gender",
    "filter_by_level",
]
