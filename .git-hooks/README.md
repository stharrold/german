# Git Hooks Templates

This directory contains git hook templates for branch protection and workflow enforcement.

## Available Hooks

### pre-push

**Purpose:** Prevents direct pushes to protected branches (`main`, `develop`)

**Installation:**
```bash
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

**What it does:**
- Checks if you're pushing to `main` or `develop`
- If yes: Blocks the push with helpful error message
- If no: Allows the push normally

**Why this is helpful:**
- Catches accidental pushes before they reach GitHub
- Reminds you to create a pull request instead
- Provides clear instructions on correct workflow
- Faster feedback than waiting for GitHub to reject

**Testing the hook:**
```bash
# Test 1: Try to push to main (should fail)
git checkout main
git commit --allow-empty -m "test"
git push origin main
# Expected: Hook blocks with error message

# Test 2: Push to feature branch (should succeed)
git checkout contrib/<your-username>
git commit --allow-empty -m "test"
git push origin contrib/<your-username>
# Expected: Push succeeds normally
```

**Bypassing (emergency only):**
```bash
git push --no-verify origin main
```

⚠️ **WARNING:** Bypassing the hook doesn't bypass GitHub branch protection. The remote will still reject your push. Only bypass in true emergencies.

## How Git Hooks Work

**Git hooks are scripts that run automatically at certain points in the git workflow:**

1. **Template location:** `.git-hooks/` (this directory)
2. **Active location:** `.git/hooks/` (git's hook directory)
3. **Installation:** Copy template to active location + make executable
4. **Execution:** Git runs the hook script before/after certain operations

**Hook types:**
- `pre-commit` - Before creating a commit
- `pre-push` - Before pushing to remote
- `post-merge` - After merging branches
- `commit-msg` - Validate commit message format

**This repository provides:**
- `pre-push` - Branch protection enforcement

## Installation for All Contributors

**After cloning the repository:**

```bash
# Install all available hooks
cp .git-hooks/* .git/hooks/
chmod +x .git/hooks/*
```

**Or install selectively:**
```bash
# Install only pre-push hook
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Why .git-hooks/ Instead of .git/hooks/?

**Problem with .git/hooks/:**
- `.git/` directory is not tracked by git
- Hooks can't be shared via repository
- Each contributor must configure hooks manually

**Solution: .git-hooks/ directory:**
- Template hooks tracked in repository
- Contributors copy templates to `.git/hooks/`
- Consistent hook behavior across team
- Easy to update hooks (commit changes to templates)

## Creating New Hooks

**1. Create hook script in .git-hooks/:**
```bash
touch .git-hooks/pre-commit
chmod +x .git-hooks/pre-commit
```

**2. Write hook logic:**
```bash
#!/bin/bash
# Your hook code here
exit 0  # Success
exit 1  # Failure (blocks operation)
```

**3. Document in this README**

**4. Commit to repository:**
```bash
git add .git-hooks/pre-commit
git commit -m "feat: add pre-commit hook for ..."
```

**5. Contributors install:**
```bash
cp .git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Troubleshooting

### Problem: "Hook not running"

**Cause:** Hook not installed in `.git/hooks/` or not executable

**Fix:**
```bash
# Verify hook exists and is executable
ls -la .git/hooks/pre-push
# Should show: -rwxr-xr-x  (x = executable)

# If not executable:
chmod +x .git/hooks/pre-push

# If doesn't exist:
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### Problem: "Hook runs but doesn't work"

**Cause:** Script error or wrong shebang

**Fix:**
```bash
# Test hook directly
bash .git/hooks/pre-push

# Check for syntax errors
bash -n .git/hooks/pre-push

# Verify shebang
head -1 .git/hooks/pre-push
# Should be: #!/bin/bash
```

### Problem: "Want to disable hook temporarily"

**Fix:**
```bash
# Option 1: Rename hook (disable)
mv .git/hooks/pre-push .git/hooks/pre-push.disabled

# Option 2: Bypass for one push only
git push --no-verify origin branch-name

# Option 3: Delete hook
rm .git/hooks/pre-push
```

## Related Documentation

- **[WORKFLOW.md](../WORKFLOW.md#branch-protection-policy)** - Branch protection policy
- **[CONTRIBUTING.md](../CONTRIBUTING.md#protected-branches)** - Protected branches rules
- **[.github/BRANCH_PROTECTION.md](../.github/BRANCH_PROTECTION.md)** - GitHub protection setup
- **[Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)** - Official git hooks docs

---

**Note:** Hooks in this directory are templates. They must be installed to `.git/hooks/` to become active.
