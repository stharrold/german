"""Tests for adaptive learning concept derivation."""

from german.adaptive.concepts import (
    CONCEPT_DESCRIPTIONS,
    DIFFICULTY_MAP,
    SCORABLE_SKILLS,
    derive_concept_id,
    get_concepts_for_level,
    get_difficulty,
)


def test_derive_concept_id_lesen():
    """Test concept ID derivation for a Lesen exercise."""
    class FakeExercise:
        level = "A2"
        skill = "lesen"
        part = 1
    assert derive_concept_id(FakeExercise()) == "a2-lesen-teil-1"


def test_derive_concept_id_hoeren():
    """Test concept ID derivation for a Hören exercise."""
    class FakeExercise:
        level = "B1"
        skill = "hoeren"
        part = 3
    assert derive_concept_id(FakeExercise()) == "b1-hoeren-teil-3"


def test_derive_concept_id_case_insensitive():
    """Test that level is lowercased."""
    class FakeExercise:
        level = "C1"
        skill = "lesen"
        part = 5
    assert derive_concept_id(FakeExercise()) == "c1-lesen-teil-5"


def test_difficulty_map_teil_order():
    """Test that difficulty increases with Teil number."""
    assert DIFFICULTY_MAP[1] < DIFFICULTY_MAP[2]
    assert DIFFICULTY_MAP[2] < DIFFICULTY_MAP[3]
    assert DIFFICULTY_MAP[3] < DIFFICULTY_MAP[4]


def test_difficulty_map_range():
    """Test all difficulties are in [0, 1]."""
    for teil, diff in DIFFICULTY_MAP.items():
        assert 0.0 <= diff <= 1.0, f"Teil {teil} difficulty {diff} out of range"


def test_get_difficulty():
    """Test get_difficulty helper."""
    assert get_difficulty(1) == 0.3
    assert get_difficulty(4) == 0.9
    assert get_difficulty(5) == 0.9


def test_scorable_skills():
    """Test that only Lesen and Hören are scorable."""
    assert SCORABLE_SKILLS == {"hoeren", "lesen"}


def test_concept_descriptions_populated():
    """Test that concept descriptions exist for common concepts."""
    assert "a2-lesen-teil-1" in CONCEPT_DESCRIPTIONS
    assert "a2-hoeren-teil-4" in CONCEPT_DESCRIPTIONS
    assert len(CONCEPT_DESCRIPTIONS) >= 48


def test_get_concepts_for_level():
    """Test getting all scorable concepts for a level."""
    a2_concepts = get_concepts_for_level("a2")
    assert "a2-lesen-teil-1" in a2_concepts
    assert "a2-hoeren-teil-4" in a2_concepts
    assert "a2-schreiben-aufgabe-1" not in a2_concepts
    assert len(a2_concepts) == 8


def test_get_concepts_for_level_b1():
    """Test B1 has 9 concepts (5 lesen + 4 hoeren)."""
    b1_concepts = get_concepts_for_level("b1")
    assert len(b1_concepts) == 9


def test_get_concepts_for_level_c2():
    """Test C2 has 6 concepts (4 lesen + 2 hoeren)."""
    c2_concepts = get_concepts_for_level("c2")
    assert len(c2_concepts) == 6
