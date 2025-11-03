---
type: workflow-manifest
workflow_type: feature
slug: azure-devops-cli
timestamp: 20251103T170721Z
github_user: stharrold

metadata:
  title: "Azure DevOps CLI Support"
  description: "Add Azure DevOps CLI (az) support alongside GitHub CLI (gh) through VCS provider abstraction"
  created: "2025-11-03T17:07:21Z"
  stack: python
  package_manager: uv
  test_framework: pytest
  containers: []
  vcs_providers: ["github", "azure_devops"]

workflow_progress:
  phase: 1
  current_step: "1.0"
  last_task: null
  last_update: "2025-11-03T17:07:21Z"
  status: "pending"

quality_gates:
  test_coverage: 80
  tests_passing: false
  build_successful: false
  linting_clean: false
  types_clean: false
  semantic_version: "1.5.0"

tasks:
  implementation:
    # Phase 1: Foundation - VCS Abstraction Layer
    - id: impl_001
      description: "Create VCS abstraction module structure (.claude/skills/workflow-utilities/scripts/vcs/)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/__init__.py
      dependencies: []

    - id: impl_002
      description: "Implement VCSProvider enum and detection logic (provider.py)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/provider.py
      dependencies: [impl_001]
      notes: |
        - Enum: GITHUB, AZURE_DEVOPS
        - detect_from_remote(): Parse git remote URL
        - detect_from_config(): Load from .vcs_config.yaml

    - id: impl_003
      description: "Implement configuration loading and validation (config.py)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/config.py
      dependencies: [impl_001]
      notes: |
        - load_vcs_config(): Read .vcs_config.yaml
        - validate_config(): Validate provider-specific settings
        - Error handling for missing/invalid config

    - id: impl_004
      description: "Create BaseVCSAdapter abstract class (base_adapter.py)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/base_adapter.py
      dependencies: [impl_001]
      notes: |
        Abstract methods:
        - check_authentication() -> bool
        - get_current_user() -> str
        - create_pull_request(source, target, title, body) -> str

    - id: impl_005
      description: "Implement GitHubAdapter with gh CLI commands (github_adapter.py)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/github_adapter.py
      dependencies: [impl_004]
      notes: |
        Commands:
        - check_authentication: gh auth status
        - get_current_user: gh api user --jq '.login'
        - create_pull_request: gh pr create --base X --head Y --title T --body B

    - id: impl_006
      description: "Implement AzureDevOpsAdapter with az CLI commands (azure_adapter.py)"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/azure_adapter.py
      dependencies: [impl_004]
      notes: |
        Requires: organization, project from config
        Commands:
        - check_authentication: az account show
        - get_current_user: az devops user show --user me --query user.emailAddress
        - create_pull_request: az repos pr create --source-branch X --target-branch Y

    - id: impl_007
      description: "Create get_vcs_adapter() factory function in __init__.py"
      status: pending
      completed_at: null
      files:
        - .claude/skills/workflow-utilities/scripts/vcs/__init__.py
      dependencies: [impl_002, impl_003, impl_005, impl_006]
      notes: |
        Logic:
        1. Try load config → use specified provider
        2. Try detect from git remote
        3. Default to GitHub
        Returns: GitHubAdapter or AzureDevOpsAdapter instance

    # Phase 2: Script Integration
    - id: impl_008
      description: "Update initialize_repository.py to use VCS adapter"
      status: pending
      completed_at: null
      files:
        - .claude/skills/initialize-repository/scripts/initialize_repository.py
      dependencies: [impl_007]
      notes: |
        Line 303: Replace gh api user with vcs.get_current_user()
        Add: from vcs import get_vcs_adapter
        Handle errors from VCS adapter

    - id: impl_009
      description: "Update create_worktree.py to use VCS adapter"
      status: pending
      completed_at: null
      files:
        - .claude/skills/git-workflow-manager/scripts/create_worktree.py
      dependencies: [impl_007]
      notes: |
        Lines 103-113: Replace gh api user with vcs.get_current_user()
        Update error messages to be provider-agnostic

    - id: impl_010
      description: "Update create_release.py to use VCS adapter"
      status: pending
      completed_at: null
      files:
        - .claude/skills/git-workflow-manager/scripts/create_release.py
      dependencies: [impl_007]
      notes: |
        Lines 295-302: Replace gh api user with vcs.get_current_user()
        Update error handling

  testing:
    # Phase 3: Testing
    - id: test_001
      description: "Write VCS provider detection tests (test_vcs_provider.py)"
      status: pending
      completed_at: null
      files:
        - tests/skills/test_vcs_provider.py
      dependencies: [impl_002]
      test_cases: |
        - test_detect_github_from_https_url
        - test_detect_github_from_ssh_url
        - test_detect_azuredevops_from_https_url
        - test_detect_azuredevops_from_ssh_url
        - test_detect_from_config_github
        - test_detect_from_config_azuredevops
        - test_fallback_to_github

    - id: test_002
      description: "Write VCS adapter tests (test_vcs_adapters.py)"
      status: pending
      completed_at: null
      files:
        - tests/skills/test_vcs_adapters.py
      dependencies: [impl_005, impl_006]
      test_cases: |
        GitHub Adapter:
        - test_github_check_authentication_success
        - test_github_check_authentication_failure
        - test_github_get_current_user
        - test_github_create_pull_request

        Azure DevOps Adapter:
        - test_azure_check_authentication_success
        - test_azure_check_authentication_failure
        - test_azure_get_current_user
        - test_azure_create_pull_request
        - test_azure_requires_org_and_project

    - id: test_003
      description: "Write integration tests with subprocess mocks (test_vcs_integration.py)"
      status: pending
      completed_at: null
      files:
        - tests/skills/test_vcs_integration.py
      dependencies: [impl_007]
      test_cases: |
        - test_get_adapter_github_from_config
        - test_get_adapter_azuredevops_from_config
        - test_get_adapter_github_from_remote
        - test_get_adapter_azuredevops_from_remote
        - test_end_to_end_github_workflow
        - test_end_to_end_azuredevops_workflow
        - test_error_handling_missing_cli
        - test_error_handling_not_authenticated

    - id: test_004
      description: "Write configuration tests (test_vcs_config.py)"
      status: pending
      completed_at: null
      files:
        - tests/skills/test_vcs_config.py
      dependencies: [impl_003]
      test_cases: |
        - test_load_valid_github_config
        - test_load_valid_azuredevops_config
        - test_load_missing_config_returns_none
        - test_validate_github_config
        - test_validate_azuredevops_config_requires_org
        - test_validate_azuredevops_config_requires_project
        - test_invalid_provider_raises_error
        - test_malformed_yaml_raises_error

  documentation:
    # Phase 4: Documentation
    - id: doc_001
      description: "Update CLAUDE.md with VCS configuration guidance"
      status: pending
      completed_at: null
      files:
        - CLAUDE.md
      dependencies: [impl_010]
      notes: |
        Sections to add/update:
        - Prerequisites: Add az CLI as alternative to gh CLI
        - Common Development Commands: Add .vcs_config.yaml setup
        - VCS Configuration section (new)

    - id: doc_002
      description: "Update WORKFLOW.md with dual CLI examples (GitHub and Azure DevOps)"
      status: pending
      completed_at: null
      files:
        - WORKFLOW.md
      dependencies: [impl_010]
      notes: |
        Update all gh command examples:
        - Authentication checks
        - PR creation commands
        - Add Azure DevOps equivalents side-by-side

    - id: doc_003
      description: "Update README.md prerequisites section"
      status: pending
      completed_at: null
      files:
        - README.md
      dependencies: [impl_010]
      notes: |
        Prerequisites:
        - GitHub CLI (gh) OR Azure DevOps CLI (az)
        - Link to authentication setup for both

    - id: doc_004
      description: "Update CONTRIBUTING.md with Azure DevOps setup instructions"
      status: pending
      completed_at: null
      files:
        - CONTRIBUTING.md
      dependencies: [impl_010]
      notes: |
        Sections:
        - Setup for Azure DevOps users
        - Fork workflow alternatives
        - PR creation for Azure DevOps

    - id: doc_005
      description: "Update git-workflow-manager/SKILL.md"
      status: pending
      completed_at: null
      files:
        - .claude/skills/git-workflow-manager/SKILL.md
      dependencies: [impl_010]
      notes: |
        Update PR creation examples with dual commands
        Add Azure DevOps configuration notes

    - id: doc_006
      description: "Update initialize-repository/SKILL.md"
      status: pending
      completed_at: null
      files:
        - .claude/skills/initialize-repository/SKILL.md
      dependencies: [impl_010]
      notes: |
        Update validation requirements
        Add Azure DevOps CLI as alternative requirement

    - id: doc_007
      description: "Create .vcs_config.yaml.example with both providers"
      status: pending
      completed_at: null
      files:
        - .vcs_config.yaml.example
      dependencies: [impl_003]
      notes: |
        Include:
        - GitHub example (minimal config)
        - Azure DevOps example (with org + project)
        - Comments explaining each field

    - id: doc_008
      description: "Create Azure DevOps migration guide"
      status: pending
      completed_at: null
      files:
        - docs/azure-devops-migration.md
      dependencies: [impl_010, doc_001, doc_002]
      notes: |
        Guide contents:
        - Installing Azure DevOps CLI
        - Authentication setup
        - Creating .vcs_config.yaml
        - Testing configuration
        - Troubleshooting common issues

  qa:
    # Phase 5: Quality Assurance
    - id: qa_001
      description: "Run full test suite and verify ≥80% coverage"
      status: pending
      completed_at: null
      files: []
      dependencies: [test_001, test_002, test_003, test_004]
      notes: |
        Commands:
        - uv run pytest --cov=.claude/skills/workflow-utilities/scripts/vcs --cov-fail-under=80
        - uv run pytest tests/skills/test_vcs_*.py -v

    - id: qa_002
      description: "Manual testing with GitHub CLI (backward compatibility)"
      status: pending
      completed_at: null
      files: []
      dependencies: [impl_010, doc_001]
      notes: |
        Test scenarios:
        - Initialize new repository (no config file)
        - Create worktree
        - Create release
        - Verify all existing workflows work unchanged

    - id: qa_003
      description: "Manual testing with Azure DevOps CLI (if available)"
      status: pending
      completed_at: null
      files: []
      dependencies: [impl_010, doc_007]
      notes: |
        Test scenarios:
        - Create .vcs_config.yaml with Azure DevOps settings
        - Initialize repository
        - Create worktree
        - Verify username detection
        - (PR creation requires actual Azure DevOps repo)

  integration:
    # Phase 6: Integration and Polish
    - id: intg_001
      description: "Run quality gates (lint, type check, build)"
      status: pending
      completed_at: null
      files: []
      dependencies: [qa_001, qa_002]
      notes: |
        Commands:
        - uv run ruff check .claude/skills/workflow-utilities/scripts/vcs/
        - uv run mypy .claude/skills/workflow-utilities/scripts/vcs/
        - python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

    - id: intg_002
      description: "Update TODO.md master manifest with this feature"
      status: pending
      completed_at: null
      files:
        - TODO.md
      dependencies: [intg_001]
      notes: |
        Register this workflow in active list:
        python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
          TODO_feature_20251103T170721Z_azure-devops-cli.md feature azure-devops-cli \
          --title "Azure DevOps CLI Support"

    - id: intg_003
      description: "Create feature worktree for implementation"
      status: pending
      completed_at: null
      files: []
      dependencies: []
      notes: |
        This task should be done BEFORE starting implementation:
        python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
          feature azure-devops-cli contrib/stharrold

    - id: intg_004
      description: "Commit changes and create PR to contrib/stharrold"
      status: pending
      completed_at: null
      files: []
      dependencies: [intg_001]
      notes: |
        From feature worktree:
        - git add all changes
        - git commit with semantic message
        - gh pr create --base contrib/stharrold --head feature/...

context_checkpoints: []
---

# TODO: Azure DevOps CLI Support (Feature)

## Overview

Add Azure DevOps CLI (`az`) support alongside GitHub CLI (`gh`) through a VCS provider abstraction layer. This enables the workflow system to work with both GitHub and Azure DevOps repositories without breaking existing GitHub workflows.

## Motivation

**Current state:** Workflow scripts hardcode GitHub CLI (`gh`) commands for:
- User authentication checking
- Current username detection
- Pull request creation

**Problem:** Users with Azure DevOps repositories cannot use the workflow system.

**Solution:** Create VCS provider abstraction with adapters for both GitHub and Azure DevOps.

## Required Reading for Implementation

This section lists files Claude Code should read before starting each phase to understand existing patterns and code to be modified.

### Before Phase 1: Foundation (impl_001 - impl_007)

**Understand existing script patterns:**
- `.claude/skills/workflow-utilities/scripts/directory_structure.py` - Script structure, argument parsing, error handling patterns
- `.claude/skills/workflow-utilities/scripts/deprecate_files.py` - Module imports, subprocess usage, validation patterns
- `.claude/skills/workflow-utilities/scripts/workflow_registrar.py` - YAML loading/parsing patterns (PyYAML usage)

**Understand subprocess patterns:**
- `.claude/skills/git-workflow-manager/scripts/create_worktree.py` lines 95-120 - How subprocess calls are structured, error handling
- `.claude/skills/git-workflow-manager/scripts/create_release.py` lines 285-310 - Subprocess with capture_output, text=True patterns

**Rationale:** Match coding style, error handling patterns, and subprocess usage conventions.

### Before Phase 2: Script Integration (impl_008 - impl_010)

**Files to modify - read completely:**
- `.claude/skills/initialize-repository/scripts/initialize_repository.py` lines 295-315 - Current `gh api user` usage, error handling
- `.claude/skills/git-workflow-manager/scripts/create_worktree.py` lines 95-125 - Current `gh api user` usage, authentication error messages
- `.claude/skills/git-workflow-manager/scripts/create_release.py` lines 285-310 - Current `gh api user` usage in TODO file context

**Understand what's being replaced:**
```python
# Current pattern in all three scripts:
result = subprocess.run(['gh', 'api', 'user', '--jq', '.login'],
                       capture_output=True, text=True, check=True)
github_user = result.stdout.strip()
```

**Rationale:** Ensure replacement with VCS adapter maintains exact same behavior and error handling.

### Before Phase 3: Testing (test_001 - test_004)

**Understand test patterns:**
- `tests/skills/test_create_release.py` - Complete file for test structure, pytest fixtures, mocking patterns
- `tests/test_models.py` - Pydantic validation testing patterns
- `tests/test_vocabulary_loader.py` - Error handling test patterns, pytest.raises usage

**Test execution patterns:**
```bash
# From existing tests, understand:
- How to use pytest.mark.skip for tests requiring external dependencies
- How to mock subprocess.run calls
- How to structure test classes and test functions
- How to use pytest fixtures
```

**Rationale:** Match existing test structure and achieve ≥80% coverage goal.

### Before Phase 4: Documentation (doc_001 - doc_008)

**Understand documentation style:**
- `CLAUDE.md` lines 195-295 - Command documentation format, examples structure
- `WORKFLOW.md` lines 180-220 - Step-by-step workflow documentation style
- `README.md` lines 1-50 - Prerequisites and quick start format
- `.claude/skills/git-workflow-manager/SKILL.md` lines 1-100 - Skill documentation structure

**Configuration file examples:**
- `.gitignore` - Example of configuration file in repo root
- `pyproject.toml` - TOML structure, comments style

**Rationale:** Match documentation voice, structure, and example format across all files.

### Before Phase 5: Quality Assurance (qa_001 - qa_003)

**Understand quality standards:**
- `CONTRIBUTING.md` complete file - Quality gates, testing requirements, PR standards
- `.claude/skills/quality-enforcer/SKILL.md` - Quality gate definitions, coverage requirements

**Rationale:** Understand ≥80% coverage requirement, lint rules, type checking expectations.

### Quick Reference: Files Modified by Line Number

**initialize_repository.py:**
- Line 58: `REQUIRED_TOOLS = ['git', 'gh']` → Add VCS adapter check
- Line 303-307: `gh api user` call → Replace with `vcs.get_current_user()`

**create_worktree.py:**
- Line 103-107: `gh api user` call → Replace with `vcs.get_current_user()`
- Line 113: Error message mentioning `gh auth login` → Make provider-agnostic

**create_release.py:**
- Line 295-302: `gh api user` call → Replace with `vcs.get_current_user()`

### Token Efficiency Note

**Reading strategy for Claude Code:**
1. **Phase 1:** Read 3-4 utility scripts to understand patterns (~1,500 tokens)
2. **Phase 2:** Read 3 scripts being modified, focus on specific line ranges (~800 tokens)
3. **Phase 3:** Read 3-4 test files to understand patterns (~1,200 tokens)
4. **Phase 4:** Read 4-5 documentation files to match style (~1,000 tokens)

**Total reading: ~4,500 tokens across 5 weeks** (instead of ~15,000 if reading entire files)

**Strategy:** Read targeted sections, not entire files. Use line number ranges provided above.

## Architecture

### VCS Abstraction Layer

```
┌─────────────────────────────────────┐
│   Workflow Scripts                  │
│   (create_worktree.py, etc.)       │
└─────────┬───────────────────────────┘
          │
          │ get_vcs_adapter()
          ▼
┌─────────────────────────────────────┐
│   VCS Provider Factory              │
│   - Detect from config              │
│   - Detect from git remote          │
│   - Default to GitHub               │
└─────────┬───────────────────────────┘
          │
          ├──────────────┬──────────────┐
          ▼              ▼              ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ GitHub  │    │ Azure   │    │ Future  │
    │ Adapter │    │ DevOps  │    │ (GitLab)│
    └─────────┘    └─────────┘    └─────────┘
```

### Configuration

**Option 1: Automatic detection (no config file)**
```bash
# Git remote determines provider
git remote get-url origin
# → https://github.com/user/repo → GitHub
# → https://dev.azure.com/org/project → Azure DevOps
```

**Option 2: Explicit configuration (.vcs_config.yaml)**
```yaml
vcs_provider: azure_devops

azure_devops:
  organization: "https://dev.azure.com/myorg"
  project: "MyProject"
```

## Implementation Plan

### Phase 1: Foundation (Week 1)
Create VCS abstraction module with:
- `BaseVCSAdapter` abstract class (3 methods: check_authentication, get_current_user, create_pull_request)
- `GitHubAdapter` (mirrors current behavior with `gh` CLI)
- `AzureDevOpsAdapter` (uses `az` CLI)
- Provider detection logic (config file → git remote → default GitHub)
- Configuration loading and validation

**Files created:**
- `.claude/skills/workflow-utilities/scripts/vcs/__init__.py` (factory function)
- `.claude/skills/workflow-utilities/scripts/vcs/provider.py` (enum, detection)
- `.claude/skills/workflow-utilities/scripts/vcs/config.py` (YAML loading)
- `.claude/skills/workflow-utilities/scripts/vcs/base_adapter.py` (ABC)
- `.claude/skills/workflow-utilities/scripts/vcs/github_adapter.py` (GitHub implementation)
- `.claude/skills/workflow-utilities/scripts/vcs/azure_adapter.py` (Azure DevOps implementation)

### Phase 2: Script Integration (Week 2)
Update workflow scripts to use VCS adapter:
- `initialize_repository.py` (line 303: username detection)
- `create_worktree.py` (lines 103-113: username detection, error messages)
- `create_release.py` (lines 295-302: username detection)

**Changes:**
```python
# Before (hardcoded GitHub):
result = subprocess.run(['gh', 'api', 'user', '--jq', '.login'], ...)

# After (abstracted):
from vcs import get_vcs_adapter
vcs = get_vcs_adapter()
github_user = vcs.get_current_user()
```

### Phase 3: Testing (Week 3)
Comprehensive test coverage:
- Unit tests for each adapter (GitHub, Azure DevOps)
- Integration tests with subprocess mocks
- Configuration loading/validation tests
- Provider detection tests

**Test files:**
- `tests/skills/test_vcs_provider.py` (detection logic)
- `tests/skills/test_vcs_adapters.py` (adapter commands)
- `tests/skills/test_vcs_integration.py` (end-to-end mocks)
- `tests/skills/test_vcs_config.py` (YAML parsing)

**Target:** ≥80% code coverage

### Phase 4: Documentation (Week 4)
Update all documentation with dual examples:
- `CLAUDE.md` - Prerequisites, VCS configuration section
- `WORKFLOW.md` - Dual CLI examples (GitHub and Azure DevOps)
- `README.md` - Prerequisites update
- `CONTRIBUTING.md` - Azure DevOps setup instructions
- Skill SKILL.md files - Updated command references
- Create `.vcs_config.yaml.example`
- Create Azure DevOps migration guide

### Phase 5: Quality Assurance (Week 5)
- Full test suite (≥80% coverage)
- Manual testing with GitHub CLI (backward compatibility)
- Manual testing with Azure DevOps CLI (if available)
- Quality gates: lint, type check, build
- PR creation and review

## VCS Command Mappings

| Operation | GitHub CLI | Azure DevOps CLI |
|-----------|-----------|------------------|
| Check auth | `gh auth status` | `az account show` |
| Get username | `gh api user --jq '.login'` | `az devops user show --user me --query user.emailAddress` |
| Create PR | `gh pr create --base X --head Y --title T --body B` | `az repos pr create --source-branch Y --target-branch X --title T --description B` |

## Backward Compatibility

**Critical requirement:** Zero breaking changes for existing GitHub users.

**Strategy:**
1. **Phase 1:** Add abstraction layer (no script changes yet)
2. **Phase 2:** Detect GitHub from git remote → use GitHub adapter (same behavior)
3. **Phase 3:** Azure DevOps only enabled via explicit `.vcs_config.yaml`
4. **Default:** If detection fails, default to GitHub (current behavior)

## Success Criteria

- ✅ All existing GitHub workflows work unchanged (no config file needed)
- ✅ Azure DevOps workflows supported via `.vcs_config.yaml`
- ✅ Test coverage ≥80%
- ✅ All quality gates passing (lint, type check, tests, build)
- ✅ Documentation updated with dual examples
- ✅ Zero breaking changes for current users
- ✅ Semantic version: v1.5.0 (MINOR - new feature, backward compatible)

## Migration Path for Azure DevOps Users

1. **Install Azure DevOps CLI:**
   ```bash
   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

   # Install Azure DevOps extension
   az extension add --name azure-devops
   ```

2. **Authenticate:**
   ```bash
   az login
   az devops configure --defaults organization=https://dev.azure.com/myorg project=MyProject
   ```

3. **Create configuration:**
   ```bash
   # In repository root
   cat > .vcs_config.yaml << 'EOF'
   vcs_provider: azure_devops

   azure_devops:
     organization: "https://dev.azure.com/myorg"
     project: "MyProject"
   EOF
   ```

4. **Test configuration:**
   ```bash
   # Should detect Azure DevOps
   python .claude/skills/workflow-utilities/scripts/vcs/provider.py detect
   ```

5. **Use workflows normally:**
   ```bash
   # All workflow commands work as documented
   python .claude/skills/bmad-planner/scripts/create_planning.py my-feature myuser
   ```

## Risk Mitigation

**High risk items:**
1. **Authentication differences** - Different auth patterns between `gh` and `az`
   - Mitigation: Abstract behind `check_authentication()` method
   - Each adapter handles its own auth checking

2. **PR creation output parsing** - Different output formats
   - Mitigation: Each adapter returns standardized string (PR URL)
   - Document expected output format per provider

3. **Error handling** - Different error codes/messages
   - Mitigation: Catch exceptions in adapters, raise standardized errors
   - Provider-agnostic error messages in scripts

**Medium risk items:**
1. **Configuration complexity** - Azure DevOps requires org + project
   - Mitigation: Clear validation with helpful error messages
   - Example config file with comments

2. **Testing coverage** - Comprehensive mocks needed
   - Mitigation: Follow existing test patterns (test_create_release.py)
   - Mock subprocess calls consistently

**Low risk items:**
1. **Git operations** - Unchanged (both providers use git CLI)
2. **Backward compatibility** - GitHub remains default
3. **File structure** - Clean separation of concerns

## Next Steps

**Before starting implementation:**
1. ✅ Research complete (this document)
2. ⏳ Create feature worktree: `python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature azure-devops-cli contrib/stharrold`
3. ⏳ Register in TODO.md: `python .claude/skills/workflow-utilities/scripts/workflow_registrar.py ...`
4. ⏳ Start Phase 1: Foundation (impl_001)

**Estimated timeline:** 4-5 weeks for complete implementation

**Recommended order:**
1. Week 1: Foundation (abstraction layer, both adapters)
2. Week 2: Script integration (3 scripts)
3. Week 3: Testing (4 test files, ≥80% coverage)
4. Week 4: Documentation (8 files + migration guide)
5. Week 5: QA + PR creation

## References

- **Azure DevOps CLI Docs:** https://learn.microsoft.com/en-us/cli/azure/devops
- **GitHub CLI Docs:** https://cli.github.com/manual/
- **Research:** Task agent analysis (2025-11-03)
- **Related Skills:** workflow-utilities, git-workflow-manager, initialize-repository
