"""Retry and user-facing errors for transient LLM / gateway failures."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware

from app.agent.harness.config import HarnessConfig, load_harness_config
from app.agent.harness.mcp_resilience import _unwrap_exception

logger = logging.getLogger(__name__)


def is_rate_limit_error(exc: BaseException) -> bool:
    root = _unwrap_exception(exc)
    status = getattr(getattr(root, "response", None), "status_code", None)
    if status == 429:
        return True
    name = type(root).__name__.lower()
    if "ratelimit" in name:
        return True
    text = str(root).lower()
    return any(
        token in text
        for token in (
            "rate_limit",
            "rate limit",
            "too_many_requests",
            "429",
            "exceeded rate limit",
        )
    )


def is_stream_chunk_timeout_error(exc: BaseException) -> bool:
    root = _unwrap_exception(exc)
    try:
        from langchain_openai.chat_models._client_utils import StreamChunkTimeoutError

        if isinstance(root, StreamChunkTimeoutError):
            return True
    except ImportError:
        pass
    name = type(root).__name__.lower()
    if "streamchunktimeout" in name:
        return True
    text = str(root).lower()
    return "no streaming chunk received" in text or "stream_chunk_timeout" in text


def is_transient_llm_error(exc: BaseException) -> bool:
    return is_rate_limit_error(exc) or is_stream_chunk_timeout_error(exc)


def _retry_after_seconds(exc: BaseException) -> float | None:
    root = _unwrap_exception(exc)
    response = getattr(root, "response", None)
    headers = getattr(response, "headers", None)
    if not headers:
        return None
    raw = headers.get("retry-after") or headers.get("Retry-After")
    if raw is None:
        return None
    try:
        return max(0.5, float(raw))
    except (TypeError, ValueError):
        return None


def format_rate_limit_error(exc: BaseException | None = None) -> str:
    model_hint = ""
    if exc is not None:
        detail = str(_unwrap_exception(exc))
        if "gpt-5.1" in detail:
            model_hint = " Try GPT-5 Mini, GPT-4o, or Gemini 3.5 Flash in the model switcher."
    return (
        "The selected model is temporarily rate-limited by the Synnex Azure gateway "
        f"(HTTP 429). Please wait a minute and retry, or switch to another model.{model_hint}"
    )


def format_stream_chunk_timeout_error(exc: BaseException | None = None) -> str:
    model_hint = ""
    if exc is not None:
        detail = str(_unwrap_exception(exc))
        if "model-router" in detail:
            model_hint = (
                " Model Router can pause while routing — try Gemini 3.5 Flash or GPT-4o "
                "if this keeps happening."
            )
    return (
        "The model stream paused longer than expected (gateway may still be thinking or routing). "
        "Your thread is saved — click Continue or retry."
        f"{model_hint}"
    )


class LlmRateLimitMiddleware(AgentMiddleware):
    """Retry model calls on transient gateway failures (429, stream stalls)."""

    def __init__(self, cfg: HarnessConfig | None = None) -> None:
        loaded = cfg or load_harness_config()
        self.max_retries = loaded.llm_max_retries
        self.retry_backoff = loaded.llm_retry_backoff

    async def awrap_model_call(self, request: Any, handler: Any) -> Any:
        last_exc: BaseException | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await handler(request)
            except Exception as exc:
                last_exc = exc
                if not is_transient_llm_error(exc) or attempt >= self.max_retries:
                    raise
                if is_rate_limit_error(exc):
                    wait = _retry_after_seconds(exc) or self.retry_backoff * (2**attempt)
                    reason = "rate limited"
                else:
                    wait = self.retry_backoff * (2**attempt)
                    reason = "stream chunk timeout"
                logger.warning(
                    "LLM %s (attempt %d/%d); retrying in %.1fs: %s",
                    reason,
                    attempt + 1,
                    self.max_retries + 1,
                    wait,
                    _unwrap_exception(exc),
                )
                await asyncio.sleep(wait)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("LLM call failed without exception")


__all__ = [
    "LlmRateLimitMiddleware",
    "format_rate_limit_error",
    "format_stream_chunk_timeout_error",
    "is_rate_limit_error",
    "is_stream_chunk_timeout_error",
    "is_transient_llm_error",
]
