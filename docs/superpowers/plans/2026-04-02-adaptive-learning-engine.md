# Adaptive Learning Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an adaptive drill engine that tracks student proficiency per exam concept, selects Lesen/Hören exercises by mastery gaps, and provides interactive CLI practice sessions.

**Architecture:** Five focused modules under `src/german/adaptive/` — concepts (taxonomy), profiler (student state), scorer (answer checking), selector (adaptive pick), cli (interactive drill). Each module has one responsibility and well-defined interfaces. Student state persists as JSON at `~/.german/profile.json`.

**Tech Stack:** Python 3.12, Pydantic (existing models), JSON stdlib, pathlib, datetime. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-04-02-adaptive-learning-engine-design.md`

---

## File Map

### New files to create
| File | Purpose |
|------|---------|
| `src/german/adaptive/__init__.py` | Public API exports |
| `src/german/adaptive/concepts.py` | `derive_concept_id()`, difficulty map, concept descriptions |
| `src/german/adaptive/profiler.py` | `StudentProfile` — load/save JSON, update proficiency |
| `src/german/adaptive/scorer.py` | `score_answer()` — check MC, true/false, matching answers |
| `src/german/adaptive/selector.py` | `AdaptiveSelector` — pick next concept + exercise |
| `src/german/adaptive/cli.py` | Interactive drill loop, progress dashboard |
| `src/german/adaptive/__main__.py` | Entry point for `python -m german.adaptive` |
| `tests/test_concepts.py` | Tests for concept derivation |
| `tests/test_profiler.py` | Tests for proficiency tracking |
| `tests/test_scorer.py` | Tests for answer scoring |
| `tests/test_selector.py` | Tests for adaptive selection |
| `tests/test_drill_integration.py` | Integration test for drill session |

### Files to modify
| File | Change |
|------|--------|
| None | This is a new module — no existing files modified |

---

## Task 1: Concepts Module

**Files:**
- Create: `src/german/adaptive/__init__.py`
- Create: `src/german/adaptive/concepts.py`
- Test: `tests/test_concepts.py`

- [ ] **Step 1: Write failing tests for concept derivation**

Create `tests/test_concepts.py`:

```python
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
    # Simulate an exercise object with level, skill, part attributes
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
    assert get_difficulty(5) == 0.9  # Teil 5 same as Teil 4


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
    assert "a2-schreiben-aufgabe-1" not in a2_concepts  # not scorable
    assert len(a2_concepts) == 8  # 4 lesen + 4 hoeren


def test_get_concepts_for_level_b1():
    """Test B1 has 9 concepts (5 lesen + 4 hoeren)."""
    b1_concepts = get_concepts_for_level("b1")
    assert len(b1_concepts) == 9


def test_get_concepts_for_level_c2():
    """Test C2 has 6 concepts (4 lesen + 2 hoeren)."""
    c2_concepts = get_concepts_for_level("c2")
    assert len(c2_concepts) == 6
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_concepts.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.adaptive'`

- [ ] **Step 3: Create the adaptive package and concepts module**

Create `src/german/adaptive/__init__.py`:

```python
"""Adaptive learning engine for German exam practice."""
```

Create `src/german/adaptive/concepts.py`:

```python
"""Concept taxonomy for adaptive learning.

Concepts are auto-derived from exercise fields: {level}-{skill}-teil-{part}.
No manual tagging needed — the exercise's level, skill, and part fields
uniquely identify the comprehension skill being tested.
"""

from pathlib import Path

SCORABLE_SKILLS = {"hoeren", "lesen"}

DIFFICULTY_MAP: dict[int, float] = {
    1: 0.3,
    2: 0.5,
    3: 0.7,
    4: 0.9,
    5: 0.9,
}

# Concept descriptions by level and skill
# Format: {concept_id: human-readable description}
CONCEPT_DESCRIPTIONS: dict[str, str] = {}

# Build concept descriptions from the actual directory structure
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

# Populate CONCEPT_DESCRIPTIONS
for level, skills in _SKILL_TEIL_DESCRIPTIONS.items():
    for skill, teile in skills.items():
        for teil, desc in teile.items():
            concept_id = f"{level}-{skill}-teil-{teil}"
            CONCEPT_DESCRIPTIONS[concept_id] = desc


def derive_concept_id(exercise) -> str:
    """Derive concept ID from an exercise object.

    Args:
        exercise: Any object with level, skill, and part attributes.

    Returns:
        Concept ID string, e.g. "a2-lesen-teil-1".
    """
    return f"{exercise.level.lower()}-{exercise.skill}-teil-{exercise.part}"


def get_difficulty(teil: int) -> float:
    """Get difficulty for a given Teil number.

    Args:
        teil: Teil number (1-5).

    Returns:
        Difficulty float in [0.0, 1.0].
    """
    return DIFFICULTY_MAP.get(teil, 0.9)


def get_concepts_for_level(level: str) -> list[str]:
    """Get all scorable concept IDs for a CEFR level.

    Args:
        level: CEFR level string, e.g. "a2".

    Returns:
        List of concept IDs for Lesen and Hören at that level.
    """
    level = level.lower()
    result = []
    if level in _SKILL_TEIL_DESCRIPTIONS:
        for skill in SCORABLE_SKILLS:
            if skill in _SKILL_TEIL_DESCRIPTIONS[level]:
                for teil in sorted(_SKILL_TEIL_DESCRIPTIONS[level][skill].keys()):
                    result.append(f"{level}-{skill}-teil-{teil}")
    return sorted(result)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_concepts.py -v`
Expected: ALL PASS (12 tests)

- [ ] **Step 5: Commit**

```bash
git add src/german/adaptive/__init__.py src/german/adaptive/concepts.py tests/test_concepts.py
git commit -m "feat(adaptive): add concept taxonomy with auto-derived IDs (#363)"
```

---

## Task 2: Profiler Module

**Files:**
- Create: `src/german/adaptive/profiler.py`
- Test: `tests/test_profiler.py`

- [ ] **Step 1: Write failing tests for StudentProfile**

Create `tests/test_profiler.py`:

```python
"""Tests for adaptive learning proficiency tracker."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from german.adaptive.profiler import StudentProfile


@pytest.fixture
def tmp_profile(tmp_path):
    """Create a temporary profile path."""
    return tmp_path / "profile.json"


def test_create_new_profile(tmp_profile):
    """Test creating a new student profile."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    assert profile.student_name == "Test"
    assert profile.concepts == {}
    assert profile.active_levels == []


def test_save_and_load_roundtrip(tmp_profile):
    """Test that save/load preserves data."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.active_levels = ["a2"]
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="a2-lesen-teil-1-001", question_number=1)
    profile.save()

    loaded = StudentProfile.load(tmp_profile)
    assert loaded.student_name == "Test"
    assert loaded.active_levels == ["a2"]
    assert "a2-lesen-teil-1" in loaded.concepts


def test_update_correct_answer(tmp_profile):
    """Test proficiency increases on correct answer."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    concept = profile.concepts["a2-lesen-teil-1"]
    # Formula: 0.0 + (1.0 - 0.0) * 0.3 * 0.3 = 0.09
    assert abs(concept["proficiency"] - 0.09) < 0.01
    assert concept["total_attempts"] == 1
    assert concept["correct_attempts"] == 1
    assert concept["mastered"] is False


def test_update_incorrect_answer(tmp_profile):
    """Test proficiency decreases on incorrect answer."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    # Set initial proficiency
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    old_prof = profile.concepts["a2-lesen-teil-1"]["proficiency"]
    profile.update("a2-lesen-teil-1", is_correct=False, difficulty=0.3, exercise_id="ex1", question_number=2)
    new_prof = profile.concepts["a2-lesen-teil-1"]["proficiency"]
    # Formula: old_prof * 0.7
    assert abs(new_prof - old_prof * 0.7) < 0.01


def test_mastery_threshold(tmp_profile):
    """Test that mastery is achieved at 0.85."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    # Manually set proficiency high
    profile.concepts["a2-lesen-teil-1"] = {
        "proficiency": 0.84,
        "total_attempts": 20,
        "correct_attempts": 18,
        "mastered": False,
        "last_attempt": datetime.now().isoformat(),
        "next_review": datetime.now().isoformat(),
        "attempt_history": [],
    }
    # One more correct answer at high difficulty should push over 0.85
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.9, exercise_id="ex1", question_number=1)
    assert profile.concepts["a2-lesen-teil-1"]["mastered"] is True


def test_proficiency_clamped(tmp_profile):
    """Test proficiency stays in [0, 1]."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    # Many correct answers
    for i in range(50):
        profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.9, exercise_id="ex1", question_number=i)
    assert profile.concepts["a2-lesen-teil-1"]["proficiency"] <= 1.0


def test_get_proficiency_unseen(tmp_profile):
    """Test that unseen concepts return 0.0."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    assert profile.get_proficiency("a2-lesen-teil-1") == 0.0


def test_get_proficiency_existing(tmp_profile):
    """Test get_proficiency for an existing concept."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    assert profile.get_proficiency("a2-lesen-teil-1") > 0.0


def test_get_priority_unseen(tmp_profile):
    """Test priority for unseen concept is high."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    priority = profile.get_priority("a2-lesen-teil-1")
    # (1 - 0) * days = 1.0 * large_number
    assert priority > 0


def test_get_priority_mastered(tmp_profile):
    """Test priority for mastered concept is low."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.concepts["a2-lesen-teil-1"] = {
        "proficiency": 0.95,
        "total_attempts": 50,
        "correct_attempts": 48,
        "mastered": True,
        "last_attempt": datetime.now().isoformat(),
        "next_review": (datetime.now() + timedelta(days=7)).isoformat(),
        "attempt_history": [],
    }
    priority = profile.get_priority("a2-lesen-teil-1")
    # (1 - 0.95) * 0 days = 0.05 * ~0 = very low
    assert priority < 0.1


def test_review_scheduling(tmp_profile):
    """Test next_review is set based on proficiency."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    concept = profile.concepts["a2-lesen-teil-1"]
    next_review = datetime.fromisoformat(concept["next_review"])
    now = datetime.now()
    # Low proficiency → review soon (1-2 days)
    assert next_review - now < timedelta(days=3)


def test_attempt_history_recorded(tmp_profile):
    """Test that attempt history is recorded."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="a2-lesen-teil-1-001", question_number=3)
    history = profile.concepts["a2-lesen-teil-1"]["attempt_history"]
    assert len(history) == 1
    assert history[0]["exercise_id"] == "a2-lesen-teil-1-001"
    assert history[0]["question"] == 3
    assert history[0]["is_correct"] is True
    assert "old_proficiency" in history[0]
    assert "new_proficiency" in history[0]


def test_get_stats(tmp_profile):
    """Test stats summary."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    profile.update("a2-lesen-teil-1", is_correct=False, difficulty=0.3, exercise_id="ex1", question_number=2)
    stats = profile.get_stats()
    assert stats["total_attempts"] == 2
    assert stats["total_correct"] == 1
    assert stats["accuracy"] == 0.5
    assert stats["concepts_studied"] == 1
    assert stats["concepts_mastered"] == 0


def test_json_format(tmp_profile):
    """Test JSON is properly formatted (UTF-8, indented, trailing newline)."""
    profile = StudentProfile.load(tmp_profile, student_name="Test")
    profile.update("a2-lesen-teil-1", is_correct=True, difficulty=0.3, exercise_id="ex1", question_number=1)
    profile.save()
    content = tmp_profile.read_text(encoding="utf-8")
    assert content.endswith("\n")
    # Verify it's valid JSON
    data = json.loads(content)
    assert data["student_name"] == "Test"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_profiler.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.adaptive.profiler'`

- [ ] **Step 3: Implement StudentProfile**

Create `src/german/adaptive/profiler.py`:

```python
"""Student proficiency tracker for adaptive learning.

Tracks per-concept mastery scores using gain/decay formulas adapted
from the chimeu ConceptProfiler. Persists state as JSON.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


class StudentProfile:
    """Tracks student proficiency across exam concepts."""

    MASTERY_THRESHOLD = 0.85
    GAIN_MULTIPLIER = 0.3
    DECAY_MULTIPLIER = 0.7

    def __init__(self, path: Path, student_name: str, active_levels: list[str], concepts: dict, created: str, last_session: str | None):
        self._path = path
        self.student_name = student_name
        self.active_levels = active_levels
        self.concepts = concepts
        self.created = created
        self.last_session = last_session

    @classmethod
    def load(cls, path: Path, student_name: str = "Student") -> "StudentProfile":
        """Load profile from JSON file, or create new if not found."""
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls(
                path=path,
                student_name=data.get("student_name", student_name),
                active_levels=data.get("active_levels", []),
                concepts=data.get("concepts", {}),
                created=data.get("created", datetime.now().isoformat()),
                last_session=data.get("last_session"),
            )
        return cls(
            path=path,
            student_name=student_name,
            active_levels=[],
            concepts={},
            created=datetime.now().isoformat(),
            last_session=None,
        )

    def save(self) -> None:
        """Save profile to JSON file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "student_name": self.student_name,
            "active_levels": self.active_levels,
            "created": self.created,
            "last_session": self.last_session,
            "concepts": self.concepts,
        }
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    def update(self, concept_id: str, is_correct: bool, difficulty: float, exercise_id: str, question_number: int) -> None:
        """Update proficiency for a concept based on answer correctness."""
        now = datetime.now()

        if concept_id not in self.concepts:
            self.concepts[concept_id] = {
                "proficiency": 0.0,
                "total_attempts": 0,
                "correct_attempts": 0,
                "mastered": False,
                "last_attempt": None,
                "next_review": None,
                "attempt_history": [],
            }

        concept = self.concepts[concept_id]
        old_proficiency = concept["proficiency"]

        if is_correct:
            concept["proficiency"] += (1.0 - concept["proficiency"]) * difficulty * self.GAIN_MULTIPLIER
            concept["correct_attempts"] += 1
        else:
            concept["proficiency"] *= self.DECAY_MULTIPLIER

        # Clamp to [0, 1]
        concept["proficiency"] = max(0.0, min(1.0, concept["proficiency"]))

        concept["total_attempts"] += 1
        concept["mastered"] = concept["proficiency"] >= self.MASTERY_THRESHOLD
        concept["last_attempt"] = now.isoformat()

        # Review scheduling: 1 + (proficiency * 6) days
        review_days = 1 + (concept["proficiency"] * 6)
        concept["next_review"] = (now + timedelta(days=review_days)).isoformat()

        concept["attempt_history"].append({
            "timestamp": now.isoformat(),
            "exercise_id": exercise_id,
            "question": question_number,
            "is_correct": is_correct,
            "old_proficiency": round(old_proficiency, 4),
            "new_proficiency": round(concept["proficiency"], 4),
        })

        self.last_session = now.isoformat()

    def get_proficiency(self, concept_id: str) -> float:
        """Get proficiency for a concept. Returns 0.0 if unseen."""
        if concept_id not in self.concepts:
            return 0.0
        return self.concepts[concept_id]["proficiency"]

    def get_priority(self, concept_id: str) -> float:
        """Get review priority for a concept. Higher = needs more review."""
        proficiency = self.get_proficiency(concept_id)
        if concept_id not in self.concepts or self.concepts[concept_id]["last_attempt"] is None:
            # Never attempted — high priority
            return (1.0 - proficiency) * 30.0
        last = datetime.fromisoformat(self.concepts[concept_id]["last_attempt"])
        days_since = max(0.0, (datetime.now() - last).total_seconds() / 86400)
        return (1.0 - proficiency) * days_since

    def get_stats(self) -> dict:
        """Get summary statistics."""
        total_attempts = sum(c["total_attempts"] for c in self.concepts.values())
        total_correct = sum(c["correct_attempts"] for c in self.concepts.values())
        return {
            "total_attempts": total_attempts,
            "total_correct": total_correct,
            "accuracy": total_correct / total_attempts if total_attempts > 0 else 0.0,
            "concepts_studied": len(self.concepts),
            "concepts_mastered": sum(1 for c in self.concepts.values() if c["mastered"]),
        }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_profiler.py -v`
Expected: ALL PASS (14 tests)

- [ ] **Step 5: Commit**

```bash
git add src/german/adaptive/profiler.py tests/test_profiler.py
git commit -m "feat(adaptive): add StudentProfile with gain/decay proficiency tracking (#363)"
```

---

## Task 3: Scorer Module

**Files:**
- Create: `src/german/adaptive/scorer.py`
- Test: `tests/test_scorer.py`

- [ ] **Step 1: Write failing tests for answer scoring**

Create `tests/test_scorer.py`:

```python
"""Tests for adaptive learning answer scorer."""

from german.adaptive.scorer import ScoreResult, score_answer
from german.exams.models import Question, QuestionType


def _make_mc_question(correct: str = "b") -> Question:
    return Question(
        number=1,
        type=QuestionType.MULTIPLE_CHOICE,
        text_de="Was ist richtig?",
        correct_answer=correct,
        options=["a) Ja", "b) Nein", "c) Vielleicht"],
        explanation_de="Erklärung",
        explanation_en="Explanation",
    )


def _make_tf_question(correct: bool = True) -> Question:
    return Question(
        number=1,
        type=QuestionType.TRUE_FALSE,
        text_de="Sarah ist in Afrika geboren.",
        correct_answer=correct,
    )


def _make_matching_question(correct: str = "c") -> Question:
    return Question(
        number=6,
        type=QuestionType.MATCHING,
        text_de="Sie möchten Rosen schenken.",
        correct_answer=correct,
        options=["a", "b", "c"],
    )


def test_score_mc_correct():
    """Test correct multiple choice answer."""
    result = score_answer(_make_mc_question("b"), "b")
    assert result.is_correct is True
    assert result.correct_answer == "b"


def test_score_mc_incorrect():
    """Test incorrect multiple choice answer."""
    result = score_answer(_make_mc_question("b"), "a")
    assert result.is_correct is False
    assert result.correct_answer == "b"


def test_score_mc_case_insensitive():
    """Test MC scoring is case insensitive."""
    result = score_answer(_make_mc_question("b"), "B")
    assert result.is_correct is True


def test_score_mc_whitespace():
    """Test MC scoring strips whitespace."""
    result = score_answer(_make_mc_question("b"), " b ")
    assert result.is_correct is True


def test_score_tf_correct_ja():
    """Test true/false correct with 'ja'."""
    result = score_answer(_make_tf_question(True), "ja")
    assert result.is_correct is True


def test_score_tf_correct_nein():
    """Test true/false correct with 'nein'."""
    result = score_answer(_make_tf_question(False), "nein")
    assert result.is_correct is True


def test_score_tf_incorrect():
    """Test true/false incorrect."""
    result = score_answer(_make_tf_question(True), "nein")
    assert result.is_correct is False


def test_score_tf_richtig_falsch():
    """Test true/false with richtig/falsch."""
    assert score_answer(_make_tf_question(True), "richtig").is_correct is True
    assert score_answer(_make_tf_question(False), "falsch").is_correct is True


def test_score_matching_correct():
    """Test correct matching answer."""
    result = score_answer(_make_matching_question("c"), "c")
    assert result.is_correct is True


def test_score_matching_incorrect():
    """Test incorrect matching answer."""
    result = score_answer(_make_matching_question("c"), "a")
    assert result.is_correct is False


def test_score_matching_x():
    """Test matching with 'x' (keine Lösung)."""
    q = _make_matching_question("x")
    result = score_answer(q, "x")
    assert result.is_correct is True


def test_score_result_has_explanation():
    """Test ScoreResult includes explanation when available."""
    result = score_answer(_make_mc_question("b"), "a")
    assert result.explanation_de == "Erklärung"
    assert result.explanation_en == "Explanation"


def test_score_result_no_explanation():
    """Test ScoreResult handles missing explanation."""
    q = Question(number=1, type=QuestionType.MULTIPLE_CHOICE, text_de="?", correct_answer="a", options=["a", "b"])
    result = score_answer(q, "b")
    assert result.explanation_de is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_scorer.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'german.adaptive.scorer'`

- [ ] **Step 3: Implement scorer**

Create `src/german/adaptive/scorer.py`:

```python
"""Answer scorer for adaptive learning.

Scores student answers against correct answers for multiple choice,
true/false, and matching question types.
"""

from dataclasses import dataclass

from german.exams.models import Question, QuestionType


@dataclass
class ScoreResult:
    """Result of scoring a student's answer."""

    is_correct: bool
    correct_answer: str
    explanation_de: str | None = None
    explanation_en: str | None = None


def score_answer(question: Question, user_answer: str) -> ScoreResult:
    """Score a student's answer against the correct answer.

    Args:
        question: The exam question with correct_answer.
        user_answer: The student's answer string.

    Returns:
        ScoreResult with correctness and explanation.
    """
    user_clean = user_answer.strip().lower()

    if question.type == QuestionType.TRUE_FALSE:
        # Accept ja/nein, true/false, richtig/falsch
        user_bool = user_clean in ("ja", "true", "richtig")
        correct_bool = question.correct_answer if isinstance(question.correct_answer, bool) else str(question.correct_answer).lower() in ("ja", "true", "richtig")
        is_correct = user_bool == correct_bool
        correct_display = "Ja" if correct_bool else "Nein"
    else:
        # Multiple choice and matching — direct string comparison
        correct_clean = str(question.correct_answer).strip().lower()
        is_correct = user_clean == correct_clean
        correct_display = str(question.correct_answer)

    return ScoreResult(
        is_correct=is_correct,
        correct_answer=correct_display,
        explanation_de=getattr(question, "explanation_de", None),
        explanation_en=getattr(question, "explanation_en", None),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_scorer.py -v`
Expected: ALL PASS (14 tests)

- [ ] **Step 5: Commit**

```bash
git add src/german/adaptive/scorer.py tests/test_scorer.py
git commit -m "feat(adaptive): add answer scorer for MC, true/false, matching (#363)"
```

---

## Task 4: Selector Module

**Files:**
- Create: `src/german/adaptive/selector.py`
- Test: `tests/test_selector.py`

- [ ] **Step 1: Write failing tests for AdaptiveSelector**

Create `tests/test_selector.py`:

```python
"""Tests for adaptive exercise selector."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from german.adaptive.selector import AdaptiveSelector
from german.adaptive.profiler import StudentProfile


@pytest.fixture
def tmp_profile(tmp_path):
    """Create a temporary profile."""
    path = tmp_path / "profile.json"
    profile = StudentProfile.load(path, student_name="Test")
    profile.active_levels = ["a2"]
    return profile


def test_pick_next_cold_start(tmp_profile):
    """Test that cold start returns first concept in order."""
    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    exercise, concept_id = result
    # Cold start should pick first concept (alphabetically: hoeren before lesen)
    assert concept_id in ["a2-hoeren-teil-1", "a2-lesen-teil-1"]


def test_pick_next_returns_exercise(tmp_profile):
    """Test that pick_next returns a valid exercise."""
    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    exercise, concept_id = result
    assert hasattr(exercise, "questions")
    assert hasattr(exercise, "id")


def test_pick_next_prioritizes_weak_concepts(tmp_profile):
    """Test that weak concepts get higher priority."""
    # Mark most concepts as mastered
    for teil in range(1, 5):
        for skill in ["lesen", "hoeren"]:
            cid = f"a2-{skill}-teil-{teil}"
            tmp_profile.concepts[cid] = {
                "proficiency": 0.95,
                "total_attempts": 50,
                "correct_attempts": 48,
                "mastered": True,
                "last_attempt": datetime.now().isoformat(),
                "next_review": (datetime.now() + timedelta(days=7)).isoformat(),
                "attempt_history": [],
            }
    # Leave one concept weak
    tmp_profile.concepts["a2-lesen-teil-3"]["proficiency"] = 0.2
    tmp_profile.concepts["a2-lesen-teil-3"]["mastered"] = False

    selector = AdaptiveSelector(tmp_profile, "a2")
    result = selector.pick_next()
    assert result is not None
    _, concept_id = result
    assert concept_id == "a2-lesen-teil-3"


def test_pick_next_none_when_no_exercises(tmp_profile):
    """Test that pick_next returns None for invalid level."""
    selector = AdaptiveSelector(tmp_profile, "z9")
    result = selector.pick_next()
    assert result is None


def test_get_concept_order(tmp_profile):
    """Test cold-start concept ordering."""
    selector = AdaptiveSelector(tmp_profile, "a2")
    order = selector.get_concept_order()
    assert len(order) == 8  # 4 lesen + 4 hoeren
    # All should be a2 concepts
    for cid in order:
        assert cid.startswith("a2-")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_selector.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement AdaptiveSelector**

Create `src/german/adaptive/selector.py`:

```python
"""Adaptive exercise selector.

Picks the next exercise based on student proficiency gaps,
prioritizing concepts that need the most review.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from german.exams.loader import load_exercises
from german.exams.models import ListeningExercise, ReadingExercise

from .concepts import SCORABLE_SKILLS, get_concepts_for_level
from .profiler import StudentProfile

Exercise = Union[ListeningExercise, ReadingExercise]


class AdaptiveSelector:
    """Selects exercises adaptively based on student proficiency."""

    def __init__(self, profile: StudentProfile, level: str):
        self._profile = profile
        self._level = level.lower()
        self._exercises: dict[str, list[Exercise]] = {}
        self._load_exercises()

    def _load_exercises(self) -> None:
        """Load all scorable exercises for the level."""
        resources_dir = Path(__file__).parent.parent.parent.parent / "resources" / "exams" / self._level
        if not resources_dir.exists():
            return

        for skill in SCORABLE_SKILLS:
            skill_dir = resources_dir / skill
            if not skill_dir.exists():
                continue
            model_class = ListeningExercise if skill == "hoeren" else ReadingExercise
            for teil_dir in sorted(skill_dir.iterdir()):
                if not teil_dir.is_dir() or not teil_dir.name.startswith("teil-"):
                    continue
                teil_num = int(teil_dir.name.split("-")[1])
                concept_id = f"{self._level}-{skill}-teil-{teil_num}"
                exercises = load_exercises(teil_dir, model_class)
                if exercises:
                    self._exercises[concept_id] = exercises

    def pick_next(self) -> tuple[Exercise, str] | None:
        """Pick the next exercise based on proficiency gaps.

        Returns:
            Tuple of (exercise, concept_id) or None if no exercises available.
        """
        concepts = self.get_concept_order()
        if not concepts:
            return None

        # Sort by priority (highest first)
        concepts_with_priority = [
            (cid, self._profile.get_priority(cid))
            for cid in concepts
            if cid in self._exercises
        ]
        if not concepts_with_priority:
            return None

        concepts_with_priority.sort(key=lambda x: x[1], reverse=True)
        selected_concept = concepts_with_priority[0][0]

        # Pick exercise within concept
        exercises = self._exercises[selected_concept]
        exercise = self._pick_exercise(selected_concept, exercises)
        return exercise, selected_concept

    def _pick_exercise(self, concept_id: str, exercises: list[Exercise]) -> Exercise:
        """Pick an exercise, avoiding recently attempted ones."""
        now = datetime.now()
        cutoff = now - timedelta(hours=24)

        # Get recently attempted exercise IDs
        recent_ids = set()
        if concept_id in self._profile.concepts:
            for attempt in self._profile.concepts[concept_id].get("attempt_history", []):
                attempt_time = datetime.fromisoformat(attempt["timestamp"])
                if attempt_time > cutoff:
                    recent_ids.add(attempt["exercise_id"])

        # Filter out recent exercises
        available = [ex for ex in exercises if ex.id not in recent_ids]
        if not available:
            # All attempted recently — pick least recent
            available = exercises

        return random.choice(available)

    def get_concept_order(self) -> list[str]:
        """Get ordered list of concepts for the level."""
        return get_concepts_for_level(self._level)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_selector.py -v`
Expected: ALL PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add src/german/adaptive/selector.py tests/test_selector.py
git commit -m "feat(adaptive): add priority-based exercise selector (#363)"
```

---

## Task 5: CLI Drill Session

**Files:**
- Create: `src/german/adaptive/cli.py`
- Create: `src/german/adaptive/__main__.py`
- Test: `tests/test_drill_integration.py`

- [ ] **Step 1: Write failing integration test**

Create `tests/test_drill_integration.py`:

```python
"""Integration tests for adaptive drill CLI."""

from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from german.adaptive.cli import DrillSession


@pytest.fixture
def tmp_profile_path(tmp_path):
    return tmp_path / "profile.json"


def test_drill_session_creates_profile(tmp_profile_path):
    """Test that DrillSession creates a profile on first run."""
    session = DrillSession(level="a2", num_questions=1, profile_path=tmp_profile_path)
    assert session.profile.student_name is not None
    assert session.profile.active_levels == ["a2"]


def test_drill_session_selects_exercise(tmp_profile_path):
    """Test that DrillSession can select an exercise."""
    session = DrillSession(level="a2", num_questions=1, profile_path=tmp_profile_path)
    result = session.selector.pick_next()
    assert result is not None


def test_drill_session_run_with_input(tmp_profile_path):
    """Test running a 2-question drill session with simulated input."""
    session = DrillSession(level="a2", num_questions=2, profile_path=tmp_profile_path)
    # Simulate user answering "b" for every question, then "n" to not continue
    answers = "b\n" * 20 + "n\n"  # Enough answers for any exercise
    with patch("builtins.input", side_effect=answers.split("\n")):
        with patch("sys.stdout", new_callable=StringIO):
            try:
                session.run()
            except (StopIteration, EOFError):
                pass  # Expected when input runs out

    # Profile should have been updated
    assert session.profile.get_stats()["total_attempts"] > 0


def test_drill_session_stats(tmp_profile_path):
    """Test stats display doesn't crash."""
    session = DrillSession(level="a2", num_questions=0, profile_path=tmp_profile_path)
    # Just verify show_stats doesn't raise
    output = StringIO()
    with patch("sys.stdout", output):
        session.show_stats()
    assert "A2" in output.getvalue() or "a2" in output.getvalue()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_drill_integration.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement CLI drill session**

Create `src/german/adaptive/cli.py`:

```python
"""Interactive CLI drill session for adaptive German exam practice.

Usage:
    uv run python -m german.adaptive --level a2 --questions 10
    uv run python -m german.adaptive --stats
    uv run python -m german.adaptive --reset
"""

import sys
from datetime import datetime
from pathlib import Path

from german.exams.models import ListeningExercise, ReadingExercise

from .concepts import CONCEPT_DESCRIPTIONS, get_concepts_for_level, get_difficulty
from .profiler import StudentProfile
from .scorer import score_answer
from .selector import AdaptiveSelector

DEFAULT_PROFILE_PATH = Path.home() / ".german" / "profile.json"


class DrillSession:
    """Interactive adaptive drill session."""

    def __init__(self, level: str, num_questions: int = 10, profile_path: Path = DEFAULT_PROFILE_PATH):
        self.level = level.lower()
        self.num_questions = num_questions
        self.profile = StudentProfile.load(profile_path, student_name="Student")
        if self.level not in self.profile.active_levels:
            self.profile.active_levels.append(self.level)
        self.selector = AdaptiveSelector(self.profile, self.level)
        self._questions_answered = 0
        self._session_correct = 0

    def run(self) -> None:
        """Run the interactive drill session."""
        print(f"\n=== German Adaptive Drill — {self.level.upper()} ===")
        stats = self.profile.get_stats()
        concepts = get_concepts_for_level(self.level)
        mastered = sum(
            1 for c in concepts
            if c in self.profile.concepts and self.profile.concepts[c].get("mastered", False)
        )
        print(f"Student: {self.profile.student_name} | Mastered: {mastered}/{len(concepts)} concepts | Session: 0/{self.num_questions}\n")

        while self._questions_answered < self.num_questions:
            result = self.selector.pick_next()
            if result is None:
                print("No exercises available for this level.")
                break

            exercise, concept_id = result
            self._run_exercise(exercise, concept_id)

            if self._questions_answered >= self.num_questions:
                break

            try:
                cont = input("\nContinue? [Y/n]: ").strip().lower()
                if cont == "n":
                    break
            except (EOFError, KeyboardInterrupt):
                break

        self._show_session_summary()
        self.profile.save()

    def _run_exercise(self, exercise, concept_id: str) -> None:
        """Run a single exercise — present all questions."""
        desc = CONCEPT_DESCRIPTIONS.get(concept_id, concept_id)
        prof = self.profile.get_proficiency(concept_id)
        bar = self._proficiency_bar(prof)
        priority = "HIGH" if prof < 0.5 else "MED" if prof < 0.85 else "LOW"

        print(f"\n{'─' * 50}")
        teil_num = int(concept_id.split("-")[-1])
        skill_name = "Lesen" if "lesen" in concept_id else "Hören"
        print(f"{skill_name} Teil {teil_num}: {desc}")
        print(f"[Proficiency: {prof:.2f} {bar} | Priority: {priority}]")
        print()

        # Show passage or transcript context
        if isinstance(exercise, ReadingExercise):
            print(exercise.instructions)
            print()
            print(exercise.passage.text_de)
            print()
        elif isinstance(exercise, ListeningExercise):
            print(exercise.instructions)
            print()
            print("[Transcript]")
            for line in exercise.transcript:
                print(f"  {line.speaker}: {line.text_de}")
            print()

        difficulty = get_difficulty(teil_num)

        for i, question in enumerate(exercise.questions):
            if self._questions_answered >= self.num_questions:
                break

            print(f"Frage {i + 1}/{len(exercise.questions)}: {question.text_de}")
            if question.options:
                for opt in question.options:
                    print(f"  {opt}")

            try:
                user_answer = input("\nYour answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_answer:
                continue

            result = score_answer(question, user_answer)
            self.profile.update(concept_id, result.is_correct, difficulty, exercise.id, question.number)

            self._questions_answered += 1
            if result.is_correct:
                self._session_correct += 1
                new_prof = self.profile.get_proficiency(concept_id)
                print(f"✓ Richtig! ({prof:.2f} → {new_prof:.2f})")
            else:
                new_prof = self.profile.get_proficiency(concept_id)
                print(f"✗ Falsch. Richtige Antwort: {result.correct_answer} ({prof:.2f} → {new_prof:.2f})")

            if result.explanation_de:
                print(f"  {result.explanation_de}")

            prof = new_prof
            print()

    def _show_session_summary(self) -> None:
        """Show end-of-session summary."""
        print(f"\n{'═' * 50}")
        print(f"Session complete: {self._session_correct}/{self._questions_answered} correct")
        if self._questions_answered > 0:
            print(f"Accuracy: {self._session_correct / self._questions_answered:.0%}")
        print()

    def show_stats(self) -> None:
        """Show progress dashboard."""
        concepts = get_concepts_for_level(self.level)
        print(f"\n=== {self.level.upper()} Progress ===")
        print(f"{'Concept':<30} {'Prof.':>6} {'Mastered':>8}  {'Last':<12} {'Next Review':<12}")
        print("─" * 75)

        for cid in concepts:
            desc = CONCEPT_DESCRIPTIONS.get(cid, cid)
            short_desc = desc[:25] if len(desc) > 25 else desc

            teil = cid.split("-")[-1]
            skill = "Lesen" if "lesen" in cid else "Hören"
            label = f"{skill} Teil {teil} ({short_desc})"

            if cid in self.profile.concepts:
                c = self.profile.concepts[cid]
                prof = c["proficiency"]
                mastered = "✓" if c["mastered"] else "·"
                last = self._format_relative_date(c.get("last_attempt"))
                next_rev = self._format_date(c.get("next_review"))
                overdue = ""
                if c.get("next_review"):
                    if datetime.fromisoformat(c["next_review"]) < datetime.now():
                        next_rev += " !"
            else:
                prof = 0.0
                mastered = "·"
                last = "never"
                next_rev = "—"

            print(f"{label:<30} {prof:>5.2f} {mastered:>8}  {last:<12} {next_rev:<12}")

        stats = self.profile.get_stats()
        print()
        total_mastered = sum(
            1 for c in concepts
            if c in self.profile.concepts and self.profile.concepts[c].get("mastered", False)
        )
        print(f"Overall: {total_mastered}/{len(concepts)} mastered | {stats['total_attempts']} questions answered | {stats['accuracy']:.0%} accuracy")

    @staticmethod
    def _proficiency_bar(prof: float, width: int = 10) -> str:
        filled = int(prof * width)
        return "▓" * filled + "░" * (width - filled)

    @staticmethod
    def _format_relative_date(iso_str: str | None) -> str:
        if not iso_str:
            return "never"
        dt = datetime.fromisoformat(iso_str)
        days = (datetime.now() - dt).days
        if days == 0:
            return "today"
        elif days == 1:
            return "yesterday"
        else:
            return f"{days}d ago"

    @staticmethod
    def _format_date(iso_str: str | None) -> str:
        if not iso_str:
            return "—"
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%b %d")


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="German Adaptive Drill")
    parser.add_argument("--level", choices=["a1", "a2", "b1", "b2", "c1", "c2"], help="CEFR level to drill")
    parser.add_argument("--questions", type=int, default=10, help="Questions per session (default: 10)")
    parser.add_argument("--stats", action="store_true", help="Show progress dashboard")
    parser.add_argument("--reset", action="store_true", help="Reset profile")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE_PATH, help="Profile path")
    args = parser.parse_args()

    if args.reset:
        if args.profile.exists():
            args.profile.unlink()
            print("Profile reset.")
        else:
            print("No profile to reset.")
        return

    if args.stats:
        if not args.level:
            # Try to get level from existing profile
            if args.profile.exists():
                profile = StudentProfile.load(args.profile)
                if profile.active_levels:
                    args.level = profile.active_levels[0]
                else:
                    print("No active level. Use --level to set one.")
                    sys.exit(1)
            else:
                print("No profile found. Start a drill session first.")
                sys.exit(1)
        session = DrillSession(level=args.level, num_questions=0, profile_path=args.profile)
        session.show_stats()
        return

    if not args.level:
        # Try existing profile
        if args.profile.exists():
            profile = StudentProfile.load(args.profile)
            if profile.active_levels:
                args.level = profile.active_levels[0]
                print(f"Continuing with level {args.level.upper()}")
            else:
                print("No active level. Use --level to set one.")
                sys.exit(1)
        else:
            print("First run — use --level to set your CEFR level (e.g., --level a2)")
            sys.exit(1)

    session = DrillSession(level=args.level, num_questions=args.questions, profile_path=args.profile)
    session.run()
```

Create `src/german/adaptive/__main__.py`:

```python
"""Entry point for python -m german.adaptive."""

from .cli import main

main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_drill_integration.py -v`
Expected: ALL PASS (4 tests)

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS — no regressions

- [ ] **Step 6: Manual smoke test**

```bash
uv run python -m german.adaptive --level a2 --questions 2
```

Answer 2 questions, verify proficiency updates, then:

```bash
uv run python -m german.adaptive --stats
```

Verify the dashboard shows the concept you just practiced.

- [ ] **Step 7: Commit**

```bash
git add src/german/adaptive/cli.py src/german/adaptive/__main__.py tests/test_drill_integration.py
git commit -m "feat(adaptive): add CLI drill session with progress dashboard (#363)"
```

---

## Task 6: Package Exports and Final Integration

**Files:**
- Modify: `src/german/adaptive/__init__.py`
- Test: verify full suite

- [ ] **Step 1: Update __init__.py with public API**

Update `src/german/adaptive/__init__.py`:

```python
"""Adaptive learning engine for German exam practice."""

from .cli import DrillSession
from .concepts import (
    CONCEPT_DESCRIPTIONS,
    DIFFICULTY_MAP,
    SCORABLE_SKILLS,
    derive_concept_id,
    get_concepts_for_level,
    get_difficulty,
)
from .profiler import StudentProfile
from .scorer import ScoreResult, score_answer
from .selector import AdaptiveSelector

__all__ = [
    "AdaptiveSelector",
    "CONCEPT_DESCRIPTIONS",
    "DIFFICULTY_MAP",
    "DrillSession",
    "SCORABLE_SKILLS",
    "ScoreResult",
    "StudentProfile",
    "derive_concept_id",
    "get_concepts_for_level",
    "get_difficulty",
    "score_answer",
]
```

- [ ] **Step 2: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 3: Run ruff**

Run: `uv run ruff check src/german/adaptive/ tests/test_concepts.py tests/test_profiler.py tests/test_scorer.py tests/test_selector.py tests/test_drill_integration.py`
Expected: Clean

- [ ] **Step 4: Commit**

```bash
git add src/german/adaptive/__init__.py
git commit -m "feat(adaptive): add public API exports (#363)"
```

---

## Task 7: Version Bump and Finalize

**Files:**
- Modify: `pyproject.toml`
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Bump version to v2.10.0**

In `pyproject.toml`, change `version = "2.9.0"` to `version = "2.10.0"`.

- [ ] **Step 2: Update CHANGELOG.md**

Add entry at top:

```markdown
## [2.10.0] - 2026-04-02

### Added
- **Adaptive learning engine** ([#363](https://github.com/stharrold/german/issues/363))
  - Proficiency tracking per exam concept with gain/decay formulas
  - Priority-based exercise selection for Lesen and Hören
  - Interactive CLI drill: `uv run python -m german.adaptive --level a2`
  - Progress dashboard: `uv run python -m german.adaptive --stats`
  - Student state persisted at `~/.german/profile.json`
  - 48 auto-derived concepts across all CEFR levels (A1–C2)
```

- [ ] **Step 3: Update CLAUDE.md status**

Add to the status section:
```
- Adaptive learning engine: complete (#363), v2.10.0
- 48 exam concepts (Lesen + Hören), proficiency tracking, CLI drill
```

- [ ] **Step 4: Commit and update uv.lock**

```bash
uv run python -c "pass"
git add pyproject.toml uv.lock CHANGELOG.md CLAUDE.md
git commit -m "chore: bump version to v2.10.0, update CHANGELOG and CLAUDE.md (#363)"
```

- [ ] **Step 5: Final full test run**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

---

## Dependencies Between Tasks

```
Task 1 (concepts)   ──→  Task 2 (profiler)  ──→  Task 4 (selector)  ──→  Task 5 (cli)
                                                                           ↑
Task 3 (scorer)    ────────────────────────────────────────────────────────┘
Task 5 (cli)       ──→  Task 6 (exports)   ──→  Task 7 (version bump)
```

**Parallelizable:** Tasks 2 + 3 (profiler and scorer are independent)
