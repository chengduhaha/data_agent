"""Platform MCP servers loaded from ``backend/platform/mcp/*.yaml`` manifests."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from app.store.paths import PLATFORM_MCP_DIR
from app.store.schemas import McpConfig, McpServerConfig

logger = logging.getLogger(__name__)

_PLACEHOLDER = re.compile(r"\$\{([A-Z0-9_]+)(?::([^}]*))?\}")


def _resolve_placeholders(value: str, env: dict[str, str]) -> str:
    def _sub(match: re.Match[str]) -> str:
        name, default = match.group(1), match.group(2)
        val = env.get(name, "")
        return val if val else (default or "")

    return _PLACEHOLDER.sub(_sub, value)


def _resolve_dict(data: dict[str, Any], env: dict[str, str]) -> dict[str, str]:
    return {k: _resolve_placeholders(str(v), env) for k, v in data.items()}


def _load_manifest_files() -> list[Path]:
    if not PLATFORM_MCP_DIR.exists():
        return []
    return sorted(PLATFORM_MCP_DIR.glob("*.yaml")) + sorted(PLATFORM_MCP_DIR.glob("*.yml"))


def _server_from_manifest(manifest: dict[str, Any], env: dict[str, str]) -> tuple[str, McpServerConfig] | None:
    name = str(manifest.get("name") or "").strip()
    if not name:
        return None
    required = list(manifest.get("required_env") or [])
    if required and not all((env.get(v) or "").strip() for v in required):
        return None

    transport = str(manifest.get("transport") or "streamable_http")
    headers = _resolve_dict(manifest.get("headers") or {}, env)

    if transport in ("streamable_http", "sse"):
        url_env = manifest.get("url_env")
        url = (
            (env.get(str(url_env)) or "").strip() if url_env else ""
        ) or str(manifest.get("url_default") or "").strip()
        if not url:
            return None
        return name, McpServerConfig(
            transport=transport,  # type: ignore[arg-type]
            url=url,
            headers=headers,
            enabled=True,
        )

    if transport == "stdio":
        command = manifest.get("command")
        if not command:
            return None
        args = [_resolve_placeholders(str(a), env) for a in (manifest.get("args") or [])]
        server_env = _resolve_dict(manifest.get("env") or {}, env)
        return name, McpServerConfig(
            transport="stdio",
            command=str(command),
            args=args,
            env=server_env,
            enabled=True,
        )

    return None


def load_platform_mcp_config(env: dict[str, str] | None = None) -> McpConfig:
    """Build platform MCP config from YAML manifests + process env."""
    import os

    env = env if env is not None else dict(os.environ)
    servers: dict[str, McpServerConfig] = {}
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            logger.warning("Failed to parse platform MCP manifest: %s", path, exc_info=True)
            continue
        if not isinstance(manifest, dict):
            continue
        entry = _server_from_manifest(manifest, env)
        if not entry:
            continue
        primary_name, server = entry
        servers[primary_name] = server
        for alias in manifest.get("aliases") or []:
            if isinstance(alias, str) and alias.strip():
                servers[alias.strip()] = server
    return McpConfig(mcpServers=servers)


def platform_mcp_allowed_tools(server_name: str) -> frozenset[str] | None:
    """Metadata-tool allowlist declared by a manifest."""
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(manifest, dict):
            continue
        names = {str(manifest.get("name") or "")}
        names.update(str(a) for a in (manifest.get("aliases") or []) if a)
        if server_name in names:
            allowed = manifest.get("allowed_tools")
            if allowed:
                return frozenset(str(t) for t in allowed)
            return None
    return None


def platform_mcp_summary() -> list[dict[str, object]]:
    """Public metadata for Settings UI (no secrets)."""
    cfg = load_platform_mcp_config()
    seen: set[str] = set()
    out: list[dict[str, object]] = []
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(manifest, dict):
            continue
        name = str(manifest.get("name") or "").strip()
        if not name or name not in cfg.mcpServers or name in seen:
            continue
        seen.add(name)
        server = cfg.mcpServers[name]
        out.append(
            {
                "name": name,
                "aliases": list(manifest.get("aliases") or []),
                "enabled": server.enabled,
                "managed": True,
                "transport": server.transport,
                "url": server.url,
                "description": str(
                    manifest.get("description")
                    or "Platform-managed MCP (secrets held server-side)"
                ),
            }
        )
    return out


def manifest_path_for_server(server_name: str) -> Path | None:
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(manifest, dict):
            continue
        names = {str(manifest.get("name") or "")}
        names.update(str(a) for a in (manifest.get("aliases") or []) if a)
        if server_name in names:
            return path
    return None


# Backward-compatible aliases (tests / legacy imports).
load_org_mcp_config = load_platform_mcp_config
org_mcp_allowed_tools = platform_mcp_allowed_tools
org_mcp_summary = platform_mcp_summary
