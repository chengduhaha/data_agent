"""Signed cookie sessions for OAuth flow state and user sessions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.auth.models import AuthenticatedUser
from app.auth.settings import OAuth2Settings

FLOW_COOKIE = "da_oauth_flow"
SESSION_COOKIE = "da_session"


def _serializer(secret: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret, salt="data-agent-oauth")


def dumps_flow(secret: str, payload: Dict[str, Any]) -> str:
    return _serializer(secret).dumps(payload)


def loads_flow(secret: str, token: str, *, max_age: int = 600) -> Dict[str, Any]:
    return _serializer(secret).loads(token, max_age=max_age)


def dumps_session(secret: str, user: AuthenticatedUser) -> str:
    payload = {
        "sub": user.sub,
        "email": user.email,
        "name": user.name,
        "cis_login_id": user.cis_login_id,
        "global_user_id": user.global_user_id,
        "workspace_slug": user.workspace_slug,
        "login_at": datetime.now(timezone.utc).isoformat(),
    }
    return _serializer(secret).dumps(payload)


def loads_session(
    secret: str,
    token: str,
    *,
    max_age: int,
) -> Optional[AuthenticatedUser]:
    try:
        data = _serializer(secret).loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None
    if not isinstance(data, dict):
        return None
    sub = str(data.get("sub") or "").strip()
    if not sub:
        return None
    workspace_slug = str(data.get("workspace_slug") or "").strip()
    if not workspace_slug:
        return None
    return AuthenticatedUser(
        sub=sub,
        email=data.get("email"),
        name=data.get("name"),
        cis_login_id=data.get("cis_login_id"),
        global_user_id=data.get("global_user_id"),
        workspace_slug=workspace_slug,
        is_anonymous=False,
    )


def session_cookie_params(config: OAuth2Settings) -> Dict[str, Any]:
    return {
        "httponly": True,
        "samesite": "lax",
        "secure": config.cookie_secure,
        "path": "/",
        "max_age": config.cookie_max_age_seconds,
    }


def delete_cookie_params(config: OAuth2Settings) -> Dict[str, Any]:
    return {
        "httponly": True,
        "samesite": "lax",
        "secure": config.cookie_secure,
        "path": "/",
    }
