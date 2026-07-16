"""Tests for large tool result spill middleware."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from langchain_core.messages import ToolMessage

from app.agent.harness.context import reset_harness_context, set_harness_context
from app.agent.harness.spill import LargeResultSpillMiddleware
from app.store.paths import ensure_user_layout, files_dir


@pytest.fixture(autouse=True)
def _ctx() -> None:
    ensure_user_layout("spill-test")
    token = set_harness_context(
        thread_id="t-spill",
        run_segment=1,
        user_id="spill-test",
    )
    yield
    reset_harness_context(token)


def test_spills_large_tool_output_to_workspace() -> None:
    mw = LargeResultSpillMiddleware()
    big = "x" * 12_000
    req = SimpleNamespace(
        tool_call={"name": "run_query_safely", "args": {}, "id": "call99"}
    )

    async def _handler(_request: SimpleNamespace) -> ToolMessage:
        return ToolMessage(content=big, tool_call_id="call99")

    result = asyncio.run(mw.awrap_tool_call(req, _handler))
    assert isinstance(result, ToolMessage)
    assert "large_tool_results" in str(result.content)
    assert len(str(result.content)) < len(big)
    spill_files = list((files_dir("spill-test") / "large_tool_results").glob("*.txt"))
    assert spill_files
