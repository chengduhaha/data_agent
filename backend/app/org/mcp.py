"""Organization MCP servers loaded from the org pack's `extensions/*.yaml` manifests.

Core makes no assumption about Vertica or any other specific provider — each
YAML file under `<org bundle>/extensions/` declares one MCP server template
with `${ENV_VAR}` / `${ENV_VAR:default}` placeholders. A server is only
activated when all of its `required_env` variables are set (secrets stay in
process env / `.env.secrets`, never persisted per user).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from app.store.paths import ORG_EXTENSIONS_DIR
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
    if not ORG_EXTENSIONS_DIR.exists():
        return []
    return sorted(ORG_EXTENSIONS_DIR.glob("*.yaml")) + sorted(ORG_EXTENSIONS_DIR.glob("*.yml"))


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


def load_org_mcp_config(env: dict[str, str] | None = None) -> McpConfig:
    """Build org MCP config from the org pack's extension manifests + process env."""
    import os

    env = env if env is not None else dict(os.environ)
    servers: dict[str, McpServerConfig] = {}
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            logger.warning("Failed to parse org MCP manifest: %s", path, exc_info=True)
            continue
        if not isinstance(manifest, dict):
            continue
        entry = _server_from_manifest(manifest, env)
        if entry:
            servers[entry[0]] = entry[1]
    return McpConfig(mcpServers=servers)


def org_mcp_allowed_tools(server_name: str) -> frozenset[str] | None:
    """Metadata-tool allowlist declared by a manifest (e.g. hide Vertica discovery tools)."""
    for path in _load_manifest_files():
        try:
            manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if isinstance(manifest, dict) and manifest.get("name") == server_name:
            allowed = manifest.get("allowed_tools")
            if allowed:
                return frozenset(str(t) for t in allowed)
            return None
    return None


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
