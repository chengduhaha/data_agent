"""EvidenceSnapshot: compact record of governed tool results kept across compaction.

Delegates storage to RunSegment.evidence_items while keeping the v1 public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.agent.harness.segment_manager import get_segment_state


@dataclass
class EvidenceItem:
    tool: str
    input_preview: str
    output_preview: str


class EvidenceSnapshot:
    def __init__(self, items: list[EvidenceItem] | None = None, max_items: int = 20) -> None:
        self._items: list[EvidenceItem] = items if items is not None else []
        self.max_items = max_items
        self._segment_bound = False

    @classmethod
    def from_segment(cls, thread_id: str, run_segment: int) -> "EvidenceSnapshot":
        segment = get_segment_state(thread_id, run_segment)
        snap = cls(items=segment.evidence_items, max_items=segment.evidence_max_items)
        snap._segment = segment
        snap._segment_bound = True
        return snap

    @property
    def items(self) -> list[EvidenceItem]:
        if self._segment_bound:
            return self._segment.evidence_items
        return self._items

    def add(self, tool: str, input_preview: str, output_preview: str) -> None:
        if self._segment_bound:
            self._segment.add_evidence(tool, input_preview, output_preview)
            return
        self._items.append(
            EvidenceItem(
                tool=tool,
                input_preview=input_preview[:500],
                output_preview=output_preview[:1500],
            )
        )
        if len(self._items) > self.max_items:
            self._items.pop(0)

    def as_text(self) -> str:
        if not self.items:
            return ""
        lines = ["### Evidence snapshot (governed tool results)"]
        for i, item in enumerate(self.items, start=1):
            lines.append(
                f"{i}. tool={item.tool}\n   input: {item.input_preview}\n   output: {item.output_preview}"
            )
        return "\n".join(lines)


def get_evidence_snapshot(thread_id: str, run_segment: int) -> EvidenceSnapshot:
    return EvidenceSnapshot.from_segment(thread_id, run_segment)


def reset_evidence_snapshot(thread_id: str, run_segment: int) -> None:
    segment = get_segment_state(thread_id, run_segment)
    segment.evidence_items.clear()


def record_evidence(
    thread_id: str, run_segment: int, tool: str, input_preview: str, output_preview: str
) -> None:
    get_segment_state(thread_id, run_segment).add_evidence(tool, input_preview, output_preview)


__all__ = [
    "EvidenceItem",
    "EvidenceSnapshot",
    "get_evidence_snapshot",
    "record_evidence",
    "reset_evidence_snapshot",
]
