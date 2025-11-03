#!/usr/bin/env python3
"""Azure DevOps VCS adapter using az CLI.

This adapter implements VCS operations for Azure DevOps using the az command-line tool.

Requirements:
- Azure CLI installed (https://learn.microsoft.com/cli/azure/)
- Azure DevOps extension: az extension add --name azure-devops
- Authenticated via: az login
- Configured: az devops configure --defaults organization=... project=...

Constants:
- AZURE_CLI: az command name
  Rationale: Centralize CLI command name for easier testing/mocking
"""

import subprocess
import sys
from typing import Optional

from .base_adapter import BaseVCSAdapter


# Constants
AZURE_CLI = 'az'


class AzureDevOpsAdapter(BaseVCSAdapter):
    """Azure DevOps VCS adapter using az CLI.

    Implements VCS operations for Azure DevOps repositories.

    Args:
        organization: Azure DevOps organization URL (e.g., https://dev.azure.com/myorg)
        project: Azure DevOps project name
    """

    def __init__(self, organization: str, project: str):
        """Initialize Azure DevOps adapter.

        Args:
            organization: Azure DevOps organization URL
            project: Azure DevOps project name

        Raises:
            ValueError: If organization or project is empty
        """
        if not organization or not organization.strip():
            raise ValueError("organization is required for Azure DevOps")
        if not project or not project.strip():
            raise ValueError("project is required for Azure DevOps")

        self.organization = organization.strip()
        self.project = project.strip()

    def check_authentication(self) -> bool:
        """Check if user is authenticated with Azure.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            subprocess.run(
                [AZURE_CLI, 'account', 'show'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_current_user(self) -> str:
        """Get the current authenticated Azure DevOps user.

        Returns:
            User email address

        Raises:
            RuntimeError: If not authenticated or command fails
        """
        try:
            result = subprocess.check_output(
                [
                    AZURE_CLI, 'devops', 'user', 'show',
                    '--user', 'me',
                    '--query', 'user.emailAddress',
                    '--output', 'tsv',
                    '--organization', self.organization
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=15
            )
            return result.strip()

        except FileNotFoundError:
            raise RuntimeError(
                f"'{AZURE_CLI}' CLI not found. "
                f"Install from https://learn.microsoft.com/cli/azure/"
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(
                f"Failed to get Azure DevOps user. "
                f"Make sure you're authenticated: az login\n"
                f"And have the Azure DevOps extension: az extension add --name azure-devops\n"
                f"Error: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while getting Azure DevOps user")

    def create_pull_request(
        self,
        source_branch: str,
        target_branch: str,
        title: str,
        body: str
    ) -> str:
        """Create an Azure DevOps pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name
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
                    AZURE_CLI, 'repos', 'pr', 'create',
                    '--source-branch', source_branch,
                    '--target-branch', target_branch,
                    '--title', title,
                    '--description', body,
                    '--organization', self.organization,
                    '--project', self.project,
                    '--query', 'url',
                    '--output', 'tsv'
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30
            )
            pr_url = result.strip()
            return pr_url

        except FileNotFoundError:
            raise RuntimeError(
                f"'{AZURE_CLI}' CLI not found. "
                f"Install from https://learn.microsoft.com/cli/azure/"
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(
                f"Failed to create Azure DevOps pull request.\n"
                f"Error: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating Azure DevOps pull request")

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            "Azure DevOps"
        """
        return "Azure DevOps"
