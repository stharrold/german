# Azure DevOps Branch Policies Setup Guide

This guide provides step-by-step instructions for configuring Azure DevOps branch policies for the `main` and `develop` branches.

## Why Branch Policies?

**Branch policies prevent:**
- Accidental deletion of `main` or `develop`
- Direct commits (bypassing review and quality gates)
- Force pushes that rewrite history
- Merging without required approvals or status checks

**Branch policies enforce:**
- Pull request workflow (all changes reviewed)
- Quality gates (tests, coverage, linting must pass)
- Work item linking (traceability to requirements)
- Linear history (clean merge commits)

## Prerequisites

- Azure DevOps organization and project created
- You have admin access to the repository
- Repository has `main` and `develop` branches
- Azure CLI (`az`) installed for automation (optional)

## Setup Instructions

### Step 1: Navigate to Branch Policies

1. Go to your Azure DevOps project
2. Click **Repos** in left sidebar
3. Click **Branches** in the Repos menu
4. Find the `main` branch
5. Click the **⋯** (three dots) next to the branch name
6. Click **Branch policies**

### Step 2: Configure `main` Branch Policies

#### Require a minimum number of reviewers

☑️ **Enable:** Require a minimum number of reviewers
- **Minimum number of reviewers:** `1` (or more for team repositories)
- ☑️ **Requestors can approve their own changes:** **UNCHECK THIS**
  - Prevents self-approval (critical for solo dev → team transition)
- ☑️ **Prohibit the most recent pusher from approving their own changes:** **CHECK THIS**
  - Ensures at least one other person reviews
- ☑️ **Allow completion even if some reviewers vote to wait or reject:** **UNCHECK THIS**
  - All reviewers must approve or abstain
- ☑️ **When new changes are pushed:** Reset all approval votes
  - Re-review required if PR changes after approval

#### Check for linked work items

☑️ **Enable:** Check for linked work items
- **Setting:** `Required` (or `Optional` for less strict enforcement)
- Ensures traceability: every change links to a work item/user story
- Helps with release notes and change tracking

#### Check for comment resolution

☑️ **Enable:** Check for comment resolution
- **Setting:** `All comments must be resolved`
- Ensures all review feedback is addressed before merge

#### Limit merge types

☑️ **Enable:** Limit merge types
- ☑️ **Allow basic merge (no fast-forward):** **CHECK THIS**
  - Creates merge commit (preserves branch history)
- ☐ **Allow squash merge:** Optional (clean history but loses commit detail)
- ☐ **Allow rebase and fast-forward:** **UNCHECK THIS**
  - Rebase rewrites history (dangerous for protected branches)
- ☐ **Allow rebase with merge commit:** Optional (hybrid approach)

#### Build validation

☑️ **Enable:** Build validation (if Azure Pipelines configured)

Click **+ Add build policy**:
- **Build pipeline:** Select your CI/CD pipeline (e.g., `quality-gates`)
- **Path filter:** Leave blank (applies to all changes)
- **Policy requirement:** `Required`
- **Build expiration:** `Immediately when main is updated`
- **Display name:** `Quality Gates (Tests, Coverage, Linting)`

Repeat for each required check:
- `test` pipeline - Test suite must pass
- `coverage` pipeline - Coverage ≥80% requirement
- `lint` pipeline - Linting must pass (ruff)
- `type-check` pipeline - Type checking must pass (mypy)

☐ Skip if you don't have Azure Pipelines yet (you can add later)

#### Status checks

☑️ **Enable:** Status checks (if external CI/CD like GitHub Actions)
- Add external status checks from GitHub Actions, Jenkins, etc.
- Requires webhook integration with Azure DevOps

#### Automatically include code reviewers

☐ **Optional:** Automatically include code reviewers
- Add specific reviewers or groups
- Useful for CODEOWNERS-like behavior

**Save all changes** by clicking the back arrow (policies auto-save)

### Step 3: Configure `develop` Branch Policies

Repeat Step 2 for the `develop` branch:

1. Navigate to **Repos → Branches**
2. Find `develop` branch
3. Click **⋯ → Branch policies**
4. Configure same policies as `main`:

#### Require a minimum number of reviewers

☑️ **Enable:** Require a minimum number of reviewers
- **Minimum number of reviewers:** `1`
- ☑️ **Requestors can approve their own changes:** **UNCHECK THIS**
- ☑️ **Prohibit the most recent pusher from approving their own changes:** **CHECK THIS**
- ☑️ **When new changes are pushed:** Reset all approval votes

#### Check for linked work items

☑️ **Enable:** Check for linked work items
- **Setting:** `Required` (or `Optional` for less strict)

#### Check for comment resolution

☑️ **Enable:** Check for comment resolution
- **Setting:** `All comments must be resolved`

#### Limit merge types

☑️ **Enable:** Limit merge types
- ☑️ **Allow basic merge (no fast-forward)**
- ☐ **Allow rebase and fast-forward:** **UNCHECK THIS**

#### Build validation

☑️ **Enable:** Build validation (if Azure Pipelines configured)
- Add same pipelines as `main` branch

**Save all changes**

## Verification

After configuring both branches, verify policies are active:

### Test 1: Attempt Direct Commit to Main

```bash
# Try to commit and push directly to main
git checkout main
git commit --allow-empty -m "test: branch policy"
git push origin main
```

**Expected result:**
```
remote:
remote: The following policies are not met:
remote:
remote:   [main] Require a pull request before merging.
remote:
remote: Policy enforcement: https://dev.azure.com/org/project/_git/repo/policy?_a=branchpolicy&branch=refs/heads/main
To https://dev.azure.com/org/project/_git/repo
 ! [remote rejected] main -> main (TF402455: Pushes to this branch are not permitted; you must use a pull request to update this branch.)
error: failed to push some refs to 'https://dev.azure.com/org/project/_git/repo'
```

✅ If you see this error, policies are working correctly!

### Test 2: Create PR Workflow

```bash
# Proper workflow (should succeed)
git checkout contrib/<your-username>
git commit --allow-empty -m "test: PR workflow"
git push origin contrib/<your-username>

# Create PR via Azure DevOps UI or az CLI
az repos pr create --repository repo \
  --source-branch contrib/<your-username> \
  --target-branch main \
  --title "Test PR" \
  --description "Testing branch policies"
```

**Expected result:**
- PR created successfully
- Azure DevOps shows policies as "Not met" or "Pending"
- After approval and checks pass, "Complete" button becomes active

✅ If PR requires approval before merge, policies are working!

### Test 3: Verify Policy Dashboard

1. Navigate to **Project Settings → Repos → Policies**
2. You should see:
   - `main` branch with policies icon (🛡️)
   - `develop` branch with policies icon (🛡️)
3. Click each branch to view configured policies

## Summary of Branch Policies

| Branch | Policy | Purpose |
|--------|--------|---------|
| `main` | Require minimum reviewers: 1 | At least 1 reviewer must approve |
| `main` | No self-approval | Prevents requestor from approving own PR |
| `main` | Check for linked work items | Traceability to requirements |
| `main` | Check for comment resolution | All comments addressed |
| `main` | Limit merge types | Only basic merge (no rebase) |
| `main` | Build validation | Tests/coverage/lint pass |
| `main` | Reset votes on new changes | Re-review after updates |
| `develop` | Require minimum reviewers: 1 | At least 1 reviewer must approve |
| `develop` | No self-approval | Prevents requestor from approving own PR |
| `develop` | Check for linked work items | Traceability to requirements |
| `develop` | Check for comment resolution | All comments addressed |
| `develop` | Limit merge types | Only basic merge (no rebase) |
| `develop` | Build validation | Tests/coverage/lint pass |
| `develop` | Reset votes on new changes | Re-review after updates |

## Azure Pipelines Integration (Recommended)

Enforce quality gates automatically with Azure Pipelines:

### Pipeline YAML Example

Create `azure-pipelines-quality-gates.yml`:

```yaml
# Quality Gates Pipeline for Pull Requests
trigger: none  # Only run on PRs

pr:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - README.md
      - CHANGELOG.md

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: QualityGates
    displayName: 'Quality Gates'
    jobs:
      - job: Test
        displayName: 'Run Tests with Coverage'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
            displayName: 'Use Python 3.11'

          - script: |
              pip install uv
              uv sync
            displayName: 'Install dependencies'

          - script: |
              uv run pytest --cov=src --cov-report=xml --cov-report=term --cov-fail-under=80
            displayName: 'Run tests (≥80% coverage required)'

          - task: PublishCodeCoverageResults@1
            inputs:
              codeCoverageTool: 'Cobertura'
              summaryFileLocation: '$(System.DefaultWorkingDirectory)/coverage.xml'
            displayName: 'Publish coverage report'

      - job: Lint
        displayName: 'Run Linting'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
            displayName: 'Use Python 3.11'

          - script: |
              pip install uv
              uv sync
            displayName: 'Install dependencies'

          - script: |
              uv run ruff check src/ tests/
            displayName: 'Run ruff linting'

      - job: TypeCheck
        displayName: 'Run Type Checking'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
            displayName: 'Use Python 3.11'

          - script: |
              pip install uv
              uv sync
            displayName: 'Install dependencies'

          - script: |
              uv run mypy src/
            displayName: 'Run mypy type checking'
```

### Setting up the Pipeline

1. **Create pipeline:**
   - Navigate to **Pipelines → New pipeline**
   - Select your repository
   - Select **Existing Azure Pipelines YAML file**
   - Choose `azure-pipelines-quality-gates.yml`
   - Click **Save** (don't run yet)

2. **Add build policy to branches:**
   - Navigate to **Repos → Branches → main → Branch policies**
   - Click **+ Add build policy**
   - **Build pipeline:** Select `quality-gates` pipeline
   - **Policy requirement:** `Required`
   - **Build expiration:** `Immediately when main is updated`
   - Click **Save**

3. **Repeat for `develop` branch**

Now all PRs to `main` and `develop` must pass quality gates before merge.

## Comparison: Azure DevOps vs GitHub

| Feature | Azure DevOps | GitHub | Notes |
|---------|--------------|--------|-------|
| **PR required** | ✓ Require min reviewers | ✓ Require PR before merge | Same outcome |
| **Approvals** | ✓ Min 1+ reviewers | ✓ Required approvals: 1+ | Same |
| **No self-approval** | ✓ Configurable | ✓ Configurable | Azure DevOps has "no most recent pusher" option |
| **Comment resolution** | ✓ All comments | ✓ Require conversation resolution | Same |
| **Status checks** | ✓ Build validation | ✓ Require status checks | Azure uses pipelines, GitHub uses Actions |
| **Work items** | ✓ Check for linked work items | ✗ Not built-in | Azure DevOps advantage (traceability) |
| **Merge types** | ✓ Configurable | ✓ Configurable | Both support merge, squash, rebase |
| **CODEOWNERS** | ✓ Auto-include reviewers | ✓ CODEOWNERS file | Similar capability |
| **Reset approvals** | ✓ On new push | ✓ Dismiss stale approvals | Same |

**Key difference:** Azure DevOps has native work item linking, GitHub requires manual issue references in commits.

## Troubleshooting

### Problem: "Policy not enforced on push"

**Cause:** Policies apply to pull requests, not direct pushes

**Fix:**
- Policies don't block local pushes (by design)
- They block completion of PRs that don't meet requirements
- For stricter enforcement, also enable repository-level permissions

### Problem: "Can't complete PR even though all policies are green"

**Cause:** Additional policies or required reviewers

**Fix:**
- Check all tabs: Overview, Files, Commits, Policies
- Ensure all required reviewers have approved (not just minimum)
- Check "Automatically include code reviewers" policy
- Ensure all comments are resolved

### Problem: "Build validation never completes"

**Cause:** Pipeline not configured for PR trigger

**Fix:**
- Check pipeline YAML has `pr:` trigger configured
- Ensure pipeline is saved (not draft)
- Check pipeline run history in **Pipelines** tab
- Verify pipeline has access to repository (permissions)

### Problem: "Work item linking fails but none are needed"

**Cause:** Policy set to "Required"

**Fix:**
- Change policy to "Optional" if work items not used
- Or create a simple work item and link it to PR
- Or disable the policy entirely

### Problem: "Policy blocks merge but I'm an admin"

**Cause:** Azure DevOps policies apply to everyone by default

**Fix:**
- **Option 1:** Configure policy exemptions for specific users/groups
  - In branch policy settings, scroll to bottom
  - Add exempted users under "Exempt from policy"
- **Option 2:** Temporarily disable policy (emergency only)
- **Better:** Follow proper PR workflow (policies exist for a reason)

### Problem: "Multiple pipelines required but only one configured"

**Cause:** Need separate build policies for each quality gate

**Fix:**
- Create separate pipelines or separate jobs
- Add each pipeline as a distinct build policy
- All build policies must pass before merge

### Problem: "Repository-level vs branch-level permissions confusion"

**Cause:** Two layers of control in Azure DevOps

**Fix:**
- **Repository permissions:** Control who can read/write/admin
  - Navigate to **Project Settings → Repos → Repositories → Security**
- **Branch policies:** Control PR workflow for specific branches
  - Navigate to **Repos → Branches → Branch policies**
- Both layers must be configured correctly

## CLI Automation (Advanced)

Configure policies via Azure CLI for automation:

### Install Azure DevOps CLI Extension

```bash
az extension add --name azure-devops
```

### Configure Default Organization

```bash
az devops configure --defaults organization=https://dev.azure.com/YourOrg project=YourProject
```

### Create Minimum Reviewer Policy

```bash
# For main branch
az repos policy approver-count create \
  --repository-id <repo-id> \
  --branch main \
  --minimum-approver-count 1 \
  --creator-vote-counts false \
  --allow-downvotes false \
  --reset-on-source-push true \
  --enabled true

# For develop branch
az repos policy approver-count create \
  --repository-id <repo-id> \
  --branch develop \
  --minimum-approver-count 1 \
  --creator-vote-counts false \
  --allow-downvotes false \
  --reset-on-source-push true \
  --enabled true
```

### Create Comment Resolution Policy

```bash
# For main
az repos policy comment-required create \
  --repository-id <repo-id> \
  --branch main \
  --enabled true

# For develop
az repos policy comment-required create \
  --repository-id <repo-id> \
  --branch develop \
  --enabled true
```

### Create Build Validation Policy

```bash
# For main
az repos policy build create \
  --repository-id <repo-id> \
  --branch main \
  --build-definition-id <pipeline-id> \
  --display-name "Quality Gates" \
  --queue-on-source-update-only true \
  --manual-queue-only false \
  --valid-duration 0 \
  --enabled true

# For develop (same)
az repos policy build create \
  --repository-id <repo-id> \
  --branch develop \
  --build-definition-id <pipeline-id> \
  --display-name "Quality Gates" \
  --queue-on-source-update-only true \
  --manual-queue-only false \
  --valid-duration 0 \
  --enabled true
```

### List All Policies

```bash
# List all policies for repository
az repos policy list --repository-id <repo-id>

# List policies for specific branch
az repos policy list --repository-id <repo-id> --branch main
```

## Additional Security

### Repository Permissions

Configure who can bypass policies (use sparingly):

1. Navigate to **Project Settings → Repos → Repositories → [Your Repo] → Security**
2. Find "Bypass policies when pushing" permission
3. Set to **Deny** for all groups except administrators (if needed)

**Recommendation:** Set to **Deny** for everyone to enforce policies strictly.

### Pre-push Hook (Local Safety Net)

Install pre-push hook to prevent accidental local pushes:

```bash
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

This adds local protection before Azure DevOps rejects.

### Required Reviewers (Advanced)

Configure specific people/groups that MUST approve PRs:

1. Navigate to **Repos → Branches → main → Branch policies**
2. Click **+ Add automatic reviewers**
3. Configure:
   - **Reviewers:** Add users or groups
   - **Path filter:** Optionally filter by file paths (e.g., `.claude/skills/*`)
   - **Policy requirement:** Required or optional
   - **For pull requests affecting these folders:** Select paths
4. Click **Save**

Example: Require workflow maintainers for skill changes:
- **Reviewers:** stharrold
- **Path filter:** `.claude/skills/*`, `WORKFLOW.md`
- **Policy requirement:** Required

## VCS Abstraction Layer

This repository's workflow scripts support both GitHub (gh CLI) and Azure DevOps (az CLI):

### GitHub CLI (`gh`)
```bash
# Install
brew install gh  # macOS
# or https://cli.github.com/

# Authenticate
gh auth login

# Create PR
gh pr create --base main --head feature/my-feature --title "..." --body "..."
```

### Azure DevOps CLI (`az`)
```bash
# Install
pip install azure-cli
az extension add --name azure-devops

# Authenticate
az login
az devops configure --defaults organization=... project=...

# Create PR
az repos pr create --repository repo \
  --source-branch feature/my-feature \
  --target-branch main \
  --title "..." \
  --description "..."
```

### Workflow Script Detection

Workflow scripts automatically detect available CLI:

```python
# From backmerge_release.py
try:
    subprocess.run(['gh', '--version'], capture_output=True, check=True)
    use_gh = True
except (subprocess.CalledProcessError, FileNotFoundError):
    use_gh = False

if not use_gh:
    try:
        subprocess.run(['az', '--version'], capture_output=True, check=True)
        use_az = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("Neither gh nor az CLI available")
```

## Resources

- **Azure DevOps Docs:** [Branch policies overview](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- **Azure DevOps Docs:** [Branch policy reference](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies-overview)
- **Azure CLI Docs:** [az repos policy](https://learn.microsoft.com/en-us/cli/azure/repos/policy)
- **Workflow Guide:** [WORKFLOW.md](../WORKFLOW.md#branch-protection-policy)
- **Contributing Guide:** [CONTRIBUTING.md](../CONTRIBUTING.md#protected-branches)
- **GitHub Alternative:** [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)

## Migration from GitHub

If migrating from GitHub to Azure DevOps:

1. **Export GitHub branch protection rules** (manually document them)
2. **Map GitHub features to Azure DevOps:**
   - "Require PR" → "Require minimum reviewers"
   - "Required approvals" → "Minimum number of reviewers"
   - "Dismiss stale approvals" → "Reset votes on new changes"
   - "Require status checks" → "Build validation"
   - "CODEOWNERS" → "Automatically include code reviewers"
3. **Configure Azure Pipelines** equivalent to GitHub Actions
4. **Test thoroughly** before enforcing policies

## Questions?

If you encounter issues not covered here:

1. Check [Azure DevOps Community](https://developercommunity.visualstudio.com/AzureDevOps)
2. Review [WORKFLOW.md "Branch Protection Policy"](../WORKFLOW.md#branch-protection-policy)
3. Check repository's Azure DevOps Issues/Work Items
4. Ask repository maintainers

---

**Last updated:** 2025-11-07
**Version:** 1.0.0 (initial release with workflow v5.2)
