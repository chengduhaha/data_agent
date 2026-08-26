"""Mutable overlay on frozen HarnessConfig (Settings tab live updates)."""

from __future__ import annotations

from typing import Any

_overrides: dict[str, Any] = {}


def get_overrides() -> dict[str, Any]:
    return dict(_overrides)


def set_overrides(values: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "budget_warn_threshold",
        "segment_max_per_thread",
        "evidence_max_items",
        "enable_dw_governance",
        "enable_completeness_enhanced",
        "enable_pack_framework",
        "forward_instruction_language",
    }
    for key, value in values.items():
        if key in allowed:
            _overrides[key] = value
    return get_overrides()
