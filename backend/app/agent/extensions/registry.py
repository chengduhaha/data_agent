"""CapabilityRegistry: resolves which tools/MCP/rules/harness apply to a run.

Agent Core (factory.py) calls `CapabilityRegistry.resolve(...)` instead of
hardcoding org-specific tools (e.g. `wkb_query`) or MCP servers. Everything
extra comes from skill frontmatter (see `manifest.py`) filtered by the user's
`disabled_skills` / `disabled_mcp_servers`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.agent.extensions.manifest import SkillManifest, parse_skill_manifest
from app.agent.extensions.default_skills import is_default_builtin_skill
from app.agent.extensions.subagent_routing import (
    SubagentRoutingPlan,
    manifests_by_name,
    resolve_subagent_routing,
)
from app.store.io import load_subagents_config
from app.store.schemas import SkillHarness, UserConfig


@dataclass
class ResolvedCapabilities:
    extra_tool_names: set[str] = field(default_factory=set)
    extra_mcp_servers: set[str] = field(default_factory=set)
    rule_fragments: list[str] = field(default_factory=list)
    subagent_names: list[str] = field(default_factory=list)
    harness: SkillHarness = field(default_factory=SkillHarness)
    active_skill_manifests: list[SkillManifest] = field(default_factory=list)
    subagent_routing: SubagentRoutingPlan = field(default_factory=SubagentRoutingPlan)


class CapabilityRegistry:
    """Aggregates skill manifests into `ResolvedCapabilities` for agent assembly."""

    def __init__(self) -> None:
        self._manifest_cache: dict[str, SkillManifest] = {}

    def _load_manifest(self, path: str) -> SkillManifest | None:
        from pathlib import Path

        p = Path(path)
        if not p.exists():
            return None
        cache_key = f"{p}:{p.stat().st_mtime_ns}"
        cached = self._manifest_cache.get(cache_key)
        if cached is not None:
            return cached
        try:
            content = p.read_text(encoding="utf-8")
        except OSError:
            return None
        manifest = parse_skill_manifest(content)
        from app.platform.pack import merge_pack_into_manifest

        source = "org"
        if "/skills_builtin/" in str(p) or "/skills/builtin/" in str(p):
            source = "builtin"
        elif "/skills/user/" in str(p) or "/users/" in str(p):
            source = "user"
        manifest = merge_pack_into_manifest(manifest, p, source=source)
        self._manifest_cache[cache_key] = manifest
        return manifest

    async def resolve(
        self,
        user_id: str,
        cfg: UserConfig,
        *,
        active_skills: list[str] | None = None,
    ) -> ResolvedCapabilities:
        """Resolve extra tools/MCP/rules/harness from enabled skill manifests.

        `active_skills`, when provided, restricts resolution to those names
        only (finer-grained gating for a future per-turn skill activation).
        By default every non-disabled skill that declares `extensions.tools`
        or `extensions.mcp` contributes its capabilities — this is what makes
        e.g. `wkb_query` appear only when the contract-guided-data-analysis
        skill (or an equivalent) is present and enabled.
        """
        from app.store.io import list_skills

        disabled_skills = set(cfg.disabled_skills or [])
        disabled_skills -= {n for n in disabled_skills if is_default_builtin_skill(n)}
        disabled_mcp = set(cfg.disabled_mcp_servers or [])
        restrict_to = set(active_skills) if active_skills else None

        out = ResolvedCapabilities()
        all_skills = await list_skills(user_id)
        for info in all_skills:
            if info.name in disabled_skills:
                continue
            if restrict_to is not None and info.name not in restrict_to:
                continue
            manifest = self._load_manifest(info.path)
            if manifest is None:
                continue
            if not (manifest.extensions.tools or manifest.extensions.mcp):
                continue
            out.active_skill_manifests.append(manifest)
            for tool in manifest.extensions.tools:
                out.extra_tool_names.add(tool)
            for server in manifest.extensions.mcp:
                if server not in disabled_mcp:
                    out.extra_mcp_servers.add(server)
            for rule in manifest.extensions.rules:
                if rule not in out.rule_fragments:
                    out.rule_fragments.append(rule)
            out.subagent_names.extend(manifest.extensions.subagents)
            if manifest.harness.tool_budgets:
                out.harness.tool_budgets.update(manifest.harness.tool_budgets)
            if manifest.harness.phases:
                out.harness.phases = manifest.harness.phases
            if manifest.harness.require_synthesis:
                out.harness.require_synthesis = True
            if manifest.harness.evidence_tools:
                existing = list(out.harness.evidence_tools)
                for name in manifest.harness.evidence_tools:
                    if name not in existing:
                        existing.append(name)
                out.harness.evidence_tools = existing
            if manifest.harness.synthesis_guidance:
                out.harness.synthesis_guidance = manifest.harness.synthesis_guidance

        if active_skills:
            sub_cfg = await load_subagents_config(user_id)
            out.subagent_routing = resolve_subagent_routing(
                active_skill_names=active_skills,
                manifests_by_name=manifests_by_name(out.active_skill_manifests),
                user_subagents=sub_cfg.subagents,
            )

        return out


capability_registry = CapabilityRegistry()

__all__ = ["CapabilityRegistry", "ResolvedCapabilities", "capability_registry"]
