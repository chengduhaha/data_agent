"""Agent execution harness (platform-wide controls)."""

from app.agent.harness.config import (
    HarnessConfig,
    load_harness_config,
    recursion_limit,
    step_limit,
    step_warn_threshold,
)
from app.agent.harness.evidence import get_evidence_snapshot, record_evidence
from app.agent.harness.hooks import HarnessHooks, harness_hooks
from app.agent.harness.middleware import ToolGovernanceMiddleware, reset_segment_state
from app.agent.harness.phases import RunPhaseMiddleware, get_run_phase
from app.agent.harness.prompts import HARNESS_SYSTEM_SUFFIX
from app.agent.harness.spill import LargeResultSpillMiddleware
from app.agent.harness.step_budget import StepBudgetMiddleware, get_segment_budget
from app.agent.harness.tool_budget import ToolBudgetMiddleware
from app.agent.harness.tools import make_search_knowledge_tool, make_wkb_query_tool
from app.agent.harness.wrapup import invoke_wrapup, stream_wrapup_tokens

__all__ = [
    "HARNESS_SYSTEM_SUFFIX",
    "HarnessConfig",
    "HarnessHooks",
    "LargeResultSpillMiddleware",
    "RunPhaseMiddleware",
    "StepBudgetMiddleware",
    "ToolBudgetMiddleware",
    "ToolGovernanceMiddleware",
    "get_evidence_snapshot",
    "get_run_phase",
    "get_segment_budget",
    "harness_hooks",
    "invoke_wrapup",
    "load_harness_config",
    "make_search_knowledge_tool",
    "make_wkb_query_tool",
    "record_evidence",
    "recursion_limit",
    "reset_segment_state",
    "step_limit",
    "step_warn_threshold",
    "stream_wrapup_tokens",
]
