from __future__ import annotations

from app.agent.harness.budget_registry import BudgetRegistry
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
    assert removed >= 1
    assert mgr.get("t", 5).segment_id == 5
