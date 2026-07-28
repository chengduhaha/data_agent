"""HTTP-level acceptance checks for harness plan criteria."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.auth.settings import clear_oauth_settings_cache
from app.main import app
from app.store import paths
from app.store.schemas import UserConfig


@pytest.fixture(autouse=True)
def _oauth_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_ENABLED", "false")
    clear_oauth_settings_cache()


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)
    return ws


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_capabilities_lists_org_tools(client: TestClient, workspace_tmp: Path) -> None:
    r = client.get("/api/capabilities")
    assert r.status_code == 200
    data = r.json()
    assert "extra_tools" in data
    assert "wkb_query" in data["extra_tools"]


def test_contract_skill_has_extensions(client: TestClient, workspace_tmp: Path) -> None:
    r = client.get("/api/skills/contract-guided-data-analysis", params={"source": "org"})
    assert r.status_code == 200
    body = r.json()
    assert body.get("harness", {}).get("tool_budgets", {}).get("run_query_safely") == 12
    assert "wkb_query" in (body.get("extensions", {}).get("tools") or [])


def test_disabled_skill_hidden_from_slash_list(
    client: TestClient, workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def _cfg(_uid: str) -> UserConfig:
        return UserConfig(disabled_skills=["contract-guided-data-analysis"])

    import app.api.skills as skills_mod

    monkeypatch.setattr(skills_mod, "load_user_config", _cfg)
    r = client.get("/api/skills")
    assert r.status_code == 200
    names = [s["name"] for s in r.json().get("skills", [])]
    assert "contract-guided-data-analysis" not in names
    assert "file-ops" not in names
    assert "web-research" not in names


def test_default_skills_visible_in_settings_list(
    client: TestClient, workspace_tmp: Path,
) -> None:
    r = client.get("/api/skills", params={"include_disabled": "true"})
    assert r.status_code == 200
    by_name = {s["name"]: s for s in r.json().get("skills", [])}
    assert by_name.get("file-ops", {}).get("default_skill") is True
    assert by_name.get("web-research", {}).get("default_skill") is True


def test_disabled_skill_visible_with_include_disabled(
    client: TestClient, workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def _cfg(_uid: str) -> UserConfig:
        return UserConfig(disabled_skills=["contract-guided-data-analysis"])

    import app.api.skills as skills_mod

    monkeypatch.setattr(skills_mod, "load_user_config", _cfg)
    r = client.get("/api/skills", params={"include_disabled": "true"})
    assert r.status_code == 200
    names = [s["name"] for s in r.json().get("skills", [])]
    assert "contract-guided-data-analysis" in names
    skill = next(s for s in r.json()["skills"] if s["name"] == "contract-guided-data-analysis")
    assert skill.get("disabled") is True


def test_mcp_health_endpoint_shape(
    client: TestClient, workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def _health(_uid: str, *, ttl: float = 30.0) -> dict:
        return {"gateway-vertica-prod": {"ok": True, "tool_count": 3}}

    import app.api.mcp as mcp_mod

    monkeypatch.setattr(mcp_mod.mcp_manager, "health_check", _health)
    r = client.get("/api/mcp/health")
    assert r.status_code == 200
    assert "servers" in r.json()
    assert "gateway-vertica-prod" in r.json()["servers"]
