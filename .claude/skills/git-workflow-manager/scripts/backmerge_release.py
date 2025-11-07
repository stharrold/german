#!/usr/bin/env python3
"""Create PR to merge release branch back to develop after main merge.

⚠️ BRANCH PROTECTION EXCEPTION POLICY ⚠️

This script handles the ONLY workflow that merges to the protected branch
`develop` outside of feature PRs. The develop branch is a protected branch
that requires PRs (but not approvals) for ALL merges. This script creates a
pull request (never pushes directly) to ensure proper workflow and compliance.

Previous versions of this script merged directly to develop, which violated
branch protection. This was fixed in v1.8.0 to enforce PR workflow. As of
v1.8.0, PR approval is no longer required (self-merge enabled).

This script implements Step 5.6 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It creates a pull request to merge the release branch back
into develop to ensure all release changes are integrated into the development
branch.

This script ALWAYS creates a PR and never pushes directly to develop, ensuring
proper review workflow and branch protection compliance.

Usage:
    python backmerge_release.py <version> <target_branch>

Example:
    python backmerge_release.py v1.1.0 develop

Requirements:
    - Release branch release/<version> must exist
    - Target branch must exist
    - Tag <version> must exist (ensures release was tagged)
    - gh CLI or az CLI required for PR creation
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


def create_pr(version, target_branch):
    """
    Create PR to merge release branch back to target branch.

    This function creates a PR for back-merge. GitHub/CI will detect any
    merge conflicts automatically. This ensures all merges to develop go
    through proper review workflow and branch protection policies.

    Args:
        version: Release version (e.g., 'v1.1.0')
        target_branch: Target branch (e.g., 'develop')

    Returns:
        PR URL if successful

    Raises:
        RuntimeError: If gh/az CLI not available or PR creation fails
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
            "gh CLI not available. Cannot create PR. "
            "Install gh CLI: https://cli.github.com/"
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

    pr_body = f"""## Back-merge Release to Develop

This PR merges `{release_branch}` back to `{target_branch}` to complete the release cycle.

### Release Information
- **Version:** {version}
- **Release Tag:** {tag_url}
- **Source Branch:** `{release_branch}`
- **Target Branch:** `{target_branch}`

### What This PR Does

Merges release-specific changes (documentation, version bumps) from the release branch back to develop, ensuring develop stays in sync with production releases.

### Review Instructions

1. **Review changes** - Verify documentation updates and version changes
2. **Wait for CI** - Ensure all tests pass
3. **Merge** - Use GitHub/Azure DevOps portal merge button when ready (no approval required)

GitHub will automatically detect any merge conflicts. If conflicts exist, resolve them in the PR.

This follows the git-flow release workflow where all merges to develop go through PRs, even for release back-merges.

### Next Steps After Merge

Run cleanup script:
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}
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

        # Step 2: Create PR directly (no local merge attempts)
        print("Creating pull request for back-merge...", file=sys.stderr)
        pr_url = create_pr(version, target_branch)

        # Output
        print(f"\n✓ Created PR: {pr_url}")
        print(f"  Title: \"chore(release): back-merge {version} to {target_branch}\"")
        print("\n📋 Next steps:")
        print("  1. Review PR in GitHub/Azure DevOps portal")
        print("  2. Wait for CI checks to pass")
        print("  3. Merge through portal when ready")
        print(f"  4. Run cleanup: python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBack-merge cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
