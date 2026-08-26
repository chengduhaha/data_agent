"""Structured forward instruction emitted when a tool call is blocked (C3)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BlockReason(str, Enum):
    BUDGET_EXHAUSTED = "budget_exhausted"
    PHASE_BLOCKED = "phase_blocked"
    STEP_BUDGET = "step_budget"
    GOVERNANCE = "governance"


class ExpectedAction(str, Enum):
    SYNTHESIZE = "synthesize"
    CLARIFY = "clarify"
    STOP = "stop"


@dataclass
class ForwardInstruction:
    reason: BlockReason
    tool_name: str
    used: int
    limit: int | None
    expected_action: ExpectedAction
    evidence_summary: str
    custom_guidance: str = ""
    language: str = "en"

    def to_tool_message_content(self) -> str:
        action = self.expected_action.value.capitalize()
        if self.reason == BlockReason.BUDGET_EXHAUSTED:
            limit = self.limit if self.limit is not None else "?"
            headline = (
                f"Blocked: tool budget exceeded for `{self.tool_name}` "
                f"({self.used}/{limit} calls in this segment)."
            )
        elif self.reason == BlockReason.PHASE_BLOCKED:
            headline = (
                f"Blocked: run is in the synthesize phase; `{self.tool_name}` calls are "
                "no longer permitted for this run segment. Produce the final answer now."
            )
        else:
            headline = f"Blocked: `{self.tool_name}` is not permitted ({self.reason.value})."

        evidence = self.evidence_summary.strip() or (
            "No evidence collected yet. Please state that you were unable to retrieve the necessary data."
        )
        parts = [
            f"[Action Required: {action}]",
            headline,
            "",
            "Evidence collected so far:",
            evidence,
            "",
            "Required action: Write your final answer now using ONLY the evidence above.",
            "Do not call any more tools. If the evidence is insufficient, state this clearly.",
        ]
        if self.custom_guidance.strip():
            parts.extend(["", self.custom_guidance.strip()])
        return "\n".join(parts)
