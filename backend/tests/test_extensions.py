"""Extension registry: skill frontmatter parsing + capability resolution."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from app.agent.extensions.manifest import parse_skill_manifest
from app.agent.extensions.registry import CapabilityRegistry
from app.store import paths
from app.store.io import load_user_config
from app.store.schemas import UserConfig


def test_parse_manifest_legacy_frontmatter_has_no_extensions() -> None:
    content = "---\nname: plain-skill\ndescription: just docs\n---\n\nBody text.\n"
    manifest = parse_skill_manifest(content)
    assert manifest.name == "plain-skill"
    assert manifest.description == "just docs"
    assert manifest.extensions.tools == []
    assert manifest.extensions.mcp == []
    assert manifest.harness.tool_budgets == {}
    assert manifest.harness.require_synthesis is False


def test_parse_manifest_extensions_and_harness() -> None:
    content = """---
name: contract-guided-data-analysis
description: test
extensions:
  rules:
    - /rules/org/AGENTS.contract-skill.md
  tools: [wkb_query]
  mcp: [gateway-vertica-prod]
harness:
  phases: [research, execute, synthesize]
  tool_budgets:
    run_query_safely: 12
    wkb_query: 8
  require_synthesis: true
---

Body.
"""
    manifest = parse_skill_manifest(content)
    assert manifest.extensions.tools == ["wkb_query"]
    assert manifest.extensions.mcp == ["gateway-vertica-prod"]
    assert manifest.extensions.rules == ["/rules/org/AGENTS.contract-skill.md"]
    assert manifest.harness.tool_budgets == {"run_query_safely": 12, "wkb_query": 8}
    assert manifest.harness.require_synthesis is True
    assert manifest.harness.phases == ["research", "execute", "synthesize"]


def test_parse_manifest_malformed_yaml_is_safe() -> None:
    content = "---\nname: [unterminated\n---\nBody\n"
    manifest = parse_skill_manifest(content)
    # Falls back to empty manifest rather than raising.
    assert manifest.name == ""


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)
    return ws


def test_registry_resolves_org_pack_capabilities_by_default(workspace_tmp: Path) -> None:
    async def run() -> None:
        cfg = await load_user_config("local")
        registry = CapabilityRegistry()
        resolved = await registry.resolve("local", cfg)
        assert "wkb_query" in resolved.extra_tool_names
        assert "gateway-vertica-prod" in resolved.extra_mcp_servers
        assert resolved.harness.tool_budgets.get("run_query_safely") == 12
        assert resolved.harness.require_synthesis is True

    asyncio.run(run())


def test_registry_respects_disabled_skills(workspace_tmp: Path) -> None:
    async def run() -> None:
        cfg = UserConfig(disabled_skills=["contract-guided-data-analysis"])
        registry = CapabilityRegistry()
        resolved = await registry.resolve("local", cfg)
        assert "wkb_query" not in resolved.extra_tool_names
        assert "gateway-vertica-prod" not in resolved.extra_mcp_servers

    asyncio.run(run())


def test_registry_respects_disabled_mcp_servers(workspace_tmp: Path) -> None:
    async def run() -> None:
        cfg = UserConfig(disabled_mcp_servers=["gateway-vertica-prod"])
        registry = CapabilityRegistry()
        resolved = await registry.resolve("local", cfg)
        # Skill's tool is still requested (wkb_query has no MCP dependency),
        # but the MCP server itself is excluded.
        assert "gateway-vertica-prod" not in resolved.extra_mcp_servers

    asyncio.run(run())


def test_registry_zero_org_bundle_has_no_capabilities(
    workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import app.store.io as io_mod

    monkeypatch.setattr(io_mod, "ORG_SKILLS_DIR", workspace_tmp / "_missing_org_skills")

    async def run() -> None:
        cfg = await load_user_config("local")
        registry = CapabilityRegistry()
        resolved = await registry.resolve("local", cfg)
        assert resolved.extra_tool_names == set()
        assert resolved.extra_mcp_servers == set()

    asyncio.run(run())
