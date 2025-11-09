# Changelog

All notable changes to the German Language Learning Repository workflow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- None currently planned

## [1.9.0] - 2025-11-09

### Added
- **Work-item generation workflow (Option A)** - Complete PR feedback handling system
  - VCS-agnostic PR comment extraction (GitHub + Azure DevOps support)
  - Automatic work-item generation from unresolved PR conversations
  - `generate_work_items_from_pr.py` script with auto-detection of VCS provider
  - Work-item slug pattern: `pr-{pr_number}-issue-{sequence}`
  - Compatible with all issue tracking systems
  - Token-efficient implementation (pure CLI operations, no prompt overhead)
  - Successfully demonstrated 5-level nested workflow capability (14 PRs, 10 work-items)

- **VCS adapter enhancements** - Extended PR feedback capabilities
  - `fetch_pr_comments()` method in AzureDevOpsAdapter and GitHubAdapter
  - Conversation thread support with resolution status tracking
  - Unified comment format across GitHub and Azure DevOps providers
  - Filtering for unresolved conversations only

- **ARCHITECTURE.md** - Comprehensive workflow architecture documentation (604 lines)
  - High-level execution flow and phase map (Phases 0-6)
  - Key architectural patterns (progressive skill loading, BMAD→SpecKit context reuse)
  - Token efficiency analysis (50-92% reductions through various patterns)
  - Skill integration patterns and decision trees
  - Complete constants reference with rationale
  - Critical design decisions and system constraints

### Changed
- **WORKFLOW.md updates** - Enhanced Phase 4.3 documentation
  - Added PR Feedback Handling workflow (Option A: work-items)
  - Decision tree for simple fixes vs. substantive changes
  - Work-item generation and nested workflow patterns
  - Updated Phase 4 steps to include optional feedback handling

- **CLAUDE.md improvements** - Added architectural cross-references
  - Cross-reference to ARCHITECTURE.md for deep-dive analysis
  - Separation of concerns: operational guidance (CLAUDE.md) vs. architecture (ARCHITECTURE.md)
  - Improved navigation for future Claude Code instances

### Fixed
- **Azure DevOps repository parameter handling** - Fixed 4 related issues (#105-106, #110, #112, #115)
  - Issue #105 (PR #107): Added warning when repository extraction returns None
  - Issue #106 (PR #108): Fixed AttributeError when repository parameter is None
  - Issue #110 (PR #111): Enhanced repository parameter validation with better error messages
  - Issue #112 (PR #113): Optimized validation to avoid redundant strip() calls
  - Issue #115 (PR #116): Documented empty string behavior for repository parameter

- **ARCHITECTURE.md documentation clarifications** - Fixed 4 GitHub Copilot review issues (#120-123)
  - Issue #120 (PR #124): Clarified pseudo-code notation (algorithmic, not executable Python)
  - Issue #121 (PR #124): Standardized terminology for PR merge operations
  - Issue #122 (PR #124): Enhanced timestamp format description with rationale
  - Issue #123 (PR #124): Clarified branch protection policy (no direct local commits/pushes)

- **Code quality improvements**
  - Fixed linting errors in generate_work_items_from_pr.py
  - Resolved all GitHub Copilot code review issues from PR feedback iterations

### Workflow Metrics
- **Total PRs:** 14 (all merged successfully)
  - PR #95: Initial work-item generation implementation
  - PR #104, #107-109, #111, #113-114, #116-119, #124-125: Nested fixes and improvements
- **Work-items generated:** 10 issues across 5 nested levels
- **Nested workflow depth:** 5 levels (unprecedented recursive dogfooding)
- **PR merge pattern:** feature → contrib → develop (branch protection compliant)

### Quality
- All tests passing (114 passed, 15 skipped)
- Test coverage: 88% (above required 80%)
- Linting: Clean - all ruff checks pass
- Type checking: Clean - all mypy checks pass
- Build: Successful

### Migration Notes
- Replaces iterative PR feedback workflow (Option B) with work-item generation (Option A)
- No breaking changes - backward compatible with existing workflows
- Work-item generation is optional; simple fixes can still be done directly on PR branch


## [1.8.2] - 2025-11-07

### Fixed
- **GitHub Copilot code quality issues** - Resolved 7 code quality issues (Issues #77-#84)
  - Issue #84: Fixed version reference (v1.8.1 → v1.8.0) in backmerge_release.py
  - Issue #83: Removed extra bracket in markdown link (migrate_directory_frontmatter.py:222)
  - Issue #82: Removed extra bracket in markdown link (migrate_directory_frontmatter.py:213)
  - Issue #81: Removed extra bracket in markdown link (specs/CLAUDE.md:68)
  - Issue #79: Fixed git merge abort logic (use --no-commit + git merge --abort)
  - Issue #78: Clarified conflicts parameter docstring in create_pr function
  - Issue #77: Fixed YAML formatting inconsistency (directory_structure.py)

### Changed
- **Simplified backmerge workflow** - Updated backmerge_release.py to pure PR-based workflow
  - Removed all local merge operations (checkout, merge, abort)
  - Script now only validates inputs and creates PR directly
  - GitHub/CI automatically detects merge conflicts
  - Eliminated uncommitted changes issues (uv.lock modifications)
  - Reduced code by 204 lines (cleaner and simpler)
  - Follows pure PR-based workflow principle

### Quality
- All tests passing (114 passed, 15 skipped)
- Test coverage: 88% (above required 80%)
- Linting: Clean - all checks pass

## [1.8.1] - 2025-11-07

### Fixed
- **Branch protection compliance** - Enforced PR workflow for all merges to protected branches
  - Updated backmerge_release.py to create PRs instead of direct pushes
  - Removed branch protection exception from WORKFLOW.md
  - Self-merge enabled (no approval required for compliant workflow)

### Added
- **Azure DevOps branch policies documentation** - Comprehensive guide for Azure DevOps users
  - Created .github/AZURE_DEVOPS_POLICIES.md (644 lines)
  - Complete policy configuration for main and develop branches
  - Build validation, required reviewers, merge strategies
  - Work item linking and comment requirements
  - Migration guide from GitHub branch protection

### Documentation
- Updated CLAUDE.md with v1.8.1 release information
- Updated WORKFLOW.md to remove branch protection exception
- Added Azure DevOps policy references throughout workflow docs

## [1.8.0] - 2025-11-07

### Added
- **CI/CD replication guide** - Comprehensive guide for replicating GitHub Actions to other platforms
  - Created WORKFLOW-INIT-PROMPT.md - DRY navigation guide (~500 tokens)
  - Reference-based navigation to avoid duplication
  - Progressive skill loading pattern
  - Token-efficient workflow initialization

### Changed
- **Workflow documentation** - Improved navigation and reduced duplication
  - Restructured CLAUDE.md to use reference pattern
  - Added quick-start workflow initialization
  - Improved token efficiency for skill loading

## [1.7.0] - 2025-11-06

### Added
- **Cross-platform CI/CD infrastructure** - GitHub Actions workflow for automated testing
  - Created .github/workflows/tests.yml - Run tests on push/PR
  - Python 3.12 test environment
  - UV package manager integration
  - Automated pytest execution with coverage reporting
  - Cross-platform testing (Ubuntu, macOS, Windows)

### Quality
- Automated test execution on all PRs
- Coverage reporting in CI/CD pipeline
- Multi-platform validation

## [1.6.0] - 2025-11-04

### Added
- **GitHub Issue Management documentation** - Comprehensive issue tracking workflow added to CLAUDE.md
  - Documents issue sources (Copilot reviews, manual creation, security alerts)
  - 5-step issue workflow (fix on contrib, reference in commits, PR to develop, auto-close)
  - Common issue types with solutions (unused variables, bare except, line length, syntax, security)
  - Quality commands reference (ruff, pytest)
  - Best practices for issue handling
- **Production Safety & Rollback procedures** - Emergency rollback documentation
  - Added "Production Safety & Rollback" section to WORKFLOW.md
  - 3 rollback scenarios (fast rollback, revert + hotfix, rollback decision tree)
  - Timeline estimates (10 min rollback, 20 min cleanup)
  - Tag-based deployment principles (immutable, reproducible, instant rollback)
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

### Fixed
- **GitHub Copilot code quality issues** - Resolved 13 code quality issues (Issues #43-#57)
  - Removed unused variables: args, timestamp, all_valid, result, commit_sha, req_path (Issues #44-47)
  - Fixed bare except blocks with specific exception types (Issue #49)
  - Fixed Python 3 syntax error: double backslash line continuation (Issue #48)
  - Clarified commented code as intentional placeholder (Issue #43)
  - Fixed regex false positives in branch protection tests with word boundaries (Issue #53)
  - Fixed duplicate violation logic with break statement (Issue #52)
  - Added explanatory comment to empty except/pass block (Issue #57)
  - Documented title variable usage in commit messages (Issue #56)
  - Added rollback safety warning to WORKFLOW.md (Issue #54)
- **Pydantic v2 migration** - Updated from deprecated v1 Config to v2 ConfigDict
  - Changed `class Config:` to `model_config = ConfigDict()` in src/german/models.py
  - Maintains same behavior (use_enum_values=True)
  - Eliminates deprecation warnings

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
- All 127 tests passing (112 passed, 15 skipped)
- Test coverage: 88.1% (above required 80%)
- Version validation: All checks passed
- Linting: Clean - all pyflakes (F-series) checks pass
- All GitHub Copilot code review issues resolved

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
| 1.8.2   | 2025-11-07 | PATCH | Bug fixes for code quality issues + simplified backmerge workflow |
| 1.8.1   | 2025-11-07 | PATCH | Branch protection compliance + Azure DevOps documentation |
| 1.8.0   | 2025-11-07 | MINOR | CI/CD replication guide + DRY navigation improvements |
| 1.7.0   | 2025-11-06 | MINOR | Cross-platform CI/CD infrastructure (GitHub Actions) |
| 1.6.0   | 2025-11-04 | MINOR | Branch protection + GitHub issue management + rollback procedures |
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
