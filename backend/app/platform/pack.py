"""Parse standard skill ``pack.yaml`` (+ optional ``data_agent.overlay.yaml``)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from app.agent.extensions.manifest import SkillManifest
from app.store.schemas import SkillExtensions, SkillHarness, SubagentHint

logger = logging.getLogger(__name__)

# Built-in harness for contract-guided analysis when overlay is absent.
_CONTRACT_GUIDED_HARNESS = SkillHarness(
    phases=["research", "execute", "synthesize"],
    tool_budgets={
        "run_query_safely": 12,
        "execute_query_paginated": 12,
        "wkb_query": 8,
    },
    require_synthesis=True,
)

_RULE_CANDIDATES = (
    "references/vertica-rules.md",
    "references/analysis-clarification.md",
)

# MCP name aliases (pack.yaml name → runtime server name in platform MCP dir).
MCP_NAME_ALIASES: dict[str, str] = {
    "vertica-prod": "vertica-prod",
    "gateway-vertica-prod": "vertica-prod",
}


def expand_mcp_disable_names(disabled: set[str]) -> set[str]:
    """Treat alias names as the same server for disable checks."""
    expanded = set(disabled)
    for name in list(disabled):
        canonical = MCP_NAME_ALIASES.get(name, name)
        expanded.add(canonical)
        for alias, target in MCP_NAME_ALIASES.items():
            if target == canonical:
                expanded.add(alias)
    return expanded


def mcp_server_disabled(server: str, disabled: set[str]) -> bool:
    return server in expand_mcp_disable_names(disabled)


def skill_root_from_skill_md(skill_md: Path) -> Path:
    return skill_md.parent.resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        logger.warning("Failed to parse YAML: %s", path, exc_info=True)
        return {}
    return data if isinstance(data, dict) else {}


def _overlay_harness(overlay: dict[str, Any]) -> SkillHarness | None:
    raw = overlay.get("harness")
    if not isinstance(raw, dict):
        return None
    hints: list[SubagentHint] = []
    for item in raw.get("subagent_hints") or []:
        if isinstance(item, dict) and item.get("id"):
            hints.append(
                SubagentHint(
                    id=str(item["id"]),
                    label=str(item.get("label") or item["id"]),
                )
            )
    return SkillHarness(
        phases=list(raw.get("phases") or []),
        tool_budgets=dict(raw.get("tool_budgets") or {}),
        require_synthesis=bool(raw.get("require_synthesis")),
        subagent_hints=hints,
    )


def _extensions_from_pack(pack: dict[str, Any], skill_root: Path, source: str) -> SkillExtensions:
    ext = SkillExtensions()
    requires = pack.get("requires") or {}
    if isinstance(requires, dict):
        for entry in requires.get("mcp_servers") or []:
            if isinstance(entry, dict) and entry.get("name"):
                name = str(entry["name"])
                ext.mcp.append(MCP_NAME_ALIASES.get(name, name))
    scripts = pack.get("scripts") or {}
    if isinstance(scripts, dict) and scripts.get("wkb_query"):
        ext.tools.append("wkb_query")
    skill_name = skill_root.name
    prefix = f"/skills/{source}/{skill_name}"
    for rel in _RULE_CANDIDATES:
        if (skill_root / rel).exists():
            ext.rules.append(f"{prefix}/{rel}")
    return ext


def merge_pack_into_manifest(
    manifest: SkillManifest,
    skill_md: Path,
    *,
    source: str,
) -> SkillManifest:
    """Merge ``pack.yaml`` and optional overlay into a skill manifest."""
    skill_root = skill_root_from_skill_md(skill_md)
    pack = _load_yaml(skill_root / "pack.yaml")
    overlay = _load_yaml(skill_root / "data_agent.overlay.yaml")

    if not pack and not overlay:
        return manifest

    pack_ext = _extensions_from_pack(pack, skill_root, source) if pack else SkillExtensions()

    merged_tools = list(dict.fromkeys([*manifest.extensions.tools, *pack_ext.tools]))
    merged_mcp = list(dict.fromkeys([*manifest.extensions.mcp, *pack_ext.mcp]))
    merged_rules = list(dict.fromkeys([*manifest.extensions.rules, *pack_ext.rules]))

    harness = manifest.harness
    overlay_harness = _overlay_harness(overlay) if overlay else None
    if overlay_harness and (
        overlay_harness.phases
        or overlay_harness.tool_budgets
        or overlay_harness.require_synthesis
    ):
        harness = overlay_harness
    elif pack and pack_ext.tools and "wkb_query" in pack_ext.tools and not harness.tool_budgets:
        harness = _CONTRACT_GUIDED_HARNESS

    return SkillManifest(
        name=manifest.name or str(pack.get("name") or skill_root.name),
        description=manifest.description or str(pack.get("description") or ""),
        extensions=SkillExtensions(
            rules=merged_rules,
            tools=merged_tools,
            mcp=merged_mcp,
            subagents=list(manifest.extensions.subagents),
        ),
        harness=harness,
        raw={**manifest.raw, "pack": pack, "overlay": overlay},
    )


def find_wkb_skill_roots(user_id: str, *, active_names: list[str] | None = None) -> list[Path]:
    """Return skill roots that declare ``scripts.wkb_query`` in pack.yaml."""
    from app.store.paths import PLATFORM_SKILLS_DIR, skills_dir

    roots: list[Path] = []
    restrict = set(active_names) if active_names else None

    def _scan(base: Path) -> None:
        if not base.exists():
            return
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            if restrict is not None and child.name not in restrict:
                continue
            pack = _load_yaml(child / "pack.yaml")
            scripts = pack.get("scripts") or {}
            if isinstance(scripts, dict) and scripts.get("wkb_query"):
                roots.append(child.resolve())

    _scan(PLATFORM_SKILLS_DIR)
    _scan(skills_dir(user_id))
    return roots
