# Changelog

All notable changes to the German Language Learning Repository workflow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- None currently planned

## [1.6.0] - 2025-11-04

### Added
- **Comprehensive branch protection documentation** - Explicit rules for `main` and `develop` protected branches
  - Added "Branch Protection Policy" section to WORKFLOW.md (~95 lines)
  - Added "Protected Branches" section to CLAUDE.md with rules and exceptions
  - Added "Protected Branches" section to CONTRIBUTING.md with enforcement details
  - Added protected branches warning to README.md
  - Added protected branch policy to git-workflow-manager/SKILL.md
  - Added "Post-Application Steps" section to initialize-repository/SKILL.md
- **GitHub branch protection setup guide** - Step-by-step configuration instructions
  - Created .github/BRANCH_PROTECTION.md with detailed setup instructions (~350 lines)
  - Created .github/README.md explaining directory purpose
  - Includes GitHub Actions CI/CD integration examples
  - Includes Azure DevOps branch policies alternative
  - Includes troubleshooting section
- **Pre-push hook template** - Local safety net to prevent accidental protected branch pushes
  - Created .git-hooks/pre-push hook template (prevents pushes to main/develop)
  - Created .git-hooks/README.md with installation and usage instructions
  - Hook provides helpful error messages and correct workflow guidance
- **Branch protection compliance tests** - Automated validation of protection policy
  - Added tests/test_branch_protection.py with 6 test cases
  - Verifies no scripts commit to main (except tagging)
  - Verifies only backmerge_release.py commits to develop
  - Verifies backmerge_release.py has exception warning comment
  - Verifies pre-push hook exists and is executable
  - Verifies branch protection documentation exists in all files
  - All tests passing (112 passed, 15 skipped, 88% coverage)

### Changed
- **Documented exception** - Clarified backmerge_release.py as allowed develop commit
  - Added prominent warning comment to backmerge_release.py (~18 lines)
  - Explains why exception is safe (merge-only, no code changes, preserves history)
  - References WORKFLOW.md Branch Protection Policy section

### Documentation
- Branch protection now explicitly documented in 6 core files
- Recovery procedures documented for accidental violations
- GitHub setup guide with screenshots and troubleshooting
- Pre-push hook installation instructions
- Exception policy clearly documented

### Quality
- 6 new tests for branch protection compliance
- All 118 tests passing (112 passed, 15 skipped)
- Test coverage: 88.1% (above required 80%)
- Version validation: All checks passed
- Linting: Clean (1 import sorting issue auto-fixed)

## [1.5.1] - 2025-11-04

### Fixed
- **Critical bugs** - Resolved 27 GitHub issues identified in Copilot code reviews
  - Fixed pyproject.toml configuration errors
  - Fixed SpecKit template rendering issues
  - Fixed German translation inaccuracies
  - Auto-fixed 23 code quality issues with ruff (unused imports, variables, formatting)
  - Quality: 106 tests passing, 88% coverage

### Added
- **Comprehensive skill documentation** - Completed documentation for all workflow skills
  - Added 5 missing `scripts/__init__.py` files (proper Python package structure)
  - Completed 6 CLAUDE.md files (352-1,019 lines each) for Claude Code integration
  - Completed 5 README.md files (232-435 lines each) for human developers
  - All skills now have comprehensive documentation for both Claude Code and humans

### Changed
- **Workflow documentation** - Enhanced Phase 4.5 instructions
  - Added worktree/branch cleanup instructions
  - Clarified git worktree removal process
  - Added git branch deletion commands (local and remote)

### Documentation
- Skills with complete documentation: 9/9 (100%)
- CLAUDE.md coverage: All skills (bmad-planner, speckit-author, quality-enforcer, git-workflow-manager, tech-stack-adapter, workflow-orchestrator, workflow-utilities, initialize-repository, agentdb-state-manager)
- README.md coverage: All skills
- Version validation: All checks passed

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
| 1.5.1   | 2025-11-04 | PATCH | Bug fixes + comprehensive skill documentation |
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
