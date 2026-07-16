"""Tool-step budget tracking and soft warnings before hard recursion limit."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import SystemMessage, ToolMessage

from app.agent.harness.config import HarnessConfig, step_limit, step_warn_threshold
from app.agent.harness.context import get_harness_context
from app.agent.harness.middleware import get_segment_state, reset_segment_state

_STEP_BUDGET_SUFFIX = (
    "\n\n[Harness: tool-step budget is nearly exhausted. "
    "Prioritize a complete final answer for the user. "
    "Avoid new exploratory tool calls unless essential.]"
)


class StepBudgetMiddleware(AgentMiddleware):
    """Track tool steps per run segment and warn the model as the budget fills."""

    def __init__(self, cfg: HarnessConfig | None = None) -> None:
        self.cfg = cfg or HarnessConfig()

    def _segment_key(self) -> tuple[str, int]:
        ctx = get_harness_context()
        return str(ctx.get("thread_id") or "default"), int(ctx.get("run_segment") or 1)

    def _extended(self) -> bool:
        return bool(get_harness_context().get("extended_run"))

    def _record_tool_step(self) -> int:
        thread_id, run_segment = self._segment_key()
        state = get_segment_state(thread_id, run_segment)
        state.tool_step_count += 1
        return state.tool_step_count

    def _budget_payload(self) -> dict[str, Any]:
        thread_id, run_segment = self._segment_key()
        state = get_segment_state(thread_id, run_segment)
        extended = self._extended()
        limit = step_limit(extended_run=extended)
        used = state.tool_step_count
        warn_at = step_warn_threshold(extended_run=extended)
        phase = "ok"
        if used >= limit:
            phase = "exhausted"
        elif used >= warn_at:
            phase = "warn"
        return {
            "steps_used": used,
            "steps_limit": limit,
            "steps_warn_at": warn_at,
            "phase": phase,
            "run_segment": run_segment,
            "thread_id": thread_id,
        }

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        self._record_tool_step()
        return await handler(request)

    async def awrap_model_call(self, request: Any, handler: Any) -> Any:
        budget = self._budget_payload()
        extended = self._extended()
        warn_at = step_warn_threshold(extended_run=extended)
        if budget["steps_used"] >= warn_at:
            system_message = getattr(request, "system_message", None)
            base = ""
            if system_message is not None:
                content = getattr(system_message, "content", "")
                base = content if isinstance(content, str) else str(content)
            if _STEP_BUDGET_SUFFIX.strip() not in base:
                request = request.override(
                    system_message=SystemMessage(content=base + _STEP_BUDGET_SUFFIX)
                )
        response = await handler(request)
        setattr(response, "_harness_budget", budget)
        return response


def get_segment_budget() -> dict[str, Any]:
    """Return current segment step budget for SSE / wrap-up."""
    ctx = get_harness_context()
    thread_id = str(ctx.get("thread_id") or "default")
    run_segment = int(ctx.get("run_segment") or 1)
    extended = bool(ctx.get("extended_run"))
    state = get_segment_state(thread_id, run_segment)
    limit = step_limit(extended_run=extended)
    used = state.tool_step_count
    warn_at = step_warn_threshold(extended_run=extended)
    phase = "ok"
    if used >= limit:
        phase = "exhausted"
    elif used >= warn_at:
        phase = "warn"
    return {
        "steps_used": used,
        "steps_limit": limit,
        "steps_warn_at": warn_at,
        "phase": phase,
        "run_segment": run_segment,
        "thread_id": thread_id,
    }


__all__ = ["StepBudgetMiddleware", "get_segment_budget", "reset_segment_state"]
