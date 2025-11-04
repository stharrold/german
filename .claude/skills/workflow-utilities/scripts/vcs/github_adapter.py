#!/usr/bin/env python3
"""GitHub VCS adapter using gh CLI.

This adapter implements VCS operations for GitHub using the gh command-line tool.

Requirements:
- gh CLI installed (https://cli.github.com/)
- Authenticated via: gh auth login

Constants:
- GITHUB_CLI: gh command name
  Rationale: Centralize CLI command name for easier testing/mocking
"""

import subprocess

from .base_adapter import BaseVCSAdapter

# Constants
GITHUB_CLI = 'gh'


class GitHubAdapter(BaseVCSAdapter):
    """GitHub VCS adapter using gh CLI.

    Implements VCS operations for GitHub repositories.
    """

    def check_authentication(self) -> bool:
        """Check if user is authenticated with GitHub.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            subprocess.run(
                [GITHUB_CLI, 'auth', 'status'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_current_user(self) -> str:
        """Get the current authenticated GitHub user.

        Returns:
            GitHub username

        Raises:
            RuntimeError: If not authenticated or command fails
        """
        try:
            result = subprocess.check_output(
                [GITHUB_CLI, 'api', 'user', '--jq', '.login'],
                text=True,
                stderr=subprocess.PIPE,
                timeout=10
            )
            return result.strip()

        except FileNotFoundError:
            raise RuntimeError(
                f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/"
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(
                f"Failed to get GitHub username. "
                f"Make sure you're authenticated: gh auth login\n"
                f"Error: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while getting GitHub username")

    def create_pull_request(
        self,
        source_branch: str,
        target_branch: str,
        title: str,
        body: str
    ) -> str:
        """Create a GitHub pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name (base)
            title: PR title
            body: PR description

        Returns:
            Pull request URL

        Raises:
            RuntimeError: If PR creation fails
        """
        try:
            result = subprocess.check_output(
                [
                    GITHUB_CLI, 'pr', 'create',
                    '--base', target_branch,
                    '--head', source_branch,
                    '--title', title,
                    '--body', body
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30
            )
            # gh pr create outputs the PR URL
            pr_url = result.strip()
            return pr_url

        except FileNotFoundError:
            raise RuntimeError(
                f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/"
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(
                f"Failed to create GitHub pull request.\n"
                f"Error: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating GitHub pull request")

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            "GitHub"
        """
        return "GitHub"
