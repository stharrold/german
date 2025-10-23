# German Language Learning Repository

A Python-based repository for German language learning resources with an automated skill-based development workflow.

## Purpose

This repository contains:
- German language reference materials (vocabulary, grammar, etc.)
- Python tools for language processing and learning
- Structured German language content data
- Workflow v5.0 skill-based architecture for development

## Quick Start

```bash
# Install dependencies
uv sync

# Authenticate with GitHub
gh auth login

# Start development workflow
# Say "next step?" to Claude Code
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide with command reference
- **[WORKFLOW.md](WORKFLOW.md)** - Complete 5-phase workflow guide (setup, planning, development, quality, integration, release)

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **Testing:** pytest with ≥80% coverage requirement
- **Linting:** ruff
- **Type Checking:** mypy
- **Containerization:** Podman (optional)
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees

## Workflow Overview

This project uses a skill-based progressive workflow:

1. **Phase 0:** Initial setup and prerequisites
2. **Phase 1:** Planning with BMAD (requirements + architecture)
3. **Phase 2:** Feature development in isolated worktrees
4. **Phase 3:** Quality assurance (tests, coverage, linting, types)
5. **Phase 4:** Integration via pull requests
6. **Phase 5:** Production releases with semantic versioning

For complete workflow details, see [WORKFLOW.md](WORKFLOW.md).

## Development Commands

See [CLAUDE.md](CLAUDE.md) for complete command reference.

Quick reference:
```bash
# Create feature worktree
python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature <slug> contrib/<user>

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Run tests with coverage
uv run pytest --cov=src --cov-fail-under=80
```

## Contributing

This repository uses `contrib/<gh-user>` branches for personal contributions. See [WORKFLOW.md](WORKFLOW.md) Phase 4 for the complete integration process.

## License

[Add license information]
