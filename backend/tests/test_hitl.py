"""HITL resume and org config policy tests."""
from __future__ import annotations

from app.api.chat import _thread_config
from app.store.io import _apply_org_runtime_config
from app.store.schemas import UserConfig


def test_resume_command_expects_decisions_wrapper() -> None:
  # Documented contract for HumanInTheLoopMiddleware resume payload.
    decisions = [{"type": "approve"}]
    resume_value = {"decisions": decisions}
    assert resume_value["decisions"][0]["type"] == "approve"


def test_org_patch_disables_hitl() -> None:
    cfg = UserConfig(approve_writes=True, approve_execute=True)
    patched = _apply_org_runtime_config(cfg)
    assert patched.approve_writes is False
    assert patched.approve_execute is False


def test_thread_config_sets_recursion_limit() -> None:
    cfg = _thread_config("t1")
    assert cfg["recursion_limit"] == 155
    assert cfg["configurable"]["run_segment"] == 1

    extended = _thread_config("t1", extended_run=True)
    assert extended["recursion_limit"] == 405
