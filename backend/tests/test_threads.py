"""Thread sidebar listing tests."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from app.store import paths
from app.store.io import upsert_thread_meta
from app.store.threads import list_user_threads


@pytest.fixture()
def workspace_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setattr(paths, "WORKSPACE_ROOT", ws)
    return ws


def test_list_threads_from_meta_without_checkpointer(workspace_tmp: Path) -> None:
    async def _seed() -> None:
        await upsert_thread_meta("alice", "thread-a", title="First question")
        await upsert_thread_meta("alice", "thread-b", title="Second question")

    asyncio.run(_seed())
    threads = asyncio.run(list_user_threads("alice"))
    ids = {t["thread_id"] for t in threads}
    assert ids == {"thread-a", "thread-b"}
    titles = {t["title"] for t in threads}
    assert "First question" in titles


def test_thread_list_isolated_per_user(workspace_tmp: Path) -> None:
    async def _seed() -> None:
        await upsert_thread_meta("alice", "a1", title="Alice chat")
        await upsert_thread_meta("bob", "b1", title="Bob chat")

    asyncio.run(_seed())
    alice = asyncio.run(list_user_threads("alice"))
    bob = asyncio.run(list_user_threads("bob"))
    assert [t["thread_id"] for t in alice] == ["a1"]
    assert [t["thread_id"] for t in bob] == ["b1"]


def test_threads_meta_persisted_on_disk(workspace_tmp: Path) -> None:
    asyncio.run(upsert_thread_meta("alice", "t1", title="Persist me"))
    meta_path = paths.threads_meta_path("alice")
    assert meta_path.exists()
    data = json.loads(meta_path.read_text())
    assert data["t1"]["title"] == "Persist me"
