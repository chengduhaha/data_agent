"""Tests for skill.zip upload and platform publish."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.auth.settings import clear_oauth_settings_cache
from app.main import app
from app.store import paths


@pytest.fixture(autouse=True)
def _oauth_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OAUTH2_ENABLED", "false")
    monkeypatch.delenv("DATA_AGENT_PLATFORM_EDITORS", raising=False)
    clear_oauth_settings_cache()


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)

    platform_skills = tmp_path / "platform_skills"
    platform_skills.mkdir()
    monkeypatch.setattr(paths, "PLATFORM_SKILLS_DIR", platform_skills)

    org_skills = tmp_path / "org_skills"
    org_skills.mkdir()
    monkeypatch.setattr(paths, "ORG_SKILLS_DIR", org_skills)
    monkeypatch.setattr(paths, "ORG_BUNDLE_DIR", tmp_path / "org_bundle")

    registry = tmp_path / "registry.json"
    monkeypatch.setattr(paths, "PLATFORM_REGISTRY_PATH", registry)

    builtin = tmp_path / "builtin"
    builtin.mkdir()
    monkeypatch.setattr(paths, "BUILTIN_SKILLS_DIR", builtin)

    return ws


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def _make_skill_zip(name: str = "demo-skill", *, version: str = "1.2.0") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(
            f"{name}/SKILL.md",
            f"---\nname: {name}\ndescription: demo zip skill\n---\n\n# {name}\n\nHello.\n",
        )
        zf.writestr(f"{name}/pack.yaml", f'name: {name}\nversion: "{version}"\n')
        zf.writestr(f"{name}/knowledge/readme.md", "# kb\n")
    return buf.getvalue()


def test_upload_skill_zip_creates_personal_skill(client: TestClient, workspace_tmp: Path) -> None:
    data = _make_skill_zip("zip-demo")
    r = client.post(
        "/api/skills/upload",
        files={"file": ("zip-demo.zip", data, "application/zip")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["skill"]["name"] == "zip-demo"
    assert body["skill"]["source"] == "user"
    skill_md = workspace_tmp / "local" / "skills" / "zip-demo" / "SKILL.md"
    assert skill_md.exists()
    assert (workspace_tmp / "local" / "skills" / "zip-demo" / "knowledge" / "readme.md").exists()


def test_upload_rejects_non_zip(client: TestClient, workspace_tmp: Path) -> None:
    r = client.post(
        "/api/skills/upload",
        files={"file": ("notes.txt", b"not a zip", "text/plain")},
    )
    assert r.status_code == 400


def test_publish_personal_skill_overwrites_platform(
    client: TestClient, workspace_tmp: Path
) -> None:
    # Seed existing shared skill
    old = paths.ORG_SKILLS_DIR / "zip-demo"
    old.mkdir(parents=True)
    (old / "SKILL.md").write_text(
        "---\nname: zip-demo\ndescription: old\n---\n\n# old\n", encoding="utf-8"
    )
    plat = paths.PLATFORM_SKILLS_DIR / "zip-demo"
    plat.mkdir(parents=True)
    (plat / "SKILL.md").write_text(
        "---\nname: zip-demo\ndescription: old-platform\n---\n\n# old platform\n",
        encoding="utf-8",
    )

    data = _make_skill_zip("zip-demo", version="2.0.0")
    up = client.post(
        "/api/skills/upload",
        files={"file": ("zip-demo.zip", data, "application/zip")},
    )
    assert up.status_code == 200, up.text

    pub = client.post("/api/skills/zip-demo/publish")
    assert pub.status_code == 200, pub.text
    result = pub.json()
    assert result["ok"] is True
    assert result["replaced"] is True
    assert result["version"] == "2.0.0"

    published = (paths.PLATFORM_SKILLS_DIR / "zip-demo" / "SKILL.md").read_text(encoding="utf-8")
    assert "demo zip skill" in published
    mirrored = (paths.ORG_SKILLS_DIR / "zip-demo" / "SKILL.md").read_text(encoding="utf-8")
    assert "demo zip skill" in mirrored
    assert paths.PLATFORM_REGISTRY_PATH.exists()


def test_publish_cannot_overwrite_builtin(client: TestClient, workspace_tmp: Path) -> None:
    builtin = paths.BUILTIN_SKILLS_DIR / "file-ops"
    builtin.mkdir(parents=True)
    (builtin / "SKILL.md").write_text(
        "---\nname: file-ops\ndescription: builtin\n---\n\n# file-ops\n",
        encoding="utf-8",
    )
    user_dir = workspace_tmp / "local" / "skills" / "file-ops"
    user_dir.mkdir(parents=True)
    (user_dir / "SKILL.md").write_text(
        "---\nname: file-ops\ndescription: personal\n---\n\n# personal\n",
        encoding="utf-8",
    )
    r = client.post("/api/skills/file-ops/publish")
    assert r.status_code == 400
    assert "built-in" in r.text.lower() or "Cannot overwrite" in r.text


def test_publish_forbidden_when_not_editor(
    client: TestClient, workspace_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DATA_AGENT_PLATFORM_EDITORS", "someone-else")
    data = _make_skill_zip("zip-demo")
    up = client.post(
        "/api/skills/upload",
        files={"file": ("zip-demo.zip", data, "application/zip")},
    )
    assert up.status_code == 200
    r = client.post("/api/skills/zip-demo/publish")
    assert r.status_code == 403
