"""MCP server configuration routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.agent.mcp_manager import mcp_manager
from app.deps import get_user_id
from app.org.mcp import org_mcp_summary
from app.store.io import load_mcp_config, save_mcp_config
from app.store.schemas import McpConfig, McpServerConfig
from app.store.secrets import merge_preserved_secrets, redact_mapping

router = APIRouter(prefix="/api/mcp", tags=["mcp"])


def _redact_mcp_response(data: dict) -> dict:
    redacted = redact_mapping(data)
    redacted["org_servers"] = org_mcp_summary()
    return redacted


@router.get("")
async def get_mcp(user_id: str = Depends(get_user_id)):
    cfg = await load_mcp_config(user_id)
    return _redact_mcp_response(cfg.model_dump())


@router.put("")
async def put_mcp(body: McpConfig, user_id: str = Depends(get_user_id)):
    existing = await load_mcp_config(user_id)
    merged = merge_preserved_secrets(body.model_dump(), existing.model_dump())
    saved = await save_mcp_config(user_id, McpConfig.model_validate(merged))
    await mcp_manager.invalidate(user_id)
    return _redact_mcp_response(saved.model_dump())


@router.post("/test")
async def test_mcp(server: McpServerConfig):
    return await mcp_manager.test_connection(server)


@router.get("/tools")
async def mcp_tools(user_id: str = Depends(get_user_id)):
    tools = await mcp_manager.get_tools(user_id)
    return {
        "tools": [
            {
                "name": getattr(t, "name", str(t)),
                "description": getattr(t, "description", "") or "",
            }
            for t in tools
        ],
        "org_servers": org_mcp_summary(),
    }


@router.get("/health")
async def mcp_health(user_id: str = Depends(get_user_id)):
    """Per-server MCP reachability (cached ~30s)."""
    return {"servers": await mcp_manager.health_check(user_id)}
