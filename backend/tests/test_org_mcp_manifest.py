"""Generalized org MCP manifest loader (Phase 3: pack manifest, not Vertica-specific)."""

from __future__ import annotations

from app.org.mcp import load_org_mcp_config, org_mcp_allowed_tools


def test_vertica_manifest_activates_when_env_present(monkeypatch) -> None:
    env = {
        "VERTICA_API_KEY": "k",
        "VERTICA_HOST": "h",
        "VERTICA_DATABASE": "d",
        "VERTICA_USER": "u",
        "VERTICA_PASSWORD": "p",
    }
    cfg = load_org_mcp_config(env)
    assert "gateway-vertica-prod" in cfg.mcpServers
    server = cfg.mcpServers["gateway-vertica-prod"]
    assert server.headers["x-api-key"] == "k"
    assert server.headers["X-Vertica-Port"] == "5433"  # default placeholder


def test_manifest_inactive_without_required_env() -> None:
    cfg = load_org_mcp_config({})
    assert "gateway-vertica-prod" not in cfg.mcpServers


def test_org_mcp_allowed_tools_from_manifest() -> None:
    allowed = org_mcp_allowed_tools("gateway-vertica-prod")
    assert allowed == frozenset({"run_query_safely", "execute_query_paginated"})


def test_org_mcp_allowed_tools_missing_manifest_returns_none() -> None:
    assert org_mcp_allowed_tools("does-not-exist") is None
