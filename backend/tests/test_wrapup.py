"""Tests for wrap-up on step budget exhaustion."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from langgraph.errors import GraphRecursionError

from app.agent.harness.wrapup import (
    _build_wrapup_context,
    count_research_tool_calls,
    count_sql_evidence_in_messages,
    last_ai_text,
    looks_like_substantial_answer,
    looks_truncated,
    missing_answer_in_stream,
    needs_final_answer_wrapup,
    needs_synthesis_wrapup,
    stream_wrapup_tokens,
)
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
    assert needs_synthesis_wrapup(
        "### Analysis Approach Needed\n\n- Confirm month mapping",
        query_count=12,
    )
    assert not needs_synthesis_wrapup(
        "## 结论\n毛利率下降主要由客户结构变化驱动。",
        query_count=12,
    )
    assert not needs_synthesis_wrapup(
        "## Summary\n\nNGM% declined because of mix shift.",
        query_count=12,
    )


def test_stream_wrapup_preserves_chunk_whitespace() -> None:
    agent = MagicMock()
    agent.aget_state = AsyncMock(return_value=SimpleNamespace(values={"messages": []}))
    model = MagicMock()

    async def _astream(_msgs):
        yield SimpleNamespace(content="## Summary\n\n")
        yield SimpleNamespace(content="NGM% declined.\n\n## Evidence\n\n")
        yield SimpleNamespace(content="| Metric | Value |\n| :--- | :--- |\n")

    model.astream = _astream
    model.bind = MagicMock(return_value=model)
    config = {"configurable": {"thread_id": "t-wrap", "run_segment": 1}}

    async def _collect() -> str:
        parts: list[str] = []
        async for piece in stream_wrapup_tokens(model, agent, config):
            parts.append(piece)
        return "".join(parts)

    text = asyncio.run(_collect())
    assert "## Summary\n\nNGM% declined." in text
    assert "NGM% declined.\n\n## Evidence\n\n| Metric" in text


def test_needs_synthesis_wrapup_long_planning_with_many_queries() -> None:
    planning = "Let me analyze this step by step. " * 30
    assert len(planning) > 400
    assert needs_synthesis_wrapup(planning, query_count=9)


def test_needs_synthesis_wrapup_based_on_without_summary() -> None:
    mixed = (
        "Let me execute the query.\n\n"
        "Based on the database query for PM 706187, NGM% fell in March."
    )
    assert needs_synthesis_wrapup(mixed, query_count=9)
    assert not needs_synthesis_wrapup(
        "## Summary\n\nBased on the database query, NGM% fell.",
        query_count=9,
    )


def test_missing_answer_in_stream() -> None:
    streamed = "Let me analyze this."
    ckpt = "## Summary\n\nNGM% dropped due to mix shift."
    assert missing_answer_in_stream(streamed, ckpt) == ckpt
    assert missing_answer_in_stream(ckpt, ckpt) == ""
    assert missing_answer_in_stream("", ckpt) == ckpt


def test_looks_truncated_and_substantial_chinese_answer() -> None:
    truncated = (
        "C. 供应商维度分析\n\n"
        "| Vendor | Feb |\n| :--- | :--- |\n| NVIDIA | 1 |\n\n"
        "D. 订单分析\n该单一业务链的 NGM% 从 2 月的 3.783% 降至 3 月的 1.767%。由于其绝对体量巨大，该"
    )
    assert looks_truncated(truncated)
    complete = truncated + "客户组合是主要驱动因素。"
    assert not looks_truncated(complete)
    assert looks_like_substantial_answer(complete)
    assert not needs_final_answer_wrapup(
        "Let me dig deeper.",
        query_count=4,
        streamed_text=complete,
    )


def test_last_ai_text_scopes_to_current_turn() -> None:
    messages = [
        SimpleNamespace(type="human", content="Q1", tool_calls=[]),
        SimpleNamespace(type="ai", content="## Summary\nAnswer one.", tool_calls=[]),
        SimpleNamespace(type="human", content="Q2", tool_calls=[]),
        SimpleNamespace(type="ai", content="Now let me query.", tool_calls=[]),
        SimpleNamespace(type="ai", content="", tool_calls=[]),
    ]
    assert last_ai_text(messages) == "Now let me query."
    assert last_ai_text(messages, current_turn_only=False) == "Now let me query."


def test_last_ai_text_skips_trailing_empty_assistant() -> None:
    messages = [
        SimpleNamespace(type="human", content="Why?", tool_calls=[]),
        SimpleNamespace(
            type="ai",
            content="Now let me synthesize the answer.",
            tool_calls=[],
        ),
        SimpleNamespace(type="tool", content="ok", tool_calls=[]),
        SimpleNamespace(type="ai", content="", tool_calls=[]),
    ]
    assert last_ai_text(messages) == "Now let me synthesize the answer."


def test_count_sql_evidence_in_messages() -> None:
    messages = [
        SimpleNamespace(
            type="ai",
            content="",
            tool_calls=[
                {
                    "name": "run_query_safely",
                    "args": {"query": "SELECT 1 AS x"},
                }
            ],
        ),
        SimpleNamespace(
            type="ai",
            content="",
            tool_calls=[
                {
                    "name": "run_query_safely",
                    "args": {"query": "SELECT 1 AS x"},
                }
            ],
        ),
    ]
    assert count_sql_evidence_in_messages(messages) == 1


def test_needs_final_answer_wrapup_require_synthesis_without_sql() -> None:
    planning = (
        "The golden case routes to dm_disty_brpt_pm_mtd for NGM, "
        "but the PM table only has gross_sales and net_sales."
    )
    assert needs_final_answer_wrapup(
        planning,
        query_count=0,
        require_synthesis=True,
        research_tool_count=21,
    )
    assert not needs_final_answer_wrapup(
        "## Summary\n\nNGM% fell due to mix shift.",
        query_count=0,
        require_synthesis=True,
        research_tool_count=21,
    )


def test_needs_final_answer_wrapup_research_heavy_without_sql() -> None:
    assert needs_final_answer_wrapup(
        "Let me check the metric-index for ngm_amt PM routing.",
        query_count=0,
        research_tool_count=12,
    )
    assert not needs_final_answer_wrapup(
        "Let me check the metric-index.",
        query_count=0,
        research_tool_count=3,
    )


def test_count_research_tool_calls() -> None:
    messages = [
        SimpleNamespace(
            type="ai",
            content="",
            tool_calls=[{"name": "read_file", "args": {}}],
        ),
        SimpleNamespace(
            type="ai",
            content="",
            tool_calls=[{"name": "grep", "args": {}}],
        ),
    ]
    assert count_research_tool_calls(messages) == 2


def test_stream_wrapup_when_research_only_contract_skill() -> None:
    agent = MagicMock()

    async def _events(*_args, **_kwargs):
        if False:
            yield {}

    agent.astream_events = _events
    planning = (
        "The golden case routes to dm_disty_brpt_pm_mtd for NGM, "
        "but the PM table only has gross_sales and net_sales."
    )
    agent.aget_state = AsyncMock(
        return_value=SimpleNamespace(
            values={
                "messages": [
                    SimpleNamespace(type="human", content="Why did NGM% drop?", tool_calls=[]),
                    SimpleNamespace(
                        type="ai",
                        content="",
                        tool_calls=[{"name": "read_file", "args": {"file_path": "/x"}}],
                    ),
                    SimpleNamespace(type="tool", content="table schema", tool_calls=[]),
                    SimpleNamespace(type="ai", content=planning, tool_calls=[]),
                ]
            },
            tasks=[],
            next=[],
        )
    )

    wrapup_model = MagicMock()

    async def _astream(_msgs):
        yield SimpleNamespace(content="## Summary\nResearch incomplete; NGM% needs SQL evidence.")

    wrapup_model.astream = _astream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    config = {
        "configurable": {
            "thread_id": "t-research-only",
            "run_segment": 1,
            "extended_run": False,
        }
    }

    from app.agent.harness.context import set_harness_context, reset_harness_context

    token = set_harness_context(
        thread_id="t-research-only",
        run_segment=1,
        require_synthesis=True,
    )

    async def _collect() -> list[str]:
        events: list[str] = []
        async for chunk in stream_agent_events(
            agent,
            None,
            config,
            wrapup_model=wrapup_model,
        ):
            events.append(chunk)
        return events

    try:
        events = asyncio.run(_collect())
    finally:
        reset_harness_context(token)

    assert any("event: wrapup_done" in e for e in events)
    assert any("event: token" in e and "NGM%" in e for e in events)
    assert any("event: done" in e and '"incomplete": true' in e for e in events)


def test_stream_wrapup_when_final_assistant_empty_but_sql_in_checkpoint() -> None:
    agent = MagicMock()

    async def _events(*_args, **_kwargs):
        if False:
            yield {}

    agent.astream_events = _events
    agent.aget_state = AsyncMock(
        return_value=SimpleNamespace(
            values={
                "messages": [
                    SimpleNamespace(type="human", content="Why did NGM% drop?", tool_calls=[]),
                    SimpleNamespace(
                        type="ai",
                        content="",
                        tool_calls=[
                            {
                                "name": "run_query_safely",
                                "args": {"query": "SELECT ngm FROM t"},
                            }
                        ],
                    ),
                    SimpleNamespace(type="tool", content='[{"ngm": 1}]', tool_calls=[]),
                    SimpleNamespace(
                        type="ai",
                        content="Now let me synthesize the answer.",
                        tool_calls=[],
                    ),
                    SimpleNamespace(type="tool", content="todos done", tool_calls=[]),
                    SimpleNamespace(type="ai", content="", tool_calls=[]),
                ]
            },
            tasks=[],
            next=[],
        )
    )

    wrapup_model = MagicMock()

    async def _astream(_msgs):
        yield SimpleNamespace(content="## Summary\nNGM% fell due to mix.")

    wrapup_model.astream = _astream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    config = {
        "configurable": {
            "thread_id": "t-continue-end",
            "run_segment": 2,
            "extended_run": False,
        }
    }

    async def _collect() -> list[str]:
        events: list[str] = []
        async for chunk in stream_agent_events(
            agent,
            None,
            config,
            wrapup_model=wrapup_model,
        ):
            events.append(chunk)
        return events

    events = asyncio.run(_collect())

    assert any("event: wrapup_done" in e for e in events)
    assert any("event: token" in e and "NGM%" in e for e in events)
    assert any("event: done" in e and '"incomplete": true' in e for e in events)


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


def test_stream_flushes_checkpoint_answer_when_tokens_missing() -> None:
    agent = MagicMock()
    final_answer = "## Summary\n\nNGM% fell due to mix shift in March."

    async def _events(*_args, **_kwargs):
        yield {
            "event": "on_chat_model_stream",
            "data": {"chunk": SimpleNamespace(content="Let me analyze the vendor data.")},
        }
        yield {
            "event": "on_tool_start",
            "name": "run_query_safely",
            "data": {"input": {"query": "SELECT 1"}},
            "run_id": "rq1",
        }
        yield {
            "event": "on_tool_end",
            "name": "run_query_safely",
            "data": {"output": '[{"x":1}]'},
            "run_id": "rq1",
        }

    agent.astream_events = _events
    agent.aget_state = AsyncMock(
        return_value=SimpleNamespace(
            values={
                "messages": [
                    SimpleNamespace(type="human", content="Why did NGM% drop?", tool_calls=[]),
                    SimpleNamespace(type="ai", content="Let me analyze the vendor data.", tool_calls=[]),
                    SimpleNamespace(
                        type="ai",
                        content="",
                        tool_calls=[{"name": "run_query_safely", "args": {"query": "SELECT 1"}}],
                    ),
                    SimpleNamespace(type="tool", content='[{"x":1}]', tool_calls=[]),
                    SimpleNamespace(type="ai", content=final_answer, tool_calls=[]),
                ]
            },
            tasks=[],
            next=[],
        )
    )

    config = {
        "configurable": {
            "thread_id": "t-flush",
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
            wrapup_model=None,
        ):
            events.append(chunk)
        return events

    events = asyncio.run(_collect())
    assert any("event: token" in e and "mix shift" in e for e in events)
    assert any("event: done" in e for e in events)


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
