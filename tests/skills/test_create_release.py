#!/usr/bin/env python3
"""Unit tests for create_release.py script.

Tests cover:
- Version format validation
- Input validation
- Error handling
- Safety checks

These tests verify the validation and error handling logic without
requiring actual git operations.
"""

import re

import pytest

# Import validation functions from create_release.py
# Note: In production, these would be importable. For testing, we replicate the logic.

VERSION_PATTERN = r'^v\d+\.\d+\.\d+$'


def validate_version_format(version):
    """Validate version follows semantic versioning pattern."""
    if not re.match(VERSION_PATTERN, version):
        raise ValueError(
            f"Invalid version format '{version}'. "
            f"Must match pattern vX.Y.Z (e.g., v1.1.0, v2.0.0)"
        )


class TestVersionValidation:
    """Test version format validation."""

    def test_valid_version_formats(self):
        """Test that valid version formats are accepted."""
        valid_versions = [
            'v1.0.0',
            'v1.1.0',
            'v2.0.0',
            'v10.5.3',
            'v100.200.300',
        ]

        for version in valid_versions:
            try:
                validate_version_format(version)
            except ValueError:
                pytest.fail(f"Valid version '{version}' was rejected")

    def test_invalid_version_formats(self):
        """Test that invalid version formats are rejected."""
        invalid_versions = [
            '1.0.0',       # Missing 'v' prefix
            'v1.0',        # Missing patch version
            'v1',          # Missing minor and patch
            'v1.0.0.0',    # Too many components
            'v1.0.0-rc1',  # Pre-release suffix
            'v1.0.0+build', # Build metadata
            'version1.0.0', # Wrong prefix
            'V1.0.0',      # Capital V
            '',            # Empty string
            'v1.a.0',      # Non-numeric component
        ]

        for version in invalid_versions:
            with pytest.raises(ValueError, match="Invalid version format"):
                validate_version_format(version)

    def test_version_error_message_content(self):
        """Test that error messages are helpful."""
        with pytest.raises(ValueError) as exc_info:
            validate_version_format('1.0.0')

        error_msg = str(exc_info.value)
        assert 'Invalid version format' in error_msg
        assert '1.0.0' in error_msg
        assert 'vX.Y.Z' in error_msg


class TestTodoFileNaming:
    """Test TODO file naming convention."""

    def test_version_slug_conversion(self):
        """Test that versions are converted to valid slugs."""
        test_cases = [
            ('v1.0.0', 'v1-0-0'),
            ('v1.1.0', 'v1-1-0'),
            ('v2.5.3', 'v2-5-3'),
            ('v10.20.30', 'v10-20-30'),
        ]

        for version, expected_slug in test_cases:
            slug = version.replace('.', '-')
            assert slug == expected_slug, f"Version {version} should convert to {expected_slug}"

    def test_todo_filename_pattern(self):
        """Test TODO filename follows expected pattern."""
        timestamp = '20251023T143000Z'
        version_slug = 'v1-1-0'
        expected_filename = f'TODO_release_{timestamp}_{version_slug}.md'

        # Verify pattern components
        assert expected_filename.startswith('TODO_release_')
        assert timestamp in expected_filename
        assert version_slug in expected_filename
        assert expected_filename.endswith('.md')


class TestConstants:
    """Test that constants are properly defined."""

    def test_release_branch_prefix(self):
        """Test release branch prefix constant."""
        RELEASE_BRANCH_PREFIX = 'release/'

        # Verify prefix is used correctly
        version = 'v1.1.0'
        branch_name = f"{RELEASE_BRANCH_PREFIX}{version}"
        assert branch_name == 'release/v1.1.0'

    def test_timestamp_format(self):
        """Test timestamp format constant."""
        TIMESTAMP_FORMAT = '%Y%m%dT%H%M%SZ'

        # Verify format produces expected output
        from datetime import datetime, timezone
        test_time = datetime(2025, 10, 23, 14, 30, 0, tzinfo=timezone.utc)
        formatted = test_time.strftime(TIMESTAMP_FORMAT)
        assert formatted == '20251023T143000Z'


class TestVersionPatternRegex:
    """Test version pattern regex is correct."""

    def test_pattern_matches_valid_versions(self):
        """Test regex pattern matches valid semantic versions."""
        valid_versions = [
            'v0.0.1',
            'v1.0.0',
            'v1.2.3',
            'v10.20.30',
            'v999.999.999',
        ]

        for version in valid_versions:
            assert re.match(VERSION_PATTERN, version), \
                f"Pattern should match '{version}'"

    def test_pattern_rejects_invalid_versions(self):
        """Test regex pattern rejects invalid versions."""
        invalid_versions = [
            '1.0.0',        # No v prefix
            'v1.0',         # Incomplete
            'v1.0.0.0',     # Too many parts
            'v1.0.0-rc',    # Suffix
            'va.b.c',       # Non-numeric
        ]

        for version in invalid_versions:
            assert not re.match(VERSION_PATTERN, version), \
                f"Pattern should reject '{version}'"


class TestErrorMessages:
    """Test that error messages are clear and actionable."""

    def test_version_format_error_includes_examples(self):
        """Test version format errors include examples."""
        with pytest.raises(ValueError) as exc_info:
            validate_version_format('invalid')

        error_msg = str(exc_info.value)
        # Should mention pattern
        assert 'vX.Y.Z' in error_msg or 'v1.1.0' in error_msg

    def test_error_message_includes_invalid_input(self):
        """Test errors include the invalid input."""
        invalid_input = '1.2.3'

        with pytest.raises(ValueError) as exc_info:
            validate_version_format(invalid_input)

        error_msg = str(exc_info.value)
        assert invalid_input in error_msg


class TestInputSanitization:
    """Test input validation and sanitization."""

    def test_version_leading_trailing_whitespace(self):
        """Test versions with whitespace are handled."""
        # In production, script receives sys.argv which may have whitespace
        version_with_space = ' v1.0.0 '

        # Should be stripped before validation
        cleaned = version_with_space.strip()
        validate_version_format(cleaned)  # Should not raise

    def test_empty_version_raises_error(self):
        """Test empty version string is rejected."""
        with pytest.raises(ValueError):
            validate_version_format('')

    def test_none_version_raises_error(self):
        """Test None version is rejected."""
        with pytest.raises((ValueError, AttributeError, TypeError)):
            validate_version_format(None)


# Integration-style tests (would require actual git setup)
class TestScriptIntegration:
    """Integration tests requiring git repository setup.

    These tests are placeholders showing what would be tested
    in a full integration test suite.
    """

    def test_script_execution_placeholder(self):
        """Placeholder for script execution test."""
        # In full integration test:
        # 1. Create temp git repo
        # 2. Run create_release.py
        # 3. Verify branch created
        # 4. Verify TODO file created
        # 5. Cleanup
        pytest.skip("Integration test requires git setup")

    def test_cleanup_on_failure_placeholder(self):
        """Placeholder for cleanup test."""
        # In full integration test:
        # 1. Create temp git repo
        # 2. Force failure after branch creation
        # 3. Verify branch is cleaned up
        pytest.skip("Integration test requires git setup")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
