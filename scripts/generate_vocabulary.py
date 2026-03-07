#!/usr/bin/env python3
"""Generate expanded vocabulary JSON files with CEFR level tagging.

This script contains comprehensive German vocabulary data organized by CEFR level
and part of speech. It validates all entries through Pydantic models before writing
the JSON files to resources/vocabulary/.

Usage:
    uv run python scripts/generate_vocabulary.py            # Generate JSON files
    uv run python scripts/generate_vocabulary.py --dry-run  # Validate only
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from german.models import VocabularyWord  # noqa: E402


def generate_nouns() -> list[dict]:
    """Generate noun vocabulary data across all CEFR levels."""
    return [
        *_nouns_a1(),
        *_nouns_a2(),
        *_nouns_b1(),
        *_nouns_b2(),
        *_nouns_c1(),
        *_nouns_c2(),
    ]


def generate_verbs() -> list[dict]:
    """Generate verb vocabulary data across all CEFR levels."""
    return [
        *_verbs_a1(),
        *_verbs_a2(),
        *_verbs_b1(),
        *_verbs_b2(),
        *_verbs_c1(),
        *_verbs_c2(),
    ]


def generate_adjectives() -> list[dict]:
    """Generate adjective vocabulary data across all CEFR levels."""
    return [
        *_adjectives_a1(),
        *_adjectives_a2(),
        *_adjectives_b1(),
        *_adjectives_b2(),
        *_adjectives_c1(),
        *_adjectives_c2(),
    ]


def validate_and_write(words: list[dict], filepath: Path, dry_run: bool = False) -> bool:
    """Validate vocabulary entries and write to JSON file.

    Args:
        words: List of word dictionaries to validate and write.
        filepath: Output path for the JSON file.
        dry_run: If True, validate only without writing.

    Returns:
        True if validation passed, False otherwise.
    """
    errors = []
    seen = set()
    validated = []

    for i, entry in enumerate(words):
        german = entry.get("german", f"entry-{i}")

        # Check duplicates
        key = entry.get("german", "").lower()
        if key in seen:
            errors.append(f"  Duplicate: {german}")
            continue
        seen.add(key)

        # Validate through Pydantic
        try:
            word = VocabularyWord(**entry)
            validated.append(entry)
        except Exception as e:
            errors.append(f"  Invalid '{german}': {e}")

    if errors:
        print(f"\nErrors in {filepath.name}:")
        for err in errors:
            print(err)
        return False

    # Print summary
    level_counts = Counter(w.get("level", "?") for w in validated)
    print(f"\n{filepath.name}: {len(validated)} words")
    for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        print(f"  {level}: {level_counts.get(level, 0)}")

    if not dry_run:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump({"words": validated}, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"  Written to {filepath}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate vocabulary JSON files")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, don't write files")
    args = parser.parse_args()

    resources_dir = Path(__file__).parent.parent / "resources" / "vocabulary"

    generators = {
        "nouns.json": generate_nouns,
        "verbs.json": generate_verbs,
        "adjectives.json": generate_adjectives,
    }

    all_ok = True
    total = 0
    for filename, generator in generators.items():
        words = generator()
        total += len(words)
        ok = validate_and_write(words, resources_dir / filename, dry_run=args.dry_run)
        if not ok:
            all_ok = False

    print(f"\nTotal: {total} words")

    if not all_ok:
        print("\nValidation FAILED — see errors above")
        sys.exit(1)
    elif args.dry_run:
        print("\nDry run: validation PASSED")
    else:
        print("\nGeneration complete")


# ---------------------------------------------------------------------------
# Vocabulary data by level and part of speech
# ---------------------------------------------------------------------------

def _nouns_a1() -> list[dict]:
    return [
        {"german": "Haus", "english": "house", "part_of_speech": "noun", "gender": "neuter", "plural": "Häuser", "level": "A1"},
        {"german": "Buch", "english": "book", "part_of_speech": "noun", "gender": "neuter", "plural": "Bücher", "level": "A1"},
        {"german": "Tisch", "english": "table", "part_of_speech": "noun", "gender": "masculine", "plural": "Tische", "level": "A1"},
        {"german": "Stuhl", "english": "chair", "part_of_speech": "noun", "gender": "masculine", "plural": "Stühle", "level": "A1"},
        {"german": "Tür", "english": "door", "part_of_speech": "noun", "gender": "feminine", "plural": "Türen", "level": "A1"},
        {"german": "Fenster", "english": "window", "part_of_speech": "noun", "gender": "neuter", "plural": "Fenster", "level": "A1"},
        {"german": "Stadt", "english": "city", "part_of_speech": "noun", "gender": "feminine", "plural": "Städte", "level": "A1"},
        {"german": "Land", "english": "country", "part_of_speech": "noun", "gender": "neuter", "plural": "Länder", "level": "A1"},
        {"german": "Mensch", "english": "person/human", "part_of_speech": "noun", "gender": "masculine", "plural": "Menschen", "level": "A1"},
        {"german": "Frau", "english": "woman", "part_of_speech": "noun", "gender": "feminine", "plural": "Frauen", "level": "A1"},
        {"german": "Mann", "english": "man", "part_of_speech": "noun", "gender": "masculine", "plural": "Männer", "level": "A1"},
        {"german": "Kind", "english": "child", "part_of_speech": "noun", "gender": "neuter", "plural": "Kinder", "level": "A1"},
        {"german": "Tag", "english": "day", "part_of_speech": "noun", "gender": "masculine", "plural": "Tage", "level": "A1"},
        {"german": "Nacht", "english": "night", "part_of_speech": "noun", "gender": "feminine", "plural": "Nächte", "level": "A1"},
        {"german": "Zeit", "english": "time", "part_of_speech": "noun", "gender": "feminine", "plural": "Zeiten", "level": "A1"},
        {"german": "Jahr", "english": "year", "part_of_speech": "noun", "gender": "neuter", "plural": "Jahre", "level": "A1"},
        {"german": "Wasser", "english": "water", "part_of_speech": "noun", "gender": "neuter", "plural": "Wasser", "level": "A1"},
        {"german": "Brot", "english": "bread", "part_of_speech": "noun", "gender": "neuter", "plural": "Brote", "level": "A1"},
        {"german": "Apfel", "english": "apple", "part_of_speech": "noun", "gender": "masculine", "plural": "Äpfel", "level": "A1"},
        {"german": "Baum", "english": "tree", "part_of_speech": "noun", "gender": "masculine", "plural": "Bäume", "level": "A1"},
    ]


def _nouns_a2() -> list[dict]:
    return []


def _nouns_b1() -> list[dict]:
    return []


def _nouns_b2() -> list[dict]:
    return []


def _nouns_c1() -> list[dict]:
    return []


def _nouns_c2() -> list[dict]:
    return []


def _verbs_a1() -> list[dict]:
    return [
        {"german": "sein", "english": "to be", "part_of_speech": "verb", "level": "A1"},
        {"german": "haben", "english": "to have", "part_of_speech": "verb", "level": "A1"},
        {"german": "werden", "english": "to become", "part_of_speech": "verb", "level": "A1"},
        {"german": "können", "english": "to be able to / can", "part_of_speech": "verb", "level": "A1"},
        {"german": "müssen", "english": "to have to / must", "part_of_speech": "verb", "level": "A1"},
        {"german": "sagen", "english": "to say", "part_of_speech": "verb", "level": "A1"},
        {"german": "machen", "english": "to make / to do", "part_of_speech": "verb", "level": "A1"},
        {"german": "geben", "english": "to give", "part_of_speech": "verb", "level": "A1"},
        {"german": "kommen", "english": "to come", "part_of_speech": "verb", "level": "A1"},
        {"german": "sollen", "english": "should / ought to", "part_of_speech": "verb", "level": "A1"},
        {"german": "wollen", "english": "to want", "part_of_speech": "verb", "level": "A1"},
        {"german": "gehen", "english": "to go", "part_of_speech": "verb", "level": "A1"},
        {"german": "wissen", "english": "to know (facts)", "part_of_speech": "verb", "level": "A1"},
        {"german": "sehen", "english": "to see", "part_of_speech": "verb", "level": "A1"},
        {"german": "lassen", "english": "to let / to leave", "part_of_speech": "verb", "level": "A1"},
        {"german": "stehen", "english": "to stand", "part_of_speech": "verb", "level": "A1"},
        {"german": "finden", "english": "to find", "part_of_speech": "verb", "level": "A1"},
        {"german": "bleiben", "english": "to stay / to remain", "part_of_speech": "verb", "level": "A1"},
        {"german": "liegen", "english": "to lie / to be located", "part_of_speech": "verb", "level": "A1"},
        {"german": "heißen", "english": "to be called / to mean", "part_of_speech": "verb", "level": "A1"},
        {"german": "denken", "english": "to think", "part_of_speech": "verb", "level": "A1"},
        {"german": "nehmen", "english": "to take", "part_of_speech": "verb", "level": "A1"},
        {"german": "tun", "english": "to do", "part_of_speech": "verb", "level": "A1"},
        {"german": "dürfen", "english": "to be allowed to / may", "part_of_speech": "verb", "level": "A1"},
        {"german": "glauben", "english": "to believe", "part_of_speech": "verb", "level": "A1"},
        {"german": "halten", "english": "to hold / to stop", "part_of_speech": "verb", "level": "A1"},
        {"german": "nennen", "english": "to name / to call", "part_of_speech": "verb", "level": "A1"},
        {"german": "mögen", "english": "to like", "part_of_speech": "verb", "level": "A1"},
        {"german": "zeigen", "english": "to show", "part_of_speech": "verb", "level": "A1"},
        {"german": "führen", "english": "to lead", "part_of_speech": "verb", "level": "A1"},
    ]


def _verbs_a2() -> list[dict]:
    return []


def _verbs_b1() -> list[dict]:
    return []


def _verbs_b2() -> list[dict]:
    return []


def _verbs_c1() -> list[dict]:
    return []


def _verbs_c2() -> list[dict]:
    return []


def _adjectives_a1() -> list[dict]:
    return [
        {"german": "groß", "english": "big / large / tall", "part_of_speech": "adjective", "level": "A1"},
        {"german": "klein", "english": "small / little", "part_of_speech": "adjective", "level": "A1"},
        {"german": "gut", "english": "good", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schlecht", "english": "bad", "part_of_speech": "adjective", "level": "A1"},
        {"german": "neu", "english": "new", "part_of_speech": "adjective", "level": "A1"},
        {"german": "alt", "english": "old", "part_of_speech": "adjective", "level": "A1"},
        {"german": "jung", "english": "young", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schön", "english": "beautiful / nice", "part_of_speech": "adjective", "level": "A1"},
        {"german": "lang", "english": "long", "part_of_speech": "adjective", "level": "A1"},
        {"german": "kurz", "english": "short", "part_of_speech": "adjective", "level": "A1"},
        {"german": "hoch", "english": "high / tall", "part_of_speech": "adjective", "level": "A1"},
        {"german": "tief", "english": "deep / low", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schnell", "english": "fast / quick", "part_of_speech": "adjective", "level": "A1"},
        {"german": "langsam", "english": "slow", "part_of_speech": "adjective", "level": "A1"},
        {"german": "wichtig", "english": "important", "part_of_speech": "adjective", "level": "A1"},
        {"german": "richtig", "english": "correct / right", "part_of_speech": "adjective", "level": "A1"},
        {"german": "falsch", "english": "wrong / false", "part_of_speech": "adjective", "level": "A1"},
        {"german": "leicht", "english": "easy / light", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schwer", "english": "heavy / difficult", "part_of_speech": "adjective", "level": "A1"},
        {"german": "hell", "english": "bright / light", "part_of_speech": "adjective", "level": "A1"},
    ]


def _adjectives_a2() -> list[dict]:
    return []


def _adjectives_b1() -> list[dict]:
    return []


def _adjectives_b2() -> list[dict]:
    return []


def _adjectives_c1() -> list[dict]:
    return []


def _adjectives_c2() -> list[dict]:
    return []


if __name__ == "__main__":
    main()
