"""Map LangGraph astream_events(v2) to typed SSE payloads."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from langgraph.errors import GraphRecursionError

from app.agent.harness.config import load_harness_config, step_limit
from app.agent.harness.step_budget import get_segment_budget
from app.agent.harness.wrapup import (
    last_ai_text,
    needs_synthesis_wrapup,
    stream_wrapup_tokens,
)

logger = logging.getLogger(__name__)

# Vertica MCP tools whose `query` field must not be truncated in SSE payloads.
VERTICA_QUERY_TOOLS = frozenset({
    "run_query_safely",
    "execute_query_paginated",
    "execute_query_stream",
    "profile_query",
})


def sse(event: str, data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, default=str)
    return f"event: {event}\ndata: {payload}\n\n"


def _message_text(chunk: Any) -> str:
    content = getattr(chunk, "content", None)
    if content is None and isinstance(chunk, dict):
        content = chunk.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif hasattr(block, "text"):
                parts.append(str(block.text))
        return "".join(parts)
    return ""


def _tool_name(event: dict[str, Any]) -> str:
    name = event.get("name")
    if name:
        return str(name)
    data = event.get("data") or {}
    for key in ("name", "tool"):
        if key in data and data[key]:
            return str(data[key])
    return "tool"


def _safe_preview(value: Any, limit: int = 2000) -> Any:
    try:
        text = json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        text = str(value)
    if len(text) > limit:
        return text[:limit] + "…"
    try:
        return json.loads(text)
    except Exception:
        return text


def _is_vertica_query_tool(tool: str) -> bool:
    name = (tool or "").lower()
    return (
        name in VERTICA_QUERY_TOOLS
        or "run_query" in name
        or name.startswith("execute_query")
    )


def _extract_query_from_input(raw_input: Any) -> str | None:
    if raw_input is None:
        return None
    if isinstance(raw_input, dict):
        for key in ("query", "sql"):
            value = raw_input.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None
    if isinstance(raw_input, str):
        try:
            return _extract_query_from_input(json.loads(raw_input))
        except Exception:
            return None
    return None


def _preview_tool_input(raw_input: Any, tool: str, limit: int = 2000) -> Any:
    if not _is_vertica_query_tool(tool):
        return _safe_preview(raw_input, limit)
    if isinstance(raw_input, dict):
        preview = _safe_preview(
            {k: v for k, v in raw_input.items() if k not in ("query", "sql")},
            limit,
        )
        if not isinstance(preview, dict):
            preview = {}
        query = _extract_query_from_input(raw_input)
        if query is not None:
            preview["query"] = query
        return preview or raw_input
    return _safe_preview(raw_input, limit)


async def _emit_budget() -> str:
    return sse("budget", get_segment_budget())


async def _stream_wrapup_sse(
    model: Any,
    agent: Any,
    config: dict[str, Any],
) -> AsyncIterator[str]:
    extended = bool(config.get("configurable", {}).get("extended_run"))
    cfg = load_harness_config(extended_run=extended)
    yield sse("status", {"text": "Composing final answer…", "phase": "wrapup"})
    had_tokens = False
    async for piece in stream_wrapup_tokens(model, agent, config, harness_cfg=cfg):
        had_tokens = True
        yield sse("token", {"text": piece})
    if not had_tokens:
        yield sse(
            "token",
            {
                "text": (
                    "\n\n---\n**Run paused** (tool-step limit). "
                    "Click **Continue** to resume from the checkpoint."
                )
            },
        )
    yield sse("wrapup_done", {"ok": True})


async def stream_agent_events(
    agent: Any,
    input_payload: dict[str, Any] | Any,
    config: dict[str, Any],
    *,
    wrapup_model: Any | None = None,
) -> AsyncIterator[str]:
    """Yield SSE strings from agent.astream_events(version='v2')."""
    executed_queries: list[dict[str, str]] = []
    seen_sql: set[str] = set()
    extended = bool(config.get("configurable", {}).get("extended_run"))
    harness_cfg = load_harness_config(extended_run=extended)
    budget_every = 0

    try:
        yield sse("status", {"text": "Running agent…", "phase": "run"})
        yield await _emit_budget()

        async for event in agent.astream_events(input_payload, config=config, version="v2"):
            kind = event.get("event")
            tags = event.get("tags") or []
            name = event.get("name") or ""

            if kind == "on_chat_model_start":
                yield sse(
                    "status",
                    {"text": "Thinking — planning next step…", "phase": "model"},
                )
                budget_every += 1
                if budget_every % 2 == 0:
                    yield await _emit_budget()

            elif kind == "on_chat_model_stream":
                chunk = (event.get("data") or {}).get("chunk")
                text = _message_text(chunk)
                if text:
                    yield sse("token", {"text": text})

            elif kind == "on_tool_start":
                data = event.get("data") or {}
                tool = _tool_name(event)
                raw_input = data.get("input")
                if _is_vertica_query_tool(tool):
                    sql = _extract_query_from_input(raw_input)
                    if sql and sql not in seen_sql:
                        seen_sql.add(sql)
                        executed_queries.append({"sql": sql, "tool": tool})
                payload = {
                    "tool": tool,
                    "input": _preview_tool_input(raw_input, tool),
                    "run_id": event.get("run_id"),
                }
                if tool == "task" or "subagent" in str(tags).lower():
                    yield sse(
                        "subagent",
                        {
                            "phase": "start",
                            "tool": tool,
                            "input": payload["input"],
                            "run_id": payload["run_id"],
                        },
                    )
                yield sse("tool_start", payload)
                yield sse(
                    "status",
                    {
                        "text": f"Running tool: {tool}",
                        "phase": "tool",
                        "tool": tool,
                    },
                )
                yield await _emit_budget()

            elif kind == "on_tool_end":
                data = event.get("data") or {}
                tool = _tool_name(event)
                output = data.get("output")
                if hasattr(output, "content"):
                    output = output.content
                inline_limit = harness_cfg.tool_result_inline_max_chars
                payload = {
                    "tool": tool,
                    "output": _safe_preview(output, min(2000, inline_limit // 4)),
                    "run_id": event.get("run_id"),
                }
                if tool == "task" or "subagent" in str(tags).lower():
                    yield sse(
                        "subagent",
                        {
                            "phase": "end",
                            "tool": tool,
                            "output": payload["output"],
                            "run_id": payload["run_id"],
                        },
                    )
                yield sse("tool_end", payload)

            elif kind == "on_chain_end" and name in ("LangGraph", "RunnableSequence"):
                pass

        try:
            state = await agent.aget_state(config)
            interrupts = []
            if state and getattr(state, "tasks", None):
                for task in state.tasks:
                    for intr in getattr(task, "interrupts", None) or []:
                        interrupts.append(
                            {
                                "id": getattr(intr, "id", None),
                                "value": _safe_preview(getattr(intr, "value", intr)),
                            }
                        )
            values = getattr(state, "values", None) or {}
            if isinstance(values, dict) and values.get("__interrupt__"):
                interrupts.append({"value": _safe_preview(values["__interrupt__"])})

            if interrupts:
                yield sse(
                    "interrupt",
                    {
                        "interrupts": interrupts,
                        "thread_id": config.get("configurable", {}).get("thread_id"),
                    },
                )
            else:
                incomplete = False
                if (
                    harness_cfg.auto_wrapup
                    and wrapup_model is not None
                    and executed_queries
                ):
                    try:
                        values = getattr(state, "values", None) or {}
                        prior = last_ai_text(values.get("messages") or [])
                        if needs_synthesis_wrapup(
                            prior, query_count=len(executed_queries)
                        ):
                            yield sse(
                                "status",
                                {"text": "Composing final answer…", "phase": "wrapup"},
                            )
                            async for piece in stream_wrapup_tokens(
                                wrapup_model,
                                agent,
                                config,
                                harness_cfg=harness_cfg,
                            ):
                                yield sse("token", {"text": piece})
                            yield sse("wrapup_done", {"ok": True})
                            incomplete = True
                    except Exception:
                        logger.exception("synthesis wrap-up after normal completion failed")

                if executed_queries:
                    yield sse("executed_sql", {"queries": executed_queries})
                yield sse(
                    "done",
                    {
                        "thread_id": config.get("configurable", {}).get("thread_id"),
                        "incomplete": incomplete,
                    },
                )
        except Exception:
            logger.debug("post-stream state inspect failed", exc_info=True)
            if executed_queries:
                yield sse("executed_sql", {"queries": executed_queries})
            yield sse(
                "done",
                {
                    "thread_id": config.get("configurable", {}).get("thread_id"),
                    "incomplete": False,
                },
            )

    except GraphRecursionError as exc:
        logger.info("agent hit recursion/step limit: %s", exc)
        thread_id = config.get("configurable", {}).get("thread_id")
        run_segment = int(config.get("configurable", {}).get("run_segment") or 1)
        steps = step_limit(extended_run=extended)
        budget = get_segment_budget()

        # Auto wrap-up: synthesize a final answer when the model did not finish.
        if harness_cfg.auto_wrapup and wrapup_model is not None:
            try:
                state = await agent.aget_state(config)
                values = getattr(state, "values", None) or {}
                prior = last_ai_text(values.get("messages") or [])
                async for chunk in _stream_wrapup_sse(wrapup_model, agent, config):
                    yield chunk
                if prior:
                    yield sse("status", {"text": "Appended wrap-up conclusion.", "phase": "wrapup"})
            except Exception:
                logger.exception("wrap-up after recursion limit failed")

        yield sse(
            "continue_prompt",
            {
                "thread_id": thread_id,
                "run_segment": run_segment,
                "steps_used": budget.get("steps_used", steps),
                "steps_limit": budget.get("steps_limit", steps),
                "message": (
                    "Agent reached the tool-step limit for this segment. "
                    "A wrap-up summary was added when possible. "
                    "Click Continue to keep working, or send a narrower follow-up."
                ),
            },
        )
        yield sse(
            "done",
            {
                "thread_id": thread_id,
                "incomplete": True,
                "run_segment": run_segment,
            },
        )
    except Exception as exc:
        logger.exception("agent stream failed")
        yield sse("error", {"message": str(exc)})
