"""Tests for LLM rate-limit retry and error formatting."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.agent.harness.llm_resilience import (
    LlmRateLimitMiddleware,
    format_rate_limit_error,
    format_stream_chunk_timeout_error,
    is_rate_limit_error,
    is_stream_chunk_timeout_error,
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


class _StreamChunkTimeoutError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def test_is_stream_chunk_timeout_error_detects_message() -> None:
    exc = _StreamChunkTimeoutError(
        "No streaming chunk received for 120.0s (model=model-router, chunks_received=32)"
    )
    assert is_stream_chunk_timeout_error(exc)


def test_format_stream_error_stream_chunk_timeout() -> None:
    exc = _StreamChunkTimeoutError(
        "No streaming chunk received for 120.0s (model=model-router, chunks_received=32)"
    )
    msg = format_stream_error(exc)
    assert "paused longer than expected" in msg
    assert "Model Router" in msg


def test_format_stream_chunk_timeout_error() -> None:
    msg = format_stream_chunk_timeout_error(
        _StreamChunkTimeoutError("model=model-router")
    )
    assert "Model Router" in msg


def test_llm_middleware_retries_on_stream_chunk_timeout() -> None:
    calls = 0

    async def handler(_request):
        nonlocal calls
        calls += 1
        if calls < 2:
            raise _StreamChunkTimeoutError("No streaming chunk received for 120.0s")
        return "ok"

    mw = LlmRateLimitMiddleware(
        SimpleNamespace(llm_max_retries=2, llm_retry_backoff=0.01)
    )
    result = asyncio.run(mw.awrap_model_call(object(), handler))
    assert result == "ok"
    assert calls == 2


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
