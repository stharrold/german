#!/usr/bin/env python3
"""Integration tests for VCS adapter factory and end-to-end workflows.

Tests cover:
- Factory function get_vcs_adapter()
- Configuration-based adapter selection
- Remote-based adapter detection
- End-to-end workflows with GitHub
- End-to-end workflows with Azure DevOps
- Error handling for missing CLIs
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile

import pytest

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'workflow-utilities' / 'scripts'))
from vcs import get_vcs_adapter
from vcs.github_adapter import GitHubAdapter
from vcs.azure_adapter import AzureDevOpsAdapter
from vcs.provider import VCSProvider


class TestGetVCSAdapter:
    """Test VCS adapter factory function."""

    @patch('vcs.load_vcs_config')
    def test_get_adapter_github_from_config(self, mock_load_config):
        """Test getting GitHub adapter from config."""
        mock_load_config.return_value = {'vcs_provider': 'github'}

        adapter = get_vcs_adapter()

        assert isinstance(adapter, GitHubAdapter)

    @patch('vcs.load_vcs_config')
    def test_get_adapter_azuredevops_from_config(self, mock_load_config):
        """Test getting Azure DevOps adapter from config."""
        mock_load_config.return_value = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg',
                'project': 'MyProject'
            }
        }

        adapter = get_vcs_adapter()

        assert isinstance(adapter, AzureDevOpsAdapter)
        assert adapter.organization == 'https://dev.azure.com/myorg'
        assert adapter.project == 'MyProject'

    @patch('vcs.load_vcs_config')
    def test_get_adapter_azuredevops_missing_org_raises_error(self, mock_load_config):
        """Test error when Azure DevOps config missing organization."""
        mock_load_config.return_value = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'project': 'MyProject'
            }
        }

        with pytest.raises(ValueError, match="Azure DevOps requires 'organization'"):
            get_vcs_adapter()

    @patch('vcs.load_vcs_config')
    def test_get_adapter_azuredevops_missing_project_raises_error(self, mock_load_config):
        """Test error when Azure DevOps config missing project."""
        mock_load_config.return_value = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg'
            }
        }

        with pytest.raises(ValueError, match="Azure DevOps requires 'organization'"):
            get_vcs_adapter()

    @patch('vcs.load_vcs_config')
    def test_get_adapter_unknown_provider_raises_error(self, mock_load_config):
        """Test error for unknown provider in config."""
        mock_load_config.return_value = {'vcs_provider': 'gitlab'}

        with pytest.raises(ValueError, match="Unknown VCS provider"):
            get_vcs_adapter()

    @patch('vcs.detect_provider')
    @patch('vcs.load_vcs_config')
    def test_get_adapter_github_from_remote(self, mock_load_config, mock_detect):
        """Test getting GitHub adapter from git remote detection."""
        mock_load_config.return_value = None
        mock_detect.return_value = VCSProvider.GITHUB

        adapter = get_vcs_adapter()

        assert isinstance(adapter, GitHubAdapter)

    @patch('vcs.detect_provider')
    @patch('vcs.load_vcs_config')
    def test_get_adapter_azuredevops_from_remote_requires_config(self, mock_load_config, mock_detect):
        """Test that Azure DevOps detected from remote still requires config."""
        mock_load_config.return_value = None
        mock_detect.return_value = VCSProvider.AZURE_DEVOPS

        with pytest.raises(ValueError, match="Azure DevOps detected but requires .vcs_config.yaml"):
            get_vcs_adapter()

    @patch('vcs.detect_provider')
    @patch('vcs.load_vcs_config')
    def test_get_adapter_defaults_to_github(self, mock_load_config, mock_detect):
        """Test fallback to GitHub when no config and no detection."""
        mock_load_config.return_value = None
        mock_detect.return_value = VCSProvider.GITHUB

        adapter = get_vcs_adapter()

        assert isinstance(adapter, GitHubAdapter)


class TestEndToEndGitHubWorkflow:
    """Test end-to-end workflows with GitHub adapter."""

    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('vcs.load_vcs_config')
    def test_end_to_end_github_workflow(self, mock_load_config, mock_run, mock_check_output):
        """Test complete GitHub workflow: authenticate, get user, create PR."""
        # Setup
        mock_load_config.return_value = {'vcs_provider': 'github'}
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            'testuser\n',  # get_current_user()
            'https://github.com/user/repo/pull/123\n'  # create_pull_request()
        ]

        # Execute workflow
        adapter = get_vcs_adapter()
        assert adapter.check_authentication() is True

        username = adapter.get_current_user()
        assert username == 'testuser'

        pr_url = adapter.create_pull_request(
            'feature/test',
            'main',
            'Test PR',
            'Test description'
        )
        assert pr_url == 'https://github.com/user/repo/pull/123'


class TestEndToEndAzureDevOpsWorkflow:
    """Test end-to-end workflows with Azure DevOps adapter."""

    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('vcs.load_vcs_config')
    def test_end_to_end_azuredevops_workflow(self, mock_load_config, mock_run, mock_check_output):
        """Test complete Azure DevOps workflow: authenticate, get user, create PR."""
        # Setup
        mock_load_config.return_value = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg',
                'project': 'MyProject'
            }
        }
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            'test@example.com\n',  # get_current_user()
            'https://dev.azure.com/myorg/MyProject/_git/repo/pullrequest/123\n'  # create_pull_request()
        ]

        # Execute workflow
        adapter = get_vcs_adapter()
        assert adapter.check_authentication() is True

        username = adapter.get_current_user()
        assert username == 'test@example.com'

        pr_url = adapter.create_pull_request(
            'feature/test',
            'main',
            'Test PR',
            'Test description'
        )
        assert pr_url == 'https://dev.azure.com/myorg/MyProject/_git/repo/pullrequest/123'


class TestErrorHandling:
    """Test error handling scenarios."""

    @patch('subprocess.check_output')
    @patch('vcs.load_vcs_config')
    def test_error_handling_missing_cli(self, mock_load_config, mock_check_output):
        """Test error when CLI is not installed."""
        mock_load_config.return_value = {'vcs_provider': 'github'}
        mock_check_output.side_effect = FileNotFoundError()

        adapter = get_vcs_adapter()

        with pytest.raises(RuntimeError, match="CLI not found"):
            adapter.get_current_user()

    @patch('subprocess.check_output')
    @patch('vcs.load_vcs_config')
    def test_error_handling_not_authenticated(self, mock_load_config, mock_check_output):
        """Test error when not authenticated."""
        mock_load_config.return_value = {'vcs_provider': 'github'}
        error = subprocess.CalledProcessError(1, 'gh')
        error.stderr = 'Not authenticated'
        mock_check_output.side_effect = error

        adapter = get_vcs_adapter()

        with pytest.raises(RuntimeError, match="Failed to get"):
            adapter.get_current_user()
