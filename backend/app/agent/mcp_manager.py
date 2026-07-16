"""Per-user MCP client manager using langchain-mcp-adapters."""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.tools import BaseTool

from app.agent.harness.config import load_harness_config
from app.store.io import load_effective_mcp_config
from app.store.schemas import McpConfig, McpServerConfig

logger = logging.getLogger(__name__)

try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
except ImportError:  # pragma: no cover
    MultiServerMCPClient = None  # type: ignore[misc, assignment]


# Vertica MCP tools exposed to the agent (execution-only; metadata tools filtered).
VERTICA_ALLOWED_TOOLS = frozenset({
    "run_query_safely",
    "execute_query_paginated",
})


class McpManager:
    """Cache MultiServerMCPClient instances per user and expose tools."""

    def __init__(self) -> None:
        self._clients: dict[str, Any] = {}
        self._tool_cache: dict[str, list[BaseTool]] = {}
        self._config_fingerprint: dict[str, str] = {}

    def _fingerprint(self, cfg: McpConfig) -> str:
        return cfg.model_dump_json()

    @staticmethod
    def _server_to_connection(
        server: McpServerConfig,
        *,
        mcp_timeout: float = 60.0,
    ) -> dict[str, Any] | None:
        transport = server.transport
        if transport == "stdio":
            if not server.command:
                return None
            conn: dict[str, Any] = {
                "transport": "stdio",
                "command": server.command,
                "args": server.args or [],
            }
            if server.env:
                conn["env"] = server.env
            return conn
        if transport in ("streamable_http", "sse"):
            if not server.url:
                return None
            conn = {
                "transport": transport,
                "url": server.url,
                "timeout": mcp_timeout,
                "sse_read_timeout": mcp_timeout,
            }
            if server.headers:
                conn["headers"] = server.headers
            return conn
        return None

    def _to_client_connections(self, cfg: McpConfig) -> dict[str, dict[str, Any]]:
        harness_cfg = load_harness_config()
        connections: dict[str, dict[str, Any]] = {}
        for name, server in cfg.mcpServers.items():
            if not server.enabled:
                continue
            entry = self._server_to_connection(server, mcp_timeout=harness_cfg.mcp_timeout)
            if entry:
                connections[name] = entry
        return connections

    async def get_client(self, user_id: str, cfg: McpConfig | None = None) -> Any | None:
        if MultiServerMCPClient is None:
            logger.warning("langchain-mcp-adapters not installed")
            return None
        cfg = cfg or await load_effective_mcp_config(user_id)
        fp = self._fingerprint(cfg)
        if user_id in self._clients and self._config_fingerprint.get(user_id) == fp:
            return self._clients[user_id]

        await self.invalidate(user_id)
        connections = self._to_client_connections(cfg)
        if not connections:
            return None
        client = MultiServerMCPClient(connections)
        self._clients[user_id] = client
        self._config_fingerprint[user_id] = fp
        return client

    async def get_tools(self, user_id: str, cfg: McpConfig | None = None) -> list[BaseTool]:
        cfg = cfg or await load_effective_mcp_config(user_id)
        fp = self._fingerprint(cfg)
        if user_id in self._tool_cache and self._config_fingerprint.get(user_id) == fp:
            return self._tool_cache[user_id]

        client = await self.get_client(user_id, cfg)
        if client is None:
            self._tool_cache[user_id] = []
            return []
        try:
            tools = await client.get_tools()
        except Exception:
            logger.exception("Failed to load MCP tools for user=%s", user_id)
            tools = []
        tools = self._filter_tools(tools, cfg)
        self._tool_cache[user_id] = list(tools)
        return self._tool_cache[user_id]

    def _filter_tools(self, tools: list[BaseTool], cfg: McpConfig) -> list[BaseTool]:
        """Hide Vertica metadata/discovery tools when a Vertica MCP server is enabled."""
        has_vertica = any(
            server.enabled and "vertica" in name.lower()
            for name, server in cfg.mcpServers.items()
        )
        if not has_vertica:
            return list(tools)
        kept: list[BaseTool] = []
        for tool in tools:
            name = getattr(tool, "name", "") or ""
            base = name.split("__")[-1] if "__" in name else name
            if base not in VERTICA_ALLOWED_TOOLS:
                logger.info("MCP tool filtered (vertica allowlist): %s", name)
                continue
            kept.append(tool)
        return kept

    async def test_connection(self, server: McpServerConfig) -> dict[str, Any]:
        if MultiServerMCPClient is None:
            return {"ok": False, "error": "langchain-mcp-adapters not installed"}
        conn = self._server_to_connection(
            server,
            mcp_timeout=load_harness_config().mcp_timeout,
        )
        if not conn:
            return {"ok": False, "error": "Invalid server configuration"}
        try:
            client = MultiServerMCPClient({"test": conn})
            tools = await client.get_tools()
            return {
                "ok": True,
                "tool_count": len(tools),
                "tools": [getattr(t, "name", str(t)) for t in tools[:50]],
            }
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    async def invalidate(self, user_id: str) -> None:
        client = self._clients.pop(user_id, None)
        self._tool_cache.pop(user_id, None)
        self._config_fingerprint.pop(user_id, None)
        if client is not None:
            close = getattr(client, "aclose", None) or getattr(client, "close", None)
            if close:
                try:
                    result = close()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:
                    logger.debug("MCP client close failed for %s", user_id, exc_info=True)


mcp_manager = McpManager()
