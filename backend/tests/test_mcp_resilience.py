"""Tests for MCP tool resilience middleware."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
from langchain_core.messages import ToolMessage

from app.agent.harness.mcp_resilience import (
    McpToolResilienceMiddleware,
    format_mcp_tool_error,
    format_stream_error,
    is_mcp_query_tool,
    is_transient_mcp_error,
)


def test_is_mcp_query_tool_detects_vertica_tools() -> None:
    assert is_mcp_query_tool("run_query_safely")
    assert is_mcp_query_tool("gateway-vertica-prod__run_query_safely")
    assert not is_mcp_query_tool("grep")


def test_is_transient_mcp_error_502() -> None:
    exc = httpx.HTTPStatusError(
        "502",
        request=httpx.Request("POST", "https://example/mcp"),
        response=httpx.Response(502),
    )
    assert is_transient_mcp_error(exc)


def test_format_stream_error_unwraps_taskgroup() -> None:
    inner = httpx.HTTPStatusError(
        "502",
        request=httpx.Request("POST", "https://example/mcp"),
        response=httpx.Response(502),
    )
    group = ExceptionGroup("unhandled errors in a TaskGroup", [inner])
    msg = format_stream_error(group)
    assert "502" in msg
    assert "gateway" in msg.lower()


def test_format_mcp_tool_error_json() -> None:
    exc = httpx.HTTPStatusError(
        "502",
        request=httpx.Request("POST", "https://example/mcp"),
        response=httpx.Response(502),
    )
    payload = json.loads(format_mcp_tool_error("run_query_safely", exc))
    assert payload["ok"] is False
    assert payload["status_code"] == 502


def test_middleware_retries_then_returns_tool_message() -> None:
    mw = McpToolResilienceMiddleware(
        SimpleNamespace(mcp_tool_max_retries=1, mcp_retry_backoff=0.01)
    )
    calls = {"n": 0}

    async def _handler(_request):
        calls["n"] += 1
        raise httpx.HTTPStatusError(
            "502",
            request=httpx.Request("POST", "https://example/mcp"),
            response=httpx.Response(502),
        )

    request = SimpleNamespace(tool_call={"name": "run_query_safely", "id": "tc1"})

    async def _run():
        return await mw.awrap_tool_call(request, _handler)

    result = asyncio.run(_run())
    assert isinstance(result, ToolMessage)
    assert calls["n"] == 2
    payload = json.loads(str(result.content))
    assert payload["ok"] is False


def test_middleware_passes_through_non_mcp_tools() -> None:
    mw = McpToolResilienceMiddleware(
        SimpleNamespace(mcp_tool_max_retries=0, mcp_retry_backoff=0.01)
    )
    handler = AsyncMock(return_value=ToolMessage(content="ok", tool_call_id="tc2"))
    request = SimpleNamespace(tool_call={"name": "grep", "id": "tc2"})

    async def _run():
        return await mw.awrap_tool_call(request, handler)

    result = asyncio.run(_run())
    assert result.content == "ok"
    handler.assert_awaited_once()
