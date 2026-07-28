"""Simple workspace role checks (admin vs user)."""

from __future__ import annotations

import os
from typing import Literal

from app.auth.settings import get_oauth_settings

Role = Literal["admin", "user"]

_DEFAULT_ADMIN_USERS = ("fredyc", "rickw", "shilpac")


def _admin_ids() -> set[str]:
    raw = os.getenv("DATA_AGENT_ADMIN_USERS", "").strip()
    if not raw:
        return {name.lower() for name in _DEFAULT_ADMIN_USERS}
    return {part.strip().lower() for part in raw.split(",") if part.strip()}


def is_admin(workspace_slug: str) -> bool:
    """Return True when the workspace may access Settings and admin APIs."""
    oauth = get_oauth_settings()
    if not oauth.enabled or not oauth.is_configured():
        return True
    slug = (workspace_slug or "").strip().lower()
    if not slug:
        return False
    return slug in _admin_ids()


def user_role(workspace_slug: str) -> Role:
    return "admin" if is_admin(workspace_slug) else "user"
