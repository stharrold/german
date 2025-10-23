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
- `spec.md.template` - Detailed technical specification (297 lines)
- `plan.md.template` - Task breakdown and implementation plan (367 lines)

## Interactive Specification Approach

SpecKit uses interactive Q&A to create detailed specifications informed by BMAD planning (if it exists).

### When BMAD Planning Exists (from Phase 1)

**Process:**
1. Read BMAD planning context from `../planning/<feature>/`
2. Analyze requirements, architecture, epics
3. Ask user about implementation preferences
4. Generate spec.md and plan.md informed by planning + user answers

**Interactive Q&A Flow:**

#### 1. Implementation Approach:
```
Based on the BMAD architecture (FastAPI + PostgreSQL), I'll create detailed specs.

For the data layer (Epic E-001):
  - Use SQLAlchemy ORM (from architecture.md)
  - How should we handle migrations? (Alembic / manual SQL)
  > [User chooses: Alembic]

  - Database connection pooling strategy? (default / custom pool size)
  > [User answers: Default]
```

#### 2. Testing Strategy:
```
BMAD requires ≥80% coverage. Let me plan the testing approach.

Testing breakdown:
  - Unit tests: ✓ (individual functions, classes)
  - Integration tests: ✓ (API endpoints with test database)
  - E2E tests: Optional (full workflows)

Do you want to add E2E tests? (Y/n)
> [User answers]

Do you want to add performance tests? (load testing with locust/k6)
> [User answers]

Do you want to add security tests? (OWASP checks, vulnerability scanning)
> [User answers]
```

#### 3. Task Breakdown Preferences:
```
From epics.md, I see 3 epics. How should I organize tasks?

Task granularity preference:
  - Small tasks (1-2 hours each) or larger tasks (half-day)?
  > [User chooses: Small tasks]

Implementation order:
  - Follow epic priority (E-001 → E-002 → E-003)?
  > [User confirms or suggests alternative]

Parallel work opportunities:
  - Can E-002 and E-003 be done in parallel? (depends on team size)
  > [User answers: Just me, sequential is fine]
```

**Output:**
- spec.md with detailed implementation approach
- plan.md with tasks organized per user preferences
- Both aligned with BMAD planning + user's implementation choices

### When BMAD Planning Doesn't Exist

**Process:**
1. Gather requirements from scratch through Q&A
2. Ask about technology stack preferences
3. Create lightweight planning inline
4. Generate spec.md and plan.md

**Interactive Q&A Flow:**

```
No BMAD planning found. I'll gather requirements to create specifications.

What is the main purpose of this feature?
> [User describes purpose]

Who will use this feature?
> [User describes users]

Technology stack preferences:
  - Web framework: FastAPI / Flask / Django?
  > [User chooses]

  - Database: SQLite / PostgreSQL / MySQL?
  > [User chooses]

  - Testing framework: pytest (recommended for this project)?
  > [User confirms]

[Continue with implementation approach, testing, task breakdown Q&A...]
```

**Output:**
- spec.md with gathered requirements and design
- plan.md with task breakdown
- Recommendation: Create BMAD planning for future features

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

## SpecKit → BMAD Feedback (As-Built Documentation)

After implementation completes and PR is merged to contrib branch, SpecKit outputs should update BMAD planning docs with as-built details.

### When to Update BMAD Planning

**Trigger:** Phase 4, after feature PR merged to contrib/<gh-user>

**Location:** Back in main repo on contrib branch

**Process:**
```bash
# After PR merge, back in main repo
cd /Users/user/Documents/GitHub/german
git checkout contrib/stharrold
git pull origin contrib/stharrold

# Run as-built documentation update
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/<feature>/ \
  specs/<feature>/
```

### What Gets Updated

**planning/<feature>/requirements.md:**
```markdown
## As-Built Notes

**Implementation Date:** 2025-10-23
**Final Implementation:** specs/<feature>/spec.md in feature worktree

### Deviations from Original Plan

**FR-001: Original Requirement**
- Planned: Use Redis for caching
- As-Built: Used in-memory caching (LRU cache)
- Reason: Redis not needed for current scale, simpler deployment

**FR-003: Original Requirement**
- Planned: Real-time WebSocket updates
- As-Built: Polling every 30 seconds
- Reason: Simpler implementation, meets performance requirements

### Lessons Learned

- Database connection pooling: Default settings were sufficient
- Testing: Achieved 87% coverage (exceeded 80% goal)
- Performance: Response times < 100ms (better than 200ms target)
```

**planning/<feature>/architecture.md:**
```markdown
## As-Built Architecture

**Implemented:** 2025-10-23
**Detailed Spec:** specs/<feature>/spec.md

### Technology Stack (Final)

Matches planned architecture with these changes:
- Database: PostgreSQL (as planned)
- Caching: ~~Redis~~ → Python LRU cache
- API Framework: FastAPI (as planned)

### Actual Data Models

Final database schema implemented in src/models/:
- [Link to actual code files]
- Schema migration: migrations/versions/abc123_initial.py

### API Endpoints (Implemented)

All planned endpoints implemented:
- POST /api/endpoint (spec.md line 89)
- GET /api/endpoint/{id} (spec.md line 144)
- Additional endpoint added: GET /api/endpoint/search (user request)

### Performance Metrics (Actual)

- Response time p95: 87ms (target: 200ms) ✓
- Throughput: 1200 req/s (target: 1000 req/s) ✓
- Test coverage: 87% (target: 80%) ✓
```

**planning/<feature>/epics.md:**
```markdown
## Epic Completion Status

### E-001: Data Layer (COMPLETED)
- Status: ✓ Completed 2025-10-23
- Actual effort: 2.5 days (estimated: 3 days)
- Delivered:
  - Database models (src/models/example.py)
  - Migrations (migrations/versions/)
  - Unit tests (tests/test_models.py)
- Notes: Faster than expected, schema design was solid

### E-002: API Layer (COMPLETED)
- Status: ✓ Completed 2025-10-25
- Actual effort: 3 days (estimated: 3 days)
- Delivered:
  - FastAPI routes (src/api/routes.py)
  - Request/response models (src/api/models.py)
  - Integration tests (tests/test_api.py)
- Deviations:
  - Added search endpoint (not in original epic)
  - Used simpler caching strategy

### E-003: Testing & Quality (COMPLETED)
- Status: ✓ Completed 2025-10-26
- Actual effort: 1.5 days (estimated: 2 days)
- Delivered:
  - Test coverage: 87% (target: 80%)
  - All quality gates passing
- Notes: Exceeded coverage target

## Lessons Learned for Future Epics

1. **Estimation accuracy:** Data layer took less time due to good planning
2. **Scope changes:** Added search endpoint mid-implementation (user request)
3. **Technology choices:** Simpler caching was sufficient, saved complexity
4. **Quality gates:** Setting ≥80% coverage target was appropriate
```

### Script: `update_asbuilt.py`

**Location:** `.claude/skills/speckit-author/scripts/update_asbuilt.py`

**Purpose:** Reads specs/ from worktree, updates planning/ with as-built details

**Usage:**
```bash
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/my-feature/ \
  specs/my-feature/
```

**What it does:**
1. Read spec.md and plan.md from merged feature specs/
2. Extract: deviations, actual timelines, lessons learned
3. Update planning/ files with "As-Built" sections
4. Prompt user for: deviation reasons, lessons learned, metrics
5. Commit updates to contrib branch

**Interactive prompts:**
```
Reading as-built specs from merged feature...
  ✓ Found specs/my-feature/spec.md
  ✓ Found specs/my-feature/plan.md

Analyzing deviations from BMAD planning...

Found potential deviation:
  Planned: Redis caching (architecture.md line 64)
  As-Built: LRU cache (spec.md line 142)

Why was this changed?
> [User explains: Simpler, meets requirements]

[Continue for all deviations...]

Found completed epics:
  E-001: Data Layer (3 tasks completed)
  E-002: API Layer (4 tasks completed)

E-001 estimated 3 days, how long did it actually take?
> [User: 2.5 days]

Any lessons learned for E-001?
> [User: Schema design was solid, migrations went smoothly]

[Continue for all epics...]

Updating planning documents...
  ✓ Updated planning/my-feature/requirements.md (added as-built notes)
  ✓ Updated planning/my-feature/architecture.md (added as-built architecture)
  ✓ Updated planning/my-feature/epics.md (added completion status)

Commit these updates? (Y/n)
```

### Why This Matters

**Living Documentation:**
- Planning docs evolve from "planned" to "as-built"
- Historical record of decisions and changes
- Future features can reference actual outcomes

**Improved Planning:**
- Learn from deviations (why did we change the plan?)
- Improve estimation accuracy (actual vs estimated effort)
- Identify patterns (certain epics always take longer)

**Traceability:**
```
requirements.md (planned) → spec.md (detailed) → src/ (code) → requirements.md (as-built)
```
- Complete lifecycle documented
- Easy to find why decisions were made
- Reference for similar future features
