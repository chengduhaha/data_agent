"""RunSegment: public per-(thread, segment) harness state (C1)."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_completeness.models.evidence import EvidenceSet, RunContext
    from app.agent.harness.evidence import EvidenceItem
    from dw_agent_governance.context import DWGovernanceContext


@dataclass
class SpilledFile:
    tool_name: str
    call_index: int
    path: str
    token_estimate: int = 0
    tool_call_id: str = ""


@dataclass
class RunSegment:
    thread_id: str
    segment_id: int
    tool_call_counts: dict[str, int] = field(default_factory=dict)
    phase: str = "research"
    task_count: int = 0
    tool_step_count: int = 0
    evidence_items: list["EvidenceItem"] = field(default_factory=list)
    evidence_max_items: int = 20
    spilled_files: list[SpilledFile] = field(default_factory=list)
    read_cache: OrderedDict[str, str] = field(default_factory=OrderedDict)
    read_cache_max: int = 256
    l1_offset_counts: dict[str, int] = field(default_factory=dict)
    budget_warned: dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_active_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_closed: bool = False

    def touch(self) -> None:
        self.last_active_at = datetime.now(timezone.utc)

    def add_evidence(self, tool: str, input_preview: str, output_preview: str) -> None:
        from app.agent.harness.evidence import EvidenceItem

        self.evidence_items.append(
            EvidenceItem(
                tool=tool,
                input_preview=input_preview[:500],
                output_preview=output_preview[:1500],
            )
        )
        if len(self.evidence_items) > self.evidence_max_items:
            self.evidence_items.pop(0)
        self.touch()

    def evidence_summary(self) -> str:
        if not self.evidence_items:
            return "No evidence collected yet. Please state that you were unable to retrieve the necessary data."
        lines: list[str] = []
        for i, item in enumerate(self.evidence_items, start=1):
            lines.append(
                f"{i}. tool={item.tool}\n   input: {item.input_preview}\n   output: {item.output_preview}"
            )
        return "\n".join(lines)

    def to_evidence_set(self) -> "EvidenceSet":
        try:
            from agent_completeness.models.evidence import Evidence
        except ImportError:
            return []
        items = [
            Evidence(
                tool_name=item.tool,
                tool_call_id=f"{self.thread_id}:{self.segment_id}:{i}",
                result_summary=item.output_preview,
                result_token_count=max(1, len(item.output_preview) // 4),
                is_successful=True,
                run_segment=self.segment_id,
            )
            for i, item in enumerate(self.evidence_items)
        ]
        return items

    def to_run_context(self) -> "RunContext | None":
        try:
            from agent_completeness.models.evidence import RunContext
        except ImportError:
            return None
        phase = self.phase if self.phase in ("research", "execute", "synthesize") else "research"
        return RunContext(
            thread_id=self.thread_id,
            run_segment=self.segment_id,
            phase=phase,  # type: ignore[arg-type]
            tool_call_counts=dict(self.tool_call_counts),
        )

    def to_dw_context(self) -> "DWGovernanceContext | None":
        try:
            from dw_agent_governance.context import DWGovernanceContext
            from dw_agent_governance.models.result import SpilledFile as DwSpill
        except ImportError:
            return None
        spills = [
            DwSpill(
                tool_name=item.tool_name,
                call_index=item.call_index,
                path=item.path,  # type: ignore[arg-type]
                token_estimate=item.token_estimate,
            )
            for item in self.spilled_files
        ]
        return DWGovernanceContext(
            thread_id=self.thread_id,
            run_segment=self.segment_id,
            query_counts=dict(self.tool_call_counts),
            token_budget_used=0,
            spilled_files=spills,
        )


# Backward-compatible alias used by existing tests/imports.
_SegmentState = RunSegment
