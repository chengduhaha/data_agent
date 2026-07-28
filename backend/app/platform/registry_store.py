"""Read/write ``backend/platform/registry.json`` publish metadata."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app.store import paths as store_paths


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_registry() -> dict[str, Any]:
    if not store_paths.PLATFORM_REGISTRY_PATH.exists():
        return {"skills": {}, "mcp": {}}
    try:
        data = json.loads(store_paths.PLATFORM_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"skills": {}, "mcp": {}}
    if not isinstance(data, dict):
        return {"skills": {}, "mcp": {}}
    data.setdefault("skills", {})
    data.setdefault("mcp", {})
    return data


def save_registry(data: dict[str, Any]) -> None:
    store_paths.PLATFORM_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    store_paths.PLATFORM_REGISTRY_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def record_skill_publish(name: str, *, published_by: str, version: str = "") -> None:
    reg = load_registry()
    skills = reg.setdefault("skills", {})
    skills[name] = {
        "published_by": published_by,
        "version": version,
        "published_at": _now(),
    }
    save_registry(reg)


def record_mcp_publish(name: str, *, published_by: str) -> None:
    reg = load_registry()
    mcp = reg.setdefault("mcp", {})
    mcp[name] = {
        "published_by": published_by,
        "published_at": _now(),
    }
    save_registry(reg)


def remove_skill_record(name: str) -> None:
    reg = load_registry()
    skills = reg.get("skills") or {}
    if name in skills:
        del skills[name]
        save_registry(reg)


def remove_mcp_record(name: str) -> None:
    reg = load_registry()
    mcp = reg.get("mcp") or {}
    if name in mcp:
        del mcp[name]
        save_registry(reg)
