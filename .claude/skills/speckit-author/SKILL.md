---
name: speckit-author
version: 5.0.0
description: |
  Creates SpecKit specifications (spec.md, plan.md) in feature/release/hotfix
  worktrees. Detailed implementation guidance.

  Use when: In worktree, need specifications, implementation planning

  Triggers: write spec, create plan, feature specification
---

# SpecKit Author

## Purpose

Creates detailed specifications and implementation plans for features,
releases, and hotfixes within worktree directories.

## When to Use

- Current directory: worktree (feature/release/hotfix)
- Phase: Specification (Phase 2)

## Document Templates

Templates are located in `templates/`:
- `spec.md.template` - Detailed technical specification
- `plan.md.template` - Task breakdown and implementation plan

## Creating Specifications

```python
from pathlib import Path
from datetime import datetime

def create_specifications(slug, workflow_type, gh_user):
    """Create SpecKit documents in worktree."""

    date = datetime.utcnow().strftime('%Y-%m-%d')

    # Create specs directory
    specs_dir = Path('specs') / slug
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Load and customize spec template
    templates_dir = Path('.claude/skills/speckit-author/templates')

    with open(templates_dir / 'spec.md.template') as f:
        spec = f.read()

    spec = spec.replace('{{TITLE}}', slug.replace('-', ' ').title())
    spec = spec.replace('{{WORKFLOW_TYPE}}', workflow_type)
    spec = spec.replace('{{SLUG}}', slug)
    spec = spec.replace('{{DATE}}', date)
    spec = spec.replace('{{GH_USER}}', gh_user)

    with open(specs_dir / 'spec.md', 'w') as f:
        f.write(spec)

    # Load and customize plan template
    with open(templates_dir / 'plan.md.template') as f:
        plan = f.read()

    plan = plan.replace('{{TITLE}}', slug.replace('-', ' ').title())
    plan = plan.replace('{{WORKFLOW_TYPE}}', workflow_type)
    plan = plan.replace('{{SLUG}}', slug)
    plan = plan.replace('{{DATE}}', date)

    with open(specs_dir / 'plan.md', 'w') as f:
        f.write(plan)

    print(f"✓ Specifications created in {specs_dir}")
```

## Directory Structure

Specification documents are created in:

```
specs/
└── <feature-slug>/
    ├── spec.md           # Technical specification
    ├── plan.md          # Implementation plan
    ├── CLAUDE.md        # Context for this spec
    ├── README.md        # Human-readable overview
    └── ARCHIVED/        # Deprecated specs
```

## Integration with Workflow

The workflow-orchestrator calls this skill during Phase 2:

```python
# In workflow orchestrator
if current_phase == 2 and current_step == '2.2':
    load_skill('speckit-author')
    create_specifications(slug, workflow_type, gh_user)
    commit_changes('docs: add SpecKit specifications for ' + slug)
```

## Template Placeholders

Both templates use these placeholders:
- `{{TITLE}}` - Feature name (title case)
- `{{WORKFLOW_TYPE}}` - feature, release, or hotfix
- `{{SLUG}}` - Feature slug (kebab-case)
- `{{DATE}}` - Creation date (YYYY-MM-DD)
- `{{GH_USER}}` - GitHub username

## Best Practices

- **Reference requirements**: Link back to planning/requirements.md
- **Be specific**: Include exact file names, function signatures, data structures
- **Code examples**: Show actual implementation patterns
- **API contracts**: Define exact request/response formats
- **Test cases**: Specify what to test and expected outcomes
- **Dependencies**: List what must be done first
