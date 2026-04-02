"""Concept taxonomy for adaptive learning.

Concepts are auto-derived from exercise fields: {level}-{skill}-teil-{part}.
No manual tagging needed.
"""

SCORABLE_SKILLS = {"hoeren", "lesen"}

DIFFICULTY_MAP: dict[int, float] = {
    1: 0.3,
    2: 0.5,
    3: 0.7,
    4: 0.9,
    5: 0.9,
}

_SKILL_TEIL_DESCRIPTIONS: dict[str, dict[str, dict[int, str]]] = {
    "a1": {
        "lesen": {1: "Korrespondenz verstehen", 2: "Informationstafeln verstehen", 3: "Kleinanzeigen verstehen", 4: "Forumsbeiträge verstehen"},
        "hoeren": {1: "Kurze Alltagstexte verstehen", 2: "Kurze Gespräche verstehen", 3: "Durchsagen verstehen"},
    },
    "a2": {
        "lesen": {1: "Medientexte verstehen", 2: "Informationstafeln verstehen", 3: "Korrespondenz verstehen", 4: "Anzeigen verstehen"},
        "hoeren": {1: "Radio/Anrufbeantworter", 2: "Zusammenhängendes Gespräch", 3: "Einzelgespräche", 4: "Radiointerview"},
    },
    "b1": {
        "lesen": {1: "Blogtexte verstehen", 2: "Zeitungsmeldungen verstehen", 3: "Anzeigen/Anleitungen verstehen", 4: "Leserbriefe verstehen", 5: "Formelle Mitteilungen verstehen"},
        "hoeren": {1: "Durchsagen/Nachrichten verstehen", 2: "Vortrag verstehen", 3: "Alltagsgespräch verstehen", 4: "Diskussion verstehen"},
    },
    "b2": {
        "lesen": {1: "Sachtext global verstehen", 2: "Sachtext detailliert verstehen", 3: "Kommentare/Meinungen verstehen", 4: "Informationen zuordnen", 5: "Formelle Korrespondenz verstehen"},
        "hoeren": {1: "Alltagsgespräch verstehen", 2: "Vortrag/Interview verstehen", 3: "Diskussion verstehen", 4: "Radiobeitrag verstehen"},
    },
    "c1": {
        "lesen": {1: "Sachtext detailliert verstehen", 2: "Fachtext analysieren", 3: "Meinungen zuordnen", 4: "Sprachliche Mittel erkennen", 5: "Wissenschaftstext verstehen"},
        "hoeren": {1: "Alltagsgespräch verstehen", 2: "Experteninterview verstehen", 3: "Diskussion analysieren", 4: "Radiosendung verstehen"},
    },
    "c2": {
        "lesen": {1: "Sachtext global verstehen", 2: "Sachtext detailliert verstehen", 3: "Textvergleich", 4: "Lückentext ergänzen"},
        "hoeren": {1: "Vortrag verstehen", 2: "Expertendiskussion verstehen"},
    },
}

CONCEPT_DESCRIPTIONS: dict[str, str] = {}
for _level, _skills in _SKILL_TEIL_DESCRIPTIONS.items():
    for _skill, _teile in _skills.items():
        for _teil, _desc in _teile.items():
            CONCEPT_DESCRIPTIONS[f"{_level}-{_skill}-teil-{_teil}"] = _desc


def derive_concept_id(exercise) -> str:
    """Derive concept ID from an exercise object."""
    return f"{exercise.level.lower()}-{exercise.skill}-teil-{exercise.part}"


def get_difficulty(teil: int) -> float:
    """Get difficulty for a given Teil number."""
    return DIFFICULTY_MAP.get(teil, 0.9)


def get_concepts_for_level(level: str) -> list[str]:
    """Get all scorable concept IDs for a CEFR level."""
    level = level.lower()
    result = []
    if level in _SKILL_TEIL_DESCRIPTIONS:
        for skill in sorted(SCORABLE_SKILLS):
            if skill in _SKILL_TEIL_DESCRIPTIONS[level]:
                for teil in sorted(_SKILL_TEIL_DESCRIPTIONS[level][skill].keys()):
                    result.append(f"{level}-{skill}-teil-{teil}")
    return sorted(result)
