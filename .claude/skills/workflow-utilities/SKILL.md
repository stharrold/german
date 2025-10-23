---
name: workflow-utilities
version: 5.0.0
description: |
  Shared utilities for file deprecation, directory structure creation,
  TODO file updates, and archive management. Used by all other skills.

  Use when: Need shared utilities, deprecating files, updating TODO

  Triggers: deprecate, archive, update TODO, create directory
---

# Workflow Utilities

## Purpose

Provides reusable Python utilities for common workflow tasks that are used
across multiple skills.

## Scripts

### deprecate_files.py

Archive deprecated files with timestamp into ARCHIVED/ directory.

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo_file> <description> <file1> [file2 ...]
```

**Arguments:**
- `todo_file`: Path to TODO file (for timestamp extraction)
- `description`: Short description (e.g., 'old-auth-flow')
- `files`: One or more file paths to deprecate

**Creates:**
- `ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip`

### directory_structure.py

Create standard directory structure with required files.

```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Arguments:**
- `directory`: Path to directory to create/populate

**Creates:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (with its own CLAUDE.md and README.md)

### todo_updater.py

Update task status and workflow progress in TODO file.

```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  <todo_file> <task_id> <status> [context_usage]
```

**Arguments:**
- `todo_file`: Path to TODO file
- `task_id`: Task ID (e.g., 'impl_003')
- `status`: New status ('pending' | 'complete' | 'blocked')
- `context_usage` (optional): Context usage percentage

**Updates:**
- Task status in YAML frontmatter
- `completed_at` timestamp
- `workflow_progress.last_task`
- `workflow_progress.last_update`

### archive_manager.py

List and extract archived files.

```bash
# List archives
python .claude/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive
python .claude/skills/workflow-utilities/scripts/archive_manager.py extract <archive> [output_dir]
```

## Usage Examples

### Deprecating Old Files

```python
import subprocess

# Deprecate old implementation files
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/deprecate_files.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'old-validator',
    'src/old_validator.py',
    'tests/test_old_validator.py'
], check=True)
```

### Creating Standard Directories

```python
import subprocess

# Create planning directory with standard structure
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/json-validator'
], check=True)
```

### Updating TODO Tasks

```python
import subprocess

# Mark task as complete
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/todo_updater.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'impl_003',
    'complete',
    '35'  # context usage percentage
], check=True)
```

## Directory Standards

All directories created by these utilities follow the standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

## Integration with Other Skills

All skills can use these helper functions:

```python
# Example from bmad-planner
from pathlib import Path
import subprocess

def create_planning_with_structure(feature_name):
    """Create planning directory with standard structure."""

    planning_dir = Path('planning') / feature_name

    # Create directory structure
    subprocess.run([
        'python',
        '.claude/skills/workflow-utilities/scripts/directory_structure.py',
        str(planning_dir)
    ], check=True)

    # Now create planning documents
    # ...
```

## Best Practices

- Always use these utilities for consistency
- Don't manually create directory structures
- Use deprecation for old files, not deletion
- Update TODO file after each meaningful step
- Check archives before deleting files permanently
