"""Path helpers for per-user workspace layout and shared org bundle."""

from __future__ import annotations

import os
from pathlib import Path

# backend/app/store/paths.py -> backend/
BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent
APP_ROOT = BACKEND_ROOT / "app"
WORKSPACE_ROOT = REPO_ROOT / "workspace"
BUILTIN_SKILLS_DIR = BACKEND_ROOT / "skills_builtin"
ORG_BUNDLE_DIR = BACKEND_ROOT / "defaults" / "b_report"
ORG_SKILLS_DIR = ORG_BUNDLE_DIR / "skills"
ORG_KNOWLEDGE_DIR = ORG_BUNDLE_DIR / "workspace"
ORG_FRAGMENTS_DIR = ORG_BUNDLE_DIR / "fragments"
# Legacy location (pre-migration); used only by migrate_workspace.sh
LEGACY_USERS_ROOT = APP_ROOT / "users"

DEFAULT_USER_ID = os.getenv("DATA_AGENT_DEFAULT_USER_ID", "local")


def user_dir(user_id: str) -> Path:
    return WORKSPACE_ROOT / user_id


def ensure_user_layout(user_id: str) -> Path:
    """Create the per-user directory tree if missing and return its root."""
    root = user_dir(user_id)
    for sub in ("rules", "skills", "files"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    config_path = root / "config.json"
    if not config_path.exists():
        config_path.write_text(_default_config_json(), encoding="utf-8")
    mcp_path = root / "mcp.json"
    if not mcp_path.exists():
        mcp_path.write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")
    subagents_path = root / "subagents.json"
    if not subagents_path.exists():
        subagents_path.write_text(_default_subagents_json(), encoding="utf-8")
    agents_md = root / "rules" / "AGENTS.md"
    if not agents_md.exists():
        agents_md.write_text(_default_agents_md(), encoding="utf-8")
    gitkeep = root / "files" / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")
    return root


def config_path(user_id: str) -> Path:
    return user_dir(user_id) / "config.json"


def mcp_path(user_id: str) -> Path:
    return user_dir(user_id) / "mcp.json"


def subagents_path(user_id: str) -> Path:
    return user_dir(user_id) / "subagents.json"


def rules_path(user_id: str) -> Path:
    return user_dir(user_id) / "rules" / "AGENTS.md"


def rules_dir(user_id: str) -> Path:
    return user_dir(user_id) / "rules"


def skills_dir(user_id: str) -> Path:
    return user_dir(user_id) / "skills"


def files_dir(user_id: str) -> Path:
    return user_dir(user_id) / "files"


def threads_db_path(user_id: str) -> Path:
    return user_dir(user_id) / "threads.sqlite"


def threads_meta_path(user_id: str) -> Path:
    return user_dir(user_id) / "threads_meta.json"


def org_rule_fragment_paths() -> list[Path]:
    """Organization rule fragments injected into agent memory (read-only).

    Excludes contract-skill-only fragments (injected via slash skill expansion).
    """
    if not ORG_FRAGMENTS_DIR.exists():
        return []
    paths: list[Path] = []
    for p in sorted(ORG_FRAGMENTS_DIR.glob("*.md")):
        name = p.name.lower()
        if "contract-skill" in name or name.startswith("agents.contract"):
            continue
        if name.startswith("contract-data-analysis"):
            continue
        paths.append(p)
    return paths


def _default_config_json() -> str:
    return """{
  "model": {
    "provider": "",
    "model": "",
    "api_key": "",
    "base_url": "",
    "temperature": 0
  },
  "system_prompt": "You are a helpful, careful general-purpose agent. Prefer using skills, tools, and the workspace under /workspace/.",
  "approve_writes": false,
  "approve_execute": false,
  "enabled_tools": {
    "web_fetch": true,
    "web_search": true
  },
  "permissions": []
}
"""


def _default_subagents_json() -> str:
    return """{
  "subagents": []
}
"""


def _default_agents_md() -> str:
    return """# Agent Rules

## Identity
You are a general-purpose assistant running in a browser-based agent workspace.

## Workspace
- User files live under `/workspace/`. Prefer reading and writing there.
- Shared org skills: `/skills/org/` and `/skills/builtin/`
- Personal skills: `/skills/user/`
- Shared org knowledge: `/knowledge/org/`
- Follow `/rules/AGENTS.md` for your personal conventions.

## Safety
- Ask before destructive shell commands when approval is required.
- Do not exfiltrate secrets or credentials.
- Prefer minimal, reversible changes.

## Style
- Be concise and actionable.
- Show your plan for multi-step work.
"""
