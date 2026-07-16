"""Tests for wrap-up on step budget exhaustion."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from langgraph.errors import GraphRecursionError

from app.agent.harness.wrapup import _build_wrapup_context, needs_synthesis_wrapup
from app.agent.streaming import stream_agent_events


def test_build_wrapup_context_includes_tools() -> None:
    messages = [
        SimpleNamespace(type="human", content="What is revenue?", id="u1", tool_calls=[]),
        SimpleNamespace(
            type="ai",
            content="",
            id="a1",
            tool_calls=[{"id": "tc1", "name": "run_query_safely", "args": {"query": "SELECT 1"}}],
        ),
        SimpleNamespace(type="tool", content='[{"rev": 100}]', tool_call_id="tc1", id="t1"),
        SimpleNamespace(type="ai", content="Revenue is 100.", id="a2", tool_calls=[]),
    ]
    text = _build_wrapup_context(messages)
    assert "revenue" in text.lower() or "Revenue" in text
    assert "run_query_safely" in text


def test_needs_synthesis_wrapup_detects_planning_stub() -> None:
    assert needs_synthesis_wrapup(
        "Now let me query the order-level table for NVIDIA.",
        query_count=12,
    )
    assert not needs_synthesis_wrapup(
        "## 结论\n毛利率下降主要由客户结构变化驱动。",
        query_count=12,
    )


def test_stream_wrapup_on_empty_completion() -> None:
    agent = MagicMock()

    async def _events(*_args, **_kwargs):
        yield {
            "event": "on_tool_start",
            "name": "run_query_safely",
            "data": {"input": {"query": "SELECT 1"}},
            "run_id": "rq1",
        }

    agent.astream_events = _events
    agent.aget_state = AsyncMock(
        return_value=SimpleNamespace(
            values={
                "messages": [
                    SimpleNamespace(type="human", content="Why did GM% drop?", tool_calls=[]),
                    SimpleNamespace(
                        type="ai",
                        content="Now let me query customer breakdown.",
                        id="a1",
                        tool_calls=[],
                    ),
                ]
            },
            tasks=[],
        )
    )

    wrapup_model = MagicMock()

    async def _astream(_msgs):
        yield SimpleNamespace(content="## Answer\nGM% fell due to mix shift.")

    wrapup_model.astream = _astream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    config = {
        "configurable": {
            "thread_id": "t2",
            "run_segment": 1,
            "extended_run": False,
        }
    }

    async def _collect() -> list[str]:
        events: list[str] = []
        async for chunk in stream_agent_events(
            agent,
            {"messages": []},
            config,
            wrapup_model=wrapup_model,
        ):
            events.append(chunk)
        return events

    events = asyncio.run(_collect())

    assert any("event: wrapup_done" in e for e in events)
    assert any("event: token" in e and "mix shift" in e for e in events)
    assert any("event: done" in e and '"incomplete": true' in e for e in events)


def test_stream_wrapup_on_recursion_error() -> None:
    agent = MagicMock()

    async def _raise(*_args, **_kwargs):
        raise GraphRecursionError("limit")
        yield  # pragma: no cover

    agent.astream_events = _raise
    agent.aget_state = AsyncMock(
        return_value=SimpleNamespace(
            values={
                "messages": [
                    SimpleNamespace(type="human", content="Q", tool_calls=[]),
                ]
            },
            tasks=[],
        )
    )

    wrapup_model = MagicMock()

    async def _astream(_msgs):
        yield SimpleNamespace(content="Final answer.")

    wrapup_model.astream = _astream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    config = {
        "configurable": {
            "thread_id": "t1",
            "run_segment": 1,
            "extended_run": False,
        }
    }

    async def _collect() -> list[str]:
        events: list[str] = []
        async for chunk in stream_agent_events(
            agent, {"messages": []}, config, wrapup_model=wrapup_model
        ):
            events.append(chunk)
        return events

    events = asyncio.run(_collect())

    assert any("event: wrapup_done" in e for e in events)
    assert any("event: continue_prompt" in e for e in events)
    assert any("event: token" in e and "Final answer" in e for e in events)
    assert any("event: done" in e and '"incomplete": true' in e for e in events)


def test_topic_detect_followup() -> None:
    from app.agent.harness.topic_detect import detect_topic_relation as det

    r = det("继续按区域拆分", "NVIDIA 收入是多少")
    assert r["relation"] == "followup"
    assert r["suggest_new_thread"] is False


def test_topic_detect_new_topic() -> None:
    from app.agent.harness.topic_detect import detect_topic_relation as det

    r = det(
        "帮我分析 Dell 服务器库存周转率和缺货风险",
        "NVIDIA GPU 在 FY24 的 NGM 趋势",
    )
    assert r.get("suggest_new_thread") is True
