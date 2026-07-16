"""Spill oversized tool results to workspace files; keep checkpoint messages small."""

from __future__ import annotations

import json
import uuid
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import ToolMessage

from app.agent.harness.config import HarnessConfig
from app.agent.harness.context import get_harness_context
from app.store.paths import files_dir


def _tool_name(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("name") or "")
    return ""


def _tool_call_id(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("id") or uuid.uuid4().hex[:12])
    return uuid.uuid4().hex[:12]


def _content_text(result: Any) -> str:
    if isinstance(result, ToolMessage):
        content = result.content
    else:
        content = getattr(result, "content", result)
    if isinstance(content, list):
        return json.dumps(content, ensure_ascii=False, default=str)
    return str(content)


class LargeResultSpillMiddleware(AgentMiddleware):
    """Write very large tool outputs to /workspace/large_tool_results/."""

    def __init__(self, cfg: HarnessConfig | None = None) -> None:
        self.cfg = cfg or HarnessConfig()

    def _spill_dir(self) -> Path | None:
        ctx = get_harness_context()
        user_id = str(ctx.get("user_id") or "")
        if not user_id:
            return None
        base = files_dir(user_id) / "large_tool_results"
        base.mkdir(parents=True, exist_ok=True)
        return base

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        result = await handler(request)
        text = _content_text(result)
        max_chars = self.cfg.tool_result_inline_max_chars
        if len(text) <= max_chars:
            return result

        spill_dir = self._spill_dir()
        if spill_dir is None:
            truncated = text[:max_chars] + f"\n…[truncated, {len(text)} chars total]"
            return ToolMessage(content=truncated, tool_call_id=_tool_call_id(request))

        tool = _tool_name(request) or "tool"
        call_id = _tool_call_id(request)
        rel = f"large_tool_results/{call_id}.txt"
        path = spill_dir / f"{call_id}.txt"
        path.write_text(text, encoding="utf-8")

        preview = text[: min(2000, max_chars)]
        notice = (
            f"Tool result too large ({len(text)} chars). "
            f"Full output saved at /workspace/{rel}.\n"
            f"Do not paginate-read this file; use the preview below and prior reasoning.\n\n"
            f"--- preview ({tool}) ---\n{preview}"
        )
        if len(text) > len(preview):
            notice += "\n…[preview truncated]"

        if isinstance(result, ToolMessage):
            return ToolMessage(content=notice, tool_call_id=result.tool_call_id)
        return ToolMessage(content=notice, tool_call_id=call_id)
