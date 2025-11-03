---
type: workflow-master-manifest
version: 5.0.0
last_update: '2025-11-03T18:26:14.736743+00:00'
workflows:
  active:
  - slug: azure-devops-cli
    timestamp: '2025-11-03T17:07:21Z'
    title: Azure DevOps CLI Support
    status: in_progress
    file: TODO_feature_20251103T170721Z_azure-devops-cli.md
  archived:
  - slug: workflow
    timestamp: 20251023T123254Z
    title: Release Workflow Automation
    status: completed
    completed_at: '2025-10-23T19:30:00Z'
    semantic_version: 1.2.0
    file: ARCHIVED/TODO_feature_20251023T123254Z_workflow.md
    summary: Implemented 4 release automation scripts (create_release.py, tag_release.py,
      backmerge_release.py, cleanup_release.py) with tests and documentation
context_stats:
  total_workflows_completed: 1
  current_token_usage: 55000
  last_checkpoint: '2025-11-03T17:07:21Z'
  recent_improvements: Added agentdb-state-manager skill (v1.0.0), TODO lifecycle
    management in workflow-utilities (v5.1.0), existing repository documentation for
    initialize-repository (v1.0.1)
---

# Master TODO Manifest

This is the master manifest tracking all workflow TODO files in this repository.

## Active Workflows

None currently active.

## Archived Workflows

### Release Workflow Automation (v1.2.0)
- **Completed:** 2025-10-23T19:30:00Z
- **File:** ARCHIVED/TODO_feature_20251023T123254Z_workflow.md
- **Summary:** Implemented Phase 5 release automation scripts with full test coverage
- **Quality:** 85% coverage, all tests passing, linting clean

## Recent Session (2025-11-03)

Direct improvements made outside formal workflow (not tracked as active workflows):
- **agentdb-state-manager** (v1.0.0) - 9th skill for persistent state tracking and analytics
- **workflow-utilities** (v5.1.0) - TODO lifecycle management (workflow_registrar.py, workflow_archiver.py, sync_manifest.py)
- **initialize-repository** (v1.0.1) - Comprehensive documentation for applying workflow to existing repositories

Commits: 47d8f9f, cf719fe, b7d8328, 6f9e0a5, 5fa5586, db81681

## Usage

- **Active workflows** are in progress (tracked with TODO_feature_*.md files)
- **Archived workflows** are completed and moved to ARCHIVED/
- **Direct improvements** (skills, documentation) don't use formal workflow
- Each formal workflow has a dedicated TODO_feature_<timestamp>_<slug>.md file
- Run `/context` to monitor token usage
- Checkpoint at 100K tokens, then `/init` and `/compact`
