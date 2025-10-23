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
- `requirements.md.template` - Business requirements and acceptance criteria (170 lines)
- `architecture.md.template` - System architecture and design decisions (418 lines)
- `epics.md.template` - Epic breakdown with priorities and dependencies (245 lines)

## Interactive Planning Approach

BMAD uses a three-persona method to gather comprehensive planning information through interactive Q&A sessions with the user.

### 🧠 Persona 1: BMAD Analyst (Requirements)

**Role:** Business Analyst creating Product Requirements Document

**Process:**
1. Ask user about problem statement and business context
2. Identify target users and stakeholders
3. Define success criteria and measurable outcomes
4. Gather functional and non-functional requirements
5. Document user stories with scenarios
6. Identify risks and constraints

**Interactive Q&A Example:**
```
I'll help create the requirements document using the BMAD Analyst persona.

What problem does this feature solve?
> [User describes the problem]

Who are the primary users of this feature?
> [User identifies user types]

How will we measure success for this feature?
> [User defines success metrics]

What are the must-have capabilities? (functional requirements)
> [User lists key capabilities]

Any performance, security, or scalability requirements? (non-functional)
> [User specifies NFRs]
```

**Generates:** `planning/<feature>/requirements.md` using comprehensive template

### 🏗️ Persona 2: BMAD Architect (Architecture)

**Role:** Technical Architect designing system architecture

**Process:**
1. Read requirements.md for business context
2. Ask user about technology preferences and constraints
3. Design system components and data models
4. Define API contracts and integration points
5. Specify security, error handling, testing strategies
6. Document deployment and observability approach

**Interactive Q&A Example:**
```
Based on the requirements, I'll design the technical architecture.

Technology preferences?
- Web framework: FastAPI / Flask / Django?
> [User chooses framework]

Database requirements?
- Development: SQLite
- Production: PostgreSQL / MySQL?
> [User chooses database]

Performance targets?
- Response time: < 200ms?
- Concurrent users: How many?
> [User specifies targets]

Container strategy?
- Using Podman (default for this project)
- Multi-container setup needed?
> [User confirms approach]
```

**Generates:** `planning/<feature>/architecture.md` using comprehensive template

### 📋 Persona 3: BMAD PM (Epic Breakdown)

**Role:** Project Manager breaking down work into epics

**Process:**
1. Read requirements.md + architecture.md for full context
2. Identify major work streams (epics)
3. Define scope, complexity, and dependencies for each epic
4. Prioritize epics (P0/P1/P2)
5. Create implementation timeline
6. Estimate effort and identify risks

**Analysis:**
```
Analyzing requirements and architecture to create epic breakdown...

Identified 3 major epics:
1. E-001: Data Layer (Foundation) - P0, High complexity
2. E-002: API Layer (Core functionality) - P0, Medium complexity
3. E-003: Testing & Quality - P1, Medium complexity

Dependencies detected:
  E-001 → E-002 (API needs data layer)
  E-002 → E-003 (tests need API)

Creating epic breakdown document...
```

**Generates:** `planning/<feature>/epics.md` with epic definitions, priorities, timeline

## How to Invoke BMAD

When workflow-orchestrator loads bmad-planner during Phase 1:

**Sequential Execution:**
```
1. Load bmad-planner skill
2. Execute BMAD Analyst persona
   ├─ Interactive Q&A with user
   ├─ Generate planning/<feature>/requirements.md
   └─ Commit to contrib branch

3. Execute BMAD Architect persona
   ├─ Read requirements.md for context
   ├─ Interactive Q&A with user
   ├─ Generate planning/<feature>/architecture.md
   └─ Commit to contrib branch

4. Execute BMAD PM persona
   ├─ Read requirements.md + architecture.md
   ├─ Analyze and break down into epics
   ├─ Generate planning/<feature>/epics.md
   └─ Commit to contrib branch
```

**User Experience:**
```
Phase 1: BMAD Planning Session

🧠 BMAD Analyst: Creating requirements...
  [Interactive Q&A - 5-10 questions]
  ✓ Generated: planning/my-feature/requirements.md

🏗️ BMAD Architect: Designing architecture...
  [Interactive Q&A - 5-8 questions]
  ✓ Generated: planning/my-feature/architecture.md

📋 BMAD PM: Breaking down into epics...
  [Automatic analysis based on requirements + architecture]
  ✓ Generated: planning/my-feature/epics.md

✓ BMAD planning complete!
  Next: Create feature worktree (Phase 2 will use these docs)
```

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

## Output Files

BMAD generates three planning documents that become input context for SpecKit:

```
planning/<feature-name>/
├── requirements.md    # Business requirements (170 lines from template)
│   ├─ Problem statement, stakeholders
│   ├─ Functional requirements (FR-001, FR-002...)
│   ├─ Non-functional requirements (performance, security...)
│   ├─ User stories with scenarios
│   └─ Risks, assumptions, success criteria
│
├── architecture.md    # Technical architecture (418 lines from template)
│   ├─ System overview, components
│   ├─ Technology stack with justifications
│   ├─ Data models, API endpoints
│   ├─ Container architecture (Containerfile, podman-compose.yml)
│   ├─ Security, error handling, testing strategies
│   └─ Deployment, observability, disaster recovery
│
├── epics.md          # Epic breakdown (245 lines from template)
│   ├─ Epic definitions (scope, complexity, priority)
│   ├─ Dependencies and critical path
│   ├─ Implementation timeline
│   └─ Resource requirements and risks
│
├── CLAUDE.md         # Context for this planning directory
├── README.md         # Human-readable overview
└── ARCHIVED/         # Deprecated planning documents
```

**These files become input context for SpecKit in Phase 2.**

## Integration with SpecKit

BMAD documents are used as context when creating SpecKit specifications:

### Data Flow: BMAD → SpecKit

**Phase 1 (Main Repo, contrib branch):**
```
BMAD Interactive Session
  ↓
planning/<feature>/
├── requirements.md
├── architecture.md
└── epics.md
```

**Create Worktree:**
```bash
# Worktree creation preserves link to main repo
git worktree add ../repo_feature_<slug> feature/<timestamp>_<slug>
```

**Phase 2 (Worktree):**
```
SpecKit reads from main repo:
../planning/<feature>/requirements.md → Business context
../planning/<feature>/architecture.md → Technical design
../planning/<feature>/epics.md        → Epic priorities

SpecKit generates (informed by BMAD):
specs/<feature>/spec.md  ← Detailed specification
specs/<feature>/plan.md  ← Implementation tasks
```

### Why This Connection Matters

**Consistency:**
- Technology choices in spec.md match architecture.md stack
- spec.md acceptance criteria cover requirements.md success criteria
- plan.md tasks align with epics.md breakdown

**Completeness:**
- All functional requirements from requirements.md appear in spec.md
- Non-functional requirements (performance, security) included
- Epic dependencies reflected in plan.md task ordering

**Traceability:**
- spec.md sections reference FR-001, FR-002... from requirements.md
- plan.md tasks map to E-001, E-002... from epics.md
- Architecture decisions from architecture.md justify implementation choices

**Less Rework:**
- Planning clarifies requirements before coding
- Design decisions made explicit
- Reduces ambiguity and prevents scope creep

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
