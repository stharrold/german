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
            VocabularyWord(**entry)
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
# NOUNS
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
        # Family
        {"german": "Mutter", "english": "mother", "part_of_speech": "noun", "gender": "feminine", "plural": "Mütter", "level": "A1"},
        {"german": "Vater", "english": "father", "part_of_speech": "noun", "gender": "masculine", "plural": "Väter", "level": "A1"},
        {"german": "Bruder", "english": "brother", "part_of_speech": "noun", "gender": "masculine", "plural": "Brüder", "level": "A1"},
        {"german": "Schwester", "english": "sister", "part_of_speech": "noun", "gender": "feminine", "plural": "Schwestern", "level": "A1"},
        {"german": "Sohn", "english": "son", "part_of_speech": "noun", "gender": "masculine", "plural": "Söhne", "level": "A1"},
        {"german": "Tochter", "english": "daughter", "part_of_speech": "noun", "gender": "feminine", "plural": "Töchter", "level": "A1"},
        {"german": "Familie", "english": "family", "part_of_speech": "noun", "gender": "feminine", "plural": "Familien", "level": "A1"},
        {"german": "Baby", "english": "baby", "part_of_speech": "noun", "gender": "neuter", "plural": "Babys", "level": "A1"},
        {"german": "Freund", "english": "friend", "part_of_speech": "noun", "gender": "masculine", "plural": "Freunde", "level": "A1"},
        {"german": "Freundin", "english": "female friend", "part_of_speech": "noun", "gender": "feminine", "plural": "Freundinnen", "level": "A1"},
        # Body
        {"german": "Kopf", "english": "head", "part_of_speech": "noun", "gender": "masculine", "plural": "Köpfe", "level": "A1"},
        {"german": "Hand", "english": "hand", "part_of_speech": "noun", "gender": "feminine", "plural": "Hände", "level": "A1"},
        {"german": "Auge", "english": "eye", "part_of_speech": "noun", "gender": "neuter", "plural": "Augen", "level": "A1"},
        {"german": "Nase", "english": "nose", "part_of_speech": "noun", "gender": "feminine", "plural": "Nasen", "level": "A1"},
        {"german": "Mund", "english": "mouth", "part_of_speech": "noun", "gender": "masculine", "plural": "Münder", "level": "A1"},
        {"german": "Ohr", "english": "ear", "part_of_speech": "noun", "gender": "neuter", "plural": "Ohren", "level": "A1"},
        {"german": "Fuß", "english": "foot", "part_of_speech": "noun", "gender": "masculine", "plural": "Füße", "level": "A1"},
        {"german": "Arm", "english": "arm", "part_of_speech": "noun", "gender": "masculine", "plural": "Arme", "level": "A1"},
        {"german": "Bein", "english": "leg", "part_of_speech": "noun", "gender": "neuter", "plural": "Beine", "level": "A1"},
        {"german": "Haar", "english": "hair", "part_of_speech": "noun", "gender": "neuter", "plural": "Haare", "level": "A1"},
        # Food & Drink
        {"german": "Milch", "english": "milk", "part_of_speech": "noun", "gender": "feminine", "plural": "Milch", "level": "A1"},
        {"german": "Kaffee", "english": "coffee", "part_of_speech": "noun", "gender": "masculine", "plural": "Kaffees", "level": "A1"},
        {"german": "Tee", "english": "tea", "part_of_speech": "noun", "gender": "masculine", "plural": "Tees", "level": "A1"},
        {"german": "Ei", "english": "egg", "part_of_speech": "noun", "gender": "neuter", "plural": "Eier", "level": "A1"},
        {"german": "Fleisch", "english": "meat", "part_of_speech": "noun", "gender": "neuter", "plural": "Fleisch", "level": "A1"},
        {"german": "Fisch", "english": "fish", "part_of_speech": "noun", "gender": "masculine", "plural": "Fische", "level": "A1"},
        {"german": "Käse", "english": "cheese", "part_of_speech": "noun", "gender": "masculine", "plural": "Käse", "level": "A1"},
        {"german": "Butter", "english": "butter", "part_of_speech": "noun", "gender": "feminine", "plural": "Butter", "level": "A1"},
        {"german": "Reis", "english": "rice", "part_of_speech": "noun", "gender": "masculine", "plural": "Reis", "level": "A1"},
        {"german": "Kuchen", "english": "cake", "part_of_speech": "noun", "gender": "masculine", "plural": "Kuchen", "level": "A1"},
        {"german": "Suppe", "english": "soup", "part_of_speech": "noun", "gender": "feminine", "plural": "Suppen", "level": "A1"},
        {"german": "Saft", "english": "juice", "part_of_speech": "noun", "gender": "masculine", "plural": "Säfte", "level": "A1"},
        {"german": "Obst", "english": "fruit", "part_of_speech": "noun", "gender": "neuter", "plural": "Obst", "level": "A1"},
        {"german": "Gemüse", "english": "vegetables", "part_of_speech": "noun", "gender": "neuter", "plural": "Gemüse", "level": "A1"},
        # Home
        {"german": "Küche", "english": "kitchen", "part_of_speech": "noun", "gender": "feminine", "plural": "Küchen", "level": "A1"},
        {"german": "Zimmer", "english": "room", "part_of_speech": "noun", "gender": "neuter", "plural": "Zimmer", "level": "A1"},
        {"german": "Bett", "english": "bed", "part_of_speech": "noun", "gender": "neuter", "plural": "Betten", "level": "A1"},
        {"german": "Bad", "english": "bathroom", "part_of_speech": "noun", "gender": "neuter", "plural": "Bäder", "level": "A1"},
        {"german": "Wohnung", "english": "apartment", "part_of_speech": "noun", "gender": "feminine", "plural": "Wohnungen", "level": "A1"},
        {"german": "Garten", "english": "garden", "part_of_speech": "noun", "gender": "masculine", "plural": "Gärten", "level": "A1"},
        {"german": "Lampe", "english": "lamp", "part_of_speech": "noun", "gender": "feminine", "plural": "Lampen", "level": "A1"},
        {"german": "Uhr", "english": "clock", "part_of_speech": "noun", "gender": "feminine", "plural": "Uhren", "level": "A1"},
        {"german": "Schlüssel", "english": "key", "part_of_speech": "noun", "gender": "masculine", "plural": "Schlüssel", "level": "A1"},
        # Clothing
        {"german": "Schuh", "english": "shoe", "part_of_speech": "noun", "gender": "masculine", "plural": "Schuhe", "level": "A1"},
        {"german": "Hose", "english": "trousers", "part_of_speech": "noun", "gender": "feminine", "plural": "Hosen", "level": "A1"},
        {"german": "Hemd", "english": "shirt", "part_of_speech": "noun", "gender": "neuter", "plural": "Hemden", "level": "A1"},
        {"german": "Kleid", "english": "dress", "part_of_speech": "noun", "gender": "neuter", "plural": "Kleider", "level": "A1"},
        {"german": "Jacke", "english": "jacket", "part_of_speech": "noun", "gender": "feminine", "plural": "Jacken", "level": "A1"},
        {"german": "Mantel", "english": "coat", "part_of_speech": "noun", "gender": "masculine", "plural": "Mäntel", "level": "A1"},
        {"german": "Hut", "english": "hat", "part_of_speech": "noun", "gender": "masculine", "plural": "Hüte", "level": "A1"},
        # School
        {"german": "Schule", "english": "school", "part_of_speech": "noun", "gender": "feminine", "plural": "Schulen", "level": "A1"},
        {"german": "Lehrer", "english": "teacher", "part_of_speech": "noun", "gender": "masculine", "plural": "Lehrer", "level": "A1"},
        {"german": "Lehrerin", "english": "female teacher", "part_of_speech": "noun", "gender": "feminine", "plural": "Lehrerinnen", "level": "A1"},
        {"german": "Stift", "english": "pen", "part_of_speech": "noun", "gender": "masculine", "plural": "Stifte", "level": "A1"},
        {"german": "Heft", "english": "notebook", "part_of_speech": "noun", "gender": "neuter", "plural": "Hefte", "level": "A1"},
        {"german": "Tasche", "english": "bag", "part_of_speech": "noun", "gender": "feminine", "plural": "Taschen", "level": "A1"},
        {"german": "Sprache", "english": "language", "part_of_speech": "noun", "gender": "feminine", "plural": "Sprachen", "level": "A1"},
        {"german": "Wort", "english": "word", "part_of_speech": "noun", "gender": "neuter", "plural": "Wörter", "level": "A1"},
        # Transport & Places
        {"german": "Auto", "english": "car", "part_of_speech": "noun", "gender": "neuter", "plural": "Autos", "level": "A1"},
        {"german": "Bus", "english": "bus", "part_of_speech": "noun", "gender": "masculine", "plural": "Busse", "level": "A1"},
        {"german": "Zug", "english": "train", "part_of_speech": "noun", "gender": "masculine", "plural": "Züge", "level": "A1"},
        {"german": "Straße", "english": "street", "part_of_speech": "noun", "gender": "feminine", "plural": "Straßen", "level": "A1"},
        {"german": "Platz", "english": "place/square", "part_of_speech": "noun", "gender": "masculine", "plural": "Plätze", "level": "A1"},
        {"german": "Bahnhof", "english": "train station", "part_of_speech": "noun", "gender": "masculine", "plural": "Bahnhöfe", "level": "A1"},
        {"german": "Supermarkt", "english": "supermarket", "part_of_speech": "noun", "gender": "masculine", "plural": "Supermärkte", "level": "A1"},
        {"german": "Arzt", "english": "doctor", "part_of_speech": "noun", "gender": "masculine", "plural": "Ärzte", "level": "A1"},
        {"german": "Krankenhaus", "english": "hospital", "part_of_speech": "noun", "gender": "neuter", "plural": "Krankenhäuser", "level": "A1"},
        # Nature & Animals
        {"german": "Hund", "english": "dog", "part_of_speech": "noun", "gender": "masculine", "plural": "Hunde", "level": "A1"},
        {"german": "Katze", "english": "cat", "part_of_speech": "noun", "gender": "feminine", "plural": "Katzen", "level": "A1"},
        {"german": "Vogel", "english": "bird", "part_of_speech": "noun", "gender": "masculine", "plural": "Vögel", "level": "A1"},
        {"german": "Blume", "english": "flower", "part_of_speech": "noun", "gender": "feminine", "plural": "Blumen", "level": "A1"},
        {"german": "Sonne", "english": "sun", "part_of_speech": "noun", "gender": "feminine", "plural": "Sonnen", "level": "A1"},
        {"german": "Mond", "english": "moon", "part_of_speech": "noun", "gender": "masculine", "plural": "Monde", "level": "A1"},
        {"german": "Regen", "english": "rain", "part_of_speech": "noun", "gender": "masculine", "plural": "Regen", "level": "A1"},
        {"german": "Schnee", "english": "snow", "part_of_speech": "noun", "gender": "masculine", "plural": "Schnee", "level": "A1"},
        {"german": "Berg", "english": "mountain", "part_of_speech": "noun", "gender": "masculine", "plural": "Berge", "level": "A1"},
        {"german": "Meer", "english": "sea", "part_of_speech": "noun", "gender": "neuter", "plural": "Meere", "level": "A1"},
        {"german": "Tier", "english": "animal", "part_of_speech": "noun", "gender": "neuter", "plural": "Tiere", "level": "A1"},
        # Time
        {"german": "Woche", "english": "week", "part_of_speech": "noun", "gender": "feminine", "plural": "Wochen", "level": "A1"},
        {"german": "Monat", "english": "month", "part_of_speech": "noun", "gender": "masculine", "plural": "Monate", "level": "A1"},
        {"german": "Stunde", "english": "hour", "part_of_speech": "noun", "gender": "feminine", "plural": "Stunden", "level": "A1"},
        {"german": "Minute", "english": "minute", "part_of_speech": "noun", "gender": "feminine", "plural": "Minuten", "level": "A1"},
        {"german": "Morgen", "english": "morning", "part_of_speech": "noun", "gender": "masculine", "plural": "Morgen", "level": "A1"},
        {"german": "Abend", "english": "evening", "part_of_speech": "noun", "gender": "masculine", "plural": "Abende", "level": "A1"},
        # Everyday Objects & Concepts
        {"german": "Telefon", "english": "telephone", "part_of_speech": "noun", "gender": "neuter", "plural": "Telefone", "level": "A1"},
        {"german": "Geld", "english": "money", "part_of_speech": "noun", "gender": "neuter", "plural": "Gelder", "level": "A1"},
        {"german": "Name", "english": "name", "part_of_speech": "noun", "gender": "masculine", "plural": "Namen", "level": "A1"},
        {"german": "Nummer", "english": "number", "part_of_speech": "noun", "gender": "feminine", "plural": "Nummern", "level": "A1"},
        {"german": "Bild", "english": "picture", "part_of_speech": "noun", "gender": "neuter", "plural": "Bilder", "level": "A1"},
        {"german": "Brief", "english": "letter", "part_of_speech": "noun", "gender": "masculine", "plural": "Briefe", "level": "A1"},
        {"german": "Zeitung", "english": "newspaper", "part_of_speech": "noun", "gender": "feminine", "plural": "Zeitungen", "level": "A1"},
        {"german": "Musik", "english": "music", "part_of_speech": "noun", "gender": "feminine", "plural": "Musik", "level": "A1"},
        {"german": "Farbe", "english": "color", "part_of_speech": "noun", "gender": "feminine", "plural": "Farben", "level": "A1"},
        {"german": "Frage", "english": "question", "part_of_speech": "noun", "gender": "feminine", "plural": "Fragen", "level": "A1"},
        {"german": "Antwort", "english": "answer", "part_of_speech": "noun", "gender": "feminine", "plural": "Antworten", "level": "A1"},
        {"german": "Arbeit", "english": "work", "part_of_speech": "noun", "gender": "feminine", "plural": "Arbeiten", "level": "A1"},
        {"german": "Spiel", "english": "game", "part_of_speech": "noun", "gender": "neuter", "plural": "Spiele", "level": "A1"},
        {"german": "Essen", "english": "food/meal", "part_of_speech": "noun", "gender": "neuter", "plural": "Essen", "level": "A1"},
        {"german": "Mädchen", "english": "girl", "part_of_speech": "noun", "gender": "neuter", "plural": "Mädchen", "level": "A1"},
        {"german": "Junge", "english": "boy", "part_of_speech": "noun", "gender": "masculine", "plural": "Jungen", "level": "A1"},
        {"german": "Fest", "english": "party/celebration", "part_of_speech": "noun", "gender": "neuter", "plural": "Feste", "level": "A1"},
        {"german": "Geburtstag", "english": "birthday", "part_of_speech": "noun", "gender": "masculine", "plural": "Geburtstage", "level": "A1"},
        {"german": "Problem", "english": "problem", "part_of_speech": "noun", "gender": "neuter", "plural": "Probleme", "level": "A1"},
        {"german": "Beispiel", "english": "example", "part_of_speech": "noun", "gender": "neuter", "plural": "Beispiele", "level": "A1"},
    ]


def _nouns_a2() -> list[dict]:
    return [
        # Family & People
        {"german": "Großvater", "english": "grandfather", "part_of_speech": "noun", "gender": "masculine", "plural": "Großväter", "level": "A2"},
        {"german": "Großmutter", "english": "grandmother", "part_of_speech": "noun", "gender": "feminine", "plural": "Großmütter", "level": "A2"},
        {"german": "Onkel", "english": "uncle", "part_of_speech": "noun", "gender": "masculine", "plural": "Onkel", "level": "A2"},
        {"german": "Tante", "english": "aunt", "part_of_speech": "noun", "gender": "feminine", "plural": "Tanten", "level": "A2"},
        {"german": "Cousin", "english": "male cousin", "part_of_speech": "noun", "gender": "masculine", "plural": "Cousins", "level": "A2"},
        {"german": "Cousine", "english": "female cousin", "part_of_speech": "noun", "gender": "feminine", "plural": "Cousinen", "level": "A2"},
        {"german": "Nachbar", "english": "neighbor", "part_of_speech": "noun", "gender": "masculine", "plural": "Nachbarn", "level": "A2"},
        {"german": "Nachbarin", "english": "female neighbor", "part_of_speech": "noun", "gender": "feminine", "plural": "Nachbarinnen", "level": "A2"},
        {"german": "Kollege", "english": "colleague", "part_of_speech": "noun", "gender": "masculine", "plural": "Kollegen", "level": "A2"},
        {"german": "Kollegin", "english": "female colleague", "part_of_speech": "noun", "gender": "feminine", "plural": "Kolleginnen", "level": "A2"},
        {"german": "Chef", "english": "boss", "part_of_speech": "noun", "gender": "masculine", "plural": "Chefs", "level": "A2"},
        {"german": "Gast", "english": "guest", "part_of_speech": "noun", "gender": "masculine", "plural": "Gäste", "level": "A2"},
        # Body & Health
        {"german": "Finger", "english": "finger", "part_of_speech": "noun", "gender": "masculine", "plural": "Finger", "level": "A2"},
        {"german": "Rücken", "english": "back", "part_of_speech": "noun", "gender": "masculine", "plural": "Rücken", "level": "A2"},
        {"german": "Bauch", "english": "belly", "part_of_speech": "noun", "gender": "masculine", "plural": "Bäuche", "level": "A2"},
        {"german": "Hals", "english": "neck/throat", "part_of_speech": "noun", "gender": "masculine", "plural": "Hälse", "level": "A2"},
        {"german": "Zahn", "english": "tooth", "part_of_speech": "noun", "gender": "masculine", "plural": "Zähne", "level": "A2"},
        {"german": "Herz", "english": "heart", "part_of_speech": "noun", "gender": "neuter", "plural": "Herzen", "level": "A2"},
        {"german": "Schulter", "english": "shoulder", "part_of_speech": "noun", "gender": "feminine", "plural": "Schultern", "level": "A2"},
        {"german": "Knie", "english": "knee", "part_of_speech": "noun", "gender": "neuter", "plural": "Knie", "level": "A2"},
        {"german": "Gesundheit", "english": "health", "part_of_speech": "noun", "gender": "feminine", "plural": "Gesundheit", "level": "A2"},
        {"german": "Krankheit", "english": "illness", "part_of_speech": "noun", "gender": "feminine", "plural": "Krankheiten", "level": "A2"},
        {"german": "Schmerz", "english": "pain", "part_of_speech": "noun", "gender": "masculine", "plural": "Schmerzen", "level": "A2"},
        {"german": "Medikament", "english": "medication", "part_of_speech": "noun", "gender": "neuter", "plural": "Medikamente", "level": "A2"},
        {"german": "Apotheke", "english": "pharmacy", "part_of_speech": "noun", "gender": "feminine", "plural": "Apotheken", "level": "A2"},
        # Food & Drink
        {"german": "Kartoffel", "english": "potato", "part_of_speech": "noun", "gender": "feminine", "plural": "Kartoffeln", "level": "A2"},
        {"german": "Tomate", "english": "tomato", "part_of_speech": "noun", "gender": "feminine", "plural": "Tomaten", "level": "A2"},
        {"german": "Salat", "english": "salad/lettuce", "part_of_speech": "noun", "gender": "masculine", "plural": "Salate", "level": "A2"},
        {"german": "Nudel", "english": "noodle/pasta", "part_of_speech": "noun", "gender": "feminine", "plural": "Nudeln", "level": "A2"},
        {"german": "Hähnchen", "english": "chicken", "part_of_speech": "noun", "gender": "neuter", "plural": "Hähnchen", "level": "A2"},
        {"german": "Schokolade", "english": "chocolate", "part_of_speech": "noun", "gender": "feminine", "plural": "Schokoladen", "level": "A2"},
        {"german": "Zucker", "english": "sugar", "part_of_speech": "noun", "gender": "masculine", "plural": "Zucker", "level": "A2"},
        {"german": "Salz", "english": "salt", "part_of_speech": "noun", "gender": "neuter", "plural": "Salze", "level": "A2"},
        {"german": "Mehl", "english": "flour", "part_of_speech": "noun", "gender": "neuter", "plural": "Mehle", "level": "A2"},
        {"german": "Getränk", "english": "beverage", "part_of_speech": "noun", "gender": "neuter", "plural": "Getränke", "level": "A2"},
        {"german": "Wein", "english": "wine", "part_of_speech": "noun", "gender": "masculine", "plural": "Weine", "level": "A2"},
        {"german": "Bier", "english": "beer", "part_of_speech": "noun", "gender": "neuter", "plural": "Biere", "level": "A2"},
        {"german": "Gabel", "english": "fork", "part_of_speech": "noun", "gender": "feminine", "plural": "Gabeln", "level": "A2"},
        {"german": "Messer", "english": "knife", "part_of_speech": "noun", "gender": "neuter", "plural": "Messer", "level": "A2"},
        {"german": "Löffel", "english": "spoon", "part_of_speech": "noun", "gender": "masculine", "plural": "Löffel", "level": "A2"},
        {"german": "Teller", "english": "plate", "part_of_speech": "noun", "gender": "masculine", "plural": "Teller", "level": "A2"},
        {"german": "Tasse", "english": "cup", "part_of_speech": "noun", "gender": "feminine", "plural": "Tassen", "level": "A2"},
        {"german": "Glas", "english": "glass", "part_of_speech": "noun", "gender": "neuter", "plural": "Gläser", "level": "A2"},
        {"german": "Flasche", "english": "bottle", "part_of_speech": "noun", "gender": "feminine", "plural": "Flaschen", "level": "A2"},
        {"german": "Rezept", "english": "recipe/prescription", "part_of_speech": "noun", "gender": "neuter", "plural": "Rezepte", "level": "A2"},
        # Home & Furniture
        {"german": "Sofa", "english": "sofa", "part_of_speech": "noun", "gender": "neuter", "plural": "Sofas", "level": "A2"},
        {"german": "Schrank", "english": "cupboard/wardrobe", "part_of_speech": "noun", "gender": "masculine", "plural": "Schränke", "level": "A2"},
        {"german": "Regal", "english": "shelf", "part_of_speech": "noun", "gender": "neuter", "plural": "Regale", "level": "A2"},
        {"german": "Spiegel", "english": "mirror", "part_of_speech": "noun", "gender": "masculine", "plural": "Spiegel", "level": "A2"},
        {"german": "Teppich", "english": "carpet", "part_of_speech": "noun", "gender": "masculine", "plural": "Teppiche", "level": "A2"},
        {"german": "Treppe", "english": "stairs", "part_of_speech": "noun", "gender": "feminine", "plural": "Treppen", "level": "A2"},
        {"german": "Wand", "english": "wall", "part_of_speech": "noun", "gender": "feminine", "plural": "Wände", "level": "A2"},
        {"german": "Decke", "english": "ceiling/blanket", "part_of_speech": "noun", "gender": "feminine", "plural": "Decken", "level": "A2"},
        {"german": "Boden", "english": "floor/ground", "part_of_speech": "noun", "gender": "masculine", "plural": "Böden", "level": "A2"},
        {"german": "Herd", "english": "stove", "part_of_speech": "noun", "gender": "masculine", "plural": "Herde", "level": "A2"},
        {"german": "Kühlschrank", "english": "refrigerator", "part_of_speech": "noun", "gender": "masculine", "plural": "Kühlschränke", "level": "A2"},
        {"german": "Waschmaschine", "english": "washing machine", "part_of_speech": "noun", "gender": "feminine", "plural": "Waschmaschinen", "level": "A2"},
        {"german": "Dusche", "english": "shower", "part_of_speech": "noun", "gender": "feminine", "plural": "Duschen", "level": "A2"},
        {"german": "Balkon", "english": "balcony", "part_of_speech": "noun", "gender": "masculine", "plural": "Balkone", "level": "A2"},
        {"german": "Miete", "english": "rent", "part_of_speech": "noun", "gender": "feminine", "plural": "Mieten", "level": "A2"},
        # Clothing
        {"german": "Rock", "english": "skirt", "part_of_speech": "noun", "gender": "masculine", "plural": "Röcke", "level": "A2"},
        {"german": "Bluse", "english": "blouse", "part_of_speech": "noun", "gender": "feminine", "plural": "Blusen", "level": "A2"},
        {"german": "Anzug", "english": "suit", "part_of_speech": "noun", "gender": "masculine", "plural": "Anzüge", "level": "A2"},
        {"german": "Pullover", "english": "sweater", "part_of_speech": "noun", "gender": "masculine", "plural": "Pullover", "level": "A2"},
        {"german": "Handschuh", "english": "glove", "part_of_speech": "noun", "gender": "masculine", "plural": "Handschuhe", "level": "A2"},
        {"german": "Schal", "english": "scarf", "part_of_speech": "noun", "gender": "masculine", "plural": "Schals", "level": "A2"},
        {"german": "Stiefel", "english": "boot", "part_of_speech": "noun", "gender": "masculine", "plural": "Stiefel", "level": "A2"},
        {"german": "Socke", "english": "sock", "part_of_speech": "noun", "gender": "feminine", "plural": "Socken", "level": "A2"},
        {"german": "Größe", "english": "size", "part_of_speech": "noun", "gender": "feminine", "plural": "Größen", "level": "A2"},
        # Work & Education
        {"german": "Büro", "english": "office", "part_of_speech": "noun", "gender": "neuter", "plural": "Büros", "level": "A2"},
        {"german": "Beruf", "english": "profession", "part_of_speech": "noun", "gender": "masculine", "plural": "Berufe", "level": "A2"},
        {"german": "Firma", "english": "company", "part_of_speech": "noun", "gender": "feminine", "plural": "Firmen", "level": "A2"},
        {"german": "Termin", "english": "appointment", "part_of_speech": "noun", "gender": "masculine", "plural": "Termine", "level": "A2"},
        {"german": "Kurs", "english": "course", "part_of_speech": "noun", "gender": "masculine", "plural": "Kurse", "level": "A2"},
        {"german": "Prüfung", "english": "exam", "part_of_speech": "noun", "gender": "feminine", "plural": "Prüfungen", "level": "A2"},
        {"german": "Hausaufgabe", "english": "homework", "part_of_speech": "noun", "gender": "feminine", "plural": "Hausaufgaben", "level": "A2"},
        {"german": "Übung", "english": "exercise", "part_of_speech": "noun", "gender": "feminine", "plural": "Übungen", "level": "A2"},
        {"german": "Universität", "english": "university", "part_of_speech": "noun", "gender": "feminine", "plural": "Universitäten", "level": "A2"},
        {"german": "Zeugnis", "english": "certificate/report card", "part_of_speech": "noun", "gender": "neuter", "plural": "Zeugnisse", "level": "A2"},
        {"german": "Computer", "english": "computer", "part_of_speech": "noun", "gender": "masculine", "plural": "Computer", "level": "A2"},
        # Transport & Travel
        {"german": "Fahrrad", "english": "bicycle", "part_of_speech": "noun", "gender": "neuter", "plural": "Fahrräder", "level": "A2"},
        {"german": "Flugzeug", "english": "airplane", "part_of_speech": "noun", "gender": "neuter", "plural": "Flugzeuge", "level": "A2"},
        {"german": "Flughafen", "english": "airport", "part_of_speech": "noun", "gender": "masculine", "plural": "Flughäfen", "level": "A2"},
        {"german": "Haltestelle", "english": "bus/tram stop", "part_of_speech": "noun", "gender": "feminine", "plural": "Haltestellen", "level": "A2"},
        {"german": "Fahrkarte", "english": "ticket", "part_of_speech": "noun", "gender": "feminine", "plural": "Fahrkarten", "level": "A2"},
        {"german": "Reise", "english": "trip/journey", "part_of_speech": "noun", "gender": "feminine", "plural": "Reisen", "level": "A2"},
        {"german": "Koffer", "english": "suitcase", "part_of_speech": "noun", "gender": "masculine", "plural": "Koffer", "level": "A2"},
        {"german": "Hotel", "english": "hotel", "part_of_speech": "noun", "gender": "neuter", "plural": "Hotels", "level": "A2"},
        {"german": "Gepäck", "english": "luggage", "part_of_speech": "noun", "gender": "neuter", "plural": "Gepäck", "level": "A2"},
        {"german": "Brücke", "english": "bridge", "part_of_speech": "noun", "gender": "feminine", "plural": "Brücken", "level": "A2"},
        {"german": "Parkplatz", "english": "parking space", "part_of_speech": "noun", "gender": "masculine", "plural": "Parkplätze", "level": "A2"},
        # Places & City
        {"german": "Kirche", "english": "church", "part_of_speech": "noun", "gender": "feminine", "plural": "Kirchen", "level": "A2"},
        {"german": "Museum", "english": "museum", "part_of_speech": "noun", "gender": "neuter", "plural": "Museen", "level": "A2"},
        {"german": "Restaurant", "english": "restaurant", "part_of_speech": "noun", "gender": "neuter", "plural": "Restaurants", "level": "A2"},
        {"german": "Bank", "english": "bank", "part_of_speech": "noun", "gender": "feminine", "plural": "Banken", "level": "A2"},
        {"german": "Post", "english": "post office", "part_of_speech": "noun", "gender": "feminine", "plural": "Posten", "level": "A2"},
        {"german": "Bibliothek", "english": "library", "part_of_speech": "noun", "gender": "feminine", "plural": "Bibliotheken", "level": "A2"},
        {"german": "Markt", "english": "market", "part_of_speech": "noun", "gender": "masculine", "plural": "Märkte", "level": "A2"},
        {"german": "Geschäft", "english": "shop/business", "part_of_speech": "noun", "gender": "neuter", "plural": "Geschäfte", "level": "A2"},
        {"german": "Bäckerei", "english": "bakery", "part_of_speech": "noun", "gender": "feminine", "plural": "Bäckereien", "level": "A2"},
        {"german": "Polizei", "english": "police", "part_of_speech": "noun", "gender": "feminine", "plural": "Polizei", "level": "A2"},
        {"german": "Rathaus", "english": "town hall", "part_of_speech": "noun", "gender": "neuter", "plural": "Rathäuser", "level": "A2"},
        {"german": "Spielplatz", "english": "playground", "part_of_speech": "noun", "gender": "masculine", "plural": "Spielplätze", "level": "A2"},
        # Nature & Weather
        {"german": "Wald", "english": "forest", "part_of_speech": "noun", "gender": "masculine", "plural": "Wälder", "level": "A2"},
        {"german": "See", "english": "lake", "part_of_speech": "noun", "gender": "masculine", "plural": "Seen", "level": "A2"},
        {"german": "Fluss", "english": "river", "part_of_speech": "noun", "gender": "masculine", "plural": "Flüsse", "level": "A2"},
        {"german": "Strand", "english": "beach", "part_of_speech": "noun", "gender": "masculine", "plural": "Strände", "level": "A2"},
        {"german": "Insel", "english": "island", "part_of_speech": "noun", "gender": "feminine", "plural": "Inseln", "level": "A2"},
        {"german": "Wetter", "english": "weather", "part_of_speech": "noun", "gender": "neuter", "plural": "Wetter", "level": "A2"},
        {"german": "Wind", "english": "wind", "part_of_speech": "noun", "gender": "masculine", "plural": "Winde", "level": "A2"},
        {"german": "Wolke", "english": "cloud", "part_of_speech": "noun", "gender": "feminine", "plural": "Wolken", "level": "A2"},
        {"german": "Stern", "english": "star", "part_of_speech": "noun", "gender": "masculine", "plural": "Sterne", "level": "A2"},
        {"german": "Himmel", "english": "sky/heaven", "part_of_speech": "noun", "gender": "masculine", "plural": "Himmel", "level": "A2"},
        {"german": "Erde", "english": "earth/ground", "part_of_speech": "noun", "gender": "feminine", "plural": "Erden", "level": "A2"},
        {"german": "Luft", "english": "air", "part_of_speech": "noun", "gender": "feminine", "plural": "Lüfte", "level": "A2"},
        # Animals
        {"german": "Pferd", "english": "horse", "part_of_speech": "noun", "gender": "neuter", "plural": "Pferde", "level": "A2"},
        {"german": "Kuh", "english": "cow", "part_of_speech": "noun", "gender": "feminine", "plural": "Kühe", "level": "A2"},
        {"german": "Schwein", "english": "pig", "part_of_speech": "noun", "gender": "neuter", "plural": "Schweine", "level": "A2"},
        {"german": "Maus", "english": "mouse", "part_of_speech": "noun", "gender": "feminine", "plural": "Mäuse", "level": "A2"},
        {"german": "Schmetterling", "english": "butterfly", "part_of_speech": "noun", "gender": "masculine", "plural": "Schmetterlinge", "level": "A2"},
        {"german": "Bär", "english": "bear", "part_of_speech": "noun", "gender": "masculine", "plural": "Bären", "level": "A2"},
        # Abstract & Everyday
        {"german": "Erfahrung", "english": "experience", "part_of_speech": "noun", "gender": "feminine", "plural": "Erfahrungen", "level": "A2"},
        {"german": "Meinung", "english": "opinion", "part_of_speech": "noun", "gender": "feminine", "plural": "Meinungen", "level": "A2"},
        {"german": "Nachricht", "english": "message/news", "part_of_speech": "noun", "gender": "feminine", "plural": "Nachrichten", "level": "A2"},
        {"german": "Entschuldigung", "english": "apology/excuse", "part_of_speech": "noun", "gender": "feminine", "plural": "Entschuldigungen", "level": "A2"},
        {"german": "Einladung", "english": "invitation", "part_of_speech": "noun", "gender": "feminine", "plural": "Einladungen", "level": "A2"},
        {"german": "Geschenk", "english": "gift", "part_of_speech": "noun", "gender": "neuter", "plural": "Geschenke", "level": "A2"},
        {"german": "Glück", "english": "luck/happiness", "part_of_speech": "noun", "gender": "neuter", "plural": "Glück", "level": "A2"},
        {"german": "Angst", "english": "fear", "part_of_speech": "noun", "gender": "feminine", "plural": "Ängste", "level": "A2"},
        {"german": "Freude", "english": "joy", "part_of_speech": "noun", "gender": "feminine", "plural": "Freuden", "level": "A2"},
        {"german": "Urlaub", "english": "vacation", "part_of_speech": "noun", "gender": "masculine", "plural": "Urlaube", "level": "A2"},
        {"german": "Hobby", "english": "hobby", "part_of_speech": "noun", "gender": "neuter", "plural": "Hobbys", "level": "A2"},
        {"german": "Sport", "english": "sport", "part_of_speech": "noun", "gender": "masculine", "plural": "Sportarten", "level": "A2"},
        {"german": "Mannschaft", "english": "team", "part_of_speech": "noun", "gender": "feminine", "plural": "Mannschaften", "level": "A2"},
        {"german": "Regel", "english": "rule", "part_of_speech": "noun", "gender": "feminine", "plural": "Regeln", "level": "A2"},
        {"german": "Recht", "english": "right/law", "part_of_speech": "noun", "gender": "neuter", "plural": "Rechte", "level": "A2"},
        {"german": "Grund", "english": "reason/ground", "part_of_speech": "noun", "gender": "masculine", "plural": "Gründe", "level": "A2"},
        {"german": "Unterschied", "english": "difference", "part_of_speech": "noun", "gender": "masculine", "plural": "Unterschiede", "level": "A2"},
        {"german": "Anfang", "english": "beginning", "part_of_speech": "noun", "gender": "masculine", "plural": "Anfänge", "level": "A2"},
        {"german": "Ende", "english": "end", "part_of_speech": "noun", "gender": "neuter", "plural": "Enden", "level": "A2"},
        {"german": "Seite", "english": "page/side", "part_of_speech": "noun", "gender": "feminine", "plural": "Seiten", "level": "A2"},
        {"german": "Idee", "english": "idea", "part_of_speech": "noun", "gender": "feminine", "plural": "Ideen", "level": "A2"},
        {"german": "Möglichkeit", "english": "possibility", "part_of_speech": "noun", "gender": "feminine", "plural": "Möglichkeiten", "level": "A2"},
        {"german": "Sicherheit", "english": "safety/security", "part_of_speech": "noun", "gender": "feminine", "plural": "Sicherheiten", "level": "A2"},
        {"german": "Hilfe", "english": "help", "part_of_speech": "noun", "gender": "feminine", "plural": "Hilfen", "level": "A2"},
        {"german": "Fehler", "english": "mistake", "part_of_speech": "noun", "gender": "masculine", "plural": "Fehler", "level": "A2"},
        {"german": "Erfolg", "english": "success", "part_of_speech": "noun", "gender": "masculine", "plural": "Erfolge", "level": "A2"},
    ]


def _nouns_b1() -> list[dict]:
    return []


def _nouns_b2() -> list[dict]:
    return []


def _nouns_c1() -> list[dict]:
    return []


def _nouns_c2() -> list[dict]:
    return []


# ---------------------------------------------------------------------------
# VERBS
# ---------------------------------------------------------------------------

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
        {"german": "sprechen", "english": "to speak", "part_of_speech": "verb", "level": "A1"},
        {"german": "arbeiten", "english": "to work", "part_of_speech": "verb", "level": "A1"},
        {"german": "spielen", "english": "to play", "part_of_speech": "verb", "level": "A1"},
        {"german": "lernen", "english": "to learn", "part_of_speech": "verb", "level": "A1"},
        {"german": "lesen", "english": "to read", "part_of_speech": "verb", "level": "A1"},
        {"german": "schreiben", "english": "to write", "part_of_speech": "verb", "level": "A1"},
        {"german": "hören", "english": "to hear", "part_of_speech": "verb", "level": "A1"},
        {"german": "kaufen", "english": "to buy", "part_of_speech": "verb", "level": "A1"},
        {"german": "essen", "english": "to eat", "part_of_speech": "verb", "level": "A1"},
        {"german": "trinken", "english": "to drink", "part_of_speech": "verb", "level": "A1"},
        {"german": "schlafen", "english": "to sleep", "part_of_speech": "verb", "level": "A1"},
        {"german": "wohnen", "english": "to live (reside)", "part_of_speech": "verb", "level": "A1"},
        {"german": "fahren", "english": "to drive / to travel", "part_of_speech": "verb", "level": "A1"},
        {"german": "fragen", "english": "to ask", "part_of_speech": "verb", "level": "A1"},
        {"german": "antworten", "english": "to answer", "part_of_speech": "verb", "level": "A1"},
        {"german": "verstehen", "english": "to understand", "part_of_speech": "verb", "level": "A1"},
        {"german": "brauchen", "english": "to need", "part_of_speech": "verb", "level": "A1"},
        {"german": "kennen", "english": "to know (a person/place)", "part_of_speech": "verb", "level": "A1"},
        {"german": "leben", "english": "to live (be alive)", "part_of_speech": "verb", "level": "A1"},
        {"german": "bringen", "english": "to bring", "part_of_speech": "verb", "level": "A1"},
        {"german": "helfen", "english": "to help", "part_of_speech": "verb", "level": "A1"},
        {"german": "laufen", "english": "to run / to walk", "part_of_speech": "verb", "level": "A1"},
        {"german": "kosten", "english": "to cost", "part_of_speech": "verb", "level": "A1"},
        {"german": "öffnen", "english": "to open", "part_of_speech": "verb", "level": "A1"},
        {"german": "schließen", "english": "to close", "part_of_speech": "verb", "level": "A1"},
        {"german": "beginnen", "english": "to begin", "part_of_speech": "verb", "level": "A1"},
        {"german": "kochen", "english": "to cook", "part_of_speech": "verb", "level": "A1"},
        {"german": "warten", "english": "to wait", "part_of_speech": "verb", "level": "A1"},
        {"german": "bezahlen", "english": "to pay", "part_of_speech": "verb", "level": "A1"},
        {"german": "suchen", "english": "to search / to look for", "part_of_speech": "verb", "level": "A1"},
        {"german": "sitzen", "english": "to sit", "part_of_speech": "verb", "level": "A1"},
        {"german": "rufen", "english": "to call (shout)", "part_of_speech": "verb", "level": "A1"},
        {"german": "tragen", "english": "to carry / to wear", "part_of_speech": "verb", "level": "A1"},
        {"german": "fallen", "english": "to fall", "part_of_speech": "verb", "level": "A1"},
        {"german": "ziehen", "english": "to pull / to move", "part_of_speech": "verb", "level": "A1"},
        {"german": "bekommen", "english": "to receive / to get", "part_of_speech": "verb", "level": "A1"},
        {"german": "versuchen", "english": "to try", "part_of_speech": "verb", "level": "A1"},
        {"german": "aufstehen", "english": "to get up / to stand up", "part_of_speech": "verb", "level": "A1"},
        {"german": "anfangen", "english": "to start / to begin", "part_of_speech": "verb", "level": "A1"},
        {"german": "einkaufen", "english": "to shop / to go shopping", "part_of_speech": "verb", "level": "A1"},
        {"german": "anrufen", "english": "to call (phone)", "part_of_speech": "verb", "level": "A1"},
        {"german": "mitkommen", "english": "to come along", "part_of_speech": "verb", "level": "A1"},
        {"german": "fernsehen", "english": "to watch TV", "part_of_speech": "verb", "level": "A1"},
        {"german": "gefallen", "english": "to be pleasing / to like", "part_of_speech": "verb", "level": "A1"},
        {"german": "gehören", "english": "to belong to", "part_of_speech": "verb", "level": "A1"},
        {"german": "stimmen", "english": "to be correct / to be right", "part_of_speech": "verb", "level": "A1"},
        {"german": "dauern", "english": "to last / to take (time)", "part_of_speech": "verb", "level": "A1"},
    ]


def _verbs_a2() -> list[dict]:
    return [
        {"german": "erklären", "english": "to explain", "part_of_speech": "verb", "level": "A2"},
        {"german": "erzählen", "english": "to tell / to narrate", "part_of_speech": "verb", "level": "A2"},
        {"german": "vergessen", "english": "to forget", "part_of_speech": "verb", "level": "A2"},
        {"german": "erinnern", "english": "to remind", "part_of_speech": "verb", "level": "A2"},
        {"german": "beschreiben", "english": "to describe", "part_of_speech": "verb", "level": "A2"},
        {"german": "entscheiden", "english": "to decide", "part_of_speech": "verb", "level": "A2"},
        {"german": "empfehlen", "english": "to recommend", "part_of_speech": "verb", "level": "A2"},
        {"german": "bestellen", "english": "to order", "part_of_speech": "verb", "level": "A2"},
        {"german": "besuchen", "english": "to visit", "part_of_speech": "verb", "level": "A2"},
        {"german": "verbringen", "english": "to spend (time)", "part_of_speech": "verb", "level": "A2"},
        {"german": "reisen", "english": "to travel", "part_of_speech": "verb", "level": "A2"},
        {"german": "fliegen", "english": "to fly", "part_of_speech": "verb", "level": "A2"},
        {"german": "schwimmen", "english": "to swim", "part_of_speech": "verb", "level": "A2"},
        {"german": "wandern", "english": "to hike", "part_of_speech": "verb", "level": "A2"},
        {"german": "aufhören", "english": "to stop / to cease", "part_of_speech": "verb", "level": "A2"},
        {"german": "einladen", "english": "to invite", "part_of_speech": "verb", "level": "A2"},
        {"german": "ausgeben", "english": "to spend (money)", "part_of_speech": "verb", "level": "A2"},
        {"german": "umziehen", "english": "to move (residence)", "part_of_speech": "verb", "level": "A2"},
        {"german": "vorbereiten", "english": "to prepare", "part_of_speech": "verb", "level": "A2"},
        {"german": "teilnehmen", "english": "to participate", "part_of_speech": "verb", "level": "A2"},
        {"german": "stattfinden", "english": "to take place", "part_of_speech": "verb", "level": "A2"},
        {"german": "vorschlagen", "english": "to suggest / to propose", "part_of_speech": "verb", "level": "A2"},
        {"german": "abholen", "english": "to pick up / to collect", "part_of_speech": "verb", "level": "A2"},
        {"german": "ankommen", "english": "to arrive", "part_of_speech": "verb", "level": "A2"},
        {"german": "abfahren", "english": "to depart", "part_of_speech": "verb", "level": "A2"},
        {"german": "umsteigen", "english": "to transfer / to change (trains)", "part_of_speech": "verb", "level": "A2"},
        {"german": "aussteigen", "english": "to get off / to exit", "part_of_speech": "verb", "level": "A2"},
        {"german": "einsteigen", "english": "to get on / to board", "part_of_speech": "verb", "level": "A2"},
        {"german": "verdienen", "english": "to earn", "part_of_speech": "verb", "level": "A2"},
        {"german": "sparen", "english": "to save (money)", "part_of_speech": "verb", "level": "A2"},
        {"german": "leihen", "english": "to lend / to borrow", "part_of_speech": "verb", "level": "A2"},
        {"german": "wechseln", "english": "to change / to exchange", "part_of_speech": "verb", "level": "A2"},
        {"german": "reparieren", "english": "to repair", "part_of_speech": "verb", "level": "A2"},
        {"german": "putzen", "english": "to clean", "part_of_speech": "verb", "level": "A2"},
        {"german": "waschen", "english": "to wash", "part_of_speech": "verb", "level": "A2"},
        {"german": "aufräumen", "english": "to tidy up / to clean up", "part_of_speech": "verb", "level": "A2"},
        {"german": "schmecken", "english": "to taste", "part_of_speech": "verb", "level": "A2"},
        {"german": "riechen", "english": "to smell", "part_of_speech": "verb", "level": "A2"},
        {"german": "backen", "english": "to bake", "part_of_speech": "verb", "level": "A2"},
        {"german": "schneiden", "english": "to cut", "part_of_speech": "verb", "level": "A2"},
        {"german": "hoffen", "english": "to hope", "part_of_speech": "verb", "level": "A2"},
        {"german": "wünschen", "english": "to wish", "part_of_speech": "verb", "level": "A2"},
        {"german": "träumen", "english": "to dream", "part_of_speech": "verb", "level": "A2"},
        {"german": "lachen", "english": "to laugh", "part_of_speech": "verb", "level": "A2"},
        {"german": "weinen", "english": "to cry", "part_of_speech": "verb", "level": "A2"},
        {"german": "übersetzen", "english": "to translate", "part_of_speech": "verb", "level": "A2"},
        {"german": "üben", "english": "to practice", "part_of_speech": "verb", "level": "A2"},
        {"german": "wiederholen", "english": "to repeat / to review", "part_of_speech": "verb", "level": "A2"},
        {"german": "prüfen", "english": "to test / to check", "part_of_speech": "verb", "level": "A2"},
        {"german": "unterschreiben", "english": "to sign (a document)", "part_of_speech": "verb", "level": "A2"},
        {"german": "erreichen", "english": "to reach / to achieve", "part_of_speech": "verb", "level": "A2"},
        {"german": "verlieren", "english": "to lose", "part_of_speech": "verb", "level": "A2"},
        {"german": "gewinnen", "english": "to win", "part_of_speech": "verb", "level": "A2"},
    ]


def _verbs_b1() -> list[dict]:
    return []


def _verbs_b2() -> list[dict]:
    return []


def _verbs_c1() -> list[dict]:
    return []


def _verbs_c2() -> list[dict]:
    return []


# ---------------------------------------------------------------------------
# ADJECTIVES
# ---------------------------------------------------------------------------

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
        # Colors
        {"german": "rot", "english": "red", "part_of_speech": "adjective", "level": "A1"},
        {"german": "blau", "english": "blue", "part_of_speech": "adjective", "level": "A1"},
        {"german": "grün", "english": "green", "part_of_speech": "adjective", "level": "A1"},
        {"german": "gelb", "english": "yellow", "part_of_speech": "adjective", "level": "A1"},
        {"german": "weiß", "english": "white", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schwarz", "english": "black", "part_of_speech": "adjective", "level": "A1"},
        {"german": "braun", "english": "brown", "part_of_speech": "adjective", "level": "A1"},
        # Temperature & Physical
        {"german": "warm", "english": "warm", "part_of_speech": "adjective", "level": "A1"},
        {"german": "kalt", "english": "cold", "part_of_speech": "adjective", "level": "A1"},
        {"german": "heiß", "english": "hot", "part_of_speech": "adjective", "level": "A1"},
        {"german": "nett", "english": "nice/kind", "part_of_speech": "adjective", "level": "A1"},
        {"german": "lieb", "english": "dear/sweet", "part_of_speech": "adjective", "level": "A1"},
        {"german": "müde", "english": "tired", "part_of_speech": "adjective", "level": "A1"},
        {"german": "krank", "english": "sick/ill", "part_of_speech": "adjective", "level": "A1"},
        {"german": "gesund", "english": "healthy", "part_of_speech": "adjective", "level": "A1"},
        {"german": "frei", "english": "free", "part_of_speech": "adjective", "level": "A1"},
        {"german": "fertig", "english": "finished/ready", "part_of_speech": "adjective", "level": "A1"},
        {"german": "billig", "english": "cheap", "part_of_speech": "adjective", "level": "A1"},
        {"german": "teuer", "english": "expensive", "part_of_speech": "adjective", "level": "A1"},
        {"german": "voll", "english": "full", "part_of_speech": "adjective", "level": "A1"},
        {"german": "leer", "english": "empty", "part_of_speech": "adjective", "level": "A1"},
        {"german": "offen", "english": "open", "part_of_speech": "adjective", "level": "A1"},
        {"german": "dunkel", "english": "dark", "part_of_speech": "adjective", "level": "A1"},
        {"german": "dick", "english": "thick/fat", "part_of_speech": "adjective", "level": "A1"},
        {"german": "dünn", "english": "thin", "part_of_speech": "adjective", "level": "A1"},
        {"german": "laut", "english": "loud", "part_of_speech": "adjective", "level": "A1"},
        {"german": "leise", "english": "quiet", "part_of_speech": "adjective", "level": "A1"},
        {"german": "nah", "english": "near/close", "part_of_speech": "adjective", "level": "A1"},
        {"german": "weit", "english": "far/wide", "part_of_speech": "adjective", "level": "A1"},
        {"german": "breit", "english": "wide/broad", "part_of_speech": "adjective", "level": "A1"},
        {"german": "eng", "english": "narrow/tight", "part_of_speech": "adjective", "level": "A1"},
        {"german": "froh", "english": "happy/glad", "part_of_speech": "adjective", "level": "A1"},
        {"german": "traurig", "english": "sad", "part_of_speech": "adjective", "level": "A1"},
        {"german": "hungrig", "english": "hungry", "part_of_speech": "adjective", "level": "A1"},
        {"german": "durstig", "english": "thirsty", "part_of_speech": "adjective", "level": "A1"},
        {"german": "sauber", "english": "clean", "part_of_speech": "adjective", "level": "A1"},
        {"german": "schmutzig", "english": "dirty", "part_of_speech": "adjective", "level": "A1"},
        {"german": "trocken", "english": "dry", "part_of_speech": "adjective", "level": "A1"},
        {"german": "nass", "english": "wet", "part_of_speech": "adjective", "level": "A1"},
        {"german": "rund", "english": "round", "part_of_speech": "adjective", "level": "A1"},
    ]


def _adjectives_a2() -> list[dict]:
    return [
        # Colors
        {"german": "grau", "english": "gray", "part_of_speech": "adjective", "level": "A2"},
        {"german": "rosa", "english": "pink", "part_of_speech": "adjective", "level": "A2"},
        {"german": "lila", "english": "purple", "part_of_speech": "adjective", "level": "A2"},
        # Personality
        {"german": "freundlich", "english": "friendly", "part_of_speech": "adjective", "level": "A2"},
        {"german": "unfreundlich", "english": "unfriendly", "part_of_speech": "adjective", "level": "A2"},
        {"german": "höflich", "english": "polite", "part_of_speech": "adjective", "level": "A2"},
        {"german": "unhöflich", "english": "impolite/rude", "part_of_speech": "adjective", "level": "A2"},
        {"german": "lustig", "english": "funny", "part_of_speech": "adjective", "level": "A2"},
        {"german": "langweilig", "english": "boring", "part_of_speech": "adjective", "level": "A2"},
        {"german": "interessant", "english": "interesting", "part_of_speech": "adjective", "level": "A2"},
        # Safety & Possibility
        {"german": "gefährlich", "english": "dangerous", "part_of_speech": "adjective", "level": "A2"},
        {"german": "sicher", "english": "safe/sure", "part_of_speech": "adjective", "level": "A2"},
        {"german": "möglich", "english": "possible", "part_of_speech": "adjective", "level": "A2"},
        {"german": "unmöglich", "english": "impossible", "part_of_speech": "adjective", "level": "A2"},
        # Familiarity
        {"german": "bekannt", "english": "well-known/familiar", "part_of_speech": "adjective", "level": "A2"},
        {"german": "berühmt", "english": "famous", "part_of_speech": "adjective", "level": "A2"},
        {"german": "gemütlich", "english": "cozy/comfortable", "part_of_speech": "adjective", "level": "A2"},
        {"german": "bequem", "english": "comfortable/convenient", "part_of_speech": "adjective", "level": "A2"},
        {"german": "praktisch", "english": "practical", "part_of_speech": "adjective", "level": "A2"},
        {"german": "typisch", "english": "typical", "part_of_speech": "adjective", "level": "A2"},
        {"german": "normal", "english": "normal", "part_of_speech": "adjective", "level": "A2"},
        {"german": "verschieden", "english": "different/various", "part_of_speech": "adjective", "level": "A2"},
        {"german": "gleich", "english": "same/equal", "part_of_speech": "adjective", "level": "A2"},
        {"german": "ähnlich", "english": "similar", "part_of_speech": "adjective", "level": "A2"},
        {"german": "einfach", "english": "simple/easy", "part_of_speech": "adjective", "level": "A2"},
        {"german": "schwierig", "english": "difficult", "part_of_speech": "adjective", "level": "A2"},
        # Physical
        {"german": "stark", "english": "strong", "part_of_speech": "adjective", "level": "A2"},
        {"german": "schwach", "english": "weak", "part_of_speech": "adjective", "level": "A2"},
        {"german": "frisch", "english": "fresh", "part_of_speech": "adjective", "level": "A2"},
        # Taste
        {"german": "süß", "english": "sweet", "part_of_speech": "adjective", "level": "A2"},
        {"german": "sauer", "english": "sour", "part_of_speech": "adjective", "level": "A2"},
        {"german": "salzig", "english": "salty", "part_of_speech": "adjective", "level": "A2"},
        {"german": "bitter", "english": "bitter", "part_of_speech": "adjective", "level": "A2"},
        {"german": "scharf", "english": "spicy/sharp", "part_of_speech": "adjective", "level": "A2"},
        {"german": "lecker", "english": "delicious/tasty", "part_of_speech": "adjective", "level": "A2"},
        # Evaluation
        {"german": "wunderbar", "english": "wonderful", "part_of_speech": "adjective", "level": "A2"},
        {"german": "schrecklich", "english": "terrible/awful", "part_of_speech": "adjective", "level": "A2"},
        {"german": "herrlich", "english": "splendid/magnificent", "part_of_speech": "adjective", "level": "A2"},
        # Emotions
        {"german": "ärgerlich", "english": "annoying/annoyed", "part_of_speech": "adjective", "level": "A2"},
        {"german": "nervös", "english": "nervous", "part_of_speech": "adjective", "level": "A2"},
        {"german": "aufgeregt", "english": "excited", "part_of_speech": "adjective", "level": "A2"},
        {"german": "zufrieden", "english": "satisfied/content", "part_of_speech": "adjective", "level": "A2"},
        {"german": "neugierig", "english": "curious", "part_of_speech": "adjective", "level": "A2"},
        {"german": "stolz", "english": "proud", "part_of_speech": "adjective", "level": "A2"},
        {"german": "ängstlich", "english": "anxious/fearful", "part_of_speech": "adjective", "level": "A2"},
        # Weather
        {"german": "sonnig", "english": "sunny", "part_of_speech": "adjective", "level": "A2"},
        {"german": "bewölkt", "english": "cloudy", "part_of_speech": "adjective", "level": "A2"},
        {"german": "windig", "english": "windy", "part_of_speech": "adjective", "level": "A2"},
        {"german": "kühl", "english": "cool", "part_of_speech": "adjective", "level": "A2"},
        {"german": "mild", "english": "mild", "part_of_speech": "adjective", "level": "A2"},
        # Character
        {"german": "notwendig", "english": "necessary", "part_of_speech": "adjective", "level": "A2"},
        {"german": "günstig", "english": "favorable/affordable", "part_of_speech": "adjective", "level": "A2"},
        {"german": "verrückt", "english": "crazy", "part_of_speech": "adjective", "level": "A2"},
        {"german": "mutig", "english": "brave/courageous", "part_of_speech": "adjective", "level": "A2"},
        {"german": "ehrlich", "english": "honest", "part_of_speech": "adjective", "level": "A2"},
        {"german": "fleißig", "english": "hard-working/diligent", "part_of_speech": "adjective", "level": "A2"},
        {"german": "faul", "english": "lazy", "part_of_speech": "adjective", "level": "A2"},
        {"german": "ruhig", "english": "calm/quiet", "part_of_speech": "adjective", "level": "A2"},
        {"german": "schlimm", "english": "bad/severe", "part_of_speech": "adjective", "level": "A2"},
        {"german": "seltsam", "english": "strange/odd", "part_of_speech": "adjective", "level": "A2"},
        {"german": "ordentlich", "english": "tidy/orderly", "part_of_speech": "adjective", "level": "A2"},
        {"german": "hübsch", "english": "pretty", "part_of_speech": "adjective", "level": "A2"},
        {"german": "hässlich", "english": "ugly", "part_of_speech": "adjective", "level": "A2"},
        {"german": "weich", "english": "soft", "part_of_speech": "adjective", "level": "A2"},
        {"german": "hart", "english": "hard", "part_of_speech": "adjective", "level": "A2"},
        {"german": "glücklich", "english": "happy/lucky", "part_of_speech": "adjective", "level": "A2"},
    ]


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
