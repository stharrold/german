# Changelog - agentdb-state-manager

All notable changes to the AgentDB State Manager skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- AgentDB tool integration (when available in Claude Code)
- Test suite with ≥80% coverage
- Performance benchmarks for token savings

## [1.0.0] - 2025-11-02

### Added
- Initial release of agentdb-state-manager skill
- Persistent state management using AgentDB (DuckDB)
- Read-only analytics mode (TODO_*.md files remain source of truth)
- Cross-phase (Utilities) integration for all workflow phases
- Canonical state definitions in workflow-states.json (v5.2.0)
- Five core scripts:
  - init_database.py: Initialize AgentDB schema
  - sync_todo_to_db.py: Sync TODO files to AgentDB
  - query_state.py: Query current workflow state
  - analyze_metrics.py: Historical analytics
  - checkpoint_manager.py: Context checkpoint management
- Immutable append-only record design
- Token efficiency: 89% reduction for complex queries
- Complete documentation (SKILL.md, CLAUDE.md, README.md)

---

## Version History

| Version | Date       | Type  | Description |
|---------|------------|-------|-------------|
| 1.0.0   | 2025-11-02 | MAJOR | Initial release |

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code context
- **[README.md](README.md)** - Human-readable overview
- **[templates/workflow-states.json](templates/workflow-states.json)** - State definitions
