"""Harness configuration (env-driven execution controls)."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw.strip())
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw.strip())
    except ValueError:
        return default


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() not in ("0", "false", "no", "off")


@dataclass(frozen=True)
class HarnessConfig:
    tool_step_limit: int = 150
    tool_step_limit_extended: int = 400
    recursion_buffer: int = 5
    step_warn_fraction: float = 0.80
    shell_timeout: int = 60
    mcp_timeout: float = 60.0
    mcp_tool_max_retries: int = 2
    mcp_retry_backoff: float = 1.0
    summarization_trigger_fraction: float = 0.85
    summarization_keep_fraction: float = 0.15
    summarization_buffer_tokens: int = 13_000
    strict: bool = True
    max_l1_catalog_offset_reads: int = 3
    max_task_per_segment: int = 1
    max_read_dup_cache: int = 256
    tool_result_inline_max_chars: int = 8000
    auto_wrapup: bool = True
    auto_continue: bool = False
    auto_continue_max_segments: int = 2
    wrapup_max_tokens: int = 4096
    default_max_input_tokens: int = 128_000


def load_harness_config(*, extended_run: bool = False) -> HarnessConfig:
    step = _int_env(
        "DATA_AGENT_TOOL_STEP_LIMIT_EXTENDED" if extended_run else "DATA_AGENT_TOOL_STEP_LIMIT",
        400 if extended_run else 150,
    )
    return HarnessConfig(
        tool_step_limit=_int_env("DATA_AGENT_TOOL_STEP_LIMIT", 150),
        tool_step_limit_extended=_int_env("DATA_AGENT_TOOL_STEP_LIMIT_EXTENDED", 400),
        recursion_buffer=_int_env("DATA_AGENT_RECURSION_BUFFER", 5),
        step_warn_fraction=_float_env("DATA_AGENT_STEP_WARN_FRACTION", 0.80),
        shell_timeout=_int_env("DATA_AGENT_SHELL_TIMEOUT", 60),
        mcp_timeout=_float_env("DATA_AGENT_MCP_TIMEOUT", 60.0),
        mcp_tool_max_retries=_int_env("DATA_AGENT_MCP_TOOL_MAX_RETRIES", 2),
        mcp_retry_backoff=_float_env("DATA_AGENT_MCP_RETRY_BACKOFF", 1.0),
        summarization_trigger_fraction=_float_env(
            "DATA_AGENT_SUMMARIZATION_TRIGGER_FRACTION", 0.85
        ),
        summarization_keep_fraction=_float_env(
            "DATA_AGENT_SUMMARIZATION_KEEP_FRACTION", 0.15
        ),
        summarization_buffer_tokens=_int_env(
            "DATA_AGENT_SUMMARIZATION_BUFFER_TOKENS", 13_000
        ),
        strict=_bool_env("DATA_AGENT_HARNESS_STRICT", True),
        max_l1_catalog_offset_reads=_int_env("DATA_AGENT_MAX_L1_OFFSET_READS", 3),
        max_task_per_segment=_int_env("DATA_AGENT_MAX_TASK_PER_SEGMENT", 1),
        max_read_dup_cache=_int_env("DATA_AGENT_MAX_READ_DUP_CACHE", 256),
        tool_result_inline_max_chars=_int_env(
            "DATA_AGENT_TOOL_RESULT_INLINE_MAX_CHARS", 8000
        ),
        auto_wrapup=_bool_env("DATA_AGENT_AUTO_WRAPUP", True),
        auto_continue=_bool_env("DATA_AGENT_AUTO_CONTINUE", False),
        auto_continue_max_segments=_int_env("DATA_AGENT_AUTO_CONTINUE_MAX_SEGMENTS", 2),
        wrapup_max_tokens=_int_env("DATA_AGENT_WRAPUP_MAX_TOKENS", 4096),
        default_max_input_tokens=_int_env("DATA_AGENT_MAX_INPUT_TOKENS", 128_000),
    )


def recursion_limit(*, extended_run: bool = False) -> int:
    cfg = load_harness_config(extended_run=extended_run)
    base = cfg.tool_step_limit_extended if extended_run else cfg.tool_step_limit
    return base + cfg.recursion_buffer


def step_limit(*, extended_run: bool = False) -> int:
    cfg = load_harness_config(extended_run=extended_run)
    return cfg.tool_step_limit_extended if extended_run else cfg.tool_step_limit


def step_warn_threshold(*, extended_run: bool = False) -> int:
    cfg = load_harness_config(extended_run=extended_run)
    limit = step_limit(extended_run=extended_run)
    return max(1, int(limit * cfg.step_warn_fraction))
