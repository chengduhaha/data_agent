"""Governance settings + pack listing (v2.0)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.harness.config import load_harness_config
from app.agent.harness.runtime_overrides import get_overrides, set_overrides

router = APIRouter(prefix="/api", tags=["governance"])


class GovernancePatch(BaseModel):
    budget_warn_threshold: float | None = None
    segment_max_per_thread: int | None = None
    evidence_max_items: int | None = None
    enable_dw_governance: bool | None = None
    enable_completeness_enhanced: bool | None = None
    enable_pack_framework: bool | None = None
    forward_instruction_language: str | None = None


@router.get("/governance")
async def get_governance() -> dict[str, Any]:
    cfg = load_harness_config()
    return {
        "config": {
            "budget_warn_threshold": cfg.budget_warn_threshold,
            "segment_max_per_thread": cfg.segment_max_per_thread,
            "evidence_max_items": cfg.evidence_max_items,
            "enable_dw_governance": cfg.enable_dw_governance,
            "enable_completeness_enhanced": cfg.enable_completeness_enhanced,
            "enable_pack_framework": cfg.enable_pack_framework,
            "forward_instruction_language": cfg.forward_instruction_language,
            "budget_merge_strategy": cfg.budget_merge_strategy,
        },
        "overrides": get_overrides(),
    }


@router.put("/governance")
async def put_governance(body: GovernancePatch) -> dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    set_overrides(payload)
    return await get_governance()


@router.get("/packs")
async def list_packs() -> dict[str, Any]:
    try:
        from agent_pack_framework import PackRegistry
    except ImportError:
        return {"installed": False, "packs": [], "message": "Pack Framework not installed"}
    registry = PackRegistry()
    current = registry.current()
    return {
        "installed": True,
        "packs": [item.model_dump() for item in registry.list()],
        "current": current.manifest.name if current else None,
    }


class PackActivateBody(BaseModel):
    name: str = Field(min_length=1)


@router.post("/packs/activate")
async def activate_pack(body: PackActivateBody) -> dict[str, Any]:
    try:
        from agent_pack_framework import PackRegistry
    except ImportError:
        return {"ok": False, "message": "Pack Framework not installed"}
    registry = PackRegistry()
    registry.activate(body.name)
    current = registry.current()
    return {"ok": True, "current": current.manifest.name if current else None}
