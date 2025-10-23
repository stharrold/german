---
type: claude-code-directive
name: Workflow-SpecKit-BMAD
version: 4.1.0
date: 2025-10-18
status: production-ready
purpose: Git-flow + GitHub-flow hybrid with BMAD + SpecKit + Claude Code orchestration
execution-model: interactive-confirmation
applies-to: full-stack web applications
---

# Claude Code Workflow: SpecKit-BMAD v4.1

## Directive for Claude Code

**YOU ARE CLAUDE CODE.** This document is your execution directive for orchestrating a git workflow that integrates:
- **BMAD Method** for requirements and architecture (in main repo)
- **SpecKit Method** for feature/release/hotfix specifications (in worktrees)
- **Multi-branch git strategy** with controlled promotion
- **Interactive user confirmation** at each step
- **Status tracking** in TODO_[feature,release,hotfix]_*.md files
- **Semantic versioning** based on component change analysis

### Your Core Responsibilities

1. **Detect project context** from package.json/pyproject.toml and adapt ALL examples
2. **Create workflow files** adapted to the detected tech stack
3. **Guide user step-by-step** with explicit confirmation prompts
4. **Execute git operations** after user confirms with "Y"
5. **Document progress** by updating TODO_[feature,release,hotfix]_*.md status entries
6. **Context-switch behavior** based on current directory:
   - In `/path/to/repo` on `contrib/gh-user` → Use BMAD workflow
   - In `/path/to/repo_*` → Use SpecKit workflow
7. **Reason through merge conflicts** with context-aware resolution
8. **Calculate semantic versions** by analyzing component changes
9. **Enforce quality gates**: 80% test coverage, passing tests, successful builds
10. **Manage context capacity**: At 50% context capacity, update TODO_[feature,release,hotfix]_*.md files with status then run /init

### Important Notes

- **All infrastructure examples** (databases, containers, CI/CD) are PSEUDO-CODE for you to adapt
- **Database migrations** are examples - adapt to user's actual database (or none)
- **Container orchestration** uses Podman with Containerfile (auto-generate if missing)
- **Test coverage** minimum 80% - features incomplete without passing tests
- **Daily developer workflow**: Each developer rebases their branch onto develop daily, then rebases feature branches onto contrib branch
- **Context management**: When context reaches 50% capacity, save progress to TODO file and run /init to reset

---

## Initial Setup: First Run Detection

When the user first submits this prompt to you:

### Step 0.1: Detect Project Tech Stack and Adapt Workflow

**CRITICAL: You must modify ALL code examples in workflow files to match the detected tech stack.**

```bash
# Detect tech stack and package manager
if [ -f package.json ]; then
  STACK="nodejs"
  PKG_MGR=$(jq -r '.packageManager // "npm"' package.json 2>/dev/null || echo "npm")
  PROJECT_NAME=$(jq -r '.name' package.json)
  TEST_CMD="npm test"
  BUILD_CMD="npm run build"
  INSTALL_CMD="npm install"
elif [ -f pyproject.toml ]; then
  STACK="python"
  PKG_MGR="uv"
  PROJECT_NAME=$(grep -m1 '^name = ' pyproject.toml | cut -d'"' -f2)
  TEST_CMD="uv run pytest"
  BUILD_CMD="uv run python setup.py build"
  INSTALL_CMD="uv sync"
else
  echo "ERROR: No package.json or pyproject.toml found"
  echo "This workflow requires a Node.js or Python project."
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Detect database (examples - adapt as needed)
if [ -f prisma/schema.prisma ]; then
  DATABASE="postgresql"
  ORM="prisma"
  MIGRATE_CMD="npx prisma migrate deploy"
  GENERATE_CMD="npx prisma generate"
elif [ -f alembic.ini ]; then
  DATABASE="postgresql"
  ORM="alembic"
  MIGRATE_CMD="uv run alembic upgrade head"
  GENERATE_CMD="# No generation needed for Alembic"
elif [ -f package.json ] && grep -q "mongoose" package.json; then
  DATABASE="mongodb"
  ORM="mongoose"
  MIGRATE_CMD="# No migrations for MongoDB"
  GENERATE_CMD="# No generation needed"
else
  DATABASE="none"
  ORM="none"
  MIGRATE_CMD="# No database"
  GENERATE_CMD="# No database"
fi

# Detect container setup
if [ -f Containerfile ]; then
  CONTAINER="exists"
elif [ -f Dockerfile ]; then
  CONTAINER="dockerfile_exists"
else
  CONTAINER="none"
fi

# Detect test framework
if [ "$STACK" = "nodejs" ]; then
  if grep -q "jest" package.json; then
    TEST_FRAMEWORK="jest"
    COVERAGE_CMD="npm test -- --coverage"
    COVERAGE_CHECK="npx nyc check-coverage --lines 80 --functions 80 --branches 80"
  elif grep -q "vitest" package.json; then
    TEST_FRAMEWORK="vitest"
    COVERAGE_CMD="npm test -- --coverage"
    COVERAGE_CHECK="# Check coverage in output"
  else
    TEST_FRAMEWORK="unknown"
    COVERAGE_CMD="npm test"
    COVERAGE_CHECK="# Configure coverage checking"
  fi
elif [ "$STACK" = "python" ]; then
  TEST_FRAMEWORK="pytest"
  COVERAGE_CMD="uv run pytest --cov"
  COVERAGE_CHECK="uv run pytest --cov --cov-report=term --cov-fail-under=80"
fi
```

**Prompt user:**
```
Detected project configuration:
  Stack: $STACK
  Package Manager: $PKG_MGR
  Project Name: $PROJECT_NAME
  Database: $DATABASE (ORM: $ORM)
  Container: $CONTAINER
  Test Framework: $TEST_FRAMEWORK
  Repository: $REPO_ROOT

Next step from WORKFLOW.md:
Step 0.1: Initialize workflow files

This will create/update:
- WORKFLOW.md (comprehensive workflow guide)
- CLAUDE.md (Claude Code interaction guide)
- README.md (project overview - will preserve existing content)
- TODO.md (manifest tracking active/completed features/releases/hotfixes)
- .github/workflows/ci-cd.yml (CI/CD pipeline adapted to your stack)
- Containerfile (if missing - using Podman)

**IMPORTANT: All code examples will be automatically adapted to your detected tech stack.**

Test command: $TEST_CMD
Build command: $BUILD_CMD
Install command: $INSTALL_CMD

Would you like to proceed with Step 0.1? (Y/n)
```

### Step 0.2: Create Workflow Files (Adapted to Tech Stack)

After user confirms "Y", create these files with **all code examples adapted**:

#### Directory Structure Standards

**CRITICAL:** Every directory in the project must follow these standards:

1. **Every directory** (including ARCHIVED) must contain:
   - `CLAUDE.md` - Context-specific guidance for Claude Code
   - `README.md` - Human-readable documentation

2. **Every directory** (except ARCHIVED directories themselves) must contain:
   - `ARCHIVED/` subdirectory with its own CLAUDE.md and README.md

3. **File deprecation process:**
   - When files become obsolete during a feature/release/hotfix
   - Zip deprecated files: `YYYYMMDDTHHMMSSZ_<description>.zip`
   - Timestamp matches the TODO_[feature,release,hotfix]_*.md that deprecated them
   - Store in ARCHIVED/ directory

**Example structure:**
```
specs/feature-auth/
├── CLAUDE.md           ← "Guide for working with auth specs"
├── README.md           ← "Authentication feature specifications"
├── ARCHIVED/
│   ├── CLAUDE.md       ← "Guide for archived auth specs"
│   ├── README.md       ← "Archive of deprecated auth specs"
│   └── 20251018T120000Z_old-oauth-flow.zip  ← Deprecated files
├── spec.md
└── plan.md
```

#### File: `WORKFLOW.md`

```markdown
# ${PROJECT_NAME} Workflow Guide

**Version:** 4.1.0  
**Tech Stack:** ${STACK}  
**Package Manager:** ${PKG_MGR}  
**Database:** ${DATABASE} (${ORM})  
**Container Runtime:** Podman  
**Test Framework:** ${TEST_FRAMEWORK}

This project uses a multi-branch git workflow orchestrated by Claude Code.

## Branch Structure

```
main                       ← Production releases (tagged vX.Y.Z)
  ↑
release/vX.Y.Z            ← Release candidates (staging)
  ↑
develop                    ← Integration branch (pre-release)
  ↑
contrib/<github-username>  ← Personal contribution branch (YOUR branch)
  ↑
feature/<timestamp>_<slug> ← Isolated feature development (git worktree)
hotfix/vX.Y.Z-hotfix.N    ← Production hotfixes (git worktree)
```

## Daily Developer Workflow

**Every day before starting work:**

1. Rebase your contrib branch onto develop:
   \`\`\`bash
   git checkout contrib/<your-username>
   git fetch origin
   git rebase origin/develop
   git push origin contrib/<your-username> --force-with-lease
   \`\`\`

2. Rebase any active feature branches onto your updated contrib branch:
   \`\`\`bash
   # In each feature worktree
   git fetch origin
   git rebase origin/contrib/<your-username>
   \`\`\`

**Why?** This prevents merge conflicts when creating PRs. The GitHub branch protection will **require** your contrib branch to be up-to-date with develop before allowing PR merge.

## Context Management

**Claude Code tracks context usage.** When context reaches **50% capacity**:

1. Claude Code automatically updates TODO_[feature,release,hotfix]_*.md with current status
2. Claude Code runs \`/init\` to reset context
3. Workflow continues from last saved state

You'll see:
\`\`\`
⚠️ Context at 50% capacity
✓ Saving progress to TODO_feature_*.md
✓ Running /init to reset context
✓ Resuming from Step X.Y...
\`\`\`

## Workflow Phases

### Phase 1: Feature Initialization (Main Repo)
**Location:** \`/path/to/repo\` on \`contrib/<username>\` branch  
**Tool:** BMAD Method (optional planning)

1. User asks Claude Code: "next step?"
2. Claude Code creates git worktree at \`/path/to/repo_feature_<timestamp>_<slug>\`
3. Claude Code initializes TODO_feature_*.md tracking file

### Phase 2: Feature Development (Worktree)
**Location:** \`/path/to/repo_feature_<timestamp>_<slug>\`  
**Tool:** SpecKit Method (specifications + implementation)

4. User opens Claude Code in worktree directory
5. Claude Code uses SpecKit to create detailed specifications
6. Claude Code generates implementation tasks
7. User asks "next step?" repeatedly as Claude Code implements each task
8. Claude Code updates TODO_feature_*.md with progress after each task
9. Claude Code enforces 80% test coverage before completion

### Phase 3: Multi-Branch Promotion
**Location:** Main repo + GitHub UI  
**Manual Steps:** PR merges via GitHub UI

10. **Feature → Contrib:** PR created, user merges manually, branches deleted
11. **Contrib → Develop:** PR created, user merges manually
12. **Develop → Release:** Claude Code calculates semver, creates release branch
13. **Release → Main:** PR created, user merges manually, tagged
14. **Release → Develop:** PR for bidirectional sync, user merges manually
15. **Release branch deleted** after both merges complete

### Phase 4: Cleanup

16. Archive TODO_feature_*.md to ARCHIVED/
17. Remove git worktree directory
18. Update TODO.md manifest

## Semantic Versioning Rules

Claude Code analyzes commits to determine version bump:

- **Major (vX.0.0):** Breaking changes
  - UI component renamed/removed
  - API endpoint path changed/removed  
  - Database schema breaking change
  - Public artifact structure changed
  
- **Minor (v1.X.0):** New features (backwards compatible)
  - New UI component added
  - New API endpoint added
  - New database table added
  - New artifact type introduced
  
- **Patch (v1.2.X):** Bug fixes (backwards compatible)
  - UI/API/artifact unchanged
  - Bug fixes, performance improvements
  - Documentation updates

## Quality Gates

Features must pass ALL gates before promotion:

✓ All tasks in TODO_feature_*.md complete  
✓ Tests exist and pass (\`${TEST_CMD}\`)  
✓ Test coverage ≥ 80% (\`${COVERAGE_CMD}\`)  
✓ Build succeeds (\`${BUILD_CMD}\`)  
✓ No merge conflicts

## References

- [TODO.md](./TODO.md) - Active and completed features/releases/hotfixes manifest (last 10 tracked)
- [CLAUDE.md](./CLAUDE.md) - How to interact with Claude Code
- [README.md](./README.md) - Project documentation

**Directory Structure:** Every directory contains CLAUDE.md, README.md, and ARCHIVED/ subdirectory (with its own documentation). Deprecated files are archived as YYYYMMDDTHHMMSSZ_<description>.zip in ARCHIVED/ directories.
```

#### File: `CLAUDE.md`

```markdown
# Claude Code Interaction Guide

## Starting a New Feature

1. Ensure you've done daily rebase (see WORKFLOW.md)
2. Navigate to repository root: \`cd /path/to/repo\`
3. Checkout your contrib branch: \`git checkout contrib/<username>\`
4. Open Claude Code and ask: **"next step?"**
5. Claude Code will prompt to create a worktree
6. Confirm with **"Y"**
7. Open NEW terminal: \`cd ../repo_feature_<timestamp>_<slug>\`
8. Open Claude Code in worktree and ask: **"next step?"**

## During Feature Development

Every time you want to proceed:
- Ask: **"next step?"**
- Claude Code shows: \`Next step from WORKFLOW.md: Step N.N <description>\`
- Review what will happen
- Confirm with **"Y"** to proceed or **"n"** to skip

## Status Tracking

Claude Code maintains status in \`TODO_[feature,release,hotfix]_<timestamp>_<slug>.md\`:

- **Section:** "## Workflow Progress" 
- **Updated:** After each completed step
- **Example:**
  \`\`\`yaml
  workflow_progress:
    phase: 2
    current_step: "2.5"
    last_task: "impl_003"
    last_update: "2025-10-18T15:30:00Z"
    status: "implementation"
    context_usage: "35%"
  \`\`\`

You can always check: \`cat TODO_feature_*.md | grep -A 6 "workflow_progress"\`

## Context Management

**Automatic context preservation at 50% capacity:**

When Claude Code's context reaches 50%, you'll see:
\`\`\`
⚠️ Context at 50% capacity
✓ Saving current progress to TODO_feature_*.md
✓ Running /init to reset context
✓ Context reset complete
→ Resuming from Step 2.5...
\`\`\`

This is automatic and seamless. Your workflow continues without interruption.

## Context-Aware Behavior

**In main repository (\`/path/to/repo\` on \`contrib/<username>\`):**
- Claude Code uses BMAD Method for planning
- Creates: PRD, architecture, epic documents (optional)
- Helps with high-level feature design

**In worktree (\`/path/to/repo_*\`):**
- Claude Code uses SpecKit Method
- Creates: specifications, implementation tasks, tests
- Implements feature/release/hotfix code iteratively

## After PR Creation

Claude Code creates PRs but **you must merge manually**:

1. Click the PR URL shown by Claude Code
2. Review changes in GitHub UI
3. Wait for CI/CD checks to pass
4. Click "Merge pull request"
5. Return to terminal
6. Ask Claude Code: **"next step?"**
7. Claude Code will clean up (delete branches, etc.)

## Merge Conflict Resolution

If rebase encounters conflicts, Claude Code will:

1. Show conflicted files
2. Analyze the conflict context using:
   - Feature specifications
   - Recent commit history
   - BMAD planning documents
3. Propose a resolution with reasoning
4. Ask for your confirmation

Example:
\`\`\`
Rebase conflict in src/api/auth.ts

Conflict: Both branches modified validateToken function

Analysis:
  - Current branch: Added rate limiting
  - Incoming branch: Added token refresh logic
  - Context: Both changes are necessary

Proposed Resolution: Merge both changes (rate limiting + refresh)

Apply this resolution? (Y/n)
\`\`\`

If Claude Code's resolution doesn't look right:
- Answer **"n"**
- Manually resolve: \`code src/api/auth.ts\`
- Continue: \`git rebase --continue\`

## Quality Gates

Before feature completion, Claude Code checks:

✓ **All tasks complete** - Every task in TODO_feature_*.md status='complete'  
✓ **Tests exist** - Test files created for all new functionality  
✓ **Tests pass** - \`${TEST_CMD}\` exits 0  
✓ **Coverage ≥ 80%** - \`${COVERAGE_CMD}\` meets minimum threshold  
✓ **Build succeeds** - \`${BUILD_CMD}\` completes successfully  

If any gate fails, Claude Code will:
- Stop the workflow
- Show which gate failed
- Recommend next actions
- Wait for you to fix issues

## Useful Commands

- **"next step?"** - Get next action from workflow
- **"show status"** - Display current TODO_[feature,release,hotfix]_*.md progress
- **"list active features"** - Show all active TODO files
- **"show conflicts"** - Display current merge conflicts (if any)

## Emergency: Aborting a Feature

If you need to abandon a feature:

\`\`\`bash
# In worktree directory
git checkout contrib/<username>
cd ..
git worktree remove repo_feature_<timestamp>_<slug>
rm -rf repo_feature_<timestamp>_<slug>

# In main repo
git branch -D feature/<timestamp>_<slug>
git push origin --delete feature/<timestamp>_<slug>

# Move TODO file to ARCHIVED
mv TODO_feature_*.md ARCHIVED/
git add ARCHIVED/ TODO.md
git commit -m "chore: abort feature <slug>"
\`\`\`

## Deprecating Files

When implementation replaces existing files, Claude Code will ask:

\`\`\`
This implementation deprecates existing files.
Files to be deprecated:
  - src/old-auth.ts
  - src/legacy-api.ts

Archive description (e.g., 'old-auth-flow'): 
\`\`\`

Enter a brief description. Files will be archived as:
\`YYYYMMDDTHHMMSSZ_<your-description>.zip\`

Example: \`20251018T120000Z_old-auth-flow.zip\`

The timestamp comes from the TODO file that deprecated them, ensuring traceability.

## Directory Standards

Every directory in this project follows these standards:

1. **Contains CLAUDE.md and README.md**
   - CLAUDE.md: Claude Code usage guide for that directory
   - README.md: Human-readable documentation

2. **Contains ARCHIVED/ subdirectory** (except ARCHIVED directories themselves)
   - For storing deprecated items from that directory
   - Also has its own CLAUDE.md and README.md

3. **Example structure:**
   \`\`\`
   specs/feature-auth/
   ├── CLAUDE.md
   ├── README.md
   ├── ARCHIVED/
   │   ├── CLAUDE.md
   │   ├── README.md
   │   └── 20251018T120000Z_v1-implementation.zip
   ├── spec.md
   └── plan.md
   \`\`\`
```

#### File: `README.md` (preserve existing + add workflow section)

```markdown
# ${PROJECT_NAME}

[EXISTING README CONTENT PRESERVED]

---

## Development Workflow

This project uses **SpecKit-BMAD v4.1** workflow orchestrated by Claude Code.

### Quick Start for New Features

1. Ensure you're on your \`contrib/<username>\` branch
2. Open Claude Code in repository root
3. Ask: **"next step?"**
4. Follow prompts to create worktree and develop feature

### Daily Workflow

Before starting work each day:

\`\`\`bash
# Update your contrib branch
git checkout contrib/<username>
git fetch origin
git rebase origin/develop
git push origin contrib/<username> --force-with-lease

# Update any active feature branches
cd ../repo_feature_*/
git rebase origin/contrib/<username>
\`\`\`

### Tech Stack

- **Language:** ${STACK}
- **Package Manager:** ${PKG_MGR}
- **Database:** ${DATABASE} (${ORM})
- **Test Framework:** ${TEST_FRAMEWORK}
- **Container:** Podman

### Documentation

- [WORKFLOW.md](./WORKFLOW.md) - Complete workflow guide
- [CLAUDE.md](./CLAUDE.md) - How to interact with Claude Code
- [TODO.md](./TODO.md) - Active and completed features

### Repository Structure

\`\`\`
/
├── WORKFLOW.md              ← Workflow documentation
├── CLAUDE.md                ← Claude Code interaction guide
├── TODO.md                  ← Features/releases/hotfixes manifest
├── TODO_feature_*.md        ← Active feature tracking
├── TODO_release_*.md        ← Active release tracking
├── TODO_hotfix_*.md         ← Active hotfix tracking
├── ARCHIVED/                ← Completed items
│   ├── CLAUDE.md            ← Claude Code guide for archived items
│   ├── README.md            ← Archive documentation
│   ├── TODO_feature_*.md
│   ├── TODO_release_*.md
│   ├── TODO_hotfix_*.md
│   └── YYYYMMDDTHHMMSSZ_<description>.zip  ← Deprecated files
├── docs/                    ← BMAD planning docs (optional)
│   ├── CLAUDE.md
│   ├── README.md
│   ├── ARCHIVED/
│   │   ├── CLAUDE.md
│   │   └── README.md
│   ├── prd_*.md
│   ├── architecture_*.md
│   └── epics_*.md
├── specs/                   ← SpecKit specifications
│   ├── CLAUDE.md
│   ├── README.md
│   ├── ARCHIVED/
│   │   ├── CLAUDE.md
│   │   └── README.md
│   └── feature-slug/
│       ├── CLAUDE.md
│       ├── README.md
│       ├── ARCHIVED/
│       │   ├── CLAUDE.md
│       │   └── README.md
│       └── spec.md
└── [your project files]
\`\`\`
```

#### File: `TODO.md`

```markdown
---
version: 4.1.0
active_features: []
active_releases: []
active_hotfixes: []
completed_features: []
completed_releases: []
completed_hotfixes: []
---

# ${PROJECT_NAME} TODO Manifest

This file tracks active and completed features, releases, and hotfixes. Managed by Claude Code via git operations.

## Active Features

(No active features)

## Active Releases

(No active releases)

## Active Hotfixes

(No active hotfixes)

## Recently Completed Features (Last 10)

(No completed features)

## Recently Completed Releases (Last 10)

(No completed releases)

## Recently Completed Hotfixes (Last 10)

(No completed hotfixes)

---

**Usage:**
- Claude Code updates this file automatically
- \`active_features/releases/hotfixes\`: List of TODO_*.md files currently in development
- \`completed_features/releases/hotfixes\`: Last 10 archived TODO files with completion dates
- Each directory contains CLAUDE.md and README.md for context
- Deprecated files are archived as YYYYMMDDTHHMMSSZ_<description>.zip in ARCHIVED/
```

#### File: `.github/workflows/ci-cd.yml` (Adapted to detected stack)

```yaml
name: CI/CD Pipeline

on:
  pull_request:
    branches: [main, develop, 'contrib/*', 'release/*', 'hotfix/*']
  push:
    branches: [main, develop]
    tags: ['v*', 'v*-hotfix.*']

jobs:
  test:
    runs-on: ubuntu-latest
    
    # Database service (adapt based on detected DATABASE)
    $([ "$DATABASE" = "postgresql" ] && cat <<'DBSERVICE'
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
DBSERVICE
    )
    $([ "$DATABASE" = "mongodb" ] && cat <<'DBSERVICE'
    services:
      mongodb:
        image: mongo:7
        ports:
          - 27017:27017
DBSERVICE
    )

    steps:
      - uses: actions/checkout@v4

      # Setup language runtime
      $([ "$STACK" = "nodejs" ] && cat <<'LANGSETUP'
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '${PKG_MGR}'
LANGSETUP
      )
      $([ "$STACK" = "python" ] && cat <<'LANGSETUP'
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
LANGSETUP
      )

      # Install dependencies
      - name: Install dependencies
        run: ${INSTALL_CMD}

      # Database migrations (if applicable)
      $([ "$DATABASE" != "none" ] && cat <<MIGRATIONS
      - name: Run database migrations
        env:
          DATABASE_URL: $([ "$DATABASE" = "postgresql" ] && echo "postgresql://postgres:postgres@localhost:5432/testdb" || echo "mongodb://localhost:27017/testdb")
        run: |
          ${MIGRATE_CMD}
          ${GENERATE_CMD}
MIGRATIONS
      )

      # Run tests
      - name: Run tests
        run: ${TEST_CMD}

      # Check test coverage (≥80%)
      - name: Check test coverage
        run: ${COVERAGE_CHECK}

      # Build
      - name: Build
        run: ${BUILD_CMD}

  container-build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/')

    steps:
      - uses: actions/checkout@v4

      - name: Setup Podman
        run: |
          sudo apt-get update
          sudo apt-get install -y podman

      - name: Login to GitHub Container Registry
        run: |
          echo "\${{ secrets.GITHUB_TOKEN }}" | podman login ghcr.io -u \${{ github.actor }} --password-stdin

      - name: Extract version
        id: version
        run: |
          if [[ "\${{ github.ref }}" == refs/tags/* ]]; then
            echo "version=\${GITHUB_REF#refs/tags/}" >> \$GITHUB_OUTPUT
          else
            echo "version=latest" >> \$GITHUB_OUTPUT
          fi

      - name: Build and push container
        run: |
          podman build -t ghcr.io/\${{ github.repository }}:\${{ steps.version.outputs.version }} .
          podman push ghcr.io/\${{ github.repository }}:\${{ steps.version.outputs.version }}
          
          # Also tag as latest if this is a release
          if [[ "\${{ github.ref }}" == refs/tags/* ]]; then
            podman tag ghcr.io/\${{ github.repository }}:\${{ steps.version.outputs.version }} ghcr.io/\${{ github.repository }}:latest
            podman push ghcr.io/\${{ github.repository }}:latest
          fi

  deploy:
    runs-on: ubuntu-latest
    needs: [test, container-build]
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        run: |
          # Add your deployment steps here
          # Example: kubectl, ssh, etc.
          echo "Deploying to production..."
```

#### File: `Containerfile` (Adapted to detected stack)

```dockerfile
# Containerfile for Podman
# Adapted to ${STACK}

$([ "$STACK" = "nodejs" ] && cat <<'NODECONTAINER'
FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN ${INSTALL_CMD}

# Copy application code
COPY . .

# Build
RUN ${BUILD_CMD}

# Expose port
EXPOSE 3000

# Start command
CMD ["npm", "start"]
NODECONTAINER
)

$([ "$STACK" = "python" ] && cat <<'PYCONTAINER'
FROM python:3.11-slim AS base

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Build (if needed)
RUN ${BUILD_CMD}

# Expose port
EXPOSE 8000

# Start command
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
PYCONTAINER
)
```

#### Directory: `ARCHIVED/` (Create with documentation)

```bash
# Create ARCHIVED directory structure
mkdir -p ARCHIVED

# Create ARCHIVED/CLAUDE.md
cat > ARCHIVED/CLAUDE.md <<'EOF'
# Claude Code Guide: ARCHIVED Directory

## Purpose

This directory contains completed and deprecated items:
- **TODO_feature_*.md** - Completed feature tracking files
- **TODO_release_*.md** - Completed release tracking files
- **TODO_hotfix_*.md** - Completed hotfix tracking files
- **YYYYMMDDTHHMMSSZ_<description>.zip** - Deprecated files from features/releases/hotfixes

## Deprecated Files

When files become obsolete during development:

1. **Identify deprecated files** during feature/release/hotfix work
2. **Create zip archive** with timestamp format:
   \`\`\`bash
   TIMESTAMP=\$(date -u +"%Y%m%dT%H%M%SZ")
   zip -r "ARCHIVED/\${TIMESTAMP}_\${DESCRIPTION}.zip" [files...]
   \`\`\`
3. **Remove original files** from active directories
4. **Update TODO file** to reference the archive

## Naming Convention

\`YYYYMMDDTHHMMSSZ_<description>.zip\`

- **YYYYMMDDTHHMMSSZ**: Timestamp from TODO file that deprecated the files
- **description**: Brief hyphen-separated description (e.g., "old-auth-flow")

## Examples

- \`20251018T120000Z_legacy-api-v1.zip\` - Old API version 1 files
- \`20251019T143000Z_unused-components.zip\` - Removed UI components
- \`20251020T091500Z_deprecated-migrations.zip\` - Old database migrations

## Claude Code Workflow

When working with archived items:

1. **Reference completed TODOs** for historical context
2. **Extract zip files** if need to review deprecated code
3. **Never modify** archived items directly
4. **Create new TODO** if need to revive deprecated functionality

## Searching Archives

Find archived work:
\`\`\`bash
# List all archived features
ls -1 ARCHIVED/TODO_feature_*.md

# Search in archived TODOs
grep -r "search term" ARCHIVED/TODO_*.md

# List deprecated file archives by date
ls -lt ARCHIVED/*.zip
\`\`\`
EOF

# Create ARCHIVED/README.md
cat > ARCHIVED/README.md <<'EOF'
# Archive Directory

## Overview

This directory contains completed work and deprecated files.

## Contents

### Completed Tracking Files

- **TODO_feature_*.md** - Completed features with full implementation history
- **TODO_release_*.md** - Completed releases with deployment records
- **TODO_hotfix_*.md** - Completed hotfixes with fix details

### Deprecated File Archives

Zip files containing obsolete code, configurations, or documentation:
- Format: \`YYYYMMDDTHHMMSSZ_<description>.zip\`
- Timestamp corresponds to the TODO file that deprecated them

## Reference Guide

### Finding Completed Work

View completed features by date:
\`\`\`bash
ls -lt TODO_feature_*.md | head -10
\`\`\`

Search for specific features:
\`\`\`bash
grep -l "authentication" TODO_feature_*.md
\`\`\`

### Extracting Deprecated Files

To review deprecated code:
\`\`\`bash
# Extract to temporary directory
unzip YYYYMMDDTHHMMSSZ_description.zip -d /tmp/review

# View contents without extracting
unzip -l YYYYMMDDTHHMMSSZ_description.zip
\`\`\`

### Retention Policy

- **TODO files**: Kept indefinitely (last 10 in main TODO.md manifest)
- **Deprecated archives**: Review quarterly, remove after 1 year if not needed

## Maintenance

This directory is managed automatically by Claude Code workflow.
Manual intervention should not be necessary.
EOF

# Create docs/ARCHIVED/ structure
mkdir -p docs/ARCHIVED
cat > docs/ARCHIVED/CLAUDE.md <<'EOF'
# Claude Code Guide: docs/ARCHIVED

## Purpose

Archived BMAD planning documents (PRD, architecture, epics) from completed or deprecated features.

## Working with Archived Docs

These documents provide historical context for past architectural decisions and requirements.

### Reference archived planning:
\`\`\`bash
# Find PRD for completed feature
ls -1 docs/ARCHIVED/prd_*.md

# Search architecture decisions
grep -r "database choice" docs/ARCHIVED/architecture_*.md
\`\`\`
EOF

cat > docs/ARCHIVED/README.md <<'EOF'
# Archived Planning Documents

This directory contains archived BMAD planning documents from completed features.

## Contents

- **prd_*.md** - Product Requirements Documents
- **architecture_*.md** - Architecture design documents  
- **epics_*.md** - Epic breakdown documents

These documents are preserved for historical reference and future architectural decisions.
EOF

# Create specs/ARCHIVED/ structure
mkdir -p specs/ARCHIVED
cat > specs/ARCHIVED/CLAUDE.md <<'EOF'
# Claude Code Guide: specs/ARCHIVED

## Purpose

Archived SpecKit specifications from completed features, releases, and hotfixes.

## Working with Archived Specs

Reference these specifications to understand implementation details of past work.

### Find archived specs:
\`\`\`bash
# List all archived feature specs
ls -1d specs/ARCHIVED/feature-*

# Search in archived plans
find specs/ARCHIVED -name "plan.md" -exec grep -l "authentication" {} \;
\`\`\`
EOF

cat > specs/ARCHIVED/README.md <<'EOF'
# Archived Specifications

This directory contains SpecKit specifications from completed work.

## Structure

Each archived feature/release/hotfix has a subdirectory containing:
- spec.md - Feature specification
- plan.md - Implementation plan
- data-model.md - Database schema (if applicable)
- api-contracts.md - API documentation (if applicable)

These specifications document what was built and how it was implemented.
EOF
```

#### Helper Function: Create Directory Structure

Add this helper function that Claude Code should use when creating new directories:

```bash
create_directory_structure() {
    local DIR_PATH="$1"
    local DIR_PURPOSE="$2"
    
    # Create directory
    mkdir -p "$DIR_PATH"
    
    # Create CLAUDE.md
    cat > "$DIR_PATH/CLAUDE.md" <<EOF
# Claude Code Guide: $(basename $DIR_PATH)

## Purpose

${DIR_PURPOSE}

## Working in this directory

[Claude Code will update this with specific guidance]

## References

- [Main workflow](../WORKFLOW.md)
- [Claude Code guide](../CLAUDE.md)
EOF
    
    # Create README.md
    cat > "$DIR_PATH/README.md" <<EOF
# $(basename $DIR_PATH)

${DIR_PURPOSE}

[Human-readable documentation will be added here]
EOF
    
    # Create ARCHIVED subdirectory (unless this IS an archived directory)
    if [[ "$DIR_PATH" != *"/ARCHIVED"* ]] && [[ "$DIR_PATH" != *"/ARCHIVED" ]]; then
        mkdir -p "$DIR_PATH/ARCHIVED"
        
        cat > "$DIR_PATH/ARCHIVED/CLAUDE.md" <<EOF
# Claude Code Guide: $(basename $DIR_PATH)/ARCHIVED

Archived items from $(basename $DIR_PATH).

Reference these files for historical context.
EOF
        
        cat > "$DIR_PATH/ARCHIVED/README.md" <<EOF
# Archived Items

This directory contains archived items from $(basename $DIR_PATH).
EOF
    fi
    
    echo "✓ Created directory structure: $DIR_PATH"
}
```

#### Helper Function: Deprecate Files

Add this helper function for deprecating files:

```bash
deprecate_files() {
    local TODO_FILE="$1"
    local DESCRIPTION="$2"
    shift 2
    local FILES=("$@")
    
    # Extract timestamp from TODO filename
    # Format: TODO_[type]_YYYYMMDDTHHMMSSZ_slug.md
    if [[ "$TODO_FILE" =~ TODO_[^_]+_([0-9]{8}T[0-9]{6}Z)_ ]]; then
        TIMESTAMP="${BASH_REMATCH[1]}"
    else
        TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
    fi
    
    # Create zip archive
    ARCHIVE_NAME="${TIMESTAMP}_${DESCRIPTION}.zip"
    
    echo "Deprecating files to ARCHIVED/${ARCHIVE_NAME}:"
    for file in "${FILES[@]}"; do
        echo "  - $file"
    done
    
    # Create zip
    zip -r "ARCHIVED/${ARCHIVE_NAME}" "${FILES[@]}"
    
    # Remove original files
    rm -rf "${FILES[@]}"
    
    # Update TODO file to reference the archive
    echo "- ${TIMESTAMP}: Deprecated files archived to ${ARCHIVE_NAME}" >> "$TODO_FILE"
    
    echo "✓ Files deprecated and archived"
}
```

**Prompt user:**
```
✓ Created workflow files (all adapted to ${STACK}):
  - WORKFLOW.md (adapted commands)
  - CLAUDE.md (interaction guide)
  - README.md (tech stack documented)
  - TODO.md (features/releases/hotfixes manifest - last 10 tracked)
  - .github/workflows/ci-cd.yml (CI/CD adapted to ${STACK})
  - Containerfile (Podman config for ${STACK})

✓ Created directory structure with documentation:
  - ARCHIVED/ (with CLAUDE.md and README.md)
  - docs/ and docs/ARCHIVED/ (with documentation)
  - specs/ and specs/ARCHIVED/ (with documentation)

✓ Directory standards implemented:
  - Every directory has CLAUDE.md and README.md
  - Every directory (except ARCHIVED) has ARCHIVED/ subdirectory
  - Deprecated files will be stored as YYYYMMDDTHHMMSSZ_<description>.zip

All code examples use:
  - Install: ${INSTALL_CMD}
  - Test: ${TEST_CMD}
  - Build: ${BUILD_CMD}
  - Coverage: ${COVERAGE_CMD}

Next step from WORKFLOW.md:
Step 0.2: Commit initial workflow files

Would you like to proceed with Step 0.2? (Y/n)
```

### Step 0.3: Commit Workflow Files

```bash
# Create initial directory structure with documentation
create_directory_structure "ARCHIVED" "Archive for completed TODO files and deprecated code"
create_directory_structure "docs" "BMAD planning documents (PRD, architecture, epics)"
create_directory_structure "specs" "SpecKit specifications for features/releases/hotfixes"

git add WORKFLOW.md CLAUDE.md README.md TODO.md .github/ Containerfile
git add ARCHIVED/ docs/ specs/
git commit -m "chore: initialize SpecKit-BMAD workflow v4.1

- Add workflow documentation
- Add CI/CD with 80% test coverage requirement
- Add Containerfile for Podman
- Create directory structure with CLAUDE.md and README.md
- Setup ARCHIVED directories for deprecation tracking
- All examples adapted to ${STACK} stack

Tech stack:
  - Language: ${STACK}
  - Package Manager: ${PKG_MGR}
  - Database: ${DATABASE} (${ORM})
  - Test Framework: ${TEST_FRAMEWORK}

Directory standards:
  - Every directory has CLAUDE.md and README.md
  - Every directory (except ARCHIVED) has ARCHIVED/ subdirectory
  - Deprecated files stored as YYYYMMDDTHHMMSSZ_<description>.zip"
git push origin "$(git branch --show-current)"
```

**Prompt user:**
```
✓ Workflow files committed and pushed

Setup complete! You're ready to start features.

Next step from WORKFLOW.md:
Step 1.1: Ensure you're on your contrib/<username> branch

Would you like to proceed with Step 1.1? (Y/n)
```

---

## Phase 1: Feature Initialization (Main Repository)

**Context Detection:** User is in `/path/to/repo` on `contrib/<github-username>` branch

### Step 1.1: Verify and Sync Branch

```bash
CURRENT_BRANCH=$(git branch --show-current)
GITHUB_USER=$(git config user.name | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
EXPECTED_BRANCH="contrib/${GITHUB_USER}"

if [ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]; then
  echo "WARNING: You are on branch: $CURRENT_BRANCH"
  echo "Expected branch: $EXPECTED_BRANCH"
  echo ""
  
  # Check if contrib branch exists
  if git show-ref --verify --quiet "refs/heads/$EXPECTED_BRANCH"; then
    echo "Contrib branch exists. Checkout? (Y/n)"
  else
    echo "Create contrib branch from develop? (Y/n)"
  fi
  
  # Wait for confirmation, then checkout or create
fi

# Perform daily sync
echo "Performing daily rebase onto develop..."
git fetch origin
git rebase origin/develop

if [ $? -ne 0 ]; then
  echo ""
  echo "Rebase conflict detected during daily sync."
  echo "This is unexpected - contrib branches should stay in sync."
  echo ""
  # Use AI-assisted conflict resolution
  resolve_conflicts_with_reasoning
fi

git push origin "$EXPECTED_BRANCH" --force-with-lease
```

**Prompt user:**
```
✓ Verified branch: contrib/<username>
✓ Rebased onto latest develop
✓ Pushed updated branch

Next step from WORKFLOW.md:
Step 1.2: BMAD Planning (Optional)

Would you like to create planning documents using BMAD Method?

BMAD Method helps with:
- Product Requirements Document (PRD)
- System Architecture Design
- Epic Breakdown

This is recommended for:
- Complex features with unclear requirements
- Features requiring architectural decisions
- Features that impact multiple systems

Skip if you have clear, simple requirements.

Would you like to proceed with Step 1.2? (Y/n)
```

### Step 1.2: BMAD Planning (Optional)

If user confirms "Y":

```markdown
I'll guide you through BMAD planning using three agent personas:

---

### 🧠 BMAD Analyst: Product Requirements

Let's create a Product Requirements Document (PRD).

**Feature Name:** [Ask user for feature name]

**Problem Statement:**  
What problem does this feature solve?  
[Interactive Q&A with user]

**Target Users:**  
Who will use this feature?  
[Interactive Q&A]

**User Stories:**  
Based on your answers, here are the user stories:

1. As a [user type], I want to [action] so that [benefit]
2. As a [user type], I want to [action] so that [benefit]
3. [Additional stories...]

**Acceptance Criteria:**  
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Out of Scope:**  
- [What we're NOT building]

**Success Metrics:**  
- [How we measure success]

[Generate complete PRD]

Saving to: docs/prd_<feature-slug>.md

---

### 🏗️ BMAD Architect: Technical Design

Based on the PRD, I'll design the technical architecture.

**Tech Stack:** ${STACK}, ${DATABASE}, ${ORM}

**Component Design:**

1. **Data Layer**
   - Models: [List data models]
   - Schema changes: [Database changes needed]
   - Migrations: [Migration steps]

2. **API Layer** (if applicable)
   - Endpoints: [List new/modified endpoints]
   - Authentication: [Auth requirements]
   - Validation: [Input validation rules]

3. **UI Layer** (if applicable)
   - Components: [List UI components]
   - State management: [How state is handled]
   - Routing: [New routes needed]

4. **Integration Points**
   - External services: [APIs, services]
   - Internal dependencies: [Other modules]

**Non-Functional Requirements:**
- Performance targets
- Security considerations
- Scalability needs
- Monitoring/observability

[Generate complete architecture document]

Saving to: docs/architecture_<feature-slug>.md

---

### 📋 BMAD PM: Epic Breakdown

I'll break down the feature into implementable epics.

**Epic 1: [Name]**
- Scope: [What's included]
- Estimated complexity: [Low/Medium/High]
- Dependencies: [Prerequisites]
- Deliverables: [What gets built]

**Epic 2: [Name]**
- Scope: [What's included]
- Estimated complexity: [Low/Medium/High]
- Dependencies: [Prerequisites]
- Deliverables: [What gets built]

**Epic 3: [Name]**
- [Continue pattern...]

**Implementation Order:**
1. Epic [N] - [Reason for priority]
2. Epic [N] - [Reason for priority]
3. Epic [N] - [Reason for priority]

[Generate complete epic breakdown]

Saving to: docs/epics_<feature-slug>.md

---

[Create all three documents]
```

```bash
# Create docs directory if needed
mkdir -p docs

# Save planning documents
cat > "docs/prd_${FEATURE_SLUG}.md" <<EOF
[Generated PRD content]
EOF

cat > "docs/architecture_${FEATURE_SLUG}.md" <<EOF
[Generated architecture content]
EOF

cat > "docs/epics_${FEATURE_SLUG}.md" <<EOF
[Generated epics content]
EOF

git add docs/
git commit -m "docs: add BMAD planning for ${FEATURE_SLUG}"
git push origin "${EXPECTED_BRANCH}"
```

**Prompt user:**
```
✓ BMAD planning documents created:
  - docs/prd_<slug>.md
  - docs/architecture_<slug>.md
  - docs/epics_<slug>.md

These documents will provide context for the SpecKit specifications.

Next step from WORKFLOW.md:
Step 1.3: Create git worktree for feature development

Feature description (3-5 words): 
```

### Step 1.3: Create Git Worktree

```bash
# Get feature description from user
read -p "Feature description (3-5 words): " DESCRIPTION

# Validate input (alphanumeric, spaces, hyphens, underscores only)
if ! [[ "$DESCRIPTION" =~ ^[a-zA-Z0-9\ _-]+$ ]]; then
  echo "ERROR: Description contains invalid characters"
  echo "Allowed: letters, numbers, spaces, hyphens, underscores"
  exit 1
fi

# Generate identifiers
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
FEATURE_SLUG=$(echo "$DESCRIPTION" | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/[^a-z0-9 ]//g' | \
  awk '{print $1"-"$2"-"$3}' | \
  sed 's/-$//' | sed 's/^-//')

if [ -z "$FEATURE_SLUG" ]; then
  echo "ERROR: Could not generate valid feature slug from description"
  exit 1
fi

FEATURE_ID="${TIMESTAMP}_${FEATURE_SLUG}"
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_PATH="${REPO_ROOT}_feature_${FEATURE_ID}"
FEATURE_BRANCH="feature/${FEATURE_ID}"
BASE_BRANCH="contrib/${GITHUB_USER}"

echo ""
echo "Creating feature worktree:"
echo "  Feature ID: ${FEATURE_ID}"
echo "  Branch: ${FEATURE_BRANCH}"
echo "  Path: ${WORKTREE_PATH}"
echo "  Base: ${BASE_BRANCH}"
echo ""

# Create feature branch from contrib branch
git branch "$FEATURE_BRANCH" "$BASE_BRANCH"

# Create worktree
git worktree add "$WORKTREE_PATH" "$FEATURE_BRANCH"
```

**Prompt user:**
```
✓ Git worktree created

Branch: feature/<timestamp>_<slug>
Path: <worktree-path>

Next step from WORKFLOW.md:
Step 1.4: Initialize feature tracking

This will:
1. Create TODO_feature_<id>.md in main repo
2. Update TODO.md manifest
3. Initialize SpecKit in worktree

Would you like to proceed with Step 1.4? (Y/n)
```

### Step 1.4: Initialize Feature Tracking

```bash
# Create TODO file at main repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
TODO_FILE="${REPO_ROOT}/TODO_feature_${FEATURE_ID}.md"

cat > "$TODO_FILE" <<EOF
---
feature_id: ${FEATURE_ID}
timestamp: ${TIMESTAMP}
feature_slug: ${FEATURE_SLUG}
feature_description: "${DESCRIPTION}"
branch: ${FEATURE_BRANCH}
worktree_path: ${WORKTREE_PATH}
status: initialization
created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
version: 4.1.0
tech_stack:
  language: ${STACK}
  package_manager: ${PKG_MGR}
  database: ${DATABASE}
  orm: ${ORM}
  test_framework: ${TEST_FRAMEWORK}
---

# Feature: ${FEATURE_SLUG}

**Feature ID:** ${FEATURE_ID}  
**Description:** ${DESCRIPTION}  
**Status:** Initialization

---

## Workflow Progress

\`\`\`yaml
workflow_progress:
  phase: 1
  current_step: "1.4"
  last_task: "initialization"
  last_update: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  status: "initialization"
  context_usage: "5%"
\`\`\`

---

## Phase 1: SpecKit Specification

### Batch 1.1: Feature Specification

#### speckit_spec_001
- **task**: Create detailed feature specification
- **files**: [specs/${FEATURE_SLUG}/spec.md]
- **status**: pending
- **prompt**: |
    Use SpecKit /specify command to create detailed specification.
    
    Include:
    - User stories with acceptance criteria
    - Functional requirements (what the feature does)
    - Non-functional requirements (performance, security, usability)
    - Edge cases and error handling scenarios
    - UI/UX considerations (if applicable)
    
    $([ -f ${REPO_ROOT}/docs/prd_${FEATURE_SLUG}.md ] && echo "Context: See PRD at docs/prd_${FEATURE_SLUG}.md" || echo "Context: No BMAD planning documents available")
    
    Tech Stack: ${STACK}, ${DATABASE}, ${ORM}
    
    On completion: Update status to 'complete'

#### speckit_plan_001
- **task**: Create technical implementation plan
- **files**: [specs/${FEATURE_SLUG}/plan.md, specs/${FEATURE_SLUG}/data-model.md]
- **status**: pending
- **prompt**: |
    Use SpecKit /plan command to create implementation plan.
    
    Include:
    - Component architecture and module boundaries
    - Data models and database schema (if applicable)
    - API endpoints and contracts (if applicable)
    - External integrations and dependencies
    - Testing strategy (unit, integration, e2e)
    - Deployment considerations
    
    $([ -f ${REPO_ROOT}/docs/architecture_${FEATURE_SLUG}.md ] && echo "Context: See architecture at docs/architecture_${FEATURE_SLUG}.md" || echo "Context: Design the architecture as needed")
    
    Tech Stack: ${STACK}, ${DATABASE}, ${ORM}
    Commands:
      - Install: ${INSTALL_CMD}
      - Test: ${TEST_CMD}
      - Build: ${BUILD_CMD}
    
    On completion: Update status to 'complete'

---

## Phase 2: Implementation

### Batch 2.1: Core Development

(Tasks will be generated after specifications are complete)

---

## Phase 3: Testing

### Batch 3.1: Unit Tests

(Tasks will be generated after implementation)

### Batch 3.2: Integration Tests

(Tasks will be generated after unit tests)

---

## Quality Gates

- [ ] All specification tasks complete
- [ ] All implementation tasks complete
- [ ] All test tasks complete
- [ ] Tests pass: \`${TEST_CMD}\`
- [ ] Coverage ≥ 80%: \`${COVERAGE_CHECK}\`
- [ ] Build succeeds: \`${BUILD_CMD}\`
- [ ] No merge conflicts with contrib branch

---

## Status History

- $(date -u +"%Y-%m-%dT%H:%M:%SZ"): Feature initialized
EOF

# Update main repo TODO.md manifest
cd "$REPO_ROOT"

python3 <<PYSCRIPT
import re
from pathlib import Path
from datetime import datetime

todo_path = Path("TODO.md")
content = todo_path.read_text()

yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
if not yaml_match:
    print("ERROR: Invalid TODO.md format")
    exit(1)

yaml_content = yaml_match.group(1)
body = yaml_match.group(2)

# Add to active_features list in YAML frontmatter
if "active_features: []" in yaml_content:
    yaml_content = yaml_content.replace(
        "active_features: []",
        f"active_features:\n  - TODO_feature_${FEATURE_ID}.md"
    )
else:
    # Append to existing list
    yaml_content = re.sub(
        r'(active_features:)',
        rf'\1\n  - TODO_feature_${FEATURE_ID}.md',
        yaml_content
    )

# Add to active features section in body
if "(No active features)" in body:
    body = body.replace(
        "(No active features)",
        f"- [{FEATURE_SLUG}](TODO_feature_${FEATURE_ID}.md) - Started {datetime.utcnow().strftime('%Y-%m-%d')}"
    )
else:
    body = re.sub(
        r'(## Active Features\n\n)',
        rf'\1- [{FEATURE_SLUG}](TODO_feature_${FEATURE_ID}.md) - Started {datetime.utcnow().strftime("%Y-%m-%d")}\n',
        body
    )

todo_path.write_text(f"---\n{yaml_content}\n---\n{body}")
PYSCRIPT

# Commit in main repo
git add TODO.md "TODO_feature_${FEATURE_ID}.md"
git commit -m "feat: initialize ${FEATURE_ID}"
git push origin "${BASE_BRANCH}"

# Initialize SpecKit in worktree
cd "$WORKTREE_PATH"
specify init --here --ai claude --force --no-git

# Push feature branch
git push origin "${FEATURE_BRANCH}"
```

**Prompt user:**
```
✓ Feature tracking initialized
✓ TODO_feature_<id>.md created with adapted tech stack
✓ TODO.md manifest updated
✓ SpecKit initialized in worktree
✓ Feature branch pushed

**IMPORTANT: Open NEW terminal window**

Run these commands:
  cd <worktree-path>
  # Open Claude Code here

Then ask Claude Code: "next step?"

This terminal session is complete for Phase 1.
Context will continue in the worktree.
```

---

## Phase 2: Feature Development (Worktree)

**Context Detection:** User is in `/path/to/repo_*` directory

### Context Capacity Monitoring

**CRITICAL:** Claude Code must monitor context usage throughout Phase 2.

```python
def check_context_capacity():
    """
    Monitor context usage and save state when reaching 50%.
    """
    current_usage = get_context_usage_percentage()
    
    if current_usage >= 50:
        print("⚠️ Context at 50% capacity")
        print("✓ Saving current progress to TODO file...")
        
        # Update TODO file with current state
        update_todo_file_status()
        
        print("✓ Running /init to reset context...")
        run_init_command()
        
        print("✓ Context reset complete")
        print(f"→ Resuming from Step {current_step}...")
        
        # Resume workflow from saved state
        return True
    
    return False


def update_todo_file_status():
    """
    Save current workflow state to TODO file before context reset.
    """
    # Read current TODO file
    todo_path = Path(TODO_FILE)
    content = todo_path.read_text()
    
    # Update workflow_progress section
    current_time = datetime.utcnow().isoformat() + 'Z'
    context_usage = get_context_usage_percentage()
    
    new_progress = f'''workflow_progress:
  phase: {current_phase}
  current_step: "{current_step}"
  last_task: "{last_completed_task}"
  last_update: "{current_time}"
  status: "{current_status}"
  context_usage: "{context_usage}%"
  context_reset_count: {context_reset_count + 1}
'''
    
    content = re.sub(
        r'workflow_progress:.*?(?=```)',
        new_progress,
        content,
        flags=re.DOTALL
    )
    
    # Add to status history
    content = re.sub(
        r'(## Status History)',
        rf'\1\n- {current_time}: Context reset at {context_usage}% (Step {current_step})',
        content
    )
    
    todo_path.write_text(content)
    
    # Commit the update
    run(f'cd {MAIN_REPO}')
    run(f'git add TODO_feature_{FEATURE_ID}.md')
    run(f'git commit -m "chore: save workflow state before context reset (Step {current_step})"')
    run(f'git push origin contrib/{GITHUB_USER}')
```

### Step 2.1: Verify Worktree Context

```bash
# Check context capacity BEFORE starting
check_context_capacity

CURRENT_DIR=$(pwd)
CURRENT_BRANCH=$(git branch --show-current)

# Extract feature ID from directory path (works for feature/release/hotfix)
if [[ "$CURRENT_DIR" =~ _feature_([0-9]{8}T[0-9]{6}Z)_(.+)$ ]]; then
  TYPE="feature"
  TIMESTAMP="${BASH_REMATCH[1]}"
  SLUG="${BASH_REMATCH[2]}"
  ID="${TIMESTAMP}_${SLUG}"
elif [[ "$CURRENT_DIR" =~ _release_([0-9]{8}T[0-9]{6}Z)_(.+)$ ]]; then
  TYPE="release"
  TIMESTAMP="${BASH_REMATCH[1]}"
  SLUG="${BASH_REMATCH[2]}"
  ID="${TIMESTAMP}_${SLUG}"
elif [[ "$CURRENT_DIR" =~ _hotfix_([0-9]{8}T[0-9]{6}Z)_(.+)$ ]]; then
  TYPE="hotfix"
  TIMESTAMP="${BASH_REMATCH[1]}"
  SLUG="${BASH_REMATCH[2]}"
  ID="${TIMESTAMP}_${SLUG}"
else
  echo "ERROR: Not in a worktree directory"
  echo "Expected pattern: /path/to/repo_[feature|release|hotfix]_<timestamp>_<slug>"
  echo "Current directory: $CURRENT_DIR"
  exit 1
fi

# Verify branch matches
EXPECTED_BRANCH="${TYPE}/${ID}"
if [ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]; then
  echo "ERROR: Branch mismatch"
  echo "Expected: $EXPECTED_BRANCH"
  echo "Current: $CURRENT_BRANCH"
  exit 1
fi

# Locate TODO file in main repo
REPO_ROOT=$(git rev-parse --show-toplevel)
MAIN_REPO="${REPO_ROOT%_${TYPE}_*}"
TODO_FILE="${MAIN_REPO}/TODO_${TYPE}_${ID}.md"

if [ ! -f "$TODO_FILE" ]; then
  echo "ERROR: TODO file not found: $TODO_FILE"
  exit 1
fi
```

**Prompt user:**
```
✓ Verified worktree context

Type: <type>
ID: <timestamp>_<slug>
Branch: <type>/<timestamp>_<slug>
TODO File: ../TODO_<type>_<id>.md

Next step from WORKFLOW.md:
Step 2.2: Create specifications using SpecKit

I'll guide you through creating detailed specifications.

Would you like to proceed with Step 2.2? (Y/n)
```

### Step 2.2: SpecKit Specification

```markdown
# Check context capacity before specification
check_context_capacity

I'll help create detailed specifications using SpecKit.

---

### 📝 SpecKit /specify: Feature Specification

Let's create a comprehensive specification document.

$([ -f ${MAIN_REPO}/docs/prd_${SLUG}.md ] && echo "I'll use the BMAD PRD as context: docs/prd_${SLUG}.md" || echo "I'll gather requirements interactively.")

**User Stories:**

Based on $([ -f ${MAIN_REPO}/docs/prd_${SLUG}.md ] && echo "the PRD" || echo "your description"), here are the user stories:

1. As a [user type], I want to [action] so that [benefit]
   - Acceptance Criteria:
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]
     - [ ] [Criterion 3]

2. As a [user type], I want to [action] so that [benefit]
   - Acceptance Criteria:
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]

[Continue for all stories...]

**Functional Requirements:**

1. **[Component 1]**
   - Description: [What it does]
   - Inputs: [What it receives]
   - Outputs: [What it produces]
   - Business Rules: [Constraints and logic]

2. **[Component 2]**
   - [Continue pattern...]

**Non-Functional Requirements:**

- **Performance:**
  - Response time: [Target]
  - Throughput: [Target]
  - Resource usage: [Limits]

- **Security:**
  - Authentication: [Requirements]
  - Authorization: [Rules]
  - Data protection: [Measures]

- **Usability:**
  - Accessibility: [Standards]
  - User experience: [Goals]

**Edge Cases:**

1. [Edge case 1]: [How to handle]
2. [Edge case 2]: [How to handle]
3. [Edge case 3]: [How to handle]

**Error Handling:**

| Error Scenario | Expected Behavior | User Message |
|----------------|-------------------|--------------|
| [Scenario 1] | [Behavior] | [Message] |
| [Scenario 2] | [Behavior] | [Message] |

[Generate complete specification]

Saving to: specs/${SLUG}/spec.md

---

# Check context capacity before plan
check_context_capacity

### 🏗️ SpecKit /plan: Implementation Plan

Now I'll create the technical implementation plan.

$([ -f ${MAIN_REPO}/docs/architecture_${SLUG}.md ] && echo "Using BMAD architecture document as foundation." || echo "Designing architecture from requirements.")

**1. Component Architecture**

\`\`\`
[Component Diagram or Description]

Module A (UI Layer)
  ├─ Component 1
  ├─ Component 2
  └─ Component 3

Module B (API Layer)
  ├─ Endpoint 1: POST /api/resource
  ├─ Endpoint 2: GET /api/resource/:id
  └─ Endpoint 3: PUT /api/resource/:id

Module C (Data Layer)
  ├─ Model 1
  └─ Model 2
\`\`\`

**2. Data Model**

$([ "$DATABASE" != "none" ] && echo "Database: ${DATABASE}, ORM: ${ORM}" || echo "No database required")

[Generate data model in appropriate format for ${ORM}]

**3. API Contracts**

[Generate API contracts in appropriate format for ${STACK}]

**4. Integration Points**

- External Services: [List APIs, webhooks, etc.]
- Internal Dependencies: [Other modules, services]
- Data Sources: [Databases, caches, etc.]

**5. Testing Strategy**

- **Unit Tests:**
  - Test all business logic functions
  - Test data model methods
  - Test utility functions
  - Target: ≥80% coverage
  - Command: ${TEST_CMD}

- **Integration Tests:**
  - Test API endpoints
  - Test database operations
  - Test external service integrations

- **E2E Tests (if applicable):**
  - Test critical user flows
  - Test error scenarios

**6. Implementation Steps**

1. Database schema and migrations (if applicable)
   - Command: ${MIGRATE_CMD}
2. Data models and ORM entities
3. Business logic functions
4. API endpoints (if applicable)
5. UI components (if applicable)
6. Integration with external services
7. Unit tests
8. Integration tests
9. Documentation

[Generate complete implementation plan]

Saving to:
  - specs/${SLUG}/plan.md
  - specs/${SLUG}/data-model.md (if database changes)
  - specs/${SLUG}/api-contracts.md (if API changes)
```

```bash
# Check context capacity
check_context_capacity

# Create specs directory with proper structure
create_directory_structure "specs/${SLUG}" "SpecKit specifications for ${SLUG}"

# Save specification
cat > "specs/${SLUG}/spec.md" <<EOF
[Generated specification content]
EOF

# Save implementation plan
cat > "specs/${SLUG}/plan.md" <<EOF
[Generated plan content adapted to ${STACK}]
EOF

# Save data model (if applicable)
if [ "$DATABASE" != "none" ]; then
  cat > "specs/${SLUG}/data-model.md" <<EOF
[Generated data model for ${ORM}]
EOF
fi

# Update directory CLAUDE.md with specific context
cat > "specs/${SLUG}/CLAUDE.md" <<EOF
# Claude Code Guide: specs/${SLUG}

## Purpose

SpecKit specifications for ${SLUG} feature.

## Contents

- **spec.md** - Feature specification with user stories and requirements
- **plan.md** - Technical implementation plan
- **data-model.md** - Database schema (${DATABASE} with ${ORM})

## Working with these specs

Reference these documents when:
- Implementing tasks from TODO_${TYPE}_${ID}.md
- Resolving implementation questions
- Understanding feature requirements
- Reviewing architecture decisions

## Tech Stack

- Language: ${STACK}
- Package Manager: ${PKG_MGR}
- Database: ${DATABASE} (${ORM})
- Test Framework: ${TEST_FRAMEWORK}
EOF

# Commit specifications
git add specs/
git commit -m "docs(${SLUG}): add SpecKit specifications"
git push origin "${CURRENT_BRANCH}"

# Update TODO file with progress
python3 <<PYSCRIPT
import re
from pathlib import Path
from datetime import datetime

todo_path = Path("${TODO_FILE}")
content = todo_path.read_text()

# Mark specification tasks as complete
content = re.sub(
    r'(#### speckit_spec_001.*?status: )pending',
    r'\1complete',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(#### speckit_plan_001.*?status: )pending',
    r'\1complete',
    content,
    flags=re.DOTALL
)

# Update workflow progress
context_usage = get_context_usage_percentage()
content = re.sub(
    r'workflow_progress:.*?(?=\`\`\`)',
    f'''workflow_progress:
  phase: 2
  current_step: "2.2"
  last_task: "speckit_plan_001"
  last_update: "{datetime.utcnow().isoformat()}Z"
  status: "specification_complete"
  context_usage: "{context_usage}%"
''',
    content,
    flags=re.DOTALL
)

# Update overall status
content = re.sub(r'status: initialization', 'status: specification_complete', content)

# Add status history entry
timestamp = datetime.utcnow().isoformat() + 'Z'
content = re.sub(
    r'(## Status History)',
    rf'\1\n- {timestamp}: Specifications completed (spec + plan)',
    content
)

todo_path.write_text(content)
PYSCRIPT

# Commit TODO update in main repo
cd "${MAIN_REPO}"
git add "TODO_${TYPE}_${ID}.md"
git commit -m "docs(${SLUG}): specifications complete"
git push origin "contrib/${GITHUB_USER}"

cd "${CURRENT_DIR}"

# Check context capacity after specification
check_context_capacity
```

**Prompt user:**
```
✓ Specifications complete:
  - specs/<slug>/spec.md (user stories, requirements, edge cases)
  - specs/<slug>/plan.md (architecture, implementation steps)
  - specs/<slug>/data-model.md (database schema for ${ORM})
✓ TODO file updated (tasks marked complete)

Context usage: <percentage>%

Next step from WORKFLOW.md:
Step 2.3: Generate implementation tasks from specifications

I'll analyze the specs and create detailed implementation tasks.

Would you like to proceed with Step 2.3? (Y/n)
```

### Step 2.3: Generate Implementation Tasks

```python
# Check context capacity
check_context_capacity()

# Read and analyze specifications
import re
from pathlib import Path

spec_file = Path(f"specs/{SLUG}/spec.md")
plan_file = Path(f"specs/{SLUG}/plan.md")

spec_content = spec_file.read_text()
plan_content = plan_file.read_text()

# Parse implementation steps from plan
# Extract components, endpoints, models, etc.
# Generate detailed tasks adapted to ${STACK}

tasks = []
task_id = 1

# Task 1: Database schema (if applicable)
if DATABASE != "none":
    tasks.append({
        "id": f"impl_{task_id:03d}",
        "task": "Create database schema and migrations",
        "files": get_schema_files_for_orm(ORM),
        "status": "pending",
        "prompt": f"""Implement data models from specs/{SLUG}/data-model.md.

Create:
1. Database schema with all models, fields, relations
2. Indexes for performance (on foreign keys, frequently queried fields)
3. Enums for status fields
4. Migration file

Tech: {DATABASE}, {ORM}
Commands:
  - Migrate: {MIGRATE_CMD}
  - Generate: {GENERATE_CMD}

Quality checks:
- All fields have appropriate types and constraints
- Relations are bidirectional where needed
- Indexes on all foreign keys
- Migration is reversible (includes 'down' migration if supported)

On completion: Run migration, generate ORM client
"""
    })
    task_id += 1

# Generate additional tasks based on plan analysis
# ... (task generation logic adapted to STACK)

# Check context after task generation
check_context_capacity()

# Update TODO file with generated tasks
todo_path = Path(f"{TODO_FILE}")
content = todo_path.read_text()

# Build task markdown
task_markdown = "\n\n".join([
    f"""#### {task['id']}
- **task**: {task['task']}
- **files**: {task['files']}
- **status**: {task['status']}
- **prompt**: |
    {task['prompt']}"""
    for task in tasks
])

# Insert into Batch 2.1 section
content = re.sub(
    r'(### Batch 2.1: Core Development\n\n)\(Tasks will be generated after specifications are complete\)',
    rf'\1{task_markdown}',
    content
)

# Generate test tasks for Batch 3.1
test_tasks = generate_test_tasks(tasks, TEST_FRAMEWORK, TEST_CMD)

test_markdown = "\n\n".join([
    f"""#### {task['id']}
- **task**: {task['task']}
- **files**: {task['files']}
- **status**: {task['status']}
- **prompt**: |
    Write comprehensive unit tests using {TEST_FRAMEWORK}.
    
    Coverage requirements:
    - All functions tested
    - All branches covered
    - Edge cases tested
    - Error scenarios tested
    - Minimum 80% coverage
    
    Commands:
      - Test: {TEST_CMD}
      - Coverage: {COVERAGE_CMD}"""
    for task in test_tasks
])

content = re.sub(
    r'(### Batch 3.1: Unit Tests\n\n)\(Tasks will be generated after implementation\)',
    rf'\1{test_markdown}',
    content
)

# Update workflow progress
context_usage = get_context_usage_percentage()
content = re.sub(
    r'workflow_progress:.*?(?=\`\`\`)',
    f'''workflow_progress:
  phase: 2
  current_step: "2.3"
  last_task: "task_generation"
  last_update: "{datetime.utcnow().isoformat()}Z"
  status: "tasks_generated"
  total_impl_tasks: {len(tasks)}
  total_test_tasks: {len(test_tasks)}
  context_usage: "{context_usage}%"
''',
    content,
    flags=re.DOTALL
)

# Add status history
timestamp = datetime.utcnow().isoformat() + 'Z'
content = re.sub(
    r'(## Status History)',
    rf'\1\n- {timestamp}: Generated {len(tasks)} implementation tasks, {len(test_tasks)} test tasks',
    content
)

todo_path.write_text(content)

# Commit TODO update
cd("${MAIN_REPO}")
run(f'git add TODO_{TYPE}_{ID}.md')
run(f'git commit -m "feat({SLUG}): generate implementation tasks"')
run(f'git push origin contrib/{GITHUB_USER}')
cd("${CURRENT_DIR}")

# Final context check
check_context_capacity()
```

**Prompt user:**
```
✓ Generated implementation tasks (adapted to ${STACK})

Created <N> implementation tasks:
  - impl_001: Create database schema and migrations (${ORM})
  - impl_002: Create core business logic functions
  - impl_003: Create API endpoints
  - impl_004: Create UI components
  [... additional tasks]

Created <M> test tasks:
  - test_001: Unit tests using ${TEST_FRAMEWORK}
  - test_002: Unit tests for business logic
  - test_003: Integration tests for API
  [... additional tests]

Context usage: <percentage>%

Next step from WORKFLOW.md:
Step 2.4: Implement task impl_001

Task: Create database schema and migrations
Files: [List files]

Would you like to proceed with Step 2.4? (Y/n)
```

### Step 2.4 - 2.N: Implement Tasks Iteratively

For each pending implementation task:

```bash
# CRITICAL: Check context capacity before EVERY task
check_context_capacity
```

```markdown
**Executing task: <task_id>**

Context usage: <percentage>%

Reading prompt from TODO_${TYPE}_*.md...

[Show task prompt to user]

---

I'll implement this task now using ${STACK} conventions.

[Read spec files for context]
[Analyze requirements]
[Generate implementation adapted to STACK]

Example for impl_001 (Database schema):

Based on specs/<slug>/data-model.md, I'll create the schema for ${ORM}.

[Generate code appropriate for detected ORM]

Now running migration:

\`\`\`bash
${MIGRATE_CMD}
${GENERATE_CMD}
\`\`\`

✓ Schema created
✓ Migration applied
✓ ORM client generated

[Create implementation files]
[Write code according to spec]
[Add comments and documentation]
```

```bash
# Check context before commit
check_context_capacity

# Check if implementation replaces/deprecates existing files
if [ -n "$DEPRECATED_FILES" ]; then
  echo "This implementation deprecates existing files."
  echo "Files to be deprecated:"
  for file in $DEPRECATED_FILES; do
    echo "  - $file"
  done
  echo ""
  read -p "Archive description (e.g., 'old-auth-flow'): " DEPRECATION_DESC
  
  # Use deprecate_files helper function
  deprecate_files "${TODO_FILE}" "$DEPRECATION_DESC" $DEPRECATED_FILES
fi

# Commit the implementation
git add .
git commit -m "feat(${SLUG}): ${TASK_DESCRIPTION}

Implements: ${TASK_ID}
Spec: specs/${SLUG}/spec.md
Stack: ${STACK}

Changes:
- [List key changes]
$([ -n "$DEPRECATED_FILES" ] && echo "
Deprecated:
- Archived to ARCHIVED/\${TIMESTAMP}_\${DEPRECATION_DESC}.zip")

Refs: TODO_${TYPE}_${ID}.md"

git push origin "${CURRENT_BRANCH}"

# Update TODO file
python3 <<PYSCRIPT
import re
from pathlib import Path
from datetime import datetime

todo_path = Path("${TODO_FILE}")
content = todo_path.read_text()

# Mark task as complete
content = re.sub(
    rf'(#### {TASK_ID}.*?status: )pending',
    r'\1complete',
    content,
    flags=re.DOTALL
)

# Update workflow progress with context usage
context_usage = get_context_usage_percentage()
content = re.sub(
    r'workflow_progress:.*?(?=\`\`\`)',
    f'''workflow_progress:
  phase: 2
  current_step: "2.{STEP_NUM}"
  last_task: "{TASK_ID}"
  last_update: "{datetime.utcnow().isoformat()}Z"
  status: "implementation"
  context_usage: "{context_usage}%"
''',
    content,
    flags=re.DOTALL
)

# Add to status history
timestamp = datetime.utcnow().isoformat() + 'Z'
content = re.sub(
    r'(## Status History)',
    rf'\1\n- {timestamp}: Completed {TASK_ID}: {TASK_DESCRIPTION}',
    content
)

todo_path.write_text(content)
PYSCRIPT

# Commit TODO update
cd "${MAIN_REPO}"
git add "TODO_${TYPE}_${ID}.md"
git commit -m "chore(${SLUG}): mark ${TASK_ID} complete"
git push origin "contrib/${GITHUB_USER}"
cd "${CURRENT_DIR}"

# Check context after update
check_context_capacity
```

**Prompt user:**
```
✓ Task <task_id> complete
✓ Implementation committed
✓ TODO file updated

Context usage: <percentage>%
$([ $CONTEXT_USAGE -ge 50 ] && echo "⚠️ Context will be reset before next step")

Next step from WORKFLOW.md:
Step 2.<N+1>: Implement task <next_task_id>

Task: <next_task_description>
Files: [List files]

Would you like to proceed with Step 2.<N+1>? (Y/n)
```

**Repeat for ALL implementation and test tasks, checking context at each step...**

**[Continue with remaining workflow phases as before, adding check_context_capacity() calls at strategic points throughout]**

---

## Summary for Claude Code

**YOU ARE CLAUDE CODE.** When the user asks "next step?":

1. **Check context capacity FIRST**
   - If ≥ 50% → Update TODO file → Run /init → Resume

2. **Detect context:**
   - Check current directory (main repo vs worktree)
   - Check current branch
   - Determine workflow phase
   - Worktree can be feature, release, or hotfix

3. **Find TODO file:**
   - If in worktree: `../TODO_[feature,release,hotfix]_<timestamp>_<slug>.md`
   - If in main repo: `TODO_[feature,release,hotfix]_*.md` (find active)

4. **Parse TODO:**
   - Read `workflow_progress` section
   - Find next pending task
   - Check quality gates
   - Note tech stack in frontmatter

5. **Prompt user:**
   ```
   Next step from WORKFLOW.md:
   Step <phase>.<step>: <description>
   
   <what will happen>
   
   Would you like to proceed with Step <phase>.<step>? (Y/n)
   ```

6. **Wait for "Y":**
   - Do NOTHING until user confirms
   - If "n", skip and wait for next "next step?"

7. **Execute step:**
   - Check context capacity
   - Run git operations
   - Create/modify files using detected tech stack
   - Update TODO file workflow_progress section
   - Commit changes
   - Check context capacity again

8. **Update status:**
   - Mark task complete in TODO
   - Update workflow_progress with timestamp and context_usage
   - Add entry to status history

9. **Repeat:** Wait for next "next step?"

---

## Key Behaviors

✓ **Monitor context at 50%** - Save state and run /init automatically  
✓ **Adapt everything** - Detect tech stack, adapt all examples  
✓ **BMAD in main repo** - Planning documents when on contrib branch  
✓ **SpecKit in worktree** - Specifications for features/releases/hotfixes  
✓ **Interactive confirmation** - Never proceed without "Y"  
✓ **AI conflict resolution** - Reason through merge conflicts with context  
✓ **Semantic versioning** - Analyze components for version bump  
✓ **Quality gates** - Enforce 80% coverage using detected test framework  
✓ **Status tracking** - Document progress in TODO_[feature,release,hotfix]_*.md files  
✓ **Manual PR merges** - User merges in GitHub UI  
✓ **Daily rebase** - Expected developer workflow  
✓ **Tech stack adaptation** - Use detected commands (TEST_CMD, BUILD_CMD, etc.)

---

## Never Do These

✗ **Never proceed without confirmation**  
✗ **Never merge PRs automatically**  
✗ **Never skip quality gates**  
✗ **Never make assumptions about project structure**  
✗ **Never use Dockerfile** (use Containerfile for Podman)  
✗ **Never forget to update TODO workflow_progress**  
✗ **Never delete branches before PRs are merged**  
✗ **Never exceed 50% context without saving state**  
✗ **Never use hardcoded commands** (always use detected variables)

---

## Always Do These

✓ **Always check context capacity at strategic points**  
✓ **Always adapt examples to detected tech stack**  
✓ **Always update TODO file after each step with context_usage**  
✓ **Always run tests using detected TEST_CMD**  
✓ **Always check coverage using detected COVERAGE_CHECK**  
✓ **Always build using detected BUILD_CMD**  
✓ **Always provide reasoning for AI decisions**  
✓ **Always show what will happen before executing**  
✓ **Always keep TODO files in sync via git operations**  
✓ **Always use Containerfile (not Dockerfile)**  
✓ **Always use detected ORM commands for migrations**  
✓ **Always maintain directory standards:**
  - Every directory has CLAUDE.md and README.md
  - Every directory (except ARCHIVED) has an ARCHIVED/ subdirectory
  - Use create_directory_structure() helper for new directories
✓ **Always deprecate files properly:**
  - Use deprecate_files() helper function
  - Zip format: YYYYMMDDTHHMMSSZ_<description>.zip
  - Store in ARCHIVED/ directory
✓ **Always limit completed items to last 10 in TODO.md**  

---

**END OF DIRECTIVE**