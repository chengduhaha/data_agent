"""Unit tests for pack-driven multi-perspective subagent routing."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from app.agent.extensions.manifest import parse_skill_manifest
from app.agent.extensions.registry import CapabilityRegistry
from app.agent.extensions.subagent_routing import (
    detect_active_skills_from_message,
    filter_subagents_for_routing,
    format_subagent_routing_prompt,
    load_pack_subagent_routing,
    manifests_by_name,
    resolve_subagent_routing,
)
from app.store import paths
from app.store.schemas import SubAgentSpec, SubAgentsConfig, UserConfig


CONTRACT_SKILL = """---
name: contract-guided-data-analysis
description: test
extensions:
  tools: [wkb_query]
  mcp: [gateway-vertica-prod]
harness:
  subagent_hints:
    - id: customer
      label: Customer mix / ranking angle
    - id: vendor
      label: Vendor rate / mix angle
---
Body.
"""


def test_detect_active_skills_from_expanded_message() -> None:
    msg = (
        'Use skill "contract-guided-data-analysis". Read and follow '
        "`/skills/org/contract-guided-data-analysis/SKILL.md` before answering.\n\n"
        "User request:\nTop customers"
    )
    assert detect_active_skills_from_message(msg) == ["contract-guided-data-analysis"]


def test_detect_active_skills_from_slash_prefix() -> None:
    assert detect_active_skills_from_message("/contract-guided-data-analysis revenue") == [
        "contract-guided-data-analysis"
    ]


def test_load_pack_subagent_routing_reads_b_report_manifest() -> None:
    routing = load_pack_subagent_routing()
    assert "contract-guided-data-analysis" in routing
    assert routing["contract-guided-data-analysis"][:3] == ["customer", "vendor", "order"]


def test_resolve_subagent_routing_marks_configured_subagents() -> None:
    manifest = parse_skill_manifest(CONTRACT_SKILL)
    plan = resolve_subagent_routing(
        active_skill_names=["contract-guided-data-analysis"],
        manifests_by_name={"contract-guided-data-analysis": manifest},
        user_subagents=[
            SubAgentSpec(
                name="customer",
                description="Customer ranking specialist",
                system_prompt="Focus on customer mix.",
            )
        ],
        pack_routing={"contract-guided-data-analysis": ["customer", "vendor"]},
    )
    assert plan.skill_names == ["contract-guided-data-analysis"]
    assert [r.id for r in plan.routes] == ["customer", "vendor"]
    assert plan.routes[0].configured is True
    assert plan.routes[0].label == "Customer mix / ranking angle"
    assert plan.routes[1].configured is False


def test_filter_subagents_for_routing_limits_task_targets() -> None:
    manifest = parse_skill_manifest(CONTRACT_SKILL)
    plan = resolve_subagent_routing(
        active_skill_names=["contract-guided-data-analysis"],
        manifests_by_name={"contract-guided-data-analysis": manifest},
        user_subagents=[
            SubAgentSpec(name="customer", description="", system_prompt="c"),
            SubAgentSpec(name="misc", description="", system_prompt="m"),
        ],
        pack_routing={"contract-guided-data-analysis": ["customer"]},
    )
    filtered = filter_subagents_for_routing(
        [
            SubAgentSpec(name="customer", description="", system_prompt="c"),
            SubAgentSpec(name="misc", description="", system_prompt="m"),
        ],
        plan,
    )
    assert [s.name for s in filtered] == ["customer"]


def test_format_subagent_routing_prompt_lists_perspectives() -> None:
    manifest = parse_skill_manifest(CONTRACT_SKILL)
    plan = resolve_subagent_routing(
        active_skill_names=["contract-guided-data-analysis"],
        manifests_by_name=manifests_by_name([manifest]),
        user_subagents=[],
        pack_routing={"contract-guided-data-analysis": ["customer"]},
    )
    prompt = format_subagent_routing_prompt(plan)
    assert "Multi-perspective subagents" in prompt
    assert "customer" in prompt
    assert "Customer mix / ranking angle" in prompt


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)
    return ws


def test_registry_resolves_routing_when_skill_active(workspace_tmp: Path) -> None:
    async def run() -> None:
        cfg = UserConfig()
        registry = CapabilityRegistry()
        resolved = await registry.resolve(
            "local",
            cfg,
            active_skills=["contract-guided-data-analysis"],
        )
        routes = resolved.subagent_routing.routes
        assert resolved.subagent_routing.skill_names == ["contract-guided-data-analysis"]
        assert {r.id for r in routes} >= {"customer", "vendor", "order"}

    asyncio.run(run())


def test_registry_skips_routing_without_active_skill(workspace_tmp: Path) -> None:
    async def run() -> None:
        cfg = UserConfig()
        registry = CapabilityRegistry()
        resolved = await registry.resolve("local", cfg)
        assert resolved.subagent_routing.routes == []

    asyncio.run(run())
