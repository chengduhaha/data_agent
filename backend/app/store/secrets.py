"""Redact sensitive values before sending config to the browser."""

from __future__ import annotations

import copy
import re
from typing import Any

_MASK = "****"
_SENSITIVE_KEY = re.compile(
    r"(api[_-]?key|secret|password|token|authorization|credential|x-api-key)",
    re.IGNORECASE,
)


def _is_masked(value: str) -> bool:
    v = value.strip()
    return not v or v == _MASK or "…" in v or v.endswith("…")


def mask_string(value: str, *, preview: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= preview:
        return _MASK
    return value[:preview] + "…"


def redact_mapping(data: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with sensitive string values masked and *_set flags added."""
    out: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, dict):
            out[key] = redact_mapping(value)
            continue
        if isinstance(value, str) and _SENSITIVE_KEY.search(key):
            if value:
                out[key] = mask_string(value)
                out[f"{key}_set"] = True
            else:
                out[key] = ""
                out[f"{key}_set"] = False
        else:
            out[key] = value
    return out


def merge_preserved_secrets(
    incoming: dict[str, Any],
    existing: dict[str, Any],
) -> dict[str, Any]:
    """When client sends masked secrets, keep server-side originals."""
    merged = copy.deepcopy(incoming)
    for key, value in existing.items():
        if key.endswith("_set"):
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_preserved_secrets(merged[key], value)
            continue
        if isinstance(value, str) and _SENSITIVE_KEY.search(key):
            inc = merged.get(key)
            if isinstance(inc, str) and _is_masked(inc) and value:
                merged[key] = value
    return merged
