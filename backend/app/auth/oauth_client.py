"""OAuth2/OIDC HTTP client (authorization code + PKCE, no client_secret)."""
from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urlencode

import httpx

from app.auth.settings import OAuth2Settings


class OAuthClientError(Exception):
    def __init__(self, message: str, *, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def build_authorize_url(
    config: OAuth2Settings,
    *,
    state: str,
    code_challenge: str,
    redirect_uri: Optional[str] = None,
) -> str:
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "scope": config.scopes,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{config.authorize_url}?{urlencode(params)}"


async def exchange_authorization_code(
    config: OAuth2Settings,
    *,
    code: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "client_id": config.client_id,
        "code_verifier": code_verifier,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            config.token_url,
            data=data,
            headers={"Accept": "application/json"},
        )
    if resp.status_code >= 400:
        raise OAuthClientError(
            f"Token exchange failed: {resp.status_code} {resp.text[:500]}",
            status_code=resp.status_code,
        )
    body = resp.json()
    if not isinstance(body, dict):
        raise OAuthClientError("Token response is not a JSON object")
    return body


async def fetch_userinfo(
    config: OAuth2Settings,
    access_token: str,
) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
    if resp.status_code >= 400:
        raise OAuthClientError(
            f"Userinfo failed: {resp.status_code} {resp.text[:500]}",
            status_code=resp.status_code,
        )
    body = resp.json()
    if not isinstance(body, dict):
        raise OAuthClientError("Userinfo response is not a JSON object")
    return body
