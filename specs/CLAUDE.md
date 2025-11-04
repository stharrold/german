# Claude Code Context: specs

## Purpose

Storage for SpecKit specifications (Phase 2) created during feature development. Each feature has a subdirectory with technical specifications and implementation plans.

## Directory Structure

```
specs/
├── <feature-slug>/           # One directory per feature
│   ├── spec.md              # Technical specification (from SpecKit)
│   ├── plan.md              # Implementation plan with tasks (from SpecKit)
│   ├── CLAUDE.md            # Context for this feature's specs
│   ├── README.md            # Human-readable overview
│   └── ARCHIVED/            # Deprecated spec versions
├── CLAUDE.md                # This file
├── README.md                # Human-readable overview
└── ARCHIVED/                # Archived feature specs (after completion)
```

## SpecKit Integration (Phase 2)

**Created by:** `python .claude/skills/speckit-author/scripts/create_specifications.py`

**When:** Phase 2 (Development), after BMAD planning (Phase 1)

**Location:** Feature worktrees create specs in this directory via `../specs/<slug>/`

**Contents:**
- `spec.md` - Technical specification with architecture, data models, APIs, edge cases
- `plan.md` - Implementation plan with ordered tasks, dependencies, test strategy
- Tasks from plan.md automatically added to `../TODO_feature_*.md` frontmatter

## Workflow Integration

**Phase 1 (Planning):** BMAD creates `planning/<slug>/` with requirements/architecture

**Phase 2 (Development):** SpecKit auto-detects planning context, creates `specs/<slug>/`
- Adaptive Q&A: 5-8 questions (with BMAD) vs 10-15 (without BMAD)
- Token savings: 1,700-2,700 tokens by reusing planning context

**Phase 4 (Integration):** `update_asbuilt.py` compares specs/ with planning/ to document deviations

**Phase 4.3 (Archival):** Completed specs moved to `specs/ARCHIVED/<slug>/` or `ARCHIVED/specs_<slug>.zip`

## Related Skills

- speckit-author (Phase 2: creates specifications)
- bmad-planner (Phase 1: provides planning context)
- workflow-utilities (archival, directory management)
- git-workflow-manager (worktree management)
