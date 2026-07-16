"""Shared FastAPI dependencies."""
from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException

from app.auth.models import ANONYMOUS_DEV_USER, AuthenticatedUser
from app.auth.session import SESSION_COOKIE, loads_session
from app.auth.settings import get_oauth_settings
from app.store.paths import ensure_user_layout


def _oauth_enabled() -> bool:
    oauth = get_oauth_settings()
    return bool(oauth.enabled and oauth.is_configured())


def get_session_user(
    da_session: str | None = Cookie(None, alias=SESSION_COOKIE),
) -> AuthenticatedUser | None:
    if not _oauth_enabled():
        return ANONYMOUS_DEV_USER
    oauth = get_oauth_settings()
    if not da_session:
        return None
    return loads_session(
        oauth.session_secret,
        da_session,
        max_age=oauth.cookie_max_age_seconds,
    )


async def get_current_user(
    user: AuthenticatedUser | None = Depends(get_session_user),
) -> AuthenticatedUser:
    if not _oauth_enabled():
        return ANONYMOUS_DEV_USER
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    ensure_user_layout(user.workspace_slug)
    return user


async def require_web_auth(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    return user


async def get_user_id(
    user: AuthenticatedUser = Depends(get_current_user),
) -> str:
    """Resolve per-user workspace slug from authenticated session."""
    return user.workspace_slug
