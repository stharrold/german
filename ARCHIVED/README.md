# Archived Files

## Overview

Archive of deprecated files and completed workflows that are no longer in active use.

## Contents

This directory contains:

### Completed Workflows
- Archived TODO workflow tracking files (TODO_feature_*.md)
- Historical workflow state and progress

### Archived Documentation
- Previous versions of workflow documentation
- Deprecated workflow system specifications
- Historical reference materials

## Structure

Files are organized by:
- **Workflow files**: `TODO_feature_<timestamp>_<slug>.md`
- **ZIP archives**: `<timestamp>_<description>.zip` (for deprecated code)
- **Documentation**: Historical markdown files

## Usage

### Listing Archives
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py list
```

### Extracting Archives
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py extract ARCHIVED/<file>.zip output/
```

### Archiving Workflows
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py archive TODO_feature_*.md
```

## Retention Policy

- Archived files are retained indefinitely for historical reference
- Files may be permanently deleted only after explicit approval
- Always use archive_manager.py to verify contents before deletion
