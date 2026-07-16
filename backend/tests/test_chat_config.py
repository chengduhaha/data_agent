"""Chat API config helpers."""
from __future__ import annotations

from app.api.chat import _thread_config
from app.agent.harness.config import recursion_limit


def test_thread_config_sets_recursion_limit() -> None:
    cfg = _thread_config("thread-abc")
    assert cfg["configurable"]["thread_id"] == "thread-abc"
    assert cfg["recursion_limit"] == recursion_limit(extended_run=False)
    assert cfg["recursion_limit"] == 155
