---
type: workflow-manifest
workflow_type: feature
slug: phase-2-engine
github_user: stharrold
created_at: "2025-11-17T02:43:49Z"

related_issues:
  - number: 160
    title: "Phase 2 - Synchronization Engine Implementation"
    url: "https://github.com/stharrold/german/issues/160"
    status: open
    labels: ["phase-2-engine", "blocked", "parallel-ok", "enhancement"]
  - number: 158
    title: "Autonomous Implementation - MIT Agent Synchronization Pattern"
    url: "https://github.com/stharrold/german/issues/158"
    status: open
    labels: ["MIT-sync-pattern"]

workflow_progress:
  phase: 2
  current_step: "0.0"
  last_task: null
  blocked_by: "Schema migration required"

dependencies:
  completed:
    - issue: 159
      title: "Phase 1 - Database Schema"
      status: "✅ Completed in v1.10.0"
  can_parallelize_with:
    - issue: 161
      title: "Phase 3 - Integration Layer"
      time_savings: "40-47% reduction (12-16h parallel vs 22-30h sequential)"

estimated_effort:
  total_hours: "12-16"
  breakdown:
    schema_migration: "2-3"
    core_implementation: "6-8"
    testing: "3-4"
    documentation: "1"

quality_gates:
  test_coverage: null
  tests_passing: null
  semantic_version: null

tasks:
  schema_migration:
    - id: schema_001
      name: "Analyze schema mismatch between Phase 1 and Phase 2 requirements"
      status: pending
      priority: critical
      estimated_hours: 0.5
    - id: schema_002
      name: "Create SQL migration script to add missing fields"
      status: pending
      priority: critical
      estimated_hours: 1
      depends_on: [schema_001]
    - id: schema_003
      name: "Test migration on copy of Phase 1 database"
      status: pending
      priority: critical
      estimated_hours: 0.5
      depends_on: [schema_002]
    - id: schema_004
      name: "Update test_schema_migration.py to validate new fields"
      status: pending
      priority: high
      estimated_hours: 1
      depends_on: [schema_003]

  core_implementation:
    - id: impl_001
      name: "Implement _compute_provenance_hash() method"
      status: pending
      priority: high
      estimated_hours: 1
      file: ".claude/skills/agentdb-state-manager/scripts/sync_engine.py"
    - id: impl_002
      name: "Implement _resolve_params() method"
      status: pending
      priority: high
      estimated_hours: 1
      file: ".claude/skills/agentdb-state-manager/scripts/sync_engine.py"
    - id: impl_003
      name: "Adapt DuckDB JSON query patterns"
      status: pending
      priority: critical
      estimated_hours: 2
      notes: "Replace PostgreSQL JSONB @> operator with DuckDB JSON functions"
    - id: impl_004
      name: "Implement _find_matching_syncs() method"
      status: pending
      priority: high
      estimated_hours: 2
      depends_on: [impl_003]
      file: ".claude/skills/agentdb-state-manager/scripts/sync_engine.py"
    - id: impl_005
      name: "Implement _execute_sync() method"
      status: pending
      priority: high
      estimated_hours: 1
      depends_on: [impl_002]
      file: ".claude/skills/agentdb-state-manager/scripts/sync_engine.py"
    - id: impl_006
      name: "Implement on_agent_action_complete() method"
      status: pending
      priority: high
      estimated_hours: 1
      depends_on: [impl_001, impl_004, impl_005]
      file: ".claude/skills/agentdb-state-manager/scripts/sync_engine.py"

  testing:
    - id: test_001
      name: "Create test fixture and database setup"
      status: pending
      priority: high
      estimated_hours: 0.5
      file: "tests/skills/test_sync_engine.py"
    - id: test_002
      name: "Implement pattern matching tests"
      status: pending
      priority: high
      estimated_hours: 1
      file: "tests/skills/test_sync_engine.py"
    - id: test_003
      name: "Implement idempotency tests (10k iterations)"
      status: pending
      priority: critical
      estimated_hours: 1
      file: "tests/skills/test_sync_engine.py"
    - id: test_004
      name: "Implement parameter substitution tests"
      status: pending
      priority: high
      estimated_hours: 0.5
      file: "tests/skills/test_sync_engine.py"
    - id: test_005
      name: "Implement performance baseline benchmarks"
      status: pending
      priority: high
      estimated_hours: 1
      notes: "<100ms p95 single agent, <200ms p95 for 13 concurrent"

  documentation:
    - id: doc_001
      name: "Add inline type hints and docstrings"
      status: pending
      priority: medium
      estimated_hours: 0.5
    - id: doc_002
      name: "Create integration guide for Phase 3"
      status: pending
      priority: medium
      estimated_hours: 0.5

success_criteria:
  - criterion: "Unit test coverage ≥85%"
    status: pending
  - criterion: "Pattern matching: 100% test pass rate"
    status: pending
  - criterion: "Idempotency: Zero duplicates in 10k iteration test"
    status: pending
  - criterion: "Parameter substitution: Nested paths handled correctly"
    status: pending
  - criterion: "Error handling: No unhandled exceptions"
    status: pending
  - criterion: "Performance: <100ms p95 latency for single agent"
    status: pending
  - criterion: "DuckDB compatibility validated"
    status: pending
  - criterion: "Healthcare compliance logging working"
    status: pending
---

# Phase 2 - Synchronization Engine Implementation

**Issue**: #160 - MIT Agent Synchronization Pattern (Phase 2)
**Status**: Ready to implement (Phase 1 completed ✅)
**Effort**: 12-16 hours
**Can parallelize with**: Phase 3 (#161) for 40-47% time savings

## Executive Summary

This TODO tracks the implementation of the MIT Agent Synchronization Engine - the core coordination layer for multi-agent workflows with declarative pattern matching, idempotency enforcement, and healthcare compliance.

**⚠️ CRITICAL BLOCKER**: Schema mismatch between Phase 1 implementation and Phase 2 requirements must be resolved first.

## 1. Overview

### What is Phase 2?

Phase 2 implements the **Synchronization Engine** - the core runtime component that:
- Monitors agent actions (commits, tests, deployments)
- Matches actions against declarative synchronization rules
- Triggers target agents with computed parameters
- Enforces idempotency via content-addressed hashing
- Logs all operations for healthcare compliance (HIPAA/FDA/IRB)

### Parent Issue Context

From **Issue #158 - MIT Agent Synchronization Pattern**:

This is a 6-phase implementation plan for autonomous multi-agent coordination:
- Phase 1 (#159): Database Schema ✅ **COMPLETED in v1.10.0**
- Phase 2 (#160): **Synchronization Engine** ← THIS WORK
- Phase 3 (#161): Integration Layer (can parallelize)
- Phase 4 (#162): Default Synchronization Rules
- Phase 5 (#163): Testing and Compliance Validation (can parallelize with Phase 6)
- Phase 6 (#164): Performance Validation and Documentation

### Dependencies

**Phase 1 Completion** ✅ **DONE**
- Database schema implemented (agentdb_sync_schema.sql, 458 lines)
- 3 core tables created with 20+ indexes
- Test suite with 557 test cases
- HIPAA/FDA/IRB compliance documentation
- PRs #165, #173, #179 merged to main
- All Phase 1 issues (#159, #167-#172) closed in v1.10.0-v1.10.1

**Blocks**: Phase 4 (#162) - Default Synchronization Rules

**Can Parallelize With**: Phase 3 (#161) - Integration Layer
- Different files, minimal overlap
- Time savings: 40-47% reduction (12-16h parallel vs 22-30h sequential)

## 2. CRITICAL: Schema Migration Required

### The Problem

**Schema Mismatch Discovered:**

Issue #160 (written for PostgreSQL) expects:
```sql
-- Expected by Phase 2
CREATE TABLE agent_synchronizations (
  sync_id UUID PRIMARY KEY,
  trigger_agent_id VARCHAR NOT NULL,
  trigger_action VARCHAR NOT NULL,
  trigger_pattern JSONB NOT NULL,
  target_agent_id VARCHAR NOT NULL,
  target_action VARCHAR NOT NULL,
  priority INTEGER DEFAULT 100,
  enabled BOOLEAN DEFAULT TRUE,
  ...
);

CREATE TABLE sync_executions (
  execution_id UUID PRIMARY KEY,
  sync_id UUID REFERENCES agent_synchronizations(sync_id),
  provenance_hash VARCHAR(64) UNIQUE NOT NULL,
  trigger_state_snapshot JSONB NOT NULL,
  status VARCHAR CHECK (status IN ('pending', 'completed', 'failed')),
  ...
);
```

Phase 1 (v1.10.0) actually implemented (in DuckDB):
```sql
-- Actual Phase 1 schema
CREATE TABLE agent_synchronizations (
  sync_id VARCHAR PRIMARY KEY,
  agent_id VARCHAR NOT NULL,
  worktree_path VARCHAR,
  sync_type VARCHAR NOT NULL,
  pattern VARCHAR NOT NULL,
  status VARCHAR CHECK (...),
  created_at TIMESTAMP,
  ...
);

CREATE TABLE sync_executions (
  execution_id VARCHAR PRIMARY KEY,
  sync_id VARCHAR REFERENCES agent_synchronizations(sync_id),
  execution_order INTEGER NOT NULL,
  operation_type VARCHAR CHECK (...),
  -- NO provenance_hash field
  -- NO trigger_state_snapshot field
  -- NO status field
  ...
);
```

**Missing fields:**
- `trigger_agent_id`, `trigger_action`, `trigger_pattern` (JSON)
- `target_agent_id`, `target_action`, `priority`, `enabled`
- `provenance_hash` (UNIQUE), `trigger_state_snapshot` (JSON), `status`

### Migration Solution

**Task**: schema_002 - Create SQL migration script

**File**: `.claude/skills/agentdb-state-manager/schemas/phase2_migration.sql`

```sql
-- Phase 2 Schema Migration
-- Adds MIT Agent Synchronization Pattern fields to Phase 1 schema

-- Add missing fields to agent_synchronizations
ALTER TABLE agent_synchronizations
  ADD COLUMN trigger_agent_id VARCHAR,
  ADD COLUMN trigger_action VARCHAR,
  ADD COLUMN trigger_pattern JSON,
  ADD COLUMN target_agent_id VARCHAR,
  ADD COLUMN target_action VARCHAR,
  ADD COLUMN priority INTEGER DEFAULT 100,
  ADD COLUMN enabled BOOLEAN DEFAULT TRUE;

-- Add missing fields to sync_executions
ALTER TABLE sync_executions
  ADD COLUMN provenance_hash VARCHAR(64) UNIQUE,
  ADD COLUMN trigger_state_snapshot JSON,
  ADD COLUMN exec_status VARCHAR CHECK (exec_status IN ('pending', 'completed', 'failed'));

-- Create indexes for performance
CREATE INDEX idx_sync_trigger ON agent_synchronizations(trigger_agent_id, trigger_action);
CREATE INDEX idx_sync_enabled ON agent_synchronizations(enabled) WHERE enabled = TRUE;
CREATE INDEX idx_exec_provenance ON sync_executions(provenance_hash);
CREATE INDEX idx_exec_status ON sync_executions(exec_status);

-- Add comment explaining migration
COMMENT ON TABLE agent_synchronizations IS
  'Synchronization rules for MIT Agent Pattern. Extended in Phase 2 with trigger/target fields.';
```

**Validation**:
```bash
# Test migration
duckdb test.db < .claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql
duckdb test.db < .claude/skills/agentdb-state-manager/schemas/phase2_migration.sql

# Verify fields exist
duckdb test.db -c "PRAGMA table_info(agent_synchronizations);"
duckdb test.db -c "PRAGMA table_info(sync_executions);"
```

**Update test suite**:
```python
# tests/skills/test_schema_migration.py
def test_phase2_fields_exist():
    """Verify Phase 2 migration added required fields."""
    conn = duckdb.connect(':memory:')

    # Load Phase 1 schema
    with open('.claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql') as f:
        conn.execute(f.read())

    # Load Phase 2 migration
    with open('.claude/skills/agentdb-state-manager/schemas/phase2_migration.sql') as f:
        conn.execute(f.read())

    # Verify agent_synchronizations fields
    result = conn.execute("PRAGMA table_info(agent_synchronizations)").fetchall()
    field_names = [row[1] for row in result]

    assert 'trigger_agent_id' in field_names
    assert 'trigger_action' in field_names
    assert 'trigger_pattern' in field_names
    assert 'target_agent_id' in field_names
    assert 'priority' in field_names
    assert 'enabled' in field_names

    # Verify sync_executions fields
    result = conn.execute("PRAGMA table_info(sync_executions)").fetchall()
    field_names = [row[1] for row in result]

    assert 'provenance_hash' in field_names
    assert 'trigger_state_snapshot' in field_names
    assert 'exec_status' in field_names
```

## 3. Core Implementation: sync_engine.py

### File Structure

**File**: `.claude/skills/agentdb-state-manager/scripts/sync_engine.py`
**Estimated Lines**: 400-600
**Language**: Python 3.11+
**Database**: DuckDB (NOT PostgreSQL - requires adaptation)

### Class Overview

```python
#!/usr/bin/env python3
"""MIT Agent Synchronization Pattern - Core Engine

Implements declarative synchronization coordination with pattern matching,
idempotency enforcement, and healthcare compliance.

Performance Requirements:
- <100ms p95 latency for single agent
- <200ms p95 latency for 13 concurrent agents
- <1ms p99 for hash computation

Healthcare Compliance:
- All PHI access logged to sync_audit_trail
- APPEND-ONLY paradigm (no deletes, no updates to history)
- Actor/role attribution for all operations
"""

import hashlib
import json
import logging
import re
from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime

import duckdb

logger = logging.getLogger(__name__)


class SynchronizationEngine:
    """Core synchronization engine for multi-agent workflows.

    Coordinates autonomous agents via declarative synchronization rules with
    pattern matching, idempotency enforcement, and healthcare compliance.

    Example Usage:
        engine = SynchronizationEngine(db_path="agentdb.duckdb")

        # Agent "develop" completed a commit
        execution_ids = await engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="worktree-20251117",
            state_snapshot={
                "commit_sha": "abc123",
                "coverage": {"percentage": 85, "lines_covered": 1234},
                "lint_status": "pass"
            }
        )

        # Returns: ['exec-uuid-1', 'exec-uuid-2'] - IDs of triggered syncs
    """

    def __init__(self, db_path: str, cache_ttl: int = 300):
        """Initialize sync engine with database connection.

        Args:
            db_path: Path to DuckDB database (e.g., "agentdb.duckdb")
            cache_ttl: Cache TTL in seconds for active syncs (default 5 minutes)
        """
        self.conn = duckdb.connect(db_path, read_only=False)
        self.cache_ttl = cache_ttl
        self._sync_cache: Dict[str, Any] = {}
        self._cache_invalidated_at: Optional[datetime] = None

    async def on_agent_action_complete(
        self,
        agent_id: str,
        action: str,
        flow_token: str,
        state_snapshot: Dict[str, Any]
    ) -> List[str]:
        """Main entry point - called after any agent action completes.

        Performance Requirements:
        - <100ms p95 latency for single agent
        - <200ms p95 latency for 13 concurrent agents

        Args:
            agent_id: Which agent triggered this (e.g., "develop", "assess")
            action: What action completed (e.g., "commit_complete", "test_passed")
            flow_token: Workflow session identifier (worktree path or issue ID)
            state_snapshot: Current state of the workflow (JSON-serializable dict)

        Returns:
            List of execution_ids (UUIDs) for triggered synchronizations

        Example:
            execution_ids = await engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="worktree-auth-system",
                state_snapshot={
                    "commit_sha": "abc123",
                    "coverage": {"percentage": 85}
                }
            )
            # Returns: ['uuid-1', 'uuid-2'] if 2 syncs matched and triggered
        """
        execution_ids = []

        # Find matching synchronization rules
        matching_syncs = await self._find_matching_syncs(agent_id, action, state_snapshot)

        for sync in matching_syncs:
            # Compute provenance hash for idempotency
            prov_hash = self._compute_provenance_hash(
                sync_id=sync['sync_id'],
                flow_token=flow_token,
                state=state_snapshot
            )

            # Check if this sync already executed for this exact state
            existing = self.conn.execute(
                "SELECT execution_id FROM sync_executions WHERE provenance_hash = ?",
                [prov_hash]
            ).fetchone()

            if existing:
                logger.info(f"Idempotency: Sync {sync['sync_id']} already executed (hash={prov_hash[:8]}...)")
                continue

            # Execute sync (trigger target agent)
            try:
                execution_id = await self._execute_sync(
                    sync=sync,
                    flow_token=flow_token,
                    trigger_state=state_snapshot,
                    prov_hash=prov_hash
                )
                execution_ids.append(execution_id)
                logger.info(f"Triggered sync {sync['sync_id']} → execution {execution_id}")
            except Exception as e:
                # Log error but don't raise (append-only paradigm)
                logger.error(f"Failed to execute sync {sync['sync_id']}: {e}")

        return execution_ids

    async def _find_matching_syncs(
        self,
        agent_id: str,
        action: str,
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find synchronization rules matching current agent/action/state.

        Query Pattern (DuckDB adapted from PostgreSQL):
            SELECT * FROM agent_synchronizations
            WHERE trigger_agent_id = ?
              AND trigger_action = ?
              AND enabled = TRUE
              -- Pattern matching via DuckDB JSON functions
            ORDER BY priority DESC

        Args:
            agent_id: Triggering agent ID
            action: Triggering action
            state: Current workflow state

        Returns:
            List of matching sync rules (ordered by priority, highest first)
        """
        # TODO: Implement caching with TTL

        # Query for matching syncs
        query = """
            SELECT
                sync_id,
                trigger_agent_id,
                trigger_action,
                trigger_pattern,
                target_agent_id,
                target_action,
                priority,
                enabled
            FROM agent_synchronizations
            WHERE trigger_agent_id = ?
              AND trigger_action = ?
              AND enabled = TRUE
            ORDER BY priority DESC
        """

        results = self.conn.execute(query, [agent_id, action]).fetchall()

        # Convert to list of dicts
        columns = ['sync_id', 'trigger_agent_id', 'trigger_action', 'trigger_pattern',
                   'target_agent_id', 'target_action', 'priority', 'enabled']
        syncs = [dict(zip(columns, row)) for row in results]

        # Filter by pattern matching (state must contain pattern)
        matched_syncs = []
        for sync in syncs:
            pattern = json.loads(sync['trigger_pattern']) if sync['trigger_pattern'] else {}

            if self._pattern_matches(pattern, state):
                matched_syncs.append(sync)

        return matched_syncs

    def _pattern_matches(self, pattern: Dict[str, Any], state: Dict[str, Any]) -> bool:
        """Check if state contains pattern (partial match).

        Pattern matching rules:
        - Empty pattern {} matches any state
        - Pattern keys must exist in state
        - Pattern values must equal state values
        - Nested dicts are matched recursively

        Examples:
            pattern = {"coverage": {"percentage": 85}}
            state = {"coverage": {"percentage": 85, "lines": 1234}, "lint": "pass"}
            result = True  # state ⊃ pattern

            pattern = {"lint": "fail"}
            state = {"lint": "pass"}
            result = False  # values don't match

        Args:
            pattern: Pattern to match (subset)
            state: Current state (superset)

        Returns:
            True if state contains pattern, False otherwise
        """
        if not pattern:
            return True  # Empty pattern matches everything

        for key, expected_value in pattern.items():
            if key not in state:
                return False

            actual_value = state[key]

            # Recursive matching for nested dicts
            if isinstance(expected_value, dict) and isinstance(actual_value, dict):
                if not self._pattern_matches(expected_value, actual_value):
                    return False
            elif expected_value != actual_value:
                return False

        return True

    async def _execute_sync(
        self,
        sync: Dict[str, Any],
        flow_token: str,
        trigger_state: Dict[str, Any],
        prov_hash: str
    ) -> str:
        """Record sync execution and trigger target agent.

        Database Operations:
        1. INSERT into sync_executions (append-only)
        2. INSERT into sync_audit_trail (compliance logging)
        3. Trigger target agent (Phase 3 integration point)

        Args:
            sync: Synchronization rule from database
            flow_token: Workflow session ID
            trigger_state: State that triggered this sync
            prov_hash: Provenance hash for idempotency

        Returns:
            execution_id (UUID string)
        """
        execution_id = str(uuid4())

        # Resolve parameters from trigger state
        # Example: "${trigger_state.coverage.percentage}" → 85
        action_spec = {
            "action": sync['target_action'],
            "agent_id": sync['target_agent_id']
        }
        resolved_params = self._resolve_params(action_spec, trigger_state)

        # Insert execution record (append-only)
        self.conn.execute("""
            INSERT INTO sync_executions (
                execution_id,
                sync_id,
                provenance_hash,
                trigger_state_snapshot,
                exec_status,
                execution_order,
                operation_type,
                metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            execution_id,
            sync['sync_id'],
            prov_hash,
            json.dumps(trigger_state),
            'pending',
            1,  # TODO: Proper sequence number
            'sync_triggered',
            json.dumps(resolved_params)
        ])

        # Log to audit trail (healthcare compliance)
        self._log_audit_trail(
            sync_id=sync['sync_id'],
            execution_id=execution_id,
            event_type='sync_triggered',
            phi_involved=self._detect_phi(trigger_state),
            event_details={
                "trigger_agent": sync['trigger_agent_id'],
                "target_agent": sync['target_agent_id'],
                "flow_token": flow_token
            }
        )

        # TODO (Phase 3): Actually trigger target agent
        # This is the integration point with Phase 3 (Integration Layer)
        # For now, just record the execution

        return execution_id

    def _compute_provenance_hash(
        self,
        sync_id: str,
        flow_token: str,
        state: Dict[str, Any]
    ) -> str:
        """Compute SHA-256 content-addressed hash for idempotency.

        Performance Target: <1ms p99

        Algorithm:
        1. Serialize state to deterministic JSON (sort_keys=True)
        2. Combine sync_id + flow_token + state_json
        3. SHA-256 hash

        Determinism Requirement:
        - Same inputs MUST produce same hash across all invocations
        - JSON key ordering must be consistent (sort_keys=True)

        Args:
            sync_id: Synchronization rule ID
            flow_token: Workflow session ID
            state: Current workflow state

        Returns:
            64-character hex string (SHA-256 hash)

        Example:
            hash = _compute_provenance_hash(
                sync_id="sync-123",
                flow_token="worktree-auth",
                state={"coverage": {"percentage": 85}}
            )
            # Returns: "a3f2b8..." (64 chars)
        """
        # Deterministic JSON serialization (sort keys)
        state_json = json.dumps(state, sort_keys=True)

        # Combine components
        content = f"{sync_id}:{flow_token}:{state_json}"

        # SHA-256 hash
        hash_bytes = hashlib.sha256(content.encode('utf-8')).digest()
        return hash_bytes.hex()

    def _resolve_params(
        self,
        action_spec: Dict[str, Any],
        trigger_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve ${trigger_state.path} placeholders in action spec.

        Template Syntax:
        - Simple path: ${trigger_state.field} → extract top-level field
        - Nested path: ${trigger_state.coverage.percentage} → nested access
        - Array access: ${trigger_state.failed_tests[0]} → first element
        - Missing path: ${trigger_state.nonexistent} → null + warning log

        Args:
            action_spec: Action specification with ${...} placeholders
            trigger_state: State to extract values from

        Returns:
            Action spec with placeholders replaced by actual values

        Example:
            action_spec = {
                "action": "notify",
                "message": "Coverage: ${trigger_state.coverage.percentage}%"
            }
            trigger_state = {"coverage": {"percentage": 85}}

            result = _resolve_params(action_spec, trigger_state)
            # Returns: {"action": "notify", "message": "Coverage: 85%"}
        """
        # Convert to JSON string for regex replacement
        spec_json = json.dumps(action_spec)

        # Pattern: ${trigger_state.path.to.value}
        pattern = r'\$\{trigger_state\.([^}]+)\}'

        def replacer(match):
            path = match.group(1)
            value = self._get_nested_value(trigger_state, path)

            if value is None:
                logger.warning(f"Missing path in trigger_state: {path}")
                return "null"

            return json.dumps(value) if not isinstance(value, str) else value

        # Replace all ${...} patterns
        resolved_json = re.sub(pattern, replacer, spec_json)

        return json.loads(resolved_json)

    def _get_nested_value(self, obj: Dict[str, Any], path: str) -> Any:
        """Extract nested value from dict using dot-notation path.

        Args:
            obj: Dictionary to extract from
            path: Dot-notation path (e.g., "coverage.percentage")

        Returns:
            Value at path, or None if path doesn't exist

        Example:
            obj = {"coverage": {"percentage": 85, "lines": 1234}}
            value = _get_nested_value(obj, "coverage.percentage")
            # Returns: 85
        """
        keys = path.split('.')
        current = obj

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]

        return current

    def _detect_phi(self, state: Dict[str, Any]) -> bool:
        """Detect if state contains PHI (Protected Health Information).

        Heuristics:
        - Check for common PHI field names
        - Check for patterns (SSN, MRN, email, phone)

        Note: This is a conservative heuristic. False positives are acceptable
        (better to over-log than under-log for compliance).

        Args:
            state: Workflow state to check

        Returns:
            True if PHI detected, False otherwise
        """
        # TODO: Implement PHI detection heuristics
        # For Phase 2, return False (Phase 3 will implement proper detection)
        return False

    def _log_audit_trail(
        self,
        sync_id: str,
        execution_id: str,
        event_type: str,
        phi_involved: bool,
        event_details: Dict[str, Any]
    ):
        """Log event to sync_audit_trail (APPEND-ONLY compliance log).

        Healthcare Compliance Requirements:
        - All operations logged with actor attribution
        - PHI access logged with justification
        - APPEND-ONLY (no deletes, no updates)

        Args:
            sync_id: Synchronization rule ID
            execution_id: Execution ID
            event_type: Type of event (e.g., 'sync_triggered')
            phi_involved: Was PHI accessed?
            event_details: Additional event metadata
        """
        audit_id = str(uuid4())

        self.conn.execute("""
            INSERT INTO sync_audit_trail (
                audit_id,
                sync_id,
                execution_id,
                event_type,
                actor,
                actor_role,
                phi_involved,
                compliance_context,
                event_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            audit_id,
            sync_id,
            execution_id,
            event_type,
            'sync_engine',  # Actor
            'autonomous_agent',  # Role
            phi_involved,
            json.dumps({
                "purpose": "Workflow synchronization",
                "legal_basis": "Research protocol"
            }),
            json.dumps(event_details)
        ])
```

### Key Implementation Notes

**DuckDB Adaptations:**
1. **No asyncpg**: Use DuckDB Python API (synchronous)
2. **JSON not JSONB**: Use `json.loads()` and `json.dumps()`
3. **No `@>` operator**: Implement `_pattern_matches()` in Python
4. **Connection pooling**: DuckDB supports concurrent access, but consider connection reuse

**Performance Optimizations:**
1. **Caching**: Cache active synchronization rules (invalidate on schema changes)
2. **Index usage**: Ensure queries use `idx_sync_trigger`, `idx_exec_provenance`
3. **Batching**: If multiple syncs match, could batch INSERT operations

**Healthcare Compliance:**
1. **APPEND-ONLY**: Never DELETE or UPDATE sync_executions or sync_audit_trail
2. **PHI detection**: Conservative heuristics (over-log rather than under-log)
3. **Actor attribution**: All logs include actor and actor_role

## 4. Test Suite: test_sync_engine.py

### File Structure

**File**: `tests/skills/test_sync_engine.py`
**Estimated Lines**: 300-500
**Coverage Target**: ≥85%

### Test Outline

```python
#!/usr/bin/env python3
"""Test suite for MIT Agent Synchronization Engine

Success Criteria (Gate 2):
- Unit test coverage ≥85%
- Pattern matching: 100% test pass rate
- Idempotency: Zero duplicates in 10k iteration test
- Parameter substitution: Nested paths handled correctly
- Error handling: No unhandled exceptions
- Performance: <100ms p95 latency (baseline benchmark)
"""

import pytest
import pytest_asyncio
import json
import duckdb
from pathlib import Path
from uuid import uuid4
import time

from claude.skills.agentdb_state_manager.scripts.sync_engine import SynchronizationEngine


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

    # Insert test data
    _populate_test_data(conn)

    conn.close()
    return str(db_path)


def _populate_test_data(conn):
    """Populate test database with sample synchronization rules."""
    # Sample sync rule: develop.commit_complete → assess.run_tests
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
            pattern,
            status,
            created_by,
            metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        'commit_complete',
        'active',
        'test_setup',
        json.dumps({})
    ])

    # Add more test sync rules...


@pytest.fixture
def sync_engine(test_db):
    """Create SynchronizationEngine instance."""
    return SynchronizationEngine(db_path=test_db)


# ============================================================================
# Pattern Matching Tests
# ============================================================================

class TestPatternMatching:
    """Test pattern matching correctness (100% pass rate required)."""

    @pytest.mark.asyncio
    async def test_exact_match(self, sync_engine):
        """State exactly equals pattern → sync triggers."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with exact state {"lint_status": "pass"}
        # Expected: Sync matches and triggers

        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-001",
            state_snapshot={"lint_status": "pass"}
        )

        assert len(execution_ids) == 1

    @pytest.mark.asyncio
    async def test_partial_match(self, sync_engine):
        """State ⊃ pattern → sync triggers (state contains pattern)."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with superset {"lint_status": "pass", "coverage": 85}
        # Expected: Sync matches (partial match)

        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-002",
            state_snapshot={
                "lint_status": "pass",
                "coverage": {"percentage": 85}
            }
        )

        assert len(execution_ids) == 1

    @pytest.mark.asyncio
    async def test_no_match(self, sync_engine):
        """State ⊄ pattern → sync does not trigger."""
        # Setup: Sync rule requires {"lint_status": "pass"}
        # Action: Trigger with {"lint_status": "fail"}
        # Expected: Sync does NOT match

        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-003",
            state_snapshot={"lint_status": "fail"}
        )

        assert len(execution_ids) == 0

    @pytest.mark.asyncio
    async def test_nested_pattern_match(self, sync_engine):
        """Nested pattern matching works correctly."""
        # Setup: Add sync rule with nested pattern
        conn = duckdb.connect(sync_engine.conn.execute("PRAGMA database_list").fetchone()[2])
        conn.execute("""
            INSERT INTO agent_synchronizations (...)
            VALUES (..., ?, ...)
        """, [json.dumps({"coverage": {"percentage": 85}})])

        # Action: Trigger with matching nested state
        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-004",
            state_snapshot={
                "coverage": {"percentage": 85, "lines_covered": 1234}
            }
        )

        assert len(execution_ids) >= 1


# ============================================================================
# Idempotency Tests
# ============================================================================

class TestIdempotency:
    """Test idempotency enforcement (zero duplicates required)."""

    @pytest.mark.asyncio
    async def test_duplicate_state_single_execution(self, sync_engine):
        """Same state twice → only one execution recorded."""
        state = {"lint_status": "pass"}

        # First execution
        exec_ids_1 = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-dup",
            state_snapshot=state
        )

        # Second execution with SAME state
        exec_ids_2 = await sync_engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="test-flow-dup",
            state_snapshot=state
        )

        assert len(exec_ids_1) == 1
        assert len(exec_ids_2) == 0  # Idempotency: no duplicate

    @pytest.mark.asyncio
    async def test_10k_iterations_idempotency(self, sync_engine):
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
            exec_ids = await sync_engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="test-flow-10k",
                state_snapshot=state
            )
            all_exec_ids.extend(exec_ids)

        # Count unique executions in database
        conn = sync_engine.conn
        result = conn.execute("""
            SELECT COUNT(DISTINCT provenance_hash) FROM sync_executions
            WHERE sync_id = 'sync-001'
        """).fetchone()

        unique_count = result[0]

        # Should be ~1000 unique executions (not 10,000)
        assert unique_count <= 1000
        assert unique_count > 900  # Allow some variation

        # Verify zero duplicate provenance hashes
        dup_check = conn.execute("""
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

    @pytest.mark.asyncio
    async def test_latency_single_agent(self, sync_engine):
        """Measure p50, p95, p99 latency for single agent.

        Goal: <100ms p95 latency
        """
        state = {"lint_status": "pass"}
        latencies = []

        # Measure 100 iterations
        for i in range(100):
            start = time.perf_counter()

            await sync_engine.on_agent_action_complete(
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

    @pytest.mark.asyncio
    async def test_latency_concurrent_agents(self, sync_engine):
        """Measure latency for 13 concurrent agents.

        Goal: <200ms p95 latency for 13 concurrent
        """
        # TODO: Implement concurrent execution test
        # This requires asyncio concurrency or threading
        pass


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error scenarios don't raise unhandled exceptions."""

    @pytest.mark.asyncio
    async def test_invalid_sync_rule_graceful(self, sync_engine):
        """Invalid sync rule → log error, continue (no exception)."""
        # TODO: Test with malformed trigger_pattern JSON
        pass

    @pytest.mark.asyncio
    async def test_database_error_logged(self, sync_engine):
        """Database error → log error, continue (no exception)."""
        # TODO: Test with database connection failure simulation
        pass
```

### Test Data Requirements

**Minimal test database:**
- 5-10 synchronization rules with different patterns
- Mix of exact match, partial match patterns
- Mix of priorities (1, 50, 100, 200)
- At least one disabled rule (enabled=FALSE) for filtering tests

**Performance test data:**
- Sufficient to measure latency distributions
- 100+ iterations for statistical significance

## 5. Success Criteria Checklist

From Issue #160 (Gate 2):

### Required Criteria

- [ ] **Unit test coverage ≥85%**
  - Measure with: `uv run pytest --cov=.claude/skills/agentdb-state-manager/scripts/sync_engine.py --cov-report=term`
  - Target: ≥85% line coverage

- [ ] **Pattern matching: 100% test pass rate**
  - All pattern matching tests must pass
  - Test cases: exact match, partial match, no match, nested patterns
  - Zero test failures allowed

- [ ] **Idempotency: Zero duplicates in 10k iteration test**
  - Run 10,000 iterations with duplicate states
  - Count unique `provenance_hash` values in database
  - Verify: zero duplicate executions (idempotency enforced)

- [ ] **Parameter substitution: Handles nested paths correctly**
  - Simple paths: `${trigger_state.field}` ✓
  - Nested paths: `${trigger_state.nested.field}` ✓
  - Missing paths: `${trigger_state.missing}` → null + warning ✓

- [ ] **Error handling: No unhandled exceptions**
  - All error scenarios logged but don't crash
  - Append-only paradigm maintained (continue on error)

- [ ] **Performance: <100ms p95 latency for single agent**
  - Run baseline benchmark
  - Measure p50, p95, p99 latencies
  - Verify: p95 < 100ms

### Additional Criteria

- [ ] **Schema migration tested and documented**
  - Phase 2 migration SQL script created
  - Migration tested on Phase 1 database
  - Test suite validates new fields

- [ ] **DuckDB compatibility validated**
  - All queries use DuckDB syntax (no PostgreSQL JSONB)
  - JSON functions adapted correctly
  - Connection pooling working

- [ ] **Healthcare compliance logging working**
  - All syncs logged to `sync_audit_trail`
  - PHI detection heuristics implemented
  - Actor/role attribution present

- [ ] **All type hints present**
  - Every method has type hints
  - Return types specified
  - Mypy validation passes

- [ ] **Structured logging implemented**
  - JSON-formatted logs
  - Correlation IDs for tracing
  - Log levels appropriate (INFO, WARNING, ERROR)

## 6. Implementation Sequence

### Phase 2.0: Schema Migration (2-3 hours)

**Tasks**: schema_001 → schema_004

**Order**:
1. Analyze Phase 1 schema vs Phase 2 requirements (schema_001)
2. Create `phase2_migration.sql` script (schema_002)
3. Test migration on copy of Phase 1 DB (schema_003)
4. Update test_schema_migration.py (schema_004)

**Validation**:
```bash
# Test migration
duckdb test.db < .claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql
duckdb test.db < .claude/skills/agentdb-state-manager/schemas/phase2_migration.sql

# Verify fields
duckdb test.db -c "PRAGMA table_info(agent_synchronizations);"

# Run updated tests
uv run pytest tests/skills/test_schema_migration.py -v
```

### Phase 2.1: Core Engine Implementation (6-8 hours)

**Tasks**: impl_001 → impl_006

**Order** (minimizes dependencies):
1. `_compute_provenance_hash()` - No dependencies (impl_001)
2. `_resolve_params()` + `_get_nested_value()` - No dependencies (impl_002)
3. DuckDB JSON query adaptation (impl_003)
4. `_find_matching_syncs()` + `_pattern_matches()` - Needs impl_003 (impl_004)
5. `_execute_sync()` - Needs impl_002 (impl_005)
6. `on_agent_action_complete()` - Needs all above (impl_006)

**Validation after each step**:
```bash
# Run tests for completed methods
uv run pytest tests/skills/test_sync_engine.py::TestProvenanceHash -v
uv run pytest tests/skills/test_sync_engine.py::TestParameterSubstitution -v
# etc.
```

### Phase 2.2: Test Suite (3-4 hours)

**Tasks**: test_001 → test_005

**Order**:
1. Test fixture and database setup (test_001)
2. Pattern matching tests (test_002)
3. Idempotency tests - including 10k iteration test (test_003)
4. Parameter substitution tests (test_004)
5. Performance baseline benchmarks (test_005)

**Coverage measurement**:
```bash
uv run pytest --cov=.claude/skills/agentdb-state-manager/scripts/sync_engine.py \
             --cov-report=term \
             --cov-report=html \
             --cov-fail-under=85
```

### Phase 2.3: Documentation (1 hour)

**Tasks**: doc_001 → doc_002

**Order**:
1. Add inline type hints and docstrings (doc_001)
   - Performance requirements in docstrings
   - Type hints for all methods
   - Examples in docstrings
2. Create integration guide for Phase 3 (doc_002)
   - How Phase 3 will call `on_agent_action_complete()`
   - Mock interface for testing

**Validation**:
```bash
# Type checking
uv run mypy .claude/skills/agentdb-state-manager/scripts/sync_engine.py

# Documentation linting
# (if available)
```

## 7. Integration with Phase 3

### Integration Point

Phase 3 (Integration Layer) will **call** Phase 2's `on_agent_action_complete()` method.

**Example Integration** (from Phase 3's perspective):

```python
# Phase 3: .claude/skills/agentdb-state-manager/scripts/worktree_agent_integration.py

from .sync_engine import SynchronizationEngine

# Initialize engine (singleton pattern recommended)
sync_engine = SynchronizationEngine(db_path="agentdb.duckdb")

async def on_commit_complete(worktree_id: str, commit_sha: str, coverage: dict, lint_status: str):
    """Hook called when agent 'develop' completes a commit.

    This is implemented in Phase 3 (Integration Layer).
    """
    # Call Phase 2 sync engine
    execution_ids = await sync_engine.on_agent_action_complete(
        agent_id="develop",
        action="commit_complete",
        flow_token=worktree_id,
        state_snapshot={
            "commit_sha": commit_sha,
            "coverage": coverage,
            "lint_status": lint_status
        }
    )

    logger.info(f"Commit {commit_sha} triggered {len(execution_ids)} synchronizations")
    return execution_ids
```

### Mocking for Phase 2 Tests

Phase 2 tests **don't need** actual agent triggering (that's Phase 3's job).

**Mock approach**:
```python
# In test_sync_engine.py

# Phase 2 just records executions, doesn't actually trigger
# Verify execution records in database:
def test_execute_sync_records_execution(sync_engine):
    """_execute_sync() inserts record into sync_executions."""

    # ... call on_agent_action_complete() ...

    # Verify execution record exists
    result = conn.execute("""
        SELECT execution_id, provenance_hash, exec_status
        FROM sync_executions
        WHERE sync_id = 'sync-001'
    """).fetchone()

    assert result is not None
    assert result[2] == 'pending'  # Status = pending (not yet triggered)
```

## 8. Parallelization with Phase 3

### Why Parallelizable?

**Minimal File Overlap:**
- Phase 2: Creates `sync_engine.py` (engine logic)
- Phase 3: Creates `worktree_agent_integration.py` (agent hooks)

**Different Scopes:**
- Phase 2: Database queries, pattern matching, idempotency
- Phase 3: Agent instrumentation, PHI detection, feature flags

**Clear Interface:**
- Phase 3 imports Phase 2's `SynchronizationEngine` class
- Can develop with mocked interface initially

### Time Savings

**Sequential:**
- Phase 2: 12-16 hours
- Phase 3: 10-14 hours
- **Total: 22-30 hours**

**Parallel:**
- Both phases run concurrently
- **Total: max(12-16h, 10-14h) = 12-16 hours**
- **Savings: 40-47% reduction**

### Coordination Points

**Week 1:**
- Both phases: Schema migration (shared dependency)
- Phase 2: Start core implementation
- Phase 3: Start agent hook design

**Week 2:**
- Phase 2: Testing and documentation
- Phase 3: PHI detection and feature flags
- Integration: Phase 3 begins calling Phase 2's completed methods

**Week 3:**
- Both phases: Integration testing
- Validate end-to-end flow works correctly

## 9. Open Questions / Decisions Needed

### Q1: Schema Migration Approach

**Question**: Should we extend Phase 1 schema (ALTER TABLE) or create new tables?

**Options**:
- **Option A**: ALTER TABLE to add fields (recommended)
  - Pros: Single unified schema, simpler migration
  - Cons: Phase 1 fields unused by Phase 2

- **Option B**: Create separate tables for MIT sync pattern
  - Pros: Clean separation, no unused fields
  - Cons: Duplicate table structure, complex migration

**Recommendation**: Option A (ALTER TABLE) for simplicity

### Q2: DuckDB Async Support

**Question**: Does Phase 2 need async/await or can it be synchronous?

**Context**:
- Issue #160 written for asyncpg (async PostgreSQL)
- DuckDB Python API is synchronous (no native async)

**Options**:
- **Option A**: Use synchronous DuckDB API (simpler)
  - Change method signatures from `async def` to `def`
  - Remove all `await` keywords

- **Option B**: Wrap DuckDB in async executor
  - Use `asyncio.to_thread()` to run sync code in thread pool
  - Maintain `async def` signatures for future compatibility

**Recommendation**: Option A (synchronous) for Phase 2, Option B if Phase 3 requires async

### Q3: PHI Detection Heuristics

**Question**: How sophisticated should PHI detection be in Phase 2?

**Options**:
- **Option A**: Simple heuristics (field name matching)
  - Check for keys like "patient_id", "mrn", "ssn"
  - Conservative (over-logs)

- **Option B**: Advanced pattern matching
  - Regex for SSN, MRN, email, phone patterns
  - NER (Named Entity Recognition) for PII

- **Option C**: Defer to Phase 3
  - Phase 2 just provides `_detect_phi()` stub
  - Phase 3 implements sophisticated detection

**Recommendation**: Option C (defer to Phase 3) - keeps Phase 2 focused on core engine

## 10. Related Documentation

### Reference Files

**Schema**:
- `.claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql` - Phase 1 schema
- `.claude/skills/agentdb-state-manager/schemas/phase2_migration.sql` - To be created

**Tests**:
- `.claude/skills/agentdb-state-manager/scripts/test_schema_migration.py` - Existing tests
- `tests/skills/test_sync_engine.py` - To be created

**Issue Tracking**:
- Issue #158: MIT Agent Synchronization Pattern (parent)
- Issue #159: Phase 1 - Database Schema (✅ completed)
- Issue #160: Phase 2 - Synchronization Engine (this work)
- Issue #161: Phase 3 - Integration Layer (can parallelize)

### Workflow Documentation

**From CLAUDE.md**:
- Workflow v5.3 architecture
- Quality gates (≥80% coverage required)
- DuckDB development guidelines
- Healthcare compliance requirements

**Version History**:
- v1.10.0: Phase 1 completed (schema + tests)
- v1.10.1: Phase 1 cleanup (issues #167-172 closed)
- v1.10.2: Documentation improvements
- **v1.11.0 (target)**: Phase 2 + Phase 3 completion

---

## Next Steps

1. **Review this TODO**: Ensure all requirements understood
2. **Ask questions**: Clarify any ambiguities before starting
3. **Begin with schema migration**: Tasks schema_001 → schema_004 (critical path)
4. **Implement core engine**: Tasks impl_001 → impl_006
5. **Build test suite**: Tasks test_001 → test_005
6. **Validate success criteria**: Check all Gate 2 requirements met

**Estimated Delivery**: 12-16 hours of focused work

**Parallelization**: Consider starting Phase 3 (#161) after schema migration completes for 40-47% time savings.
