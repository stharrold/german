# German Language Learning Repository

A Python-based repository for German language learning resources with a v7x1 workflow for autonomous development.

## Purpose

This repository contains:
- German language reference materials (vocabulary, grammar, etc.)
- Python tools for language processing and learning
- Structured German language content data
- v7x1 workflow with Claude Code for development automation

## Quick Start

```bash
# Install dependencies
uv sync

# Authenticate with your VCS provider
gh auth login              # For GitHub

# Start development workflow
/workflow:v7x1_1-worktree "feature description"
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide
- **[WORKFLOW.md](WORKFLOW.md)** - v7x1 workflow guide (4-step)

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **Testing:** pytest with coverage
- **Linting:** ruff
- **Type Checking:** mypy
- **Containerization:** Podman (optional)
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees
- **CI:** GitHub Actions (tests, Claude Code review)

**Protected Branches:** `main` and `develop` are permanent. Never delete or commit directly. All changes via PRs only.

## v7x1 Workflow

```
/workflow:v7x1_1-worktree "description"  → Create worktree + implement
/workflow:v7x1_2-integrate "branch"      → PR feature → contrib → develop
/workflow:v7x1_3-release [version]       → Release → main, tag
/workflow:v7x1_4-backmerge               → Sync release → develop
```

See [WORKFLOW.md](WORKFLOW.md) for full details.

## Development Commands

```bash
# Create feature worktree
/workflow:v7x1_1-worktree "add new vocabulary category"

# Run tests with coverage
uv run pytest --cov=src --cov-report=term

# Run linting
uv run ruff check .

# Run type checking
uv run mypy src/
```

## Using This Workflow in Other Projects

This repository's workflow can be applied to other projects using the bundle system from `stharrold-templates`:

```bash
# Clone templates
git clone https://github.com/stharrold/stharrold-templates.git .tmp/stharrold-templates

# Apply git workflow bundle
python .tmp/stharrold-templates/scripts/apply_bundle.py .tmp/stharrold-templates . --bundle git

# Cleanup
rm -rf .tmp/stharrold-templates
```

## Contributing

This repository uses `contrib/<gh-user>` branches for personal contributions. See [WORKFLOW.md](WORKFLOW.md) for the complete integration process.

## License

[Add license information]
