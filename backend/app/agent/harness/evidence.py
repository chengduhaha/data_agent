"""EvidenceSnapshot: compact record of governed tool results kept across compaction.

Complements `SummarizationMiddleware` (token-threshold compaction): whenever a
budgeted tool (e.g. a SQL/WKB query declared in a skill's `harness.tool_budgets`)
completes, a short summary is appended to an in-memory snapshot for the run
segment. This snapshot survives message summarization/spill and is available
to wrap-up so a forced synthesis still cites concrete evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvidenceItem:
    tool: str
    input_preview: str
    output_preview: str


@dataclass
class EvidenceSnapshot:
    items: list[EvidenceItem] = field(default_factory=list)
    max_items: int = 20

    def add(self, tool: str, input_preview: str, output_preview: str) -> None:
        self.items.append(
            EvidenceItem(
                tool=tool,
                input_preview=input_preview[:500],
                output_preview=output_preview[:1500],
            )
        )
        if len(self.items) > self.max_items:
            self.items.pop(0)

    def as_text(self) -> str:
        if not self.items:
            return ""
        lines = ["### Evidence snapshot (governed tool results)"]
        for i, item in enumerate(self.items, start=1):
            lines.append(f"{i}. tool={item.tool}\n   input: {item.input_preview}\n   output: {item.output_preview}")
        return "\n".join(lines)


_snapshots: dict[tuple[str, int], EvidenceSnapshot] = {}


def get_evidence_snapshot(thread_id: str, run_segment: int) -> EvidenceSnapshot:
    key = (thread_id, run_segment)
    if key not in _snapshots:
        _snapshots[key] = EvidenceSnapshot()
    return _snapshots[key]


def reset_evidence_snapshot(thread_id: str, run_segment: int) -> None:
    _snapshots[(thread_id, run_segment)] = EvidenceSnapshot()


def record_evidence(thread_id: str, run_segment: int, tool: str, input_preview: str, output_preview: str) -> None:
    get_evidence_snapshot(thread_id, run_segment).add(tool, input_preview, output_preview)


__all__ = [
    "EvidenceItem",
    "EvidenceSnapshot",
    "get_evidence_snapshot",
    "record_evidence",
    "reset_evidence_snapshot",
]
