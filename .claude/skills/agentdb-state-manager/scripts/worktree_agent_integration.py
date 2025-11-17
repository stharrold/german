#!/usr/bin/env python3
"""Integration layer for MIT Agent Synchronization Pattern.

Provides non-invasive hooks for existing agents to trigger sync engine.

Components:
- FlowTokenManager: Maps workflow sessions to sync engine flow tokens
- PHIDetector: Detects Protected Health Information in state snapshots
- ComplianceWrapper: Wraps sync engine calls with healthcare compliance logging
- SyncEngineFactory: Creates sync engine instances with dependency injection
- trigger_sync_completion: Main entry point for agent hooks

Created: 2025-11-17
Issue: #161 - Phase 3 Integration Layer Implementation
"""

import asyncio
import logging
import os
import re
import subprocess
import uuid
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class FlowTokenType(Enum):
    """Types of flow tokens for different workflow contexts."""
    MAIN_REPO = "main_repo"
    WORKTREE = "worktree"
    ISSUE = "issue"
    AD_HOC = "ad_hoc"


class FlowTokenManager:
    """
    Maps workflow sessions to sync engine flow tokens.

    Flow tokens enable cross-worktree coordination and session tracking.
    Different workflow contexts generate different token formats:
    - Worktree: feature/<timestamp>_<slug>
    - Main repo (contrib): contrib/<user>
    - Issue-based: issue-<number>
    - Ad-hoc: ad-hoc-<uuid>
    """

    @staticmethod
    def get_flow_token() -> str:
        """
        Detect current workflow context and generate appropriate flow token.

        Returns:
            Flow token string (e.g., "contrib/stharrold", "feature/20251117_slug", "issue-161")
        """
        cwd = Path.cwd()

        # Check if in worktree (directory name pattern: german_feature_*)
        if cwd.name.startswith("german_feature_"):
            # Extract branch name from worktree directory
            # Example: german_feature_20251117T024349Z_phase-3-integration
            parts = cwd.name.split("_", 2)  # ["german", "feature", "20251117T024349Z_phase-3-integration"]
            if len(parts) >= 3:
                return f"feature/{parts[2]}"

        # Check if in main repo on contrib branch
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            branch = result.stdout.strip()
            if branch.startswith("contrib/"):
                return branch
            # Also accept claude/ branches for development
            if branch.startswith("claude/"):
                return branch
        except Exception as e:
            logger.warning(f"Failed to detect git branch: {e}")

        # Fallback: generate UUID for ad-hoc workflows
        return f"ad-hoc-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def extract_issue_number(flow_token: str) -> Optional[int]:
        """
        Extract issue number from flow token if present.

        Args:
            flow_token: Flow token string

        Returns:
            Issue number or None
        """
        # Pattern: issue-123 or feature/timestamp_issue-123-description
        match = re.search(r'issue-(\d+)', flow_token)
        if match:
            return int(match.group(1))
        return None


class PHIDetector:
    """
    Detects Protected Health Information (PHI) in state snapshots.

    Replaces stub in sync_engine.py _detect_phi() method.
    Uses conservative heuristics - false positives are acceptable
    (better to over-log than under-log for compliance).
    """

    # PHI field name patterns (case-insensitive)
    PHI_FIELD_PATTERNS = [
        r'patient_?id',
        r'mrn',
        r'medical_?record',
        r'ssn',
        r'social_?security',
        r'dob',
        r'date_?of_?birth',
        r'diagnosis',
        r'treatment',
        r'prescription',
        r'icd_?code',
        r'health_?record',
        r'phi_data',
        r'protected_?health'
    ]

    # PHI path patterns
    PHI_PATH_PATTERNS = [
        r'/data/protected/',
        r'/phi/',
        r'/medical/',
        r'/patient/',
        r'/health_?records/'
    ]

    # SSN regex: 123-45-6789 or 123456789
    SSN_PATTERN = r'\b\d{3}-?\d{2}-?\d{4}\b'

    @classmethod
    def detect_phi(cls, state_snapshot: Dict[str, Any]) -> bool:
        """
        Detect if state snapshot contains PHI.

        Detection Strategy:
        1. Explicit PHI marker: _contains_phi field
        2. Field name patterns: patient_id, mrn, ssn, etc.
        3. Value patterns: SSN regex
        4. Path patterns: /data/protected/, /phi/, etc.

        Args:
            state_snapshot: State data to check

        Returns:
            True if PHI detected, False otherwise
        """
        # Explicit PHI marker
        if state_snapshot.get("_contains_phi") is True:
            logger.info("PHI detected: explicit _contains_phi marker")
            return True

        # Check field names
        for field_name in state_snapshot.keys():
            for pattern in cls.PHI_FIELD_PATTERNS:
                if re.search(pattern, field_name, re.IGNORECASE):
                    logger.info(f"PHI detected: field name '{field_name}' matches pattern '{pattern}'")
                    return True

        # Check for SSN in string values
        for key, value in state_snapshot.items():
            if isinstance(value, str):
                if re.search(cls.SSN_PATTERN, value):
                    logger.info(f"PHI detected: SSN pattern in field '{key}'")
                    return True

        # Check for PHI paths in file paths
        for key, value in state_snapshot.items():
            if isinstance(value, str):
                for pattern in cls.PHI_PATH_PATTERNS:
                    if re.search(pattern, value, re.IGNORECASE):
                        logger.info(f"PHI detected: path '{value}' in field '{key}' matches pattern '{pattern}'")
                        return True

        return False

    @classmethod
    def extract_justification(cls, context: Dict[str, Any]) -> str:
        """
        Extract or generate access justification from workflow context.

        Priority:
        1. Explicit justification (phi_justification field)
        2. Issue number (from GitHub/Azure DevOps)
        3. Commit message (first line)
        4. Generic fallback (user + action)

        Args:
            context: Workflow context (commit message, issue, user, etc.)

        Returns:
            Justification string
        """
        # Priority 1: Explicit justification
        if "phi_justification" in context:
            return context["phi_justification"]

        # Priority 2: Issue number
        issue_num = context.get("issue_number")
        if issue_num:
            return f"Development work for issue #{issue_num}"

        # Priority 3: Commit message (first line)
        commit_msg = context.get("commit_message", "")
        if commit_msg:
            first_line = commit_msg.split("\n")[0][:100]  # First line, max 100 chars
            return f"Code change: {first_line}"

        # Priority 4: Generic development justification
        user = context.get("user", "unknown")
        action = context.get("action", "development")
        return f"{user} performing {action}"


class ComplianceWrapper:
    """
    Wraps sync engine calls with healthcare compliance logging.

    Responsibilities:
    - Detect PHI in state snapshots
    - Extract access justification
    - Log compliance warnings
    - Delegate to sync engine
    """

    def __init__(self, sync_engine):
        """
        Initialize compliance wrapper.

        Args:
            sync_engine: SynchronizationEngine instance
        """
        self.sync_engine = sync_engine

    async def on_agent_action_complete(
        self,
        agent_id: str,
        action: str,
        flow_token: str,
        state_snapshot: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Wrapped version of sync_engine.on_agent_action_complete with compliance logging.

        Args:
            agent_id: Agent performing action
            action: Action completed (e.g., "commit_complete")
            flow_token: Workflow session identifier
            state_snapshot: State data
            context: Additional context for compliance (user, issue, commit message)

        Returns:
            List of execution IDs (UUIDs) for triggered synchronizations
        """
        context = context or {}

        # Detect PHI
        phi_detected = PHIDetector.detect_phi(state_snapshot)

        # Extract justification if PHI detected
        phi_justification = None
        if phi_detected:
            phi_justification = PHIDetector.extract_justification(context)
            logger.warning(f"PHI detected in sync for agent={agent_id}, action={action}")
            logger.info(f"PHI justification: {phi_justification}")

            # Check if justification is present
            if not phi_justification or phi_justification.startswith("unknown performing"):
                logger.error(
                    f"PHI detected but no proper justification provided - potential compliance violation! "
                    f"agent={agent_id}, action={action}"
                )

        # Call sync engine
        # Note: We're calling the synchronous method but wrapping it in async for future compatibility
        try:
            execution_ids = await asyncio.to_thread(
                self.sync_engine.on_agent_action_complete,
                agent_id=agent_id,
                action=action,
                flow_token=flow_token,
                state_snapshot=state_snapshot
            )
        except Exception as e:
            logger.error(f"Sync engine call failed: {e}", exc_info=True)
            raise

        return execution_ids


class SyncEngineFactory:
    """
    Factory for creating sync engine instances with dependency injection.

    Supports:
    - Feature flag control (SYNC_ENGINE_ENABLED)
    - Database path configuration (AGENTDB_PATH)
    - Graceful degradation on errors
    """

    _instance: Optional[ComplianceWrapper] = None
    _db_path: Optional[str] = None

    @classmethod
    def create_sync_engine(cls, db_path: Optional[str] = None) -> Optional[ComplianceWrapper]:
        """
        Create sync engine instance if enabled.

        Uses singleton pattern to reuse connection across calls.

        Args:
            db_path: Path to DuckDB database (optional, defaults to AGENTDB_PATH env var)

        Returns:
            ComplianceWrapper instance or None if disabled
        """
        # Check feature flag
        enabled = os.getenv("SYNC_ENGINE_ENABLED", "false").lower() == "true"

        if not enabled:
            logger.debug("Sync engine disabled (SYNC_ENGINE_ENABLED=false)")
            return None

        # Use provided db_path or environment variable or default
        if db_path is None:
            db_path = os.getenv("AGENTDB_PATH", "agentdb.duckdb")

        # Return existing instance if same db_path
        if cls._instance is not None and cls._db_path == db_path:
            logger.debug("Reusing existing sync engine instance")
            return cls._instance

        try:
            # Import sync engine (delayed to avoid import if disabled)
            from sync_engine import SynchronizationEngine

            # Create engine
            logger.info(f"Initializing sync engine with db_path={db_path}")
            engine = SynchronizationEngine(db_path=db_path)

            # Wrap with compliance
            wrapper = ComplianceWrapper(engine)

            # Store as singleton
            cls._instance = wrapper
            cls._db_path = db_path

            logger.info("Sync engine enabled and initialized")
            return wrapper

        except ImportError as e:
            logger.error(f"Failed to import sync_engine module: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize sync engine: {e}", exc_info=True)
            return None

    @classmethod
    def reset(cls):
        """Reset singleton instance (for testing)."""
        if cls._instance is not None and hasattr(cls._instance.sync_engine, 'close'):
            try:
                cls._instance.sync_engine.close()
            except Exception as e:
                logger.warning(f"Error closing sync engine: {e}")
        cls._instance = None
        cls._db_path = None


async def trigger_sync_completion(
    agent_id: str,
    action: str,
    state_snapshot: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
    sync_engine: Optional[ComplianceWrapper] = None
) -> bool:
    """
    Trigger sync engine after agent action completes.

    This is the main entry point for agent hooks.

    Non-Invasive Integration:
    - Feature flag controlled (SYNC_ENGINE_ENABLED)
    - Graceful degradation on errors (returns False, doesn't raise)
    - Minimal overhead when disabled (~1 µs)

    Args:
        agent_id: Agent performing action (e.g., "develop", "assess")
        action: Action completed (e.g., "commit_complete", "test_complete")
        state_snapshot: State data (coverage, test results, etc.)
        context: Additional context (user, issue, commit message)
        sync_engine: Optional sync engine instance (created if None)

    Returns:
        True if sync triggered successfully, False otherwise

    Example:
        await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123", "coverage": 85},
            context={"user": "stharrold", "commit_message": "fix: bug"}
        )
    """
    # Get or create sync engine
    if sync_engine is None:
        sync_engine = SyncEngineFactory.create_sync_engine()

    # If disabled, return early
    if sync_engine is None:
        logger.debug(f"Sync skipped (disabled): agent={agent_id}, action={action}")
        return False

    try:
        # Get flow token
        flow_token = FlowTokenManager.get_flow_token()

        # Add flow token to context
        context = context or {}
        context["flow_token"] = flow_token

        # Trigger sync
        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id=agent_id,
            action=action,
            flow_token=flow_token,
            state_snapshot=state_snapshot,
            context=context
        )

        logger.info(
            f"Sync triggered: agent={agent_id}, action={action}, "
            f"flow_token={flow_token}, targets={len(execution_ids)}"
        )

        # Log execution IDs for debugging
        if execution_ids:
            for exec_id in execution_ids:
                logger.debug(f"Execution ID: {exec_id}")

        return True

    except Exception as e:
        logger.error(f"Sync trigger failed: {e}", exc_info=True)
        # Graceful degradation: don't crash the agent
        return False
