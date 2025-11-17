---
type: claude-context
directory: benchmarks/ARCHIVED
purpose: Archive of deprecated files from benchmarks
parent: ../CLAUDE.md
sibling_readme: README.md
children: []
related_skills:
  - workflow-utilities
---

# Claude Code Context: Archived Content

## Purpose

Archive of deprecated files from benchmarks directory. Maintains historical context for benchmark results and test data that has been superseded or removed.

## Directory Structure

Archived files are stored as timestamped zip files created by the workflow-utilities deprecation script. Each archive is self-contained with metadata about the deprecation.

## Files in This Directory

Currently empty. Files will appear here when benchmarks are deprecated following the repository's archive-not-delete policy.

Expected file pattern: `YYYYMMDD_HHMMSS_description.zip`

## Usage

When working with archived benchmarks:
1. Use `archive_manager.py list benchmarks/ARCHIVED` to view available archives
2. Use `archive_manager.py extract benchmarks/ARCHIVED/<archive>.zip <output_dir>` to restore archived files for reference
3. Never modify archived files directly - they are read-only historical records
4. To deprecate new files, use `deprecate_files.py` from workflow-utilities

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: Benchmarks

## Related Skills

- workflow-utilities
