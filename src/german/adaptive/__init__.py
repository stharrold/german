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
