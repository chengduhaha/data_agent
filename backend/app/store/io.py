"""File I/O helpers for per-user config artifacts."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiofiles

from app.org.mcp import load_org_mcp_config
from app.store.paths import (
    BUILTIN_SKILLS_DIR,
    ORG_BUNDLE_DIR,
    ORG_SKILLS_DIR,
    config_path,
    ensure_user_layout,
    files_dir,
    mcp_path,
    rules_path,
    skills_dir,
    subagents_path,
    threads_meta_path,
)
from app.store.schemas import (
    McpConfig,
    SkillInfo,
    SubAgentsConfig,
    UserConfig,
)


async def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    async with aiofiles.open(path, encoding="utf-8") as f:
        raw = await f.read()
    if not raw.strip():
        return default
    return json.loads(raw)


async def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


async def load_user_config(user_id: str) -> UserConfig:
    ensure_user_layout(user_id)
    data = await _read_json(config_path(user_id), {})
    cfg = UserConfig.model_validate(data)
    return _apply_org_runtime_config(cfg)


def _load_org_config_patch() -> dict[str, Any]:
    patch_path = ORG_BUNDLE_DIR / "fragments" / "config.patch.json"
    if not patch_path.exists():
        return {}
    try:
        data = json.loads(patch_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _apply_org_runtime_config(cfg: UserConfig) -> UserConfig:
    """Org bundle policy (contract-guided analysis): full tool access, no HITL."""
    patch = _load_org_config_patch()
    if not patch:
        return cfg
    if "approve_writes" in patch:
        cfg.approve_writes = bool(patch["approve_writes"])
    if "approve_execute" in patch:
        cfg.approve_execute = bool(patch["approve_execute"])
    if "enabled_tools" in patch and isinstance(patch["enabled_tools"], dict):
        cfg.enabled_tools = {**cfg.enabled_tools, **patch["enabled_tools"]}
    if isinstance(patch.get("system_prompt"), str) and patch["system_prompt"].strip():
        cfg.system_prompt = patch["system_prompt"].strip()
    return cfg


async def save_user_config(user_id: str, cfg: UserConfig) -> UserConfig:
    ensure_user_layout(user_id)
    await _write_json(config_path(user_id), cfg.model_dump())
    return cfg


async def load_mcp_config(user_id: str) -> McpConfig:
    """Load user-owned MCP config only (org MCP is injected at runtime)."""
    ensure_user_layout(user_id)
    data = await _read_json(mcp_path(user_id), {"mcpServers": {}})
    return McpConfig.model_validate(data)


async def load_effective_mcp_config(user_id: str) -> McpConfig:
    """Merge organization MCP (server-side) with user MCP for agent runtime."""
    user_cfg = await load_mcp_config(user_id)
    org_cfg = load_org_mcp_config()
    merged_servers = {**org_cfg.mcpServers, **user_cfg.mcpServers}
    return McpConfig(mcpServers=merged_servers)


async def save_mcp_config(user_id: str, cfg: McpConfig) -> McpConfig:
    ensure_user_layout(user_id)
    await _write_json(mcp_path(user_id), cfg.model_dump())
    return cfg


async def load_subagents_config(user_id: str) -> SubAgentsConfig:
    ensure_user_layout(user_id)
    data = await _read_json(subagents_path(user_id), {"subagents": []})
    return SubAgentsConfig.model_validate(data)


async def save_subagents_config(user_id: str, cfg: SubAgentsConfig) -> SubAgentsConfig:
    ensure_user_layout(user_id)
    await _write_json(subagents_path(user_id), cfg.model_dump())
    return cfg


async def load_rules(user_id: str) -> str:
    ensure_user_layout(user_id)
    path = rules_path(user_id)
    async with aiofiles.open(path, encoding="utf-8") as f:
        return await f.read()


async def save_rules(user_id: str, content: str) -> str:
    ensure_user_layout(user_id)
    path = rules_path(user_id)
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(content)
    return content


def _parse_skill_frontmatter(content: str) -> tuple[str, str]:
    name = ""
    description = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                line = line.strip()
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip("\"'")
    return name, description


def _list_skills_in_dir(root: Path, source: str) -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    if not root.exists():
        return skills
    for child in sorted(root.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            name, description = _parse_skill_frontmatter(content)
            skills.append(
                SkillInfo(
                    name=name or child.name,
                    description=description,
                    source=source,  # type: ignore[arg-type]
                    path=str(skill_md),
                    content=None,
                    editable=source == "user",
                )
            )
    return skills


async def list_skills(user_id: str) -> list[SkillInfo]:
    ensure_user_layout(user_id)
    builtin = _list_skills_in_dir(BUILTIN_SKILLS_DIR, "builtin")
    org = _list_skills_in_dir(ORG_SKILLS_DIR, "org")
    user = _list_skills_in_dir(skills_dir(user_id), "user")
    return builtin + org + user


async def get_skill(user_id: str, name: str, source: str = "user") -> SkillInfo | None:
    ensure_user_layout(user_id)
    if source == "builtin":
        root = BUILTIN_SKILLS_DIR
    elif source == "org":
        root = ORG_SKILLS_DIR
    else:
        root = skills_dir(user_id)
    skill_md = root / name / "SKILL.md"
    if not skill_md.exists():
        for info in _list_skills_in_dir(root, source):
            if info.name == name:
                skill_md = Path(info.path)
                break
        else:
            return None
    content = skill_md.read_text(encoding="utf-8")
    parsed_name, description = _parse_skill_frontmatter(content)
    return SkillInfo(
        name=parsed_name or name,
        description=description,
        source=source,  # type: ignore[arg-type]
        path=str(skill_md),
        content=content,
        editable=source == "user",
    )


async def save_user_skill(user_id: str, name: str, content: str) -> SkillInfo:
    ensure_user_layout(user_id)
    safe = "".join(c for c in name if c.isalnum() or c in "-_").strip("-_") or "skill"
    skill_dir = skills_dir(user_id) / safe
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(content, encoding="utf-8")
    parsed_name, description = _parse_skill_frontmatter(content)
    return SkillInfo(
        name=parsed_name or safe,
        description=description,
        source="user",
        path=str(skill_md),
        content=content,
        editable=True,
    )


async def delete_user_skill(user_id: str, name: str) -> bool:
    ensure_user_layout(user_id)
    skill_dir = skills_dir(user_id) / name
    if not skill_dir.exists():
        return False
    shutil.rmtree(skill_dir)
    return True


def resolve_workspace_path(user_id: str, rel: str) -> Path:
    """Resolve a workspace-relative path safely under the user's files dir."""
    ensure_user_layout(user_id)
    root = files_dir(user_id).resolve()
    cleaned = rel.lstrip("/").replace("\\", "/")
    if cleaned.startswith("workspace/"):
        cleaned = cleaned[len("workspace/") :]
    target = (root / cleaned).resolve()
    if not str(target).startswith(str(root)):
        raise ValueError("Path escapes workspace")
    return target


async def load_threads_meta(user_id: str) -> dict[str, dict[str, Any]]:
    ensure_user_layout(user_id)
    data = await _read_json(threads_meta_path(user_id), {})
    if isinstance(data, dict):
        return data
    return {}


async def save_threads_meta(user_id: str, meta: dict[str, dict[str, Any]]) -> None:
    ensure_user_layout(user_id)
    await _write_json(threads_meta_path(user_id), meta)


def make_thread_title(message: str, *, max_len: int = 56) -> str:
    text = " ".join(message.strip().split())
    if not text:
        return "New chat"
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


async def upsert_thread_meta(
    user_id: str,
    thread_id: str,
    *,
    title: str | None = None,
    touch: bool = True,
    run_segment: int | None = None,
) -> dict[str, Any]:
    meta = await load_threads_meta(user_id)
    entry = dict(meta.get(thread_id) or {})
    if title and not entry.get("title"):
        entry["title"] = title
    if run_segment is not None:
        entry["run_segment"] = run_segment
    if touch:
        entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    if "created_at" not in entry:
        entry["created_at"] = entry.get("updated_at") or datetime.now(timezone.utc).isoformat()
    if "run_segment" not in entry:
        entry["run_segment"] = 1
    meta[thread_id] = entry
    await save_threads_meta(user_id, meta)
    return entry


async def increment_thread_run_segment(user_id: str, thread_id: str) -> int:
    meta = await load_threads_meta(user_id)
    entry = dict(meta.get(thread_id) or {})
    segment = int(entry.get("run_segment") or 1) + 1
    entry["run_segment"] = segment
    entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    if "created_at" not in entry:
        entry["created_at"] = entry["updated_at"]
    meta[thread_id] = entry
    await save_threads_meta(user_id, meta)
    return segment


async def increment_thread_turn_index(user_id: str, thread_id: str) -> int:
    meta = await load_threads_meta(user_id)
    entry = dict(meta.get(thread_id) or {})
    turn = int(entry.get("turn_index") or 0) + 1
    entry["turn_index"] = turn
    entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    if "created_at" not in entry:
        entry["created_at"] = entry["updated_at"]
    meta[thread_id] = entry
    await save_threads_meta(user_id, meta)
    return turn


async def append_turn_summary(
    user_id: str,
    thread_id: str,
    *,
    turn_index: int,
    summary: str,
) -> None:
    if not summary.strip():
        return
    meta = await load_threads_meta(user_id)
    entry = dict(meta.get(thread_id) or {})
    summaries = list(entry.get("turn_summaries") or [])
    summaries.append(
        {
            "turn_index": turn_index,
            "summary": summary.strip(),
        }
    )
    entry["turn_summaries"] = summaries[-20:]
    entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta[thread_id] = entry
    await save_threads_meta(user_id, meta)


async def get_thread_meta_entry(user_id: str, thread_id: str) -> dict[str, Any]:
    meta = await load_threads_meta(user_id)
    return dict(meta.get(thread_id) or {})


async def delete_thread_meta(user_id: str, thread_id: str) -> None:
    meta = await load_threads_meta(user_id)
    if thread_id in meta:
        del meta[thread_id]
        await save_threads_meta(user_id, meta)
