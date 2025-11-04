# .github Directory

This directory contains GitHub-specific configuration and documentation files.

## Contents

- **[BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)** - Step-by-step guide for configuring GitHub branch protection rules for `main` and `develop` branches

## Purpose

The `.github/` directory is a special directory recognized by GitHub for:

- Repository configuration files
- GitHub-specific documentation
- Workflow templates (`.github/workflows/`)
- Issue/PR templates (`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE/`)
- Community health files (`CODE_OF_CONDUCT.md`, `SECURITY.md`)

## Future Files (Not Yet Created)

Potential future additions to this directory:

- `.github/workflows/` - GitHub Actions CI/CD workflows
- `.github/ISSUE_TEMPLATE/` - Issue templates for bug reports, features
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template with checklist
- `.github/CODEOWNERS` - Code ownership and required reviewers
- `.github/dependabot.yml` - Automated dependency updates

## Related Documentation

- **[WORKFLOW.md](../WORKFLOW.md)** - Complete 6-phase workflow guide
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contributor guidelines
- **[README.md](../README.md)** - Project README

## Current Workflow Version

Workflow v5.2.0

---

**Note:** This directory is part of the workflow system created by the `initialize-repository` meta-skill. Files here are specific to GitHub integration and branch protection enforcement.
