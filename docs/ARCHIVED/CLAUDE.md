---
type: claude-context
directory: docs/ARCHIVED
purpose: Archive of deprecated files from docs
parent: ../CLAUDE.md
sibling_readme: README.md
children: []
related_skills:
  - workflow-utilities
---

# Claude Code Context: Archived Content

## Purpose

Archive of deprecated files from docs directory. Maintains historical context for documentation that has been superseded or removed.

## Directory Structure

Archived files are stored as timestamped zip files created by the workflow-utilities deprecation script. Each archive is self-contained with metadata about the deprecation.

## Files in This Directory

Currently empty. Files will appear here when documentation is deprecated following the repository's archive-not-delete policy.

Expected file pattern: `YYYYMMDD_HHMMSS_description.zip`

## Usage

When working with archived documentation:
1. Use `archive_manager.py list docs/ARCHIVED` to view available archives
2. Use `archive_manager.py extract docs/ARCHIVED/<archive>.zip <output_dir>` to restore archived files for reference
3. Never modify archived files directly - they are read-only historical records
4. To deprecate new files, use `deprecate_files.py` from workflow-utilities

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: Docs

## Related Skills

- workflow-utilities
