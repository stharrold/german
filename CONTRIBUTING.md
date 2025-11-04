# Contributing to German Language Learning Repository

Thank you for considering contributing to this project! This document provides guidelines for contributing code, documentation, and workflow improvements.

## Table of Contents

- [Official Claude Code Documentation](#official-claude-code-documentation)
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Documentation Requirements](#documentation-requirements)
- [Skill Development Guidelines](#skill-development-guidelines)
- [Pull Request Process](#pull-request-process)
- [Quality Standards](#quality-standards)

## Official Claude Code Documentation

**IMPORTANT:** This workflow system extends official Claude Code patterns. Always review official documentation when creating new skills or repositories.

### Official Documentation Sources

**Claude Code Skills:**
- **Specification:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- **Building Agents:** https://docs.claude.com/en/docs/agents-and-tools/building-agents
- **Getting Started:** https://docs.claude.com/en/docs/claude-code/getting-started
- **Docs Map:** https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md

### Relationship to Official Patterns

This workflow system implements an extended skill architecture optimized for multi-phase development workflows. Key differences:

| Aspect | Official Pattern | This Workflow | Rationale |
|--------|------------------|---------------|-----------|
| **File structure** | `skill.md`, `README.md` | `SKILL.md`, `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `ARCHIVED/` | More context for Claude Code, version tracking, archival |
| **Frontmatter** | Simple YAML (name, description) | Extended YAML (version, triggers, description) | Version control, orchestrator integration |
| **Organization** | Flat structure | `scripts/`, `templates/` subdirs | Separates code from documentation |
| **Integration** | Standalone skills | Phase-based coordination | Workflow orchestrator manages skill loading |
| **Loading** | All at once | Progressive per phase | Token efficiency (~600-900 vs 2,718 tokens) |

**Both patterns are valid.** This system uses extended patterns for workflow-specific benefits while maintaining compatibility with core Claude Code concepts.

### When Creating New Skills

**Always start with official documentation:**

1. **Use the skill creation script:**
   ```bash
   python .claude/skills/workflow-utilities/scripts/create_skill.py <skill-name>
   ```

2. **The script automatically:**
   - Fetches official Claude Code documentation
   - Compares local patterns with official best practices
   - Alerts you to discrepancies with citations
   - Generates skill files following local patterns (after confirmation)

3. **Review discrepancies:**
   - Local patterns are optimized for this multi-phase workflow
   - Official patterns are general-purpose Claude Code patterns
   - Choose local practices if they provide value for the workflow
   - Document rationale for divergence in skill's `SKILL.md`

See [Skill Development Guidelines](#skill-development-guidelines) for complete details.

## Code of Conduct

This project follows a professional and respectful code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize technical accuracy and truthfulness
- Welcome contributions from all skill levels

## Getting Started

### Prerequisites

Ensure you have the required tools installed:

```bash
# Required
gh --version          # GitHub CLI (for authentication)
uv --version          # Python package manager
git --version         # Version control
python3 --version     # Python 3.11+

# Optional
podman --version      # Container operations
```

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   gh repo fork stharrold/german --clone
   cd german
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Authenticate with GitHub:**
   ```bash
   gh auth login
   ```

4. **Create your contrib branch:**
   ```bash
   GH_USER=$(gh api user --jq '.login')
   git checkout -b "contrib/$GH_USER"
   git push -u origin "contrib/$GH_USER"
   ```

## Development Workflow

This repository uses a **skill-based workflow** with 6 phases. See [WORKFLOW.md](WORKFLOW.md) for complete details.

### Protected Branches

**CRITICAL:** Before contributing, understand that `main` and `develop` are **protected branches**.

**Rules (MUST follow):**

1. ❌ **Never delete** `main` or `develop`
   - These branches are permanent
   - Deleting them breaks the entire workflow

2. ❌ **Never commit directly** to `main` or `develop`
   - All changes must go through pull requests
   - Direct commits bypass review and quality gates
   - Use worktrees to isolate your work

3. ✅ **Only merge via pull requests**
   - Feature → contrib (PR required)
   - Contrib → develop (PR required)
   - Release → main (PR required)

**What happens if you violate these rules?**

See [WORKFLOW.md "Branch Protection Policy"](WORKFLOW.md#branch-protection-policy) for:
- Recovery procedures if you accidentally commit to protected branches
- How to undo accidental commits
- How to recreate deleted branches
- When to ask for help

**Technical enforcement (recommended):**

Install the pre-push hook to prevent accidents:
```bash
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Repository maintainers should configure GitHub branch protection rules (see `.github/BRANCH_PROTECTION.md`).

### Quick Start

1. **Plan your feature** (Phase 1):
   ```bash
   # From main repo on contrib branch
   python .claude/skills/bmad-planner/scripts/create_planning.py \
     my-feature $GH_USER
   ```

2. **Create feature worktree** (Phase 2):
   ```bash
   python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
     feature my-feature contrib/$GH_USER
   ```

3. **Create specifications**:
   ```bash
   # From worktree
   cd ../german_feature_my-feature
   python .claude/skills/speckit-author/scripts/create_specifications.py \
     feature my-feature $GH_USER \
     --todo-file ../TODO_feature_*.md
   ```

4. **Implement and test** (ensure ≥80% coverage)

5. **Run quality gates** (Phase 3):
   ```bash
   python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
   ```

6. **Create pull request** (Phase 4)

See the [WORKFLOW.md](WORKFLOW.md) for detailed phase-by-phase instructions.

## Documentation Requirements

**CRITICAL: All skill changes require documentation updates.**

### When to Update Documentation

Update documentation when you:
- Modify a skill's Python script
- Add/remove features from a skill
- Change a skill's interactive Q&A flow
- Update templates used by a skill
- Modify skill integration with other skills
- Update performance or token efficiency metrics

### Documentation Update Checklist

**Use the comprehensive checklist:**
```bash
# Review the complete checklist before making changes
cat .claude/skills/UPDATE_CHECKLIST.md
```

**Minimum required updates:**

1. **Skill's SKILL.md** - Update version, commands, integration
2. **Skill's CLAUDE.md** - Update usage examples
3. **Skill's CHANGELOG.md** - Add version entry
4. **WORKFLOW.md** - Update affected phase sections
5. **Root CLAUDE.md** - Update command reference

**Validation:**
```bash
# Validate version consistency (once created)
python .claude/skills/workflow-utilities/scripts/validate_versions.py
```

### Semantic Versioning for Skills

Skills use semantic versioning: `MAJOR.MINOR.PATCH`

**MAJOR (X.0.0):**
- Breaking changes to skill API
- Removed features or parameters
- Incompatible workflow changes

**MINOR (x.Y.0):**
- New features (backward compatible)
- Enhanced capabilities
- New parameters (with defaults)

**PATCH (x.y.Z):**
- Bug fixes
- Documentation improvements
- Performance optimizations (no behavior change)

## Skill Development Guidelines

### Creating a New Skill

**RECOMMENDED:** Use the automated skill creation script that fetches official documentation and validates patterns.

#### Automated Approach (Recommended)

```bash
# Create new skill with official docs validation
python .claude/skills/workflow-utilities/scripts/create_skill.py <skill-name>
```

**The script will:**
1. Ask configuration questions (purpose, phase integration, components)
2. **Fetch official Claude Code documentation** automatically
3. **Compare local patterns with official best practices**
4. **Alert you to discrepancies with citations** (URLs provided)
5. Generate all required files (SKILL.md, CLAUDE.md, README.md, etc.)
6. Commit changes with proper semantic message

**Example:**
```bash
python .claude/skills/workflow-utilities/scripts/create_skill.py my-new-skill

=== Phase 1: Skill Configuration ===
Skill name: my-new-skill
Purpose: [Select from options]
...

=== Phase 2: Official Documentation Review ===
ℹ Fetching official Claude Code documentation...
✓ Official documentation fetched

⚠️  DISCREPANCY ALERT

[INFO] file_structure
  Local:    ['SKILL.md', 'CLAUDE.md', 'README.md', 'CHANGELOG.md', 'ARCHIVED/']
  Official: ['skill.md', 'README.md']
  Citation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills

  Rationale: Local pattern provides additional context for Claude Code...

Continue with local practices? (Y/n) > y

=== Phase 3: File Generation ===
[Files created automatically]
```

**Benefits:**
- ✓ Ensures alignment with official docs
- ✓ Validates local patterns with citations
- ✓ Documents rationale for divergences
- ✓ Saves ~800 tokens + time
- ✓ Consistent file structure

#### Manual Approach (If Needed)

If you need to create a skill manually:

1. **Review official documentation first:**
   - https://docs.claude.com/en/docs/agents-and-tools/agent-skills
   - Note any differences from local patterns

2. **Create skill directory structure:**
   ```bash
   .claude/skills/my-skill/
   ├── scripts/
   │   ├── __init__.py
   │   └── my_script.py
   ├── templates/           # If applicable
   │   └── template.md.template
   ├── SKILL.md             # Complete documentation
   ├── CLAUDE.md            # Claude Code context
   ├── README.md            # Human-readable overview
   ├── CHANGELOG.md         # Version history
   └── ARCHIVED/            # Deprecated files
       ├── CLAUDE.md
       └── README.md
   ```

3. **Create SKILL.md with YAML frontmatter:**
   ```yaml
   ---
   name: my-skill
   version: 1.0.0
   description: |
     Brief description of what this skill does.

     Use when: [context when to use]

     Triggers: [keywords that trigger this skill]
   ---
   ```

4. **Document alignment with official docs:**
   - Add "Official Documentation Alignment" section to SKILL.md
   - List any discrepancies with official patterns
   - Provide rationale and citations

3. **Follow coding standards:**
   - Use type hints
   - Include docstrings
   - Add error handling with helpful messages
   - Document constants with rationale
   - Clean up artifacts on failure

4. **Add to workflow-orchestrator:**
   - Update orchestrator to call your skill at appropriate phase
   - Update WORKFLOW.md with new phase or skill reference

### Modifying Existing Skills

**Always use the UPDATE_CHECKLIST:**

```bash
# Review checklist
cat .claude/skills/UPDATE_CHECKLIST.md

# Common updates:
# 1. Update script in scripts/
# 2. Bump version in SKILL.md frontmatter
# 3. Update SKILL.md documentation
# 4. Update CLAUDE.md examples
# 5. Update WORKFLOW.md phase sections
# 6. Add CHANGELOG.md entry
# 7. Validate consistency
# 8. Commit with semantic message
```

### Interactive Tool Best Practices

If creating an interactive callable tool (like BMAD or SpecKit):

1. **Use clear prompts:**
   ```python
   def ask_question(prompt: str, options: Optional[List[str]] = None):
       print(f"\n{prompt}")
       if options:
           for i, option in enumerate(options, 1):
               print(f"  {i}) {option}")
   ```

2. **Provide defaults:**
   ```python
   response = ask_question("Database?",
                          options=["SQLite", "PostgreSQL", "None"],
                          default="SQLite")
   ```

3. **Validate input:**
   ```python
   while True:
       response = input("> ").strip()
       if response.isdigit() and 0 <= int(response) - 1 < len(options):
           return options[int(response) - 1]
       print("Invalid selection. Please try again.")
   ```

4. **Handle errors gracefully:**
   ```python
   try:
       result = subprocess.run(cmd, check=True, capture_output=True)
   except subprocess.CalledProcessError as e:
       error_exit(f"Command failed: {cmd}\n{e.stderr}")
   ```

## Pull Request Process

### Before Submitting a PR

1. **Run quality gates:**
   ```bash
   # From feature worktree
   python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
   ```

2. **Verify all quality gates pass:**
   - ✓ Test coverage ≥ 80%
   - ✓ All tests passing
   - ✓ Linting clean (ruff)
   - ✓ Type checking clean (mypy)
   - ✓ Build successful

3. **Update documentation** (use UPDATE_CHECKLIST.md)

4. **Validate version consistency:**
   ```bash
   python .claude/skills/workflow-utilities/scripts/validate_versions.py
   ```

### PR Title Format

Use semantic commit message format:

```
<type>(<scope>): <subject>

Examples:
feat(vocab): add A1 certificate vocabulary
fix(bmad): correct template placeholder regex
docs(workflow): update Phase 2 SpecKit instructions
refactor(quality): extract coverage check to separate function
test(git): add worktree creation edge cases
chore(deps): update uv dependencies
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### PR Description Template

```markdown
## Summary
[Brief description of changes]

## Changes
- Change 1
- Change 2
- Change 3

## Documentation Updates
- [ ] SKILL.md version bumped
- [ ] CLAUDE.md examples updated
- [ ] WORKFLOW.md phase sections updated
- [ ] CHANGELOG.md entry added
- [ ] Root CLAUDE.md updated (if applicable)

## Quality Gates
- Coverage: XX% (✓ ≥80%)
- Tests: XX/XX passing (✓)
- Linting: Clean (✓)
- Types: Clean (✓)
- Build: Success (✓)

## Semantic Version
Recommended: vX.Y.Z (TYPE - rationale)

## Testing
[Description of testing performed]

## References
- TODO: TODO_feature_YYYYMMDDTHHMMSSZ_slug.md
- Spec: specs/slug/spec.md
- Plan: specs/slug/plan.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Review Process

1. **Self-review:**
   - Review your own PR before requesting review
   - Check for any debug code, print statements, or TODOs
   - Verify commit messages follow format

2. **Address feedback:**
   - Respond to all review comments
   - Push fixes as new commits (don't force push)
   - Mark conversations as resolved

3. **Merge:**
   - Merges are performed in GitHub UI
   - Squash commits if requested
   - Delete feature branch after merge

## Quality Standards

### Code Quality

**Required:**
- ✓ Type hints on all functions
- ✓ Docstrings on all public functions
- ✓ Error handling with helpful messages
- ✓ Constants documented with rationale
- ✓ No hardcoded values (use constants)
- ✓ Clean up artifacts on failure

**Example:**
```python
def ask_question(prompt: str, options: Optional[List[str]] = None,
                 default: Optional[str] = None) -> str:
    """Ask user a question and return response.

    Args:
        prompt: Question to ask user
        options: Optional list of choices
        default: Default value if user presses Enter

    Returns:
        User's response or default value

    Raises:
        ValueError: If response is invalid
    """
    # Implementation
```

### Test Coverage

**Requirement: ≥80% coverage**

```bash
# Run with coverage
uv run pytest --cov=src --cov-report=term --cov-fail-under=80

# View HTML report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Test structure:**
```
tests/
├── test_models.py          # Unit tests for models
├── test_vocabulary.py      # Unit tests for vocabulary module
├── test_loader.py          # Unit tests for loader
└── integration/            # Integration tests
    └── test_workflow.py
```

### Linting and Formatting

**Required: Clean linting**

```bash
# Check linting
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Type Checking

**Required: Clean type checking**

```bash
# Check types
uv run mypy src/
```

## Common Scenarios

### Scenario 1: Adding a German Vocabulary Module

```bash
# 1. Plan
python .claude/skills/bmad-planner/scripts/create_planning.py \
  vocab-b1 $GH_USER

# 2. Create worktree
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature vocab-b1 contrib/$GH_USER

# 3. Switch to worktree
cd ../german_feature_vocab-b1

# 4. Create spec
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature vocab-b1 $GH_USER \
  --todo-file ../TODO_feature_*.md

# 5. Implement
# - Add src/vocabulary/b1.py
# - Add tests/test_b1_vocabulary.py
# - Add resources/vocabulary/b1_nouns.json

# 6. Test
uv run pytest --cov=src --cov-report=term --cov-fail-under=80

# 7. Quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# 8. Create PR
gh pr create --base "contrib/$GH_USER" --head "feature/..."
```

### Scenario 2: Updating BMAD Planner Script

```bash
# 1. Review update checklist
cat .claude/skills/UPDATE_CHECKLIST.md

# 2. Modify script
vim .claude/skills/bmad-planner/scripts/create_planning.py

# 3. Determine version bump (e.g., 5.0.0 → 5.1.0 for new feature)

# 4. Update SKILL.md version and documentation
vim .claude/skills/bmad-planner/SKILL.md

# 5. Update CLAUDE.md examples
vim .claude/skills/bmad-planner/CLAUDE.md

# 6. Update WORKFLOW.md Phase 1 section
vim WORKFLOW.md

# 7. Update root CLAUDE.md
vim CLAUDE.md

# 8. Create CHANGELOG entry
vim .claude/skills/bmad-planner/CHANGELOG.md

# 9. Validate
python .claude/skills/workflow-utilities/scripts/validate_versions.py

# 10. Test
python .claude/skills/bmad-planner/scripts/create_planning.py test-feature $GH_USER --no-commit

# 11. Commit
git add .
git commit -m "feat(bmad): add new Q&A feature

Updated bmad-planner from v5.0.0 to v5.1.0:
- Added X feature
- Enhanced Y capability

Updated documentation:
- .claude/skills/bmad-planner/SKILL.md (version 5.1.0)
- WORKFLOW.md (Phase 1 section)

Refs: .claude/skills/bmad-planner/CHANGELOG.md
"
```

### Scenario 3: Adding a Hotfix

```bash
# 1. Create hotfix worktree (from main, not contrib)
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix critical-bug main

# 2. Switch to worktree
cd ../german_hotfix_critical-bug

# 3. Implement minimal fix
# - Fix the bug
# - Add regression test

# 4. Quality gates (required ≥80% coverage)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# 5. Create PR to main
gh pr create --base "main" --head "hotfix/..."

# 6. After merge: tag and back-merge
python .claude/skills/git-workflow-manager/scripts/tag_release.py v1.3.0-hotfix.1 main
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py v1.3.0-hotfix.1 develop
```

## Getting Help

- **Workflow questions:** See [WORKFLOW.md](WORKFLOW.md)
- **Skill documentation:** See `.claude/skills/<skill-name>/SKILL.md`
- **Claude Code usage:** See [CLAUDE.md](CLAUDE.md)
- **Update process:** See [.claude/skills/UPDATE_CHECKLIST.md](.claude/skills/UPDATE_CHECKLIST.md)

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Thank you for contributing to this project! Your contributions help make German language learning resources better for everyone.

---

Last updated: 2025-10-24
Version: 1.0.0
