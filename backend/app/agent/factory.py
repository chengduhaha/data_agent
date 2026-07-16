"""Assemble a per-user deep agent via create_deep_agent."""

from __future__ import annotations

import logging
import os
from typing import Any

from deepagents import FilesystemPermission, create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, LocalShellBackend, StateBackend
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.agent.builtin_tools import get_builtin_tools
from app.agent.harness.config import load_harness_config
from app.agent.harness.middleware import ToolGovernanceMiddleware
from app.agent.harness.profiles import register_data_agent_harness_profiles
from app.agent.harness.prompts import HARNESS_SYSTEM_SUFFIX
from app.agent.harness.spill import LargeResultSpillMiddleware
from app.agent.harness.step_budget import StepBudgetMiddleware
from app.agent.harness.summarization import make_summarization_middleware
from app.agent.harness.tools import make_search_knowledge_tool, make_wkb_query_tool
from app.agent.mcp_manager import mcp_manager
from app.agent.models import build_model
from app.store.io import load_subagents_config, load_user_config
from app.store.paths import (
    BUILTIN_SKILLS_DIR,
    ORG_FRAGMENTS_DIR,
    ORG_KNOWLEDGE_DIR,
    ORG_SKILLS_DIR,
    ensure_user_layout,
    files_dir,
    org_rule_fragment_paths,
    rules_dir,
    skills_dir,
    threads_db_path,
)
from app.store.schemas import SubAgentSpec, UserConfig

logger = logging.getLogger(__name__)

_checkpointers: dict[str, AsyncSqliteSaver] = {}
_checkpointer_cms: dict[str, Any] = {}


async def get_checkpointer(user_id: str) -> AsyncSqliteSaver:
    ensure_user_layout(user_id)
    if user_id in _checkpointers:
        return _checkpointers[user_id]
    db = str(threads_db_path(user_id))
    cm = AsyncSqliteSaver.from_conn_string(db)
    saver = await cm.__aenter__()
    _checkpointers[user_id] = saver
    _checkpointer_cms[user_id] = cm
    return saver


async def close_checkpointers() -> None:
    for user_id, cm in list(_checkpointer_cms.items()):
        try:
            await cm.__aexit__(None, None, None)
        except Exception:
            logger.debug("checkpointer close failed for %s", user_id, exc_info=True)
    _checkpointers.clear()
    _checkpointer_cms.clear()


def build_backend(user_id: str) -> CompositeBackend:
    """Composite filesystem: personal workspace + shared org resources."""
    ensure_user_layout(user_id)
    harness_cfg = load_harness_config()
    workspace = LocalShellBackend(
        root_dir=str(files_dir(user_id)),
        virtual_mode=True,
        inherit_env=True,
        env={"DATA_AGENT_ORG_KNOWLEDGE": str(ORG_KNOWLEDGE_DIR.resolve())},
        timeout=harness_cfg.shell_timeout,
    )
    routes: dict[str, FilesystemBackend] = {
        "/workspace/": FilesystemBackend(
            root_dir=str(files_dir(user_id)),
            virtual_mode=True,
        ),
        "/skills/builtin/": FilesystemBackend(
            root_dir=str(BUILTIN_SKILLS_DIR),
            virtual_mode=True,
        ),
        "/skills/user/": FilesystemBackend(
            root_dir=str(skills_dir(user_id)),
            virtual_mode=True,
        ),
        "/rules/": FilesystemBackend(
            root_dir=str(rules_dir(user_id)),
            virtual_mode=True,
        ),
    }
    if ORG_SKILLS_DIR.exists():
        routes["/skills/org/"] = FilesystemBackend(
            root_dir=str(ORG_SKILLS_DIR),
            virtual_mode=True,
        )
    if ORG_KNOWLEDGE_DIR.exists():
        routes["/knowledge/org/"] = FilesystemBackend(
            root_dir=str(ORG_KNOWLEDGE_DIR),
            virtual_mode=True,
        )
    if ORG_FRAGMENTS_DIR.exists():
        routes["/rules/org/"] = FilesystemBackend(
            root_dir=str(ORG_FRAGMENTS_DIR),
            virtual_mode=True,
        )
    return CompositeBackend(default=workspace, routes=routes)


def _load_permissions(cfg: UserConfig) -> list[FilesystemPermission] | None:
    if not cfg.permissions:
        return None
    rules: list[FilesystemPermission] = []
    for p in cfg.permissions:
        rules.append(
            FilesystemPermission(
                operations=list(p.operations),
                paths=list(p.paths),
                mode=p.mode,
            )
        )
    return rules


def _to_subagent_dicts(specs: list[SubAgentSpec]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for s in specs:
        item: dict[str, Any] = {
            "name": s.name,
            "description": s.description,
            "system_prompt": s.system_prompt,
        }
        if s.model:
            item["model"] = s.model
        if s.skills:
            item["skills"] = s.skills
        out.append(item)
    return out


def _ensure_model_profile(model: Any) -> None:
    """Give summarization middleware a token budget when the provider omits profile."""
    default_max = int(os.getenv("DATA_AGENT_MAX_INPUT_TOKENS", "128000"))
    profile = getattr(model, "profile", None)
    if profile is None:
        try:
            model.profile = {"max_input_tokens": default_max}
        except Exception:
            pass
        return
    if isinstance(profile, dict) and "max_input_tokens" not in profile:
        profile["max_input_tokens"] = default_max


def render_system_prompt(cfg: UserConfig) -> str:
    base = (cfg.system_prompt or "").strip()
    suffix = (
        "\n\n## Path conventions\n"
        "- Personal workspace files: `/workspace/`\n"
        "- Built-in skills: `/skills/builtin/`\n"
        "- Organization skills (shared): `/skills/org/`\n"
        "- Personal skills: `/skills/user/`\n"
        "- Organization knowledge (shared): `/knowledge/org/` "
        "(read_file / ls / grep / search_knowledge)\n"
        "- Organization rules (shared): `/rules/org/`\n"
        "- Personal rules memory: `/rules/AGENTS.md`\n"
        "- Shell note: `execute` cannot see `/knowledge/org/` virtual paths; "
        "use `wkb_query` or `$DATA_AGENT_ORG_KNOWLEDGE` for WKB indexing.\n"
        "Prefer `/workspace/` for durable personal artifacts.\n\n"
        + HARNESS_SYSTEM_SUFFIX
    )
    return (base + suffix).strip()


def build_memory_paths() -> list[str]:
    """Org rule fragments (read-only) + personal AGENTS.md."""
    memory: list[str] = []
    for fragment in org_rule_fragment_paths():
        memory.append(f"/rules/org/{fragment.name}")
    memory.append("/rules/AGENTS.md")
    return memory


def build_skill_paths() -> list[str]:
    """builtin → org → user (last wins on name collision)."""
    paths = ["/skills/builtin/"]
    if ORG_SKILLS_DIR.exists():
        paths.append("/skills/org/")
    paths.append("/skills/user/")
    return paths


async def create_user_agent(
    user_id: str,
    cfg: UserConfig | None = None,
    *,
    extended_run: bool = False,
) -> Any:
    """Create a compiled deep agent graph for this user."""
    register_data_agent_harness_profiles()
    ensure_user_layout(user_id)
    cfg = cfg or await load_user_config(user_id)
    harness_cfg = load_harness_config(extended_run=extended_run)
    model = build_model(cfg)
    _ensure_model_profile(model)

    mcp_tools = await mcp_manager.get_tools(user_id)
    backend = build_backend(user_id)
    builtin = get_builtin_tools(
        cfg.enabled_tools,
        backend=backend,
        include_harness_tools=True,
    )
    tools = [*builtin, make_wkb_query_tool(), *mcp_tools]

    sub_cfg = await load_subagents_config(user_id)
    subagents = _to_subagent_dicts(sub_cfg.subagents) or None

    interrupt_on: dict[str, bool] = {}
    if cfg.approve_execute:
        interrupt_on["execute"] = True
    if cfg.approve_writes:
        interrupt_on["write_file"] = True
        interrupt_on["edit_file"] = True

    checkpointer = await get_checkpointer(user_id)

    harness_middleware = [
        ToolGovernanceMiddleware(harness_cfg),
        LargeResultSpillMiddleware(harness_cfg),
        StepBudgetMiddleware(harness_cfg),
        make_summarization_middleware(model, backend, harness_cfg),
    ]

    agent = create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=render_system_prompt(cfg),
        subagents=subagents,
        skills=build_skill_paths(),
        memory=build_memory_paths(),
        backend=backend,
        permissions=_load_permissions(cfg),
        interrupt_on=interrupt_on or None,
        checkpointer=checkpointer,
        middleware=harness_middleware,
        name=f"data-agent-{user_id}",
    )
    return agent


_ = StateBackend

__all__ = [
    "build_backend",
    "build_memory_paths",
    "build_skill_paths",
    "close_checkpointers",
    "create_user_agent",
    "get_checkpointer",
    "render_system_prompt",
]
