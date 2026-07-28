"""Retry and graceful degradation for MCP / Vertica tool calls."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import ToolMessage

from app.agent.harness.config import HarnessConfig, load_harness_config

logger = logging.getLogger(__name__)

_VERTICA_QUERY_TOOLS = frozenset({
    "run_query_safely",
    "execute_query_paginated",
    "execute_query_stream",
    "profile_query",
})


def _tool_name(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("name") or "")
    return ""


def _tool_call_id(request: Any) -> str:
    tool_call = getattr(request, "tool_call", None) or {}
    if isinstance(tool_call, dict):
        return str(tool_call.get("id") or "mcp-error")
    return "mcp-error"


def _base_tool_name(name: str) -> str:
    if "__" in name:
        return name.rsplit("__", 1)[-1]
    return name


def is_mcp_query_tool(name: str) -> bool:
    base = _base_tool_name(name).lower()
    return (
        base in _VERTICA_QUERY_TOOLS
        or "run_query" in base
        or base.startswith("execute_query")
        or "vertica" in name.lower()
        or "mcp" in name.lower()
    )


def _unwrap_exception(exc: BaseException) -> BaseException:
    current: BaseException = exc
    while isinstance(current, BaseExceptionGroup) and current.exceptions:
        current = current.exceptions[0]
    return current


def is_transient_mcp_error(exc: BaseException) -> bool:
    root = _unwrap_exception(exc)
    name = type(root).__name__
    if name in ("TimeoutError", "ReadTimeout", "ConnectTimeout", "PoolTimeout"):
        return True
    if name in ("ConnectionError", "ConnectError", "RemoteProtocolError"):
        return True
    status = getattr(getattr(root, "response", None), "status_code", None)
    if status in (408, 429, 500, 502, 503, 504):
        return True
    text = str(root).lower()
    return any(
        token in text
        for token in (
            "bad gateway",
            "gateway timeout",
            "service unavailable",
            "temporarily unavailable",
            "connection reset",
            "connection refused",
            "timed out",
            "taskgroup",
        )
    )


def format_mcp_tool_error(tool: str, exc: BaseException) -> str:
    root = _unwrap_exception(exc)
    status = getattr(getattr(root, "response", None), "status_code", None)
    detail = str(root).strip() or type(root).__name__
    if status:
        headline = f"Vertica MCP gateway error ({status})"
    elif "timeout" in detail.lower():
        headline = "Vertica MCP request timed out"
    else:
        headline = "Vertica MCP call failed"
    return json.dumps(
        {
            "ok": False,
            "error": headline,
            "tool": tool,
            "status_code": status,
            "detail": detail[:1200],
            "retryable": is_transient_mcp_error(exc),
            "hint": (
                "The data gateway was temporarily unavailable. "
                "Do not crash — explain the limitation to the user and, if evidence "
                "already exists, synthesize from prior tool outputs."
            ),
        },
        ensure_ascii=False,
    )


def format_stream_error(exc: BaseException) -> str:
    """User-facing message for fatal stream failures."""
    root = _unwrap_exception(exc)
    status = getattr(getattr(root, "response", None), "status_code", None)
    if status in (502, 503, 504):
        return (
            f"Vertica data gateway is temporarily unavailable (HTTP {status}). "
            "Please retry in a moment. Your agent steps are saved in this thread."
        )
    if is_transient_mcp_error(root) and is_mcp_query_tool(str(root)):
        return (
            "Vertica MCP connection failed after retries. "
            "Please retry shortly or narrow the question."
        )
    detail = str(root).strip() or type(root).__name__
    if "taskgroup" in detail.lower():
        inner = _unwrap_exception(exc)
        return format_stream_error(inner)
    return detail


class McpToolResilienceMiddleware(AgentMiddleware):
    """Retry transient MCP failures; return structured tool errors instead of crashing."""

    def __init__(self, cfg: HarnessConfig | None = None) -> None:
        loaded = cfg or load_harness_config()
        self.max_retries = loaded.mcp_tool_max_retries
        self.retry_backoff = loaded.mcp_retry_backoff

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Callable[[Any], Awaitable[ToolMessage | Any]],
    ) -> ToolMessage | Any:
        name = _tool_name(request)
        if not is_mcp_query_tool(name):
            return await handler(request)

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await handler(request)
            except Exception as exc:
                last_exc = exc
                transient = is_transient_mcp_error(exc)
                if transient and attempt < self.max_retries:
                    wait = self.retry_backoff * (attempt + 1)
                    logger.warning(
                        "MCP tool %s failed (attempt %d/%d): %s — retrying in %.1fs",
                        name,
                        attempt + 1,
                        self.max_retries + 1,
                        _unwrap_exception(exc),
                        wait,
                    )
                    await asyncio.sleep(wait)
                    continue
                logger.error(
                    "MCP tool %s failed after %d attempt(s): %s",
                    name,
                    attempt + 1,
                    _unwrap_exception(exc),
                )
                return ToolMessage(
                    content=format_mcp_tool_error(name, exc),
                    tool_call_id=_tool_call_id(request),
                )
        if last_exc is not None:
            return ToolMessage(
                content=format_mcp_tool_error(name, last_exc),
                tool_call_id=_tool_call_id(request),
            )
        return await handler(request)


__all__ = [
    "McpToolResilienceMiddleware",
    "format_mcp_tool_error",
    "format_stream_error",
    "is_mcp_query_tool",
    "is_transient_mcp_error",
]
