"""Platform publish permissions (editor whitelist)."""

from __future__ import annotations

import os


def is_platform_editor(user_id: str) -> bool:
    """Return True when `user_id` may publish to platform skills/MCP.

    When ``DATA_AGENT_PLATFORM_EDITORS`` is unset, local/dev allows all users
    (UAT convenience). Production should set an explicit comma-separated list of
    workspace slugs / cisLoginIds.
    """
    raw = os.getenv("DATA_AGENT_PLATFORM_EDITORS", "").strip()
    if not raw:
        return True
    allowed = {part.strip() for part in raw.split(",") if part.strip()}
    return user_id in allowed
