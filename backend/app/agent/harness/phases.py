"""Run phase state machine: research -> execute -> synthesize.

This is the "single-loop" governance piece from the ClaudeCode comparison:
once a run's tool-budgeted tools (e.g. SQL/WKB calls declared by a skill's
`harness.tool_budgets`) are exhausted, or the step budget is nearly spent,
the run is forced into `synthesize` and further calls to those gated tools
are rejected so the model must produce a final answer instead of looping.

Tools with no declared budget (read_file, write_file, task, MCP tools not
covered by a skill's budgets, etc.) are left untouched — this keeps HITL
interrupts and general-purpose tool use unaffected outside the org-pack
"evidence gathering" tools that opted into governance.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, Literal

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import SystemMessage, ToolMessage

from app.agent.harness.config import HarnessConfig, step_warn_threshold
from app.agent.harness.context import get_harness_context, get_thread_segment
from app.agent.harness.evidence import record_evidence
from app.agent.harness.middleware import get_segment_state
from app.agent.harness.hooks import harness_hooks

Phase = Literal["research", "execute", "synthesize"]

_SYNTHESIZE_SUFFIX = (
    "\n\n[Harness: entering synthesize phase. Gated evidence-gathering tools are now "
    "blocked for this run segment — write the final user-facing answer from the "
    "evidence already collected.]"
)


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


class RunPhaseMiddleware(AgentMiddleware):
    """Track and enforce the research -> execute -> synthesize phase machine."""

    def __init__(
        self,
        cfg: HarnessConfig | None = None,
        *,
        tool_budgets: dict[str, int] | None = None,
    ) -> None:
        self.cfg = cfg or HarnessConfig()
        self.tool_budgets: dict[str, int] = dict(tool_budgets or {})

    def _extended(self) -> bool:
        return bool(get_harness_context().get("extended_run"))

    def _check_synthesize(self, thread_id: str, run_segment: int) -> bool:
        """Evaluate budget/step thresholds and force `synthesize` if exceeded."""
        state = get_segment_state(thread_id, run_segment)
        if state.phase == "synthesize":
            return True

        budget_exhausted = any(
            state.tool_call_counts.get(name, 0) >= limit
            for name, limit in self.tool_budgets.items()
        )
        warn_at = step_warn_threshold(extended_run=self._extended())
        step_near_limit = state.tool_step_count >= warn_at

        if budget_exhausted or step_near_limit:
            state.phase = "synthesize"
            harness_hooks.emit(
                "on_synthesis_required",
                thread_id=thread_id,
                run_segment=run_segment,
                reason="tool_budget" if budget_exhausted else "step_budget",
            )
            harness_hooks.emit(
                "on_phase_enter", thread_id=thread_id, run_segment=run_segment, phase="synthesize"
            )
            return True
        return False

    def _maybe_advance_phase(self, thread_id: str, run_segment: int, *, from_tool_call: bool) -> Phase:
        state = get_segment_state(thread_id, run_segment)
        if self._check_synthesize(thread_id, run_segment):
            return "synthesize"

        if from_tool_call and state.phase == "research":
            # A tool call in flight means research has produced its first action.
            state.phase = "execute"
            harness_hooks.emit(
                "on_phase_enter", thread_id=thread_id, run_segment=run_segment, phase="execute"
            )
        return state.phase  # type: ignore[return-value]

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        thread_id, run_segment = get_thread_segment()
        name = _tool_name(request)
        phase = self._maybe_advance_phase(thread_id, run_segment, from_tool_call=True)

        if phase == "synthesize" and name in self.tool_budgets:
            return ToolMessage(
                content=(
                    f"Blocked: run is in the synthesize phase; `{name}` calls are "
                    "no longer permitted for this run segment. Produce the final answer now."
                ),
                tool_call_id=_tool_call_id(request),
            )

        harness_hooks.emit(
            "before_tool", thread_id=thread_id, run_segment=run_segment, tool=name, phase=phase
        )
        result = await handler(request)
        harness_hooks.emit(
            "after_tool", thread_id=thread_id, run_segment=run_segment, tool=name, phase=phase
        )
        if name in self.tool_budgets:
            args = getattr(request, "tool_call", {}) or {}
            input_preview = str(args.get("args") if isinstance(args, dict) else "")
            output_preview = str(getattr(result, "content", result))
            record_evidence(thread_id, run_segment, name, input_preview, output_preview)
        return result

    async def awrap_model_call(self, request: Any, handler: Any) -> Any:
        thread_id, run_segment = get_thread_segment()
        phase = self._maybe_advance_phase(thread_id, run_segment, from_tool_call=False)
        if phase == "synthesize":
            system_message = getattr(request, "system_message", None)
            base = ""
            if system_message is not None:
                content = getattr(system_message, "content", "")
                base = content if isinstance(content, str) else str(content)
            if _SYNTHESIZE_SUFFIX.strip() not in base:
                request = request.override(
                    system_message=SystemMessage(content=base + _SYNTHESIZE_SUFFIX)
                )
        return await handler(request)


def get_run_phase(thread_id: str, run_segment: int) -> Phase:
    return get_segment_state(thread_id, run_segment).phase  # type: ignore[return-value]


__all__ = ["RunPhaseMiddleware", "get_run_phase"]
