---
type: claude-code-directive
name: Workflow-SpecKit-BMAD-Skills
version: 5.2.0
date: 2025-10-23
status: production-ready
purpose: Modular skill-based git workflow with BMAD + SpecKit + Claude Code
execution-model: skill-based-progressive-disclosure
applies-to: Python applications with uv, Podman, pytest
architecture: 7 independent skills with orchestration
changelog: |
  v5.2.0 - Enhanced TODO.md with YAML frontmatter and references
  - TODO.md now includes YAML frontmatter with metadata
  - References all active TODO_*.md files with one-sentence descriptions
  - References last 10 archived TODO_*.md files with one-sentence descriptions
  - Improved workflow tracking and historical context
  v5.1.0 - Standardized worktree naming conventions
  - Worktree directories: <repo>_feature_<YYYYMMDDTHHMMSSZ>_<slug-with-hyphens>
  - Branch names: feature/<YYYYMMDDTHHMMSSZ>_<slug-with-hyphens>
  - Consistent timestamp format across all workflow types
  v5.0.0 - Complete rewrite as modular skills
  - Decomposed 2,718-line monolith into 7 skills (~2,300 total)
  - Progressive disclosure: load orchestrator + 1-2 relevant skills per phase
  - Token efficiency: ~300-900 tokens vs 2,718 all at once
  - Python/uv exclusive, Podman containers, pytest-cov
  - gh CLI for contributor handle extraction
  - Context management via /context and /init commands
---

# Claude Code Workflow v5.2: Skill-Based Architecture

## Directive for Claude Code

**YOU ARE CLAUDE CODE.** This directive instructs you to:

1. **Create 7 independent skills** in `.claude/skills/` following best practices
2. **Use progressive disclosure** - load orchestrator + relevant skills per phase
3. **Adapt to Python/uv projects** with Podman containerization
4. **Guide user interactively** with explicit confirmation at each step
5. **Maintain TODO.md manifest** with YAML frontmatter and cross-references

## Prerequisites Check

Before creating skills, verify:

```bash
# Required: gh CLI for GitHub username
if ! command -v gh &> /dev/null; then
  echo "ERROR: gh CLI not installed"
  echo "Install: https://cli.github.com/"
  exit 1
fi

# Required: uv for Python package management
if ! command -v uv &> /dev/null; then
  echo "ERROR: uv not installed"
  echo "Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

# Required: git repository
if ! git rev-parse --git-dir &> /dev/null 2>&1; then
  echo "ERROR: Not a git repository"
  echo "Run: git init"
  exit 1
fi

# Extract GitHub username
GH_USER=$(gh api user --jq '.login' 2>/dev/null)
if [ -z "$GH_USER" ]; then
  echo "ERROR: Not authenticated with GitHub"
  echo "Run: gh auth login"
  exit 1
fi

echo "Ã¢Å“â€œ Prerequisites satisfied"
echo "  GitHub User: $GH_USER"
echo "  Python: $(python3 --version)"
echo "  uv: $(uv --version)"
echo "  Podman: $(podman --version 2>/dev/null || echo 'not installed')"
```

---

## Skill Architecture Overview

```
.claude/skills/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ workflow-orchestrator/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~300 lines - main coordinator
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ templates/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ WORKFLOW.md.template
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ CLAUDE.md.template
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ TODO_template.md
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ tech-stack-adapter/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~200 lines - detects Python/uv/Podman
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ scripts/
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ detect_stack.py
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ git-workflow-manager/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~500 lines - git operations
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ scripts/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ create_worktree.py
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ daily_rebase.py
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ semantic_version.py
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ bmad-planner/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~400 lines - requirements in main repo
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ templates/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ requirements.md.template
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ architecture.md.template
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ speckit-author/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~400 lines - specs in worktrees
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ templates/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ spec.md.template
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ plan.md.template
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ quality-enforcer/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~300 lines - tests, coverage, versioning
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ scripts/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ check_coverage.py
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ run_quality_gates.py
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ helper-functions/
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ SKILL.md                    # ~200 lines - shared utilities
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ scripts/
        Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ deprecate_files.py
        Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ archive_manager.py
        Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ todo_updater.py
        Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ directory_structure.py
```

**Total: ~2,300 lines across 7 skills vs 2,718 in monolith**

**Token efficiency:**
- Initial load: orchestrator (~300 tokens)
- Per phase: orchestrator + 1-2 relevant skills (~600-900 tokens)
- Previous: entire 2,718 lines loaded always

---

## Skill 1: workflow-orchestrator

**File: `.claude/skills/workflow-orchestrator/SKILL.md`**

```markdown
---
name: workflow-orchestrator
version: 5.1.0
description: |
  Orchestrates git workflow for Python feature/release/hotfix development.
  Loads and coordinates other skills based on current context.
  
  Use when: 
  - User says "next step?" or "continue workflow"
  - Working in git repo with TODO_[feature|release|hotfix]_*.md files
  - Need to determine workflow phase and load appropriate skills
  
  Triggers: next step, continue, what's next, workflow status
  
  Coordinates: tech-stack-adapter, git-workflow-manager, bmad-planner,
  speckit-author, quality-enforcer, helper-functions
  
  Context management: Prompt user to run /context when context usage
  is high, then /init to reset before continuing workflow.
---

# Workflow Orchestrator

## Purpose

Main coordinator for multi-branch git workflow. Detects current context
and loads appropriate skills dynamically.

## Context Detection Algorithm

```python
def detect_context():
    """Determine current workflow phase and required skills."""
    import os
    from pathlib import Path
    
    # Get repository info
    repo_root = Path(os.popen('git rev-parse --show-toplevel').read().strip())
    current_dir = Path.cwd()
    current_branch = os.popen('git branch --show-current').read().strip()
    
    # Determine if in worktree
    is_worktree = current_dir != repo_root
    
    # Find TODO file
    if is_worktree:
        # Look for TODO in parent (main repo)
        todo_pattern = '../TODO_*.md'
        import glob
        todos = glob.glob(str(current_dir / todo_pattern))
        if todos:
            todo_file = Path(todos[0]).name
            workflow_type = todo_file.split('_')[1]  # feature|release|hotfix
        else:
            return None, None, None
    else:
        # In main repo
        import glob
        todos = glob.glob(str(repo_root / 'TODO_*.md'))
        if todos:
            todo_file = Path(todos[0]).name
            workflow_type = todo_file.split('_')[1]
        else:
            workflow_type = None
            todo_file = None
    
    return {
        'repo_root': repo_root,
        'current_dir': current_dir,
        'current_branch': current_branch,
        'is_worktree': is_worktree,
        'workflow_type': workflow_type,
        'todo_file': todo_file
    }
```

## Skill Loading Logic

When user says "next step?":

1. **Always load tech-stack-adapter first (once per session)**
   ```
   Read tech-stack-adapter/SKILL.md
   Execute: python tech-stack-adapter/scripts/detect_stack.py
   Store: TEST_CMD, BUILD_CMD, COVERAGE_CMD, etc.
   ```

2. **Detect context and load appropriate skills**
   ```python
   context = detect_context()
   
   if context['is_worktree']:
       # In feature/release/hotfix worktree
       if context['workflow_type'] in ['feature', 'release', 'hotfix']:
           load_skill('speckit-author')  # For spec.md, plan.md
           load_skill('git-workflow-manager')  # For commits, pushes
   else:
       # In main repo on contrib branch
       if 'contrib' in context['current_branch']:
           load_skill('bmad-planner')  # For requirements, architecture
           load_skill('git-workflow-manager')  # For branch operations
   
   # Always available for quality checks
   load_skill('quality-enforcer')  # When running tests, checking coverage
   load_skill('helper-functions')  # For utilities
   ```

3. **Parse TODO file to determine current step**
   ```python
   import yaml
   from pathlib import Path
   
   def parse_todo_file(todo_path):
       """Extract workflow progress from TODO file."""
       content = Path(todo_path).read_text()
       
       # Extract YAML frontmatter
       if content.startswith('---'):
           parts = content.split('---', 2)
           frontmatter = yaml.safe_load(parts[1])
           body = parts[2]
       else:
           return None
       
       return {
           'workflow_progress': frontmatter.get('workflow_progress', {}),
           'quality_gates': frontmatter.get('quality_gates', {}),
           'metadata': frontmatter.get('metadata', {})
       }
   ```

## TODO.md Manifest Structure (v5.2)

The root `TODO.md` file maintains master workflow tracking with YAML frontmatter:

```markdown
---
manifest_version: 5.2.0
last_updated: 2025-10-23T14:30:22Z
repository: json-validator
active_workflows:
  count: 2
  updated: 2025-10-23T14:30:22Z
archived_workflows:
  count: 45
  last_archived: 2025-10-22T09:15:00Z
---

# Workflow Manifest

## Active Workflows

### TODO_feature_20251023T143022Z_json-validator.md
Implements JSON schema validation service with SQLite persistence and REST API endpoints.

### TODO_release_20251020T091500Z_v1-1-0.md
Prepares v1.1.0 release with JSON validator feature, updated documentation, and migration guide.

## Recently Archived Workflows (Last 10)

### ARCHIVED_TODO_feature_20251022T103000Z_auth-service.md
Added JWT-based authentication service with token refresh and role-based access control.

### ARCHIVED_TODO_hotfix_20251021T154500Z_db-connection-leak.md
Fixed database connection leak in SQLAlchemy session management that caused memory growth.

[... 8 more archived workflows ...]

## Workflow Commands

- **Create feature**: `next step?` (from contrib branch)
- **Continue workflow**: `next step?` (from any context)
- **Check quality gates**: Tests, coverage, linting, type checking
- **Create PR**: Automatic after all gates pass
- **View status**: Check current phase in active TODO_*.md files

## Archive Management

Workflows are archived when:
- Feature/hotfix PR merged to contrib branch
- Release PR merged to develop branch
- Contributor manually archives with `archive workflow` command

Archive process:
1. Move TODO_*.md → ARCHIVED_TODO_*.md
2. Update timestamp in filename
3. Create zip of all related files (spec.md, plan.md, logs)
4. Update TODO.md manifest references
5. Commit archive changes to main repo
```

## TODO.md Update Logic

The `helper-functions/scripts/todo_updater.py` maintains TODO.md:

```python
#!/usr/bin/env python3
"""Maintain TODO.md manifest with active and archived workflow references."""

import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def get_active_todos(repo_root: Path) -> List[Dict]:
    """Scan for active TODO_*.md files (not archived)."""
    todos = []
    for todo_file in sorted(repo_root.glob('TODO_*.md')):
        if 'ARCHIVED' not in todo_file.name:
            # Read first non-YAML line as description
            content = todo_file.read_text()
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body_lines = [l.strip() for l in parts[2].strip().split('\n') 
                             if l.strip() and not l.startswith('#')]
                description = body_lines[0] if body_lines else "No description available."
            else:
                description = "No description available."
            
            todos.append({
                'filename': todo_file.name,
                'description': description,
                'modified': datetime.fromtimestamp(todo_file.stat().st_mtime)
            })
    return todos

def get_archived_todos(repo_root: Path, limit: int = 10) -> List[Dict]:
    """Get last N archived TODO files by modification time."""
    archived = []
    for todo_file in repo_root.glob('ARCHIVED_TODO_*.md'):
        content = todo_file.read_text()
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body_lines = [l.strip() for l in parts[2].strip().split('\n') 
                         if l.strip() and not l.startswith('#')]
            description = body_lines[0] if body_lines else "No description available."
        else:
            description = "No description available."
        
        archived.append({
            'filename': todo_file.name,
            'description': description,
            'modified': datetime.fromtimestamp(todo_file.stat().st_mtime)
        })
    
    # Sort by modification time, most recent first
    archived.sort(key=lambda x: x['modified'], reverse=True)
    return archived[:limit]

def update_todo_manifest(repo_root: Path):
    """Update TODO.md with current active and archived workflows."""
    active_todos = get_active_todos(repo_root)
    archived_todos = get_archived_todos(repo_root, limit=10)
    
    # Build frontmatter
    frontmatter = {
        'manifest_version': '5.2.0',
        'last_updated': datetime.now().isoformat() + 'Z',
        'repository': repo_root.name,
        'active_workflows': {
            'count': len(active_todos),
            'updated': datetime.now().isoformat() + 'Z'
        },
        'archived_workflows': {
            'count': len(list(repo_root.glob('ARCHIVED_TODO_*.md'))),
            'last_archived': archived_todos[0]['modified'].isoformat() + 'Z' if archived_todos else None
        }
    }
    
    # Build content sections
    content = ['---']
    content.append(yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip())
    content.append('---')
    content.append('')
    content.append('# Workflow Manifest')
    content.append('')
    
    # Active workflows
    content.append('## Active Workflows')
    content.append('')
    if active_todos:
        for todo in active_todos:
            content.append(f"### {todo['filename']}")
            content.append(todo['description'])
            content.append('')
    else:
        content.append('*No active workflows*')
        content.append('')
    
    # Archived workflows
    content.append('## Recently Archived Workflows (Last 10)')
    content.append('')
    if archived_todos:
        for todo in archived_todos:
            content.append(f"### {todo['filename']}")
            content.append(todo['description'])
            content.append('')
    else:
        content.append('*No archived workflows*')
        content.append('')
    
    # Commands section
    content.extend([
        '## Workflow Commands',
        '',
        '- **Create feature**: `next step?` (from contrib branch)',
        '- **Continue workflow**: `next step?` (from any context)',
        '- **Check quality gates**: Tests, coverage, linting, type checking',
        '- **Create PR**: Automatic after all gates pass',
        '- **View status**: Check current phase in active TODO_*.md files',
        '',
        '## Archive Management',
        '',
        'Workflows are archived when:',
        '- Feature/hotfix PR merged to contrib branch',
        '- Release PR merged to develop branch',
        '- Contributor manually archives with `archive workflow` command',
        '',
        'Archive process:',
        '1. Move TODO_*.md → ARCHIVED_TODO_*.md',
        '2. Update timestamp in filename',
        '3. Create zip of all related files (spec.md, plan.md, logs)',
        '4. Update TODO.md manifest references',
        '5. Commit archive changes to main repo',
    ])
    
    # Write TODO.md
    todo_md = repo_root / 'TODO.md'
    todo_md.write_text('\n'.join(content))
    print(f"✅ Updated {todo_md}")
    print(f"   Active: {len(active_todos)}")
    print(f"   Archived (shown): {len(archived_todos)}")

if __name__ == '__main__':
    import sys
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    update_todo_manifest(repo_root)
```

## Integration with Archive Process

When archiving a workflow, update TODO.md automatically:

```python
# In helper-functions/scripts/archive_manager.py
def archive_workflow(todo_file: Path):
    """Archive completed workflow and update manifest."""
    # ... existing archive logic ...
    
    # Update TODO.md manifest
    from todo_updater import update_todo_manifest
    update_todo_manifest(todo_file.parent)
    
    print(f"✅ Archived {todo_file.name}")
    print(f"✅ Updated TODO.md manifest")
```

4. **Prompt user with next step**
   ```
   Next step from workflow:
   Phase <N>, Step <N.M>: <description>
   
   This will:
   - <action 1>
   - <action 2>
   - <action 3>
   
   Would you like to proceed? (Y/n)
   ```

5. **Wait for explicit "Y" confirmation**
   - Do NOTHING until user confirms
   - If "n", wait for next instruction

6. **Execute step using loaded skills**
   - Call appropriate skill methods
   - Update TODO file via helper-functions
   - Commit changes via git-workflow-manager

## TODO File Schema

Every TODO_[feature|release|hotfix]_<timestamp>_<slug>.md contains:

```yaml
---
type: workflow-manifest
workflow_type: feature  # or release, hotfix
slug: json-validator
timestamp: 20251022T143022Z
github_user: <gh-username>

metadata:
  title: "JSON Schema Validator Service"
  description: "Containerized Python service for JSON validation"
  created: "2025-10-22T14:30:22Z"
  worktree_dir: "json-validator_feature_20251022T143022Z_json-validator"
  branch_name: "feature/20251022T143022Z_json-validator"
  stack: python
  package_manager: uv
  test_framework: pytest
  containers: [app, sqlite]

workflow_progress:
  phase: 2
  current_step: "2.3"
  last_task: "impl_002"
  last_update: "2025-10-22T15:45:10Z"
  status: "implementation"

quality_gates:
  test_coverage: 80
  tests_passing: true
  build_successful: true
  semantic_version: "1.1.0"

tasks:
  planning:
    - id: plan_001
      description: "Create requirements.md"
      status: complete
      completed_at: "2025-10-22T14:35:00Z"
  
  specification:
    - id: spec_001
      description: "Write spec.md with API contracts"
      status: complete
      completed_at: "2025-10-22T14:50:00Z"
  
  implementation:
    - id: impl_001
      description: "Database schema with SQLite"
      status: complete
      completed_at: "2025-10-22T15:15:00Z"
    
    - id: impl_002
      description: "JSON validator core logic"
      status: complete
      completed_at: "2025-10-22T15:45:00Z"
    
    - id: impl_003
      description: "REST API with FastAPI"
      status: pending
  
  testing:
    - id: test_001
      description: "Unit tests for validator"
      status: pending
    
    - id: test_002
      description: "Integration tests with SQLite"
      status: pending
  
  containerization:
    - id: container_001
      description: "Containerfile for app"
      status: pending
    
    - id: container_002
      description: "Containerfile for SQLite"
      status: pending
    
    - id: container_003
      description: "podman-compose.yml"
      status: pending
---

# {Workflow Type}: {Title}

{One-sentence summary for TODO.md manifest - this should concisely describe what the workflow accomplishes}

## Active Tasks

### impl_003: REST API with FastAPI
**Status:** pending
**Files:** src/api/main.py, src/api/routes.py
**Dependencies:** impl_001, impl_002

... (rest of TODO body)
```

## Workflow Phases

### Phase 0: Initial Setup
1. Verify prerequisites (gh CLI, uv, git)
2. Create .claude/skills/ directory structure
3. Generate workflow files (WORKFLOW.md, CLAUDE.md, README.md)
4. Initialize contrib/<gh-user> branch

**Skills loaded:** tech-stack-adapter, git-workflow-manager, helper-functions

### Phase 1: Planning (Main Repo)
1. Create BMAD planning documents
2. Define requirements and architecture

**Skills loaded:** bmad-planner, helper-functions

### Phase 2: Feature Development (Worktree)
1. Create feature worktree
2. Write SpecKit specifications
3. Implement code
4. Write tests
5. Create containers

**Skills loaded:** speckit-author, git-workflow-manager, quality-enforcer, helper-functions

### Phase 3: Quality Assurance
1. Run tests with coverage
2. Validate quality gates
3. Calculate semantic version

**Skills loaded:** quality-enforcer, helper-functions

### Phase 4: Integration
1. Create PR from feature Ã¢â€ â€™ contrib/<gh-user>
2. User merges PR in GitHub UI
3. Rebase contrib/<gh-user> onto develop
4. Create PR from contrib/<gh-user> Ã¢â€ â€™ develop

**Skills loaded:** git-workflow-manager

### Phase 5: Release (Worktree)
1. Create release worktree from develop
2. Final QA and documentation
3. Create PR to main
4. Tag release after merge

**Skills loaded:** git-workflow-manager, quality-enforcer

## Context Management

**CRITICAL:** Monitor context usage throughout workflow.

```python
def check_context_usage():
    """
    User must manually check via /context command.
    When approaching limits, prompt user to:
    1. Save TODO file state
    2. Run /init to reset context
    3. Continue workflow
    """
    print("\nÃ¢Å¡Â Ã¯Â¸Â  Context Usage Check")
    print("Run: /context")
    print("If usage > 50%, then:")
    print("  1. I'll update TODO file with current state")
    print("  2. Run: /init")
    print("  3. Say 'next step?' to continue")
```

**Prompt user periodically:**
```
Current task: <task_id>
Please run: /context

If context usage > 50%:
  I'll save state to TODO file, then you run /init
```

## Interactive Confirmation Pattern

```python
def prompt_for_confirmation(step_info):
    """Always wait for explicit Y before proceeding."""
    print(f"\nNext step from workflow:")
    print(f"Step {step_info['phase']}.{step_info['step']}: {step_info['description']}")
    print(f"\nThis will:")
    for action in step_info['actions']:
        print(f"  - {action}")
    print(f"\nWould you like to proceed with Step {step_info['phase']}.{step_info['step']}? (Y/n)")
    
    # WAIT for user response - do NOT proceed automatically
    # Only continue if user types "Y"
```

## Templates Location

See `templates/` subdirectory for:
- WORKFLOW.md.template (comprehensive workflow guide)
- CLAUDE.md.template (interaction guide)
- TODO_template.md (manifest structure)

## Directory Standards

**Every directory must have:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (except ARCHIVED itself)

Use helper-functions/scripts/directory_structure.py to create compliant directories.

## Key Behaviors

Ã¢Å“â€œ Load orchestrator first, then relevant skills per phase
Ã¢Å“â€œ Always wait for "Y" confirmation
Ã¢Å“â€œ Monitor context via /context command
Ã¢Å“â€œ Save state and /init when context > 50%
Ã¢Å“â€œ Update TODO file after each step
Ã¢Å“â€œ Commit changes with descriptive messages
Ã¢Å“â€œ Use helper-functions for shared utilities
```

---

## Skill 2: tech-stack-adapter

**File: `.claude/skills/tech-stack-adapter/SKILL.md`**

```markdown
---
name: tech-stack-adapter
version: 5.1.0
description: |
  Detects Python project configuration and provides commands for
  testing, building, coverage, and containerization.
  
  Use when: Starting workflow, detecting project stack, need TEST_CMD
  
  Triggers: detect stack, what commands, initial setup
  
  Outputs: TEST_CMD, BUILD_CMD, COVERAGE_CMD, COVERAGE_CHECK, MIGRATE_CMD
---

# Tech Stack Adapter

## Purpose

One-time detection of Python/uv project configuration. Returns standardized
commands for use throughout workflow.

## Detection Script

**File: `scripts/detect_stack.py`**

```python
#!/usr/bin/env python3
"""Detect Python project stack and generate commands."""

import json
import subprocess
from pathlib import Path
import tomli

def detect_stack():
    """Detect project configuration and return commands."""
    
    repo_root = Path(subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        text=True
    ).strip())
    
    # Verify pyproject.toml exists
    pyproject_path = repo_root / 'pyproject.toml'
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found - not a Python/uv project")
    
    # Parse pyproject.toml
    with open(pyproject_path, 'rb') as f:
        pyproject = tomli.load(f)
    
    project_name = pyproject.get('project', {}).get('name', 'unknown')
    
    # Check for pytest in dependencies
    dependencies = pyproject.get('project', {}).get('dependencies', [])
    dev_dependencies = pyproject.get('project', {}).get('optional-dependencies', {}).get('dev', [])
    all_deps = dependencies + dev_dependencies
    
    has_pytest = any('pytest' in dep for dep in all_deps)
    has_coverage = any('pytest-cov' in dep for dep in all_deps)
    
    # Check for database
    has_sqlalchemy = any('sqlalchemy' in dep for dep in all_deps)
    has_alembic = any('alembic' in dep for dep in all_deps)
    
    # Generate commands
    config = {
        'stack': 'python',
        'package_manager': 'uv',
        'project_name': project_name,
        'repo_root': str(repo_root),
        
        # Core commands
        'install_cmd': 'uv sync',
        'test_cmd': 'uv run pytest' if has_pytest else 'echo "No pytest configured"',
        'build_cmd': 'uv build',
        
        # Coverage commands
        'coverage_cmd': 'uv run pytest --cov=src --cov-report=term' if has_coverage else 'uv run pytest',
        'coverage_check': 'uv run pytest --cov=src --cov-report=term --cov-fail-under=80' if has_coverage else 'echo "No coverage tool"',
        
        # Database commands
        'database': 'sqlite' if not has_sqlalchemy else 'postgresql',
        'orm': 'none' if not has_sqlalchemy else 'sqlalchemy',
        'migrate_cmd': 'uv run alembic upgrade head' if has_alembic else 'echo "No migrations"',
        
        # Container
        'container': 'podman',
        'has_containerfile': (repo_root / 'Containerfile').exists(),
        'has_compose': (repo_root / 'podman-compose.yml').exists(),
        
        # Test framework details
        'test_framework': 'pytest' if has_pytest else 'none',
        'has_pytest_cov': has_coverage,
    }
    
    return config

if __name__ == '__main__':
    config = detect_stack()
    print(json.dumps(config, indent=2))
```

## Usage in Workflow

```bash
# Run once at workflow start
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py > /tmp/stack_config.json

# Access in other skills
export TEST_CMD=$(jq -r '.test_cmd' /tmp/stack_config.json)
export BUILD_CMD=$(jq -r '.build_cmd' /tmp/stack_config.json)
export COVERAGE_CHECK=$(jq -r '.coverage_check' /tmp/stack_config.json)
```

## Output Format

```json
{
  "stack": "python",
  "package_manager": "uv",
  "project_name": "json-validator",
  "repo_root": "/home/user/projects/json-validator",
  "install_cmd": "uv sync",
  "test_cmd": "uv run pytest",
  "build_cmd": "uv build",
  "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
  "coverage_check": "uv run pytest --cov=src --cov-report=term --cov-fail-under=80",
  "database": "sqlite",
  "orm": "sqlalchemy",
  "migrate_cmd": "uv run alembic upgrade head",
  "container": "podman",
  "has_containerfile": false,
  "has_compose": false,
  "test_framework": "pytest",
  "has_pytest_cov": true
}
```
```

---

## Skill 3: git-workflow-manager

**File: `.claude/skills/git-workflow-manager/SKILL.md`**

```markdown
---
name: git-workflow-manager
version: 5.1.0
description: |
  Manages git operations: worktree creation, branch management, commits,
  PRs, semantic versioning, and daily rebase workflow.
  
  Use when: Creating branches/worktrees, committing, pushing, versioning
  
  Triggers: create worktree, commit, push, rebase, version, PR
---

# Git Workflow Manager

## Purpose

Handles all git operations following git-flow + GitHub-flow hybrid model.

## Branch Structure

```
main                           Ã¢â€ Â Production (tagged vX.Y.Z)
  Ã¢â€ â€˜
release/vX.Y.Z                Ã¢â€ Â Release candidate
  Ã¢â€ â€˜
develop                        Ã¢â€ Â Integration branch
  Ã¢â€ â€˜
contrib/<gh-user>             Ã¢â€ Â Personal contribution branch
  Ã¢â€ â€˜
feature/<timestamp>_<slug>    Ã¢â€ Â Isolated feature (worktree)
hotfix/vX.Y.Z-hotfix.N       Ã¢â€ Â Production hotfix (worktree)
```

## Scripts

### create_worktree.py

```python
#!/usr/bin/env python3
"""Create feature/release/hotfix worktree with TODO file."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def create_worktree(workflow_type, slug, base_branch):
    """
    Args:
        workflow_type: 'feature' | 'release' | 'hotfix'
        slug: Short descriptive name (e.g., 'json-validator')
        base_branch: Branch to create from (e.g., 'contrib/username')
    """
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    branch_name = f"{workflow_type}/{timestamp}_{slug}"
    
    repo_root = Path(subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        text=True
    ).strip())
    
    worktree_path = repo_root.parent / f"{repo_root.name}_{workflow_type}_{timestamp}_{slug}"
    
    # Create worktree
    subprocess.run([
        'git', 'worktree', 'add',
        str(worktree_path),
        '-b', branch_name,
        base_branch
    ], check=True)
    
    # Create TODO file in main repo
    gh_user = subprocess.check_output(['gh', 'api', 'user', '--jq', '.login'], text=True).strip()
    todo_filename = f"TODO_{workflow_type}_{timestamp}_{slug}.md"
    todo_path = repo_root / todo_filename
    
    # Copy template and customize
    template = repo_root / '.claude' / 'skills' / 'workflow-orchestrator' / 'templates' / 'TODO_template.md'
    
    with open(template) as f:
        content = f.read()
    
    content = content.replace('{{WORKFLOW_TYPE}}', workflow_type)
    content = content.replace('{{SLUG}}', slug)
    content = content.replace('{{TIMESTAMP}}', timestamp)
    content = content.replace('{{GH_USER}}', gh_user)
    
    with open(todo_path, 'w') as f:
        f.write(content)
    
    print(f"Ã¢Å“â€œ Worktree created: {worktree_path}")
    print(f"Ã¢Å“â€œ Branch: {branch_name}")
    print(f"Ã¢Å“â€œ TODO file: {todo_filename}")
    
    return {
        'worktree_path': str(worktree_path),
        'branch_name': branch_name,
        'todo_file': todo_filename
    }

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: create_worktree.py <feature|release|hotfix> <slug> <base_branch>")
        sys.exit(1)
    
    result = create_worktree(sys.argv[1], sys.argv[2], sys.argv[3])
    import json
    print(json.dumps(result))
```

### daily_rebase.py

```python
#!/usr/bin/env python3
"""Perform daily rebase workflow."""

import subprocess
import sys

def daily_rebase(contrib_branch):
    """
    1. Checkout contrib branch
    2. Fetch origin
    3. Rebase onto origin/develop
    4. Force push with lease
    """
    print(f"Rebasing {contrib_branch} onto develop...")
    
    subprocess.run(['git', 'checkout', contrib_branch], check=True)
    subprocess.run(['git', 'fetch', 'origin'], check=True)
    subprocess.run(['git', 'rebase', 'origin/develop'], check=True)
    subprocess.run(['git', 'push', 'origin', contrib_branch, '--force-with-lease'], check=True)
    
    print(f"Ã¢Å“â€œ {contrib_branch} rebased onto develop")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: daily_rebase.py <contrib_branch>")
        sys.exit(1)
    
    daily_rebase(sys.argv[1])
```

### semantic_version.py

```python
#!/usr/bin/env python3
"""Calculate semantic version based on component changes."""

import subprocess
import re
from pathlib import Path

def get_changed_files(base_branch):
    """Get list of changed files compared to base."""
    result = subprocess.check_output(
        ['git', 'diff', '--name-only', base_branch],
        text=True
    )
    return result.strip().split('\n')

def analyze_changes(changed_files):
    """
    Determine version bump type:
    - MAJOR: Breaking changes (API changes, removed features)
    - MINOR: New features (new files, new functions)
    - PATCH: Bug fixes, refactoring, docs
    """
    has_breaking = False
    has_feature = False
    has_fix = False
    
    for file in changed_files:
        if file.startswith('src/api/'):
            # API changes are potentially breaking
            has_breaking = True
        elif file.startswith('src/') and file.endswith('.py'):
            # New Python files are features
            if Path(file).exists():
                has_feature = True
        elif file.startswith('tests/'):
            has_fix = True
        elif file.startswith('docs/'):
            has_fix = True
    
    if has_breaking:
        return 'major'
    elif has_feature:
        return 'minor'
    else:
        return 'patch'

def bump_version(current_version, bump_type):
    """Increment version based on bump type."""
    match = re.match(r'v?(\d+)\.(\d+)\.(\d+)', current_version)
    if not match:
        return 'v1.0.0'
    
    major, minor, patch = map(int, match.groups())
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    
    return f"v{major}.{minor}.{patch}"

def calculate_semantic_version(base_branch, current_version):
    """Calculate next semantic version."""
    changed_files = get_changed_files(base_branch)
    bump_type = analyze_changes(changed_files)
    new_version = bump_version(current_version, bump_type)
    
    print(f"Changed files: {len(changed_files)}")
    print(f"Bump type: {bump_type}")
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")
    
    return new_version

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: semantic_version.py <base_branch> <current_version>")
        sys.exit(1)
    
    new_version = calculate_semantic_version(sys.argv[1], sys.argv[2])
    print(new_version)
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

**Example:**
```
feat(validator): add JSON schema validation endpoint

Implements REST API endpoint for validating JSON against schemas.
Uses jsonschema library for validation logic.

Implements: impl_003
Spec: specs/json-validator/spec.md
Tests: tests/test_validator.py
Coverage: 85%

Refs: TODO_feature_20251022T143022Z_json-validator.md
```

## PR Creation

```bash
# Feature Ã¢â€ â€™ contrib/<gh-user>
gh pr create \
  --base "contrib/<gh-user>" \
  --head "<feature-branch>" \
  --title "feat: <description>" \
  --body "See TODO_feature_*.md for details"

# After user merges in GitHub UI:
# Contrib Ã¢â€ â€™ develop
gh pr create \
  --base "develop" \
  --head "contrib/<gh-user>" \
  --title "feat: <description>" \
  --body "Completed feature: <name>"
```
```

---

## Skill 4: bmad-planner

**File: `.claude/skills/bmad-planner/SKILL.md`**

```markdown
---
name: bmad-planner
version: 5.1.0
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

### requirements.md.template

```markdown
# Requirements: {{TITLE}}

**Date:** {{DATE}}
**Author:** {{GH_USER}}
**Status:** Draft

## Business Context

### Problem Statement
[What problem does this solve?]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Stakeholders
- **Primary:** [Who is this for?]
- **Secondary:** [Who else is impacted?]

## Functional Requirements

### FR-001: [Requirement Name]
**Priority:** High | Medium | Low
**Description:** [Detailed description]
**Acceptance Criteria:**
- [ ] AC 1
- [ ] AC 2

### FR-002: [Requirement Name]
...

## Non-Functional Requirements

### Performance
- Response time: < 200ms
- Throughput: 1000 req/s
- Concurrency: 100 simultaneous users

### Security
- Authentication: JWT tokens
- Authorization: Role-based access
- Data encryption: At rest and in transit

### Scalability
- Horizontal scaling: Yes
- Database sharding: Not required
- Cache strategy: Redis

## Constraints

- Technology: Python 3.11+, uv, Podman
- Budget: N/A
- Timeline: 2 weeks
- Dependencies: None

## Out of Scope

- [What we're NOT doing]
- [Future enhancements]

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High | [Strategy] |
| [Risk 2] | Med | [Strategy] |
```

### architecture.md.template

```markdown
# Architecture: {{TITLE}}

**Date:** {{DATE}}
**Author:** {{GH_USER}}
**Status:** Draft

## System Overview

### High-Level Architecture

\`\`\`
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â         Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š   Client    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬>Ã¢â€â€š   FastAPI    Ã¢â€â€š
Ã¢â€â€š  (JSON)     Ã¢â€â€š         Ã¢â€â€š   Service    Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ         Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
                               Ã¢â€â€š
                               Ã¢â€“Â¼
                        Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
                        Ã¢â€â€š   SQLite     Ã¢â€â€š
                        Ã¢â€â€š   Database   Ã¢â€â€š
                        Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
\`\`\`

### Components

1. **API Service (Python/FastAPI)**
   - Receives JSON validation requests
   - Applies schema validation rules
   - Stores validation history

2. **Database (SQLite)**
   - Schemas table
   - Validation_history table
   - Lightweight, file-based storage

3. **Containers (Podman)**
   - App container: Python service
   - DB container: SQLite with persistent volume

## Technology Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Validation:** jsonschema
- **Database:** SQLite + SQLAlchemy
- **Testing:** pytest, pytest-cov
- **Containers:** Podman + podman-compose
- **Package Manager:** uv

## Data Model

\`\`\`python
# schemas table
id: int (PK)
name: str
schema_json: json
version: int
created_at: datetime

# validation_history table
id: int (PK)
schema_id: int (FK)
input_json: json
valid: bool
errors: json
validated_at: datetime
\`\`\`

## API Design

### Endpoints

#### POST /validate
Validate JSON against a schema.

**Request:**
\`\`\`json
{
  "schema_name": "user-registration",
  "data": { ... }
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "valid": true,
  "schema_version": 1,
  "validated_at": "2025-10-22T15:30:00Z"
}
\`\`\`

**Response (400):**
\`\`\`json
{
  "valid": false,
  "errors": ["field 'email' is required"],
  "schema_version": 1
}
\`\`\`

#### POST /schemas
Create a new validation schema.

#### GET /schemas
List all schemas.

#### GET /schemas/{name}
Get specific schema.

## Container Architecture

### Containerfile (App)

\`\`\`dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY src/ src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]
\`\`\`

### podman-compose.yml

\`\`\`yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      DATABASE_URL: sqlite:////app/data/validator.db
    depends_on:
      - db

  db:
    image: alpine:latest
    volumes:
      - sqlite-data:/data
    command: sleep infinity

volumes:
  sqlite-data:
\`\`\`

## Security Considerations

- Input validation: Strict JSON schema validation
- SQL injection: Use SQLAlchemy parameterized queries
- Rate limiting: 100 requests/minute per IP
- CORS: Restrict origins in production

## Testing Strategy

- Unit tests: 80%+ coverage
- Integration tests: API endpoints with test DB
- Performance tests: Load testing with locust
- Container tests: Health checks, connectivity

## Deployment

- Development: Local Podman containers
- CI/CD: GitHub Actions
- Production: TBD (out of scope)

## Monitoring & Observability

- Health check: GET /health
- Metrics: Prometheus endpoint /metrics
- Logging: Structured JSON logs

## Open Questions

- [ ] Rate limiting implementation details
- [ ] Schema versioning strategy
- [ ] Backup strategy for SQLite
```

## Usage in Workflow

```python
# In workflow-orchestrator, when on contrib branch:

def create_planning_docs(feature_name, gh_user):
    """Create BMAD planning documents."""
    
    from datetime import datetime
    from pathlib import Path
    
    date = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Create planning directory
    planning_dir = Path('planning') / feature_name
    planning_dir.mkdir(parents=True, exist_ok=True)
    
    # Load templates
    templates_dir = Path('.claude/skills/bmad-planner/templates')
    
    # Generate requirements.md
    with open(templates_dir / 'requirements.md.template') as f:
        template = f.read()
    
    requirements = template.replace('{{TITLE}}', feature_name)
    requirements = requirements.replace('{{DATE}}', date)
    requirements = requirements.replace('{{GH_USER}}', gh_user)
    
    with open(planning_dir / 'requirements.md', 'w') as f:
        f.write(requirements)
    
    # Generate architecture.md
    with open(templates_dir / 'architecture.md.template') as f:
        template = f.read()
    
    architecture = template.replace('{{TITLE}}', feature_name)
    architecture = architecture.replace('{{DATE}}', date)
    architecture = architecture.replace('{{GH_USER}}', gh_user)
    
    with open(planning_dir / 'architecture.md', 'w') as f:
        f.write(architecture)
    
    # Create directory structure
    subprocess.run([
        'python',
        '.claude/skills/helper-functions/scripts/directory_structure.py',
        str(planning_dir)
    ])
    
    print(f"Ã¢Å“â€œ Planning documents created in {planning_dir}")
```
```

---

## Skill 5: speckit-author

**File: `.claude/skills/speckit-author/SKILL.md`**

```markdown
---
name: speckit-author
version: 5.1.0
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

### spec.md.template

```markdown
# Specification: {{TITLE}}

**Type:** {{WORKFLOW_TYPE}}
**Slug:** {{SLUG}}
**Date:** {{DATE}}
**Author:** {{GH_USER}}

## Overview

[One paragraph describing what this feature does]

## Requirements Reference

See: `planning/{{SLUG}}/requirements.md` in main repository

## Detailed Specification

### Component 1: Database Schema

**File:** `src/models/schema.py`

\`\`\`python
# SQLAlchemy models

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Schema(Base):
    __tablename__ = 'schemas'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    schema_json = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class ValidationHistory(Base):
    __tablename__ = 'validation_history'
    
    id = Column(Integer, primary_key=True)
    schema_id = Column(Integer, ForeignKey('schemas.id'))
    input_json = Column(JSON, nullable=False)
    valid = Column(Boolean, nullable=False)
    errors = Column(JSON)
    validated_at = Column(DateTime, default=datetime.utcnow)
\`\`\`

### Component 2: Validation Logic

**File:** `src/validator/core.py`

\`\`\`python
# JSON schema validation

from jsonschema import validate, ValidationError as JSONSchemaError
from typing import Dict, Tuple, List

class JSONValidator:
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate(self, data: dict) -> Tuple[bool, List[str]]:
        """
        Validate JSON data against schema.
        
        Returns:
            (is_valid, error_messages)
        """
        try:
            validate(instance=data, schema=self.schema)
            return True, []
        except JSONSchemaError as e:
            return False, [str(e)]
\`\`\`

### Component 3: FastAPI Endpoints

**File:** `src/api/routes.py`

\`\`\`python
# API routes

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

router = APIRouter()

class ValidationRequest(BaseModel):
    schema_name: str
    data: Dict[str, Any]

class ValidationResponse(BaseModel):
    valid: bool
    schema_version: int
    validated_at: datetime
    errors: List[str] = []

@router.post("/validate", response_model=ValidationResponse)
async def validate_json(request: ValidationRequest):
    """Validate JSON against a schema."""
    # Implementation details in plan.md
    pass

@router.post("/schemas")
async def create_schema(name: str, schema: Dict[str, Any]):
    """Create a new validation schema."""
    pass

@router.get("/schemas")
async def list_schemas():
    """List all schemas."""
    pass

@router.get("/schemas/{name}")
async def get_schema(name: str):
    """Get specific schema."""
    pass
\`\`\`

## Testing Requirements

### Unit Tests

**File:** `tests/test_validator.py`

\`\`\`python
import pytest
from src.validator.core import JSONValidator

def test_valid_json():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    validator = JSONValidator(schema)
    
    valid, errors = validator.validate({"name": "test"})
    assert valid is True
    assert errors == []

def test_invalid_json():
    schema = {"type": "object", "properties": {"age": {"type": "integer"}}}
    validator = JSONValidator(schema)
    
    valid, errors = validator.validate({"age": "not a number"})
    assert valid is False
    assert len(errors) > 0
\`\`\`

### Integration Tests

**File:** `tests/test_api.py`

\`\`\`python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_validate_endpoint():
    response = client.post("/validate", json={
        "schema_name": "test-schema",
        "data": {"field": "value"}
    })
    assert response.status_code == 200
    assert "valid" in response.json()
\`\`\`

## Quality Gates

- Test coverage: Ã¢â€°Â¥ 80%
- All tests passing
- Linting: ruff check passes
- Type checking: mypy passes

## Container Specifications

### Containerfile

\`\`\`dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

### podman-compose.yml

\`\`\`yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Containerfile
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      DATABASE_URL: sqlite:////app/data/validator.db
      LOG_LEVEL: info
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      db:
        condition: service_started

  db:
    image: alpine:latest
    volumes:
      - sqlite-data:/data
    command: sleep infinity

volumes:
  sqlite-data:
    driver: local
\`\`\`

## Dependencies

\`\`\`toml
# pyproject.toml additions

[project]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy>=2.0.0",
    "jsonschema>=4.20.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
\`\`\`

## API Contract Examples

### Success Response (Valid JSON)

\`\`\`json
POST /validate
Request:
{
  "schema_name": "user-registration",
  "data": {
    "username": "johndoe",
    "email": "john@example.com",
    "age": 25
  }
}

Response: 200 OK
{
  "valid": true,
  "schema_version": 1,
  "validated_at": "2025-10-22T15:30:00Z",
  "errors": []
}
\`\`\`

### Error Response (Invalid JSON)

\`\`\`json
POST /validate
Request:
{
  "schema_name": "user-registration",
  "data": {
    "username": "johndoe",
    "age": "twenty-five"
  }
}

Response: 400 Bad Request
{
  "valid": false,
  "schema_version": 1,
  "validated_at": "2025-10-22T15:31:00Z",
  "errors": [
    "'email' is a required property",
    "'age' should be of type integer"
  ]
}
\`\`\`
```

### plan.md.template

```markdown
# Implementation Plan: {{TITLE}}

**Type:** {{WORKFLOW_TYPE}}
**Slug:** {{SLUG}}
**Date:** {{DATE}}

## Task Breakdown

### Phase 1: Database Setup

#### Task impl_001: SQLAlchemy Models
**Estimated:** 30 min
**Files:**
- `src/models/__init__.py`
- `src/models/schema.py`
- `src/db.py` (database connection)

**Steps:**
1. Create models package
2. Define Schema and ValidationHistory models
3. Set up database connection with SQLAlchemy
4. Create Alembic migration (if using migrations)

**Verification:**
\`\`\`bash
uv run python -c "from src.models.schema import Base; print('Models loaded')"
\`\`\`

#### Task impl_002: Database Initialization
**Estimated:** 15 min
**Files:**
- `src/db.py`
- `scripts/init_db.py`

**Steps:**
1. Create database initialization script
2. Set up connection pooling
3. Test database connectivity

**Verification:**
\`\`\`bash
uv run python scripts/init_db.py
sqlite3 data/validator.db ".tables"
\`\`\`

### Phase 2: Core Validation Logic

#### Task impl_003: JSON Validator
**Estimated:** 1 hour
**Files:**
- `src/validator/__init__.py`
- `src/validator/core.py`
- `src/validator/schemas.py`

**Steps:**
1. Implement JSONValidator class
2. Add schema caching
3. Error message formatting
4. Add logging

**Verification:**
\`\`\`python
from src.validator.core import JSONValidator

schema = {"type": "object", "properties": {"name": {"type": "string"}}}
validator = JSONValidator(schema)
assert validator.validate({"name": "test"})[0] is True
\`\`\`

### Phase 3: API Implementation

#### Task impl_004: FastAPI Application
**Estimated:** 1 hour
**Files:**
- `src/main.py`
- `src/api/__init__.py`
- `src/api/routes.py`
- `src/api/dependencies.py`

**Steps:**
1. Create FastAPI app with CORS middleware
2. Set up dependency injection for database
3. Add health check endpoint
4. Configure logging

#### Task impl_005: Validation Endpoints
**Estimated:** 1.5 hours
**Files:**
- `src/api/routes.py`
- `src/services/validator_service.py`

**Steps:**
1. Implement POST /validate endpoint
2. Add request/response validation with Pydantic
3. Database persistence of validation history
4. Error handling

#### Task impl_006: Schema Management Endpoints
**Estimated:** 1 hour
**Files:**
- `src/api/routes.py`
- `src/services/schema_service.py`

**Steps:**
1. Implement POST /schemas
2. Implement GET /schemas
3. Implement GET /schemas/{name}
4. Add schema versioning logic

### Phase 4: Testing

#### Task test_001: Unit Tests
**Estimated:** 2 hours
**Files:**
- `tests/test_validator.py`
- `tests/test_models.py`
- `tests/conftest.py`

**Steps:**
1. Set up pytest fixtures
2. Test JSONValidator with various schemas
3. Test database models
4. Test schema versioning

**Coverage Target:** 85%+

#### Task test_002: Integration Tests
**Estimated:** 2 hours
**Files:**
- `tests/test_api.py`
- `tests/test_integration.py`

**Steps:**
1. Test all API endpoints
2. Test end-to-end validation flow
3. Test error scenarios
4. Test concurrent requests

**Coverage Target:** 80%+

### Phase 5: Containerization

#### Task container_001: Application Container
**Estimated:** 30 min
**Files:**
- `Containerfile`
- `.containerignore`

**Steps:**
1. Create multi-stage Containerfile
2. Optimize layer caching
3. Add health check
4. Test container build

**Verification:**
\`\`\`bash
podman build -t json-validator:latest .
podman run --rm json-validator:latest python -c "from src.main import app; print('OK')"
\`\`\`

#### Task container_002: Podman Compose
**Estimated:** 30 min
**Files:**
- `podman-compose.yml`
- `.env.example`

**Steps:**
1. Define services (app, db)
2. Configure volumes and networking
3. Set environment variables
4. Add health checks

**Verification:**
\`\`\`bash
podman-compose up -d
curl http://localhost:8000/health
podman-compose down
\`\`\`

## Estimated Total Time

- Database: 45 min
- Validation Logic: 1 hour
- API: 3.5 hours
- Testing: 4 hours
- Containerization: 1 hour

**Total:** ~10 hours

## Dependencies Between Tasks

\`\`\`
impl_001 Ã¢â€ â€™ impl_002
impl_003 Ã¢â€ â€™ impl_005
impl_001, impl_002, impl_003 Ã¢â€ â€™ impl_004
impl_004 Ã¢â€ â€™ impl_005, impl_006
impl_005, impl_006 Ã¢â€ â€™ test_001, test_002
test_001, test_002 Ã¢â€ â€™ container_001
container_001 Ã¢â€ â€™ container_002
\`\`\`

## Quality Checklist

- [ ] All tasks completed
- [ ] Test coverage Ã¢â€°Â¥ 80%
- [ ] All tests passing
- [ ] Linting clean (ruff check)
- [ ] Type checking clean (mypy)
- [ ] Container builds successfully
- [ ] Container health checks passing
- [ ] API documentation complete
- [ ] Code reviewed
```

## Usage in Workflow

```python
# In workflow-orchestrator, when in worktree:

def create_specifications(slug, workflow_type, gh_user):
    """Create SpecKit documents in worktree."""
    
    from datetime import datetime
    from pathlib import Path
    
    date = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Create specs directory
    specs_dir = Path('specs') / slug
    specs_dir.mkdir(parents=True, exist_ok=True)
    
    # Load templates
    templates_dir = Path('.claude/skills/speckit-author/templates')
    
    # Generate spec.md
    with open(templates_dir / 'spec.md.template') as f:
        template = f.read()
    
    spec = template.replace('{{TITLE}}', slug.replace('-', ' ').title())
    spec = spec.replace('{{WORKFLOW_TYPE}}', workflow_type)
    spec = spec.replace('{{SLUG}}', slug)
    spec = spec.replace('{{DATE}}', date)
    spec = spec.replace('{{GH_USER}}', gh_user)
    
    with open(specs_dir / 'spec.md', 'w') as f:
        f.write(spec)
    
    # Generate plan.md
    with open(templates_dir / 'plan.md.template') as f:
        template = f.read()
    
    plan = template.replace('{{TITLE}}', slug.replace('-', ' ').title())
    plan = plan.replace('{{WORKFLOW_TYPE}}', workflow_type)
    plan = plan.replace('{{SLUG}}', slug)
    plan = plan.replace('{{DATE}}', date)
    
    with open(specs_dir / 'plan.md', 'w') as f:
        f.write(plan)
    
    # Create directory structure
    subprocess.run([
        'python',
        '.claude/skills/helper-functions/scripts/directory_structure.py',
        str(specs_dir)
    ])
    
    print(f"Ã¢Å“â€œ Specifications created in {specs_dir}")
```
```

---

## Skill 6: quality-enforcer

**File: `.claude/skills/quality-enforcer/SKILL.md`**

```markdown
---
name: quality-enforcer
version: 5.1.0
description: |
  Enforces quality gates: 80% test coverage, passing tests, successful builds,
  semantic versioning. Runs before PR creation.
  
  Use when: Running tests, checking coverage, validating quality, versioning
  
  Triggers: run tests, check coverage, quality gates, version bump
---

# Quality Enforcer

## Purpose

Ensures code quality standards are met before integration. Enforces:
- Test coverage Ã¢â€°Â¥ 80%
- All tests passing
- Successful builds
- Semantic versioning
- Container health

## Quality Gates

### Gate 1: Test Coverage

**Script: `scripts/check_coverage.py`**

```python
#!/usr/bin/env python3
"""Check test coverage meets 80% threshold."""

import subprocess
import sys
import re

def check_coverage(threshold=80):
    """
    Run pytest with coverage and verify threshold.
    
    Returns:
        (passed: bool, coverage: float)
    """
    try:
        # Run pytest with coverage
        result = subprocess.run(
            ['uv', 'run', 'pytest', '--cov=src', '--cov-report=term', '--cov-report=json'],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Parse coverage from JSON report
        import json
        with open('coverage.json') as f:
            coverage_data = json.load(f)
        
        total_coverage = coverage_data['totals']['percent_covered']
        
        passed = total_coverage >= threshold
        
        print(f"Coverage: {total_coverage:.1f}%")
        print(f"Threshold: {threshold}%")
        print(f"Status: {'Ã¢Å“â€œ PASS' if passed else 'Ã¢Å“â€” FAIL'}")
        
        return passed, total_coverage
    
    except Exception as e:
        print(f"Error checking coverage: {e}")
        return False, 0.0

if __name__ == '__main__':
    threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    passed, coverage = check_coverage(threshold)
    sys.exit(0 if passed else 1)
```

### Gate 2: All Tests Passing

```python
def run_tests():
    """Run all tests and verify they pass."""
    result = subprocess.run(
        ['uv', 'run', 'pytest', '-v'],
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    
    print(result.stdout)
    if not passed:
        print(result.stderr)
    
    return passed
```

### Gate 3: Successful Build

```python
def check_build():
    """Verify package builds successfully."""
    result = subprocess.run(
        ['uv', 'build'],
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    
    if passed:
        print("Ã¢Å“â€œ Build successful")
    else:
        print("Ã¢Å“â€” Build failed")
        print(result.stderr)
    
    return passed
```

### Gate 4: Container Health

```python
def check_container_health():
    """Build and test container health."""
    # Build container
    build_result = subprocess.run(
        ['podman', 'build', '-t', 'test-image:latest', '.'],
        capture_output=True,
        text=True
    )
    
    if build_result.returncode != 0:
        print("Ã¢Å“â€” Container build failed")
        return False
    
    print("Ã¢Å“â€œ Container built")
    
    # Run container and check health
    try:
        # Start container
        subprocess.run(
            ['podman', 'run', '-d', '--name', 'test-container', 'test-image:latest'],
            check=True
        )
        
        # Wait for health check
        import time
        time.sleep(5)
        
        # Check health
        health_result = subprocess.run(
            ['podman', 'healthcheck', 'run', 'test-container'],
            capture_output=True
        )
        
        healthy = health_result.returncode == 0
        
        if healthy:
            print("Ã¢Å“â€œ Container healthy")
        else:
            print("Ã¢Å“â€” Container unhealthy")
        
        return healthy
    
    finally:
        # Cleanup
        subprocess.run(['podman', 'rm', '-f', 'test-container'], capture_output=True)
```

### Gate 5: Linting & Type Checking

```python
def check_linting():
    """Run ruff linting."""
    result = subprocess.run(
        ['uv', 'run', 'ruff', 'check', 'src/', 'tests/'],
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    
    if passed:
        print("Ã¢Å“â€œ Linting passed")
    else:
        print("Ã¢Å“â€” Linting failed")
        print(result.stdout)
    
    return passed

def check_types():
    """Run mypy type checking."""
    result = subprocess.run(
        ['uv', 'run', 'mypy', 'src/'],
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    
    if passed:
        print("Ã¢Å“â€œ Type checking passed")
    else:
        print("Ã¢Å“â€” Type checking failed")
        print(result.stdout)
    
    return passed
```

## Comprehensive Quality Check

**Script: `scripts/run_quality_gates.py`**

```python
#!/usr/bin/env python3
"""Run all quality gates and report results."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from check_coverage import check_coverage

def run_all_quality_gates(coverage_threshold=80):
    """
    Run all quality gates and report results.
    
    Returns:
        (passed: bool, results: dict)
    """
    results = {}
    all_passed = True
    
    print("=" * 60)
    print("QUALITY GATES")
    print("=" * 60)
    
    # Gate 1: Test Coverage
    print("\n[1/5] Test Coverage...")
    passed, coverage = check_coverage(coverage_threshold)
    results['coverage'] = {'passed': passed, 'value': coverage}
    all_passed &= passed
    
    # Gate 2: Tests Passing
    print("\n[2/5] Running Tests...")
    passed = run_tests()
    results['tests'] = {'passed': passed}
    all_passed &= passed
    
    # Gate 3: Build
    print("\n[3/5] Build Check...")
    passed = check_build()
    results['build'] = {'passed': passed}
    all_passed &= passed
    
    # Gate 4: Linting
    print("\n[4/5] Linting...")
    passed = check_linting()
    results['linting'] = {'passed': passed}
    all_passed &= passed
    
    # Gate 5: Type Checking
    print("\n[5/5] Type Checking...")
    passed = check_types()
    results['types'] = {'passed': passed}
    all_passed &= passed
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for gate, result in results.items():
        status = "Ã¢Å“â€œ PASS" if result['passed'] else "Ã¢Å“â€” FAIL"
        print(f"{gate.upper()}: {status}")
    
    print("\n" + ("Ã¢Å“â€œ ALL GATES PASSED" if all_passed else "Ã¢Å“â€” SOME GATES FAILED"))
    
    return all_passed, results

if __name__ == '__main__':
    passed, _ = run_all_quality_gates()
    sys.exit(0 if passed else 1)
```

## Usage in Workflow

```python
# In workflow-orchestrator, before creating PR:

def enforce_quality_gates():
    """Run quality gates and block if any fail."""
    
    print("Running quality gates before PR creation...")
    
    result = subprocess.run(
        ['python', '.claude/skills/quality-enforcer/scripts/run_quality_gates.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("\nÃ¢Å¡Â Ã¯Â¸Â  QUALITY GATES FAILED")
        print("\nYou must fix these issues before creating a PR:")
        print(result.stdout)
        return False
    
    print("\nÃ¢Å“â€œ All quality gates passed")
    return True
```

## Semantic Versioning

Uses git-workflow-manager/scripts/semantic_version.py to calculate version bumps.

Integration:

```python
def update_version_in_todo(todo_file, new_version):
    """Update semantic_version in TODO file YAML frontmatter."""
    
    import yaml
    from pathlib import Path
    
    content = Path(todo_file).read_text()
    
    # Split frontmatter and body
    parts = content.split('---', 2)
    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]
    
    # Update version
    frontmatter['quality_gates']['semantic_version'] = new_version
    
    # Write back
    new_content = f"---\n{yaml.dump(frontmatter)}---{body}"
    Path(todo_file).write_text(new_content)
    
    print(f"Ã¢Å“â€œ Updated version to {new_version} in {todo_file}")
```
```

---

## Skill 7: helper-functions

**File: `.claude/skills/helper-functions/SKILL.md`**

```markdown
---
name: helper-functions
version: 5.1.0
description: |
  Shared utilities for file deprecation, directory structure creation,
  TODO file updates, and archive management. Used by all other skills.
  
  Use when: Need shared utilities, deprecating files, updating TODO
  
  Triggers: deprecate, archive, update TODO, create directory
---

# Helper Functions

## Purpose

Provides reusable Python utilities for common workflow tasks.

## Scripts

### deprecate_files.py

```python
#!/usr/bin/env python3
"""Deprecate files by archiving them with timestamp."""

import sys
import zipfile
from datetime import datetime
from pathlib import Path

def deprecate_files(todo_file, description, *files):
    """
    Archive deprecated files with timestamp.
    
    Args:
        todo_file: Path to TODO file (for timestamp extraction)
        description: Short description (e.g., 'old-auth-flow')
        *files: File paths to deprecate
    
    Creates:
        ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip
    """
    # Extract timestamp from TODO file
    todo_path = Path(todo_file)
    todo_name = todo_path.stem  # TODO_feature_20251022T143022Z_slug
    parts = todo_name.split('_')
    timestamp = parts[2] if len(parts) > 2 else datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    
    # Create ARCHIVED directory if needed
    archived_dir = Path('ARCHIVED')
    archived_dir.mkdir(exist_ok=True)
    
    # Ensure ARCHIVED has standard files
    create_directory_structure(archived_dir)
    
    # Create zip archive
    zip_name = f"{timestamp}_{description}.zip"
    zip_path = archived_dir / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            file_path = Path(file)
            if file_path.exists():
                zipf.write(file_path, file_path.name)
                print(f"  Archived: {file}")
                file_path.unlink()  # Delete original
            else:
                print(f"  Warning: {file} not found")
    
    print(f"Ã¢Å“â€œ Created archive: {zip_path}")
    return str(zip_path)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: deprecate_files.py <todo_file> <description> <file1> [file2 ...]")
        sys.exit(1)
    
    deprecate_files(sys.argv[1], sys.argv[2], *sys.argv[3:])
```

### directory_structure.py

```python
#!/usr/bin/env python3
"""Create standard directory structure with CLAUDE.md, README.md, ARCHIVED/."""

import sys
from pathlib import Path

def create_directory_structure(directory, is_archived=False):
    """
    Create standard directory structure.
    
    Args:
        directory: Path to directory
        is_archived: True if this IS an ARCHIVED directory
    
    Creates:
        - CLAUDE.md
        - README.md
        - ARCHIVED/ (unless is_archived=True)
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create CLAUDE.md
    claude_md = dir_path / 'CLAUDE.md'
    if not claude_md.exists():
        context_type = "archived content" if is_archived else dir_path.name
        claude_md.write_text(f"""# Claude Code Context: {context_type}

## Purpose

{f"Archive of deprecated files from {dir_path.parent.name}" if is_archived else f"Context-specific guidance for {dir_path.name}"}

## Files in This Directory

[List key files and their purposes]

## Related Skills

- workflow-orchestrator
- helper-functions
""")
        print(f"Ã¢Å“â€œ Created {claude_md}")
    
    # Create README.md
    readme_md = dir_path / 'README.md'
    if not readme_md.exists():
        readme_md.write_text(f"""# {dir_path.name}

## Overview

{f"Archive of deprecated files" if is_archived else f"Documentation for {dir_path.name}"}

## Contents

[Describe contents]
""")
        print(f"Ã¢Å“â€œ Created {readme_md}")
    
    # Create ARCHIVED/ subdirectory (unless this IS archived)
    if not is_archived:
        archived_dir = dir_path / 'ARCHIVED'
        archived_dir.mkdir(exist_ok=True)
        
        # Recursively create structure for ARCHIVED
        create_directory_structure(archived_dir, is_archived=True)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: directory_structure.py <directory>")
        sys.exit(1)
    
    create_directory_structure(sys.argv[1])
```

### todo_updater.py

```python
#!/usr/bin/env python3
"""Update TODO file status, workflow progress, and history."""

import sys
import yaml
from datetime import datetime
from pathlib import Path

def update_todo_task_status(todo_file, task_id, status, context_usage=None):
    """
    Update task status in TODO file.
    
    Args:
        todo_file: Path to TODO file
        task_id: Task ID (e.g., 'impl_003')
        status: New status ('pending' | 'complete' | 'blocked')
        context_usage: Optional context usage percentage
    """
    content = Path(todo_file).read_text()
    
    # Split frontmatter and body
    parts = content.split('---', 2)
    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]
    
    # Update task status in frontmatter
    task_category = task_id.split('_')[0]  # impl, test, etc.
    
    if task_category in frontmatter['tasks']:
        for task in frontmatter['tasks'][task_category]:
            if task['id'] == task_id:
                task['status'] = status
                if status == 'complete':
                    task['completed_at'] = datetime.utcnow().isoformat() + 'Z'
    
    # Update workflow progress
    frontmatter['workflow_progress']['last_task'] = task_id
    frontmatter['workflow_progress']['last_update'] = datetime.utcnow().isoformat() + 'Z'
    if context_usage:
        frontmatter['workflow_progress']['context_usage'] = f"{context_usage}%"
    
    # Write back
    new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---{body}"
    Path(todo_file).write_text(new_content)
    
    print(f"Ã¢Å“â€œ Updated {task_id} status to {status}")

def add_todo_history_entry(todo_file, message):
    """Add entry to TODO status history in body."""
    
    content = Path(todo_file).read_text()
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Find status history section
    history_marker = '## Status History'
    if history_marker in content:
        entry = f"- {timestamp}: {message}"
        content = content.replace(
            history_marker,
            f"{history_marker}\n{entry}"
        )
    
    Path(todo_file).write_text(content)
    print(f"Ã¢Å“â€œ Added history: {message}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: todo_updater.py <todo_file> <task_id> <status> [context_usage]")
        sys.exit(1)
    
    context_usage = int(sys.argv[4]) if len(sys.argv) > 4 else None
    update_todo_task_status(sys.argv[1], sys.argv[2], sys.argv[3], context_usage)
```

### archive_manager.py

```python
#!/usr/bin/env python3
"""Manage archived files: list, extract, verify."""

import sys
import zipfile
from pathlib import Path
from datetime import datetime

def list_archives(archived_dir='ARCHIVED'):
    """List all archives with timestamps."""
    
    archived_path = Path(archived_dir)
    if not archived_path.exists():
        print(f"No ARCHIVED directory found")
        return []
    
    archives = sorted(archived_path.glob('*.zip'))
    
    print(f"Archives in {archived_dir}:")
    for archive in archives:
        # Parse timestamp from filename
        name = archive.stem  # YYYYMMDDTHHMMSSZ_description
        parts = name.split('_', 1)
        if len(parts) == 2:
            timestamp_str, description = parts
            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, '%Y%m%dT%H%M%SZ')
                print(f"  {timestamp.isoformat()} - {description} ({archive.name})")
            except ValueError:
                print(f"  {archive.name}")
        else:
            print(f"  {archive.name}")
    
    return archives

def extract_archive(archive_path, output_dir='.'):
    """Extract archive to specified directory."""
    
    archive = Path(archive_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(archive, 'r') as zipf:
        zipf.extractall(output)
        print(f"Ã¢Å“â€œ Extracted {archive.name} to {output}")
        print("Files:")
        for name in zipf.namelist():
            print(f"  - {name}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: archive_manager.py <list|extract> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        archived_dir = sys.argv[2] if len(sys.argv) > 2 else 'ARCHIVED'
        list_archives(archived_dir)
    
    elif command == 'extract':
        if len(sys.argv) < 3:
            print("Usage: archive_manager.py extract <archive_path> [output_dir]")
            sys.exit(1)
        
        archive_path = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else '.'
        extract_archive(archive_path, output_dir)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

## Usage in Other Skills

```python
# Example: Using deprecate_files in implementation

from pathlib import Path
import subprocess

def implement_with_deprecation(task_id, todo_file, old_files):
    """Implement task and deprecate old files if needed."""
    
    # Implementation code...
    
    # Deprecate old files
    if old_files:
        subprocess.run([
            'python',
            '.claude/skills/helper-functions/scripts/deprecate_files.py',
            todo_file,
            'old-implementation',
            *old_files
        ], check=True)
    
    # Update TODO status
    subprocess.run([
        'python',
        '.claude/skills/helper-functions/scripts/todo_updater.py',
        todo_file,
        task_id,
        'complete',
        '35'  # context usage percentage
    ], check=True)
```
```

---

## Example Scenario: JSON Validator Service

### Initial State

```
json-validator/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ .git/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ pyproject.toml          # Existing uv project
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ src/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ __init__.py
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ tests/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ __init__.py
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ README.md
```

### Workflow Execution

#### Step 0: Setup Skills

**User prompt:**
```
Initialize workflow v5.1 skills for this Python project.
```

**Claude Code actions:**
1. Verify prerequisites (gh CLI, uv, git)
2. Extract GitHub username: `gh api user --jq '.login'`
3. Create `.claude/skills/` directory structure
4. Generate all 7 skill folders with SKILL.md files
5. Create workflow files: WORKFLOW.md, CLAUDE.md, TODO.md
6. Initialize `contrib/<gh-user>` branch
7. Prompt for confirmation

**Output:**
```
Ã¢Å“â€œ Prerequisites verified
  GitHub User: johndoe
  Python: 3.11.5
  uv: 0.4.18
  Podman: 4.9.3

Ã¢Å“â€œ Created .claude/skills/ with 7 skills:
  - workflow-orchestrator
  - tech-stack-adapter
  - git-workflow-manager
  - bmad-planner
  - speckit-author
  - quality-enforcer
  - helper-functions

Ã¢Å“â€œ Created workflow files
Ã¢Å“â€œ Initialized contrib/johndoe branch

Would you like to verify skill loading? (Y/n)
```

#### Step 1: Verify Skills

**User prompt:**
```
Y
```

**Claude Code actions:**
```bash
# Load orchestrator
python -c "
from pathlib import Path
skill = Path('.claude/skills/workflow-orchestrator/SKILL.md')
assert skill.exists(), 'Orchestrator not found'
print('Ã¢Å“â€œ workflow-orchestrator loaded')
"

# Check all skills discoverable
for skill in .claude/skills/*/SKILL.md; do
  name=$(basename $(dirname $skill))
  echo "Ã¢Å“â€œ $name"
done
```

**Output:**
```
Ã¢Å“â€œ workflow-orchestrator loaded
Ã¢Å“â€œ workflow-orchestrator
Ã¢Å“â€œ tech-stack-adapter
Ã¢Å“â€œ git-workflow-manager
Ã¢Å“â€œ bmad-planner
Ã¢Å“â€œ speckit-author
Ã¢Å“â€œ quality-enforcer
Ã¢Å“â€œ helper-functions

All skills verified. Say "next step?" to begin workflow.
```

#### Step 2: Planning Phase

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Load workflow-orchestrator
2. Detect context: main repo, contrib/johndoe branch
3. Load bmad-planner skill
4. Parse TODO.md (if exists) or create new workflow

**Output:**
```
Next step from workflow:
Phase 1, Step 1.1: Create BMAD planning documents

This will:
- Create planning/json-validator/ directory
- Generate requirements.md from template
- Generate architecture.md from template
- Set up directory structure (CLAUDE.md, README.md, ARCHIVED/)
- Commit to contrib/johndoe

Would you like to proceed with Step 1.1? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```bash
# Execute planning
python .claude/skills/bmad-planner/scripts/create_planning.py \
  json-validator johndoe

# Creates:
# planning/json-validator/
# Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ CLAUDE.md
# Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ README.md
# Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ requirements.md
# Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ architecture.md
# Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ ARCHIVED/
#     Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ CLAUDE.md
#     Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ README.md

git add planning/
git commit -m "docs: add BMAD planning for JSON validator"
git push origin contrib/johndoe
```

**Output:**
```
Ã¢Å“â€œ Planning documents created
Ã¢Å“â€œ Committed to contrib/johndoe

Please run: /context
If context > 50%, I'll save state and you run /init

Next: Say "next step?" to create feature worktree
```

#### Step 3: Create Feature Worktree

**User prompt:**
```
/context
```

**User sees:** `Context: 12% used`

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Load git-workflow-manager
2. Create feature worktree

**Output:**
```
Next step from workflow:
Phase 2, Step 2.1: Create feature worktree

This will:
- Create worktree at ../json-validator_feature_20251022T143022Z_json-validator/
- Create branch feature/20251022T143022Z_json-validator from contrib/johndoe
- Generate TODO_feature_20251022T143022Z_json-validator.md in main repo
- Switch to worktree directory

Would you like to proceed with Step 2.1? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature json-validator contrib/johndoe

# Output: worktree_path, branch_name, todo_file

cd ../json-validator_feature_20251022T143022Z_json-validator/
```

**Output:**
```
Ã¢Å“â€œ Worktree created: /home/user/projects/json-validator_feature_20251022T143022Z_json-validator
Ã¢Å“â€œ Branch: feature/20251022T143022Z_json-validator
Ã¢Å“â€œ TODO: TODO_feature_20251022T143022Z_json-validator.md

Now in worktree. Say "next step?" to create specifications.
```

#### Step 4: Create Specifications

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Detect context: in worktree
2. Load speckit-author
3. Generate specs

**Output:**
```
Next step from workflow:
Phase 2, Step 2.2: Create SpecKit specifications

This will:
- Create specs/json-validator/ directory
- Generate spec.md with detailed component specifications
- Generate plan.md with task breakdown and estimates
- Set up directory structure

Would you like to proceed with Step 2.2? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```bash
python .claude/skills/speckit-author/scripts/create_specs.py \
  json-validator feature johndoe

git add specs/
git commit -m "docs(json-validator): add SpecKit specifications"
git push origin feature/20251022T143022Z_json-validator
```

**Output:**
```
Ã¢Å“â€œ Specifications created
Ã¢Å“â€œ spec.md: 450 lines
Ã¢Å“â€œ plan.md: 380 lines
Ã¢Å“â€œ Committed and pushed

Next: Say "next step?" to begin implementation
```

#### Step 5: Implementation Tasks

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Load tech-stack-adapter (first time)
2. Detect Python/uv configuration
3. Parse TODO file for next pending task
4. Load speckit-author for spec reference

**Output:**
```
Detected stack configuration:
  Python: 3.11.5
  Package Manager: uv
  Test Framework: pytest
  Database: sqlite (sqlalchemy)
  Container: podman

Next step from workflow:
Phase 2, Step 2.3: Implement task impl_001

Task: Database schema with SQLAlchemy
Files: src/models/schema.py, src/db.py
Estimated: 30 minutes

This will:
- Create src/models/ package
- Define Schema and ValidationHistory models
- Set up database connection
- Run tests
- Commit changes

Would you like to proceed with Step 2.3? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```python
# Implementation code generation...
# (Claude generates actual Python code based on specs)

# Run tests
subprocess.run(['uv', 'run', 'pytest', 'tests/test_models.py'])

# Commit
git add src/models/ tests/test_models.py
git commit -m "feat(json-validator): implement database schema

Implements: impl_001
Spec: specs/json-validator/spec.md
Tests: tests/test_models.py
Coverage: 90%

Refs: TODO_feature_20251022T143022Z_json-validator.md"

# Update TODO
python .claude/skills/helper-functions/scripts/todo_updater.py \
  ../TODO_feature_20251022T143022Z_json-validator.md \
  impl_001 complete 18
```

**Output:**
```
Ã¢Å“â€œ Database schema implemented
Ã¢Å“â€œ Tests passing (3/3)
Ã¢Å“â€œ Coverage: 90%
Ã¢Å“â€œ TODO updated

Please run: /context
Current context: 18%

Next: Say "next step?" for impl_002
```

**[Continue for all impl_* and test_* tasks...]**

#### Step 6: Quality Gates

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Load quality-enforcer
2. Run comprehensive quality gates

**Output:**
```
Next step from workflow:
Phase 3, Step 3.1: Run quality gates

This will:
- Check test coverage (Ã¢â€°Â¥80%)
- Run all tests
- Verify build
- Run linting (ruff)
- Check types (mypy)
- Build and test containers

Would you like to proceed with Step 3.1? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Output:**
```
============================================================
QUALITY GATES
============================================================

[1/5] Test Coverage...
Coverage: 83.5%
Threshold: 80%
Status: Ã¢Å“â€œ PASS

[2/5] Running Tests...
======================== test session starts ========================
collected 24 items

tests/test_validator.py ........                            [ 33%]
tests/test_models.py ....                                   [ 50%]
tests/test_api.py ............                              [100%]

======================== 24 passed in 2.35s ========================
Status: Ã¢Å“â€œ PASS

[3/5] Build Check...
Ã¢Å“â€œ Build successful

[4/5] Linting...
Ã¢Å“â€œ Linting passed

[5/5] Type Checking...
Ã¢Å“â€œ Type checking passed

============================================================
SUMMARY
============================================================
COVERAGE: Ã¢Å“â€œ PASS
TESTS: Ã¢Å“â€œ PASS
BUILD: Ã¢Å“â€œ PASS
LINTING: Ã¢Å“â€œ PASS
TYPES: Ã¢Å“â€œ PASS

Ã¢Å“â€œ ALL GATES PASSED

Next: Say "next step?" to calculate semantic version and create PR
```

#### Step 7: Create PR

**User prompt:**
```
next step?
```

**Claude Code actions:**
1. Calculate semantic version
2. Prepare PR

**Output:**
```
Next step from workflow:
Phase 4, Step 4.1: Create PR to contrib/johndoe

Semantic version analysis:
- Changed files: 12
- New features: API endpoints, validator
- Bump type: minor
- Current: v1.0.0
- New: v1.1.0

This will:
- Create PR: feature/20251022T143022Z_json-validator Ã¢â€ â€™ contrib/johndoe
- Include quality gate results
- Reference TODO file

Would you like to proceed with Step 4.1? (Y/n)
```

**User:** `Y`

**Claude Code actions:**
```bash
gh pr create \
  --base "contrib/johndoe" \
  --head "feature/20251022T143022Z_json-validator" \
  --title "feat: JSON schema validator service" \
  --body "$(cat <<EOF
Implements JSON validation service with SQLite persistence.

## Changes
- Database schema (SQLAlchemy)
- JSON validator core logic
- FastAPI REST API
- Podman containers (app + sqlite)
- Comprehensive tests (83.5% coverage)

## Quality Gates
Ã¢Å“â€œ All tests passing (24/24)
Ã¢Å“â€œ Coverage: 83.5% (Ã¢â€°Â¥80%)
Ã¢Å“â€œ Build successful
Ã¢Å“â€œ Linting passed
Ã¢Å“â€œ Type checking passed
Ã¢Å“â€œ Containers healthy

## Semantic Version
v1.0.0 Ã¢â€ â€™ v1.1.0 (minor bump)

See: TODO_feature_20251022T143022Z_json-validator.md
EOF
)"
```

**Output:**
```
Ã¢Å“â€œ PR created: https://github.com/user/json-validator/pull/123

Workflow complete for feature phase.

Next steps:
1. Merge PR in GitHub UI
2. Say "next step?" to rebase contrib/johndoe onto develop
3. Create PR: contrib/johndoe Ã¢â€ â€™ develop
```

---

## Skill Creation Instructions

### For Claude Code

When user provides this directive, execute the following:

1. **Verify prerequisites:**
```bash
bash .claude/skills/workflow-orchestrator/scripts/verify_prereqs.sh
```

2. **Create skill directories:**
```bash
mkdir -p .claude/skills/{workflow-orchestrator,tech-stack-adapter,git-workflow-manager,bmad-planner,speckit-author,quality-enforcer,helper-functions}/{scripts,templates}
```

3. **Generate SKILL.md files:**
For each skill, create the SKILL.md file with:
- YAML frontmatter (name, version, description, triggers)
- Purpose section
- Implementation details
- Usage examples

4. **Create Python scripts:**
For each skill's scripts/ directory, create the Python utilities described in this directive.

5. **Create templates:**
For skills with templates/ directories, create the markdown templates.

6. **Generate workflow files:**
```bash
# WORKFLOW.md - comprehensive guide
# CLAUDE.md - interaction guide  
# TODO.md - manifest template
# README.md - project overview
```

7. **Initialize git branch:**
```bash
GH_USER=$(gh api user --jq '.login')
git checkout -b "contrib/$GH_USER"
git push -u origin "contrib/$GH_USER"
```

8. **Verification:**
```bash
# List all skills
ls -la .claude/skills/

# Verify skill loading
python -c "
from pathlib import Path
for skill_dir in Path('.claude/skills').iterdir():
    if skill_dir.is_dir():
        skill_md = skill_dir / 'SKILL.md'
        assert skill_md.exists(), f'{skill_dir.name} missing SKILL.md'
        print(f'Ã¢Å“â€œ {skill_dir.name}')
"
```

---

## Verification Prompts

Use these prompts to test skill functionality:

### Prompt 1: Initial Setup
```
Initialize workflow v5.1 skills for this Python project.
```

**Expected:** Creates all 7 skills, workflow files, contrib branch

### Prompt 2: Skill Loading
```
Read workflow-orchestrator/SKILL.md and list all skills you can access.
```

**Expected:** Lists all 7 skills with descriptions

### Prompt 3: Tech Stack Detection
```
next step?
```
(From clean state)

**Expected:** Detects Python/uv, loads tech-stack-adapter, shows configuration

### Prompt 4: Planning Phase
```
next step?
```
(After setup, on contrib branch)

**Expected:** Loads bmad-planner, offers to create requirements.md and architecture.md

### Prompt 5: Feature Creation
```
next step?
```
(After planning)

**Expected:** Loads git-workflow-manager, creates feature worktree, switches to it

### Prompt 6: Specifications
```
next step?
```
(In worktree)

**Expected:** Loads speckit-author, creates spec.md and plan.md

### Prompt 7: Implementation
```
next step?
```
(After specs)

**Expected:** Loads appropriate skills, implements first task from plan.md

### Prompt 8: Quality Check
```
next step?
```
(After all implementation tasks)

**Expected:** Loads quality-enforcer, runs all gates, reports results

### Prompt 9: Context Management
```
/context
```

**Expected:** User sees context percentage, Claude prompts for /init if >50%

### Prompt 10: PR Creation
```
next step?
```
(After quality gates pass)

**Expected:** Calculates semantic version, creates PR with gh CLI

---

## Key Design Principles

1. **Progressive disclosure:** Load only relevant skills per phase (~300-900 tokens vs 2,718)
2. **Independence:** Skills don't cross-reference, orchestrator coordinates
3. **Token efficiency:** YAML metadata (~100 tokens), SKILL.md only when needed
4. **Context awareness:** Orchestrator detects repo vs worktree, loads appropriately
5. **User confirmation:** Always wait for "Y" before executing
6. **Context monitoring:** User manually checks via /context, runs /init at 50%
7. **Quality enforcement:** Gates must pass before PR creation
8. **Python ecosystem:** uv, pytest-cov, Podman, FastAPI
9. **Semantic versioning:** Automatic calculation based on changed components
10. **Archive management:** Proper deprecation with timestamps and zips

---

## Migration from v5.1

**Changes in v5.2:**
1. TODO.md now includes YAML frontmatter with metadata
2. TODO.md references all active TODO_*.md files with one-sentence descriptions
3. TODO.md references last 10 archived TODO_*.md files with one-sentence descriptions
4. Each TODO file requires one-sentence summary on first line after frontmatter
5. New `todo_updater.py` script for automatic manifest updates

**Migration steps:**
1. Complete any active v5.1 workflows
2. Update skill files to v5.2
3. Run `python .claude/skills/helper-functions/scripts/todo_updater.py .` to create TODO.md
4. New features will use v5.2 manifest automatically

**Backward compatibility:** v5.1 TODO files work with v5.2 (manifest is additive)

---

## Success Metrics

Track these metrics to validate skill effectiveness:

- **Token usage per phase:** Target <1,000 tokens (orchestrator + 1-2 skills)
- **Context resets:** How often /init required (target: <3 per feature)
- **Quality gate pass rate:** Target: 100% on first run after implementation complete
- **PR cycle time:** From feature start to merged (track for optimization)
- **Skill reuse:** Which skills loaded most frequently (validates architecture)
- **Manifest accuracy:** TODO.md reflects actual workflow state (target: 100%)
- **Archive navigation:** Users reference archived workflows for context (measure via logs)

---

## Future Enhancements

Potential v5.2+ features:

- Auto-detection of context usage via API (eliminate manual /context)
- Skill marketplace with community contributions
- Multi-language support (Node.js, Go, Rust)
- Integration with MCP servers for external tools
- AI-generated migration helpers for v4.2 Ã¢â€ â€™ v5.0
- Real-time quality gate monitoring during development
- Automated semantic version suggestion based on commit history

---

**END OF WORKFLOW v5.1 DIRECTIVE**
