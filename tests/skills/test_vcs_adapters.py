#!/usr/bin/env python3
"""Unit tests for VCS adapters (GitHub and Azure DevOps).

Tests cover:
- GitHub adapter CLI commands
- Azure DevOps adapter CLI commands
- Authentication checking
- User retrieval
- Pull request creation
- Error handling
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add VCS module to path
vcs_path = (
    Path(__file__).parent.parent.parent
    / '.claude' / 'skills' / 'workflow-utilities' / 'scripts'
)
sys.path.insert(0, str(vcs_path))
from vcs.azure_adapter import AzureDevOpsAdapter  # noqa: E402
from vcs.github_adapter import GitHubAdapter  # noqa: E402


class TestGitHubAdapter:
    """Test GitHub VCS adapter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.adapter = GitHubAdapter()

    @patch('subprocess.run')
    def test_check_authentication_success(self, mock_run):
        """Test successful authentication check."""
        mock_run.return_value = MagicMock(returncode=0)

        result = self.adapter.check_authentication()
        assert result is True
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_check_authentication_failure(self, mock_run):
        """Test failed authentication check."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'gh')

        result = self.adapter.check_authentication()
        assert result is False

    @patch('subprocess.check_output')
    def test_get_current_user_success(self, mock_check_output):
        """Test getting current user successfully."""
        mock_check_output.return_value = 'testuser\n'

        result = self.adapter.get_current_user()
        assert result == 'testuser'

    @patch('subprocess.check_output')
    def test_get_current_user_not_found(self, mock_check_output):
        """Test error when gh CLI not found."""
        mock_check_output.side_effect = FileNotFoundError()

        with pytest.raises(RuntimeError, match="'gh' CLI not found"):
            self.adapter.get_current_user()

    @patch('subprocess.check_output')
    def test_get_current_user_not_authenticated(self, mock_check_output):
        """Test error when not authenticated."""
        error = subprocess.CalledProcessError(1, 'gh')
        error.stderr = 'Not logged in'
        mock_check_output.side_effect = error

        with pytest.raises(RuntimeError, match="Failed to get GitHub username"):
            self.adapter.get_current_user()

    @patch('subprocess.check_output')
    def test_create_pull_request_success(self, mock_check_output):
        """Test creating pull request successfully."""
        expected_url = 'https://github.com/user/repo/pull/123'
        mock_check_output.return_value = f'{expected_url}\n'

        result = self.adapter.create_pull_request(
            'feature/test',
            'main',
            'Test PR',
            'Test description'
        )

        assert result == expected_url

    @patch('subprocess.check_output')
    def test_create_pull_request_failure(self, mock_check_output):
        """Test error when PR creation fails."""
        error = subprocess.CalledProcessError(1, 'gh')
        error.stderr = 'PR already exists'
        mock_check_output.side_effect = error

        with pytest.raises(RuntimeError, match="Failed to create GitHub pull request"):
            self.adapter.create_pull_request(
                'feature/test',
                'main',
                'Test PR',
                'Test description'
            )

    def test_get_provider_name(self):
        """Test provider name."""
        assert self.adapter.get_provider_name() == "GitHub"


class TestAzureDevOpsAdapter:
    """Test Azure DevOps VCS adapter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.adapter = AzureDevOpsAdapter(
            organization='https://dev.azure.com/myorg',
            project='MyProject'
        )

    def test_initialization_requires_organization(self):
        """Test that organization is required."""
        with pytest.raises(ValueError, match="organization is required"):
            AzureDevOpsAdapter('', 'MyProject')

    def test_initialization_requires_project(self):
        """Test that project is required."""
        with pytest.raises(ValueError, match="project is required"):
            AzureDevOpsAdapter('https://dev.azure.com/myorg', '')

    def test_initialization_stores_config(self):
        """Test that organization and project are stored."""
        assert self.adapter.organization == 'https://dev.azure.com/myorg'
        assert self.adapter.project == 'MyProject'

    @patch('subprocess.run')
    def test_check_authentication_success(self, mock_run):
        """Test successful authentication check."""
        mock_run.return_value = MagicMock(returncode=0)

        result = self.adapter.check_authentication()
        assert result is True

    @patch('subprocess.run')
    def test_check_authentication_failure(self, mock_run):
        """Test failed authentication check."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'az')

        result = self.adapter.check_authentication()
        assert result is False

    @patch('subprocess.check_output')
    def test_get_current_user_success(self, mock_check_output):
        """Test getting current user successfully."""
        mock_check_output.return_value = 'test@example.com\n'

        result = self.adapter.get_current_user()
        assert result == 'test@example.com'

    @patch('subprocess.check_output')
    def test_get_current_user_not_found(self, mock_check_output):
        """Test error when az CLI not found."""
        mock_check_output.side_effect = FileNotFoundError()

        with pytest.raises(RuntimeError, match="'az' CLI not found"):
            self.adapter.get_current_user()

    @patch('subprocess.check_output')
    def test_get_current_user_not_authenticated(self, mock_check_output):
        """Test error when not authenticated."""
        error = subprocess.CalledProcessError(1, 'az')
        error.stderr = 'Not logged in'
        mock_check_output.side_effect = error

        with pytest.raises(RuntimeError, match="Failed to get Azure DevOps user"):
            self.adapter.get_current_user()

    @patch('subprocess.check_output')
    def test_create_pull_request_success(self, mock_check_output):
        """Test creating pull request successfully."""
        expected_url = 'https://dev.azure.com/myorg/MyProject/_git/repo/pullrequest/123'
        mock_check_output.return_value = f'{expected_url}\n'

        result = self.adapter.create_pull_request(
            'feature/test',
            'main',
            'Test PR',
            'Test description'
        )

        assert result == expected_url

    @patch('subprocess.check_output')
    def test_create_pull_request_includes_org_and_project(self, mock_check_output):
        """Test that PR creation includes organization and project."""
        mock_check_output.return_value = 'https://dev.azure.com/myorg/MyProject/_git/repo/pullrequest/123\n'

        self.adapter.create_pull_request(
            'feature/test',
            'main',
            'Test PR',
            'Test description'
        )

        # Verify the command included organization and project
        call_args = mock_check_output.call_args[0][0]
        assert '--organization' in call_args
        assert 'https://dev.azure.com/myorg' in call_args
        assert '--project' in call_args
        assert 'MyProject' in call_args

    @patch('subprocess.check_output')
    def test_create_pull_request_failure(self, mock_check_output):
        """Test error when PR creation fails."""
        error = subprocess.CalledProcessError(1, 'az')
        error.stderr = 'PR already exists'
        mock_check_output.side_effect = error

        with pytest.raises(RuntimeError, match="Failed to create Azure DevOps pull request"):
            self.adapter.create_pull_request(
                'feature/test',
                'main',
                'Test PR',
                'Test description'
            )

    def test_get_provider_name(self):
        """Test provider name."""
        assert self.adapter.get_provider_name() == "Azure DevOps"
