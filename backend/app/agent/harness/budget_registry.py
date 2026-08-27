"""Unified tool-budget declaration registry (C2)."""

from __future__ import annotations

import contextvars
from typing import Literal


class BudgetRegistry:
    """Merge skill + DW budgets. Undeclared tools are ungoverned (return None)."""

    def __init__(
        self,
        skill_budgets: dict[str, int] | None = None,
        dw_budgets: dict[str, int] | None = None,
        merge_strategy: Literal["skill_wins", "min", "max"] = "skill_wins",
    ) -> None:
        self.skill_budgets = dict(skill_budgets or {})
        self.dw_budgets = dict(dw_budgets or {})
        self.merge_strategy = merge_strategy
        self._merged = self._merge()

    def _merge(self) -> dict[str, int]:
        names = set(self.skill_budgets) | set(self.dw_budgets)
        merged: dict[str, int] = {}
        for name in names:
            skill = self.skill_budgets.get(name)
            dw = self.dw_budgets.get(name)
            if skill is None:
                merged[name] = int(dw or 0)
                continue
            if dw is None:
                merged[name] = skill
                continue
            if self.merge_strategy == "min":
                merged[name] = min(skill, dw)
            elif self.merge_strategy == "max":
                merged[name] = max(skill, dw)
            else:
                merged[name] = skill
        return merged

    def get_budget(self, tool_name: str) -> int | None:
        if tool_name in self._merged:
            return self._merged[tool_name]
        if "*" in self._merged:
            return self._merged["*"]
        return None

    def is_governed(self, tool_name: str) -> bool:
        return self.get_budget(tool_name) is not None

    def all_budgets(self) -> dict[str, int]:
        return dict(self._merged)


_active_registry: contextvars.ContextVar[BudgetRegistry | None] = contextvars.ContextVar(
    "active_budget_registry", default=None
)


def set_active_budget_registry(registry: BudgetRegistry | None) -> None:
    _active_registry.set(registry)


def get_active_budget_registry() -> BudgetRegistry | None:
    return _active_registry.get()
