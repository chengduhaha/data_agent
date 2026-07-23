"""RunPhaseMiddleware + ToolBudgetMiddleware governance tests."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.agent.harness.config import HarnessConfig
from app.agent.harness.context import reset_harness_context, set_harness_context
from app.agent.harness.middleware import get_segment_state, reset_segment_state
from app.agent.harness.phases import RunPhaseMiddleware, get_run_phase
from app.agent.harness.tool_budget import ToolBudgetMiddleware


def _mock_request(tool: str, args: dict | None = None, call_id: str = "tc1") -> SimpleNamespace:
    return SimpleNamespace(tool_call={"name": tool, "args": args or {}, "id": call_id})


@pytest.fixture(autouse=True)
def _harness_ctx():
    token = set_harness_context(thread_id="t-phases", run_segment=1)
    reset_segment_state("t-phases", 1)
    yield
    reset_harness_context(token)


async def _ok_handler(_request):
    return SimpleNamespace(content="ok")


def test_tool_budget_blocks_after_limit() -> None:
    mw = ToolBudgetMiddleware({"run_query_safely": 2})
    req = _mock_request("run_query_safely", {"query": "select 1"})

    r1 = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    r2 = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    r3 = asyncio.run(mw.awrap_tool_call(req, _ok_handler))

    assert r1.content == "ok"
    assert r2.content == "ok"
    assert "Blocked" in str(r3.content)
    assert "budget exceeded" in str(r3.content).lower()


def test_tool_budget_ignores_ungoverned_tools() -> None:
    mw = ToolBudgetMiddleware({"run_query_safely": 1})
    req = _mock_request("read_file", {"file_path": "/workspace/x.md"})
    for _ in range(5):
        result = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
        assert result.content == "ok"


def test_run_phase_advances_research_to_execute() -> None:
    mw = RunPhaseMiddleware(HarnessConfig(), tool_budgets={"run_query_safely": 12})
    assert get_run_phase("t-phases", 1) == "research"
    req = _mock_request("run_query_safely", {"query": "select 1"})
    asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    assert get_run_phase("t-phases", 1) == "execute"


def test_run_phase_forces_synthesize_on_budget_exhaustion() -> None:
    mw = RunPhaseMiddleware(HarnessConfig(), tool_budgets={"run_query_safely": 3})
    req = _mock_request("run_query_safely", {"query": "select 1"})

    for _ in range(3):
        asyncio.run(mw.awrap_tool_call(req, _ok_handler))
        state = get_segment_state("t-phases", 1)
        state.tool_call_counts["run_query_safely"] = state.tool_call_counts.get(
            "run_query_safely", 0
        )

    # Manually bump the count past budget the way ToolBudgetMiddleware would.
    state = get_segment_state("t-phases", 1)
    state.tool_call_counts["run_query_safely"] = 3

    blocked = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    assert get_run_phase("t-phases", 1) == "synthesize"
    assert "Blocked" in str(blocked.content)
    assert "synthesize phase" in str(blocked.content).lower()


def test_tool_budget_blocks_at_twelve_sql_calls() -> None:
    """Acceptance #2: contract skill budget caps run_query_safely at 12."""
    mw = ToolBudgetMiddleware({"run_query_safely": 12})
    req = _mock_request("run_query_safely", {"query": "select 1"})
    for i in range(12):
        result = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
        assert result.content == "ok", f"call {i + 1} should succeed"
    blocked = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    assert "Blocked" in str(blocked.content)


def test_run_phase_forces_synthesize_near_step_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.agent.harness import phases as phases_mod

    monkeypatch.setattr(phases_mod, "step_warn_threshold", lambda extended_run=False: 2)
    mw = RunPhaseMiddleware(HarnessConfig(), tool_budgets={})
    state = get_segment_state("t-phases", 1)
    state.tool_step_count = 2
    req = _mock_request("some_tool", {})
    asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    assert get_run_phase("t-phases", 1) == "synthesize"


def test_run_phase_does_not_block_ungoverned_tools_in_synthesize() -> None:
    mw = RunPhaseMiddleware(HarnessConfig(), tool_budgets={"run_query_safely": 1})
    state = get_segment_state("t-phases", 1)
    state.phase = "synthesize"
    req = _mock_request("write_file", {"file_path": "/workspace/out.md"})
    result = asyncio.run(mw.awrap_tool_call(req, _ok_handler))
    assert result.content == "ok"
