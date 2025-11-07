# GitHub Branch Protection Setup Guide

This guide provides step-by-step instructions for configuring GitHub branch protection rules for the `main` and `develop` branches.

## Why Branch Protection?

**Protected branches prevent:**
- Accidental deletion of `main` or `develop`
- Direct commits (bypassing review and quality gates)
- Force pushes that rewrite history
- Merging without required approvals or status checks

**Branch protection enforces:**
- Pull request workflow (all changes reviewed)
- Quality gates (tests, coverage, linting must pass)
- Conversation resolution (all comments addressed)
- Linear history (clean merge commits)

## Prerequisites

- GitHub repository created
- You have admin access to the repository
- Repository has `main` and `develop` branches

## Setup Instructions

### Step 1: Navigate to Branch Protection Settings

1. Go to your GitHub repository
2. Click **Settings** tab (top right)
3. In left sidebar, click **Branches**
4. Scroll to **Branch protection rules** section
5. Click **Add rule** button

### Step 2: Configure `main` Branch Protection

**Branch name pattern:** `main`

#### Protect matching branches

☑️ **Require a pull request before merging**
- Prevents direct commits to main
- All changes must go through PR review

**Settings under this:**
- **Required approvals:** `0` (approval optional but not required)
  - PRs can be merged without approval (self-merge allowed)
- ☑️ **Dismiss stale pull request approvals when new commits are pushed**
  - Re-review required if PR changes after approval (if approvals given)
- ☐ **Require review from Code Owners** (optional)
  - Only if you have CODEOWNERS file configured
- ☑️ **Require conversation resolution before merging**
  - All review comments must be resolved

#### Require status checks to pass before merging

☑️ **Require status checks to pass before merging** (if CI/CD configured)
- Ensures tests, linting, coverage pass before merge
- ☑️ **Require branches to be up to date before merging**
  - Branch must be rebased on latest main before merge

**Add status checks** (if you have CI/CD configured):
- `test` - Test suite must pass
- `coverage` - Coverage ≥80% requirement
- `lint` - Linting must pass (ruff)
- `type-check` - Type checking must pass (mypy)

☐ Skip if you don't have CI/CD yet (you can add later)

#### Other settings

☐ **Require signed commits** (optional)
- Only required if your organization enforces GPG signing

☑️ **Do not allow bypassing the above settings**
- Even admins must follow these rules
- Prevents accidental "emergency" commits

☐ **Allow force pushes** → **KEEP UNCHECKED**
- Force pushes rewrite history (dangerous on main)

☐ **Allow deletions** → **KEEP UNCHECKED**
- Prevents accidental branch deletion

Click **Create** to save the rule.

### Step 3: Configure `develop` Branch Protection

Repeat Step 2 with these modifications:

**Branch name pattern:** `develop`

#### Protect matching branches

☑️ **Require a pull request before merging**

**Settings under this:**
- **Required approvals:** `0` (same as main - approval optional)
- ☑️ **Dismiss stale pull request approvals when new commits are pushed**
- ☑️ **Require conversation resolution before merging**

#### Require status checks to pass before merging

☑️ **Require status checks to pass before merging** (if CI/CD configured)
- ☑️ **Require branches to be up to date before merging**

**Add status checks** (same as main):
- `test`, `coverage`, `lint`, `type-check`

#### Other settings

☑️ **Do not allow bypassing the above settings** (optional for develop)
- Can be less strict than main (allows admin overrides if needed)

☐ **Allow force pushes** → **KEEP UNCHECKED**

☐ **Allow deletions** → **KEEP UNCHECKED**

Click **Create** to save the rule.

## Verification

After configuring both rules, verify they are active:

### Test 1: Attempt Direct Commit to Main

```bash
# Try to commit and push directly to main
git checkout main
git commit --allow-empty -m "test: branch protection"
git push origin main
```

**Expected result:**
```
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Changes must be made through a pull request.
To https://github.com/user/repo.git
 ! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs to 'https://github.com/user/repo.git'
```

✅ If you see this error, protection is working correctly!

### Test 2: Create PR Workflow

```bash
# Proper workflow (should succeed)
git checkout contrib/<your-username>
git commit --allow-empty -m "test: PR workflow"
git push origin contrib/<your-username>

# Create PR via GitHub UI or gh CLI
gh pr create --base main --title "Test PR" --body "Testing branch protection"
```

**Expected result:**
- PR created successfully
- GitHub shows "Merging is blocked" until status checks pass (if configured)
- After checks pass, merge button becomes active (no approval required)

✅ If PR can be merged after status checks pass, protection is working!

## Summary of Protection Rules

| Branch | Rule | Purpose |
|--------|------|---------|
| `main` | Require PR before merge | All changes go through PR workflow |
| `main` | Require 0 approvals | Self-merge allowed (approval optional) |
| `main` | Require status checks | Tests/coverage/lint pass |
| `main` | Require conversation resolution | All comments addressed |
| `main` | No bypass | Even admins follow rules |
| `main` | No force push | Protect history |
| `main` | No deletion | Permanent branch |
| `develop` | Require PR before merge | All changes go through PR workflow |
| `develop` | Require 0 approvals | Self-merge allowed (approval optional) |
| `develop` | Require status checks | Tests/coverage/lint pass |
| `develop` | No force push | Protect history |
| `develop` | No deletion | Permanent branch |

## CI/CD Integration (Optional)

If you want to enforce quality gates automatically:

### GitHub Actions Example

Create `.github/workflows/quality-gates.yml`:

```yaml
name: Quality Gates

on:
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run tests
        run: uv run pytest --cov=src --cov-fail-under=80

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run linting
        run: uv run ruff check src/ tests/

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run type checking
        run: uv run mypy src/
```

After adding this workflow:
1. Push to your repository
2. Return to branch protection settings
3. Add status checks: `test`, `lint`, `type-check`
4. Now PRs must pass all checks before merge

## Troubleshooting

### Problem: "Branch protection rule not applying"

**Cause:** Rule pattern doesn't match branch name

**Fix:**
- Check pattern is exactly `main` (not `refs/heads/main`)
- Check branch exists (git branch -a)
- Pattern is case-sensitive

### Problem: "Can't merge even though checks pass"

**Cause:** Unresolved conversations or other blocking issues

**Fix:**
- Check "Conversation" tab - all comments resolved?
- Check "Files changed" tab - any unresolved review comments?
- Check status checks in "Checks" tab - all passing?
- Note: Approvals are optional (not required for merge)

### Problem: "Status checks never complete"

**Cause:** CI/CD workflow not configured or failing

**Fix:**
- Check "Actions" tab to see workflow runs
- Check workflow YAML syntax
- Check workflow has correct trigger (`pull_request`)
- Ensure workflow file is on base branch (main/develop)

### Problem: "Admin can't override protection"

**Cause:** "Do not allow bypassing" is enabled

**Fix:**
- If you need to override (emergency only):
  - Temporarily disable rule in settings
  - Make necessary changes
  - Re-enable rule immediately
- Better approach: Fix the issue properly with a PR

### Problem: "Force push blocked but I need to rebase"

**Cause:** Branch protection blocks force pushes

**Fix:**
- **Don't force push to main/develop** (by design)
- For feature branches: force push is allowed
- For contrib branches: use `--force-with-lease` (safer)
- For main/develop: Never force push (use revert instead)

## Alternative: Azure DevOps Branch Policies

If using Azure DevOps instead of GitHub, see equivalent configuration:

1. Navigate to: **Project → Repos → Branches → main → Branch policies**
2. Configure:
   - ☑️ Require a minimum number of reviewers: 0 (approval optional)
   - ☑️ Check for linked work items: Enabled (optional)
   - ☑️ Check for comment resolution: All comments
   - ☑️ Limit merge types: Squash merge or Merge commit
   - ☑️ Build validation: Add build policy (if pipeline configured)
3. Repeat for `develop` branch

## Additional Security

### Pre-push Hook (Local Safety Net)

Install pre-push hook to prevent accidental local pushes:

```bash
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

This adds local protection (before GitHub rejects).

### CODEOWNERS File (Optional)

Create `.github/CODEOWNERS` to require specific reviewers:

```
# Require workflow maintainers for skill changes
.claude/skills/           @stharrold
WORKFLOW.md              @stharrold

# Require docs team for documentation
*.md                     @docs-team

# Require security team for sensitive files
pyproject.toml           @security-team
.gitignore              @security-team
```

Then enable "Require review from Code Owners" in branch protection.

## Resources

- **GitHub Docs:** [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **GitHub Docs:** [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- **Workflow Guide:** [WORKFLOW.md](../WORKFLOW.md#branch-protection-policy)
- **Contributing Guide:** [CONTRIBUTING.md](../CONTRIBUTING.md#protected-branches)

## Questions?

If you encounter issues not covered here:

1. Check [GitHub Community](https://github.community/)
2. Review [WORKFLOW.md "Branch Protection Policy"](../WORKFLOW.md#branch-protection-policy)
3. Check repository's GitHub Issues
4. Ask repository maintainers

---

**Last updated:** 2025-11-04
**Version:** 1.0.0 (initial release with workflow v5.2)
