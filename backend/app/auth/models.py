"""Authenticated user model for Web SSO."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.store.paths import DEFAULT_USER_ID


@dataclass(frozen=True)
class AuthenticatedUser:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    cis_login_id: Optional[str] = None
    global_user_id: Optional[str] = None
    workspace_slug: str = ""
    is_anonymous: bool = False


ANONYMOUS_DEV_USER = AuthenticatedUser(
    sub="anonymous-dev",
    email=None,
    name="Development User",
    workspace_slug=DEFAULT_USER_ID,
    is_anonymous=True,
)
