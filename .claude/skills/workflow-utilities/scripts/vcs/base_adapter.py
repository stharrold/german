#!/usr/bin/env python3
"""Base VCS adapter abstract class.

This module defines the interface that all VCS adapters must implement.

Design:
- Abstract base class enforces consistent interface across providers
- Concrete adapters implement provider-specific CLI commands
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseVCSAdapter(ABC):
    """Abstract base class for VCS provider adapters.

    All VCS adapters must implement these methods to provide a consistent
    interface for workflow scripts.
    """

    @abstractmethod
    def check_authentication(self) -> bool:
        """Check if user is authenticated with the VCS provider.

        Returns:
            True if authenticated, False otherwise

        Example:
            GitHub: gh auth status
            Azure DevOps: az account show
        """
        pass

    @abstractmethod
    def get_current_user(self) -> str:
        """Get the current authenticated user's identifier.

        Returns:
            Username, email, or other user identifier

        Raises:
            RuntimeError: If not authenticated or command fails

        Example:
            GitHub: gh api user --jq '.login'
            Azure DevOps: az devops user show --user me --query user.emailAddress
        """
        pass

    @abstractmethod
    def create_pull_request(
        self,
        source_branch: str,
        target_branch: str,
        title: str,
        body: str
    ) -> str:
        """Create a pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            title: PR title
            body: PR description

        Returns:
            Pull request URL

        Raises:
            RuntimeError: If PR creation fails

        Example:
            GitHub: gh pr create --base target --head source --title "..." --body "..."
            Azure DevOps: az repos pr create --source-branch source --target-branch target
        """
        pass

    def get_provider_name(self) -> str:
        """Get human-readable provider name.

        Returns:
            Provider name (e.g., "GitHub", "Azure DevOps")

        Note:
            This is a concrete method with a default implementation.
            Subclasses can override if needed.
        """
        return self.__class__.__name__.replace('Adapter', '')
