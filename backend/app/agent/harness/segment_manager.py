"""SegmentManager: create / reset / close / evict RunSegment instances."""

from __future__ import annotations

from enum import Enum
from typing import Callable

from app.agent.harness.hooks import harness_hooks
from app.agent.harness.segment import RunSegment


class SegmentEvent(str, Enum):
    ON_START = "on_segment_start"
    ON_END = "on_segment_end"
    ON_PHASE_ENTER = "on_phase_enter"
    ON_EVIDENCE_ADDED = "on_evidence_added"


HookFn = Callable[..., None]


class SegmentManager:
    def __init__(self, max_per_thread: int = 10) -> None:
        self.max_per_thread = max_per_thread
        self._segments: dict[tuple[str, int], RunSegment] = {}

    def get(self, thread_id: str, segment_id: int) -> RunSegment:
        key = (thread_id, segment_id)
        segment = self._segments.get(key)
        if segment is None:
            segment = RunSegment(thread_id=thread_id, segment_id=segment_id)
            self._segments[key] = segment
        segment.touch()
        return segment

    def reset(self, thread_id: str, segment_id: int) -> RunSegment:
        segment = RunSegment(thread_id=thread_id, segment_id=segment_id)
        self._segments[(thread_id, segment_id)] = segment
        harness_hooks.emit(SegmentEvent.ON_START.value, thread_id=thread_id, run_segment=segment_id)
        self.evict_old_segments(self.max_per_thread)
        return segment

    def close(self, thread_id: str, segment_id: int) -> None:
        segment = self.get(thread_id, segment_id)
        segment.is_closed = True
        harness_hooks.emit(SegmentEvent.ON_END.value, thread_id=thread_id, run_segment=segment_id)

    def evict_old_segments(self, max_per_thread: int = 10) -> int:
        by_thread: dict[str, list[RunSegment]] = {}
        for (thread_id, _sid), segment in self._segments.items():
            by_thread.setdefault(thread_id, []).append(segment)
        removed = 0
        for thread_id, items in by_thread.items():
            if len(items) <= max_per_thread:
                continue
            items.sort(key=lambda s: (not s.is_closed, s.segment_id))
            overflow = items[: len(items) - max_per_thread]
            for segment in overflow:
                self._segments.pop((thread_id, segment.segment_id), None)
                removed += 1
        return removed

    def register_hook(self, event: SegmentEvent, fn: HookFn) -> None:
        harness_hooks.on(event.value, fn)


_manager = SegmentManager()


def get_segment_manager() -> SegmentManager:
    return _manager


def reset_segment_state(thread_id: str, run_segment: int) -> None:
    get_segment_manager().reset(thread_id, run_segment)


def get_segment_state(thread_id: str, run_segment: int) -> RunSegment:
    return get_segment_manager().get(thread_id, run_segment)
