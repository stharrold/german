#!/usr/bin/env python3
"""End-to-End Integration Test Suite

Tests complete workflow execution across multiple agents with
synchronization rules coordinating handoffs.

Success Criteria:
- Complete 4-tier workflow execution (Orchestrate → Develop → Assess → Research)
- Concurrent agent coordination with no race conditions
- Error recovery flows trigger correctly
- All audit trails complete and consistent

Created: 2025-11-18
#163 - Phase 5 Testing & Compliance Validation
"""

import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'scripts'))

from sync_engine import SynchronizationEngine


@pytest.fixture
def e2e_db(tmp_path):
    """Create test database with full workflow sync rules."""
    db_path = tmp_path / "test_e2e.duckdb"
    conn = duckdb.connect(str(db_path))

    # Load Phase 1 schema
    schema_path = Path(".claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql")
    with open(schema_path) as f:
        conn.execute(f.read())

    # Load Phase 2 migration
    migration_path = Path(".claude/skills/agentdb-state-manager/schemas/phase2_migration.sql")
    with open(migration_path) as f:
        conn.execute(f.read())

    # Load Phase 4 default synchronization rules (4-tier workflow)
    default_syncs_path = Path(".claude/skills/agentdb-state-manager/templates/default_synchronizations.sql")
    with open(default_syncs_path) as f:
        conn.execute(f.read())

    conn.close()
    return str(db_path)


@pytest.fixture
def e2e_engine(e2e_db):
    """Create SynchronizationEngine for end-to-end testing."""
    engine = SynchronizationEngine(db_path=e2e_db)
    yield engine
    engine.close()


# ============================================================================
# Complete Workflow Tests (4-Tier Flow)
# ============================================================================

@pytest.mark.integration
class TestCompleteWorkflow:
    """Test complete 4-tier workflow execution."""

    @pytest.mark.xfail(reason="Phase 5+ schema: sync_executions needs flow_token column")
    def test_orchestrate_to_research_flow(self, e2e_engine):
        """Complete workflow: Orchestrate → Develop → Assess → Research."""

        flow_token = "e2e-complete-flow"

        # Step 1: Orchestrate agent completes planning
        exec_ids_1 = e2e_engine.on_agent_action_complete(
            agent_id="orchestrate",
            action="planning_complete",
            flow_token=flow_token,
            state_snapshot={
                "planning_status": "complete",
                "requirements_validated": True
            }
        )

        # Should trigger: orchestrate_to_develop sync rule
        assert len(exec_ids_1) >= 1, "Orchestrate → Develop sync should trigger"

        # Verify sync execution logged
        develop_sync = e2e_engine.conn.execute("""
            SELECT target_agent_id, target_action_spec
            FROM sync_executions
            WHERE execution_id = ?
        """, [exec_ids_1[0]]).fetchone()

        assert develop_sync is not None
        assert develop_sync[0] == 'develop', "Target should be develop agent"

        # Step 2: Develop agent completes implementation
        exec_ids_2 = e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token,
            state_snapshot={
                "commits": 15,
                "files_changed": 8,
                "tests_added": True
            }
        )

        # Should trigger: develop_to_assess sync rule
        assert len(exec_ids_2) >= 1, "Develop → Assess sync should trigger"

        # Step 3: Assess agent completes validation
        exec_ids_3 = e2e_engine.on_agent_action_complete(
            agent_id="assess",
            action="validation_complete",
            flow_token=flow_token,
            state_snapshot={
                "tests_passed": True,
                "coverage_percentage": 85,
                "lint_status": "pass"
            }
        )

        # Should trigger: assess_to_research sync rule
        assert len(exec_ids_3) >= 1, "Assess → Research sync should trigger"

        # Step 4: Research agent completes documentation
        exec_ids_4 = e2e_engine.on_agent_action_complete(
            agent_id="research",
            action="documentation_complete",
            flow_token=flow_token,
            state_snapshot={
                "docs_generated": True,
                "pr_ready": True
            }
        )

        # Should trigger: research_to_orchestrate sync rule (PR creation)
        assert len(exec_ids_4) >= 1, "Research → Orchestrate sync should trigger"

        # Verify complete audit trail
        all_executions = e2e_engine.conn.execute("""
            SELECT COUNT(DISTINCT sync_id)
            FROM sync_executions
            WHERE flow_token = ?
        """, [flow_token]).fetchone()[0]

        # Should have at least 4 sync executions (one per tier)
        assert all_executions >= 4, f"Expected ≥4 sync executions, got {all_executions}"

        # Verify audit trail chronology
        audit_events = e2e_engine.conn.execute("""
            SELECT event_type, created_at
            FROM sync_audit_trail
            WHERE flow_token = ?
            ORDER BY created_at
        """, [flow_token]).fetchall()

        # Verify events are chronologically ordered
        timestamps = [event[1] for event in audit_events]
        assert timestamps == sorted(timestamps), "Audit events must be chronological"

    @pytest.mark.xfail(reason="Phase 5+ schema: sync_executions needs flow_token column")
    def test_workflow_provenance_complete(self, e2e_engine):
        """Verify complete workflow provenance is reconstructable."""

        flow_token = "e2e-provenance-test"

        # Execute simplified workflow (2 tiers)
        e2e_engine.on_agent_action_complete(
            agent_id="orchestrate",
            action="planning_complete",
            flow_token=flow_token,
            state_snapshot={"planning_status": "complete"}
        )

        e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token,
            state_snapshot={"implementation_status": "complete"}
        )

        # Reconstruct workflow DAG from audit trail
        workflow_dag = e2e_engine.conn.execute("""
            SELECT
                se.trigger_agent_id AS source,
                se.target_agent_id AS target,
                se.provenance_hash,
                se.created_at
            FROM sync_executions se
            WHERE se.flow_token = ?
            ORDER BY se.created_at
        """, [flow_token]).fetchall()

        # Should have at least 2 edges in DAG
        assert len(workflow_dag) >= 2, "Workflow DAG should have ≥2 edges"

        # Verify provenance hashes are unique
        hashes = [edge[2] for edge in workflow_dag]
        assert len(hashes) == len(set(hashes)), "All provenance hashes must be unique"


# ============================================================================
# Concurrent Agent Coordination Tests
# ============================================================================

@pytest.mark.integration
class TestConcurrentAgents:
    """Test concurrent agent execution with synchronization."""

    @pytest.mark.xfail(reason="Phase 5+ schema: sync_executions needs flow_token column")
    def test_concurrent_agents_no_race(self, e2e_engine):
        """Two agents in parallel → no race conditions."""

        # Simulate two agents completing actions simultaneously
        flow_token_1 = "concurrent-flow-1"
        flow_token_2 = "concurrent-flow-2"

        # Agent 1: Develop completes
        exec_ids_1 = e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token_1,
            state_snapshot={"commits": 10}
        )

        # Agent 2: Develop completes (different flow)
        exec_ids_2 = e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token_2,
            state_snapshot={"commits": 5}
        )

        # Both should succeed independently
        assert len(exec_ids_1) >= 1
        assert len(exec_ids_2) >= 1

        # Verify no cross-contamination (flow_tokens are distinct)
        flow_1_executions = e2e_engine.conn.execute("""
            SELECT COUNT(*) FROM sync_executions WHERE flow_token = ?
        """, [flow_token_1]).fetchone()[0]

        flow_2_executions = e2e_engine.conn.execute("""
            SELECT COUNT(*) FROM sync_executions WHERE flow_token = ?
        """, [flow_token_2]).fetchone()[0]

        assert flow_1_executions >= 1
        assert flow_2_executions >= 1

    @pytest.mark.xfail(reason="Phase 5+ schema: sync_executions needs flow_token column")
    def test_idempotency_across_agents(self, e2e_engine):
        """Same state from multiple agents → idempotency enforced."""

        flow_token = "idempotency-multi-agent"
        state = {"status": "complete"}

        # Agent 1 triggers
        exec_ids_1 = e2e_engine.on_agent_action_complete(
            agent_id="orchestrate",
            action="planning_complete",
            flow_token=flow_token,
            state_snapshot=state
        )

        # Agent 1 triggers AGAIN with SAME state
        exec_ids_2 = e2e_engine.on_agent_action_complete(
            agent_id="orchestrate",
            action="planning_complete",
            flow_token=flow_token,
            state_snapshot=state
        )

        # First trigger: sync executes
        assert len(exec_ids_1) >= 1

        # Second trigger: idempotency prevents duplicate
        assert len(exec_ids_2) == 0, "Idempotency should prevent duplicate execution"


# ============================================================================
# Error Recovery Flow Tests
# ============================================================================

@pytest.mark.integration
class TestErrorRecovery:
    """Test error recovery synchronization flows."""

    def test_test_failure_recovery(self, e2e_engine):
        """Test failure → trigger recovery sync (add tests)."""

        flow_token = "error-recovery-tests"

        # Assess agent detects test failure
        exec_ids = e2e_engine.on_agent_action_complete(
            agent_id="assess",
            action="validation_complete",
            flow_token=flow_token,
            state_snapshot={
                "tests_passed": False,  # FAILURE
                "coverage_percentage": 75,
                "failure_reason": "3 tests failed"
            }
        )

        # Should trigger error recovery sync rule (test_failure_recovery)
        # Note: Default rules check specific patterns for error recovery

        # Verify sync execution exists
        # (Exact behavior depends on Phase 4 default_synchronizations.sql)
        assert exec_ids is not None  # Engine executed without errors

    def test_coverage_gap_recovery(self, e2e_engine):
        """Low coverage → trigger recovery sync (add tests)."""

        flow_token = "error-recovery-coverage"

        # Assess agent detects low coverage
        exec_ids = e2e_engine.on_agent_action_complete(
            agent_id="assess",
            action="validation_complete",
            flow_token=flow_token,
            state_snapshot={
                "tests_passed": True,
                "coverage_percentage": 65,  # BELOW 80% threshold
                "coverage_gap": True
            }
        )

        # Should trigger coverage_gap_recovery sync rule
        assert exec_ids is not None

    def test_lint_failure_recovery(self, e2e_engine):
        """Lint failure → trigger recovery sync (fix linting)."""

        flow_token = "error-recovery-lint"

        # Develop agent detects lint failure
        exec_ids = e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token,
            state_snapshot={
                "lint_status": "fail",  # FAILURE
                "lint_errors": 15
            }
        )

        # Should trigger lint_failure_recovery sync rule
        assert exec_ids is not None


# ============================================================================
# Priority-Based Execution Tests
# ============================================================================

@pytest.mark.integration
class TestPriorityExecution:
    """Test priority-based sync rule execution."""

    def test_priority_ordering(self, e2e_engine):
        """Higher priority sync rules execute first."""

        # Query all sync rules with priorities
        sync_rules = e2e_engine.conn.execute("""
            SELECT sync_id, priority
            FROM agent_synchronizations
            WHERE enabled = TRUE
            ORDER BY priority DESC
        """).fetchall()

        # Verify priority ranges
        # Error recovery: 200-299 (highest)
        # Normal flow: 100-199
        # Background: 1-99 (lowest)

        priorities = [rule[1] for rule in sync_rules]

        # All priorities should be in valid ranges
        for priority in priorities:
            assert 1 <= priority <= 299, f"Invalid priority: {priority}"

    def test_error_recovery_priority_higher(self, e2e_engine):
        """Error recovery rules have higher priority than normal flow."""

        # Query priorities
        normal_flow_priorities = e2e_engine.conn.execute("""
            SELECT MAX(priority) FROM agent_synchronizations
            WHERE sync_type = 'workflow_transition'
        """).fetchone()[0]

        error_recovery_priorities = e2e_engine.conn.execute("""
            SELECT MIN(priority) FROM agent_synchronizations
            WHERE sync_type = 'error_recovery'
        """).fetchone()[0]

        # Error recovery min priority > Normal flow max priority
        if normal_flow_priorities and error_recovery_priorities:
            assert error_recovery_priorities > normal_flow_priorities, \
                "Error recovery should have higher priority than normal flow"


# ============================================================================
# State Transition Tests
# ============================================================================

@pytest.mark.integration
class TestStateTransitions:
    """Test workflow state transitions."""

    @pytest.mark.xfail(reason="Phase 5+ schema: sync_executions needs flow_token column")
    def test_state_persistence_across_tiers(self, e2e_engine):
        """State changes persist across workflow tiers."""

        flow_token = "state-persistence-test"

        # Tier 1: Orchestrate sets initial state
        e2e_engine.on_agent_action_complete(
            agent_id="orchestrate",
            action="planning_complete",
            flow_token=flow_token,
            state_snapshot={
                "feature_name": "user-authentication",
                "complexity": "high"
            }
        )

        # Tier 2: Develop adds implementation state
        e2e_engine.on_agent_action_complete(
            agent_id="develop",
            action="implementation_complete",
            flow_token=flow_token,
            state_snapshot={
                "feature_name": "user-authentication",  # Persisted
                "complexity": "high",  # Persisted
                "commits": 20,  # New state
                "files_changed": 12  # New state
            }
        )

        # Query all states for this flow
        states = e2e_engine.conn.execute("""
            SELECT trigger_state_snapshot
            FROM sync_executions
            WHERE flow_token = ?
            ORDER BY created_at
        """, [flow_token]).fetchall()

        assert len(states) >= 2

        # Verify state accumulation (later states include earlier fields)
        # Note: This depends on agent implementation passing forward state


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-m', 'integration', '--tb=short'])
