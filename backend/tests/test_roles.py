"""Role-based access for settings APIs."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.auth.roles import is_admin, user_role
from app.auth.settings import clear_oauth_settings_cache
from app.main import app


@pytest.fixture(autouse=True)
def _oauth_off(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_oauth_settings_cache()
    monkeypatch.setenv("OAUTH2_ENABLED", "false")
    clear_oauth_settings_cache()
    yield
    clear_oauth_settings_cache()


def test_default_admin_users(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_ENABLED", "true")
    monkeypatch.setenv("OAUTH2_CLIENT_ID", "x")
    monkeypatch.setenv("OAUTH2_AUTHORIZE_URL", "https://idp/a")
    monkeypatch.setenv("OAUTH2_TOKEN_URL", "https://idp/t")
    monkeypatch.setenv("OAUTH2_USERINFO_URL", "https://idp/u")
    monkeypatch.setenv("OAUTH2_REDIRECT_URI", "http://localhost/cb")
    monkeypatch.setenv("OAUTH2_SESSION_SECRET", "test-secret-key-32chars-minimum!!")
    monkeypatch.setenv("OAUTH2_FRONTEND_ORIGIN", "http://localhost:6641")
    clear_oauth_settings_cache()
    assert is_admin("fredyc")
    assert is_admin("rickw")
    assert is_admin("shilpac")
    assert not is_admin("alice")
    assert user_role("fredyc") == "admin"
    assert user_role("alice") == "user"


def test_settings_config_requires_admin_when_oauth_on(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_ENABLED", "true")
    monkeypatch.setenv("OAUTH2_CLIENT_ID", "x")
    monkeypatch.setenv("OAUTH2_AUTHORIZE_URL", "https://idp/a")
    monkeypatch.setenv("OAUTH2_TOKEN_URL", "https://idp/t")
    monkeypatch.setenv("OAUTH2_USERINFO_URL", "https://idp/u")
    monkeypatch.setenv("OAUTH2_REDIRECT_URI", "http://localhost/cb")
    monkeypatch.setenv("OAUTH2_SESSION_SECRET", "test-secret-key-32chars-minimum!!")
    monkeypatch.setenv("OAUTH2_FRONTEND_ORIGIN", "http://localhost:6641")
    clear_oauth_settings_cache()
    client = TestClient(app)
    assert client.get("/api/config").status_code == 401
    assert client.get("/api/skills").status_code == 401


def test_settings_config_open_in_dev_mode() -> None:
    client = TestClient(app)
    assert client.get("/api/config").status_code == 200
    assert client.get("/api/skills").status_code == 200


def test_non_admin_forbidden_from_settings_apis(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_ENABLED", "true")
    monkeypatch.setenv("OAUTH2_CLIENT_ID", "x")
    monkeypatch.setenv("OAUTH2_AUTHORIZE_URL", "https://idp/a")
    monkeypatch.setenv("OAUTH2_TOKEN_URL", "https://idp/t")
    monkeypatch.setenv("OAUTH2_USERINFO_URL", "https://idp/u")
    monkeypatch.setenv("OAUTH2_REDIRECT_URI", "http://localhost/cb")
    monkeypatch.setenv("OAUTH2_SESSION_SECRET", "test-secret-key-32chars-minimum!!")
    monkeypatch.setenv("OAUTH2_FRONTEND_ORIGIN", "http://localhost:6641")
    clear_oauth_settings_cache()

    from app.auth.models import AuthenticatedUser
    from app.deps import get_current_user

    alice = AuthenticatedUser(
        sub="alice-sub",
        cis_login_id="alice",
        workspace_slug="alice",
    )

    async def _alice() -> AuthenticatedUser:
        return alice

    app.dependency_overrides[get_current_user] = _alice
    try:
        client = TestClient(app)
        assert client.get("/api/config").status_code == 403
        assert client.get("/api/mcp").status_code == 403
        assert client.get("/api/skills?include_disabled=true").status_code == 403
        assert client.get("/api/skills").status_code == 200
        assert client.get("/api/chat/threads").status_code == 200
    finally:
        app.dependency_overrides.pop(get_current_user, None)
