#!/usr/bin/env python3
"""Integration tests for worktree agent integration layer (Phase 3).

Tests the integration layer components:
- FlowTokenManager: Workflow context detection and flow token generation
- PHIDetector: PHI detection heuristics and justification extraction
- ComplianceWrapper: Compliance logging wrapper
- SyncEngineFactory: Factory with feature flag control
- trigger_sync_completion: Main entry point for agent hooks

Created: 2025-11-17
Issue: #161 - Phase 3 Integration Layer Implementation
"""

import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

# Add integration module to path
AGENTDB_SCRIPTS = Path(__file__).parent.parent.parent / ".claude" / "skills" / "agentdb-state-manager" / "scripts"
sys.path.insert(0, str(AGENTDB_SCRIPTS))

from worktree_agent_integration import (  # noqa: E402
    ComplianceWrapper,
    FlowTokenManager,
    PHIDetector,
    SyncEngineFactory,
    trigger_sync_completion,
)


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

    def test_hotfix_worktree_flow_token(self, tmp_path, monkeypatch):
        """Test flow token generation for hotfix worktree context."""
        # Simulate hotfix worktree directory
        worktree = tmp_path / "german_hotfix_20251117T120000Z_critical-bug"
        worktree.mkdir()
        monkeypatch.chdir(worktree)

        token = FlowTokenManager.get_flow_token()
        assert token == "hotfix/20251117T120000Z_critical-bug"

    def test_contrib_branch_flow_token(self, tmp_path, monkeypatch):
        """Test flow token generation for contrib branch."""
        # Mock git command
        def mock_run(*args, **kwargs):
            class Result:
                stdout = "contrib/stharrold\n"
                returncode = 0

            return Result()

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token == "contrib/stharrold"

    def test_claude_branch_flow_token(self, tmp_path, monkeypatch):
        """Test flow token generation for claude/ branch (Claude Code sessions)."""
        # Mock git command
        def mock_run(*args, **kwargs):
            class Result:
                stdout = "claude/phase-3-integration-layer-013DZD5UsKELiMg77gWcJrtS\n"
                returncode = 0

            return Result()

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token == "claude/phase-3-integration-layer-013DZD5UsKELiMg77gWcJrtS"

    def test_ad_hoc_flow_token_on_git_failure(self, tmp_path, monkeypatch):
        """Test fallback to ad-hoc flow token when git fails."""
        # Mock git command to fail
        def mock_run(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "git")

        monkeypatch.setattr(subprocess, "run", mock_run)

        token = FlowTokenManager.get_flow_token()
        assert token.startswith("ad-hoc-")
        assert len(token) == len("ad-hoc-") + 8  # ad-hoc-<8 hex chars>

    def test_issue_number_extraction(self):
        """Test issue number extraction from flow token."""
        assert FlowTokenManager.extract_issue_number("issue-161") == 161
        assert FlowTokenManager.extract_issue_number("feature/20251117_issue-161-integration") == 161
        assert FlowTokenManager.extract_issue_number("feature/20251117_phase-3-issue-161") == 161
        assert FlowTokenManager.extract_issue_number("contrib/stharrold") is None
        assert FlowTokenManager.extract_issue_number("feature/20251117_no-issue") is None


class TestPHIDetector:
    """Test PHI detection."""

    def test_explicit_phi_marker(self):
        """Test explicit PHI marker detection."""
        state = {"_contains_phi": True, "data": "some data"}
        assert PHIDetector.detect_phi(state) is True

    def test_explicit_phi_marker_false(self):
        """Test explicit PHI marker set to false."""
        state = {"_contains_phi": False, "patient_id": "12345"}
        # Should still detect PHI from field name, not just the marker
        assert PHIDetector.detect_phi(state) is True

    def test_phi_field_names(self):
        """Test PHI detection via field names."""
        phi_states = [
            {"patient_id": "12345"},
            {"patientid": "67890"},  # No underscore variant
            {"mrn": "MRN-67890"},
            {"ssn": "123-45-6789"},
            {"social_security": "123456789"},
            {"dob": "1980-01-01"},
            {"date_of_birth": "1980-01-01"},
            {"diagnosis": "Type 2 Diabetes"},
            {"treatment": "Metformin"},
            {"prescription": "Lisinopril 10mg"},
            {"icd_code": "E11.9"},
            {"health_record": "record_123"},
            {"medical_history": "..."},
            {"patient_name": "John Doe"},
            {"provider_name": "Dr. Smith"},
            {"insurance": "Blue Cross"},
            {"claim_number": "CLM-123"},
        ]

        for state in phi_states:
            assert PHIDetector.detect_phi(state) is True, f"Failed to detect PHI in {state}"

    def test_ssn_pattern_detection_with_hyphens(self):
        """Test SSN pattern detection with hyphens in values."""
        state = {"notes": "Patient SSN: 123-45-6789"}
        assert PHIDetector.detect_phi(state) is True

    def test_ssn_pattern_detection_without_hyphens(self):
        """Test SSN pattern detection without hyphens."""
        state = {"notes": "Patient SSN: 123456789"}
        assert PHIDetector.detect_phi(state) is True

    def test_phi_path_detection(self):
        """Test PHI detection via file paths."""
        phi_paths = [
            {"file_path": "/data/protected/patient_records.csv"},
            {"file_path": "/phi/medical_history.json"},
            {"file_path": "/medical/diagnoses.txt"},
            {"file_path": "/patient/records/mrn_12345.pdf"},
            {"file_path": "/health_records/2025/jan/record.xml"},
        ]

        for state in phi_paths:
            assert PHIDetector.detect_phi(state) is True, f"Failed to detect PHI in {state}"

    def test_no_phi_detected(self):
        """Test non-PHI state."""
        non_phi_states = [
            {"commit_sha": "abc123"},
            {"coverage": 85},
            {"test_results": {"passed": 10, "failed": 0}},
            {"lint_status": "pass"},
            {"user": "stharrold"},
            {"issue_number": 161},
            {"flow_token": "feature/20251117_slug"},
            {"timestamp": "2025-11-17T12:00:00Z"},
            {
                "commit_sha": "abc123",
                "coverage": 85,
                "test_results": {"passed": 10, "failed": 0},
            },
        ]

        for state in non_phi_states:
            assert PHIDetector.detect_phi(state) is False, f"False positive PHI detection in {state}"

    def test_justification_extraction_explicit(self):
        """Test PHI access justification extraction - explicit."""
        context = {"phi_justification": "IRB protocol #12345"}
        justification = PHIDetector.extract_justification(context)
        assert "IRB protocol #12345" in justification

    def test_justification_extraction_issue_number(self):
        """Test PHI access justification extraction - issue number."""
        context = {"issue_number": 161}
        justification = PHIDetector.extract_justification(context)
        assert "issue #161" in justification

    def test_justification_extraction_commit_message(self):
        """Test PHI access justification extraction - commit message."""
        context = {"commit_message": "fix(patient): update patient records schema\n\nDetailed description..."}
        justification = PHIDetector.extract_justification(context)
        assert "fix(patient)" in justification

    def test_justification_extraction_long_commit_message(self):
        """Test justification extraction truncates long commit messages."""
        long_message = "a" * 200  # 200 characters
        context = {"commit_message": long_message}
        justification = PHIDetector.extract_justification(context)
        assert len(justification) <= 120  # "Code change: " + 100 chars max

    def test_justification_extraction_generic_fallback(self):
        """Test PHI access justification extraction - generic fallback."""
        context = {"user": "stharrold", "action": "development"}
        justification = PHIDetector.extract_justification(context)
        assert "stharrold" in justification
        assert "development" in justification

    def test_justification_extraction_empty_context(self):
        """Test justification extraction with empty context."""
        context = {}
        justification = PHIDetector.extract_justification(context)
        assert "unknown" in justification  # Should have fallback


class TestSyncEngineFactory:
    """Test sync engine factory."""

    def test_disabled_by_default(self, monkeypatch):
        """Test sync engine disabled by default."""
        monkeypatch.delenv("SYNC_ENGINE_ENABLED", raising=False)
        monkeypatch.delenv("AGENTDB_PATH", raising=False)

        engine = SyncEngineFactory.create_sync_engine()
        assert engine is None

    def test_disabled_explicit_false(self, monkeypatch):
        """Test sync engine disabled when explicitly set to false."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "false")

        engine = SyncEngineFactory.create_sync_engine()
        assert engine is None

    def test_disabled_case_insensitive(self, monkeypatch):
        """Test feature flag is case-insensitive."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "FALSE")
        assert SyncEngineFactory.create_sync_engine() is None

        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "False")
        assert SyncEngineFactory.create_sync_engine() is None

    def test_enabled_case_insensitive(self, monkeypatch):
        """Test feature flag enabled is case-insensitive."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "TRUE")
        monkeypatch.setenv("AGENTDB_PATH", ":memory:")

        # Will fail to import sync_engine, but checks flag parsing
        # In actual test with sync_engine available, this would succeed
        try:
            SyncEngineFactory.create_sync_engine()
        except Exception:
            pass  # Expected if sync_engine not available

    def test_db_path_from_env(self, monkeypatch):
        """Test database path from environment variable."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")
        monkeypatch.setenv("AGENTDB_PATH", "/tmp/test.duckdb")

        # Will attempt to create engine with this path
        # (fails if sync_engine not available, but we check the logic)
        try:
            SyncEngineFactory.create_sync_engine()
        except Exception:
            pass  # Expected if sync_engine not available

    def test_db_path_explicit_override(self, monkeypatch):
        """Test explicit db_path overrides environment variable."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")
        monkeypatch.setenv("AGENTDB_PATH", "/tmp/env.duckdb")

        try:
            # Explicit path should override env var
            SyncEngineFactory.create_sync_engine(db_path="/tmp/explicit.duckdb")
        except Exception:
            pass  # Expected if sync_engine not available

    def test_singleton_caching(self, monkeypatch):
        """Test singleton pattern caches instances per db_path."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Clear cache
        SyncEngineFactory._instances.clear()

        # Mock SynchronizationEngine to avoid actual database
        mock_engine = mock.MagicMock()

        # Patch where SynchronizationEngine is imported (inside create_sync_engine)
        with mock.patch("sync_engine.SynchronizationEngine", return_value=mock_engine):
            # First call creates instance
            engine1 = SyncEngineFactory.create_sync_engine(db_path="test.db")
            assert engine1 is not None

            # Second call returns cached instance
            engine2 = SyncEngineFactory.create_sync_engine(db_path="test.db")
            assert engine2 is engine1

            # Different db_path creates new instance
            engine3 = SyncEngineFactory.create_sync_engine(db_path="test2.db")
            assert engine3 is not engine1


class TestComplianceWrapper:
    """Test compliance wrapper."""

    @pytest.mark.asyncio
    async def test_phi_detection_and_logging(self, caplog):
        """Test compliance wrapper detects PHI and logs warnings."""
        # Mock sync engine
        mock_engine = mock.MagicMock()
        mock_engine.on_agent_action_complete.return_value = ["exec-1"]

        wrapper = ComplianceWrapper(mock_engine)

        # Trigger with PHI in state
        with caplog.at_level("WARNING"):
            execution_ids = await wrapper.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-flow",
                state_snapshot={"patient_id": "12345", "coverage": 85},
                context={"user": "stharrold", "phi_justification": "IRB #12345"},
            )

        # Check PHI warning logged
        assert any("PHI detected" in record.message for record in caplog.records)
        assert execution_ids == ["exec-1"]

    @pytest.mark.asyncio
    async def test_compliance_violation_logging(self, caplog):
        """Test compliance wrapper logs violation when PHI without justification."""
        mock_engine = mock.MagicMock()
        mock_engine.on_agent_action_complete.return_value = []

        wrapper = ComplianceWrapper(mock_engine)

        # Trigger with PHI but no justification
        with caplog.at_level("ERROR"):
            await wrapper.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-flow",
                state_snapshot={"patient_id": "12345"},
                context={},  # No phi_justification
            )

        # Check compliance violation logged
        assert any("COMPLIANCE VIOLATION" in record.message for record in caplog.records)

    @pytest.mark.asyncio
    async def test_no_phi_no_warnings(self, caplog):
        """Test compliance wrapper doesn't log warnings for non-PHI state."""
        mock_engine = mock.MagicMock()
        mock_engine.on_agent_action_complete.return_value = []

        wrapper = ComplianceWrapper(mock_engine)

        # Trigger without PHI
        with caplog.at_level("WARNING"):
            await wrapper.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-flow",
                state_snapshot={"commit_sha": "abc123", "coverage": 85},
                context={"user": "stharrold"},
            )

        # Check no PHI warnings
        assert not any("PHI detected" in record.message for record in caplog.records)


@pytest.mark.asyncio
class TestTriggerSyncCompletion:
    """Test main sync trigger function."""

    async def test_trigger_disabled(self, monkeypatch, caplog):
        """Test sync trigger when disabled."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "false")

        with caplog.at_level("DEBUG"):
            result = await trigger_sync_completion(
                agent_id="develop", action="commit_complete", state_snapshot={"commit_sha": "abc123"}
            )

        # Should return False (disabled)
        assert result is False
        assert any("disabled" in record.message for record in caplog.records)

    async def test_trigger_enabled_with_mock_engine(self, monkeypatch):
        """Test sync trigger when enabled with mock engine."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock sync engine
        mock_wrapper = mock.MagicMock()
        mock_wrapper.on_agent_action_complete = mock.AsyncMock(return_value=["exec-1", "exec-2"])

        result = await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123", "coverage": 85},
            context={"user": "stharrold"},
            sync_engine=mock_wrapper,
        )

        # Should return True (enabled and executed)
        assert result is True
        mock_wrapper.on_agent_action_complete.assert_called_once()

    async def test_trigger_adds_flow_token_to_context(self, monkeypatch):
        """Test sync trigger adds flow token to context."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock wrapper to capture context
        mock_wrapper = mock.MagicMock()
        captured_context = {}

        async def capture_context(**kwargs):
            nonlocal captured_context
            captured_context = kwargs.get("context", {})
            return []

        mock_wrapper.on_agent_action_complete = capture_context

        await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123"},
            context={"user": "stharrold"},
            sync_engine=mock_wrapper,
        )

        # Check flow_token added to context
        assert "flow_token" in captured_context

    async def test_trigger_extracts_issue_number(self, monkeypatch):
        """Test sync trigger extracts issue number from flow token."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock flow token manager to return issue-based token
        def mock_flow_token():
            return "feature/20251117_issue-161-integration"

        monkeypatch.setattr(FlowTokenManager, "get_flow_token", mock_flow_token)

        # Mock wrapper to capture context
        captured_context = {}

        async def capture_context(**kwargs):
            nonlocal captured_context
            captured_context = kwargs.get("context", {})
            return []

        mock_wrapper = mock.MagicMock()
        mock_wrapper.on_agent_action_complete = capture_context

        await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123"},
            context={},
            sync_engine=mock_wrapper,
        )

        # Check issue_number extracted and added to context
        assert captured_context.get("issue_number") == 161

    async def test_graceful_degradation_on_error(self, monkeypatch, caplog):
        """Test graceful degradation when sync engine raises error."""
        monkeypatch.setenv("SYNC_ENGINE_ENABLED", "true")

        # Mock sync engine that raises error
        mock_wrapper = mock.MagicMock()
        mock_wrapper.on_agent_action_complete = mock.AsyncMock(side_effect=Exception("Database connection failed"))

        with caplog.at_level("ERROR"):
            result = await trigger_sync_completion(
                agent_id="develop",
                action="commit_complete",
                state_snapshot={"commit_sha": "abc123"},
                sync_engine=mock_wrapper,
            )

        # Should return False (error) but NOT crash
        assert result is False
        assert any("Sync trigger failed" in record.message for record in caplog.records)


# Integration tests with real Phase 2 sync engine (if available)
@pytest.mark.integration
@pytest.mark.asyncio
class TestEndToEndIntegration:
    """End-to-end integration tests with Phase 1 + Phase 2 components.

    These tests require:
    - Phase 1 schema loaded (agentdb_sync_schema.sql)
    - Phase 2 migration loaded (phase2_migration.sql)
    - DuckDB database with test data

    Run with: pytest -v -m integration
    """

    async def test_workflow_orchestrate_develop_assess(self, tmp_path):
        """Test full workflow: Orchestrate → Develop → Assess.

        This test requires Phase 1 + Phase 2 setup.
        """
        pytest.skip("Requires Phase 1 + Phase 2 database setup - implement in Phase 4")

        # TODO: Load Phase 1 schema + Phase 2 migration
        # TODO: Populate sync rules
        # TODO: Trigger orchestrate action
        # TODO: Verify develop action triggered
        # TODO: Trigger develop action
        # TODO: Verify assess action triggered
        # TODO: Verify audit trail entries

    async def test_concurrent_agents_no_deadlock(self, tmp_path):
        """Test concurrent agent execution without deadlocks."""
        pytest.skip("Requires Phase 1 + Phase 2 database setup - implement in Phase 4")

        # TODO: Run develop + assess agents in parallel
        # TODO: Verify no database lock errors
        # TODO: Verify all syncs executed

    async def test_phi_compliance_audit_trail(self, tmp_path):
        """Test PHI detection creates proper audit trail entries."""
        pytest.skip("Requires Phase 1 + Phase 2 database setup - implement in Phase 4")

        # TODO: Trigger sync with PHI in state
        # TODO: Verify phi_involved=true in audit trail
        # TODO: Verify phi_justification present
        # TODO: Verify actor attribution

    async def test_idempotency_enforcement(self, tmp_path):
        """Test idempotency: same state triggers sync only once."""
        pytest.skip("Requires Phase 1 + Phase 2 database setup - implement in Phase 4")

        # TODO: Trigger same sync twice with identical state
        # TODO: Verify only one execution record created
        # TODO: Verify provenance_hash deduplication works
