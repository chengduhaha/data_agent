"""Organization MCP servers injected server-side (not stored in user mcp.json)."""

from __future__ import annotations

import os

from app.store.schemas import McpConfig, McpServerConfig

ORG_VERTICA_SERVER = "gateway-vertica-prod"


def load_org_mcp_config() -> McpConfig:
    """Build org MCP config from environment / .env.secrets (never persisted per user)."""
    api_key = (os.getenv("VERTICA_API_KEY") or "").strip()
    host = (os.getenv("VERTICA_HOST") or "").strip()
    database = (os.getenv("VERTICA_DATABASE") or "").strip()
    user = (os.getenv("VERTICA_USER") or "").strip()
    password = (os.getenv("VERTICA_PASSWORD") or "").strip()
    if not all([api_key, host, database, user, password]):
        return McpConfig()

    url = (
        os.getenv("VERTICA_MCP_URL")
        or "https://ai-gateway.synnex.org/mcp-gateway/api/v1/mcp/vertica"
    ).strip()
    port = (os.getenv("VERTICA_PORT") or "5433").strip()
    ssl = (os.getenv("VERTICA_SSL") or "false").strip()
    ssl_reject = (os.getenv("VERTICA_SSL_REJECT_UNAUTHORIZED") or "true").strip()

    return McpConfig(
        mcpServers={
            ORG_VERTICA_SERVER: McpServerConfig(
                transport="streamable_http",
                url=url,
                headers={
                    "x-api-key": api_key,
                    "X-Vertica-Host": host,
                    "X-Vertica-Port": port,
                    "X-Vertica-Database": database,
                    "X-Vertica-User": user,
                    "X-Vertica-Password": password,
                    "X-Vertica-SSL": ssl,
                    "X-Vertica-SSL-Reject-Unauthorized": ssl_reject,
                },
                enabled=True,
            )
        }
    )


def org_mcp_summary() -> list[dict[str, object]]:
    """Public metadata for Settings UI (no secrets)."""
    cfg = load_org_mcp_config()
    out: list[dict[str, object]] = []
    for name, server in cfg.mcpServers.items():
        out.append(
            {
                "name": name,
                "enabled": server.enabled,
                "managed": True,
                "transport": server.transport,
                "url": server.url,
                "description": "Organization-managed MCP (secrets held server-side)",
            }
        )
    return out
