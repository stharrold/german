---
name: initialize-repository
version: 1.0.0
description: |
  Meta-skill (Phase 0) for bootstrapping new repositories with
  workflow system. Interactive callable tool that copies skills,
  documentation, and standards from source repository.

  Use when: Starting a new project that needs the workflow system

  Triggers: "initialize new repository", "bootstrap workflow",
  "replicate workflow system"
---

# Initialize-Repository Meta-Skill

## Purpose

The **initialize-repository** meta-skill is a Phase 0 (bootstrapping) tool that replicates the complete workflow system from a source repository to a new target repository. It provides an interactive Q&A system to configure what components get copied and how they're adapted for the new context.

**Key capabilities:**
- Copy all 8 workflow skills from source to target
- Adapt documentation for new repository context
- Generate customized README.md, CLAUDE.md, pyproject.toml
- Optionally copy domain-specific content, tests, containers
- Initialize git with branch structure (main, develop, contrib)
- Create compliant directory structure (ARCHIVED/, planning/, specs/)
- Validate the created repository structure

**Token efficiency:**
- Manual setup: ~3,500 tokens
- Callable tool: ~150 tokens
- **Savings: ~3,350 tokens (96% reduction)**

## When to Use

Use this meta-skill when:

- Starting a new project that needs the workflow system
- Migrating an existing project to the workflow system
- Creating a template repository with workflow standards
- Bootstrapping multiple repositories with consistent workflow

**NOT part of normal workflow phases (1-6).** This is Phase 0, run once per repository to set up the environment for the other skills to operate.

## Interactive Callable Tool

### Command Syntax

```bash
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  <source-repo> <target-repo>
```

**Arguments:**
- `source-repo`: Path to source repository (with workflow system)
- `target-repo`: Path to target repository (will be created)

### Example Usage

```bash
# Initialize new repository from current repo
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  /path/to/german /path/to/my-new-project

# From current directory (source repo)
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project
```

### Interactive Session Flow

The script conducts a 4-phase interactive Q&A session:

#### Phase 1: Configuration Selection

**Repository details:**
1. Name (auto-detected from target path)
2. Purpose (Web app / CLI tool / Library / Data analysis / ML / Other)
3. Brief description (one line)
4. GitHub username (auto-detected from `gh` CLI)

**Technology stack:**
5. Python version (3.11 / 3.12 / 3.13)

**Components to copy:**
6. Copy workflow system? (required, always yes)
7. Copy domain-specific content (src/, resources/)? (yes/no)
8. Copy sample tests (tests/)? (yes/no)
9. Copy container configs (Containerfile, podman-compose.yml)? (yes/no)

#### Phase 2: Git Setup

10. Initialize git repository? (yes/no)
11. If yes: Create branch structure (main, develop, contrib)? (yes/no)
12. If yes: Set up remote repository? (yes/no)
13. If yes: Remote URL (e.g., https://github.com/user/repo.git)
14. If yes and remote: Push to remote? (yes/no)

#### Phase 3: File Operations (Automatic)

**Copied verbatim:**
- `.claude/skills/` (all 9 skills including this one)
- `WORKFLOW.md` (complete workflow guide)
- `CONTRIBUTING.md` (contributor guidelines)
- `.claude/skills/UPDATE_CHECKLIST.md` (skill update checklist)
- `.gitignore` (git exclusions)

**Generated/adapted:**
- `README.md` (customized for new repo purpose)
- `CLAUDE.md` (customized for new repo context)
- `pyproject.toml` (new repo name, purpose, dependencies)
- `CHANGELOG.md` (initial version 0.1.0)
- `TODO.md` (master workflow manifest)

**Created:**
- Directory structure (ARCHIVED/, planning/, specs/)
- CLAUDE.md and README.md in each directory
- ARCHIVED/ subdirectories with their own CLAUDE.md/README.md

**Optionally copied:**
- `src/` and `resources/` (if copy_domain = yes)
- `tests/` (if copy_tests = yes)
- `Containerfile`, `podman-compose.yml` (if copy_containers = yes)

#### Phase 4: Git Initialization (Conditional)

If init_git = yes:
1. Initialize git repository
2. Create initial commit on main (with proper format)
3. Create develop branch from main (if create_branches = yes)
4. Create contrib/<gh-user> branch from develop (if create_branches = yes)
5. Set up remote origin (if remote_url provided)
6. Push to remote (if user confirms)

### Example Interactive Session

```
=== Phase 1: Configuration Selection ===

What is the primary purpose of this repository?
  1) Web application
  2) CLI tool
  3) Library/package
  4) Data analysis
  5) Machine learning
  6) Other
> 3

Brief description of the repository (one line):
> Python library for task automation

GitHub username [default: stharrold]
> stharrold

Python version
  1) 3.11
  2) 3.12
  3) 3.13
  [default: 3.11]
> 1

Which components should be copied?

Copy workflow system (.claude/skills/, WORKFLOW.md, etc.)? (Y/n)
> y

Copy domain-specific content (src/, resources/)? (y/N)
> n

Copy sample tests (tests/)? (y/N)
> y

Copy container configs (Containerfile, podman-compose.yml)? (y/N)
> n

✓ Configuration complete

=== Phase 2: Git Setup ===

Initialize git repository? (Y/n)
> y

Create branch structure (main, develop, contrib)? (Y/n)
> y

Set up remote repository? (y/N)
> y

Remote URL (e.g., https://github.com/user/repo.git):
> https://github.com/stharrold/my-new-project.git

✓ Git setup configuration complete

Review Configuration:
  Source: /path/to/german
  Target: /path/to/my-new-project
  Name: my-new-project
  Purpose: Library/package
  GitHub User: stharrold
  Copy workflow: True
  Copy domain: False
  Initialize git: True

Proceed with initialization? (Y/n)
> y

=== Phase 3: File Operations ===

ℹ Copying workflow skills...
✓ Copied skill: workflow-orchestrator
✓ Copied skill: tech-stack-adapter
✓ Copied skill: git-workflow-manager
✓ Copied skill: bmad-planner
✓ Copied skill: speckit-author
✓ Copied skill: quality-enforcer
✓ Copied skill: workflow-utilities
✓ Copied skill: initialize-repository
✓ Copied 9/9 skills

ℹ Copying workflow documentation...
✓ Copied: WORKFLOW.md
✓ Copied: CONTRIBUTING.md
✓ Copied: .claude/skills/UPDATE_CHECKLIST.md

ℹ Generating README.md...
✓ Generated README.md

ℹ Generating CLAUDE.md...
✓ Generated CLAUDE.md

ℹ Generating pyproject.toml...
✓ Generated pyproject.toml

ℹ Copying .gitignore...
✓ Copied .gitignore

ℹ Creating directory structure...
✓ Created: ARCHIVED/
✓ Created: planning/
✓ Created: specs/
✓ Created: tests/
✓ Directory structure created

ℹ Creating TODO.md master manifest...
✓ Created TODO.md master manifest

ℹ Creating CHANGELOG.md...
✓ Created CHANGELOG.md

ℹ Copying tests...
✓ Copied: tests/

✓ File operations complete

=== Phase 4: Git Initialization ===

ℹ Initializing git repository...
✓ Git initialized

ℹ Creating initial commit...
✓ Initial commit created on main

ℹ Creating develop branch...
✓ Created develop branch

ℹ Creating contrib/stharrold branch...
✓ Created contrib/stharrold branch

ℹ Setting up remote: https://github.com/stharrold/my-new-project.git
✓ Remote configured

Push to remote? (y/N)
> y

✓ Pushed to remote

✓ Git initialization complete

ℹ Validating repository structure...
✓ Repository structure validated

============================================================
✓ Repository Initialization Complete
============================================================

Repository: /path/to/my-new-project
Name: my-new-project
Purpose: Library/package
GitHub User: stharrold

Created:
  ✓ Workflow system (9 skills)
  ✓ Documentation (WORKFLOW.md, CLAUDE.md, CONTRIBUTING.md)
  ✓ Quality configs (pyproject.toml, .gitignore)
  ✓ Directory structure (ARCHIVED/, planning/, specs/)
  ✓ Tests (tests/)

Git:
  ✓ Initialized repository
  ✓ Created branches: main, develop, contrib/stharrold
  ✓ Remote configured: https://github.com/stharrold/my-new-project.git

Next Steps:
  1. cd /path/to/my-new-project
  2. uv sync
  3. Start first feature:
     python .claude/skills/bmad-planner/scripts/create_planning.py \
       my-feature stharrold

Documentation:
  - README.md - Project overview
  - WORKFLOW.md - Complete workflow guide
  - CLAUDE.md - Claude Code interaction guide
  - CONTRIBUTING.md - Contributor guidelines

🎉 Happy coding!
```

## Components Copied

### Always Copied (Workflow System)

**Skills (8 total):**
```
.claude/skills/
├── workflow-orchestrator/    (~300 lines SKILL.md, orchestrator logic)
├── tech-stack-adapter/        (~200 lines, detect_stack.py)
├── git-workflow-manager/      (~500 lines, 8 scripts)
├── bmad-planner/              (~400 lines, 1006-line script, 3 templates)
├── speckit-author/            (~400 lines, 2 scripts, 2 templates)
├── quality-enforcer/          (~300 lines, 2 scripts)
├── workflow-utilities/        (~200 lines, 7 utility scripts)
└── initialize-repository/     (~400 lines, this meta-skill)
```

**Documentation:**
- `WORKFLOW.md` (2,023 lines) - Complete 6-phase workflow guide
- `CONTRIBUTING.md` (575 lines) - Contributor guidelines with quality standards
- `.claude/skills/UPDATE_CHECKLIST.md` (393 lines) - Skill update checklist

**Configuration:**
- `.gitignore` (290 chars) - Git exclusions for Python/IDE/OS files

### Generated/Adapted Files

**README.md:**
- Customized for new repository name and purpose
- Quick start guide with installation commands
- Workflow commands with correct GitHub username
- Quality standards and contributing link

**CLAUDE.md:**
- Repository purpose from Q&A
- Code architecture section (placeholder for user to fill)
- Workflow architecture section from source (copied verbatim)
- Common commands with correct GitHub username
- Quality gates and git branch structure

**pyproject.toml:**
- New repository name
- New description
- Python version from Q&A
- Standard dependencies (pytest, pytest-cov, ruff, mypy)
- Tool configurations (ruff, mypy, pytest)

**CHANGELOG.md:**
- Initial [0.1.0] entry with current date
- [Unreleased] section for future changes

**TODO.md:**
- Master workflow manifest with YAML frontmatter
- Empty active/archived workflow lists
- Ready for first workflow creation

### Directory Structure Created

```
target-repo/
├── .claude/
│   └── skills/           # 9 skills copied
├── ARCHIVED/             # With CLAUDE.md, README.md
├── planning/             # With CLAUDE.md, README.md, ARCHIVED/
├── specs/                # With CLAUDE.md, README.md, ARCHIVED/
├── src/                  # Optional (if copy_domain = yes)
├── resources/            # Optional (if copy_domain = yes)
├── tests/                # Optional (if copy_tests = yes)
├── README.md             # Generated
├── CLAUDE.md             # Generated
├── WORKFLOW.md           # Copied verbatim
├── CONTRIBUTING.md       # Copied verbatim
├── CHANGELOG.md          # Generated
├── TODO.md               # Generated
├── pyproject.toml        # Generated
└── .gitignore            # Copied verbatim
```

Every directory (except ARCHIVED itself) contains:
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory with its own CLAUDE.md and README.md

## Adaptation Logic

### Files Copied Verbatim

These files are **not modified** during copying:

**Workflow system:**
- All `.claude/skills/` files (SKILL.md, CLAUDE.md, scripts, templates)
- `WORKFLOW.md` (workflow is technology-agnostic)
- `CONTRIBUTING.md` (standards apply to all repos)
- `.claude/skills/UPDATE_CHECKLIST.md` (update process unchanged)
- `.gitignore` (Python/IDE exclusions standard)

**Rationale:** These files define the workflow system itself and should be identical across all repositories using the system.

### Files Generated/Adapted

These files are **customized** for the new repository:

**README.md:**
- Repository name → from target path
- Description → from Q&A
- Purpose → from Q&A
- GitHub username → from Q&A or `gh` CLI
- Quick start commands → adapted for new repo name
- Workflow commands → adapted for new GitHub username

**CLAUDE.md:**
- Repository purpose → from Q&A
- Code architecture → placeholder for user to fill
- Workflow architecture → from source CLAUDE.md (workflow sections)
- Commands → adapted for new GitHub username
- Branch structure → adapted for new GitHub username

**pyproject.toml:**
- project.name → new repository name
- project.description → from Q&A
- requires-python → from Q&A (3.11/3.12/3.13)
- tool.ruff.target-version → from Python version
- tool.mypy.python_version → from Python version

**CHANGELOG.md:**
- [0.1.0] date → current date
- Initial entry → describes workflow system initialization

**TODO.md:**
- last_update → current timestamp
- Empty workflow lists → ready for first workflow

## Output Structure

After running the script, the target repository will have:

**8 workflow skills:**
- All SKILL.md, CLAUDE.md, README.md, CHANGELOG.md files
- All Python scripts and templates
- All ARCHIVED/ directories with documentation

**Complete documentation:**
- Customized README.md and CLAUDE.md
- Complete WORKFLOW.md and CONTRIBUTING.md
- Initial CHANGELOG.md

**Quality configurations:**
- pyproject.toml with test/lint/type configs
- .gitignore for Python projects

**Compliant directory structure:**
- Every directory has CLAUDE.md, README.md, ARCHIVED/
- planning/, specs/, ARCHIVED/ ready for workflow use

**Optional git initialization:**
- Three-branch structure (main, develop, contrib/<gh-user>)
- Initial commit with proper format
- Remote configured and pushed (optional)

**Master workflow manifest:**
- TODO.md ready to track workflows
- Compliant YAML frontmatter structure

## Integration with Workflow

**This is NOT part of the normal 6-phase workflow.** It's Phase 0 (bootstrapping).

**Relationship to other phases:**

```
Phase 0: Initialize Repository (this meta-skill)
  ↓ Creates environment for...

Phase 1: Planning (BMAD)
Phase 2: Development (SpecKit, feature worktrees)
Phase 3: Quality (quality-enforcer)
Phase 4: Integration (git-workflow-manager, PRs)
Phase 5: Release (release automation)
Phase 6: Hotfix (production fixes)
```

**After running this meta-skill:**
1. New repository has complete workflow system
2. User can immediately start Phase 1 (BMAD planning)
3. All skills are available and ready to use

**Does NOT interact with:**
- workflow-orchestrator (orchestrator only coordinates Phases 1-6)
- Other skills (they operate in the initialized repository)

**Use case:**
- Run once per new repository
- Creates the foundation for all other skills to operate
- After initialization, never run again in that repository

## Token Efficiency

**Manual approach (without this meta-skill):**

1. Read WORKFLOW.md (~2,000 lines → ~1,500 tokens)
2. Read CLAUDE.md (~800 lines → ~600 tokens)
3. Read all 9 skill SKILL.md files (~3,200 lines → ~2,400 tokens)
4. Manually copy .claude/skills/ directory structure
5. Manually adapt README.md, CLAUDE.md, pyproject.toml
6. Manually create directory structure
7. Manually initialize git with branch structure

**Total: ~3,500 tokens + manual work**

**Callable tool approach (with this meta-skill):**

1. Call initialize_repository.py (~150 tokens)
2. Answer Q&A questions (~50 tokens for responses)
3. Script handles all copying, adaptation, git setup

**Total: ~200 tokens**

**Savings: ~3,300 tokens (94% reduction)**

**Additional benefits:**
- Consistent structure across all repositories
- No missed files or incorrect adaptations
- Proper git initialization with correct format
- Validation of created structure
- Time saved (minutes vs hours)

## Best Practices

**Before running:**
1. Ensure source repository has complete workflow system
2. Validate `gh` CLI is authenticated (`gh auth status`)
3. Decide what components to copy (workflow-only vs full template)
4. Have remote repository URL ready (if setting up remote)

**During Q&A:**
1. Provide accurate repository purpose (affects generated README)
2. Use correct GitHub username (affects branch names)
3. Choose Python version matching your project needs
4. Copy tests only if they're reusable (not domain-specific)
5. Copy containers only if architecture is similar

**After initialization:**
1. Review generated README.md and CLAUDE.md
2. Fill in code architecture section in CLAUDE.md
3. Customize CHANGELOG.md if needed
4. Run `uv sync` to install dependencies
5. Start first feature with BMAD planning

**When to NOT use:**
1. Repository already has workflow system (use update scripts instead)
2. Need partial workflow system (manually copy specific skills)
3. Completely different technology stack (adapt manually)

## Error Handling

The script validates and handles errors at each phase:

**Pre-flight checks:**
- Required tools (git, gh) must be installed
- Source repository must have .claude/skills/ directory
- Source repository must have at least 3/9 skills
- Target directory warns if not empty

**During execution:**
- Invalid user input prompts retry
- Git commands wrapped in try/except
- File operations check for existence
- Remote setup handles authentication failures

**Post-execution validation:**
- Checks for all required files
- Checks for all required directories
- Reports missing items if validation fails

**Exit codes:**
- 0: Success (or user abort before changes)
- 1: Error (tool missing, invalid repo, operation failed)

## Related Documentation

- **[scripts/initialize_repository.py](scripts/initialize_repository.py)** - Main script (993 lines)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code usage context
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Related Skills

**Does NOT integrate with other skills** - this is a meta-skill that creates the environment for them.

**Creates foundation for:**
- workflow-orchestrator (Phase 1-6 coordinator)
- bmad-planner (Phase 1: Planning)
- speckit-author (Phase 2: Specifications)
- git-workflow-manager (Phase 2-4: Git operations)
- quality-enforcer (Phase 3: Quality gates)
- tech-stack-adapter (detect configuration)
- workflow-utilities (shared utilities)

**After initialization, users interact with the 7 workflow skills, not this meta-skill.**
