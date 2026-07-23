"""Extension registry: turns skill frontmatter + org pack manifest into runtime capabilities.

Agent Core stays domain-agnostic; anything a skill needs beyond builtin tools
(extra tools, MCP servers, rule fragments, harness budgets) is declared in the
skill's SKILL.md frontmatter and resolved here at agent-build time.
"""

from app.agent.extensions.subagent_routing import (
    SubagentRoutingPlan,
    detect_active_skills_from_message,
    format_subagent_routing_prompt,
    load_pack_subagent_routing,
    resolve_subagent_routing,
)

from app.agent.extensions.manifest import (
    SkillManifest,
    parse_skill_frontmatter,
    parse_skill_manifest,
)
from app.agent.extensions.registry import CapabilityRegistry, ResolvedCapabilities

__all__ = [
    "CapabilityRegistry",
    "ResolvedCapabilities",
    "SkillManifest",
    "SubagentRoutingPlan",
    "detect_active_skills_from_message",
    "format_subagent_routing_prompt",
    "load_pack_subagent_routing",
    "parse_skill_frontmatter",
    "parse_skill_manifest",
    "resolve_subagent_routing",
]
