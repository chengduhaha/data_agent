"""Harness lifecycle hooks: on_phase_enter, before_tool, after_tool, on_synthesis_required.

Kept intentionally small — a synchronous callback registry that other harness
middleware (phases, tool_budget) can publish to, and that a skill's manifest
could eventually register handlers against. No behavior is core-specific.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

HookFn = Callable[..., None]

_HOOK_NAMES = ("on_phase_enter", "before_tool", "after_tool", "on_synthesis_required")


class HarnessHooks:
    def __init__(self) -> None:
        self._handlers: dict[str, list[HookFn]] = defaultdict(list)

    def on(self, hook_name: str, fn: HookFn) -> None:
        if hook_name not in _HOOK_NAMES:
            raise ValueError(f"Unknown harness hook: {hook_name}")
        self._handlers[hook_name].append(fn)

    def off(self, hook_name: str, fn: HookFn) -> None:
        handlers = self._handlers.get(hook_name)
        if handlers and fn in handlers:
            handlers.remove(fn)

    def emit(self, hook_name: str, *args: Any, **kwargs: Any) -> None:
        for fn in list(self._handlers.get(hook_name, [])):
            try:
                fn(*args, **kwargs)
            except Exception:  # pragma: no cover - hooks must never break the run
                import logging

                logging.getLogger(__name__).exception(
                    "Harness hook %s handler failed", hook_name
                )


harness_hooks = HarnessHooks()

__all__ = ["HarnessHooks", "harness_hooks"]
