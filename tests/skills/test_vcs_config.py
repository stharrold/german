#!/usr/bin/env python3
"""Unit tests for VCS configuration loading and validation.

Tests cover:
- Loading valid configuration files
- Handling missing configuration files
- Validating GitHub configuration
- Validating Azure DevOps configuration
- Error handling for malformed YAML
- Provider-specific validation
"""

import sys
from pathlib import Path
from unittest.mock import patch, mock_open
import tempfile

import pytest

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'workflow-utilities' / 'scripts'))
from vcs.config import load_vcs_config, validate_config, validate_azure_devops_config, CONFIG_FILE_NAME


class TestLoadVCSConfig:
    """Test loading VCS configuration from .vcs_config.yaml."""

    def test_load_missing_config_returns_none(self, tmp_path):
        """Test that missing config file returns None."""
        config_path = tmp_path / "nonexistent.yaml"
        result = load_vcs_config(config_path)
        assert result is None

    def test_load_valid_github_config(self, tmp_path):
        """Test loading valid GitHub configuration."""
        config_path = tmp_path / CONFIG_FILE_NAME
        config_path.write_text("""
vcs_provider: github
""")

        result = load_vcs_config(config_path)
        assert result is not None
        assert result['vcs_provider'] == 'github'

    def test_load_valid_azuredevops_config(self, tmp_path):
        """Test loading valid Azure DevOps configuration."""
        config_path = tmp_path / CONFIG_FILE_NAME
        config_path.write_text("""
vcs_provider: azure_devops

azure_devops:
  organization: "https://dev.azure.com/myorg"
  project: "MyProject"
""")

        result = load_vcs_config(config_path)
        assert result is not None
        assert result['vcs_provider'] == 'azure_devops'
        assert result['azure_devops']['organization'] == 'https://dev.azure.com/myorg'
        assert result['azure_devops']['project'] == 'MyProject'

    def test_load_malformed_yaml_raises_error(self, tmp_path):
        """Test that malformed YAML raises ValueError."""
        config_path = tmp_path / CONFIG_FILE_NAME
        config_path.write_text("""
vcs_provider: github
  invalid: indentation
    nested: badly
""")

        with pytest.raises(ValueError, match="Invalid YAML"):
            load_vcs_config(config_path)

    def test_load_empty_config_returns_none(self, tmp_path):
        """Test that empty config file returns None."""
        config_path = tmp_path / CONFIG_FILE_NAME
        config_path.write_text("")

        result = load_vcs_config(config_path)
        assert result is None


class TestValidateConfig:
    """Test configuration validation."""

    def test_validate_github_config(self):
        """Test validating GitHub configuration."""
        config = {'vcs_provider': 'github'}

        # Should not raise
        validate_config(config)

    def test_validate_azuredevops_config(self):
        """Test validating Azure DevOps configuration."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg',
                'project': 'MyProject'
            }
        }

        # Should not raise
        validate_config(config)

    def test_validate_missing_provider_raises_error(self):
        """Test that missing vcs_provider raises ValueError."""
        config = {}

        with pytest.raises(ValueError, match="Missing required field: vcs_provider"):
            validate_config(config)

    def test_validate_invalid_provider_raises_error(self):
        """Test that invalid provider raises ValueError."""
        config = {'vcs_provider': 'gitlab'}

        with pytest.raises(ValueError, match="Invalid vcs_provider"):
            validate_config(config)

    def test_validate_azuredevops_missing_config_raises_error(self):
        """Test that Azure DevOps without config raises ValueError."""
        config = {'vcs_provider': 'azure_devops'}

        with pytest.raises(ValueError, match="azure_devops configuration required"):
            validate_config(config)


class TestValidateAzureDevOpsConfig:
    """Test Azure DevOps-specific configuration validation."""

    def test_validate_azuredevops_requires_dict(self):
        """Test that azure_devops must be a dictionary."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': 'not a dict'
        }

        with pytest.raises(ValueError, match="must be a dictionary"):
            validate_azure_devops_config(config)

    def test_validate_azuredevops_requires_organization(self):
        """Test that organization is required."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'project': 'MyProject'
            }
        }

        with pytest.raises(ValueError, match="organization is required"):
            validate_azure_devops_config(config)

    def test_validate_azuredevops_requires_project(self):
        """Test that project is required."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg'
            }
        }

        with pytest.raises(ValueError, match="project is required"):
            validate_azure_devops_config(config)

    def test_validate_azuredevops_organization_must_be_string(self):
        """Test that organization must be a non-empty string."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': '',
                'project': 'MyProject'
            }
        }

        with pytest.raises(ValueError, match="organization must be a non-empty string"):
            validate_azure_devops_config(config)

    def test_validate_azuredevops_project_must_be_string(self):
        """Test that project must be a non-empty string."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg',
                'project': ''
            }
        }

        with pytest.raises(ValueError, match="project must be a non-empty string"):
            validate_azure_devops_config(config)

    def test_validate_valid_azuredevops_config(self):
        """Test that valid Azure DevOps config passes validation."""
        config = {
            'vcs_provider': 'azure_devops',
            'azure_devops': {
                'organization': 'https://dev.azure.com/myorg',
                'project': 'MyProject'
            }
        }

        # Should not raise
        validate_azure_devops_config(config)
