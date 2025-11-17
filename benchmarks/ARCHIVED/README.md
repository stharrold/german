---
type: directory-documentation
directory: benchmarks/ARCHIVED
title: Archived Files
sibling_claude: CLAUDE.md
parent: ../README.md
children: []
---

# Archived Files

## Overview

Archive of deprecated files from the benchmarks directory that are no longer in active use. This directory follows the repository's file deprecation policy where files are archived rather than deleted to maintain historical context.

## Contents

Currently empty. When benchmark files are deprecated, they will be archived here using the `deprecate_files.py` script which creates timestamped zip archives.

## Structure

Archived files are stored as timestamped zip files with the pattern:
- `YYYYMMDD_HHMMSS_description.zip` - Contains deprecated files with metadata

Each archive includes a manifest describing the archived content and reason for deprecation.

## Usage

To extract archived files:
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract benchmarks/ARCHIVED/<archive>.zip restored/
```

To list all archives:
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py list benchmarks/ARCHIVED
```

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code
- **[../README.md](../README.md)** - Parent directory documentation
