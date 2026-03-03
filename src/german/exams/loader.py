"""Load exam exercises from JSON files."""

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .models import ExamMeta

T = TypeVar("T", bound=BaseModel)


class ExamLoadError(Exception):
    """Exception raised when exam exercise loading fails."""

    pass


def _resources_dir() -> Path:
    """Return the resources/exams/ directory path."""
    return Path(__file__).parent.parent.parent.parent / "resources" / "exams"


def load_exam_meta(level: str) -> ExamMeta:
    """Load exam metadata from meta.json for a given level.

    Args:
        level: CEFR level (e.g. "b1")

    Returns:
        ExamMeta object with exam configuration

    Raises:
        ExamLoadError: If metadata file not found, invalid JSON, or validation fails
    """
    meta_path = _resources_dir() / level / "meta.json"
    if not meta_path.exists():
        raise ExamLoadError(f"Exam metadata not found: {meta_path}")
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ExamMeta(**data)
    except json.JSONDecodeError as e:
        raise ExamLoadError(f"Invalid JSON in {meta_path.name}: {e}")
    except UnicodeDecodeError as e:
        raise ExamLoadError(f"Encoding error in {meta_path.name}: {e}. Must be UTF-8.")
    except ValidationError as e:
        raise ExamLoadError(f"Validation error in {meta_path.name}: {e}")


def load_exercise(path: Path, model_class: type[T]) -> T:
    """Load a single exercise from a JSON file.

    Args:
        path: Path to the JSON exercise file
        model_class: Pydantic model class to validate against

    Returns:
        Validated exercise object

    Raises:
        ExamLoadError: If file not found, invalid JSON, encoding error, or validation fails
    """
    if not path.exists():
        raise ExamLoadError(f"Exercise file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ExamLoadError(f"Invalid JSON in {path.name}: {e}")
    except UnicodeDecodeError as e:
        raise ExamLoadError(f"Encoding error in {path.name}: {e}. Must be UTF-8.")
    try:
        return model_class(**data)
    except ValidationError as e:
        raise ExamLoadError(f"Validation error in {path.name}: {e}")


def load_exercises(directory: Path, model_class: type[T]) -> list[T]:
    """Load all exercises from JSON files in a directory.

    Args:
        directory: Path to directory containing JSON exercise files
        model_class: Pydantic model class to validate against

    Returns:
        List of validated exercise objects, sorted by filename

    Raises:
        ExamLoadError: If any file has invalid JSON, encoding error, or validation fails
    """
    if not directory.exists():
        return []
    exercises: list[T] = []
    for json_file in sorted(directory.glob("*.json")):
        exercises.append(load_exercise(json_file, model_class))
    return exercises
