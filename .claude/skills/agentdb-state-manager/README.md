---
type: directory-documentation
directory: .claude/skills/agentdb-state-manager
title: AgentDB State Manager Skill
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# AgentDB State Manager Skill

Persistent state management using AgentDB (DuckDB) for workflow analytics and checkpoints.

## Purpose

**Primary purpose:** Data gathering and analysis for workflow state tracking

**Workflow phase:** Cross-phase (Utilities) - All phases (1-6)

Provides read-only analytics cache synchronized from TODO_*.md files, enabling:
- Complex dependency graph queries
- Historical workflow metrics
- Context checkpoint storage/recovery
- State transition analysis

## Quick Start

### 1. Initialize AgentDB

```bash
python .claude/skills/agentdb-state-manager/scripts/init_database.py
```

### 2. Sync TODO Files

```bash
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py --all
```

### 3. Query State

```bash
# Current state
python .claude/skills/agentdb-state-manager/scripts/query_state.py

# Task dependencies
python .claude/skills/agentdb-state-manager/scripts/query_state.py --dependencies
```

### 4. Analyze Metrics

```bash
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py --trends
```

### 5. Manage Checkpoints

```bash
# Store checkpoint
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py store --todo TODO_*.md

# List checkpoints
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py list
```

## Key Features

- **Read-only analytics:** TODO_*.md files remain source of truth
- **Immutable records:** Append-only history preserves full state transitions
- **Token efficiency:** 89% reduction for complex queries vs file parsing
- **Session-scoped:** 24-hour AgentDB lifetime, re-initialize as needed

## MIT Agent Synchronization Pattern (Phase 3 - Integration Layer)

**Status:** ✅ Implemented (Issue #161)

Phase 3 provides non-invasive integration hooks for the MIT Agent Synchronization Pattern:

### Components

1. **FlowTokenManager**: Maps workflow sessions to sync engine flow tokens
2. **PHIDetector**: Detects Protected Health Information in state snapshots
3. **ComplianceWrapper**: Wraps sync engine calls with healthcare compliance logging
4. **SyncEngineFactory**: Creates sync engine instances with feature flag control
5. **trigger_sync_completion()**: Main entry point for agent hooks

### Usage

**Enable sync engine:**
```bash
export SYNC_ENGINE_ENABLED=true
export AGENTDB_PATH=agentdb.duckdb
```

**Integration points** (minimal changes, ~8 lines each):
- `bmad-planner/create_planning.py` - After BMAD planning (orchestrate agent)
- `git-workflow-manager/create_worktree.py` - After worktree creation (develop agent)
- `quality-enforcer/run_quality_gates.py` - After tests (assess agent)
- `speckit-author/create_specifications.py` - After documentation (research agent)

**Example hook:**
```python
import asyncio
from worktree_agent_integration import trigger_sync_completion

# After agent action completes
asyncio.run(trigger_sync_completion(
    agent_id="develop",
    action="commit_complete",
    state_snapshot={"commit_sha": "abc123", "coverage": 85},
    context={"user": "stharrold"}
))
```

**Features:**
- ✅ Feature-flagged (disabled by default)
- ✅ Graceful degradation on errors
- ✅ PHI detection with compliance logging
- ✅ Singleton pattern for connection reuse
- ✅ Async operations (non-blocking)

**Test suite:** 33 unit tests, 100% pass rate

### Related Issues

- **Issue #158**: MIT Agent Synchronization Pattern (parent)
- **Issue #159**: Phase 1 - Database Schema (completed in v1.10.0)
- **Issue #160**: Phase 2 - Synchronization Engine (completed in v1.11.0)
- **Issue #161**: Phase 3 - Integration Layer (completed in v1.12.0)
- **Issue #162**: Phase 4 - Default Rules (pending)

## Documentation

- **[SKILL.md](SKILL.md)** - Complete documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code context
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[templates/workflow-states.json](templates/workflow-states.json)** - State definitions
- **[docs/phase2_integration_guide.md](docs/phase2_integration_guide.md)** - Phase 2 → Phase 3 integration guide

## Version

v1.1.0 - Phase 3 integration layer (2025-11-17)

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code
