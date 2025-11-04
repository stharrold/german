#!/usr/bin/env python3
# ============================================================================
# ⚠️  BRANCH PROTECTION EXCEPTION
# ============================================================================
# WARNING: This script commits directly to the 'develop' branch, which is
#          normally a protected branch that requires pull requests.
#
# This is the ONLY documented exception to the branch protection policy.
#
# Why this exception is safe:
#   - Only merges from release branch (no code changes, just merge commit)
#   - Release branch was already reviewed and tagged on main
#   - Maintains develop's stability (inherits tested release code)
#   - Creates merge commit only (preserves history)
#   - Part of documented Phase 5.6 workflow (WORKFLOW.md)
#
# See WORKFLOW.md "Branch Protection Policy" section for complete rules.
# ============================================================================

"""Merge release branch back to develop after main merge.

This script implements Step 5.6 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It merges the release branch back into develop to ensure all
release changes are integrated into the development branch.

Usage:
    python backmerge_release.py <version> <target_branch>

Example:
    python backmerge_release.py v1.1.0 develop

Requirements:
    - Release branch release/<version> must exist
    - Target branch must exist
    - Tag <version> must exist (ensures release was tagged)
    - Working directory must be clean
    - gh CLI required for PR creation on conflicts
"""

import re
import subprocess
import sys

# Constants with documented rationale
VERSION_PATTERN = r'^v\d+\.\d+\.\d+$'
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency

RELEASE_BRANCH_PREFIX = 'release/'
# Rationale: git-flow release branch naming convention

MERGE_STRATEGY = '--no-ff'
# Rationale: Preserves release branch history in develop, easier to track releases


def validate_version_format(version):
    """
    Validate version follows semantic versioning pattern.

    Args:
        version: Version string to validate (e.g., 'v1.1.0')

    Raises:
        ValueError: If version doesn't match vX.Y.Z pattern
    """
    if not re.match(VERSION_PATTERN, version):
        raise ValueError(
            f"Invalid version format '{version}'. "
            f"Must match pattern vX.Y.Z (e.g., v1.1.0, v2.0.0)"
        )


def verify_branch_exists(branch_name):
    """
    Verify that a git branch exists.

    Args:
        branch_name: Name of branch to verify

    Raises:
        ValueError: If branch doesn't exist
    """
    try:
        subprocess.run(
            ['git', 'rev-parse', '--verify', branch_name],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        raise ValueError(
            f"Branch '{branch_name}' does not exist. "
            f"Use 'git branch -a' to list available branches."
        )


def verify_tag_exists(version):
    """
    Verify that version tag exists (ensures release was tagged).

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag doesn't exist
    """
    try:
        result = subprocess.run(
            ['git', 'tag', '-l', version],
            capture_output=True,
            text=True,
            check=True
        )

        if not result.stdout.strip():
            raise ValueError(
                f"Tag '{version}' does not exist. "
                f"Release must be tagged before back-merge. "
                f"Run: python .claude/skills/git-workflow-manager/scripts/tag_release.py {version} main"
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to check git tags: {e.stderr.strip()}"
        ) from e


def check_working_directory_clean():
    """
    Verify working directory has no uncommitted changes.

    Raises:
        RuntimeError: If working directory has uncommitted changes
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            raise RuntimeError(
                "Working directory has uncommitted changes. "
                "Please commit or stash changes before back-merge."
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to check git status: {e.stderr.strip()}"
        ) from e


def checkout_and_pull_branch(branch_name):
    """
    Checkout target branch and pull latest changes.

    Args:
        branch_name: Branch to checkout and update

    Returns:
        Latest commit SHA

    Raises:
        RuntimeError: If checkout or pull fails
    """
    try:
        # Checkout branch
        subprocess.run(
            ['git', 'checkout', branch_name],
            capture_output=True,
            check=True
        )

        # Pull latest
        subprocess.run(
            ['git', 'pull', 'origin', branch_name],
            capture_output=True,
            check=True
        )

        # Get commit SHA
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else 'Unknown error'
        raise RuntimeError(
            f"Failed to checkout/pull branch '{branch_name}': {error_msg}"
        ) from e


def attempt_merge(version, target_branch):
    """
    Attempt to merge release branch into target branch.

    Args:
        version: Release version (e.g., 'v1.1.0')
        target_branch: Target branch name (e.g., 'develop')

    Returns:
        Tuple of (success: bool, conflicts: list[str])

    Raises:
        RuntimeError: If merge command fails unexpectedly
    """
    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Attempt merge with --no-ff to preserve history
        result = subprocess.run(
            ['git', 'merge', release_branch, MERGE_STRATEGY],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            # Merge succeeded
            return True, []
        else:
            # Check if it's a merge conflict
            if 'CONFLICT' in result.stdout or 'conflict' in result.stderr.lower():
                # Get list of conflicting files
                conflicts_result = subprocess.run(
                    ['git', 'diff', '--name-only', '--diff-filter=U'],
                    capture_output=True,
                    text=True,
                    check=True
                )

                conflicts = [f for f in conflicts_result.stdout.strip().split('\n') if f]

                # Abort merge
                subprocess.run(
                    ['git', 'merge', '--abort'],
                    capture_output=True,
                    check=True
                )

                return False, conflicts
            else:
                # Unexpected error
                raise RuntimeError(
                    f"Merge failed unexpectedly: {result.stderr}"
                )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to execute merge command: {e.stderr.decode() if e.stderr else 'Unknown error'}"
        ) from e


def push_merge_to_remote(target_branch):
    """
    Push merged changes to remote.

    Args:
        target_branch: Branch to push

    Raises:
        RuntimeError: If push fails
    """
    try:
        subprocess.run(
            ['git', 'push', 'origin', target_branch],
            capture_output=True,
            check=True
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to push to remote: {e.stderr.decode() if e.stderr else 'Unknown error'}"
        ) from e


def create_pr_for_conflicts(version, target_branch, conflicts):
    """
    Create PR for manual conflict resolution using gh CLI.

    Args:
        version: Release version (e.g., 'v1.1.0')
        target_branch: Target branch (e.g., 'develop')
        conflicts: List of conflicting file paths

    Returns:
        PR URL if successful

    Raises:
        RuntimeError: If gh CLI not available or PR creation fails
    """
    # Check if gh CLI is available
    try:
        subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "gh CLI not available. Cannot create PR for conflict resolution. "
            "Install gh CLI: https://cli.github.com/ or resolve conflicts manually."
        )

    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    # Build PR title and body
    pr_title = f"chore(release): back-merge {version} to {target_branch}"

    # Get tag URL
    try:
        result = subprocess.run(
            ['gh', 'repo', 'view', '--json', 'url', '--jq', '.url'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_url = result.stdout.strip()
        tag_url = f"{repo_url}/releases/tag/{version}"
    except subprocess.CalledProcessError:
        tag_url = f"Release {version}"

    pr_body = f"""## Back-merge Conflicts Detected

This PR was automatically created because the back-merge of `{release_branch}` to `{target_branch}` resulted in conflicts.

### Release Information
- **Version:** {version}
- **Release Tag:** {tag_url}
- **Source Branch:** `{release_branch}`
- **Target Branch:** `{target_branch}`

### Conflicting Files

"""
    for conflict in conflicts:
        pr_body += f"- `{conflict}`\n"

    pr_body += """
### Resolution Instructions

1. Checkout this PR branch locally
2. Resolve conflicts in the listed files above
3. Test thoroughly (run quality gates)
4. Commit resolved changes
5. Push to this PR branch
6. Merge when all checks pass

### Commands

```bash
# Checkout PR branch
gh pr checkout <PR_NUMBER>

# After resolving conflicts
git add .
git commit -m "chore: resolve back-merge conflicts"
git push

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

---
*Generated by backmerge_release.py*
"""

    try:
        # Create PR
        result = subprocess.run(
            ['gh', 'pr', 'create',
             '--base', target_branch,
             '--head', release_branch,
             '--title', pr_title,
             '--body', pr_body],
            capture_output=True,
            text=True,
            check=True
        )

        pr_url = result.stdout.strip()
        return pr_url

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to create PR: {e.stderr.strip()}"
        ) from e


def main():
    """Main entry point for backmerge_release.py script."""
    if len(sys.argv) != 3:
        print("Usage: backmerge_release.py <version> <target_branch>", file=sys.stderr)
        print("Example: backmerge_release.py v1.1.0 develop", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    target_branch = sys.argv[2]

    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_version_format(version)
        verify_branch_exists(release_branch)
        verify_branch_exists(target_branch)
        verify_tag_exists(version)
        check_working_directory_clean()

        # Step 2: Checkout and Pull Target Branch
        print(f"Checking out {target_branch} and pulling latest...", file=sys.stderr)
        checkout_and_pull_branch(target_branch)

        # Step 3: Attempt Merge
        print(f"Attempting to merge {release_branch} into {target_branch}...", file=sys.stderr)
        success, conflicts = attempt_merge(version, target_branch)

        if success:
            # No conflicts - push merge
            print("Merge successful, pushing to remote...", file=sys.stderr)
            push_merge_to_remote(target_branch)

            # Success output
            print(f"\n✓ Checked out {target_branch}")
            print("✓ Pulled latest changes")
            print(f"✓ Merged {release_branch} into {target_branch} (no conflicts)")
            print(f"✓ Pushed to origin/{target_branch}")
            print("✓ Back-merge complete")

            print("\nNext steps:")
            print(f"  1. Cleanup release branch: python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}")

        else:
            # Conflicts detected - create PR
            print(f"⚠️  Merge conflicts detected in {len(conflicts)} file(s)", file=sys.stderr)
            print("Creating PR for manual resolution...", file=sys.stderr)

            pr_url = create_pr_for_conflicts(version, target_branch, conflicts)

            # Conflicts output
            print("\n⚠  Merge conflicts detected")
            print(f"✓ Created PR: {pr_url}")
            print(f"  Title: \"chore(release): back-merge {version} to {target_branch}\"")
            print("\nConflicting files:")
            for conflict in conflicts:
                print(f"  - {conflict}")
            print("\nPlease resolve conflicts in GitHub UI and merge the PR.")
            print("After PR is merged, run cleanup:")
            print(f"  python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBack-merge cancelled by user.", file=sys.stderr)
        # Abort any in-progress merge
        subprocess.run(['git', 'merge', '--abort'], capture_output=True, check=False)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        # Abort any in-progress merge
        subprocess.run(['git', 'merge', '--abort'], capture_output=True, check=False)
        sys.exit(1)


if __name__ == '__main__':
    main()
