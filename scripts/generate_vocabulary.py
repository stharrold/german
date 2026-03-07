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
        Number of validated words, or -1 if validation failed.
    """
    errors = []
    seen = set()
    validated = []

    for i, entry in enumerate(words):
        german = entry.get("german", f"entry-{i}")

        # Check duplicates (same word + same POS)
        key = (entry.get("german", "").lower(), entry.get("part_of_speech", ""))
        if key in seen:
            errors.append(f"  Duplicate: {german} ({entry.get('part_of_speech', '?')})")
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
        return -1

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

    return len(validated)


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
        count = validate_and_write(words, resources_dir / filename, dry_run=args.dry_run)
        if count < 0:
            all_ok = False
        else:
            total += count

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
    return [
        # Politics
        {"german": "Regierung", "english": "government", "part_of_speech": "noun", "gender": "feminine", "plural": "Regierungen", "level": "B1"},
        {"german": "Wahl", "english": "election", "part_of_speech": "noun", "gender": "feminine", "plural": "Wahlen", "level": "B1"},
        {"german": "Partei", "english": "political party", "part_of_speech": "noun", "gender": "feminine", "plural": "Parteien", "level": "B1"},
        {"german": "Gesetz", "english": "law", "part_of_speech": "noun", "gender": "neuter", "plural": "Gesetze", "level": "B1"},
        {"german": "Politiker", "english": "politician", "part_of_speech": "noun", "gender": "masculine", "plural": "Politiker", "level": "B1"},
        {"german": "Staat", "english": "state", "part_of_speech": "noun", "gender": "masculine", "plural": "Staaten", "level": "B1"},
        {"german": "Bürger", "english": "citizen", "part_of_speech": "noun", "gender": "masculine", "plural": "Bürger", "level": "B1"},
        {"german": "Demokratie", "english": "democracy", "part_of_speech": "noun", "gender": "feminine", "plural": "Demokratien", "level": "B1"},
        {"german": "Freiheit", "english": "freedom", "part_of_speech": "noun", "gender": "feminine", "plural": "Freiheiten", "level": "B1"},
        # Education
        {"german": "Bildung", "english": "education", "part_of_speech": "noun", "gender": "feminine", "plural": "Bildungen", "level": "B1"},
        {"german": "Wissenschaft", "english": "science", "part_of_speech": "noun", "gender": "feminine", "plural": "Wissenschaften", "level": "B1"},
        {"german": "Forschung", "english": "research", "part_of_speech": "noun", "gender": "feminine", "plural": "Forschungen", "level": "B1"},
        {"german": "Studium", "english": "studies (university)", "part_of_speech": "noun", "gender": "neuter", "plural": "Studien", "level": "B1"},
        {"german": "Abschluss", "english": "degree/graduation", "part_of_speech": "noun", "gender": "masculine", "plural": "Abschlüsse", "level": "B1"},
        {"german": "Stipendium", "english": "scholarship", "part_of_speech": "noun", "gender": "neuter", "plural": "Stipendien", "level": "B1"},
        {"german": "Unterricht", "english": "instruction/lesson", "part_of_speech": "noun", "gender": "masculine", "plural": "Unterrichte", "level": "B1"},
        {"german": "Ausbildung", "english": "vocational training", "part_of_speech": "noun", "gender": "feminine", "plural": "Ausbildungen", "level": "B1"},
        # Environment
        {"german": "Umwelt", "english": "environment", "part_of_speech": "noun", "gender": "feminine", "plural": "Umwelten", "level": "B1"},
        {"german": "Verschmutzung", "english": "pollution", "part_of_speech": "noun", "gender": "feminine", "plural": "Verschmutzungen", "level": "B1"},
        {"german": "Energie", "english": "energy", "part_of_speech": "noun", "gender": "feminine", "plural": "Energien", "level": "B1"},
        {"german": "Müll", "english": "waste/garbage", "part_of_speech": "noun", "gender": "masculine", "plural": "Mülle", "level": "B1"},
        {"german": "Klima", "english": "climate", "part_of_speech": "noun", "gender": "neuter", "plural": "Klimata", "level": "B1"},
        {"german": "Natur", "english": "nature", "part_of_speech": "noun", "gender": "feminine", "plural": "Naturen", "level": "B1"},
        {"german": "Schutz", "english": "protection", "part_of_speech": "noun", "gender": "masculine", "plural": "Schutze", "level": "B1"},
        {"german": "Rohstoff", "english": "raw material", "part_of_speech": "noun", "gender": "masculine", "plural": "Rohstoffe", "level": "B1"},
        # Society
        {"german": "Gesellschaft", "english": "society", "part_of_speech": "noun", "gender": "feminine", "plural": "Gesellschaften", "level": "B1"},
        {"german": "Bevölkerung", "english": "population", "part_of_speech": "noun", "gender": "feminine", "plural": "Bevölkerungen", "level": "B1"},
        {"german": "Gemeinschaft", "english": "community", "part_of_speech": "noun", "gender": "feminine", "plural": "Gemeinschaften", "level": "B1"},
        {"german": "Verantwortung", "english": "responsibility", "part_of_speech": "noun", "gender": "feminine", "plural": "Verantwortungen", "level": "B1"},
        {"german": "Verein", "english": "club/association", "part_of_speech": "noun", "gender": "masculine", "plural": "Vereine", "level": "B1"},
        {"german": "Jugend", "english": "youth", "part_of_speech": "noun", "gender": "feminine", "plural": "Jugenden", "level": "B1"},
        {"german": "Tradition", "english": "tradition", "part_of_speech": "noun", "gender": "feminine", "plural": "Traditionen", "level": "B1"},
        {"german": "Zusammenhang", "english": "context/connection", "part_of_speech": "noun", "gender": "masculine", "plural": "Zusammenhänge", "level": "B1"},
        # Culture
        {"german": "Kultur", "english": "culture", "part_of_speech": "noun", "gender": "feminine", "plural": "Kulturen", "level": "B1"},
        {"german": "Kunst", "english": "art", "part_of_speech": "noun", "gender": "feminine", "plural": "Künste", "level": "B1"},
        {"german": "Theater", "english": "theater", "part_of_speech": "noun", "gender": "neuter", "plural": "Theater", "level": "B1"},
        {"german": "Ausstellung", "english": "exhibition", "part_of_speech": "noun", "gender": "feminine", "plural": "Ausstellungen", "level": "B1"},
        {"german": "Veranstaltung", "english": "event", "part_of_speech": "noun", "gender": "feminine", "plural": "Veranstaltungen", "level": "B1"},
        {"german": "Konzert", "english": "concert", "part_of_speech": "noun", "gender": "neuter", "plural": "Konzerte", "level": "B1"},
        {"german": "Roman", "english": "novel", "part_of_speech": "noun", "gender": "masculine", "plural": "Romane", "level": "B1"},
        {"german": "Literatur", "english": "literature", "part_of_speech": "noun", "gender": "feminine", "plural": "Literaturen", "level": "B1"},
        # Technology
        {"german": "Technik", "english": "technology/technique", "part_of_speech": "noun", "gender": "feminine", "plural": "Techniken", "level": "B1"},
        {"german": "Gerät", "english": "device", "part_of_speech": "noun", "gender": "neuter", "plural": "Geräte", "level": "B1"},
        {"german": "Bildschirm", "english": "screen", "part_of_speech": "noun", "gender": "masculine", "plural": "Bildschirme", "level": "B1"},
        {"german": "Netzwerk", "english": "network", "part_of_speech": "noun", "gender": "neuter", "plural": "Netzwerke", "level": "B1"},
        {"german": "Programm", "english": "program", "part_of_speech": "noun", "gender": "neuter", "plural": "Programme", "level": "B1"},
        {"german": "Anwendung", "english": "application", "part_of_speech": "noun", "gender": "feminine", "plural": "Anwendungen", "level": "B1"},
        # Emotions & Health
        {"german": "Trauer", "english": "grief/sorrow", "part_of_speech": "noun", "gender": "feminine", "plural": "Trauern", "level": "B1"},
        {"german": "Wut", "english": "rage/anger", "part_of_speech": "noun", "gender": "feminine", "plural": "Wüte", "level": "B1"},
        {"german": "Hoffnung", "english": "hope", "part_of_speech": "noun", "gender": "feminine", "plural": "Hoffnungen", "level": "B1"},
        {"german": "Enttäuschung", "english": "disappointment", "part_of_speech": "noun", "gender": "feminine", "plural": "Enttäuschungen", "level": "B1"},
        {"german": "Leidenschaft", "english": "passion", "part_of_speech": "noun", "gender": "feminine", "plural": "Leidenschaften", "level": "B1"},
        {"german": "Stimmung", "english": "mood", "part_of_speech": "noun", "gender": "feminine", "plural": "Stimmungen", "level": "B1"},
        {"german": "Ernährung", "english": "nutrition/diet", "part_of_speech": "noun", "gender": "feminine", "plural": "Ernährungen", "level": "B1"},
        {"german": "Behandlung", "english": "treatment", "part_of_speech": "noun", "gender": "feminine", "plural": "Behandlungen", "level": "B1"},
        {"german": "Untersuchung", "english": "examination", "part_of_speech": "noun", "gender": "feminine", "plural": "Untersuchungen", "level": "B1"},
        {"german": "Versicherung", "english": "insurance", "part_of_speech": "noun", "gender": "feminine", "plural": "Versicherungen", "level": "B1"},
        {"german": "Verletzung", "english": "injury", "part_of_speech": "noun", "gender": "feminine", "plural": "Verletzungen", "level": "B1"},
        {"german": "Therapie", "english": "therapy", "part_of_speech": "noun", "gender": "feminine", "plural": "Therapien", "level": "B1"},
        {"german": "Fieber", "english": "fever", "part_of_speech": "noun", "gender": "neuter", "plural": "Fieber", "level": "B1"},
        # Media
        {"german": "Bericht", "english": "report", "part_of_speech": "noun", "gender": "masculine", "plural": "Berichte", "level": "B1"},
        {"german": "Sendung", "english": "broadcast/show", "part_of_speech": "noun", "gender": "feminine", "plural": "Sendungen", "level": "B1"},
        {"german": "Werbung", "english": "advertising", "part_of_speech": "noun", "gender": "feminine", "plural": "Werbungen", "level": "B1"},
        {"german": "Journalist", "english": "journalist", "part_of_speech": "noun", "gender": "masculine", "plural": "Journalisten", "level": "B1"},
        {"german": "Artikel", "english": "article", "part_of_speech": "noun", "gender": "masculine", "plural": "Artikel", "level": "B1"},
        {"german": "Zeitschrift", "english": "magazine", "part_of_speech": "noun", "gender": "feminine", "plural": "Zeitschriften", "level": "B1"},
        {"german": "Zuschauer", "english": "viewer/spectator", "part_of_speech": "noun", "gender": "masculine", "plural": "Zuschauer", "level": "B1"},
        {"german": "Presse", "english": "press", "part_of_speech": "noun", "gender": "feminine", "plural": "Pressen", "level": "B1"},
    ]


def _nouns_b2() -> list[dict]:
    return [
        # Science
        {"german": "Hypothese", "english": "hypothesis", "part_of_speech": "noun", "gender": "feminine", "plural": "Hypothesen", "level": "B2"},
        {"german": "Experiment", "english": "experiment", "part_of_speech": "noun", "gender": "neuter", "plural": "Experimente", "level": "B2"},
        {"german": "Ergebnis", "english": "result", "part_of_speech": "noun", "gender": "neuter", "plural": "Ergebnisse", "level": "B2"},
        {"german": "Analyse", "english": "analysis", "part_of_speech": "noun", "gender": "feminine", "plural": "Analysen", "level": "B2"},
        {"german": "Theorie", "english": "theory", "part_of_speech": "noun", "gender": "feminine", "plural": "Theorien", "level": "B2"},
        {"german": "Methode", "english": "method", "part_of_speech": "noun", "gender": "feminine", "plural": "Methoden", "level": "B2"},
        {"german": "Studie", "english": "study", "part_of_speech": "noun", "gender": "feminine", "plural": "Studien", "level": "B2"},
        {"german": "Labor", "english": "laboratory", "part_of_speech": "noun", "gender": "neuter", "plural": "Labore", "level": "B2"},
        {"german": "Beweis", "english": "proof/evidence", "part_of_speech": "noun", "gender": "masculine", "plural": "Beweise", "level": "B2"},
        {"german": "Phänomen", "english": "phenomenon", "part_of_speech": "noun", "gender": "neuter", "plural": "Phänomene", "level": "B2"},
        {"german": "Zelle", "english": "cell", "part_of_speech": "noun", "gender": "feminine", "plural": "Zellen", "level": "B2"},
        # Law
        {"german": "Gericht", "english": "court", "part_of_speech": "noun", "gender": "neuter", "plural": "Gerichte", "level": "B2"},
        {"german": "Urteil", "english": "verdict/judgment", "part_of_speech": "noun", "gender": "neuter", "plural": "Urteile", "level": "B2"},
        {"german": "Anwalt", "english": "lawyer", "part_of_speech": "noun", "gender": "masculine", "plural": "Anwälte", "level": "B2"},
        {"german": "Richter", "english": "judge", "part_of_speech": "noun", "gender": "masculine", "plural": "Richter", "level": "B2"},
        {"german": "Vertrag", "english": "contract", "part_of_speech": "noun", "gender": "masculine", "plural": "Verträge", "level": "B2"},
        {"german": "Klage", "english": "lawsuit/complaint", "part_of_speech": "noun", "gender": "feminine", "plural": "Klagen", "level": "B2"},
        {"german": "Verfahren", "english": "proceedings/procedure", "part_of_speech": "noun", "gender": "neuter", "plural": "Verfahren", "level": "B2"},
        {"german": "Vorschrift", "english": "regulation", "part_of_speech": "noun", "gender": "feminine", "plural": "Vorschriften", "level": "B2"},
        {"german": "Verfassung", "english": "constitution", "part_of_speech": "noun", "gender": "feminine", "plural": "Verfassungen", "level": "B2"},
        # Economics
        {"german": "Wirtschaft", "english": "economy", "part_of_speech": "noun", "gender": "feminine", "plural": "Wirtschaften", "level": "B2"},
        {"german": "Handel", "english": "trade/commerce", "part_of_speech": "noun", "gender": "masculine", "plural": "Handel", "level": "B2"},
        {"german": "Umsatz", "english": "revenue/turnover", "part_of_speech": "noun", "gender": "masculine", "plural": "Umsätze", "level": "B2"},
        {"german": "Gewinn", "english": "profit", "part_of_speech": "noun", "gender": "masculine", "plural": "Gewinne", "level": "B2"},
        {"german": "Verlust", "english": "loss", "part_of_speech": "noun", "gender": "masculine", "plural": "Verluste", "level": "B2"},
        {"german": "Aktie", "english": "stock/share", "part_of_speech": "noun", "gender": "feminine", "plural": "Aktien", "level": "B2"},
        {"german": "Investition", "english": "investment", "part_of_speech": "noun", "gender": "feminine", "plural": "Investitionen", "level": "B2"},
        {"german": "Konkurrenz", "english": "competition", "part_of_speech": "noun", "gender": "feminine", "plural": "Konkurrenzen", "level": "B2"},
        {"german": "Steuer", "english": "tax", "part_of_speech": "noun", "gender": "feminine", "plural": "Steuern", "level": "B2"},
        {"german": "Haushalt", "english": "budget/household", "part_of_speech": "noun", "gender": "masculine", "plural": "Haushalte", "level": "B2"},
        # Philosophy
        {"german": "Philosophie", "english": "philosophy", "part_of_speech": "noun", "gender": "feminine", "plural": "Philosophien", "level": "B2"},
        {"german": "Ethik", "english": "ethics", "part_of_speech": "noun", "gender": "feminine", "plural": "Ethiken", "level": "B2"},
        {"german": "Bewusstsein", "english": "consciousness", "part_of_speech": "noun", "gender": "neuter", "plural": "Bewusstseine", "level": "B2"},
        {"german": "Erkenntnis", "english": "insight/cognition", "part_of_speech": "noun", "gender": "feminine", "plural": "Erkenntnisse", "level": "B2"},
        {"german": "Wahrheit", "english": "truth", "part_of_speech": "noun", "gender": "feminine", "plural": "Wahrheiten", "level": "B2"},
        {"german": "Wirklichkeit", "english": "reality", "part_of_speech": "noun", "gender": "feminine", "plural": "Wirklichkeiten", "level": "B2"},
        {"german": "Gerechtigkeit", "english": "justice", "part_of_speech": "noun", "gender": "feminine", "plural": "Gerechtigkeiten", "level": "B2"},
        {"german": "Vernunft", "english": "reason/rationality", "part_of_speech": "noun", "gender": "feminine", "plural": "Vernünfte", "level": "B2"},
        {"german": "Widerspruch", "english": "contradiction", "part_of_speech": "noun", "gender": "masculine", "plural": "Widersprüche", "level": "B2"},
        # Professions & Academic
        {"german": "Architekt", "english": "architect", "part_of_speech": "noun", "gender": "masculine", "plural": "Architekten", "level": "B2"},
        {"german": "Ingenieur", "english": "engineer", "part_of_speech": "noun", "gender": "masculine", "plural": "Ingenieure", "level": "B2"},
        {"german": "Dolmetscher", "english": "interpreter", "part_of_speech": "noun", "gender": "masculine", "plural": "Dolmetscher", "level": "B2"},
        {"german": "Dissertation", "english": "dissertation", "part_of_speech": "noun", "gender": "feminine", "plural": "Dissertationen", "level": "B2"},
        {"german": "Vorlesung", "english": "lecture", "part_of_speech": "noun", "gender": "feminine", "plural": "Vorlesungen", "level": "B2"},
        {"german": "Semester", "english": "semester", "part_of_speech": "noun", "gender": "neuter", "plural": "Semester", "level": "B2"},
        {"german": "Fakultät", "english": "faculty", "part_of_speech": "noun", "gender": "feminine", "plural": "Fakultäten", "level": "B2"},
        {"german": "Dozent", "english": "lecturer", "part_of_speech": "noun", "gender": "masculine", "plural": "Dozenten", "level": "B2"},
        {"german": "Fachgebiet", "english": "field of expertise", "part_of_speech": "noun", "gender": "neuter", "plural": "Fachgebiete", "level": "B2"},
        # Culture
        {"german": "Epoche", "english": "epoch/era", "part_of_speech": "noun", "gender": "feminine", "plural": "Epochen", "level": "B2"},
        {"german": "Denkmal", "english": "monument/memorial", "part_of_speech": "noun", "gender": "neuter", "plural": "Denkmäler", "level": "B2"},
        {"german": "Aufführung", "english": "performance", "part_of_speech": "noun", "gender": "feminine", "plural": "Aufführungen", "level": "B2"},
        {"german": "Skulptur", "english": "sculpture", "part_of_speech": "noun", "gender": "feminine", "plural": "Skulpturen", "level": "B2"},
        {"german": "Oper", "english": "opera", "part_of_speech": "noun", "gender": "feminine", "plural": "Opern", "level": "B2"},
        {"german": "Kritik", "english": "criticism/review", "part_of_speech": "noun", "gender": "feminine", "plural": "Kritiken", "level": "B2"},
        {"german": "Verlag", "english": "publishing house", "part_of_speech": "noun", "gender": "masculine", "plural": "Verlage", "level": "B2"},
        {"german": "Kapitel", "english": "chapter", "part_of_speech": "noun", "gender": "neuter", "plural": "Kapitel", "level": "B2"},
        {"german": "Zitat", "english": "quotation", "part_of_speech": "noun", "gender": "neuter", "plural": "Zitate", "level": "B2"},
        {"german": "Manuskript", "english": "manuscript", "part_of_speech": "noun", "gender": "neuter", "plural": "Manuskripte", "level": "B2"},
    ]


def _nouns_c1() -> list[dict]:
    return [
        # Academic / Research
        {"german": "Abhandlung", "english": "treatise/essay", "part_of_speech": "noun", "gender": "feminine", "plural": "Abhandlungen", "level": "C1"},
        {"german": "Gutachten", "english": "expert opinion/report", "part_of_speech": "noun", "gender": "neuter", "plural": "Gutachten", "level": "C1"},
        {"german": "Lehrstuhl", "english": "professorial chair", "part_of_speech": "noun", "gender": "masculine", "plural": "Lehrstühle", "level": "C1"},
        {"german": "Promotion", "english": "doctorate/PhD", "part_of_speech": "noun", "gender": "feminine", "plural": "Promotionen", "level": "C1"},
        {"german": "Habilitation", "english": "habilitation", "part_of_speech": "noun", "gender": "feminine", "plural": "Habilitationen", "level": "C1"},
        {"german": "Korrelation", "english": "correlation", "part_of_speech": "noun", "gender": "feminine", "plural": "Korrelationen", "level": "C1"},
        {"german": "Paradigma", "english": "paradigm", "part_of_speech": "noun", "gender": "neuter", "plural": "Paradigmen", "level": "C1"},
        {"german": "Implikation", "english": "implication", "part_of_speech": "noun", "gender": "feminine", "plural": "Implikationen", "level": "C1"},
        {"german": "Kontext", "english": "context", "part_of_speech": "noun", "gender": "masculine", "plural": "Kontexte", "level": "C1"},
        {"german": "Diskurs", "english": "discourse", "part_of_speech": "noun", "gender": "masculine", "plural": "Diskurse", "level": "C1"},
        # Law / Governance
        {"german": "Rechtsprechung", "english": "jurisdiction", "part_of_speech": "noun", "gender": "feminine", "plural": "Rechtsprechungen", "level": "C1"},
        {"german": "Gesetzgebung", "english": "legislation", "part_of_speech": "noun", "gender": "feminine", "plural": "Gesetzgebungen", "level": "C1"},
        {"german": "Instanz", "english": "instance/authority", "part_of_speech": "noun", "gender": "feminine", "plural": "Instanzen", "level": "C1"},
        {"german": "Erlass", "english": "decree/edict", "part_of_speech": "noun", "gender": "masculine", "plural": "Erlasse", "level": "C1"},
        {"german": "Satzung", "english": "statute/bylaws", "part_of_speech": "noun", "gender": "feminine", "plural": "Satzungen", "level": "C1"},
        # Philosophy / Abstract
        {"german": "Prämisse", "english": "premise", "part_of_speech": "noun", "gender": "feminine", "plural": "Prämissen", "level": "C1"},
        {"german": "Analogie", "english": "analogy", "part_of_speech": "noun", "gender": "feminine", "plural": "Analogien", "level": "C1"},
        {"german": "Ambiguität", "english": "ambiguity", "part_of_speech": "noun", "gender": "feminine", "plural": "Ambiguitäten", "level": "C1"},
        {"german": "Dichotomie", "english": "dichotomy", "part_of_speech": "noun", "gender": "feminine", "plural": "Dichotomien", "level": "C1"},
        {"german": "Abstraktion", "english": "abstraction", "part_of_speech": "noun", "gender": "feminine", "plural": "Abstraktionen", "level": "C1"},
        # Technical / Professional
        {"german": "Infrastruktur", "english": "infrastructure", "part_of_speech": "noun", "gender": "feminine", "plural": "Infrastrukturen", "level": "C1"},
        {"german": "Konjunktur", "english": "economic cycle/boom", "part_of_speech": "noun", "gender": "feminine", "plural": "Konjunkturen", "level": "C1"},
        {"german": "Subvention", "english": "subsidy", "part_of_speech": "noun", "gender": "feminine", "plural": "Subventionen", "level": "C1"},
        {"german": "Rezession", "english": "recession", "part_of_speech": "noun", "gender": "feminine", "plural": "Rezessionen", "level": "C1"},
        {"german": "Bürokratie", "english": "bureaucracy", "part_of_speech": "noun", "gender": "feminine", "plural": "Bürokratien", "level": "C1"},
        # Culture / Society
        {"german": "Rhetorik", "english": "rhetoric", "part_of_speech": "noun", "gender": "feminine", "plural": "Rhetoriken", "level": "C1"},
        {"german": "Ästhetik", "english": "aesthetics", "part_of_speech": "noun", "gender": "feminine", "plural": "Ästhetiken", "level": "C1"},
        {"german": "Autonomie", "english": "autonomy", "part_of_speech": "noun", "gender": "feminine", "plural": "Autonomien", "level": "C1"},
        {"german": "Souveränität", "english": "sovereignty", "part_of_speech": "noun", "gender": "feminine", "plural": "Souveränitäten", "level": "C1"},
        {"german": "Integrität", "english": "integrity", "part_of_speech": "noun", "gender": "feminine", "plural": "Integritäten", "level": "C1"},
        {"german": "Emanzipation", "english": "emancipation", "part_of_speech": "noun", "gender": "feminine", "plural": "Emanzipationen", "level": "C1"},
        {"german": "Konvention", "english": "convention", "part_of_speech": "noun", "gender": "feminine", "plural": "Konventionen", "level": "C1"},
        {"german": "Instinkt", "english": "instinct", "part_of_speech": "noun", "gender": "masculine", "plural": "Instinkte", "level": "C1"},
        {"german": "Kapazität", "english": "capacity", "part_of_speech": "noun", "gender": "feminine", "plural": "Kapazitäten", "level": "C1"},
        {"german": "Dilemma", "english": "dilemma", "part_of_speech": "noun", "gender": "neuter", "plural": "Dilemmata", "level": "C1"},
        {"german": "Disposition", "english": "disposition", "part_of_speech": "noun", "gender": "feminine", "plural": "Dispositionen", "level": "C1"},
        {"german": "Hierarchie", "english": "hierarchy", "part_of_speech": "noun", "gender": "feminine", "plural": "Hierarchien", "level": "C1"},
        {"german": "Kompetenz", "english": "competence", "part_of_speech": "noun", "gender": "feminine", "plural": "Kompetenzen", "level": "C1"},
        {"german": "Komplexität", "english": "complexity", "part_of_speech": "noun", "gender": "feminine", "plural": "Komplexitäten", "level": "C1"},
        {"german": "Transparenz", "english": "transparency", "part_of_speech": "noun", "gender": "feminine", "plural": "Transparenzen", "level": "C1"},
    ]


def _nouns_c2() -> list[dict]:
    return [
        # Literary / Archaic
        {"german": "Abgrund", "english": "abyss/chasm", "part_of_speech": "noun", "gender": "masculine", "plural": "Abgründe", "level": "C2"},
        {"german": "Gleichnis", "english": "parable/allegory", "part_of_speech": "noun", "gender": "neuter", "plural": "Gleichnisse", "level": "C2"},
        {"german": "Trübsal", "english": "tribulation/gloom", "part_of_speech": "noun", "gender": "feminine", "plural": "Trübsale", "level": "C2"},
        {"german": "Tücke", "english": "malice/treachery", "part_of_speech": "noun", "gender": "feminine", "plural": "Tücken", "level": "C2"},
        {"german": "Muße", "english": "leisure/contemplation", "part_of_speech": "noun", "gender": "feminine", "plural": "Mußen", "level": "C2"},
        {"german": "Verlies", "english": "dungeon", "part_of_speech": "noun", "gender": "neuter", "plural": "Verliese", "level": "C2"},
        {"german": "Antlitz", "english": "countenance/visage", "part_of_speech": "noun", "gender": "neuter", "plural": "Antlitze", "level": "C2"},
        {"german": "Ödnis", "english": "wasteland/desolation", "part_of_speech": "noun", "gender": "feminine", "plural": "Ödnisse", "level": "C2"},
        # Scholarly / Specialized
        {"german": "Epistemologie", "english": "epistemology", "part_of_speech": "noun", "gender": "feminine", "plural": "Epistemologien", "level": "C2"},
        {"german": "Ontologie", "english": "ontology", "part_of_speech": "noun", "gender": "feminine", "plural": "Ontologien", "level": "C2"},
        {"german": "Hermeneutik", "english": "hermeneutics", "part_of_speech": "noun", "gender": "feminine", "plural": "Hermeneutiken", "level": "C2"},
        {"german": "Dialektik", "english": "dialectics", "part_of_speech": "noun", "gender": "feminine", "plural": "Dialektiken", "level": "C2"},
        {"german": "Pragmatik", "english": "pragmatics", "part_of_speech": "noun", "gender": "feminine", "plural": "Pragmatiken", "level": "C2"},
        {"german": "Aphorismus", "english": "aphorism", "part_of_speech": "noun", "gender": "masculine", "plural": "Aphorismen", "level": "C2"},
        {"german": "Allegorie", "english": "allegory", "part_of_speech": "noun", "gender": "feminine", "plural": "Allegorien", "level": "C2"},
        {"german": "Metaphysik", "english": "metaphysics", "part_of_speech": "noun", "gender": "feminine", "plural": "Metaphysiken", "level": "C2"},
        # Idiomatic / Cultural
        {"german": "Zeitgeist", "english": "spirit of the age", "part_of_speech": "noun", "gender": "masculine", "plural": "Zeitgeiste", "level": "C2"},
        {"german": "Weltanschauung", "english": "worldview/ideology", "part_of_speech": "noun", "gender": "feminine", "plural": "Weltanschauungen", "level": "C2"},
        {"german": "Wanderlust", "english": "wanderlust", "part_of_speech": "noun", "gender": "feminine", "plural": "Wanderlüste", "level": "C2"},
        {"german": "Sehnsucht", "english": "longing/yearning", "part_of_speech": "noun", "gender": "feminine", "plural": "Sehnsüchte", "level": "C2"},
        {"german": "Schadenfreude", "english": "malicious joy", "part_of_speech": "noun", "gender": "feminine", "plural": "Schadenfreuden", "level": "C2"},
        {"german": "Gemütlichkeit", "english": "coziness/conviviality", "part_of_speech": "noun", "gender": "feminine", "plural": "Gemütlichkeiten", "level": "C2"},
        {"german": "Zerrissenheit", "english": "inner conflict/torn state", "part_of_speech": "noun", "gender": "feminine", "plural": "Zerrissenheiten", "level": "C2"},
        {"german": "Vergänglichkeit", "english": "transience/impermanence", "part_of_speech": "noun", "gender": "feminine", "plural": "Vergänglichkeiten", "level": "C2"},
        {"german": "Unbekümmertheit", "english": "carefreeness", "part_of_speech": "noun", "gender": "feminine", "plural": "Unbekümmertheiten", "level": "C2"},
        {"german": "Geborgenheit", "english": "security/shelter", "part_of_speech": "noun", "gender": "feminine", "plural": "Geborgenheiten", "level": "C2"},
        {"german": "Erhabenheit", "english": "sublimity/grandeur", "part_of_speech": "noun", "gender": "feminine", "plural": "Erhabenheiten", "level": "C2"},
        {"german": "Zwiespalt", "english": "inner conflict/discord", "part_of_speech": "noun", "gender": "masculine", "plural": "Zwiespalte", "level": "C2"},
        {"german": "Widersacher", "english": "adversary/antagonist", "part_of_speech": "noun", "gender": "masculine", "plural": "Widersacher", "level": "C2"},
        {"german": "Fügung", "english": "providence/twist of fate", "part_of_speech": "noun", "gender": "feminine", "plural": "Fügungen", "level": "C2"},
    ]


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
    return [
        {"german": "diskutieren", "english": "to discuss", "part_of_speech": "verb", "level": "B1"},
        {"german": "streiten", "english": "to argue", "part_of_speech": "verb", "level": "B1"},
        {"german": "vereinbaren", "english": "to arrange/agree upon", "part_of_speech": "verb", "level": "B1"},
        {"german": "mitteilen", "english": "to inform/communicate", "part_of_speech": "verb", "level": "B1"},
        {"german": "überzeugen", "english": "to convince", "part_of_speech": "verb", "level": "B1"},
        {"german": "zustimmen", "english": "to agree", "part_of_speech": "verb", "level": "B1"},
        {"german": "ablehnen", "english": "to reject/decline", "part_of_speech": "verb", "level": "B1"},
        {"german": "bewerben", "english": "to apply (for a job)", "part_of_speech": "verb", "level": "B1"},
        {"german": "kündigen", "english": "to quit/resign", "part_of_speech": "verb", "level": "B1"},
        {"german": "einstellen", "english": "to hire/employ", "part_of_speech": "verb", "level": "B1"},
        {"german": "planen", "english": "to plan", "part_of_speech": "verb", "level": "B1"},
        {"german": "organisieren", "english": "to organize", "part_of_speech": "verb", "level": "B1"},
        {"german": "buchen", "english": "to book/reserve", "part_of_speech": "verb", "level": "B1"},
        {"german": "übernachten", "english": "to stay overnight", "part_of_speech": "verb", "level": "B1"},
        {"german": "enttäuschen", "english": "to disappoint", "part_of_speech": "verb", "level": "B1"},
        {"german": "vermissen", "english": "to miss (someone/something)", "part_of_speech": "verb", "level": "B1"},
        {"german": "beraten", "english": "to advise/counsel", "part_of_speech": "verb", "level": "B1"},
        {"german": "vergleichen", "english": "to compare", "part_of_speech": "verb", "level": "B1"},
        {"german": "versprechen", "english": "to promise", "part_of_speech": "verb", "level": "B1"},
        {"german": "warnen", "english": "to warn", "part_of_speech": "verb", "level": "B1"},
        {"german": "bitten", "english": "to ask/request", "part_of_speech": "verb", "level": "B1"},
        {"german": "bewundern", "english": "to admire", "part_of_speech": "verb", "level": "B1"},
        {"german": "vermuten", "english": "to suspect/assume", "part_of_speech": "verb", "level": "B1"},
        {"german": "vorziehen", "english": "to prefer", "part_of_speech": "verb", "level": "B1"},
        {"german": "veröffentlichen", "english": "to publish", "part_of_speech": "verb", "level": "B1"},
        {"german": "unterstützen", "english": "to support", "part_of_speech": "verb", "level": "B1"},
        {"german": "beobachten", "english": "to observe", "part_of_speech": "verb", "level": "B1"},
        {"german": "stören", "english": "to disturb", "part_of_speech": "verb", "level": "B1"},
        {"german": "anerkennen", "english": "to recognize/acknowledge", "part_of_speech": "verb", "level": "B1"},
        {"german": "erledigen", "english": "to take care of/complete (a task)", "part_of_speech": "verb", "level": "B1"},
        {"german": "beeinflussen", "english": "to influence", "part_of_speech": "verb", "level": "B1"},
        {"german": "bedauern", "english": "to regret", "part_of_speech": "verb", "level": "B1"},
        {"german": "gratulieren", "english": "to congratulate", "part_of_speech": "verb", "level": "B1"},
        {"german": "benachrichtigen", "english": "to notify", "part_of_speech": "verb", "level": "B1"},
    ]


def _verbs_b2() -> list[dict]:
    return [
        {"german": "analysieren", "english": "to analyze", "part_of_speech": "verb", "level": "B2"},
        {"german": "argumentieren", "english": "to argue/reason", "part_of_speech": "verb", "level": "B2"},
        {"german": "beurteilen", "english": "to assess/judge", "part_of_speech": "verb", "level": "B2"},
        {"german": "widersprechen", "english": "to contradict", "part_of_speech": "verb", "level": "B2"},
        {"german": "erörtern", "english": "to discuss/deliberate (formal)", "part_of_speech": "verb", "level": "B2"},
        {"german": "nachweisen", "english": "to prove/demonstrate", "part_of_speech": "verb", "level": "B2"},
        {"german": "behaupten", "english": "to claim/assert", "part_of_speech": "verb", "level": "B2"},
        {"german": "widerlegen", "english": "to refute", "part_of_speech": "verb", "level": "B2"},
        {"german": "hervorheben", "english": "to emphasize/highlight", "part_of_speech": "verb", "level": "B2"},
        {"german": "zusammenfassen", "english": "to summarize", "part_of_speech": "verb", "level": "B2"},
        {"german": "auswerten", "english": "to evaluate/analyze (data)", "part_of_speech": "verb", "level": "B2"},
        {"german": "erforschen", "english": "to research/explore", "part_of_speech": "verb", "level": "B2"},
        {"german": "einschätzen", "english": "to assess/estimate", "part_of_speech": "verb", "level": "B2"},
        {"german": "voraussetzen", "english": "to presuppose/require", "part_of_speech": "verb", "level": "B2"},
        {"german": "berücksichtigen", "english": "to consider/take into account", "part_of_speech": "verb", "level": "B2"},
        {"german": "ableiten", "english": "to derive/deduce", "part_of_speech": "verb", "level": "B2"},
        {"german": "verknüpfen", "english": "to link/connect", "part_of_speech": "verb", "level": "B2"},
        {"german": "bewältigen", "english": "to cope with/manage", "part_of_speech": "verb", "level": "B2"},
        {"german": "gewährleisten", "english": "to guarantee/ensure", "part_of_speech": "verb", "level": "B2"},
        {"german": "durchführen", "english": "to carry out/conduct", "part_of_speech": "verb", "level": "B2"},
        {"german": "beauftragen", "english": "to commission/assign", "part_of_speech": "verb", "level": "B2"},
        {"german": "betreuen", "english": "to supervise/look after", "part_of_speech": "verb", "level": "B2"},
        {"german": "beantragen", "english": "to apply for (formally)", "part_of_speech": "verb", "level": "B2"},
        {"german": "begründen", "english": "to justify/give reasons", "part_of_speech": "verb", "level": "B2"},
        {"german": "anstreben", "english": "to aspire to/strive for", "part_of_speech": "verb", "level": "B2"},
        {"german": "verfügen", "english": "to have at one's disposal", "part_of_speech": "verb", "level": "B2"},
        {"german": "beitragen", "english": "to contribute", "part_of_speech": "verb", "level": "B2"},
        {"german": "untersuchen", "english": "to examine/investigate", "part_of_speech": "verb", "level": "B2"},
        {"german": "ermitteln", "english": "to determine/investigate", "part_of_speech": "verb", "level": "B2"},
        {"german": "beeinträchtigen", "english": "to impair/affect negatively", "part_of_speech": "verb", "level": "B2"},
        {"german": "vernachlässigen", "english": "to neglect", "part_of_speech": "verb", "level": "B2"},
        {"german": "darstellen", "english": "to represent/depict", "part_of_speech": "verb", "level": "B2"},
        {"german": "überprüfen", "english": "to verify/review", "part_of_speech": "verb", "level": "B2"},
        {"german": "fördern", "english": "to promote/support", "part_of_speech": "verb", "level": "B2"},
        {"german": "hinterfragen", "english": "to question critically", "part_of_speech": "verb", "level": "B2"},
        {"german": "anwenden", "english": "to apply/use", "part_of_speech": "verb", "level": "B2"},
        {"german": "erwägen", "english": "to consider/contemplate", "part_of_speech": "verb", "level": "B2"},
        {"german": "ergänzen", "english": "to supplement/complement", "part_of_speech": "verb", "level": "B2"},
        {"german": "veranschaulichen", "english": "to illustrate/visualize", "part_of_speech": "verb", "level": "B2"},
    ]


def _verbs_c1() -> list[dict]:
    return [
        # Academic / Formal discourse
        {"german": "darlegen", "english": "to set forth/expound", "part_of_speech": "verb", "level": "C1"},
        {"german": "erläutern", "english": "to elucidate/explain in detail", "part_of_speech": "verb", "level": "C1"},
        {"german": "implizieren", "english": "to imply", "part_of_speech": "verb", "level": "C1"},
        {"german": "konstatieren", "english": "to state/establish (a fact)", "part_of_speech": "verb", "level": "C1"},
        {"german": "postulieren", "english": "to postulate", "part_of_speech": "verb", "level": "C1"},
        {"german": "deduzieren", "english": "to deduce", "part_of_speech": "verb", "level": "C1"},
        {"german": "abstrahieren", "english": "to abstract", "part_of_speech": "verb", "level": "C1"},
        {"german": "differenzieren", "english": "to differentiate", "part_of_speech": "verb", "level": "C1"},
        {"german": "konkretisieren", "english": "to make concrete/specify", "part_of_speech": "verb", "level": "C1"},
        {"german": "relativieren", "english": "to put into perspective/relativize", "part_of_speech": "verb", "level": "C1"},
        # Governance / Formal
        {"german": "ratifizieren", "english": "to ratify", "part_of_speech": "verb", "level": "C1"},
        {"german": "legitimieren", "english": "to legitimize", "part_of_speech": "verb", "level": "C1"},
        {"german": "reglementieren", "english": "to regulate strictly", "part_of_speech": "verb", "level": "C1"},
        {"german": "sanktionieren", "english": "to sanction", "part_of_speech": "verb", "level": "C1"},
        {"german": "konsolidieren", "english": "to consolidate", "part_of_speech": "verb", "level": "C1"},
        # Nuanced expression
        {"german": "anvisieren", "english": "to target/aim at", "part_of_speech": "verb", "level": "C1"},
        {"german": "gegenüberstellen", "english": "to juxtapose/compare", "part_of_speech": "verb", "level": "C1"},
        {"german": "einräumen", "english": "to concede/admit", "part_of_speech": "verb", "level": "C1"},
        {"german": "untermauern", "english": "to underpin/substantiate", "part_of_speech": "verb", "level": "C1"},
        {"german": "suggerieren", "english": "to suggest/insinuate", "part_of_speech": "verb", "level": "C1"},
        {"german": "antizipieren", "english": "to anticipate", "part_of_speech": "verb", "level": "C1"},
        {"german": "kompensieren", "english": "to compensate", "part_of_speech": "verb", "level": "C1"},
        {"german": "korrelieren", "english": "to correlate", "part_of_speech": "verb", "level": "C1"},
        {"german": "manifestieren", "english": "to manifest", "part_of_speech": "verb", "level": "C1"},
        {"german": "transformieren", "english": "to transform", "part_of_speech": "verb", "level": "C1"},
    ]


def _verbs_c2() -> list[dict]:
    return [
        # Literary / Archaic
        {"german": "frönen", "english": "to indulge in", "part_of_speech": "verb", "level": "C2"},
        {"german": "huldigen", "english": "to pay homage", "part_of_speech": "verb", "level": "C2"},
        {"german": "schmähen", "english": "to revile/vilify", "part_of_speech": "verb", "level": "C2"},
        {"german": "ersinnen", "english": "to devise/contrive", "part_of_speech": "verb", "level": "C2"},
        {"german": "erküren", "english": "to choose/elect (archaic)", "part_of_speech": "verb", "level": "C2"},
        {"german": "entsagen", "english": "to renounce/forswear", "part_of_speech": "verb", "level": "C2"},
        {"german": "obwalten", "english": "to prevail/obtain (formal)", "part_of_speech": "verb", "level": "C2"},
        {"german": "verheißen", "english": "to promise/foretell (literary)", "part_of_speech": "verb", "level": "C2"},
        {"german": "trachten", "english": "to strive/aspire (literary)", "part_of_speech": "verb", "level": "C2"},
        # Highly specialized
        {"german": "subsumieren", "english": "to subsume", "part_of_speech": "verb", "level": "C2"},
        {"german": "extrapolieren", "english": "to extrapolate", "part_of_speech": "verb", "level": "C2"},
        {"german": "dekonstruieren", "english": "to deconstruct", "part_of_speech": "verb", "level": "C2"},
        {"german": "kontextualisieren", "english": "to contextualize", "part_of_speech": "verb", "level": "C2"},
        {"german": "perpetuieren", "english": "to perpetuate", "part_of_speech": "verb", "level": "C2"},
        {"german": "amalgamieren", "english": "to amalgamate", "part_of_speech": "verb", "level": "C2"},
        {"german": "prädestinieren", "english": "to predestine", "part_of_speech": "verb", "level": "C2"},
        {"german": "transzendieren", "english": "to transcend", "part_of_speech": "verb", "level": "C2"},
        {"german": "oszillieren", "english": "to oscillate", "part_of_speech": "verb", "level": "C2"},
        {"german": "evozieren", "english": "to evoke", "part_of_speech": "verb", "level": "C2"},
    ]


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
    return [
        {"german": "gesellschaftlich", "english": "social/societal", "part_of_speech": "adjective", "level": "B1"},
        {"german": "verantwortlich", "english": "responsible", "part_of_speech": "adjective", "level": "B1"},
        {"german": "zuverlässig", "english": "reliable", "part_of_speech": "adjective", "level": "B1"},
        {"german": "selbstständig", "english": "independent/self-reliant", "part_of_speech": "adjective", "level": "B1"},
        {"german": "geduldig", "english": "patient", "part_of_speech": "adjective", "level": "B1"},
        {"german": "ungeduldig", "english": "impatient", "part_of_speech": "adjective", "level": "B1"},
        {"german": "großzügig", "english": "generous", "part_of_speech": "adjective", "level": "B1"},
        {"german": "geizig", "english": "stingy/miserly", "part_of_speech": "adjective", "level": "B1"},
        {"german": "eifersüchtig", "english": "jealous", "part_of_speech": "adjective", "level": "B1"},
        {"german": "bescheiden", "english": "modest/humble", "part_of_speech": "adjective", "level": "B1"},
        {"german": "selbstbewusst", "english": "self-confident", "part_of_speech": "adjective", "level": "B1"},
        {"german": "schüchtern", "english": "shy/timid", "part_of_speech": "adjective", "level": "B1"},
        {"german": "hartnäckig", "english": "persistent/stubborn", "part_of_speech": "adjective", "level": "B1"},
        {"german": "entschlossen", "english": "determined/resolute", "part_of_speech": "adjective", "level": "B1"},
        {"german": "vernünftig", "english": "reasonable/sensible", "part_of_speech": "adjective", "level": "B1"},
        {"german": "gerecht", "english": "fair/just", "part_of_speech": "adjective", "level": "B1"},
        {"german": "ungerecht", "english": "unfair/unjust", "part_of_speech": "adjective", "level": "B1"},
        {"german": "öffentlich", "english": "public", "part_of_speech": "adjective", "level": "B1"},
        {"german": "privat", "english": "private", "part_of_speech": "adjective", "level": "B1"},
        {"german": "politisch", "english": "political", "part_of_speech": "adjective", "level": "B1"},
        {"german": "wirtschaftlich", "english": "economic", "part_of_speech": "adjective", "level": "B1"},
        {"german": "persönlich", "english": "personal", "part_of_speech": "adjective", "level": "B1"},
        {"german": "beruflich", "english": "professional/career-related", "part_of_speech": "adjective", "level": "B1"},
        {"german": "ausgezeichnet", "english": "excellent/outstanding", "part_of_speech": "adjective", "level": "B1"},
        {"german": "angenehm", "english": "pleasant/agreeable", "part_of_speech": "adjective", "level": "B1"},
        {"german": "unangenehm", "english": "unpleasant/disagreeable", "part_of_speech": "adjective", "level": "B1"},
        {"german": "dankbar", "english": "grateful/thankful", "part_of_speech": "adjective", "level": "B1"},
        {"german": "wertvoll", "english": "valuable/precious", "part_of_speech": "adjective", "level": "B1"},
        {"german": "sinnvoll", "english": "meaningful/sensible", "part_of_speech": "adjective", "level": "B1"},
        {"german": "dringend", "english": "urgent/pressing", "part_of_speech": "adjective", "level": "B1"},
        {"german": "wesentlich", "english": "essential/substantial", "part_of_speech": "adjective", "level": "B1"},
        {"german": "grundsätzlich", "english": "fundamental/in principle", "part_of_speech": "adjective", "level": "B1"},
        {"german": "zahlreich", "english": "numerous", "part_of_speech": "adjective", "level": "B1"},
        {"german": "endgültig", "english": "final/definitive", "part_of_speech": "adjective", "level": "B1"},
        {"german": "offensichtlich", "english": "obvious/evident", "part_of_speech": "adjective", "level": "B1"},
        {"german": "üblich", "english": "usual/customary", "part_of_speech": "adjective", "level": "B1"},
        {"german": "angemessen", "english": "appropriate/adequate", "part_of_speech": "adjective", "level": "B1"},
        {"german": "unabhängig", "english": "independent", "part_of_speech": "adjective", "level": "B1"},
        {"german": "empfindlich", "english": "sensitive/delicate", "part_of_speech": "adjective", "level": "B1"},
        {"german": "geeignet", "english": "suitable/appropriate", "part_of_speech": "adjective", "level": "B1"},
    ]


def _adjectives_b2() -> list[dict]:
    return [
        {"german": "wissenschaftlich", "english": "scientific/academic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "theoretisch", "english": "theoretical", "part_of_speech": "adjective", "level": "B2"},
        {"german": "empirisch", "english": "empirical", "part_of_speech": "adjective", "level": "B2"},
        {"german": "systematisch", "english": "systematic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "analytisch", "english": "analytical", "part_of_speech": "adjective", "level": "B2"},
        {"german": "komplex", "english": "complex", "part_of_speech": "adjective", "level": "B2"},
        {"german": "abstrakt", "english": "abstract", "part_of_speech": "adjective", "level": "B2"},
        {"german": "konkret", "english": "concrete/specific", "part_of_speech": "adjective", "level": "B2"},
        {"german": "objektiv", "english": "objective", "part_of_speech": "adjective", "level": "B2"},
        {"german": "subjektiv", "english": "subjective", "part_of_speech": "adjective", "level": "B2"},
        {"german": "rational", "english": "rational", "part_of_speech": "adjective", "level": "B2"},
        {"german": "präzise", "english": "precise/exact", "part_of_speech": "adjective", "level": "B2"},
        {"german": "vage", "english": "vague/unclear", "part_of_speech": "adjective", "level": "B2"},
        {"german": "relevant", "english": "relevant", "part_of_speech": "adjective", "level": "B2"},
        {"german": "subtil", "english": "subtle", "part_of_speech": "adjective", "level": "B2"},
        {"german": "ironisch", "english": "ironic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "melancholisch", "english": "melancholic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "nostalgisch", "english": "nostalgic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "euphorisch", "english": "euphoric", "part_of_speech": "adjective", "level": "B2"},
        {"german": "verzweifelt", "english": "desperate/despairing", "part_of_speech": "adjective", "level": "B2"},
        {"german": "begeistert", "english": "enthusiastic/thrilled", "part_of_speech": "adjective", "level": "B2"},
        {"german": "enttäuscht", "english": "disappointed", "part_of_speech": "adjective", "level": "B2"},
        {"german": "überwältigt", "english": "overwhelmed", "part_of_speech": "adjective", "level": "B2"},
        {"german": "gleichgültig", "english": "indifferent/apathetic", "part_of_speech": "adjective", "level": "B2"},
        {"german": "sachlich", "english": "factual/objective", "part_of_speech": "adjective", "level": "B2"},
        {"german": "förmlich", "english": "formal/ceremonious", "part_of_speech": "adjective", "level": "B2"},
        {"german": "ausführlich", "english": "detailed/thorough", "part_of_speech": "adjective", "level": "B2"},
        {"german": "oberflächlich", "english": "superficial/shallow", "part_of_speech": "adjective", "level": "B2"},
        {"german": "nachhaltig", "english": "sustainable/lasting", "part_of_speech": "adjective", "level": "B2"},
        {"german": "umfassend", "english": "comprehensive/extensive", "part_of_speech": "adjective", "level": "B2"},
        {"german": "herausragend", "english": "outstanding/exceptional", "part_of_speech": "adjective", "level": "B2"},
        {"german": "bemerkenswert", "english": "remarkable/noteworthy", "part_of_speech": "adjective", "level": "B2"},
        {"german": "fragwürdig", "english": "questionable/dubious", "part_of_speech": "adjective", "level": "B2"},
        {"german": "bahnbrechend", "english": "groundbreaking/pioneering", "part_of_speech": "adjective", "level": "B2"},
        {"german": "wohlwollend", "english": "benevolent/well-meaning", "part_of_speech": "adjective", "level": "B2"},
    ]


def _adjectives_c1() -> list[dict]:
    return [
        # Academic / Formal
        {"german": "paradigmatisch", "english": "paradigmatic", "part_of_speech": "adjective", "level": "C1"},
        {"german": "interdisziplinär", "english": "interdisciplinary", "part_of_speech": "adjective", "level": "C1"},
        {"german": "ambivalent", "english": "ambivalent", "part_of_speech": "adjective", "level": "C1"},
        {"german": "stringent", "english": "stringent/rigorous", "part_of_speech": "adjective", "level": "C1"},
        {"german": "signifikant", "english": "significant", "part_of_speech": "adjective", "level": "C1"},
        {"german": "konträr", "english": "contrary/opposing", "part_of_speech": "adjective", "level": "C1"},
        {"german": "exemplarisch", "english": "exemplary/illustrative", "part_of_speech": "adjective", "level": "C1"},
        {"german": "inhärent", "english": "inherent", "part_of_speech": "adjective", "level": "C1"},
        {"german": "implizit", "english": "implicit", "part_of_speech": "adjective", "level": "C1"},
        {"german": "explizit", "english": "explicit", "part_of_speech": "adjective", "level": "C1"},
        # Nuanced evaluation
        {"german": "maßgeblich", "english": "authoritative/decisive", "part_of_speech": "adjective", "level": "C1"},
        {"german": "unerlässlich", "english": "indispensable", "part_of_speech": "adjective", "level": "C1"},
        {"german": "hinreichend", "english": "sufficient/adequate", "part_of_speech": "adjective", "level": "C1"},
        {"german": "zweckmäßig", "english": "expedient/purposeful", "part_of_speech": "adjective", "level": "C1"},
        {"german": "vorherrschend", "english": "predominant/prevailing", "part_of_speech": "adjective", "level": "C1"},
        {"german": "ausschlaggebend", "english": "decisive/determining", "part_of_speech": "adjective", "level": "C1"},
        {"german": "wegweisend", "english": "pioneering/trailblazing", "part_of_speech": "adjective", "level": "C1"},
        {"german": "tiefgreifend", "english": "profound/far-reaching", "part_of_speech": "adjective", "level": "C1"},
        {"german": "facettenreich", "english": "multifaceted", "part_of_speech": "adjective", "level": "C1"},
        {"german": "vielschichtig", "english": "multilayered/complex", "part_of_speech": "adjective", "level": "C1"},
        # Formal register
        {"german": "einschlägig", "english": "relevant/pertinent (legal/formal)", "part_of_speech": "adjective", "level": "C1"},
        {"german": "geläufig", "english": "familiar/fluent", "part_of_speech": "adjective", "level": "C1"},
        {"german": "verbindlich", "english": "binding/obligatory", "part_of_speech": "adjective", "level": "C1"},
        {"german": "etwaig", "english": "possible/any (formal)", "part_of_speech": "adjective", "level": "C1"},
        {"german": "hinfällig", "english": "invalid/obsolete", "part_of_speech": "adjective", "level": "C1"},
    ]


def _adjectives_c2() -> list[dict]:
    return [
        # Literary / Archaic
        {"german": "unergründlich", "english": "unfathomable/inscrutable", "part_of_speech": "adjective", "level": "C2"},
        {"german": "unnachahmlich", "english": "inimitable", "part_of_speech": "adjective", "level": "C2"},
        {"german": "unverbrüchlich", "english": "inviolable/unbreakable", "part_of_speech": "adjective", "level": "C2"},
        {"german": "unumstößlich", "english": "irrefutable/unshakeable", "part_of_speech": "adjective", "level": "C2"},
        {"german": "verwegen", "english": "audacious/daring", "part_of_speech": "adjective", "level": "C2"},
        {"german": "abgründig", "english": "abysmal/deeply dark", "part_of_speech": "adjective", "level": "C2"},
        {"german": "entrückt", "english": "enraptured/transported", "part_of_speech": "adjective", "level": "C2"},
        {"german": "unbändig", "english": "unruly/irrepressible", "part_of_speech": "adjective", "level": "C2"},
        {"german": "verzagt", "english": "despondent/fainthearted", "part_of_speech": "adjective", "level": "C2"},
        {"german": "ominös", "english": "ominous", "part_of_speech": "adjective", "level": "C2"},
        # Scholarly
        {"german": "axiomatisch", "english": "axiomatic", "part_of_speech": "adjective", "level": "C2"},
        {"german": "apodiktisch", "english": "apodictic/absolutely certain", "part_of_speech": "adjective", "level": "C2"},
        {"german": "immanent", "english": "immanent/inherent", "part_of_speech": "adjective", "level": "C2"},
        {"german": "transzendent", "english": "transcendent", "part_of_speech": "adjective", "level": "C2"},
        {"german": "ephemer", "english": "ephemeral/transient", "part_of_speech": "adjective", "level": "C2"},
        {"german": "idiosynkratisch", "english": "idiosyncratic", "part_of_speech": "adjective", "level": "C2"},
        {"german": "perniziös", "english": "pernicious", "part_of_speech": "adjective", "level": "C2"},
        {"german": "redundant", "english": "redundant/superfluous", "part_of_speech": "adjective", "level": "C2"},
        {"german": "obsolet", "english": "obsolete", "part_of_speech": "adjective", "level": "C2"},
        {"german": "kongenial", "english": "congenial/kindred in spirit", "part_of_speech": "adjective", "level": "C2"},
    ]


if __name__ == "__main__":
    main()
