"""OAuth2/OIDC + PKCE authentication routes (BFF)."""
from __future__ import annotations

import json
import logging
from typing import Dict, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.auth.models import AuthenticatedUser
from app.auth.oauth_client import (
    OAuthClientError,
    build_authorize_url,
    exchange_authorization_code,
    fetch_userinfo,
)
from app.auth.pkce import code_challenge_s256, generate_code_verifier, generate_oauth_state
from app.auth.session import (
    FLOW_COOKIE,
    SESSION_COOKIE,
    delete_cookie_params,
    dumps_flow,
    dumps_session,
    loads_flow,
    session_cookie_params,
)
from app.auth.settings import OAuth2Settings, get_oauth_settings
from app.auth.userinfo import parse_oidc_userinfo, workspace_slug
from app.auth.roles import user_role
from app.deps import get_session_user
from app.store.paths import ensure_user_layout

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class AuthConfigResponse(BaseModel):
    enabled: bool
    button_label: str
    idle_timeout_seconds: int = 86400


class AuthUserResponse(BaseModel):
    sub: str
    cis_login_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    workspace_slug: str
    role: str = "user"


class AuthBootstrapResponse(BaseModel):
    config: AuthConfigResponse
    user: AuthUserResponse | None = None


def _user_response(user: AuthenticatedUser) -> AuthUserResponse:
    return AuthUserResponse(
        sub=user.sub,
        cis_login_id=user.cis_login_id,
        email=user.email,
        name=user.name,
        workspace_slug=user.workspace_slug,
        role=user_role(user.workspace_slug),
    )


def _require_oauth_config() -> OAuth2Settings:
    oauth = get_oauth_settings()
    if not oauth.enabled:
        raise HTTPException(status_code=404, detail="OAuth2 is disabled")
    if not oauth.is_configured():
        raise HTTPException(status_code=503, detail="OAuth2 is not fully configured")
    return oauth


@router.get("/config", response_model=AuthConfigResponse)
async def auth_config() -> AuthConfigResponse:
    oauth = get_oauth_settings()
    return AuthConfigResponse(
        enabled=bool(oauth.enabled and oauth.is_configured()),
        button_label=oauth.button_label or "Log in with Microsoft Entra",
        idle_timeout_seconds=oauth.idle_timeout_seconds,
    )


@router.get("/bootstrap", response_model=AuthBootstrapResponse)
async def auth_bootstrap(
    session_user: AuthenticatedUser | None = Depends(get_session_user),
) -> AuthBootstrapResponse:
    """Public bootstrap: OAuth config + optional session (never 401 when SSO is on)."""
    oauth = get_oauth_settings()
    config = AuthConfigResponse(
        enabled=bool(oauth.enabled and oauth.is_configured()),
        button_label=oauth.button_label or "Log in with Microsoft Entra",
        idle_timeout_seconds=oauth.idle_timeout_seconds,
    )
    if not oauth.enabled or not oauth.is_configured():
        from app.auth.models import ANONYMOUS_DEV_USER

        return AuthBootstrapResponse(config=config, user=_user_response(ANONYMOUS_DEV_USER))
    if session_user is None:
        return AuthBootstrapResponse(config=config, user=None)
    return AuthBootstrapResponse(config=config, user=_user_response(session_user))


@router.get("/me", response_model=AuthUserResponse)
async def auth_me(
    session_user: AuthenticatedUser | None = Depends(get_session_user),
) -> AuthUserResponse:
    oauth = get_oauth_settings()
    if not oauth.enabled or not oauth.is_configured():
        from app.auth.models import ANONYMOUS_DEV_USER

        return _user_response(ANONYMOUS_DEV_USER)
    if session_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _user_response(session_user)


@router.get("/login")
async def auth_login() -> RedirectResponse:
    oauth = _require_oauth_config()
    state = generate_oauth_state()
    verifier = generate_code_verifier()
    flow_token = dumps_flow(
        oauth.session_secret,
        {"state": state, "code_verifier": verifier},
    )
    redirect = RedirectResponse(
        build_authorize_url(oauth, state=state, code_challenge=code_challenge_s256(verifier)),
        status_code=302,
    )
    redirect.set_cookie(
        FLOW_COOKIE,
        flow_token,
        httponly=True,
        samesite="lax",
        secure=oauth.cookie_secure,
        path="/",
        max_age=600,
    )
    return redirect


@router.get("/callback")
async def auth_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    da_oauth_flow: Optional[str] = Cookie(None, alias=FLOW_COOKIE),
) -> RedirectResponse:
    oauth = _require_oauth_config()
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")
    if not da_oauth_flow:
        raise HTTPException(status_code=400, detail="Missing OAuth flow cookie")

    try:
        flow = loads_flow(oauth.session_secret, da_oauth_flow, max_age=600)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid or expired OAuth flow") from exc

    if flow.get("state") != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    verifier = str(flow.get("code_verifier") or "")
    if not verifier:
        raise HTTPException(status_code=400, detail="Missing PKCE verifier")

    try:
        token_body = await exchange_authorization_code(
            oauth, code=code, code_verifier=verifier
        )
    except OAuthClientError as exc:
        logger.error("OAuth token exchange failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    access_token = str(token_body.get("access_token") or "")
    if not access_token:
        raise HTTPException(status_code=502, detail="Token response missing access_token")

    try:
        userinfo = await fetch_userinfo(oauth, access_token)
    except OAuthClientError as exc:
        logger.error("OAuth userinfo failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    sub = str(userinfo.get("sub") or "").strip()
    if not sub:
        raise HTTPException(status_code=502, detail="Userinfo missing sub")

    parsed = parse_oidc_userinfo(userinfo)
    if not parsed["cis_login_id"]:
        raise HTTPException(status_code=502, detail="Userinfo missing cisLoginId")

    logger.info(
        "OAuth login userinfo: %s",
        json.dumps(userinfo, ensure_ascii=False, default=str),
    )

    slug = workspace_slug(parsed["cis_login_id"], parsed["sub"])
    ensure_user_layout(slug)

    user = AuthenticatedUser(
        sub=parsed["sub"],
        email=parsed["email"],
        name=parsed["display_name"],
        cis_login_id=parsed["cis_login_id"],
        global_user_id=parsed["global_user_id"],
        workspace_slug=slug,
    )
    session_token = dumps_session(oauth.session_secret, user)
    redirect = RedirectResponse(oauth.frontend_origin.rstrip("/") + "/", status_code=302)
    redirect.set_cookie(SESSION_COOKIE, session_token, **session_cookie_params(oauth))
    redirect.delete_cookie(FLOW_COOKIE, **delete_cookie_params(oauth))
    return redirect


@router.post("/logout")
async def auth_logout(response: Response) -> Dict[str, str]:
    oauth = get_oauth_settings()
    cookie_kw = delete_cookie_params(oauth)
    response.delete_cookie(SESSION_COOKIE, **cookie_kw)
    response.delete_cookie(FLOW_COOKIE, **cookie_kw)
    return {"message": "logged_out"}
