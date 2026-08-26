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

from app.agent.harness.budget_registry import BudgetRegistry
from app.agent.harness.config import HarnessConfig, step_warn_threshold
from app.agent.harness.context import get_harness_context, get_thread_segment
from app.agent.harness.evidence import record_evidence
from app.agent.harness.forward_instruction import (
    BlockReason,
    ExpectedAction,
    ForwardInstruction,
)
from app.agent.harness.hooks import harness_hooks
from app.agent.harness.metrics import inc
from app.agent.harness.segment_manager import get_segment_state

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
        budget_registry: BudgetRegistry | None = None,
        evidence_tools: set[str] | None = None,
        synthesis_guidance: str = "",
    ) -> None:
        self.cfg = cfg or HarnessConfig()
        if budget_registry is not None:
            self.budget_registry = budget_registry
        else:
            self.budget_registry = BudgetRegistry(skill_budgets=tool_budgets or {})
        self.tool_budgets: dict[str, int] = self.budget_registry.all_budgets()
        self.evidence_tools = evidence_tools
        self.synthesis_guidance = synthesis_guidance

    def _is_governed(self, name: str) -> bool:
        return self.budget_registry.is_governed(name)

    def _should_record_evidence(self, name: str) -> bool:
        if self.cfg.evidence_track_all_tools or self.evidence_tools == {"*"}:
            return True
        if self.evidence_tools is None:
            return self._is_governed(name)
        return name in self.evidence_tools

    def _extended(self) -> bool:
        return bool(get_harness_context().get("extended_run"))

    def _check_synthesize(self, thread_id: str, run_segment: int) -> bool:
        """Evaluate budget/step thresholds and force `synthesize` if exceeded."""
        state = get_segment_state(thread_id, run_segment)
        if state.phase == "synthesize":
            return True

        budget_exhausted = any(
            state.tool_call_counts.get(name, 0) >= limit
            for name, limit in self.budget_registry.all_budgets().items()
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
            inc("harness_phase_transition_total", from_phase=state.phase, to_phase="synthesize")
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

        if phase == "synthesize" and self._is_governed(name):
            inc("harness_budget_block_total", tool_name=name, reason="phase_blocked")
            inc(
                "harness_forward_instruction_total",
                reason="phase_blocked",
                expected_action="synthesize",
            )
            state = get_segment_state(thread_id, run_segment)
            instruction = ForwardInstruction(
                reason=BlockReason.PHASE_BLOCKED,
                tool_name=name,
                used=state.tool_call_counts.get(name, 0),
                limit=self.budget_registry.get_budget(name),
                expected_action=ExpectedAction.SYNTHESIZE,
                evidence_summary=state.evidence_summary(),
                custom_guidance=self.synthesis_guidance,
            )
            return ToolMessage(
                content=instruction.to_tool_message_content(),
                tool_call_id=_tool_call_id(request),
            )

        harness_hooks.emit(
            "before_tool", thread_id=thread_id, run_segment=run_segment, tool=name, phase=phase
        )
        result = await handler(request)
        harness_hooks.emit(
            "after_tool", thread_id=thread_id, run_segment=run_segment, tool=name, phase=phase
        )
        if self._should_record_evidence(name):
            args = getattr(request, "tool_call", {}) or {}
            input_preview = str(args.get("args") if isinstance(args, dict) else "")
            output_preview = str(getattr(result, "content", result))
            record_evidence(thread_id, run_segment, name, input_preview, output_preview)
            harness_hooks.emit(
                "on_evidence_added", thread_id=thread_id, run_segment=run_segment, tool=name
            )
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
