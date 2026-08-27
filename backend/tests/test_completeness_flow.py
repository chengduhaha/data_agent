"""Completeness finalization flow tests (no LangGraph import at module level)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.agent.harness.config import HarnessConfig


@pytest.mark.asyncio
async def test_try_completeness_finalization_prefers_enhanced_path(monkeypatch) -> None:
    from app.agent.streaming import _try_completeness_finalization

    enhanced_called = False

    async def _fake_enhanced(user_message, draft, thread_id, run_segment):
        nonlocal enhanced_called
        enhanced_called = True
        return SimpleNamespace(
            is_complete=False,
            violations=[SimpleNamespace(violation_type=SimpleNamespace(value="CONSTRAINT"))],
        )

    monkeypatch.setattr(
        "app.agent.streaming.check_completeness_enhanced",
        _fake_enhanced,
    )

    async def _fail_regex(*_args, **_kwargs):
        raise AssertionError("regex fallback should not run when enhanced returns a result")

    monkeypatch.setattr("app.agent.streaming.assess_completeness", _fail_regex)

    agent = AsyncMock()
    agent.aget_state.return_value = SimpleNamespace(
        values={
            "messages": [
                SimpleNamespace(type="human", content="list top 5 products", tool_calls=[]),
                SimpleNamespace(type="ai", content="1. a\n2. b", tool_calls=[]),
            ]
        }
    )
    wrapup_model = MagicMock()

    async def _empty_astream(_msgs):
        if False:
            yield SimpleNamespace(content="")

    wrapup_model.astream = _empty_astream
    wrapup_model.bind = MagicMock(return_value=wrapup_model)

    harness_cfg = HarnessConfig(auto_wrapup=True)
    gen = await _try_completeness_finalization(
        agent,
        {"configurable": {"thread_id": "t-enh", "run_segment": 1}},
        wrapup_model,
        harness_cfg,
        executed_queries=[],
        streamed_text="1. a\n2. b",
        synthesis_wrapup_ran=False,
    )
    assert enhanced_called is True
    assert gen is not None
    chunks = [c async for c in gen]
    assert any("enhanced_completeness" in c for c in chunks)
