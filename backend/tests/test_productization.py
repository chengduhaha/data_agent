"""Workspace isolation, org bundle mount, and secrets redaction regression tests."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.agent.model_catalog import catalog_as_api
from app.auth.settings import clear_oauth_settings_cache
from app.main import app
from app.store import paths
from app.store.io import (
    list_skills,
    load_effective_mcp_config,
    load_mcp_config,
    make_thread_title,
    save_mcp_config,
    upsert_thread_meta,
)
from app.store.schemas import McpConfig, McpServerConfig
from app.store.secrets import merge_preserved_secrets, redact_mapping


@pytest.fixture(autouse=True)
def _oauth_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Productization API tests assume anonymous local dev user."""
    monkeypatch.setenv("OAUTH2_ENABLED", "false")
    clear_oauth_settings_cache()


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect per-user storage to an isolated temp directory."""
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)
    return ws


def test_ensure_user_layout_creates_workspace_tree(workspace_tmp: Path) -> None:
    root = paths.ensure_user_layout("alice")
    assert root == workspace_tmp / "alice"
    assert (root / "config.json").exists()
    assert (root / "mcp.json").exists()
    assert (root / "skills").is_dir()
    assert (root / "rules" / "AGENTS.md").exists()
    assert (root / "files").is_dir()


def test_user_config_isolation(workspace_tmp: Path) -> None:
    paths.ensure_user_layout("alice")
    paths.ensure_user_layout("bob")
    alice_cfg = paths.config_path("alice")
    bob_cfg = paths.config_path("bob")
    alice_cfg.write_text('{"model": {"provider": "alice"}}', encoding="utf-8")
    bob_cfg.write_text('{"model": {"provider": "bob"}}', encoding="utf-8")
    assert json.loads(alice_cfg.read_text())["model"]["provider"] == "alice"
    assert json.loads(bob_cfg.read_text())["model"]["provider"] == "bob"


def test_list_skills_includes_org_bundle(workspace_tmp: Path) -> None:
    skills = asyncio.run(list_skills("local"))
    sources = {s.source for s in skills}
    names = {s.name for s in skills}
    assert "org" in sources
    assert "contract-guided-data-analysis" in names
    org_skill = next(s for s in skills if s.name == "contract-guided-data-analysis")
    assert org_skill.editable is False
    assert org_skill.source == "org"


def test_org_mcp_not_persisted_in_user_json(
    workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("VERTICA_API_KEY", "secret-key")
    monkeypatch.setenv("VERTICA_HOST", "host")
    monkeypatch.setenv("VERTICA_DATABASE", "db")
    monkeypatch.setenv("VERTICA_USER", "user")
    monkeypatch.setenv("VERTICA_PASSWORD", "pass")

    effective = asyncio.run(load_effective_mcp_config("alice"))
    assert "gateway-vertica-prod" in effective.mcpServers

    stored = asyncio.run(load_mcp_config("alice"))
    assert "gateway-vertica-prod" not in stored.mcpServers
    raw = json.loads(paths.mcp_path("alice").read_text())
    assert "gateway-vertica-prod" not in raw.get("mcpServers", {})


def test_redact_mapping_masks_sensitive_headers() -> None:
    data = {
        "headers": {
            "x-api-key": "supersecret12345",
            "Content-Type": "application/json",
        }
    }
    redacted = redact_mapping(data)
    assert "supersecret" not in redacted["headers"]["x-api-key"]
    assert redacted["headers"]["x-api-key_set"] is True
    assert redacted["headers"]["Content-Type"] == "application/json"


def test_merge_preserved_secrets_keeps_server_value() -> None:
    existing = {"headers": {"x-api-key": "real-secret-value"}}
    incoming = {"headers": {"x-api-key": "supe…"}}
    merged = merge_preserved_secrets(incoming, existing)
    assert merged["headers"]["x-api-key"] == "real-secret-value"


def test_model_catalog_never_exposes_api_key() -> None:
    payload = catalog_as_api()
    blob = json.dumps(payload)
    assert '"api_key"' not in blob
    for model in payload.get("models", []):
        assert "api_key" not in model
        assert "has_api_key" in model


def test_mcp_get_redacts_personal_secrets(workspace_tmp: Path) -> None:
    asyncio.run(
        save_mcp_config(
            "local",
            McpConfig(
                mcpServers={
                    "personal": McpServerConfig(
                        transport="stdio",
                        command="echo",
                        env={"API_KEY": "my-personal-secret"},
                        enabled=True,
                    )
                }
            ),
        )
    )

    client = TestClient(app)
    resp = client.get("/api/mcp")
    assert resp.status_code == 200
    body = resp.json()
    assert "my-personal-secret" not in json.dumps(body)
    personal = body["mcpServers"]["personal"]
    assert personal["env"]["API_KEY_set"] is True
    assert "org_servers" in body


def test_thread_meta_isolated_per_user(workspace_tmp: Path) -> None:
    asyncio.run(upsert_thread_meta("alice", "t1", title="Alice question about sales"))
    asyncio.run(upsert_thread_meta("bob", "t2", title="Bob inventory check"))

    alice_meta = json.loads(paths.threads_meta_path("alice").read_text())
    bob_meta = json.loads(paths.threads_meta_path("bob").read_text())
    assert alice_meta["t1"]["title"] == "Alice question about sales"
    assert "t2" not in alice_meta
    assert bob_meta["t2"]["title"] == "Bob inventory check"
    assert "t1" not in bob_meta


def test_make_thread_title_truncates_long_messages() -> None:
    short = make_thread_title("What is revenue?")
    assert short == "What is revenue?"
    long_msg = "x" * 80
    title = make_thread_title(long_msg)
    assert len(title) <= 56
    assert title.endswith("…")
