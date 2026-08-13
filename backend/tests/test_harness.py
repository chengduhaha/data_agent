"""Harness middleware, continue SSE, org fragment policy, and completeness tests."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from langgraph.errors import GraphRecursionError

from app.agent.harness.completeness import (
    assess_completeness,
    extract_constraints,
)
from app.agent.harness.config import recursion_limit
from app.agent.harness.context import reset_harness_context, set_harness_context
from app.agent.harness.middleware import ToolGovernanceMiddleware, reset_segment_state
from app.agent.harness.phases import RunPhaseMiddleware, get_run_phase
from app.agent.harness.tool_budget import ToolBudgetMiddleware
from app.agent.harness.tools import _backend_grep, make_search_knowledge_tool
from app.agent.harness.wrapup import needs_final_answer_wrapup
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


def test_blocks_task_when_require_synthesis() -> None:
    token = set_harness_context(thread_id="t-harness", run_segment=1, require_synthesis=True)
    try:
        mw = ToolGovernanceMiddleware()
        blocked = mw._check(_mock_request("task", {"description": "delegate vertica"}))
        assert blocked is not None
        assert "contract-guided" in str(blocked.content).lower()
        assert "run_query_safely" in str(blocked.content).lower()
    finally:
        reset_harness_context(token)
        set_harness_context(thread_id="t-harness", run_segment=1)


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


def test_contract_skill_budget_forces_synthesis_after_12_sql() -> None:
    """Simulates the contract skill's `run_query_safely: 12` budget end-to-end."""
    budget_mw = ToolBudgetMiddleware({"run_query_safely": 12})
    phase_mw = RunPhaseMiddleware(tool_budgets={"run_query_safely": 12})
    req = _mock_request("run_query_safely", {"query": "select 1"})

    async def _handler(_request):
        return SimpleNamespace(content="1 row")

    async def _run_once():
        blocked_by_budget = await budget_mw.awrap_tool_call(req, _handler)
        return blocked_by_budget

    for _ in range(12):
        result = asyncio.run(_run_once())
        assert "Blocked" not in str(result.content)

    # 13th call is blocked by the tool budget itself.
    result_13 = asyncio.run(_run_once())
    assert "Blocked" in str(result_13.content)

    # RunPhase sees the same exhausted count and forces synthesize.
    asyncio.run(phase_mw.awrap_tool_call(req, _handler))
    assert get_run_phase("t-harness", 1) == "synthesize"


class _AgrepNoOutputMode:
    async def agrep(self, pattern: str, **kwargs):
        if "output_mode" in kwargs:
            raise TypeError("agrep() got an unexpected keyword argument 'output_mode'")
        return "path/to/file.md:10:matched line\nother.md:2:another"


async def _async_iter_empty():
    if False:
        yield None


async def _async_token_stream(text: str):
    yield SimpleNamespace(content=text)


def test_backend_grep_falls_back_without_output_mode() -> None:
    backend = _AgrepNoOutputMode()
    text = asyncio.run(
        _backend_grep(backend, "foo", "/knowledge/org", None, "content")
    )
    assert "matched line" in text


def test_backend_grep_files_with_matches_fallback() -> None:
    backend = _AgrepNoOutputMode()
    text = asyncio.run(
        _backend_grep(backend, "foo", "/knowledge/org", None, "files_with_matches")
    )
    assert "path/to/file.md" in text
    assert "other.md" in text


def test_search_knowledge_agrep_compat() -> None:
    tool = make_search_knowledge_tool(_AgrepNoOutputMode())
    raw = asyncio.run(
        tool.ainvoke({"pattern": "metric", "output_mode": "files_with_matches"})
    )
    payload = json.loads(raw)
    assert "error" not in payload
    assert payload["output_mode"] == "files_with_matches"
    assert "path/to/file.md" in payload["results"]


def test_extract_constraints_top_n_and_date() -> None:
    q = "Show negative orders on 2026-04-30. list top 10 descending."
    c = extract_constraints(q)
    assert c.top_n == 10
    assert "2026-04-30" in c.dates
    assert c.sort_direction == "desc"


def test_extract_constraints_no_constraints() -> None:
    c = extract_constraints("What is revenue?")
    assert c.top_n is None
    assert c.dates == []


def test_completeness_complete_table_top_n() -> None:
    answer = (
        "## Summary\n"
        "On 2026-04-30:\n\n"
        "| rank | value |\n| :--- | :--- |\n"
        + "\n".join(f"| {i} | {i * -1} |" for i in range(1, 11))
    )
    report = assess_completeness(
        "list top 10 on 2026-04-30",
        answer,
        query_count=1,
    )
    assert report.complete
    assert not report.needs_followup


def test_completeness_planning_only_incomplete() -> None:
    report = assess_completeness(
        "list top 10 on 2026-04-30",
        "Let me run a query to check the data.",
        query_count=2,
        research_tool_count=3,
    )
    assert not report.complete
    assert report.needs_followup
    assert report.evidence_present


def test_completeness_no_evidence_no_followup() -> None:
    report = assess_completeness(
        "list top 10",
        "Here is a short guess without tools.",
        query_count=0,
        research_tool_count=0,
    )
    assert not report.needs_followup


def test_completeness_missing_date_triggers_followup() -> None:
    answer = (
        "## Summary\n| rank | value |\n| :--- | :--- |\n"
        + "\n".join(f"| {i} | {i} |" for i in range(1, 11))
    )
    report = assess_completeness(
        "list top 10 on 2026-04-30",
        answer,
        query_count=1,
    )
    assert report.needs_followup
    assert any("date:2026-04-30" in m for m in report.missing_constraints)


def test_completeness_counts_tabular_rows_and_detects_missing_top_n() -> None:
    answer = (
        "查询已完成。\n\n"
        "order_no\tngm_amt\n"
        "-77294\t-3685483.0469\n"
        "621286\t-897747.9458\n"
        "657888\t-703095.5929\n"
        "141692\t-485643.2363\n"
        "413709\t-415449.3070\n"
    )
    report = assess_completeness(
        "list top 10",
        answer,
        query_count=1,
    )
    assert report.needs_followup
    assert any("top_n:10 (found 5)" in m for m in report.missing_constraints)


def test_stream_triggers_completeness_finalization_once() -> None:
    user_q = "list top 10 on 2026-04-30"
    table = "| rank | value |\n| :--- | :--- |\n" + "\n".join(
        f"| {i} | {i} |" for i in range(1, 6)
    )
    planning_answer = f"## Summary\n{table}"

    agent = MagicMock()

    async def _fake_astream_events(*_args, **_kwargs):
        if False:
            yield {}

    agent.astream_events = _fake_astream_events

    state = SimpleNamespace(
        values={
            "messages": [
                SimpleNamespace(type="human", content=user_q),
                SimpleNamespace(
                    type="ai",
                    content="",
                    tool_calls=[
                        {
                            "name": "run_query_safely",
                            "args": {"query": "select 1"},
                        }
                    ],
                ),
                SimpleNamespace(type="ai", content=planning_answer, tool_calls=[]),
            ]
        },
        tasks=[],
        next=[],
    )
    agent.aget_state = AsyncMock(return_value=state)

    wrapup_model = MagicMock()

    async def _fake_wrapup_stream(*_args, **_kwargs):
        yield SimpleNamespace(content="## Summary\ncompleted")

    wrapup_model.astream = _fake_wrapup_stream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    config = {
        "configurable": {
            "thread_id": "thread-comp",
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
    assert any("event: completeness_done" in e for e in events)
    assert sum(1 for e in events if "event: completeness_done" in e) == 1
    assert not needs_final_answer_wrapup(planning_answer, query_count=1)
