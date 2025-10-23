"""German language learning resources and tools."""

__version__ = "0.1.0"

from .models import Gender, PartOfSpeech, VocabularyWord
from .vocabulary import (
    VocabularyLoadError,
    filter_by_gender,
    filter_by_pos,
    get_word,
    load_vocabulary,
)

__all__ = [
    "__version__",
    "VocabularyWord",
    "PartOfSpeech",
    "Gender",
    "load_vocabulary",
    "VocabularyLoadError",
    "get_word",
    "filter_by_pos",
    "filter_by_gender",
]
