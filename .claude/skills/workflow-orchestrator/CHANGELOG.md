# Changelog - workflow-orchestrator

All notable changes to the Workflow Orchestrator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Auto-detection of current workflow phase
- Resumable workflows after context checkpoints

## [5.0.0] - 2025-10-23

### Added
- Progressive skill loading architecture
- Phase-based skill coordination
- Context-aware skill selection (main repo vs worktree)
- User confirmation prompts before actions
- TODO file state management at 100K token checkpoint
- Templates for TODO, WORKFLOW.md, CLAUDE.md

### Changed
- Migrated from monolithic workflow to modular orchestration
- Skills loaded on-demand per phase (not all at once)

### Token Efficiency
- **Previous (monolith):** ~2,718 tokens all at once
- **New (orchestrator):** ~300 tokens initial, ~600-900 per phase
- **Savings:** Progressive loading reduces active context significantly

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
