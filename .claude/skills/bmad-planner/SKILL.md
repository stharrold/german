---
name: bmad-planner
version: 5.0.0
description: |
  Creates BMAD planning documents (requirements, architecture) in main
  repository on contrib branch. Used before creating feature worktrees.

  Use when: On contrib branch, planning phase, need requirements/architecture

  Triggers: plan feature, requirements, architecture, BMAD
---

# BMAD Planner

## Purpose

Business Model, Architecture, and Design documentation created in main
repository before feature development begins.

## When to Use

- Current directory: main repository (not worktree)
- Current branch: `contrib/<gh-user>`
- Phase: Planning (Phase 1)

## Document Templates

Templates are located in `templates/`:
- `requirements.md.template` - Business requirements and acceptance criteria
- `architecture.md.template` - System architecture and design decisions

## Creating Planning Documents

```python
from pathlib import Path
from datetime import datetime

def create_planning_docs(feature_name, gh_user):
    """Create BMAD planning documents for a feature."""

    date = datetime.utcnow().strftime('%Y-%m-%d')

    # Create planning directory
    planning_dir = Path('planning') / feature_name
    planning_dir.mkdir(parents=True, exist_ok=True)

    # Load and customize requirements template
    templates_dir = Path('.claude/skills/bmad-planner/templates')

    with open(templates_dir / 'requirements.md.template') as f:
        requirements = f.read()

    requirements = requirements.replace('{{TITLE}}', feature_name)
    requirements = requirements.replace('{{DATE}}', date)
    requirements = requirements.replace('{{GH_USER}}', gh_user)

    with open(planning_dir / 'requirements.md', 'w') as f:
        f.write(requirements)

    # Load and customize architecture template
    with open(templates_dir / 'architecture.md.template') as f:
        architecture = f.read()

    architecture = architecture.replace('{{TITLE}}', feature_name)
    architecture = architecture.replace('{{DATE}}', date)
    architecture = architecture.replace('{{GH_USER}}', gh_user)

    with open(planning_dir / 'architecture.md', 'w') as f:
        f.write(architecture)

    print(f"✓ Planning documents created in {planning_dir}")
```

## Directory Structure

Planning documents are created in:

```
planning/
└── <feature-name>/
    ├── requirements.md    # Business requirements
    ├── architecture.md    # Technical architecture
    ├── CLAUDE.md         # Context for this planning directory
    ├── README.md         # Human-readable overview
    └── ARCHIVED/         # Deprecated planning documents
```

## Integration with Workflow

The workflow-orchestrator calls this skill during Phase 1:

```python
# In workflow orchestrator
if current_phase == 1 and current_step == '1.1':
    load_skill('bmad-planner')
    create_planning_docs(feature_name, gh_user)
    commit_changes('docs: add BMAD planning for ' + feature_name)
```

## Template Placeholders

Both templates use these placeholders:
- `{{TITLE}}` - Feature name (title case)
- `{{DATE}}` - Creation date (YYYY-MM-DD)
- `{{GH_USER}}` - GitHub username

## Best Practices

- **Requirements first**: Define business needs before technical design
- **Acceptance criteria**: Make success measurable
- **Architecture clarity**: Explain design decisions and trade-offs
- **Technology justification**: Document why specific tools/frameworks chosen
- **Non-functional requirements**: Don't forget performance, security, scalability
