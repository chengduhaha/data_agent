"""Resolve multi-perspective subagent routing from pack manifest + skill hints.

Core stays skill-name-agnostic: routing IDs and labels come from the org pack's
`subagent_routing` map and each skill's `harness.subagent_hints` frontmatter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

import yaml

from app.agent.extensions.manifest import SkillManifest
from app.store.paths import ORG_PACK_MANIFEST_PATH
from app.store.schemas import SubAgentSpec

_SKILL_IN_MESSAGE_RE = re.compile(
    r'Use skill\s+"([\w-]+)"',
    re.IGNORECASE,
)
_SKILL_PATH_RE = re.compile(
    r"/skills/(?:builtin|org|user)/([\w-]+)/SKILL\.md",
    re.IGNORECASE,
)
_SLASH_SKILL_RE = re.compile(r"^/([\w-]+)(?:\s|$)", re.MULTILINE)


@dataclass
class ResolvedSubagentRoute:
    """One routable perspective for an active skill."""

    id: str
    label: str
    configured: bool
    description: str = ""


@dataclass
class SubagentRoutingPlan:
    """Routing resolution for one or more active skills."""

    skill_names: list[str] = field(default_factory=list)
    routes: list[ResolvedSubagentRoute] = field(default_factory=list)

    @property
    def configured_routes(self) -> list[ResolvedSubagentRoute]:
        return [r for r in self.routes if r.configured]


@lru_cache(maxsize=1)
def load_pack_subagent_routing() -> dict[str, list[str]]:
    """Skill name → ordered subagent IDs declared in the org pack manifest."""
    path = ORG_PACK_MANIFEST_PATH
    if path is None or not path.exists():
        return {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(raw, dict):
        return {}
    routing = raw.get("subagent_routing") or {}
    if not isinstance(routing, dict):
        return {}
    out: dict[str, list[str]] = {}
    for skill_name, ids in routing.items():
        if not isinstance(skill_name, str) or not isinstance(ids, list):
            continue
        clean = [str(i) for i in ids if i]
        if clean:
            out[skill_name] = clean
    return out


def detect_active_skills_from_message(message: str) -> list[str]:
    """Infer slash-expanded or explicit skill activation from the user turn."""
    text = (message or "").strip()
    if not text:
        return []
    found: list[str] = []
    for pattern in (_SKILL_IN_MESSAGE_RE, _SKILL_PATH_RE):
        for match in pattern.finditer(text):
            name = match.group(1)
            if name and name not in found:
                found.append(name)
    slash = _SLASH_SKILL_RE.match(text)
    if slash:
        name = slash.group(1)
        if name and name not in found:
            found.append(name)
    return found


def _hint_label(manifest: SkillManifest, route_id: str) -> str:
    for hint in manifest.harness.subagent_hints:
        if hint.id == route_id:
            return hint.label or route_id
    return route_id


def resolve_subagent_routing(
    *,
    active_skill_names: list[str],
    manifests_by_name: dict[str, SkillManifest],
    user_subagents: list[SubAgentSpec],
    pack_routing: dict[str, list[str]] | None = None,
) -> SubagentRoutingPlan:
    """Match pack routing + skill hints against the user's configured subagents."""
    pack = pack_routing if pack_routing is not None else load_pack_subagent_routing()
    if not active_skill_names or not pack:
        return SubagentRoutingPlan()

    by_name = {s.name: s for s in user_subagents}
    routes: list[ResolvedSubagentRoute] = []
    seen: set[str] = set()
    matched_skills: list[str] = []

    for skill_name in active_skill_names:
        route_ids = pack.get(skill_name)
        if not route_ids:
            continue
        manifest = manifests_by_name.get(skill_name)
        if manifest is None:
            continue
        matched_skills.append(skill_name)
        for route_id in route_ids:
            if route_id in seen:
                continue
            seen.add(route_id)
            spec = by_name.get(route_id)
            routes.append(
                ResolvedSubagentRoute(
                    id=route_id,
                    label=_hint_label(manifest, route_id),
                    configured=spec is not None,
                    description=(spec.description if spec else ""),
                )
            )

    return SubagentRoutingPlan(skill_names=matched_skills, routes=routes)


def filter_subagents_for_routing(
    user_subagents: list[SubAgentSpec],
    plan: SubagentRoutingPlan,
) -> list[SubAgentSpec]:
    """When routing is active, expose only configured subagents on the route list."""
    if not plan.routes:
        return user_subagents
    allowed = {r.id for r in plan.routes}
    filtered = [s for s in user_subagents if s.name in allowed]
    return filtered or user_subagents


def format_subagent_routing_prompt(plan: SubagentRoutingPlan) -> str:
    """System-prompt suffix suggesting `task` delegation for multi-perspective work."""
    if not plan.routes or not plan.skill_names:
        return ""
    skill_list = ", ".join(plan.skill_names)
    lines = [
        f"## Multi-perspective subagents ({skill_list})",
        "",
    ]
    if "contract-guided-data-analysis" in plan.skill_names:
        lines.extend([
            "Do **NOT** use the `task` tool for contract-guided data analysis. "
            "Run contract routing, `run_query_safely`, and synthesis in the main agent.",
            "",
        ])
    else:
        lines.extend([
            "When the user's question benefits from a focused slice (ranking, mix, drilldown), "
            "you MAY delegate that slice via the `task` tool to a configured subagent. "
            "Do not delegate the full skill workflow — keep contract routing and synthesis in the main agent.",
            "",
        ])
    lines.append("Available perspectives:")
    for route in plan.routes:
        status = "configured" if route.configured else "not configured (Settings → Subagents)"
        detail = f" — {route.description}" if route.description else ""
        lines.append(f"- **{route.id}** ({route.label}): {status}{detail}")
    configured = plan.configured_routes
    if configured:
        names = ", ".join(f"`{r.id}`" for r in configured)
        lines.append("")
        lines.append(
            f"Prefer parallel `task` calls to {names} only when their angle materially "
            "improves the answer; merge results in your final synthesis."
        )
    else:
        lines.append("")
        lines.append(
            "No matching subagents are configured yet — proceed in the main agent unless "
            "the user adds specialists under Settings → Subagents."
        )
    return "\n".join(lines).strip()


def manifests_by_name(manifests: list[SkillManifest]) -> dict[str, SkillManifest]:
    return {m.name: m for m in manifests if m.name}


__all__ = [
    "ResolvedSubagentRoute",
    "SubagentRoutingPlan",
    "detect_active_skills_from_message",
    "filter_subagents_for_routing",
    "format_subagent_routing_prompt",
    "load_pack_subagent_routing",
    "manifests_by_name",
    "resolve_subagent_routing",
]
