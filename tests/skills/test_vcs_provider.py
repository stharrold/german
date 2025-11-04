#!/usr/bin/env python3
"""Unit tests for VCS provider detection.

Tests cover:
- GitHub URL pattern detection
- Azure DevOps URL pattern detection
- Provider detection from git remotes
- Fallback to default provider
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'workflow-utilities' / 'scripts'))
from vcs.provider import VCSProvider, detect_from_remote, detect_provider


class TestProviderDetection:
    """Test VCS provider detection from git remote URLs."""

    @patch('subprocess.run')
    def test_detect_github_from_https_url(self, mock_run):
        """Test GitHub detection from HTTPS URL."""
        mock_run.return_value = MagicMock(
            stdout='https://github.com/user/repo.git\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result == VCSProvider.GITHUB

    @patch('subprocess.run')
    def test_detect_github_from_ssh_url(self, mock_run):
        """Test GitHub detection from SSH URL."""
        mock_run.return_value = MagicMock(
            stdout='git@github.com:user/repo.git\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result == VCSProvider.GITHUB

    @patch('subprocess.run')
    def test_detect_azuredevops_from_https_url(self, mock_run):
        """Test Azure DevOps detection from HTTPS URL."""
        mock_run.return_value = MagicMock(
            stdout='https://dev.azure.com/org/project/_git/repo\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.run')
    def test_detect_azuredevops_from_ssh_url(self, mock_run):
        """Test Azure DevOps detection from SSH URL."""
        mock_run.return_value = MagicMock(
            stdout='git@ssh.dev.azure.com:v3/org/project/repo\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.run')
    def test_detect_azuredevops_from_visualstudio_url(self, mock_run):
        """Test Azure DevOps detection from visualstudio.com URL."""
        mock_run.return_value = MagicMock(
            stdout='https://myorg.visualstudio.com/project/_git/repo\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.run')
    def test_detect_unknown_provider_returns_none(self, mock_run):
        """Test that unknown providers return None."""
        mock_run.return_value = MagicMock(
            stdout='https://gitlab.com/user/repo.git\n',
            returncode=0
        )

        result = detect_from_remote()
        assert result is None

    @patch('subprocess.run')
    def test_detect_from_remote_handles_git_error(self, mock_run):
        """Test that git errors return None."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')

        result = detect_from_remote()
        assert result is None

    @patch('subprocess.run')
    def test_detect_from_remote_handles_timeout(self, mock_run):
        """Test that timeouts return None."""
        mock_run.side_effect = subprocess.TimeoutExpired('git', 5)

        result = detect_from_remote()
        assert result is None

    @patch('subprocess.run')
    def test_detect_from_remote_handles_missing_git(self, mock_run):
        """Test that missing git binary returns None."""
        mock_run.side_effect = FileNotFoundError()

        result = detect_from_remote()
        assert result is None


class TestProviderDetectionWithFallback:
    """Test provider detection with fallback to default."""

    @patch('vcs.provider.detect_from_remote')
    def test_detect_provider_returns_detected(self, mock_detect):
        """Test that detected provider is returned."""
        mock_detect.return_value = VCSProvider.AZURE_DEVOPS

        result = detect_provider()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('vcs.provider.detect_from_remote')
    def test_detect_provider_falls_back_to_github(self, mock_detect):
        """Test fallback to GitHub when detection returns None."""
        mock_detect.return_value = None

        result = detect_provider()
        assert result == VCSProvider.GITHUB


class TestVCSProviderEnum:
    """Test VCSProvider enum."""

    def test_github_provider_value(self):
        """Test GitHub provider enum value."""
        assert VCSProvider.GITHUB.value == "github"

    def test_azure_devops_provider_value(self):
        """Test Azure DevOps provider enum value."""
        assert VCSProvider.AZURE_DEVOPS.value == "azure_devops"

    def test_provider_enum_members(self):
        """Test that expected providers exist."""
        providers = [p.value for p in VCSProvider]
        assert "github" in providers
        assert "azure_devops" in providers
