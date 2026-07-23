"""User config + provider catalog routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.agent.extensions.registry import capability_registry
from app.agent.model_catalog import catalog_as_api
from app.agent.models import list_providers
from app.deps import get_user_id
from app.store.io import load_effective_mcp_config, load_user_config, save_user_config
from app.store.schemas import UserConfig

router = APIRouter(prefix="/api", tags=["config"])


@router.get("/providers")
async def providers():
    return {"providers": [p.model_dump() for p in list_providers()]}


@router.get("/model-catalog")
async def model_catalog():
    """Synnex / Gateway preset profiles for Settings → Model."""
    return catalog_as_api()


@router.get("/config")
async def get_config(user_id: str = Depends(get_user_id)):
    cfg = await load_user_config(user_id)
    data = cfg.model_dump()
    # Mask api key in responses
    key = data.get("model", {}).get("api_key") or ""
    if key:
        data["model"]["api_key"] = key[:4] + "…" if len(key) > 4 else "****"
        data["model"]["api_key_set"] = True
    else:
        data["model"]["api_key_set"] = False
    return data


@router.get("/capabilities")
async def capabilities(user_id: str = Depends(get_user_id)):
    """Debug/UI endpoint: capabilities actually resolved for this user right now."""
    cfg = await load_user_config(user_id)
    resolved = await capability_registry.resolve(user_id, cfg)
    mcp_cfg = await load_effective_mcp_config(user_id)
    enabled_mcp = [
        name
        for name, server in mcp_cfg.mcpServers.items()
        if server.enabled and name not in set(cfg.disabled_mcp_servers)
    ]
    return {
        "extra_tools": sorted(resolved.extra_tool_names),
        "extra_mcp_servers": sorted(resolved.extra_mcp_servers),
        "enabled_mcp_servers": enabled_mcp,
        "rule_fragments": resolved.rule_fragments,
        "subagents": resolved.subagent_names,
        "harness": {
            "phases": resolved.harness.phases,
            "tool_budgets": resolved.harness.tool_budgets,
            "require_synthesis": resolved.harness.require_synthesis,
        },
        "subagent_routing": {
            "skill_names": resolved.subagent_routing.skill_names,
            "routes": [
                {
                    "id": r.id,
                    "label": r.label,
                    "configured": r.configured,
                    "description": r.description,
                }
                for r in resolved.subagent_routing.routes
            ],
        },
        "disabled_mcp_servers": cfg.disabled_mcp_servers,
        "feature_flags": cfg.feature_flags,
    }


@router.put("/config")
async def put_config(body: UserConfig, user_id: str = Depends(get_user_id)):
    existing = await load_user_config(user_id)
    # Preserve existing key if client sent masked/empty placeholder
    incoming_key = body.model.api_key or ""
    if (not incoming_key or "…" in incoming_key or incoming_key == "****") and existing.model.api_key:
        body.model.api_key = existing.model.api_key
    # Keep Synnex endpoint fields aligned with the selected catalog model
    from app.agent.model_catalog import apply_profile_to_model_config, get_catalog_meta

    if body.model.provider == get_catalog_meta().provider_id:
        apply_profile_to_model_config(body.model)
    saved = await save_user_config(user_id, body)
    data = saved.model_dump()
    key = data.get("model", {}).get("api_key") or ""
    if key:
        data["model"]["api_key"] = key[:4] + "…" if len(key) > 4 else "****"
        data["model"]["api_key_set"] = True
    else:
        data["model"]["api_key_set"] = False
    return data
