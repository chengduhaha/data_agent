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
from app.store import paths as store_paths
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
    if ORG_BUNDLE_DIR is None:
        return {}
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
    """Legacy (name, description) shape — use `_skill_info_from_content` for extensions."""
    from app.agent.extensions.manifest import parse_skill_frontmatter

    return parse_skill_frontmatter(content)


def _skill_info_from_content(
    content: str,
    *,
    fallback_name: str,
    source: str,
    path: Path,
    with_content: bool,
    disabled_skills: set[str] | None = None,
) -> SkillInfo:
    from app.agent.extensions.manifest import parse_skill_manifest

    manifest = parse_skill_manifest(content)
    name = manifest.name or fallback_name
    return SkillInfo(
        name=name,
        description=manifest.description,
        source=source,  # type: ignore[arg-type]
        path=str(path),
        content=content if with_content else None,
        editable=source == "user",
        disabled=name in (disabled_skills or set()),
        extensions=manifest.extensions,
        harness=manifest.harness,
    )


def _list_skills_in_dir(
    root: Path, source: str, *, disabled_skills: set[str] | None = None
) -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    if not root.exists():
        return skills
    for child in sorted(root.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            skills.append(
                _skill_info_from_content(
                    content,
                    fallback_name=child.name,
                    source=source,
                    path=skill_md,
                    with_content=False,
                    disabled_skills=disabled_skills,
                )
            )
    return skills


async def list_skills(user_id: str, cfg: UserConfig | None = None) -> list[SkillInfo]:
    ensure_user_layout(user_id)
    disabled = set(cfg.disabled_skills) if cfg else None
    builtin = _list_skills_in_dir(store_paths.BUILTIN_SKILLS_DIR, "builtin", disabled_skills=disabled)
    # Org bundle is the live shared mount; platform catalog fills gaps / registry archive.
    org = _list_skills_in_dir(store_paths.ORG_SKILLS_DIR, "org", disabled_skills=disabled)
    org_names = {s.name for s in org}
    platform = [
        s
        for s in _list_skills_in_dir(store_paths.PLATFORM_SKILLS_DIR, "org", disabled_skills=disabled)
        if s.name not in org_names
    ]
    user = _list_skills_in_dir(skills_dir(user_id), "user", disabled_skills=disabled)
    return builtin + org + platform + user


async def get_skill(user_id: str, name: str, source: str = "user") -> SkillInfo | None:
    ensure_user_layout(user_id)
    if source == "builtin":
        roots = [store_paths.BUILTIN_SKILLS_DIR]
    elif source == "org":
        roots = [store_paths.ORG_SKILLS_DIR, store_paths.PLATFORM_SKILLS_DIR]
    else:
        roots = [skills_dir(user_id)]
    for root in roots:
        skill_md = root / name / "SKILL.md"
        if not skill_md.exists():
            for info in _list_skills_in_dir(root, source):
                if info.name == name:
                    skill_md = Path(info.path)
                    break
            else:
                continue
        content = skill_md.read_text(encoding="utf-8")
        cfg = await load_user_config(user_id)
        return _skill_info_from_content(
            content,
            fallback_name=name,
            source=source,
            path=skill_md,
            with_content=True,
            disabled_skills=set(cfg.disabled_skills),
        )
    return None


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


async def install_user_skill_from_zip(user_id: str, data: bytes) -> SkillInfo:
    """Extract a skill.zip into the user's personal skills directory (overwrite same name)."""
    from app.platform.skills_zip import extract_skill_zip

    ensure_user_layout(user_id)
    skill_dir, skill_name = extract_skill_zip(data, skills_dir(user_id))
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md missing after unzip for {skill_name}")
    content = skill_md.read_text(encoding="utf-8")
    return _skill_info_from_content(
        content,
        fallback_name=skill_name,
        source="user",
        path=skill_md,
        with_content=True,
    )


def _skill_pack_version(skill_dir: Path) -> str:
    pack_path = skill_dir / "pack.yaml"
    if not pack_path.exists():
        return ""
    try:
        import yaml

        data = yaml.safe_load(pack_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return ""
    if isinstance(data, dict):
        return str(data.get("version") or "").strip()
    return ""


async def publish_user_skill_to_platform(user_id: str, name: str) -> dict[str, Any]:
    """Copy a personal skill into the platform shared catalog (overwrite same name).

    Writes ``backend/platform/skills/{name}`` and mirrors into the org skills dir so
    agents already mounting ``/skills/org/`` pick up the new version. Built-in
    platform skills under ``skills_builtin`` cannot be overwritten.
    """
    from app.platform.editors import is_platform_editor
    from app.platform.registry_store import record_skill_publish
    from app.platform.skills_zip import publish_skill_dir

    ensure_user_layout(user_id)
    if not is_platform_editor(user_id):
        raise PermissionError("Not allowed to publish platform skills")

    safe = "".join(c for c in name if c.isalnum() or c in "-_").strip("-_") or name
    src = skills_dir(user_id) / safe
    if not (src / "SKILL.md").exists():
        raise FileNotFoundError(f"Personal skill not found: {safe}")

    if (store_paths.BUILTIN_SKILLS_DIR / safe / "SKILL.md").exists():
        raise ValueError(f"Cannot overwrite built-in platform skill: {safe}")

    replaced_platform = (store_paths.PLATFORM_SKILLS_DIR / safe / "SKILL.md").exists()
    replaced_org = (store_paths.ORG_SKILLS_DIR / safe / "SKILL.md").exists()

    store_paths.PLATFORM_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    publish_skill_dir(src, store_paths.PLATFORM_SKILLS_DIR / safe)

    if store_paths.ORG_BUNDLE_DIR is not None:
        store_paths.ORG_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        publish_skill_dir(src, store_paths.ORG_SKILLS_DIR / safe)

    version = _skill_pack_version(src)
    record_skill_publish(safe, published_by=user_id, version=version)

    return {
        "ok": True,
        "name": safe,
        "version": version,
        "replaced": replaced_platform or replaced_org,
        "platform_path": str(store_paths.PLATFORM_SKILLS_DIR / safe),
        "org_path": str(store_paths.ORG_SKILLS_DIR / safe)
        if store_paths.ORG_BUNDLE_DIR is not None
        else None,
    }


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
