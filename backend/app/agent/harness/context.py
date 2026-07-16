"""Per-request harness context (thread id, run segment, user)."""

from __future__ import annotations

import contextvars
from typing import Any

_harness_ctx: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar(
    "harness_ctx", default={}
)


def set_harness_context(**kwargs: Any) -> contextvars.Token[dict[str, Any]]:
    current = dict(_harness_ctx.get())
    current.update(kwargs)
    return _harness_ctx.set(current)


def reset_harness_context(token: contextvars.Token[dict[str, Any]]) -> None:
    _harness_ctx.reset(token)


def get_harness_context() -> dict[str, Any]:
    return dict(_harness_ctx.get())


def get_thread_segment() -> tuple[str, int]:
    ctx = get_harness_context()
    return str(ctx.get("thread_id") or "default"), int(ctx.get("run_segment") or 1)


def get_user_id() -> str:
    return str(get_harness_context().get("user_id") or "")
