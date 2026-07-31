"""OAuth2/OIDC + PKCE + session unit tests."""
from __future__ import annotations

import base64
import hashlib
import os

import pytest
from fastapi.testclient import TestClient

from app.auth.models import ANONYMOUS_DEV_USER, AuthenticatedUser
from app.auth.pkce import code_challenge_s256, generate_code_verifier, generate_oauth_state
from app.auth.session import SESSION_COOKIE, dumps_session, loads_session
from app.auth.settings import OAuth2Settings, clear_oauth_settings_cache, get_oauth_settings
from app.auth.userinfo import parse_oidc_userinfo, workspace_slug
from app.main import app


@pytest.fixture(autouse=True)
def _reset_oauth_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure tests start from disabled OAuth unless explicitly patched."""
    clear_oauth_settings_cache()
    # Force-disable via env so absolute env_file (.env) cannot re-enable SSO in unit tests.
    monkeypatch.setenv("OAUTH2_ENABLED", "false")
    monkeypatch.delenv("OAUTH2_CLIENT_ID", raising=False)
    monkeypatch.delenv("OAUTH2_AUTHORIZE_URL", raising=False)
    monkeypatch.delenv("OAUTH2_TOKEN_URL", raising=False)
    monkeypatch.delenv("OAUTH2_USERINFO_URL", raising=False)
    monkeypatch.delenv("OAUTH2_REDIRECT_URI", raising=False)
    monkeypatch.delenv("OAUTH2_SESSION_SECRET", raising=False)
    monkeypatch.delenv("OAUTH2_FRONTEND_ORIGIN", raising=False)
    clear_oauth_settings_cache()
    yield
    clear_oauth_settings_cache()


def _enabled_oauth_settings() -> OAuth2Settings:
    return OAuth2Settings(
        enabled=True,
        client_id="test-client",
        authorize_url="https://idp.example/authorize",
        token_url="https://idp.example/token",
        userinfo_url="https://idp.example/userinfo",
        redirect_uri="http://localhost:6641/api/auth/callback",
        session_secret="test-secret-key-32chars-minimum!!",
        frontend_origin="http://localhost:6641",
    )


def test_pkce_s256_challenge() -> None:
    verifier = generate_code_verifier(64)
    challenge = code_challenge_s256(verifier)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    expected = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    assert challenge == expected


def test_oauth_state_unique() -> None:
    a = generate_oauth_state()
    b = generate_oauth_state()
    assert a != b
    assert len(a) > 20


def test_session_roundtrip() -> None:
    user = AuthenticatedUser(
        sub="sub-1",
        email="a@example.com",
        name="Alice",
        cis_login_id="alice",
        global_user_id="1001",
        workspace_slug="alice",
    )
    token = dumps_session("test-secret-key-32chars-minimum!!", user)
    loaded = loads_session("test-secret-key-32chars-minimum!!", token, max_age=3600)
    assert loaded is not None
    assert loaded.sub == "sub-1"
    assert loaded.email == "a@example.com"
    assert loaded.cis_login_id == "alice"
    assert loaded.workspace_slug == "alice"


def test_parse_oidc_userinfo_company_portal() -> None:
    parsed = parse_oidc_userinfo(
        {
            "sub": "aad-object-id",
            "cisLoginId": "jic",
            "globalUserId": 1338086,
            "email": "jic@company.com",
        }
    )
    assert parsed["sub"] == "aad-object-id"
    assert parsed["cis_login_id"] == "jic"
    assert parsed["global_user_id"] == "1338086"
    assert parsed["email"] == "jic@company.com"


def test_workspace_slug_sanitizes_special_chars() -> None:
    assert workspace_slug("jic", "sub-1") == "jic"
    assert workspace_slug("user@corp", "sub") == "user@corp"
    assert workspace_slug("bad/name", "sub") == "bad_name"
    assert workspace_slug(None, "sub-with-dash") == "sub-with-dash"


def test_auth_config_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/api/auth/config")
    assert resp.status_code == 200
    body = resp.json()
    assert body["enabled"] is False
    assert "button_label" in body
    assert body.get("idle_timeout_seconds", 86400) == 86400


def test_auth_bootstrap_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/api/auth/bootstrap")
    assert resp.status_code == 200
    body = resp.json()
    assert "config" in body
    assert body["config"]["enabled"] is False
    assert body["user"]["workspace_slug"] == ANONYMOUS_DEV_USER.workspace_slug
    assert "branding" in body
    assert "title_suffix" in body["branding"]


def test_auth_bootstrap_title_suffix_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.config.ui import clear_ui_settings_cache

    monkeypatch.setenv("DATA_AGENT_TITLE_SUFFIX", "for dev")
    clear_ui_settings_cache()
    client = TestClient(app)
    resp = client.get("/api/auth/bootstrap")
    assert resp.status_code == 200
    assert resp.json()["branding"]["title_suffix"] == "for dev"
    clear_ui_settings_cache()


def test_auth_bootstrap_unauthenticated_when_oauth_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_oauth_enabled(monkeypatch, _enabled_oauth_settings())
    client = TestClient(app)
    resp = client.get("/api/auth/bootstrap")
    assert resp.status_code == 200
    body = resp.json()
    assert body["config"]["enabled"] is True
    assert body["user"] is None


def test_auth_me_requires_session_when_oauth_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_oauth_enabled(monkeypatch, _enabled_oauth_settings())
    client = TestClient(app)
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_auth_me_anonymous_when_oauth_disabled() -> None:
    client = TestClient(app)
    resp = client.get("/api/auth/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["sub"] == ANONYMOUS_DEV_USER.sub
    assert body["workspace_slug"] == ANONYMOUS_DEV_USER.workspace_slug


def _patch_oauth_enabled(monkeypatch: pytest.MonkeyPatch, settings: OAuth2Settings) -> None:
    monkeypatch.setattr("app.auth.settings.get_oauth_settings", lambda: settings)
    monkeypatch.setattr("app.deps.get_oauth_settings", lambda: settings)
    monkeypatch.setattr("app.api.auth.get_oauth_settings", lambda: settings)


def test_auth_logout_clears_session_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_oauth_enabled(monkeypatch, _enabled_oauth_settings())
    client = TestClient(app)
    resp = client.post("/api/auth/logout")
    assert resp.status_code == 200
    assert resp.json() == {"message": "logged_out"}
    set_cookie_headers = resp.headers.get_list("set-cookie")
    assert any("da_session=" in h for h in set_cookie_headers)


def test_protected_chat_requires_auth_when_oauth_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_oauth_enabled(monkeypatch, _enabled_oauth_settings())
    client = TestClient(app)
    resp = client.post(
        "/api/chat/stream",
        json={"message": "hi"},
    )
    assert resp.status_code == 401


def test_protected_chat_works_with_session_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    oauth = _enabled_oauth_settings()
    _patch_oauth_enabled(monkeypatch, oauth)
    user = AuthenticatedUser(
        sub="sub-1",
        email="alice@example.com",
        name="Alice",
        cis_login_id="alice",
        workspace_slug="alice",
    )
    token = dumps_session(oauth.session_secret, user)
    client = TestClient(app)
    # Stream endpoint will fail at agent creation without full setup, but must not 401
    resp = client.post(
        "/api/chat/stream",
        json={"message": "hi"},
        cookies={SESSION_COOKIE: token},
    )
    assert resp.status_code != 401
