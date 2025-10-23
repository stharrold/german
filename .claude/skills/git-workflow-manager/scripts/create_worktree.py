#!/usr/bin/env python3
"""Create feature/release/hotfix worktree with TODO file."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def create_worktree(workflow_type, slug, base_branch):
    """
    Create a worktree for feature/release/hotfix development.

    Args:
        workflow_type: 'feature' | 'release' | 'hotfix'
        slug: Short descriptive name (e.g., 'json-validator')
        base_branch: Branch to create from (e.g., 'contrib/username')

    Returns:
        dict with worktree_path, branch_name, todo_file
    """
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    branch_name = f"{workflow_type}/{timestamp}_{slug}"

    repo_root = Path(subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        text=True
    ).strip())

    worktree_path = repo_root.parent / f"{repo_root.name}_{workflow_type}_{slug}"

    # Create worktree
    subprocess.run([
        'git', 'worktree', 'add',
        str(worktree_path),
        '-b', branch_name,
        base_branch
    ], check=True)

    # Create TODO file in main repo
    gh_user = subprocess.check_output(
        ['gh', 'api', 'user', '--jq', '.login'],
        text=True
    ).strip()

    todo_filename = f"TODO_{workflow_type}_{timestamp}_{slug}.md"
    todo_path = repo_root / todo_filename

    # Copy template and customize
    template_path = repo_root / '.claude' / 'skills' / 'workflow-orchestrator' / 'templates' / 'TODO_template.md'

    if template_path.exists():
        with open(template_path) as f:
            content = f.read()

        # Replace placeholders
        content = content.replace('{{WORKFLOW_TYPE}}', workflow_type)
        content = content.replace('{{SLUG}}', slug)
        content = content.replace('{{TIMESTAMP}}', timestamp)
        content = content.replace('{{GH_USER}}', gh_user)
        content = content.replace('{{TITLE}}', slug.replace('-', ' ').title())
        content = content.replace('{{DESCRIPTION}}', f"{workflow_type.title()} for {slug}")
        content = content.replace('{{CREATED}}', datetime.utcnow().isoformat() + 'Z')

        with open(todo_path, 'w') as f:
            f.write(content)
    else:
        # Create minimal TODO if template doesn't exist
        with open(todo_path, 'w') as f:
            f.write(f"""---
type: workflow-manifest
workflow_type: {workflow_type}
slug: {slug}
timestamp: {timestamp}
github_user: {gh_user}
---

# TODO: {slug}

Workflow: {workflow_type}
Created: {datetime.utcnow().isoformat()}Z
""")

    print(f"✓ Worktree created: {worktree_path}")
    print(f"✓ Branch: {branch_name}")
    print(f"✓ TODO file: {todo_filename}")

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
