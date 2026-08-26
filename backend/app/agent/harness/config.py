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


def _stream_chunk_timeout_env(name: str, default: float) -> float | None:
    """Parse LLM stream chunk timeout seconds; 0/none/off disables the guard."""
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    lowered = raw.strip().lower()
    if lowered in ("0", "none", "off", "disable", "disabled"):
        return None
    try:
        value = float(raw.strip())
    except ValueError:
        return default
    if value <= 0:
        return None
    return value


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
    llm_max_retries: int = 4
    llm_retry_backoff: float = 2.0
    # Gap between streamed LLM chunks before LangChain aborts (None = disabled).
    # Default 600s — model-router / long tool-planning turns can pause >120s.
    llm_stream_chunk_timeout_s: float | None = 600.0
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
    segment_max_per_thread: int = 10
    evidence_max_items: int = 20
    evidence_track_all_tools: bool = False
    budget_warn_threshold: float = 0.80
    budget_merge_strategy: str = "skill_wins"
    forward_instruction_language: str = "en"
    synthesize_suffix_customizable: bool = True
    enable_dw_governance: bool = False
    enable_completeness_enhanced: bool = True
    enable_pack_framework: bool = True


def load_harness_config(*, extended_run: bool = False) -> HarnessConfig:
    step = _int_env(
        "DATA_AGENT_TOOL_STEP_LIMIT_EXTENDED" if extended_run else "DATA_AGENT_TOOL_STEP_LIMIT",
        400 if extended_run else 150,
    )
    cfg = HarnessConfig(
        tool_step_limit=_int_env("DATA_AGENT_TOOL_STEP_LIMIT", 150),
        tool_step_limit_extended=_int_env("DATA_AGENT_TOOL_STEP_LIMIT_EXTENDED", 400),
        recursion_buffer=_int_env("DATA_AGENT_RECURSION_BUFFER", 5),
        step_warn_fraction=_float_env("DATA_AGENT_STEP_WARN_FRACTION", 0.80),
        shell_timeout=_int_env("DATA_AGENT_SHELL_TIMEOUT", 60),
        mcp_timeout=_float_env("DATA_AGENT_MCP_TIMEOUT", 60.0),
        mcp_tool_max_retries=_int_env("DATA_AGENT_MCP_TOOL_MAX_RETRIES", 2),
        mcp_retry_backoff=_float_env("DATA_AGENT_MCP_RETRY_BACKOFF", 1.0),
        llm_max_retries=_int_env("DATA_AGENT_LLM_MAX_RETRIES", 4),
        llm_retry_backoff=_float_env("DATA_AGENT_LLM_RETRY_BACKOFF", 2.0),
        llm_stream_chunk_timeout_s=_stream_chunk_timeout_env(
            "DATA_AGENT_LLM_STREAM_CHUNK_TIMEOUT_S", 600.0
        ),
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
        segment_max_per_thread=_int_env("DATA_AGENT_SEGMENT_MAX_PER_THREAD", 10),
        evidence_max_items=_int_env("DATA_AGENT_EVIDENCE_MAX_ITEMS", 20),
        evidence_track_all_tools=_bool_env("DATA_AGENT_EVIDENCE_TRACK_ALL_TOOLS", False),
        budget_warn_threshold=_float_env("DATA_AGENT_BUDGET_WARN_THRESHOLD", 0.80),
        budget_merge_strategy=os.getenv("DATA_AGENT_BUDGET_MERGE_STRATEGY", "skill_wins"),
        forward_instruction_language=os.getenv("DATA_AGENT_FORWARD_INSTRUCTION_LANGUAGE", "en"),
        synthesize_suffix_customizable=_bool_env("DATA_AGENT_SYNTHESIZE_SUFFIX_CUSTOMIZABLE", True),
        enable_dw_governance=_bool_env("DATA_AGENT_ENABLE_DW_GOVERNANCE", False),
        enable_completeness_enhanced=_bool_env("DATA_AGENT_ENABLE_COMPLETENESS_ENHANCED", True),
        enable_pack_framework=_bool_env("DATA_AGENT_ENABLE_PACK_FRAMEWORK", True),
    )
    from app.agent.harness.runtime_overrides import get_overrides

    overrides = get_overrides()
    if overrides:
        data = cfg.__dict__.copy()
        data.update(overrides)
        return HarnessConfig(**data)
    return cfg


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
