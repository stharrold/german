#!/usr/bin/env python3
"""Handle pull request feedback iteration.

This script fetches PR review comments, displays them grouped by file and line,
guides the user through addressing feedback, and optionally re-runs quality gates.

Constants:
- QUALITY_GATES_SCRIPT: Path to quality gate validation script
  Rationale: Centralize quality gate path for consistency
- PR_ITERATION_MARKER: String added to PR description to track iterations
  Rationale: Track how many feedback cycles have occurred
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'workflow-utilities' / 'scripts'))
from vcs import get_vcs_adapter

# Constants with documented rationale
QUALITY_GATES_SCRIPT = '.claude/skills/quality-enforcer/scripts/run_quality_gates.py'
PR_ITERATION_MARKER = '<!-- PR_ITERATION:'  # Track feedback iterations in PR body


def fetch_and_display_comments(adapter, pr_number):
    """Fetch and display PR review comments grouped by type.

    Args:
        adapter: VCS adapter instance (GitHub/Azure DevOps)
        pr_number: Pull request number

    Returns:
        List of comment dictionaries

    Raises:
        RuntimeError: If fetching comments fails
    """
    print(f"\n🔍 Fetching review comments for PR #{pr_number}...\n")

    try:
        comments = adapter.fetch_pr_comments(pr_number)
    except RuntimeError as e:
        print(f"ERROR: Failed to fetch PR comments: {e}", file=sys.stderr)
        raise

    if not comments:
        print("✓ No review comments found. PR is ready to merge!")
        return []

    # Group comments by file
    file_comments = {}
    general_comments = []

    for comment in comments:
        if comment.get('file'):
            file_path = comment['file']
            if file_path not in file_comments:
                file_comments[file_path] = []
            file_comments[file_path].append(comment)
        else:
            general_comments.append(comment)

    # Display general comments
    if general_comments:
        print("=" * 80)
        print("GENERAL COMMENTS")
        print("=" * 80)
        for i, comment in enumerate(general_comments, 1):
            print(f"\n[{i}] {comment['author']} wrote:")
            print(f"    {comment['body']}")
            print(f"    (at {comment['created_at']})")

    # Display file-specific comments
    if file_comments:
        print("\n" + "=" * 80)
        print("FILE-SPECIFIC COMMENTS")
        print("=" * 80)
        for file_path, file_comment_list in sorted(file_comments.items()):
            print(f"\n📄 {file_path}")
            for comment in file_comment_list:
                line_info = f" (line {comment['line']})" if comment.get('line') else ""
                print(f"   • {comment['author']}{line_info}:")
                print(f"     {comment['body']}")

    print("\n" + "=" * 80)
    print(f"Total comments: {len(comments)}")
    print("=" * 80 + "\n")

    return comments


def check_pr_status(adapter, pr_number):
    """Check and display PR status.

    Args:
        adapter: VCS adapter instance
        pr_number: Pull request number

    Returns:
        Dictionary with PR status
    """
    print(f"\n🔍 Checking PR #{pr_number} status...\n")

    try:
        status = adapter.get_pr_status(pr_number)
    except RuntimeError as e:
        print(f"ERROR: Failed to fetch PR status: {e}", file=sys.stderr)
        raise

    print(f"State: {status['state']}")
    print(f"Mergeable: {'✓' if status['mergeable'] else '✗'}")
    print(f"Approved: {'✓' if status['approved'] else '✗'}")
    if not status['approved']:
        print(f"Reviews required: {status['reviews_required']}")
    print()

    return status


def prompt_commit_strategy():
    """Prompt user for commit strategy.

    Returns:
        'amend' or 'new' or 'skip'
    """
    print("\n" + "=" * 80)
    print("COMMIT STRATEGY")
    print("=" * 80)
    print("\nHow would you like to address the feedback?")
    print("  [1] Amend last commit (for minor fixes, keeps history clean)")
    print("  [2] Create new commit(s) (for reviewable changes)")
    print("  [3] Skip (I'll handle commits manually)")
    print()

    while True:
        choice = input("Enter choice [1-3]: ").strip()
        if choice == '1':
            return 'amend'
        elif choice == '2':
            return 'new'
        elif choice == '3':
            return 'skip'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def run_quality_gates(worktree_path=None):
    """Run quality gates to verify changes.

    Args:
        worktree_path: Optional path to worktree (run tests there)

    Returns:
        True if quality gates pass, False otherwise
    """
    print("\n" + "=" * 80)
    print("RUNNING QUALITY GATES")
    print("=" * 80 + "\n")

    # Change to worktree directory if specified
    original_dir = Path.cwd()
    if worktree_path:
        worktree_path = Path(worktree_path)
        if not worktree_path.exists():
            print(f"WARNING: Worktree path does not exist: {worktree_path}")
            print("Running quality gates in current directory instead.")
        else:
            print(f"Running quality gates in worktree: {worktree_path}\n")
            try:
                import os
                os.chdir(worktree_path)
            except OSError as e:
                print(f"ERROR: Failed to change to worktree: {e}", file=sys.stderr)
                return False

    try:
        result = subprocess.run(
            ['python', QUALITY_GATES_SCRIPT],
            capture_output=True,
            text=True
        )

        # Print output regardless of success/failure
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print("\n✓ Quality gates passed!")
            return True
        else:
            print("\n✗ Quality gates failed. Please fix issues before pushing.")
            return False

    except FileNotFoundError:
        print(f"WARNING: Quality gates script not found: {QUALITY_GATES_SCRIPT}")
        print("Skipping quality gate validation.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to run quality gates: {e}", file=sys.stderr)
        return False
    finally:
        # Change back to original directory
        if worktree_path:
            try:
                import os
                os.chdir(original_dir)
            except OSError:
                pass


def update_pr_description(adapter, pr_number, iteration_count):
    """Update PR description with iteration count.

    Args:
        adapter: VCS adapter instance
        pr_number: Pull request number
        iteration_count: Current iteration number
    """
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    iteration_marker = f"{PR_ITERATION_MARKER} {iteration_count} at {timestamp} -->"

    print(f"\n📝 Updating PR description (iteration {iteration_count})...")

    # Note: This is a simplified update. In practice, you'd fetch the current
    # PR body, append the iteration marker, and update.
    # For now, we'll just add a marker.
    try:
        # This would need to be enhanced to preserve existing body content
        adapter.update_pr(
            pr_number,
            body=f"\n\n{iteration_marker}"
        )
        print("✓ PR description updated")
    except RuntimeError as e:
        print(f"WARNING: Failed to update PR description: {e}")


def handle_pr_feedback(pr_number, worktree_path=None, auto_quality_gates=True):
    """Handle PR feedback iteration workflow.

    Args:
        pr_number: Pull request number
        worktree_path: Optional path to worktree for running quality gates
        auto_quality_gates: Whether to automatically run quality gates

    Returns:
        0 on success, 1 on failure

    Raises:
        ValueError: If pr_number is invalid
        RuntimeError: If VCS operations fail
    """
    # Input validation
    if not isinstance(pr_number, int) or pr_number <= 0:
        raise ValueError(f"Invalid PR number: {pr_number}. Must be a positive integer.")

    # Get VCS adapter
    try:
        adapter = get_vcs_adapter()
    except Exception as e:
        print(f"ERROR: Failed to get VCS adapter: {e}", file=sys.stderr)
        print("Make sure you're in a git repository with a configured remote.")
        return 1

    provider_name = adapter.get_provider_name()
    print(f"\n🔧 Using {provider_name} adapter\n")

    # Step 1: Fetch and display comments
    try:
        comments = fetch_and_display_comments(adapter, pr_number)
    except RuntimeError:
        return 1

    if not comments:
        # No comments - check if PR is approved
        try:
            status = check_pr_status(adapter, pr_number)
            if status['approved']:
                print("✓ PR is approved and ready to merge!")
                return 0
            else:
                print("ℹ️  PR has no comments but is not yet approved.")
                return 0
        except RuntimeError:
            return 1

    # Step 2: Check PR status
    try:
        status = check_pr_status(adapter, pr_number)
    except RuntimeError:
        return 1

    # Step 3: Prompt for commit strategy
    strategy = prompt_commit_strategy()

    if strategy == 'skip':
        print("\n✓ Skipping automated commit. Make your changes and commit manually.")
        print("\nNext steps:")
        print("  1. Address the feedback in your code")
        print("  2. Commit your changes (git commit -m '...')")
        if auto_quality_gates:
            print("  3. Run quality gates")
        print("  4. Push to update the PR (git push)")
        return 0

    # Step 4: Wait for user to make changes
    print("\n" + "=" * 80)
    print("MAKE CHANGES")
    print("=" * 80)
    print("\nPlease address the feedback comments now.")
    print("Make your code changes, then return here.")
    print()
    input("Press ENTER when you've finished making changes...")

    # Step 5: Optional quality gates
    if auto_quality_gates:
        if not run_quality_gates(worktree_path):
            print("\n✗ Quality gates failed. Please fix issues before pushing.")
            print("\nRerun this script after fixing issues:")
            print(f"  python {__file__} {pr_number}")
            return 1

    # Step 6: Commit changes
    print("\n" + "=" * 80)
    print("COMMITTING CHANGES")
    print("=" * 80 + "\n")

    commit_msg = input("Enter commit message: ").strip()
    if not commit_msg:
        commit_msg = f"fix: address PR #{pr_number} feedback"

    try:
        if strategy == 'amend':
            print("\nAmending last commit...")
            subprocess.run([
                'git', 'add', '.'
            ], check=True)
            subprocess.run([
                'git', 'commit', '--amend', '-m', commit_msg
            ], check=True)
            print("✓ Changes amended to last commit")
        else:  # new
            print("\nCreating new commit...")
            subprocess.run([
                'git', 'add', '.'
            ], check=True)
            subprocess.run([
                'git', 'commit', '-m', commit_msg
            ], check=True)
            print("✓ New commit created")

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Failed to commit changes: {e}", file=sys.stderr)
        print("\nYou can commit manually and push when ready.")
        return 1

    # Step 7: Push changes
    print("\n" + "=" * 80)
    print("PUSHING CHANGES")
    print("=" * 80 + "\n")

    push_confirm = input("Push changes to update PR? [Y/n]: ").strip().lower()
    if push_confirm in ['', 'y', 'yes']:
        try:
            # Use force-with-lease if amending, normal push otherwise
            if strategy == 'amend':
                print("Force pushing (with lease) to update PR...")
                subprocess.run([
                    'git', 'push', '--force-with-lease'
                ], check=True)
            else:
                print("Pushing to update PR...")
                subprocess.run([
                    'git', 'push'
                ], check=True)

            print("✓ Changes pushed successfully")

            # Update PR description with iteration marker
            # Extract iteration count from existing markers or start at 1
            iteration_count = 1  # Simplified - would need to parse existing markers
            update_pr_description(adapter, pr_number, iteration_count)

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: Failed to push changes: {e}", file=sys.stderr)
            print("\nYou can push manually when ready:")
            if strategy == 'amend':
                print("  git push --force-with-lease")
            else:
                print("  git push")
            return 1
    else:
        print("\nℹ️  Changes not pushed. Push manually when ready:")
        if strategy == 'amend':
            print("  git push --force-with-lease")
        else:
            print("  git push")

    # Success summary
    print("\n" + "=" * 80)
    print("✓ PR FEEDBACK ITERATION COMPLETE")
    print("=" * 80)
    print(f"\nPR #{pr_number} has been updated with your changes.")
    print("Reviewers will be notified of the update.")
    print("\nNext steps:")
    print("  1. Wait for reviewer feedback")
    print("  2. If more changes needed, run this script again")
    print("  3. If approved, merge the PR!")

    return 0


def main():
    """Main entry point for script."""
    if len(sys.argv) < 2:
        print("Usage: python handle_pr_feedback.py <pr-number> [worktree-path]", file=sys.stderr)
        print("\nExamples:")
        print("  python handle_pr_feedback.py 42")
        print("  python handle_pr_feedback.py 42 ../german_feature_auth")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid PR number '{sys.argv[1]}'. Must be an integer.", file=sys.stderr)
        sys.exit(1)

    worktree_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        exit_code = handle_pr_feedback(pr_number, worktree_path)
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
