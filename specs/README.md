# Specifications

## Overview

This directory contains technical specifications and implementation plans created by SpecKit (Phase 2) for each feature under development.

## Contents

Each feature has its own subdirectory with:
- **spec.md** - Technical specification with architecture details, data models, APIs, security considerations, and edge cases
- **plan.md** - Implementation plan with ordered tasks, dependencies, and test strategy
- **CLAUDE.md** - Claude Code context for the specification
- **README.md** - Human-readable overview of the feature

## Structure

```
specs/
├── feature-1/
│   ├── spec.md
│   ├── plan.md
│   └── ARCHIVED/        # Old versions
├── feature-2/
│   ├── spec.md
│   ├── plan.md
│   └── ARCHIVED/
└── ARCHIVED/            # Completed features
```

## Usage

**Creating specifications (Phase 2):**

```bash
# From feature worktree, create specifications
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature <slug> <github-user> --todo-file ../TODO_feature_*.md
```

**Updating planning with as-built details (Phase 4):**

```bash
# After feature completion, update planning with actual implementation
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/<slug> specs/<slug>
```

## Relationship to Planning

- **planning/** (Phase 1) - High-level requirements and architecture from BMAD
- **specs/** (Phase 2) - Detailed technical specifications from SpecKit
- SpecKit reuses planning context to reduce token usage by 1,700-2,700 tokens per feature

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed Claude Code context and workflow integration.
