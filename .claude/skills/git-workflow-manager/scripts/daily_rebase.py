#!/usr/bin/env python3
"""Perform daily rebase workflow."""

import subprocess
import sys

def daily_rebase(contrib_branch):
    """
    Rebase contrib branch onto develop.

    Steps:
    1. Checkout contrib branch
    2. Fetch origin
    3. Rebase onto origin/develop
    4. Force push with lease

    Args:
        contrib_branch: Name of contrib branch (e.g., 'contrib/username')
    """
    print(f"Rebasing {contrib_branch} onto develop...")

    try:
        # Checkout contrib branch
        subprocess.run(['git', 'checkout', contrib_branch], check=True)

        # Fetch latest from origin
        subprocess.run(['git', 'fetch', 'origin'], check=True)

        # Rebase onto origin/develop
        subprocess.run(['git', 'rebase', 'origin/develop'], check=True)

        # Force push with lease (safe force push)
        subprocess.run([
            'git', 'push', 'origin', contrib_branch, '--force-with-lease'
        ], check=True)

        print(f"✓ {contrib_branch} rebased onto develop")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Rebase failed: {e}")
        print("\nTo resolve conflicts:")
        print("  1. Fix conflicts in affected files")
        print("  2. git add <resolved-files>")
        print("  3. git rebase --continue")
        print(f"  4. git push origin {contrib_branch} --force-with-lease")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: daily_rebase.py <contrib_branch>")
        print("Example: daily_rebase.py contrib/johndoe")
        sys.exit(1)

    success = daily_rebase(sys.argv[1])
    sys.exit(0 if success else 1)
