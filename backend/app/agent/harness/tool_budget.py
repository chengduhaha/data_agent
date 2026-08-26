"""Per-tool call budgets declared by skill manifests (`harness.tool_budgets`).

Generic replacement for ad-hoc "≤12 SQL/run" enforcement: any tool name can
carry a budget (e.g. `run_query_safely: 12`, `wkb_query: 8`). When a tool
exceeds its budget for the current run segment, the call is blocked with a
structured forward instruction telling the model to synthesize.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import ToolMessage

from app.agent.harness.budget_registry import BudgetRegistry
from app.agent.harness.config import load_harness_config
from app.agent.harness.context import get_thread_segment
from app.agent.harness.forward_instruction import (
    BlockReason,
    ExpectedAction,
    ForwardInstruction,
)
from app.agent.harness.metrics import inc
from app.agent.harness.segment_manager import get_segment_state


def _tool_name(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("name") or "")
    return ""


def _tool_call_id(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("id") or "blocked")
    return "blocked"


def _append_text(result: Any, warning: str) -> Any:
    if isinstance(result, ToolMessage):
        return ToolMessage(content=str(result.content) + warning, tool_call_id=result.tool_call_id)
    content = getattr(result, "content", result)
    if hasattr(result, "content"):
        try:
            result.content = str(content) + warning
            return result
        except Exception:
            pass
    return result


class ToolBudgetMiddleware(AgentMiddleware):
    """Enforce per-tool call budgets for the active run segment."""

    def __init__(
        self,
        tool_budgets: dict[str, int] | None = None,
        budget_registry: BudgetRegistry | None = None,
        synthesis_guidance_map: dict[str, str] | None = None,
    ) -> None:
        if budget_registry is not None:
            self.budget_registry = budget_registry
        else:
            self.budget_registry = BudgetRegistry(skill_budgets=tool_budgets or {})
        self.tool_budgets = self.budget_registry.all_budgets()
        self.synthesis_guidance_map = dict(synthesis_guidance_map or {})

    def budget_for(self, tool_name: str) -> int | None:
        return self.budget_registry.get_budget(tool_name)

    def used(self, thread_id: str, run_segment: int, tool_name: str) -> int:
        state = get_segment_state(thread_id, run_segment)
        return state.tool_call_counts.get(tool_name, 0)

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        name = _tool_name(request)
        limit = self.budget_for(name)
        thread_id, run_segment = get_thread_segment()
        state = get_segment_state(thread_id, run_segment)

        if limit is not None:
            used = state.tool_call_counts.get(name, 0)
            if used >= limit:
                inc("harness_budget_block_total", tool_name=name, reason="budget_exhausted")
                inc(
                    "harness_forward_instruction_total",
                    reason="budget_exhausted",
                    expected_action="synthesize",
                )
                instruction = ForwardInstruction(
                    reason=BlockReason.BUDGET_EXHAUSTED,
                    tool_name=name,
                    used=used,
                    limit=limit,
                    expected_action=ExpectedAction.SYNTHESIZE,
                    evidence_summary=state.evidence_summary(),
                    custom_guidance=self.synthesis_guidance_map.get(name, ""),
                )
                return ToolMessage(
                    content=instruction.to_tool_message_content(),
                    tool_call_id=_tool_call_id(request),
                )

        result = await handler(request)
        state.tool_call_counts[name] = state.tool_call_counts.get(name, 0) + 1
        inc("harness_tool_call_total", tool_name=name, outcome="ok")

        if limit is not None:
            cfg = load_harness_config()
            used = state.tool_call_counts[name]
            if limit > 0 and used / limit >= cfg.budget_warn_threshold and not state.budget_warned.get(name):
                state.budget_warned[name] = True
                inc("harness_budget_warn_total", tool_name=name)
                warning = (
                    f"\n\n[Budget Warning] '{name}': {used}/{limit} calls used "
                    f"({int(used / limit * 100)}%). Consider synthesizing soon."
                )
                result = _append_text(result, warning)
        return result


__all__ = ["ToolBudgetMiddleware"]
