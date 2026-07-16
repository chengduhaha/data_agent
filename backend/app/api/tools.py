"""Tools catalog + enable/disable toggles."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.agent.builtin_tools import BUILTIN_TOOL_CATALOG
from app.agent.mcp_manager import mcp_manager
from app.deps import get_user_id
from app.store.io import load_user_config, save_user_config

router = APIRouter(prefix="/api/tools", tags=["tools"])


class ToolsUpdate(BaseModel):
    enabled_tools: dict[str, bool] = Field(default_factory=dict)


@router.get("")
async def list_tools(user_id: str = Depends(get_user_id)):
    cfg = await load_user_config(user_id)
    items = []
    for t in BUILTIN_TOOL_CATALOG:
        name = t["name"]
        enabled = True
        if t["source"] == "builtin":
            enabled = cfg.enabled_tools.get(name, True)
        items.append({**t, "enabled": enabled})

    mcp_tools = await mcp_manager.get_tools(user_id)
    for t in mcp_tools:
        items.append(
            {
                "name": getattr(t, "name", str(t)),
                "description": getattr(t, "description", "") or "",
                "source": "mcp",
                "enabled": True,
            }
        )
    return {"tools": items, "enabled_tools": cfg.enabled_tools}


@router.put("")
async def update_tools(body: ToolsUpdate, user_id: str = Depends(get_user_id)):
    cfg = await load_user_config(user_id)
    cfg.enabled_tools.update(body.enabled_tools)
    await save_user_config(user_id, cfg)
    return {"enabled_tools": cfg.enabled_tools}
