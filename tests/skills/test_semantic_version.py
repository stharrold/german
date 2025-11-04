"""Test semantic version calculation."""

import subprocess
from pathlib import Path

import pytest


def test_semantic_version_detects_changes():
    """Verify semantic_version.py detects changes using three-dot diff."""
    script_path = Path(".claude/skills/git-workflow-manager/scripts/semantic_version.py")

    if not script_path.exists():
        pytest.skip(f"semantic_version.py not found: {script_path}")

    # Run semantic_version.py comparing current branch to develop
    # This should detect at least the changes in the current branch
    result = subprocess.run(
        ["python", str(script_path), "develop", "v1.0.0"],
        capture_output=True,
        text=True,
        check=False
    )

    # Check that it doesn't return "No changed files detected"
    assert "No changed files detected" not in result.stderr, (
        "semantic_version.py failed to detect changes. "
        "This suggests the three-dot diff (develop...HEAD) is not working correctly."
    )

    # Check that it calculated a version
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert result.stdout.strip().startswith("v"), (
        f"Expected version output (vX.Y.Z), got: {result.stdout.strip()}"
    )


def test_semantic_version_uses_three_dot_diff():
    """Verify semantic_version.py uses three-dot diff pattern."""
    script_path = Path(".claude/skills/git-workflow-manager/scripts/semantic_version.py")

    if not script_path.exists():
        pytest.skip(f"semantic_version.py not found: {script_path}")

    # Read script content and verify it uses three-dot diff
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for three-dot diff pattern: base_branch...HEAD
    assert "...head" in content.lower(), (
        "semantic_version.py should use three-dot diff (base_branch...HEAD) "
        "to compare current branch against merge-base, not working directory changes."
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
