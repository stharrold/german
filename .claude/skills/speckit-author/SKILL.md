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

    # Check for BMAD planning docs in main repo
    planning_dir = Path('../planning') / slug
    has_planning = planning_dir.exists()

    if has_planning:
        # Read BMAD context
        requirements = (planning_dir / 'requirements.md').read_text()
        architecture = (planning_dir / 'architecture.md').read_text()
        epics = (planning_dir / 'epics.md').read_text() if (planning_dir / 'epics.md').exists() else None

        # Create specifications WITH planning context
        create_specifications_with_context(
            slug, workflow_type, gh_user,
            requirements_context=requirements,
            architecture_context=architecture,
            epics_context=epics
        )
    else:
        # Create specifications WITHOUT planning context
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

## Using BMAD Planning Context

When BMAD planning documents exist in `../planning/<feature>/`:

### SpecKit Should:

**1. Read planning context:**
```python
# Read BMAD planning docs from main repo
requirements = Path('../planning/<feature>/requirements.md').read_text()
architecture = Path('../planning/<feature>/architecture.md').read_text()
epics = Path('../planning/<feature>/epics.md').read_text()
```

**2. Extract key information:**
- **From requirements.md:**
  - Functional requirements (FR-001, FR-002...)
  - Non-functional requirements (performance, security, scalability)
  - User stories and acceptance criteria
  - Success criteria and constraints

- **From architecture.md:**
  - Technology stack and framework choices
  - Data models and database schema
  - API endpoint definitions
  - Container configuration
  - Security and error handling strategies

- **From epics.md:**
  - Epic breakdown (E-001, E-002...)
  - Epic priorities (P0, P1, P2)
  - Epic dependencies
  - Implementation timeline

**3. Generate spec.md informed by planning:**
```markdown
# spec.md sections should reference BMAD docs

## Functional Requirements
FR-001 from requirements.md: [Requirement description]
  - Acceptance Criteria (from requirements.md):
    - [ ] AC 1...
    - [ ] AC 2...

## Technology Stack
Stack defined in architecture.md:
  - Language: Python 3.11+
  - Framework: FastAPI (chosen in architecture.md)
  - Database: PostgreSQL (from architecture.md)

## Security Requirements
From architecture.md Section "Security Considerations":
  - Authentication: JWT tokens
  - Authorization: RBAC
  - Input validation: JSON schema
```

**4. Generate plan.md informed by epics:**
```markdown
# plan.md tasks organized by epic

## Epic E-001: Data Layer (from epics.md)
Priority: P0 (Foundation)
Dependencies: None

Tasks:
- [ ] impl_001: Create database schema (from architecture.md data models)
- [ ] impl_002: Implement ORM entities
- [ ] test_001: Unit tests for data layer

## Epic E-002: API Layer (from epics.md)
Priority: P0 (Core functionality)
Dependencies: E-001

Tasks:
- [ ] impl_003: Create API endpoints (from architecture.md)
- [ ] impl_004: Implement request validation
- [ ] test_002: API integration tests
```

### Interactive Prompts

**When planning exists:**
```
I found BMAD planning documents:
  ✓ planning/<feature>/requirements.md (15 functional requirements)
  ✓ planning/<feature>/architecture.md (Python/FastAPI stack, PostgreSQL)
  ✓ planning/<feature>/epics.md (3 epics: Data, API, Tests)

I'll use these as context to create detailed SpecKit specifications.

Based on the requirements, I see these priority P0 epics:
  - E-001: Data Layer (Foundation)
  - E-002: API Layer (Core functionality)

The architecture specifies:
  - Framework: FastAPI
  - Database: PostgreSQL with SQLAlchemy
  - Testing: pytest with ≥80% coverage

Would you like me to expand on any areas before generating specs? (Y/n)
```

**When no planning:**
```
No BMAD planning documents found.

I'll create specifications from scratch through interactive Q&A.

What is the main purpose of this feature?
> [User describes]

What technology stack should we use?
> [User specifies or accepts defaults]

Any specific performance or security requirements?
> [User answers]

Generating specifications...
```

## Best Practices

### When BMAD Planning Exists:

- **Use planning as foundation**: Reference `../planning/<feature>/requirements.md` sections
- **Be consistent**: Technology choices must match `architecture.md`
- **Epic-driven tasks**: Break down `plan.md` tasks by epic from `epics.md`
- **Acceptance criteria alignment**: `spec.md` AC must cover `requirements.md` success criteria
- **Traceability**: spec.md references FR-001, FR-002...; plan.md references E-001, E-002...
- **Justify deviations**: If deviating from architecture.md, document why

### When BMAD Planning Doesn't Exist:

- **Gather requirements interactively**: Ask user for purpose, users, success criteria
- **Document assumptions**: State technology choices and rationale
- **Start simple**: Can always add complexity later
- **Ask clarifying questions**: Better to clarify upfront than rework later

### Always:

- **Be specific**: Include exact file names, function signatures, data structures
- **Code examples**: Show actual implementation patterns
- **API contracts**: Define exact request/response formats
- **Test cases**: Specify what to test and expected outcomes
- **Dependencies**: List what must be done first (refer to epic dependencies)
