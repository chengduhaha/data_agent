"""Tests for LLM rate-limit retry and error formatting."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.agent.harness.llm_resilience import (
    LlmRateLimitMiddleware,
    format_rate_limit_error,
    is_rate_limit_error,
)
from app.agent.harness.mcp_resilience import format_stream_error


class _RateLimitError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def test_is_rate_limit_error_detects_429_message() -> None:
    exc = _RateLimitError(
        "Error code: 429 - {'error': {'code': 'rate_limit_exceeded'}}"
    )
    assert is_rate_limit_error(exc)


def test_format_rate_limit_error_mentions_alternate_models() -> None:
    msg = format_rate_limit_error(
        _RateLimitError("gpt-5.1 in eastus have exceeded rate limit")
    )
    assert "rate-limited" in msg
    assert "GPT-5 Mini" in msg


def test_format_stream_error_rate_limit() -> None:
    msg = format_stream_error(_RateLimitError("rate_limit_exceeded for gpt-5.1"))
    assert "rate-limited" in msg


def test_llm_middleware_retries_on_rate_limit() -> None:
    calls = 0

    async def handler(_request):
        nonlocal calls
        calls += 1
        if calls < 3:
            raise _RateLimitError("rate_limit_exceeded")
        return "ok"

    mw = LlmRateLimitMiddleware(
        SimpleNamespace(llm_max_retries=3, llm_retry_backoff=0.01)
    )
    result = asyncio.run(mw.awrap_model_call(object(), handler))
    assert result == "ok"
    assert calls == 3


def test_llm_middleware_raises_after_retries_exhausted() -> None:
    async def handler(_request):
        raise _RateLimitError("rate_limit_exceeded")

    mw = LlmRateLimitMiddleware(
        SimpleNamespace(llm_max_retries=1, llm_retry_backoff=0.01)
    )
    with pytest.raises(_RateLimitError):
        asyncio.run(mw.awrap_model_call(object(), handler))
