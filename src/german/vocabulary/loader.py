"""Load vocabulary data from JSON files."""

import json
from pathlib import Path
from typing import List

from ..models import VocabularyWord


class VocabularyLoadError(Exception):
    """Exception raised when vocabulary loading fails."""

    pass


def load_vocabulary(category: str | None = None) -> List[VocabularyWord]:
    """
    Load vocabulary from JSON files.

    Args:
        category: Optional category to load ("nouns", "verbs", "adjectives").
                 If None, loads all categories.

    Returns:
        List of VocabularyWord objects

    Raises:
        VocabularyLoadError: If files cannot be loaded or validated
    """
    # Find resources directory
    # When installed: resources/ is at package root
    # When developing: resources/ is at repo root
    package_dir = Path(__file__).parent.parent.parent.parent
    resources_dir = package_dir / "resources" / "vocabulary"

    if not resources_dir.exists():
        raise VocabularyLoadError(f"Vocabulary directory not found: {resources_dir}")

    words: List[VocabularyWord] = []

    # Determine which files to load
    if category:
        files = [resources_dir / f"{category}.json"]
    else:
        files = list(resources_dir.glob("*.json"))

    if not files:
        raise VocabularyLoadError(f"No vocabulary files found in {resources_dir}")

    for vocab_file in files:
        if not vocab_file.exists():
            raise VocabularyLoadError(f"Vocabulary file not found: {vocab_file}")

        try:
            with open(vocab_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "words" not in data:
                raise VocabularyLoadError(
                    f"Invalid format in {vocab_file.name}: missing 'words' key"
                )

            for word_data in data["words"]:
                try:
                    word = VocabularyWord(**word_data)
                    words.append(word)
                except Exception as e:
                    german = word_data.get('german', 'unknown')
                    raise VocabularyLoadError(
                        f"Invalid word data in {vocab_file.name}: {german}: {e}"
                    )

        except json.JSONDecodeError as e:
            raise VocabularyLoadError(f"Invalid JSON in {vocab_file.name}: {e}")
        except UnicodeDecodeError as e:
            raise VocabularyLoadError(f"Encoding error in {vocab_file.name}: {e}. Must be UTF-8.")

    return words
