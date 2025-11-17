#!/usr/bin/env python3
"""Test suite for MIT Agent Synchronization Engine

Success Criteria (Gate 2):
- Unit test coverage ≥85%
- Pattern matching: 100% test pass rate
- Idempotency: Zero duplicates in 10k iteration test
- Parameter substitution: Nested paths handled correctly
- Error handling: No unhandled exceptions
- Performance: <100ms p95 latency (baseline benchmark)

Created: 2025-11-17
Issue: #160 - Phase 2 Synchronization Engine Implementation
"""

import json

# Import the module to test
import sys
import time
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'scripts'))

from sync_engine import SynchronizationEngine


@pytest.fixture
def test_db(tmp_path):
    """Create test database with Phase 1 schema + Phase 2 migration."""
    db_path = tmp_path / "test.duckdb"
    conn = duckdb.connect(str(db_path))

    # Load Phase 1 schema
    schema_path = Path(".claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql")
    with open(schema_path) as f:
        conn.execute(f.read())

    # Load Phase 2 migration
    migration_path = Path(".claude/skills/agentdb-state-manager/schemas/phase2_migration.sql")
    with open(migration_path) as f:
        conn.execute(f.read())

    # Populate test data
    _populate_test_data(conn)

    conn.close()
    return str(db_path)


def _populate_test_data(conn):
    """Populate test database with sample synchronization rules."""

    # Sample sync rule 1: develop.commit_complete → assess.run_tests
    # Trigger when lint_status = "pass"
    conn.execute("""
        INSERT INTO agent_synchronizations (
            sync_id,
            agent_id,
            trigger_agent_id,
            trigger_action,
            trigger_pattern,
            target_agent_id,
            target_action,
            priority,
            enabled,
            worktree_path,
            sync_type,
            source_location,
            target_location,
            pattern,
            status,
            created_by,
            metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        'sync-001',
        'develop',
        'develop',
        'commit_complete',
        json.dumps({"lint_status": "pass"}),
        'assess',
        'run_tests',
        100,
        True,
        None,
        'agent_sync',
        'worktree',
        'main',
        'commit_complete',
        'pending',
        'test_setup',
        json.dumps({})
    ])

    # Sample sync rule 2: develop.commit_complete → assess.run_tests
    # Trigger when coverage.percentage >= 85 (NOTE: pattern match doesn't support >=, just equality)
    # For testing, we'll use exact match {"coverage": {"percentage": 85}}
    conn.execute("""
        INSERT INTO agent_synchronizations (
            sync_id,
            agent_id,
            trigger_agent_id,
            trigger_action,
            trigger_pattern,
            target_agent_id,
            target_action,
            priority,
            enabled,
            worktree_path,
            sync_type,
            source_location,
            target_location,
            pattern,
            status,
            created_by,
            metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        'sync-002',
        'develop',
        'develop',
        'commit_complete',
        json.dumps({"coverage": {"percentage": 85}}),
        'assess',
        'run_coverage_report',
        90,
        True,
        None,
        'agent_sync',
        'worktree',
        'main',
        'commit_complete',
        'pending',
        'test_setup',
        json.dumps({})
    ])

    # Sample sync rule 3: assess.test_passed → integrate.create_pr
    # No pattern (matches any state)
    conn.execute("""
        INSERT INTO agent_synchronizations (
            sync_id,
            agent_id,
            trigger_agent_id,
            trigger_action,
            trigger_pattern,
            target_agent_id,
            target_action,
            priority,
            enabled,
            worktree_path,
            sync_type,
            source_location,
            target_location,
            pattern,
            status,
            created_by,
            metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        'sync-003',
        'assess',
        'assess',
        'test_passed',
        json.dumps({}),  # Empty pattern matches all
        'integrate',
        'create_pr',
        100,
        True,
        None,
        'agent_sync',
        'worktree',
        'main',
        'test_passed',
        'pending',
        'test_setup',
        json.dumps({})
    ])

    # Sample sync rule 4: DISABLED rule (should not match)
    conn.execute("""
        INSERT INTO agent_synchronizations (
            sync_id,
            agent_id,
            trigger_agent_id,
            trigger_action,
            trigger_pattern,
            target_agent_id,
            target_action,
            priority,
            enabled,
            worktree_path,
            sync_type,
            source_location,
            target_location,
            pattern,
            status,
            created_by,
            metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        'sync-004-disabled',
        'develop',
        'develop',
        'commit_complete',
        json.dumps({}),
        'assess',
        'should_not_trigger',
        100,
        False,  # DISABLED
        None,
        'agent_sync',
        'worktree',
        'main',
        'commit_complete',
        'pending',
        'test_setup',
        json.dumps({})
    ])


@pytest.fixture
def sync_engine(test_db):
    """Create SynchronizationEngine instance."""
    engine = SynchronizationEngine(db_path=test_db)
    yield engine
    engine.close()


# ============================================================================
# Pattern Matching Tests
# ============================================================================

class TestPatternMatching:
    """Test pattern matching correctness (100% pass rate required)."""

    def test_exact_match(self, sync_engine):
        """State exactly equals pattern → sync triggers."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with exact state {"lint_status": "pass"}
        # Expected: Sync matches and triggers

        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-001",
            state_snapshot={"lint_status": "pass"}
        )

        assert len(execution_ids) == 1  # Only sync-001 should match

    def test_partial_match(self, sync_engine):
        """State ⊃ pattern → sync triggers (state contains pattern)."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with superset {"lint_status": "pass", "coverage": 85}
        # Expected: Sync matches (partial match)

        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-002",
            state_snapshot={
                "lint_status": "pass",
                "coverage": 75  # Different from sync-002's pattern
            }
        )

        assert len(execution_ids) == 1  # Only sync-001 matches

    def test_no_match(self, sync_engine):
        """State ⊄ pattern → sync does not trigger."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with {"lint_status": "fail"}
        # Expected: Sync does NOT match

        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-003",
            state_snapshot={"lint_status": "fail"}
        )

        assert len(execution_ids) == 0  # No match

    def test_nested_pattern_match(self, sync_engine):
        """Nested pattern matching works correctly."""
        # Setup: sync-002 has nested pattern {"coverage": {"percentage": 85}}
        # Action: Trigger with matching nested state
        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-004",
            state_snapshot={
                "coverage": {"percentage": 85, "lines_covered": 1234}
            }
        )

        assert len(execution_ids) == 1  # sync-002 should match

    def test_multiple_matches(self, sync_engine):
        """Multiple sync rules can match same trigger."""
        # sync-001 requires {"lint_status": "pass"}
        # sync-002 requires {"coverage": {"percentage": 85}}
        # If state has BOTH, both should match

        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-005",
            state_snapshot={
                "lint_status": "pass",
                "coverage": {"percentage": 85}
            }
        )

        assert len(execution_ids) == 2  # Both sync-001 and sync-002 match

    def test_empty_pattern_matches_all(self, sync_engine):
        """Empty pattern {} matches any state."""
        # sync-003 has empty pattern
        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="assess",
            action="test_passed",
            flow_token="test-flow-006",
            state_snapshot={"random": "data"}
        )

        assert len(execution_ids) == 1  # sync-003 matches

    def test_disabled_rule_not_matched(self, sync_engine):
        """Disabled sync rules (enabled=FALSE) are not matched."""
        # sync-004-disabled is disabled
        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-007",
            state_snapshot={}
        )

        # sync-004 should NOT be included (disabled)
        # No enabled rules match empty state for develop.commit_complete
        assert len(execution_ids) == 0


# ============================================================================
# Idempotency Tests
# ============================================================================

class TestIdempotency:
    """Test idempotency enforcement (zero duplicates required)."""

    def test_duplicate_state_single_execution(self, sync_engine):
        """Same state twice → only one execution recorded."""
        state = {"lint_status": "pass"}

        # First execution
        exec_ids_1 = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-dup",
            state_snapshot=state
        )

        # Second execution with SAME state
        exec_ids_2 = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-dup",
            state_snapshot=state
        )

        assert len(exec_ids_1) == 1
        assert len(exec_ids_2) == 0  # Idempotency: no duplicate

    def test_different_state_multiple_executions(self, sync_engine):
        """Different states → multiple executions."""
        # First state
        exec_ids_1 = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-diff",
            state_snapshot={"lint_status": "pass", "version": 1}
        )

        # Second state (different)
        exec_ids_2 = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-diff",
            state_snapshot={"lint_status": "pass", "version": 2}
        )

        assert len(exec_ids_1) == 1
        assert len(exec_ids_2) == 1  # Different state → new execution

    def test_10k_iterations_idempotency(self, sync_engine):
        """10,000 iterations with duplicates → count unique executions.

        Success Criteria: Zero duplicate executions (idempotency enforced)
        """
        # Generate 10,000 states (with many duplicates)
        states = []
        for i in range(10000):
            # Create states with ~1000 unique values (10x duplication)
            states.append({
                "lint_status": "pass",
                "iteration": i % 1000  # Only 1000 unique values
            })

        # Trigger 10,000 times
        all_exec_ids = []
        for i, state in enumerate(states):
            exec_ids = sync_engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-flow-10k",
                state_snapshot=state
            )
            all_exec_ids.extend(exec_ids)

            # Progress indicator (every 1000 iterations)
            if (i + 1) % 1000 == 0:
                print(f"  Processed {i + 1}/10000 iterations...")

        # Count unique executions in database
        unique_count = sync_engine.conn.execute("""
            SELECT COUNT(DISTINCT provenance_hash) FROM sync_executions
            WHERE sync_id = 'sync-001'
        """).fetchone()[0]

        # Should be ~1000 unique executions (not 10,000)
        assert unique_count <= 1000, f"Expected ≤1000 unique, got {unique_count}"
        assert unique_count >= 950, f"Expected ≥950 unique (allowing variance), got {unique_count}"

        # Verify zero duplicate provenance hashes
        dup_check = sync_engine.conn.execute("""
            SELECT provenance_hash, COUNT(*) as cnt
            FROM sync_executions
            GROUP BY provenance_hash
            HAVING COUNT(*) > 1
        """).fetchall()

        assert len(dup_check) == 0, f"Found duplicate hashes: {dup_check}"


# ============================================================================
# Parameter Substitution Tests
# ============================================================================

class TestParameterSubstitution:
    """Test ${trigger_state.path} template substitution."""

    def test_simple_path(self, sync_engine):
        """${state.field} → extract field."""
        action_spec = {
            "message": "Lint: ${trigger_state.lint_status}"
        }
        trigger_state = {"lint_status": "pass"}

        result = sync_engine._resolve_params(action_spec, trigger_state)

        assert result["message"] == "Lint: pass"

    def test_nested_path(self, sync_engine):
        """${state.nested.field} → extract nested value."""
        action_spec = {
            "message": "Coverage: ${trigger_state.coverage.percentage}%"
        }
        trigger_state = {
            "coverage": {"percentage": 85, "lines": 1234}
        }

        result = sync_engine._resolve_params(action_spec, trigger_state)

        assert result["message"] == "Coverage: 85%"

    def test_missing_path_returns_null(self, sync_engine):
        """${state.nonexistent} → null + warning log."""
        action_spec = {
            "value": "${trigger_state.missing.field}"
        }
        trigger_state = {"lint_status": "pass"}

        result = sync_engine._resolve_params(action_spec, trigger_state)

        assert result["value"] == "null"

    def test_multiple_substitutions(self, sync_engine):
        """Multiple ${...} in same string."""
        action_spec = {
            "message": "Lint: ${trigger_state.lint}, Coverage: ${trigger_state.coverage}%"
        }
        trigger_state = {"lint": "pass", "coverage": 85}

        result = sync_engine._resolve_params(action_spec, trigger_state)

        assert result["message"] == "Lint: pass, Coverage: 85%"


# ============================================================================
# Provenance Hash Tests
# ============================================================================

class TestProvenanceHash:
    """Test hash computation stability and determinism."""

    def test_hash_determinism(self, sync_engine):
        """Same input → same hash (100 iterations)."""
        sync_id = "sync-001"
        flow_token = "test-flow"
        state = {"coverage": {"percentage": 85}}

        hashes = []
        for _ in range(100):
            h = sync_engine._compute_provenance_hash(sync_id, flow_token, state)
            hashes.append(h)

        # All hashes must be identical
        assert len(set(hashes)) == 1
        assert len(hashes[0]) == 64  # SHA-256 hex = 64 chars

    def test_hash_json_normalization(self, sync_engine):
        """Different key order → same hash (sort_keys=True)."""
        sync_id = "sync-001"
        flow_token = "test-flow"

        # Same data, different key order
        state1 = {"coverage": 85, "lint": "pass"}
        state2 = {"lint": "pass", "coverage": 85}

        hash1 = sync_engine._compute_provenance_hash(sync_id, flow_token, state1)
        hash2 = sync_engine._compute_provenance_hash(sync_id, flow_token, state2)

        assert hash1 == hash2

    def test_hash_different_inputs(self, sync_engine):
        """Different inputs → different hashes."""
        sync_id = "sync-001"
        flow_token = "test-flow"

        state1 = {"coverage": 85}
        state2 = {"coverage": 86}

        hash1 = sync_engine._compute_provenance_hash(sync_id, flow_token, state1)
        hash2 = sync_engine._compute_provenance_hash(sync_id, flow_token, state2)

        assert hash1 != hash2

    def test_hash_performance(self, sync_engine):
        """Hash computation: <1ms p99."""
        sync_id = "sync-001"
        flow_token = "test-flow"
        state = {"coverage": {"percentage": 85, "lines": 1234}}

        # Measure 1000 iterations
        times = []
        for _ in range(1000):
            start = time.perf_counter()
            sync_engine._compute_provenance_hash(sync_id, flow_token, state)
            times.append((time.perf_counter() - start) * 1000)  # Convert to ms

        # Calculate p99
        times.sort()
        p99 = times[int(len(times) * 0.99)]

        assert p99 < 1.0, f"p99 latency {p99:.2f}ms exceeds 1ms target"


# ============================================================================
# Performance Baseline Tests
# ============================================================================

class TestPerformance:
    """Performance baseline benchmarks."""

    def test_latency_single_agent(self, sync_engine):
        """Measure p50, p95, p99 latency for single agent.

        Goal: <100ms p95 latency
        """
        state = {"lint_status": "pass"}
        latencies = []

        # Measure 100 iterations
        for i in range(100):
            start = time.perf_counter()

            sync_engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token=f"test-perf-{i}",
                state_snapshot=state
            )

            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)

        # Calculate percentiles
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]

        print(f"\nSingle agent latency: p50={p50:.2f}ms, p95={p95:.2f}ms, p99={p99:.2f}ms")

        assert p95 < 100.0, f"p95 latency {p95:.2f}ms exceeds 100ms target"


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error scenarios don't raise unhandled exceptions."""

    def test_no_matching_action(self, sync_engine):
        """Non-existent action → returns empty list gracefully."""
        # Should not crash
        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="nonexistent_agent",
            action="nonexistent_action",
            flow_token="test-error",
            state_snapshot={"test": "data"}
        )

        # Should return empty list (no matches)
        assert execution_ids == []


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """End-to-end integration tests."""

    def test_full_workflow(self, sync_engine):
        """Complete workflow: trigger → match → execute → audit."""

        # Trigger action
        execution_ids = sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-integration",
            state_snapshot={
                "lint_status": "pass",
                "coverage": {"percentage": 85}
            }
        )

        # Should match both sync-001 and sync-002
        assert len(execution_ids) == 2

        # Verify executions in database
        for exec_id in execution_ids:
            result = sync_engine.conn.execute(
                "SELECT execution_id, exec_status FROM sync_executions WHERE execution_id = ?",
                [exec_id]
            ).fetchone()

            assert result is not None
            assert result[1] == 'pending'

        # Verify audit trail logged
        audit_count = sync_engine.conn.execute(
            "SELECT COUNT(*) FROM sync_audit_trail WHERE event_type = 'sync_initiated'"
        ).fetchone()[0]

        assert audit_count >= 2  # At least 2 audit entries

    def test_context_manager(self, test_db):
        """Test SynchronizationEngine as context manager."""

        with SynchronizationEngine(db_path=test_db) as engine:
            execution_ids = engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-context",
                state_snapshot={"lint_status": "pass"}
            )

            assert len(execution_ids) >= 1

        # Connection should be closed after context exit
        # (Can't easily test this in DuckDB, but code coverage will show it's called)
