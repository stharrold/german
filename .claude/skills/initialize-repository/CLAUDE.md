# Claude Code Context: initialize-repository

## Purpose

Initialize-repository is a **meta-skill (Phase 0)** that bootstraps new repositories with the complete workflow system. It provides an interactive callable tool for replicating skills, documentation, and standards from a source repository to a new target repository.

## Directory Structure

```
.claude/skills/initialize-repository/
├── scripts/
│   ├── initialize_repository.py  # Main initialization script (993 lines)
│   └── __init__.py              # Package initialization
├── SKILL.md                      # Complete skill documentation (558 lines)
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Script

### initialize_repository.py

**Purpose:** Interactive tool to bootstrap new repositories with workflow system

**When to use:** Phase 0 (before any other workflow phases) - run once per new repository

**Location requirement:** Can be run from anywhere, requires paths to source and target repositories

**Invocation:**
```bash
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  <source-repo> <target-repo>
```

**Example:**
```bash
# From current repository
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project

# From absolute paths
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  /path/to/german /path/to/my-new-project
```

**What it does:**
1. Validates source repository has workflow system (≥3/7 skills)
2. Validates target repository path
3. Conducts 4-phase interactive Q&A:
   - **Phase 1:** Configuration (repo details, tech stack, components to copy)
   - **Phase 2:** Git setup (initialize, branches, remote)
   - **Phase 3:** File operations (copy skills, adapt docs, create structure)
   - **Phase 4:** Git initialization (commit, branches, push)
4. Validates created repository structure
5. Reports what was created and next steps

**Key features:**
- Copies all 8 skills (including this meta-skill)
- Adapts README.md, CLAUDE.md, pyproject.toml for new repo
- Copies WORKFLOW.md, CONTRIBUTING.md verbatim
- Creates compliant directory structure (ARCHIVED/, planning/, specs/)
- Optional git initialization with 3-branch structure
- Optional remote setup and push
- Validates result and provides next steps

## Usage by Claude Code

### When to Call This Meta-Skill

**Context:** User wants to start a new repository with the workflow system

**User says:**
- "Initialize a new repository"
- "Bootstrap workflow system"
- "Replicate workflow to new repo"
- "Start new project with this workflow"

**Claude Code should:**
1. Recognize this is Phase 0 (not part of normal workflow)
2. Call the initialize_repository.py script (don't reproduce functionality)
3. Let the script handle:
   - All Q&A with user
   - File copying and adaptation
   - Git initialization
   - Validation
4. After script completes, user can use new repository for Phase 1+

### Token Efficiency

**Before (Manual Approach):**
- Claude Code reads WORKFLOW.md, CLAUDE.md, all skills (~1,500-2,000 tokens)
- Claude Code manually copies files
- Claude Code manually adapts documentation
- Claude Code manually creates git structure
- ~3,500 tokens total

**After (Callable Tool):**
- Claude Code calls script once (~150 tokens)
- Script handles all logic
- ~150 tokens to invoke
- **Savings: ~3,350 tokens (96% reduction)**

## Integration with Other Skills

**This meta-skill does NOT integrate with other skills.**

**Relationship:**

```
Phase 0: Initialize Repository (this meta-skill)
  ↓
  Creates environment containing:
    - 8 skills (including this one)
    - Complete documentation
    - Quality configurations
    - Directory structure
  ↓
Phase 1-6: Normal workflow (bmad, speckit, quality, git, etc.)
```

**After initialization:**
- New repository has all skills installed
- User starts with Phase 1 (BMAD planning)
- This meta-skill is not used again

**Key distinction:**
- Other skills operate **within** a repository
- This meta-skill operates **across** repositories (source → target)
- Other skills are coordinated by workflow-orchestrator
- This meta-skill is standalone (no orchestrator involvement)

## Components Copied

### Always Copied (Required)

**8 workflow skills:**
- workflow-orchestrator
- tech-stack-adapter
- git-workflow-manager
- bmad-planner
- speckit-author
- quality-enforcer
- workflow-utilities
- initialize-repository (this meta-skill)

**Documentation:**
- WORKFLOW.md (copied verbatim)
- CONTRIBUTING.md (copied verbatim)
- .claude/skills/UPDATE_CHECKLIST.md (copied verbatim)

**Generated files:**
- README.md (adapted for new repo)
- CLAUDE.md (adapted for new repo)
- pyproject.toml (generated with new repo details)
- CHANGELOG.md (generated with v0.1.0 entry)
- TODO.md (generated master manifest)

**Configuration:**
- .gitignore (copied verbatim)

### Optionally Copied

**Domain content** (if user selects):
- src/ directory
- resources/ directory

**Tests** (if user selects):
- tests/ directory

**Containers** (if user selects):
- Containerfile
- podman-compose.yml

## Adaptation Logic

**Files copied verbatim (no changes):**
- .claude/skills/* (all skills)
- WORKFLOW.md
- CONTRIBUTING.md
- .claude/skills/UPDATE_CHECKLIST.md
- .gitignore

**Files generated/adapted:**
- README.md → uses repo name, purpose, description from Q&A
- CLAUDE.md → uses repo purpose, inserts workflow section from source
- pyproject.toml → uses repo name, description, Python version from Q&A
- CHANGELOG.md → uses current date for [0.1.0] entry
- TODO.md → uses current timestamp

**Rationale:**
- Workflow system is technology-agnostic → copy verbatim
- Repository-specific files must be customized → adapt via Q&A

## Interactive Q&A Summary

**Phase 1 questions (9 total):**
1. Repository purpose (Web app / CLI tool / Library / Data / ML / Other)
2. Brief description (one line)
3. GitHub username
4. Python version (3.11 / 3.12 / 3.13)
5. Copy workflow system? (required, always yes)
6. Copy domain-specific content? (yes/no)
7. Copy sample tests? (yes/no)
8. Copy container configs? (yes/no)

**Phase 2 questions (4-5 total):**
9. Initialize git repository? (yes/no)
10. If yes: Create branch structure? (yes/no)
11. If yes: Set up remote? (yes/no)
12. If yes: Remote URL
13. If yes and remote: Push to remote? (yes/no)

**Total: 13-14 questions (depending on git setup choices)**

## Output Structure

After successful initialization, target repository has:

```
target-repo/
├── .claude/
│   └── skills/              # 8 skills copied
├── ARCHIVED/                # With CLAUDE.md, README.md
├── planning/                # With CLAUDE.md, README.md, ARCHIVED/
├── specs/                   # With CLAUDE.md, README.md, ARCHIVED/
├── README.md                # Generated for new repo
├── CLAUDE.md                # Generated for new repo
├── WORKFLOW.md              # Copied verbatim
├── CONTRIBUTING.md          # Copied verbatim
├── CHANGELOG.md             # Generated with v0.1.0
├── TODO.md                  # Generated master manifest
├── pyproject.toml           # Generated with new repo details
└── .gitignore               # Copied verbatim
```

Plus optionally: src/, resources/, tests/, Containerfile, podman-compose.yml

## Workflow Integration

**NOT part of Phase 1-6 workflow.** This is Phase 0 (bootstrapping).

**When to use:**
- User: "I want to start a new project with this workflow"
- Claude Code: Call initialize_repository.py
- User: [Answer Q&A questions]
- Script: Creates new repository
- User: `cd` to new repository, start Phase 1 (BMAD planning)

**Lifecycle:**
```
1. User has repository A with workflow system
2. User wants new repository B with same workflow
3. Run initialize_repository.py (Phase 0)
4. Repository B now has workflow system
5. User works in Repository B using Phases 1-6
6. This meta-skill is not used again in Repository B
```

## Example Usage

```bash
# User has 'german' repository with workflow system
# User wants 'my-cli-tool' repository with same workflow

python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  /path/to/german /path/to/my-cli-tool

# [Interactive Q&A session]
# Repository purpose: CLI tool
# Description: Command-line tool for X
# GitHub username: stharrold
# Python version: 3.11
# Copy workflow: yes
# Copy domain: no
# Copy tests: yes
# Copy containers: no
# Initialize git: yes
# Create branches: yes
# Set up remote: yes
# Remote URL: https://github.com/stharrold/my-cli-tool.git
# Push to remote: yes

# [Script creates repository with full workflow system]

# User now works in my-cli-tool:
cd /path/to/my-cli-tool
uv sync
python .claude/skills/bmad-planner/scripts/create_planning.py first-feature stharrold
```

## Best Practices

**When calling this meta-skill:**
1. Ensure source repository has complete workflow system (≥3/7 skills)
2. Validate `gh` CLI is authenticated before running
3. Decide what to copy (workflow-only recommended for clean start)
4. Have remote repository URL ready if setting up remote
5. After initialization, review and customize generated README.md and CLAUDE.md

**When NOT to use:**
1. Repository already has workflow system (update manually instead)
2. Need only specific skills (copy them manually)
3. Completely different technology stack (requires manual adaptation)

## Token Savings

**Manual approach:** ~3,500 tokens (read docs + copy files + adapt)
**Callable tool:** ~150 tokens (invoke script)
**Savings:** ~3,350 tokens (96% reduction)

**Time savings:** ~30-60 minutes of manual work

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation (558 lines)
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**Child Directories:**
- **[scripts/](scripts/)** - Initialization script (initialize_repository.py)
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

**Does NOT integrate with other skills** - this is a meta-skill that creates the environment for other skills.

After initialization, the target repository has all 7 workflow skills ready to use:
- workflow-orchestrator
- tech-stack-adapter
- git-workflow-manager
- bmad-planner
- speckit-author
- quality-enforcer
- workflow-utilities
