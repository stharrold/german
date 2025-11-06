"""Test branch protection policy compliance for workflow scripts.

This test verifies that all workflow scripts comply with the branch protection
policy:
- No scripts commit directly to 'main' (except tag operations)
- Only backmerge_release.py commits to 'develop' (documented exception)
- All other scripts respect protected branches

See WORKFLOW.md "Branch Protection Policy" for complete rules.
"""

import re
from pathlib import Path

import pytest

# Constants
SKILLS_DIR = Path(".claude/skills")
PROTECTED_BRANCHES = ["main", "develop"]

# Documented exceptions
ALLOWED_MAIN_OPERATIONS = [
    "git tag",  # Tagging is allowed (read + annotate)
    "git checkout main",  # Checking out for tagging is allowed
]

ALLOWED_DEVELOP_SCRIPTS = [
    "backmerge_release.py",  # Only script allowed to commit to develop
]


def get_all_workflow_scripts():
    """Get all Python scripts in .claude/skills/*/scripts/ directories."""
    script_files = []
    if not SKILLS_DIR.exists():
        pytest.skip(f"Skills directory not found: {SKILLS_DIR}")

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.py"):
                if script_file.name != "__init__.py":
                    script_files.append(script_file)

    return script_files


def script_commits_to_branch(script_path, branch_name):
    """Check if script contains git commands that commit to specified branch.

    Args:
        script_path: Path to Python script
        branch_name: Branch name to check ('main' or 'develop')

    Returns:
        List of line numbers where violations found (empty if compliant)
    """
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    violations = []

    # Patterns that indicate direct commits to the branch
    # Use word boundaries to avoid false positives (e.g., 'feature/main-update')
    commit_patterns = [
        rf'git\s+commit.*\b{branch_name}\b',  # git commit ... main/develop (word boundary)
        rf'git\s+push\s+(?:\S+\s+)?\b{branch_name}\b',  # git push [remote] main/develop (word boundary)
        rf'git\s+merge\s+\b{branch_name}\b',  # git merge main/develop (word boundary)
        rf'checkout\s+\b{branch_name}\b.*commit',  # checkout main ... commit (word boundary)
    ]

    # Check each line
    lines = content.split('\n')
    for i, line in enumerate(lines, start=1):
        # Skip comments
        if line.strip().startswith('#'):
            continue

        # Check for commit patterns
        # Track if violation found to avoid duplicates for same line
        violation_found = False
        for pattern in commit_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if this is an allowed operation
                if branch_name == "main" and any(
                    allowed in line for allowed in ALLOWED_MAIN_OPERATIONS
                ):
                    continue  # Allowed operation on main
                if not violation_found:
                    violations.append((i, line.strip()))
                    violation_found = True
                    break  # Stop checking other patterns for this line

    return violations


def test_no_scripts_commit_to_main():
    """Verify no scripts commit directly to main branch."""
    scripts = get_all_workflow_scripts()
    assert len(scripts) > 0, "No workflow scripts found to test"

    violations = {}
    for script in scripts:
        script_violations = script_commits_to_branch(script, "main")
        if script_violations:
            violations[script] = script_violations

    if violations:
        error_msg = ["Scripts found that commit to 'main' branch:\n"]
        for script, script_violations in violations.items():
            error_msg.append(f"\n{script.relative_to('.')}:")
            for line_num, line in script_violations:
                error_msg.append(f"  Line {line_num}: {line}")
        error_msg.append(
            "\n\nBranch protection policy: No scripts should commit to 'main'."
        )
        error_msg.append("Tagging operations are allowed (git tag, git checkout main for tagging).")
        error_msg.append("See WORKFLOW.md 'Branch Protection Policy' section.")
        pytest.fail("\n".join(error_msg))


def test_only_backmerge_commits_to_develop():
    """Verify only backmerge_release.py commits to develop branch."""
    scripts = get_all_workflow_scripts()
    assert len(scripts) > 0, "No workflow scripts found to test"

    violations = {}
    for script in scripts:
        # Skip allowed scripts
        if script.name in ALLOWED_DEVELOP_SCRIPTS:
            continue

        script_violations = script_commits_to_branch(script, "develop")
        if script_violations:
            violations[script] = script_violations

    if violations:
        error_msg = ["Scripts found that commit to 'develop' branch:\n"]
        for script, script_violations in violations.items():
            error_msg.append(f"\n{script.relative_to('.')}:")
            for line_num, line in script_violations:
                error_msg.append(f"  Line {line_num}: {line}")
        error_msg.append(
            "\n\nBranch protection policy: Only backmerge_release.py may commit to 'develop'."
        )
        error_msg.append(f"Allowed scripts: {', '.join(ALLOWED_DEVELOP_SCRIPTS)}")
        error_msg.append("See WORKFLOW.md 'Branch Protection Policy' section.")
        pytest.fail("\n".join(error_msg))


def test_backmerge_release_has_exception_warning():
    """Verify backmerge_release.py has prominent exception warning comment."""
    backmerge_script = (
        SKILLS_DIR / "git-workflow-manager" / "scripts" / "backmerge_release.py"
    )

    if not backmerge_script.exists():
        pytest.skip(f"backmerge_release.py not found: {backmerge_script}")

    with open(backmerge_script, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for exception warning in first 50 lines
    first_lines = '\n'.join(content.split('\n')[:50])

    required_phrases = [
        "BRANCH PROTECTION EXCEPTION",
        "develop",
        "protected branch",
    ]

    missing_phrases = []
    for phrase in required_phrases:
        if phrase.lower() not in first_lines.lower():
            missing_phrases.append(phrase)

    if missing_phrases:
        error_msg = (
            f"backmerge_release.py is missing required exception warning.\n"
            f"Missing phrases: {', '.join(missing_phrases)}\n"
            f"This script is the ONLY exception to branch protection policy.\n"
            f"It must have a prominent warning comment explaining why."
        )
        pytest.fail(error_msg)


def test_pre_push_hook_exists():
    """Verify pre-push hook template exists."""
    hook_path = Path(".git-hooks/pre-push")

    if not hook_path.exists():
        pytest.fail(
            f"Pre-push hook template not found: {hook_path}\n"
            f"This hook prevents accidental direct pushes to protected branches.\n"
            f"See .github/BRANCH_PROTECTION.md for installation instructions."
        )

    # Check hook is executable
    import os
    if not os.access(hook_path, os.X_OK):
        pytest.fail(
            f"Pre-push hook is not executable: {hook_path}\n"
            f"Run: chmod +x {hook_path}"
        )


def test_branch_protection_documentation_exists():
    """Verify branch protection documentation exists."""
    required_docs = [
        Path(".github/BRANCH_PROTECTION.md"),
        Path("WORKFLOW.md"),
        Path("CLAUDE.md"),
        Path("CONTRIBUTING.md"),
    ]

    missing_docs = []
    for doc_path in required_docs:
        if not doc_path.exists():
            missing_docs.append(str(doc_path))

    if missing_docs:
        pytest.fail(
            f"Missing branch protection documentation:\n"
            f"  {', '.join(missing_docs)}\n"
            f"Branch protection must be documented in multiple locations."
        )

    # Check for "Protected Branch" or "Branch Protection" in each doc
    docs_without_policy = []
    for doc_path in required_docs:
        if not doc_path.exists():
            continue
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        if "branch protection" not in content and "protected branch" not in content:
            docs_without_policy.append(str(doc_path))

    if docs_without_policy:
        pytest.fail(
            f"Documentation files missing branch protection policy:\n"
            f"  {', '.join(docs_without_policy)}\n"
            f"Each file should document protected branch rules."
        )


def test_workflow_scripts_count():
    """Verify we're testing a reasonable number of scripts."""
    scripts = get_all_workflow_scripts()

    # Should have at least 10 scripts across all skills
    assert len(scripts) >= 10, (
        f"Expected at least 10 workflow scripts, found {len(scripts)}. "
        f"This test may not be comprehensive enough."
    )


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
