# Changelog - workflow-utilities

All notable changes to the Workflow Utilities skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- `sync_skill_docs.py` - Documentation sync automation

## [5.1.0] - 2025-11-03

### Added
- **Workflow lifecycle management scripts:**
  - `workflow_registrar.py` - Register workflows in TODO.md active list
  - `workflow_archiver.py` - Archive workflows and update TODO.md manifest
  - `sync_manifest.py` - Rebuild TODO.md from filesystem state
- TODO.md master manifest management capabilities
- Phase 4.3 workflow archival automation

### Changed
- Extended scope from "file utilities" to "workflow lifecycle utilities"
- Updated SKILL.md with workflow management documentation
- Added workflow lifecycle usage examples

### Fixed
- Gap: Phase 4.3 archival had no implementation (now workflow_archiver.py)
- Gap: TODO.md workflows.active[] never updated (now workflow_registrar.py)
- Gap: No recovery mechanism for TODO.md (now sync_manifest.py)

## [5.0.0] - 2025-10-23

### Added
- `deprecate_files.py` - File deprecation with timestamped archives
- `archive_manager.py` - Archive management (list, extract)
- `todo_updater.py` - TODO file manifest management
- `directory_structure.py` - Compliant directory creation

### Changed
- All utilities follow consistent error handling patterns
- Shared constants and validation logic

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
