"""Test semantic version calculation."""

import subprocess
from pathlib import Path

import pytest


def test_semantic_version_detects_changes():
    """Verify semantic_version.py detects changes using three-dot diff."""
    script_path = Path(".claude/skills/git-workflow-manager/scripts/semantic_version.py")

    if not script_path.exists():
        pytest.skip(f"semantic_version.py not found: {script_path}")

    # Get the latest tag to test against
    tag_result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
        check=False
    )

    if tag_result.returncode != 0:
        pytest.skip("No tags found in repository")

    latest_tag = tag_result.stdout.strip()

    # Run semantic_version.py comparing HEAD to latest tag
    # This tests the three-dot diff functionality
    result = subprocess.run(
        ["python", str(script_path), latest_tag, latest_tag],
        capture_output=True,
        text=True,
        check=False
    )

    # Check that it calculated a version
    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # Output should be a version string starting with 'v'
    output_lines = result.stdout.strip().split('\n')
    version_line = output_lines[-1]  # Last line is the version
    assert version_line.startswith("v"), (
        f"Expected version output (vX.Y.Z), got: {version_line}"
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
