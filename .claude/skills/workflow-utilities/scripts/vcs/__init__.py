#!/usr/bin/env python3
"""VCS provider abstraction for workflow scripts.

This module provides a unified interface for interacting with different VCS providers
(GitHub, Azure DevOps) through CLI tools (gh, az).

Usage:
    from vcs import get_vcs_adapter

    vcs = get_vcs_adapter()
    username = vcs.get_current_user()
    vcs.create_pull_request(source, target, title, body)
"""

from .azure_adapter import AzureDevOpsAdapter
from .base_adapter import BaseVCSAdapter
from .config import load_vcs_config
from .github_adapter import GitHubAdapter
from .provider import VCSProvider, detect_provider

__all__ = [
    'BaseVCSAdapter',
    'GitHubAdapter',
    'AzureDevOpsAdapter',
    'VCSProvider',
    'get_vcs_adapter',
]


def get_vcs_adapter() -> BaseVCSAdapter:
    """Get appropriate VCS adapter based on configuration and context.

    Detection order:
    1. Load .vcs_config.yaml if exists → use specified provider
    2. Detect from git remote URL
    3. Default to GitHub (backward compatibility)

    Returns:
        Configured VCS adapter instance

    Raises:
        ValueError: If provider configuration is invalid
    """
    # Try loading explicit configuration
    config = load_vcs_config()
    if config:
        provider = config.get('vcs_provider')
        if provider == 'github':
            return GitHubAdapter()
        elif provider == 'azure_devops':
            org = config.get('azure_devops', {}).get('organization')
            project = config.get('azure_devops', {}).get('project')
            if not org or not project:
                raise ValueError("Azure DevOps requires 'organization' and 'project' in config")
            return AzureDevOpsAdapter(organization=org, project=project)
        else:
            raise ValueError(f"Unknown VCS provider in config: {provider}")

    # Try detecting from git remote
    detected = detect_provider()
    if detected == VCSProvider.AZURE_DEVOPS:
        # TODO: Extract org/project from git remote URL
        raise ValueError("Azure DevOps detected but requires .vcs_config.yaml with org/project")

    # Default to GitHub (backward compatibility)
    return GitHubAdapter()
