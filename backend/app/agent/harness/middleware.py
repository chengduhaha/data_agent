"""Tool governance middleware — blocks runaway reads and duplicate tool patterns."""

from __future__ import annotations

import json
from collections import OrderedDict
from typing import Any, Awaitable, Callable

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import ToolMessage

from app.agent.harness.config import HarnessConfig
from app.agent.harness.context import get_thread_segment

_BLOCKED_PATH_MARKERS = (
    "conversation_history/",
    "/conversation_history/",
    "large_tool_results/",
    "/large_tool_results/",
)

_L1_CATALOG_MARKER = "l1_catalog/"


class _SegmentState:
    __slots__ = ("read_cache", "l1_offset_counts", "task_count", "tool_step_count")

    def __init__(self) -> None:
        self.read_cache: OrderedDict[str, str] = OrderedDict()
        self.l1_offset_counts: dict[str, int] = {}
        self.task_count = 0
        self.tool_step_count = 0


# Key: (thread_id, run_segment)
_segment_states: dict[tuple[str, int], _SegmentState] = {}


def reset_segment_state(thread_id: str, run_segment: int) -> None:
    _segment_states[(thread_id, run_segment)] = _SegmentState()


def get_segment_state(thread_id: str, run_segment: int) -> _SegmentState:
    key = (thread_id, run_segment)
    if key not in _segment_states:
        _segment_states[key] = _SegmentState()
    return _segment_states[key]


def _thread_segment_from_request(request: Any) -> tuple[str, int]:
    return get_thread_segment()


def _tool_name(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("name") or "")
    return ""


def _tool_args(request: Any) -> dict[str, Any]:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        args = tool_call.get("args")
        return args if isinstance(args, dict) else {}
    return {}


def _tool_call_id(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("id") or "blocked")
    return "blocked"


def _path_from_args(args: dict[str, Any]) -> str:
    for key in ("file_path", "path", "target_file"):
        val = args.get(key)
        if isinstance(val, str):
            return val
    return ""


def _is_blocked_path(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(m in norm for m in _BLOCKED_PATH_MARKERS)


def _is_l1_catalog_json(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return _L1_CATALOG_MARKER in norm and norm.endswith(".json")


def _block_message(reason: str, tool_call_id: str = "blocked") -> ToolMessage:
    return ToolMessage(content=reason, tool_call_id=tool_call_id)


class ToolGovernanceMiddleware(AgentMiddleware):
    """Intercept filesystem tool calls to prevent runaway research loops."""

    def __init__(self, cfg: HarnessConfig | None = None) -> None:
        self.cfg = cfg or HarnessConfig()

    def _check(
        self, request: Any
    ) -> ToolMessage | None:
        name = _tool_name(request)
        args = _tool_args(request)
        path = _path_from_args(args)

        if name in ("read_file", "grep", "glob", "ls") and path and _is_blocked_path(path):
            return ToolMessage(
                content=(
                    "Blocked: compressed artifact path. Use the conversation summary and "
                    "prior tool outputs instead of re-reading conversation_history or large_tool_results."
                ),
                tool_call_id=_tool_call_id(request),
            )

        thread_id, run_segment = _thread_segment_from_request(request)
        state = get_segment_state(thread_id, run_segment)

        if name == "task":
            state.task_count += 1
            if state.task_count > self.cfg.max_task_per_segment:
                return ToolMessage(
                    content=(
                        f"Blocked: task subagent limit ({self.cfg.max_task_per_segment}) "
                        "reached for this run segment. Continue in the main agent."
                    ),
                    tool_call_id=_tool_call_id(request),
                )

        if name == "read_file" and path:
            offset = int(args.get("offset") or 0)
            limit = args.get("limit")

            if _is_l1_catalog_json(path):
                if offset > 0 and self.cfg.strict:
                    count = state.l1_offset_counts.get(path, 0) + 1
                    state.l1_offset_counts[path] = count
                    if count > self.cfg.max_l1_catalog_offset_reads:
                        return ToolMessage(
                            content=(
                                "Blocked: l1_catalog JSON pagination. Use wkb_query or "
                                "search_knowledge, then open ≤3 knowledgebase md files."
                            ),
                            tool_call_id=_tool_call_id(request),
                        )
                if offset > 0 and not self.cfg.strict:
                    pass
                elif offset == 0 and limit is not None and int(limit) > 200:
                    args["limit"] = 200

            cache_key = json.dumps(
                {"tool": name, "path": path, "offset": offset, "limit": limit},
                sort_keys=True,
            )
            if cache_key in state.read_cache:
                cached = state.read_cache[cache_key]
                return ToolMessage(
                    content=(
                        "[duplicate read suppressed]\n"
                        f"{cached[:500]}{'…' if len(cached) > 500 else ''}"
                    ),
                    tool_call_id=_tool_call_id(request),
                )

        return None

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        blocked = self._check(request)
        if blocked is not None:
            return blocked

        result = await handler(request)

        name = _tool_name(request)
        if name == "read_file":
            args = _tool_args(request)
            path = _path_from_args(args)
            if path:
                thread_id, run_segment = _thread_segment_from_request(request)
                state = get_segment_state(thread_id, run_segment)
                offset = int(args.get("offset") or 0)
                limit = args.get("limit")
                cache_key = json.dumps(
                    {"tool": name, "path": path, "offset": offset, "limit": limit},
                    sort_keys=True,
                )
                content = result.content if isinstance(result, ToolMessage) else str(result)
                if isinstance(content, list):
                    content = json.dumps(content, default=str)
                text = str(content)
                state.read_cache[cache_key] = text
                while len(state.read_cache) > self.cfg.max_read_dup_cache:
                    state.read_cache.popitem(last=False)

        return result
