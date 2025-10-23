---
type: workflow-master-manifest
version: 5.0.0
last_update: "2025-10-23T19:45:00Z"

workflows:
  active: []

  archived:
    - slug: workflow
      timestamp: 20251023T123254Z
      title: "Release Workflow Automation"
      status: completed
      completed_at: "2025-10-23T19:30:00Z"
      semantic_version: "1.2.0"
      file: "ARCHIVED/TODO_feature_20251023T123254Z_workflow.md"
      summary: "Implemented 4 release automation scripts (create_release.py, tag_release.py, backmerge_release.py, cleanup_release.py) with tests and documentation"

context_stats:
  total_workflows_completed: 1
  current_token_usage: 75000
  last_checkpoint: "2025-10-23T19:30:00Z"
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

## Usage

- **Active workflows** are in progress
- **Archived workflows** are completed and moved to ARCHIVED/
- Each workflow has a dedicated TODO_feature_<timestamp>_<slug>.md file
- Run `/context` to monitor token usage
- Checkpoint at 100K tokens, then `/init` and `/compact`
