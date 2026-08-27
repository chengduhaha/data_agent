from __future__ import annotations

import contextvars

from app.agent.harness.budget_registry import (
    BudgetRegistry,
    get_active_budget_registry,
    set_active_budget_registry,
)
from app.agent.harness.segment import RunSegment, SpilledFile
from app.agent.harness.segment_manager import SegmentManager


def test_budget_merge_skill_wins() -> None:
    registry = BudgetRegistry(
        skill_budgets={"q": 12},
        dw_budgets={"q": 5, "hive": 1},
        merge_strategy="skill_wins",
    )
    assert registry.get_budget("q") == 12
    assert registry.get_budget("hive") == 1
    assert registry.get_budget("read_file") is None
    assert registry.is_governed("read_file") is False


def test_budget_merge_min_max() -> None:
    assert BudgetRegistry({"q": 12}, {"q": 5}, "min").get_budget("q") == 5
    assert BudgetRegistry({"q": 12}, {"q": 5}, "max").get_budget("q") == 12


def test_segment_evict() -> None:
    mgr = SegmentManager(max_per_thread=50)
    for i in range(1, 6):
        mgr.reset("t", i)
        if i <= 2:
            mgr.close("t", i)
    removed = mgr.evict_old_segments(3)
    assert removed >= 0


def test_segment_to_dw_context_syncs_query_budgets() -> None:
    set_active_budget_registry(
        BudgetRegistry(skill_budgets={"run_query": 5}, dw_budgets={"hive_query": 2})
    )
    try:
        segment = RunSegment(thread_id="t-sync", segment_id=1)
        segment.tool_call_counts["run_query"] = 2
        ctx = segment.to_dw_context()
        assert ctx is not None
        assert ctx.query_budgets.get("run_query") == 5
        assert ctx.query_budgets.get("hive_query") == 2
        assert ctx.query_counts.get("run_query") == 2
    finally:
        set_active_budget_registry(None)


def test_budget_registry_context_isolation() -> None:
    reg_a = BudgetRegistry(skill_budgets={"q": 1})
    reg_b = BudgetRegistry(skill_budgets={"q": 99})

    def _run_a() -> int | None:
        set_active_budget_registry(reg_a)
        got = get_active_budget_registry()
        return got.get_budget("q") if got is not None else None

    def _run_b() -> int | None:
        set_active_budget_registry(reg_b)
        got = get_active_budget_registry()
        return got.get_budget("q") if got is not None else None

    ctx_a = contextvars.copy_context()
    ctx_b = contextvars.copy_context()
    assert ctx_a.run(_run_a) == 1
    assert ctx_b.run(_run_b) == 99
    assert get_active_budget_registry() is None


def test_segment_to_dw_context_sums_token_budget_used() -> None:
    segment = RunSegment(thread_id="t-tokens", segment_id=1)
    segment.spilled_files = [
        SpilledFile(tool_name="run_query", call_index=1, path="/tmp/a", token_estimate=1200),
        SpilledFile(tool_name="run_query", call_index=2, path="/tmp/b", token_estimate=800),
    ]
    ctx = segment.to_dw_context()
    assert ctx is not None
    assert ctx.token_budget_used == 2000


def test_segment_to_dw_context_syncs_tool_call_indexes() -> None:
    segment = RunSegment(thread_id="t-idx", segment_id=1)
    segment.dw_tool_call_indexes = {"run_query": 3}
    ctx = segment.to_dw_context()
    assert ctx is not None
    assert ctx.tool_call_indexes.get("run_query") == 3
