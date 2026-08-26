"""Parse SKILL.md YAML frontmatter into a typed manifest.

Backward compatible: a plain SKILL.md with only `name:` / `description:` parses
to a manifest with empty `extensions` / `harness` (a "pure documentation" skill).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml

from app.store.schemas import SkillExtensions, SkillHarness, SubagentHint


@dataclass
class SkillManifest:
    name: str = ""
    description: str = ""
    extensions: SkillExtensions = field(default_factory=SkillExtensions)
    harness: SkillHarness = field(default_factory=SkillHarness)
    raw: dict[str, Any] = field(default_factory=dict)


def _split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body). Empty dict if no/invalid frontmatter."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}, content
    if not isinstance(data, dict):
        return {}, content
    return data, parts[2]


def parse_skill_frontmatter(content: str) -> tuple[str, str]:
    """Legacy shape: (name, description) only — kept for callers that don't need extensions."""
    data, _ = _split_frontmatter(content)
    name = str(data.get("name") or "")
    description = str(data.get("description") or "")
    return name, description


def parse_skill_manifest(content: str) -> SkillManifest:
    data, _ = _split_frontmatter(content)
    name = str(data.get("name") or "")
    description = str(data.get("description") or "")

    ext_raw = data.get("extensions") or {}
    extensions = SkillExtensions(
        rules=list(ext_raw.get("rules") or []) if isinstance(ext_raw, dict) else [],
        tools=list(ext_raw.get("tools") or []) if isinstance(ext_raw, dict) else [],
        mcp=list(ext_raw.get("mcp") or []) if isinstance(ext_raw, dict) else [],
        subagents=list(ext_raw.get("subagents") or []) if isinstance(ext_raw, dict) else [],
    )

    harness_raw = data.get("harness") or {}
    subagent_hints: list[SubagentHint] = []
    if isinstance(harness_raw, dict):
        raw_hints = harness_raw.get("subagent_hints") or []
        if isinstance(raw_hints, list):
            for item in raw_hints:
                if isinstance(item, dict) and item.get("id"):
                    subagent_hints.append(
                        SubagentHint(
                            id=str(item["id"]),
                            label=str(item.get("label") or item["id"]),
                        )
                    )
    harness = SkillHarness(
        phases=list(harness_raw.get("phases") or []) if isinstance(harness_raw, dict) else [],
        tool_budgets=(
            dict(harness_raw.get("tool_budgets") or {}) if isinstance(harness_raw, dict) else {}
        ),
        require_synthesis=bool(harness_raw.get("require_synthesis"))
        if isinstance(harness_raw, dict)
        else False,
        subagent_hints=subagent_hints,
        evidence_tools=list(harness_raw.get("evidence_tools") or [])
        if isinstance(harness_raw, dict)
        else [],
        synthesis_guidance=str(harness_raw.get("synthesis_guidance") or "")
        if isinstance(harness_raw, dict)
        else "",
    )

    return SkillManifest(
        name=name,
        description=description,
        extensions=extensions,
        harness=harness,
        raw=data,
    )
