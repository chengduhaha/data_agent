"""Harness middleware, continue SSE, and org fragment policy tests."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from langgraph.errors import GraphRecursionError

from app.agent.harness.config import recursion_limit
from app.agent.harness.context import reset_harness_context, set_harness_context
from app.agent.harness.middleware import ToolGovernanceMiddleware, reset_segment_state
from app.agent.streaming import sse, stream_agent_events
from app.store import paths


def _mock_request(tool: str, args: dict, call_id: str = "tc1") -> SimpleNamespace:
    return SimpleNamespace(tool_call={"name": tool, "args": args, "id": call_id})


@pytest.fixture(autouse=True)
def _harness_ctx() -> None:
    token = set_harness_context(thread_id="t-harness", run_segment=1)
    yield
    reset_harness_context(token)


def test_recursion_limit_defaults() -> None:
    assert recursion_limit(extended_run=False) == 155
    assert recursion_limit(extended_run=True) == 405


def test_org_fragments_exclude_contract_only() -> None:
    names = {p.name for p in paths.org_rule_fragment_paths()}
    assert "harness.defaults.md" in names
    assert "AGENTS.contract-skill.md" not in names
    assert "contract-data-analysis-vertica.md" not in names


def test_blocks_conversation_history_read() -> None:
    mw = ToolGovernanceMiddleware()
    blocked = mw._check(
        _mock_request(
            "read_file",
            {"file_path": "/workspace/files/conversation_history/thread.md"},
        )
    )
    assert blocked is not None
    assert "Blocked" in str(blocked.content)


def test_blocks_l1_catalog_offset_pagination() -> None:
    mw = ToolGovernanceMiddleware()
    path = "/knowledge/org/target/storage/wkb/snapshots/x/l1_catalog/foo.json"
    reset_segment_state("t-harness", 1)
    blocked_at = None
    for offset in (100, 200, 300, 400):
        result = mw._check(
            _mock_request("read_file", {"file_path": path, "offset": offset})
        )
        if result is not None:
            blocked_at = offset
            break
    assert blocked_at is not None
    assert blocked_at <= 400


def test_duplicate_read_suppressed() -> None:
    mw = ToolGovernanceMiddleware()
    path = "/knowledge/org/source/contracts/b-report-us/metric-index.md"
    req = _mock_request("read_file", {"file_path": path, "offset": 0, "limit": 200})

    async def _handler(request: SimpleNamespace) -> SimpleNamespace:
        return SimpleNamespace(content="full file contents " * 20)

    first = asyncio.run(mw.awrap_tool_call(req, _handler))
    second = asyncio.run(mw.awrap_tool_call(req, _handler))
    assert "full file contents" in str(first.content)
    assert "duplicate read suppressed" in str(second.content).lower()


def test_task_limit_per_segment() -> None:
    mw = ToolGovernanceMiddleware()
    first = mw._check(_mock_request("task", {"description": "sub"}))
    assert first is None
    second = mw._check(_mock_request("task", {"description": "sub again"}))
    assert second is not None
    assert "task subagent limit" in str(second.content).lower()


def test_stream_emits_continue_prompt_on_recursion_error() -> None:
    agent = MagicMock()

    async def _raise(*_args, **_kwargs):
        raise GraphRecursionError("limit")
        yield  # pragma: no cover

    agent.astream_events = _raise

    config = {
        "configurable": {
            "thread_id": "thread-1",
            "run_segment": 2,
            "extended_run": False,
        }
    }

    async def _collect() -> list[str]:
        events: list[str] = []
        async for chunk in stream_agent_events(agent, None, config):
            events.append(chunk)
        return events

    events = asyncio.run(_collect())

    assert any("event: continue_prompt" in e for e in events)
    continue_event = next(e for e in events if "event: continue_prompt" in e)
    payload_line = next(l for l in continue_event.split("\n") if l.startswith("data:"))
    data = json.loads(payload_line.removeprefix("data:").strip())
    assert data["thread_id"] == "thread-1"
    assert data["run_segment"] == 2
    assert data["steps_limit"] == 150


def test_sse_format() -> None:
    out = sse("continue_prompt", {"thread_id": "x"})
    assert out.startswith("event: continue_prompt\n")
    assert "data:" in out
