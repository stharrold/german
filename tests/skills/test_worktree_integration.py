#!/usr/bin/env python3
"""Integration tests for worktree agent integration layer (Phase 3).

Tests cover:
- FlowTokenManager: Flow token generation for different contexts
- PHIDetector: PHI detection heuristics and justification extraction
- SyncEngineFactory: Feature flag control and singleton pattern
- trigger_sync_completion: Main entry point for agent hooks
- Integration tests: End-to-end workflows (requires Phase 1 + Phase 2 setup)

Created: 2025-11-17
Issue: #161 - Phase 3 Integration Layer Implementation
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add integration module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".claude" / "skills" / "agentdb-state-manager" / "scripts"))

from worktree_agent_integration import ComplianceWrapper, FlowTokenManager, PHIDetector, SyncEngineFactory, trigger_sync_completion


class TestFlowTokenManager:
    """Test flow token management."""

    def test_worktree_flow_token(self, tmp_path, monkeypatch):
        """Test flow token generation for worktree context."""
        # Simulate worktree directory
        worktree = tmp_path / "german_feature_20251117T024349Z_phase-3-integration"
        worktree.mkdir()
        monkeypatch.chdir(worktree)

        token = FlowTokenManager.get_flow_token()
        assert token == "feature/20251117T024349Z_phase-3-integration"

    def test_contrib_branch_flow_token(self, monkeypatch):
        """Test flow token generation for contrib branch."""
        # Mock git command
        def mock_run(*args, **kwargs):
            result = Mock()
            result.stdout = "contrib/stharrold\n"
            result.returncode = 0
            return result

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token == "contrib/stharrold"

    def test_claude_branch_flow_token(self, monkeypatch):
        """Test flow token generation for claude/ branch (development)."""
        # Mock git command
        def mock_run(*args, **kwargs):
            result = Mock()
            result.stdout = "claude/phase-3-integration-layer-01AFAqHLk5GbT28yGaESZtTr\n"
            result.returncode = 0
            return result

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token == "claude/phase-3-integration-layer-01AFAqHLk5GbT28yGaESZtTr"

    def test_ad_hoc_flow_token_on_git_failure(self, monkeypatch):
        """Test ad-hoc flow token when git fails."""
        # Mock git command to raise exception
        def mock_run(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "git")

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token.startswith("ad-hoc-")
        assert len(token) == len("ad-hoc-") + 8  # UUID is 8 hex chars

    def test_issue_number_extraction(self):
        """Test issue number extraction from flow token."""
        # Test various patterns
        assert FlowTokenManager.extract_issue_number("issue-161") == 161
        assert FlowTokenManager.extract_issue_number("feature/20251117_issue-161-integration") == 161
        assert FlowTokenManager.extract_issue_number("contrib/stharrold") is None
        assert FlowTokenManager.extract_issue_number("ad-hoc-abc123") is None

    def test_issue_number_extraction_multiple_numbers(self):
        """Test issue number extraction with multiple issue references."""
        # Should extract first issue number
        token = "feature/20251117_issue-161-issue-162-combined"
        assert FlowTokenManager.extract_issue_number(token) == 161


class TestPHIDetector:
    """Test PHI detection."""

    def test_explicit_phi_marker(self):
        """Test explicit PHI marker detection."""
        state = {"_contains_phi": True, "data": "some data"}
        assert PHIDetector.detect_phi(state) is True

    def test_explicit_phi_marker_false(self):
        """Test explicit PHI marker set to False."""
        state = {"_contains_phi": False, "patient_id": "12345"}
        # Should still detect PHI from field name even if marker is False
        assert PHIDetector.detect_phi(state) is True

    def test_phi_field_names(self):
        """Test PHI detection via field names."""
        states = [
            {"patient_id": "12345"},
            {"patientid": "12345"},  # No underscore
            {"mrn": "MRN-67890"},
            {"ssn": "123-45-6789"},
            {"social_security": "123-45-6789"},
            {"dob": "1980-01-01"},
            {"date_of_birth": "1980-01-01"},
            {"diagnosis": "Type 2 Diabetes"},
            {"treatment": "Metformin"},
            {"prescription": "Rx-12345"},
            {"icd_code": "E11.9"},
            {"health_record": "HR-12345"},
            {"phi_data": "sensitive"},
            {"protected_health": "info"}
        ]

        for state in states:
            assert PHIDetector.detect_phi(state) is True, f"Failed to detect PHI in {state}"

    def test_phi_field_names_case_insensitive(self):
        """Test PHI detection is case-insensitive."""
        states = [
            {"PATIENT_ID": "12345"},
            {"Patient_Id": "12345"},
            {"MRN": "MRN-67890"},
            {"SSN": "123-45-6789"}
        ]

        for state in states:
            assert PHIDetector.detect_phi(state) is True, f"Failed to detect PHI in {state}"

    def test_ssn_pattern_detection(self):
        """Test SSN pattern detection in values."""
        # With hyphens
        state = {"notes": "Patient SSN: 123-45-6789"}
        assert PHIDetector.detect_phi(state) is True

        # Without hyphens
        state = {"notes": "Patient SSN: 123456789"}
        assert PHIDetector.detect_phi(state) is True

    def test_phi_path_detection(self):
        """Test PHI detection via file paths."""
        paths = [
            "/data/protected/patient_records.csv",
            "/phi/medical_history.json",
            "/medical/records.db",
            "/patient/data.json",
            "/health_records/archive.zip"
        ]

        for path in paths:
            state = {"file_path": path}
            assert PHIDetector.detect_phi(state) is True, f"Failed to detect PHI in path: {path}"

    def test_no_phi_detected(self):
        """Test non-PHI state."""
        states = [
            {"commit_sha": "abc123"},
            {"coverage": 85},
            {"test_results": {"passed": 10, "failed": 0}},
            {"lint_status": "pass"},
            {"user": "stharrold"},
            {"file_path": "/home/user/project/src/main.py"}
        ]

        for state in states:
            assert PHIDetector.detect_phi(state) is False, f"False positive PHI detection in {state}"

    def test_justification_extraction_explicit(self):
        """Test explicit PHI justification extraction."""
        context = {"phi_justification": "IRB protocol #12345"}
        assert "IRB protocol" in PHIDetector.extract_justification(context)

    def test_justification_extraction_issue_number(self):
        """Test justification extraction from issue number."""
        context = {"issue_number": 161}
        justification = PHIDetector.extract_justification(context)
        assert "issue #161" in justification

    def test_justification_extraction_commit_message(self):
        """Test justification extraction from commit message."""
        context = {"commit_message": "fix(patient): update patient records schema"}
        justification = PHIDetector.extract_justification(context)
        assert "fix(patient)" in justification

    def test_justification_extraction_multiline_commit(self):
        """Test justification extraction from multiline commit message."""
        context = {
            "commit_message": "fix(patient): update schema\n\nDetailed explanation\nof the changes"
        }
        justification = PHIDetector.extract_justification(context)
        # Should only include first line
        assert "fix(patient): update schema" in justification
        assert "Detailed explanation" not in justification

    def test_justification_extraction_generic_fallback(self):
        """Test generic fallback justification."""
        context = {"user": "stharrold", "action": "development"}
        justification = PHIDetector.extract_justification(context)
        assert "stharrold" in justification
        assert "development" in justification

    def test_justification_extraction_unknown_fallback(self):
        """Test fallback when no context provided."""
        context = {}
        justification = PHIDetector.extract_justification(context)
        assert "unknown" in justification


class TestComplianceWrapper:
    """Test compliance wrapper."""

    @pytest.mark.asyncio
    async def test_phi_detection_and_logging(self, caplog):
        """Test PHI detection triggers compliance logging."""
        import logging
        caplog.set_level(logging.INFO)  # Capture INFO level logs

        # Mock sync engine
        mock_engine = Mock()
        mock_engine.on_agent_action_complete = Mock(return_value=["exec-123"])

        wrapper = ComplianceWrapper(mock_engine)

        # State with PHI
        state = {"patient_id": "12345", "coverage": 85}
        context = {"user": "stharrold", "phi_justification": "IRB protocol #12345"}

        await wrapper.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-token",
            state_snapshot=state,
            context=context
        )

        # Check logging
        assert "PHI detected" in caplog.text
        assert "IRB protocol #12345" in caplog.text

    @pytest.mark.asyncio
    async def test_phi_without_justification_logs_warning(self, caplog):
        """Test PHI without justification logs compliance warning."""
        # Mock sync engine
        mock_engine = Mock()
        mock_engine.on_agent_action_complete = Mock(return_value=["exec-123"])

        wrapper = ComplianceWrapper(mock_engine)

        # State with PHI but no justification
        state = {"patient_id": "12345"}
        context = {}  # No justification

        await wrapper.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-token",
            state_snapshot=state,
            context=context
        )

        # Check error logging
        assert "compliance violation" in caplog.text

    @pytest.mark.asyncio
    async def test_no_phi_no_warnings(self, caplog):
        """Test non-PHI state doesn't trigger warnings."""
        # Mock sync engine
        mock_engine = Mock()
        mock_engine.on_agent_action_complete = Mock(return_value=["exec-123"])

        wrapper = ComplianceWrapper(mock_engine)

        # State without PHI
        state = {"commit_sha": "abc123", "coverage": 85}
        context = {"user": "stharrold"}

        await wrapper.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-token",
            state_snapshot=state,
            context=context
        )

        # Should not contain PHI warnings
        assert "PHI detected" not in caplog.text
        assert "compliance violation" not in caplog.text


class TestSyncEngineFactory:
    """Test sync engine factory."""

    def teardown_method(self):
        """Clean up singleton after each test."""
        SyncEngineFactory.reset()

    def test_disabled_by_default(self, monkeypatch):
        """Test sync engine disabled by default."""
        monkeypatch.delenv("SYNC_ENGINE_ENABLED", raising=False)

        engine = SyncEngineFactory.create_sync_engine()
        assert engine is None

    def test_disabled_explicitly(self, monkeypatch):
        """Test sync engine disabled with explicit false."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "false")

        engine = SyncEngineFactory.create_sync_engine()
        assert engine is None

    def test_enabled_via_env(self, monkeypatch, tmp_path):
        """Test sync engine enabled via environment variable."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock the SynchronizationEngine import
        mock_engine_class = Mock()
        mock_engine_instance = Mock()
        mock_engine_class.return_value = mock_engine_instance

        with patch.dict('sys.modules', {'sync_engine': Mock(SynchronizationEngine=mock_engine_class)}):
            engine = SyncEngineFactory.create_sync_engine(db_path=":memory:")

            # Should return ComplianceWrapper
            assert engine is not None
            assert isinstance(engine, ComplianceWrapper)

    def test_singleton_pattern(self, monkeypatch):
        """Test singleton pattern reuses same instance."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        mock_engine_class = Mock()
        mock_engine_instance = Mock()
        mock_engine_class.return_value = mock_engine_instance

        with patch.dict('sys.modules', {'sync_engine': Mock(SynchronizationEngine=mock_engine_class)}):
            engine1 = SyncEngineFactory.create_sync_engine(db_path=":memory:")
            engine2 = SyncEngineFactory.create_sync_engine(db_path=":memory:")

            # Should be same instance
            assert engine1 is engine2

            # Mock should only be called once
            assert mock_engine_class.call_count == 1

    def test_different_db_path_creates_new_instance(self, monkeypatch):
        """Test different db_path creates new instance."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        mock_engine_class = Mock()
        mock_engine_instance = Mock()
        mock_engine_class.return_value = mock_engine_instance

        with patch.dict('sys.modules', {'sync_engine': Mock(SynchronizationEngine=mock_engine_class)}):
            engine1 = SyncEngineFactory.create_sync_engine(db_path=":memory:")
            engine2 = SyncEngineFactory.create_sync_engine(db_path="/tmp/test.db")

            # Should be different instances
            assert engine1 is not engine2

            # Mock should be called twice
            assert mock_engine_class.call_count == 2

    def test_import_error_handling(self, monkeypatch, caplog):
        """Test graceful handling of import errors."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock import to raise ImportError
        with patch.dict('sys.modules', {'sync_engine': None}):
            engine = SyncEngineFactory.create_sync_engine()

            assert engine is None
            assert "Failed to import" in caplog.text

    def test_initialization_error_handling(self, monkeypatch, caplog):
        """Test graceful handling of initialization errors."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock engine to raise exception on init
        mock_engine_class = Mock(side_effect=Exception("Database connection failed"))

        with patch.dict('sys.modules', {'sync_engine': Mock(SynchronizationEngine=mock_engine_class)}):
            engine = SyncEngineFactory.create_sync_engine()

            assert engine is None
            assert "Failed to initialize" in caplog.text


@pytest.mark.asyncio
class TestTriggerSyncCompletion:
    """Test main sync trigger function."""

    def teardown_method(self):
        """Clean up singleton after each test."""
        SyncEngineFactory.reset()

    async def test_trigger_disabled(self, monkeypatch):
        """Test sync trigger when disabled."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "false")

        result = await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123"}
        )

        # Should return False (disabled)
        assert result is False

    async def test_trigger_enabled(self, monkeypatch):
        """Test sync trigger when enabled."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock sync engine
        mock_engine_instance = Mock()
        mock_engine_instance.on_agent_action_complete = Mock(return_value=["exec-123"])

        mock_wrapper = ComplianceWrapper(mock_engine_instance)

        result = await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123", "coverage": 85},
            context={"user": "stharrold"},
            sync_engine=mock_wrapper
        )

        # Should return True (enabled and executed)
        assert result is True

    async def test_graceful_degradation(self, monkeypatch, caplog):
        """Test graceful degradation on sync engine error."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock sync engine that raises error
        mock_engine_instance = Mock()
        mock_engine_instance.on_agent_action_complete = Mock(
            side_effect=Exception("Database connection failed")
        )

        mock_wrapper = ComplianceWrapper(mock_engine_instance)

        result = await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123"},
            sync_engine=mock_wrapper
        )

        # Should return False (error) but NOT crash
        assert result is False
        assert "Sync trigger failed" in caplog.text

    async def test_flow_token_injection(self, monkeypatch):
        """Test flow token is automatically injected into context."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock sync engine
        mock_engine_instance = Mock()
        execution_ids = []

        # Capture flow_token from call
        def capture_call(**kwargs):
            flow_token = kwargs.get('flow_token')
            assert flow_token is not None
            assert flow_token != ""
            execution_ids.append("exec-123")
            return execution_ids

        mock_engine_instance.on_agent_action_complete = Mock(side_effect=capture_call)
        mock_wrapper = ComplianceWrapper(mock_engine_instance)

        await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123"},
            context={"user": "stharrold"},
            sync_engine=mock_wrapper
        )

        # Verify flow token was injected
        assert len(execution_ids) > 0


# Integration tests requiring Phase 1 + Phase 2 setup
@pytest.mark.asyncio
@pytest.mark.integration
class TestEndToEndIntegration:
    """End-to-end integration tests with Phase 1 + Phase 2 components.

    These tests require:
    - Phase 1 schema loaded (agentdb_sync_schema.sql)
    - Phase 2 migration loaded (phase2_migration.sql)
    - DuckDB database with sample sync rules
    """

    async def test_workflow_orchestrate_develop_assess(self, tmp_path):
        """
        Test full workflow: Orchestrate (BMAD) → Develop (commit) → Assess (test).

        This test requires Phase 1 schema + Phase 2 sync engine.
        """
        pytest.skip("Requires Phase 1 + Phase 2 setup - implement after basic tests pass")

        # TODO: Load Phase 1 schema + Phase 2 migration
        # TODO: Populate sync rules
        # TODO: Trigger orchestrate action
        # TODO: Verify develop action triggered
        # TODO: Trigger develop action
        # TODO: Verify assess action triggered
        # TODO: Verify audit trail entries

    async def test_concurrent_agents_no_deadlock(self, tmp_path):
        """Test concurrent agent execution without deadlocks."""
        pytest.skip("Requires Phase 1 + Phase 2 setup - implement after basic tests pass")

        # TODO: Run develop + assess agents in parallel
        # TODO: Verify no database lock errors
        # TODO: Verify all syncs executed

    async def test_phi_compliance_audit_trail(self, tmp_path):
        """Test PHI detection creates proper audit trail entries."""
        pytest.skip("Requires Phase 1 + Phase 2 setup - implement after basic tests pass")

        # TODO: Trigger sync with PHI in state
        # TODO: Verify phi_involved=true in audit trail
        # TODO: Verify phi_justification present
        # TODO: Verify actor attribution


# Test fixtures
@pytest.fixture
def mock_git_branch(monkeypatch):
    """Fixture to mock git branch detection."""
    def _mock(branch_name):
        def mock_run(*args, **kwargs):
            result = Mock()
            result.stdout = f"{branch_name}\n"
            result.returncode = 0
            return result
        monkeypatch.setattr(subprocess, "run", mock_run)
    return _mock


@pytest.fixture
def mock_worktree_directory(tmp_path, monkeypatch):
    """Fixture to mock worktree directory."""
    def _mock(slug):
        worktree = tmp_path / f"german_feature_20251117T024349Z_{slug}"
        worktree.mkdir()
        monkeypatch.chdir(worktree)
        return worktree
    return _mock
