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

    dir_name = dir_path.name

    # Create CLAUDE.md
    claude_md = dir_path / 'CLAUDE.md'
    if not claude_md.exists():
        if is_archived:
            context_type = "Archived Content"
            purpose = f"Archive of deprecated files from {dir_path.parent.name}"
        else:
            context_type = dir_name
            purpose = f"Context-specific guidance for {dir_name}"

        claude_md.write_text(f"""# Claude Code Context: {context_type}

## Purpose

{purpose}

## Directory Structure

[Describe the organization of files in this directory]

## Files in This Directory

[List key files and their purposes]

## Usage

[How to work with code/content in this directory]

## Related Skills

- workflow-orchestrator
- helper-functions
""")
        print(f"✓ Created {claude_md}")

    # Create README.md
    readme_md = dir_path / 'README.md'
    if not readme_md.exists():
        if is_archived:
            title = "Archived Files"
            overview = "Archive of deprecated files that are no longer in active use."
        else:
            title = dir_name.replace('-', ' ').replace('_', ' ').title()
            overview = f"Documentation for {dir_name}"

        readme_md.write_text(f"""# {title}

## Overview

{overview}

## Contents

[Describe the contents of this directory]

## Structure

[Explain the organization and key files]

## Usage

[How to use the resources in this directory]
""")
        print(f"✓ Created {readme_md}")

    # Create ARCHIVED/ subdirectory (unless this IS archived)
    if not is_archived:
        archived_dir = dir_path / 'ARCHIVED'
        archived_dir.mkdir(exist_ok=True)

        # Recursively create structure for ARCHIVED
        create_directory_structure(archived_dir, is_archived=True)

    print(f"✓ Directory structure complete: {dir_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: directory_structure.py <directory>")
        print("Example: directory_structure.py planning/my-feature")
        sys.exit(1)

    create_directory_structure(sys.argv[1])
