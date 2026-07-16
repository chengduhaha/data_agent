"""Token-buffer summarization defaults (ClaudeCode-style autocompact threshold)."""

from __future__ import annotations

from typing import Any

from deepagents.middleware.summarization import SummarizationMiddleware

from app.agent.harness.config import HarnessConfig


def _max_input_tokens(model: Any, cfg: HarnessConfig) -> int:
    profile = getattr(model, "profile", None)
    if isinstance(profile, dict) and profile.get("max_input_tokens"):
        return int(profile["max_input_tokens"])
    return cfg.default_max_input_tokens


def make_summarization_middleware(
    model: Any,
    backend: Any,
    cfg: HarnessConfig,
) -> SummarizationMiddleware:
    """Summarize when within buffer tokens of model context window."""
    max_input = _max_input_tokens(model, cfg)
    buffer = cfg.summarization_buffer_tokens
    trigger_tokens = max(8_000, max_input - buffer)
    keep_frac = cfg.summarization_keep_fraction
    trigger_frac = cfg.summarization_trigger_fraction

    # Prefer absolute token trigger when profile is known; fraction as floor.
    fraction_trigger = int(max_input * trigger_frac)
    effective_trigger = min(trigger_tokens, fraction_trigger)

    return SummarizationMiddleware(
        model=model,
        backend=backend,
        trigger=("tokens", effective_trigger),
        keep=("fraction", keep_frac),
        truncate_args_settings={
            "trigger": ("tokens", effective_trigger),
            "keep": ("fraction", keep_frac),
        },
    )
