---
name: workflow-orchestrator
version: 5.0.0
description: |
  Orchestrates git workflow for Python feature/release/hotfix development.
  Loads and coordinates other skills based on current context.

  Use when:
  - User says "next step?" or "continue workflow"
  - Working in git repo with TODO_[feature|release|hotfix]_*.md files
  - Need to determine workflow phase and load appropriate skills

  Triggers: next step, continue, what's next, workflow status

  Coordinates: tech-stack-adapter, git-workflow-manager, bmad-planner,
  speckit-author, quality-enforcer, workflow-utilities

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
   load_skill('workflow-utilities')  # For utilities
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
   - Update TODO file via workflow-utilities
   - Commit changes via git-workflow-manager

## Workflow Phases

### Phase 0: Initial Setup
1. Verify prerequisites (gh CLI, uv, git)
2. Create .claude/skills/ directory structure
3. Generate workflow files (WORKFLOW.md, CLAUDE.md, README.md)
4. Initialize contrib/<gh-user> branch

**Skills loaded:** tech-stack-adapter, git-workflow-manager, workflow-utilities

### Phase 1: Planning (Main Repo)
1. Create BMAD planning documents
2. Define requirements and architecture

**Skills loaded:** bmad-planner, workflow-utilities

### Phase 2: Feature Development (Worktree)
1. Create feature worktree
2. Write SpecKit specifications
3. Implement code
4. Write tests
5. Create containers

**Skills loaded:** speckit-author, git-workflow-manager, quality-enforcer, workflow-utilities

### Phase 3: Quality Assurance
1. Run tests with coverage
2. Validate quality gates
3. Calculate semantic version

**Skills loaded:** quality-enforcer, workflow-utilities

### Phase 4: Integration
1. Create PR from feature → contrib/<gh-user>
2. User merges PR in GitHub UI
3. Rebase contrib/<gh-user> onto develop
4. Create PR from contrib/<gh-user> → develop

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
    print("\n⚠️  Context Usage Check")
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

## Directory Standards

**Every directory must have:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (except ARCHIVED itself)

Use workflow-utilities/scripts/directory_structure.py to create compliant directories.

## Key Behaviors

✓ Load orchestrator first, then relevant skills per phase
✓ Always wait for "Y" confirmation
✓ Monitor context via /context command
✓ Save state and /init when context > 50%
✓ Update TODO file after each step
✓ Commit changes with descriptive messages
✓ Use workflow-utilities for shared utilities
