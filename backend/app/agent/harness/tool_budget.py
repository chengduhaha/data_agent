"""Per-tool call budgets declared by skill manifests (`harness.tool_budgets`).

Generic replacement for ad-hoc "≤12 SQL/run" enforcement: any tool name can
carry a budget (e.g. `run_query_safely: 12`, `wkb_query: 8`). When a tool
exceeds its budget for the current run segment, the call is blocked with a
structured message telling the model to move to synthesis instead of quietly
truncating results.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import ToolMessage

from app.agent.harness.context import get_thread_segment
from app.agent.harness.middleware import get_segment_state


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


class ToolBudgetMiddleware(AgentMiddleware):
    """Enforce per-tool call budgets for the active run segment."""

    def __init__(self, tool_budgets: dict[str, int] | None = None) -> None:
        self.tool_budgets: dict[str, int] = dict(tool_budgets or {})

    def budget_for(self, tool_name: str) -> int | None:
        return self.tool_budgets.get(tool_name)

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
                return ToolMessage(
                    content=(
                        f"Blocked: tool budget exceeded for `{name}` "
                        f"({used}/{limit} calls used this run). "
                        "Stop calling this tool and synthesize a final answer from the "
                        "evidence already gathered."
                    ),
                    tool_call_id=_tool_call_id(request),
                )

        result = await handler(request)
        state.tool_call_counts[name] = state.tool_call_counts.get(name, 0) + 1
        return result


__all__ = ["ToolBudgetMiddleware"]
