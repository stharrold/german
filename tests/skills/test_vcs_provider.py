#!/usr/bin/env python3
"""Unit tests for VCS provider detection.

Tests cover:
- GitHub URL pattern detection
- Azure DevOps URL pattern detection
- Provider detection from git remotes
- Error handling for unrecognised providers
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add VCS module to path
vcs_path = (
    Path(__file__).parent.parent.parent
    / '.claude' / 'skills' / 'workflow-utilities' / 'scripts'
)
sys.path.insert(0, str(vcs_path))
from vcs.provider import VCSProvider, detect_provider  # noqa: E402


@pytest.fixture(autouse=True)
def _clear_provider_cache():
    """Clear the module-level provider cache before each test."""
    import vcs.provider
    vcs.provider._cached_provider = None
    yield
    vcs.provider._cached_provider = None


class TestDetectProvider:
    """Test VCS provider detection from git remote URLs."""

    @patch('subprocess.check_output')
    def test_detect_github_from_https_url(self, mock_output):
        """Test GitHub detection from HTTPS URL."""
        mock_output.return_value = 'https://github.com/user/repo.git'
        result = detect_provider()
        assert result == VCSProvider.GITHUB

    @patch('subprocess.check_output')
    def test_detect_github_from_ssh_url(self, mock_output):
        """Test GitHub detection from SSH URL."""
        mock_output.return_value = 'git@github.com:user/repo.git'
        result = detect_provider()
        assert result == VCSProvider.GITHUB

    @patch('subprocess.check_output')
    def test_detect_azuredevops_from_https_url(self, mock_output):
        """Test Azure DevOps detection from HTTPS URL."""
        mock_output.return_value = 'https://dev.azure.com/org/project/_git/repo'
        result = detect_provider()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.check_output')
    def test_detect_azuredevops_from_ssh_url(self, mock_output):
        """Test Azure DevOps detection from SSH URL."""
        mock_output.return_value = 'git@ssh.dev.azure.com:v3/org/project/repo'
        result = detect_provider()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.check_output')
    def test_detect_azuredevops_from_visualstudio_url(self, mock_output):
        """Test Azure DevOps detection from visualstudio.com URL."""
        mock_output.return_value = 'https://myorg.visualstudio.com/project/_git/repo'
        result = detect_provider()
        assert result == VCSProvider.AZURE_DEVOPS

    @patch('subprocess.check_output')
    def test_unknown_provider_raises_runtime_error(self, mock_output):
        """Test that unknown providers raise RuntimeError."""
        mock_output.return_value = 'https://gitlab.com/user/repo.git'
        with pytest.raises(RuntimeError, match="Unrecognised VCS provider"):
            detect_provider()

    @patch('subprocess.check_output')
    def test_git_error_raises_runtime_error(self, mock_output):
        """Test that git errors raise RuntimeError."""
        mock_output.side_effect = subprocess.CalledProcessError(1, 'git', stderr='fatal: error')
        with pytest.raises(RuntimeError, match="Failed to read git remote URL"):
            detect_provider()

    @patch('subprocess.check_output')
    def test_timeout_raises_runtime_error(self, mock_output):
        """Test that timeouts raise RuntimeError."""
        mock_output.side_effect = subprocess.TimeoutExpired('git', 5)
        with pytest.raises(RuntimeError, match="Timeout"):
            detect_provider()

    @patch('subprocess.check_output')
    def test_missing_git_raises_runtime_error(self, mock_output):
        """Test that missing git binary raises RuntimeError."""
        mock_output.side_effect = FileNotFoundError()
        with pytest.raises(RuntimeError, match="git.*CLI not found"):
            detect_provider()

    @patch('subprocess.check_output')
    def test_caches_result(self, mock_output):
        """Test that provider detection result is cached."""
        mock_output.return_value = 'https://github.com/user/repo.git'
        result1 = detect_provider()
        result2 = detect_provider()
        assert result1 == result2 == VCSProvider.GITHUB
        # Should only call subprocess once due to caching
        assert mock_output.call_count == 1


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
