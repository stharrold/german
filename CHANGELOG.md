# Changelog

All notable changes to the German Language Learning Repository workflow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- None currently planned

## [1.5.0] - 2025-11-02

### Added
- **initialize-repository meta-skill** (Phase 0) for bootstrapping new repositories
  - Interactive Q&A system (4 phases, 13-14 questions)
  - Copies all 8 workflow skills from source to target repository
  - Adapts documentation for new repository context
  - Generates README.md, CLAUDE.md, pyproject.toml
  - Optional git initialization with 3-branch structure
  - Token savings: ~3,350 tokens per repository (96% reduction)
- Version consistency validator (`validate_versions.py`)
- Comprehensive update checklist for skill modifications (`UPDATE_CHECKLIST.md`)
- CONTRIBUTING.md with contributor guidelines
- CHANGELOG system for all skills (8 skill CHANGELOGs)
- Documentation sync tool (`sync_skill_docs.py`)

### Changed
- Workflow system now has 8 skills (added initialize-repository meta-skill)
- WORKFLOW.md updated with Phase 0 (Repository Initialization)
- CLAUDE.md updated with 8th skill reference

### Token Efficiency
- Repository initialization: ~3,350 tokens saved (96% reduction)
- Previous workflow + docs system: ~3,500 tokens
- New system: ~150 tokens (single script call)

## [5.2.0] - 2025-10-23

### Changed
- TODO.md manifest structure to v5.2.0 format
- Enhanced workflow phase descriptions

## [5.0.0] - 2025-10-23

### Added
- Skill-based architecture with 7 specialized skills
- Interactive callable tools for BMAD and SpecKit
- Progressive skill loading for token efficiency
- Quality gates enforcement (≥80% coverage)
- Automated semantic versioning calculation
- File deprecation system with timestamped archives
- Release automation scripts (create, tag, backmerge, cleanup)
- Hotfix workflow support

### Changed
- Migrated from monolithic workflow to modular skill system
- BMAD and SpecKit now use interactive Q&A tools
- Workflow phases restructured (0-6 phases)
- TODO file format with YAML frontmatter
- Context management with 100K token checkpoint

### Token Efficiency
- BMAD: ~2,300 tokens saved per feature (92% reduction)
- SpecKit: ~1,700-2,700 tokens saved per feature
- Total workflow: ~600-900 tokens per phase vs 2,718 for monolith

## Earlier Versions

Earlier versions (< 5.0.0) used a different workflow architecture. See `ARCHIVED/` for historical workflow documentation.

---

## Version History Summary

| Version | Date       | Type  | Description |
|---------|------------|-------|-------------|
| 1.5.0   | 2025-11-02 | MINOR | Initialize-repository meta-skill + documentation system |
| 5.2.0   | 2025-10-23 | MINOR | Enhanced TODO.md manifest structure |
| 5.0.0   | 2025-10-23 | MAJOR | Skill-based architecture with callable tools |

---

## How to Update This CHANGELOG

When making changes to the workflow:

1. **Add entry to [Unreleased] section** during development
2. **Use categories:**
   - `Added` - New features
   - `Changed` - Changes in existing functionality
   - `Deprecated` - Soon-to-be removed features
   - `Removed` - Removed features
   - `Fixed` - Bug fixes
   - `Security` - Security fixes
   - `Token Efficiency` - Token usage improvements

3. **On release:**
   - Move [Unreleased] items to new version section
   - Add date: `## [X.Y.Z] - YYYY-MM-DD`
   - Update Version History Summary table

4. **Link to skill CHANGELOGs:**
   - For skill-specific changes, reference `.claude/skills/<skill-name>/CHANGELOG.md`

---

## Related Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Complete workflow guide
- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[.claude/skills/UPDATE_CHECKLIST.md](.claude/skills/UPDATE_CHECKLIST.md)** - Update process checklist

**Skill-Specific CHANGELOGs:**
- [bmad-planner](.claude/skills/bmad-planner/CHANGELOG.md)
- [speckit-author](.claude/skills/speckit-author/CHANGELOG.md)
- [workflow-orchestrator](.claude/skills/workflow-orchestrator/CHANGELOG.md)
- [git-workflow-manager](.claude/skills/git-workflow-manager/CHANGELOG.md)
- [quality-enforcer](.claude/skills/quality-enforcer/CHANGELOG.md)
- [tech-stack-adapter](.claude/skills/tech-stack-adapter/CHANGELOG.md)
- [workflow-utilities](.claude/skills/workflow-utilities/CHANGELOG.md)
