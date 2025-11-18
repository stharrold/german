"""
Test suite for default synchronization rules (Phase 4).

This module validates SQL insertion correctness for default_synchronizations.sql.
It does NOT test runtime behavior (that's Phase 5).

Test Coverage:
- SQL syntax validation (all INSERT statements execute without errors)
- Foreign key constraint satisfaction
- JSONB pattern validation
- JSONPath condition syntax validation
- Priority value ranges
- Rule count verification (4 normal + 4 error recovery = 8 total)

Created: 2025-11-18
Issue: #162 - Phase 4 Default Synchronization Rules Implementation
"""

import json
import shutil
import tempfile
from pathlib import Path

import duckdb
import pytest


@pytest.fixture
def temp_db():
    """Create temporary DuckDB database with Phase 1 and Phase 2 schemas."""
    # Create temporary database (use mktemp to get path without creating file)
    temp_dir = tempfile.mkdtemp()
    temp_db_path = Path(temp_dir) / 'test.duckdb'

    conn = duckdb.connect(str(temp_db_path))

    # Load Phase 1 schema
    schema_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'schemas' / 'agentdb_sync_schema.sql'
    with open(schema_path, 'r') as f:
        conn.execute(f.read())

    # Load Phase 2 migration
    migration_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'schemas' / 'phase2_migration.sql'
    with open(migration_path, 'r') as f:
        conn.execute(f.read())

    yield conn

    conn.close()
    # Cleanup temp directory
    shutil.rmtree(temp_dir)


def test_sql_syntax_validation(temp_db):
    """Test that all INSERT statements execute without SQL errors."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        sql_content = f.read()

    # Execute all SQL statements
    # Should not raise any exceptions
    temp_db.execute(sql_content)

    # Verify rules were inserted
    result = temp_db.execute("SELECT COUNT(*) FROM agent_synchronizations").fetchone()
    assert result[0] >= 8, f"Expected at least 8 rules, got {result[0]}"


def test_rule_count(temp_db):
    """Test that correct number of rules are inserted (4 normal + 4 error recovery)."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Count total rules
    total = temp_db.execute("SELECT COUNT(*) FROM agent_synchronizations").fetchone()[0]
    assert total == 8, f"Expected 8 rules, got {total}"

    # Count normal flow rules (priority 100-199)
    normal_flow = temp_db.execute(
        "SELECT COUNT(*) FROM agent_synchronizations WHERE priority BETWEEN 100 AND 199"
    ).fetchone()[0]
    assert normal_flow == 4, f"Expected 4 normal flow rules, got {normal_flow}"

    # Count error recovery rules (priority 200-299)
    error_recovery = temp_db.execute(
        "SELECT COUNT(*) FROM agent_synchronizations WHERE priority BETWEEN 200 AND 299"
    ).fetchone()[0]
    assert error_recovery == 4, f"Expected 4 error recovery rules, got {error_recovery}"


def test_json_pattern_validity(temp_db):
    """Test that all trigger_pattern fields contain valid JSON."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Fetch all trigger patterns
    patterns = temp_db.execute(
        "SELECT pattern, trigger_pattern FROM agent_synchronizations WHERE trigger_pattern IS NOT NULL"
    ).fetchall()

    for pattern_name, trigger_pattern in patterns:
        # DuckDB JSON type is already validated by database
        # Additional validation: ensure it's not empty and has expected structure
        assert trigger_pattern is not None, f"Pattern {pattern_name} has NULL trigger_pattern"

        # Validate JSON structure (should be dict/object)
        if isinstance(trigger_pattern, str):
            parsed = json.loads(trigger_pattern)
        else:
            parsed = trigger_pattern

        assert isinstance(parsed, dict), f"Pattern {pattern_name} trigger_pattern is not a dict: {type(parsed)}"
        assert len(parsed) > 0, f"Pattern {pattern_name} trigger_pattern is empty"


def test_jsonpath_condition_syntax(temp_db):
    """Test that all condition_jsonpath fields have valid JSONPath syntax."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Check if condition_jsonpath column exists (Phase 4+)
    columns = temp_db.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'agent_synchronizations'"
    ).fetchall()
    column_names = [col[0] for col in columns]

    if 'condition_jsonpath' not in column_names:
        # Column doesn't exist yet (Phase 2 schema), skip test
        pytest.skip("condition_jsonpath column not in schema (future enhancement)")

    # Fetch all JSONPath conditions
    conditions = temp_db.execute(
        "SELECT pattern, condition_jsonpath FROM agent_synchronizations WHERE condition_jsonpath IS NOT NULL"
    ).fetchall()

    for pattern_name, condition_jsonpath in conditions:
        # JSONPath syntax validation
        assert condition_jsonpath.startswith('$.'), \
            f"Pattern {pattern_name} JSONPath doesn't start with '$.' : {condition_jsonpath}"

        # Ensure no spaces (valid JSONPath has no spaces in path)
        path_parts = condition_jsonpath.split('.')
        for part in path_parts:
            if part == '$':
                continue
            # Allow array notation like [0]
            assert ' ' not in part or '[' in part, \
                f"Pattern {pattern_name} JSONPath has invalid spaces: {condition_jsonpath}"


def test_priority_ranges(temp_db):
    """Test that all priority values are in expected ranges."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Fetch all priorities
    priorities = temp_db.execute(
        "SELECT pattern, priority FROM agent_synchronizations"
    ).fetchall()

    for pattern_name, priority in priorities:
        # Priority should be in valid ranges
        assert priority >= 1, f"Pattern {pattern_name} priority too low: {priority}"
        assert priority <= 299, f"Pattern {pattern_name} priority too high: {priority}"

        # Priority range must match sync_type
        # Query sync_type from database for this pattern
        sync_type_result = temp_db.execute(
            "SELECT sync_type FROM agent_synchronizations WHERE pattern = ?",
            [pattern_name]
        ).fetchone()

        if sync_type_result:
            sync_type = sync_type_result[0]

            if 200 <= priority <= 299:
                # Error recovery priority range
                assert sync_type == 'error_recovery', \
                    f"Pattern {pattern_name} has error priority {priority} but sync_type is '{sync_type}' (expected 'error_recovery')"
            elif 100 <= priority <= 199:
                # Normal flow priority range
                assert sync_type == 'workflow_transition', \
                    f"Pattern {pattern_name} has normal priority {priority} but sync_type is '{sync_type}' (expected 'workflow_transition')"


def test_required_fields_not_null(temp_db):
    """Test that all required Phase 2 fields are populated."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Check required fields
    rules = temp_db.execute("""
        SELECT
            pattern,
            trigger_agent_id,
            trigger_action,
            trigger_pattern,
            target_agent_id,
            target_action,
            priority,
            enabled
        FROM agent_synchronizations
    """).fetchall()

    for rule in rules:
        pattern_name, trigger_agent, trigger_action, trigger_pattern, target_agent, target_action, priority, enabled = rule

        assert trigger_agent is not None, f"Pattern {pattern_name} missing trigger_agent_id"
        assert trigger_action is not None, f"Pattern {pattern_name} missing trigger_action"
        assert trigger_pattern is not None, f"Pattern {pattern_name} missing trigger_pattern"
        assert target_agent is not None, f"Pattern {pattern_name} missing target_agent_id"
        assert target_action is not None, f"Pattern {pattern_name} missing target_action"
        assert priority is not None, f"Pattern {pattern_name} missing priority"
        assert enabled is not None, f"Pattern {pattern_name} missing enabled"


def test_all_rules_enabled(temp_db):
    """Test that all default rules are enabled by default."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Count enabled rules
    enabled_count = temp_db.execute(
        "SELECT COUNT(*) FROM agent_synchronizations WHERE enabled = true"
    ).fetchone()[0]

    total_count = temp_db.execute(
        "SELECT COUNT(*) FROM agent_synchronizations"
    ).fetchone()[0]

    assert enabled_count == total_count, \
        f"All rules should be enabled by default. Enabled: {enabled_count}, Total: {total_count}"


def test_target_action_json_validity(temp_db):
    """Test that all target_action fields contain valid JSON."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Fetch all target actions
    actions = temp_db.execute(
        "SELECT pattern, target_action FROM agent_synchronizations WHERE target_action IS NOT NULL"
    ).fetchall()

    for pattern_name, target_action in actions:
        # Parse as JSON
        if isinstance(target_action, str):
            parsed = json.loads(target_action)
        else:
            # DuckDB already parsed it
            parsed = target_action

        # Should be a dict with 'action' field
        assert isinstance(parsed, dict), \
            f"Pattern {pattern_name} target_action is not a dict: {type(parsed)}"
        assert 'action' in parsed, \
            f"Pattern {pattern_name} target_action missing 'action' field"
        assert 'params' in parsed, \
            f"Pattern {pattern_name} target_action missing 'params' field"


def test_4_tier_workflow_coverage(temp_db):
    """Test that all 4 workflow tiers are represented in normal flow rules."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Expected workflow transitions (normal flow only)
    expected_transitions = [
        ('orchestrate', 'develop'),   # Orchestrate → Develop
        ('develop', 'assess'),         # Develop → Assess
        ('assess', 'research'),        # Assess → Research
        ('research', 'orchestrate'),   # Research → Orchestrate (PR)
    ]

    # Fetch normal flow rules
    normal_flow_rules = temp_db.execute("""
        SELECT trigger_agent_id, target_agent_id
        FROM agent_synchronizations
        WHERE priority BETWEEN 100 AND 199
        ORDER BY priority
    """).fetchall()

    # Convert to list of tuples
    actual_transitions = [(trigger, target) for trigger, target in normal_flow_rules]

    # Check all expected transitions exist
    for expected in expected_transitions:
        assert expected in actual_transitions, \
            f"Missing transition: {expected[0]} → {expected[1]}"


def test_error_recovery_targets_develop(temp_db):
    """Test that most error recovery rules target develop or research agents."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Fetch error recovery rules
    error_rules = temp_db.execute("""
        SELECT pattern, target_agent_id
        FROM agent_synchronizations
        WHERE priority BETWEEN 200 AND 299
    """).fetchall()

    # Count targets
    develop_target_count = sum(1 for _, target in error_rules if target == 'develop')

    # Most error recovery should go back to develop (to fix issues)
    assert develop_target_count >= 2, \
        f"Expected at least 2 error recovery rules targeting develop, got {develop_target_count}"


def test_validation_query_executes(temp_db):
    """Test that the built-in validation query executes successfully."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        sql_content = f.read()
        temp_db.execute(sql_content)

    # The validation query is the first SELECT after all INSERT statements
    # Extract and execute it
    validation_query = """
    SELECT
        'Default synchronization rules validation' AS status,
        COUNT(*) AS total_rules,
        SUM(CASE WHEN priority BETWEEN 100 AND 199 THEN 1 ELSE 0 END) AS normal_flow_rules,
        SUM(CASE WHEN priority BETWEEN 200 AND 299 THEN 1 ELSE 0 END) AS error_recovery_rules,
        SUM(CASE WHEN enabled = true THEN 1 ELSE 0 END) AS enabled_rules,
        MIN(priority) AS min_priority,
        MAX(priority) AS max_priority
    FROM agent_synchronizations
    WHERE pattern IN (
        'orchestrate_to_develop',
        'develop_to_assess',
        'assess_to_research',
        'research_to_orchestrate',
        'test_failure_recovery',
        'lint_failure_recovery',
        'coverage_gap_recovery',
        'documentation_incomplete_recovery'
    )
    """

    result = temp_db.execute(validation_query).fetchone()

    # Validation query should return 1 row with expected values
    assert result is not None, "Validation query returned no results"
    status, total, normal, error, enabled, min_pri, max_pri = result

    assert total == 8, f"Expected 8 rules, got {total}"
    assert normal == 4, f"Expected 4 normal flow rules, got {normal}"
    assert error == 4, f"Expected 4 error recovery rules, got {error}"
    assert enabled == 8, f"Expected 8 enabled rules, got {enabled}"
    assert min_pri == 100, f"Expected min priority 100, got {min_pri}"
    assert max_pri == 200, f"Expected max priority 200, got {max_pri}"


def test_no_duplicate_patterns(temp_db):
    """Test that pattern names are unique."""
    default_syncs_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'templates' / 'default_synchronizations.sql'

    with open(default_syncs_path, 'r') as f:
        temp_db.execute(f.read())

    # Check for duplicate patterns
    duplicates = temp_db.execute("""
        SELECT pattern, COUNT(*) as count
        FROM agent_synchronizations
        GROUP BY pattern
        HAVING COUNT(*) > 1
    """).fetchall()

    assert len(duplicates) == 0, f"Found duplicate patterns: {duplicates}"


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])
