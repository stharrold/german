# Changelog - git-workflow-manager

All notable changes to the Git Workflow Manager skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automatic conflict detection in rebase operations
- Enhanced worktree cleanup with validation

## [5.0.0] - 2025-10-23

### Added
- `create_worktree.py` - Feature/hotfix/release worktree creation
- `create_release.py` - Release branch creation from develop
- `tag_release.py` - Tag release on main after PR merge
- `backmerge_release.py` - Back-merge release to develop
- `cleanup_release.py` - Cleanup release branch after completion
- `daily_rebase.py` - Rebase contrib branch onto develop
- `semantic_version.py` - Automatic version calculation

### Changed
- Git operations now use standalone scripts
- Worktree creation creates TODO files automatically
- Semantic versioning based on change analysis

### Token Efficiency
- Scripts handle git operations without consuming context
- No token impact (pure git operations)

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
