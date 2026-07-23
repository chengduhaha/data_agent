"""Map LangGraph astream_events(v2) to typed SSE payloads."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from langgraph.errors import GraphRecursionError

from app.agent.harness.context import get_harness_context
from app.agent.harness.config import load_harness_config, step_limit
from app.agent.harness.step_budget import get_segment_budget
from app.agent.harness.wrapup import (
    count_research_tool_calls,
    count_sql_evidence_in_messages,
    last_ai_text,
    missing_answer_in_stream,
    needs_final_answer_wrapup,
    stream_wrapup_tokens,
    _has_synthesis_headings,
)
from app.agent.harness.task_output import humanize_task_tool_output

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


async def _emit_budget(sql_queries_used: int = 0) -> str:
    payload = get_segment_budget()
    payload["sql_queries_used"] = sql_queries_used
    return sse("budget", payload)


async def _flush_checkpoint_answer_sse(
    agent: Any,
    config: dict[str, Any],
    streamed_text: str,
) -> AsyncIterator[str]:
    """Emit checkpoint answer text that never arrived via on_chat_model_stream."""
    try:
        state = await agent.aget_state(config)
        values = getattr(state, "values", None) or {}
        msgs = values.get("messages") or []
        delta = missing_answer_in_stream(streamed_text, last_ai_text(msgs))
        if delta:
            yield sse("token", {"text": delta})
    except Exception:
        logger.debug("checkpoint answer flush failed", exc_info=True)


def _preview_tool_output(output: Any, tool: str, *, inline_limit: int) -> Any:
    if tool == "task":
        return humanize_task_tool_output(output, limit=inline_limit)
    if hasattr(output, "content"):
        output = output.content
    if isinstance(output, str) and "Command(update=" in output:
        return humanize_task_tool_output(output, limit=inline_limit)
    return _safe_preview(output, inline_limit)


def _sse_token_text(chunk: str) -> str:
    for line in chunk.split("\n"):
        if line.startswith("data:"):
            try:
                payload = json.loads(line.removeprefix("data:").strip())
            except Exception:
                return ""
            text = payload.get("text")
            return text if isinstance(text, str) else ""
    return ""


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


async def _try_synthesis_wrapup(
    agent: Any,
    config: dict[str, Any],
    wrapup_model: Any,
    harness_cfg: Any,
    *,
    executed_queries: list[dict[str, str]],
    streamed_text: str = "",
) -> AsyncIterator[str] | None:
    """Yield wrap-up SSE chunks when evidence exists but the answer is incomplete."""
    if not harness_cfg.auto_wrapup or wrapup_model is None:
        return None
    try:
        state = await agent.aget_state(config)
        values = getattr(state, "values", None) or {}
        msgs = values.get("messages") or []
        cumulative_q = max(len(executed_queries), count_sql_evidence_in_messages(msgs))
        require_synthesis = bool(get_harness_context().get("require_synthesis"))
        research_count = count_research_tool_calls(msgs)
        if cumulative_q <= 0 and not require_synthesis and research_count < 8:
            return None
        prior = last_ai_text(msgs)
        if not needs_final_answer_wrapup(
            prior,
            query_count=cumulative_q,
            require_synthesis=require_synthesis,
            research_tool_count=research_count,
        ):
            return None
        if _has_synthesis_headings(streamed_text):
            return None
    except Exception:
        logger.debug("wrap-up precheck failed", exc_info=True)
        return None

    async def _gen() -> AsyncIterator[str]:
        yield sse("status", {"text": "Composing final answer…", "phase": "wrapup"})
        async for piece in stream_wrapup_tokens(
            wrapup_model,
            agent,
            config,
            harness_cfg=harness_cfg,
        ):
            yield sse("token", {"text": piece})
        yield sse("wrapup_done", {"ok": True})

    return _gen()


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
    streamed_text = ""
    extended = bool(config.get("configurable", {}).get("extended_run"))
    harness_cfg = load_harness_config(extended_run=extended)
    budget_every = 0

    # Continue on a completed graph (next=[]): synthesize from checkpoint evidence.
    if input_payload is None:
        try:
            state = await agent.aget_state(config)
            if not list(getattr(state, "next", ()) or []):
                wrapup = await _try_synthesis_wrapup(
                    agent,
                    config,
                    wrapup_model,
                    harness_cfg,
                    executed_queries=executed_queries,
                )
                if wrapup is not None:
                    async for chunk in wrapup:
                        yield chunk
                    if executed_queries:
                        yield sse("executed_sql", {"queries": executed_queries})
                        yield sse("query_appendix", {"queries": executed_queries})
                    async for chunk in _flush_checkpoint_answer_sse(agent, config, streamed_text):
                        yield chunk
                    yield await _emit_budget(len(executed_queries))
                    yield sse(
                        "done",
                        {
                            "thread_id": config.get("configurable", {}).get("thread_id"),
                            "incomplete": True,
                        },
                    )
                    return
        except Exception:
            logger.debug("continue-at-end wrap-up check failed", exc_info=True)

    try:
        yield sse("status", {"text": "Running agent…", "phase": "run"})
        yield await _emit_budget(len(executed_queries))

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
                    yield await _emit_budget(len(executed_queries))

            elif kind == "on_chat_model_stream":
                chunk = (event.get("data") or {}).get("chunk")
                text = _message_text(chunk)
                if text:
                    streamed_text += text
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
                yield await _emit_budget(len(executed_queries))

            elif kind == "on_tool_end":
                data = event.get("data") or {}
                tool = _tool_name(event)
                output = data.get("output")
                inline_limit = harness_cfg.tool_result_inline_max_chars
                preview_output = _preview_tool_output(
                    output, tool, inline_limit=min(2000, inline_limit // 4)
                )
                payload = {
                    "tool": tool,
                    "output": preview_output,
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
                async for chunk in _flush_checkpoint_answer_sse(agent, config, streamed_text):
                    if chunk:
                        streamed_text += _sse_token_text(chunk) or ""
                        incomplete = True
                    yield chunk
                wrapup = await _try_synthesis_wrapup(
                    agent,
                    config,
                    wrapup_model,
                    harness_cfg,
                    executed_queries=executed_queries,
                    streamed_text=streamed_text,
                )
                if wrapup is not None:
                    try:
                        async for chunk in wrapup:
                            yield chunk
                        incomplete = True
                    except Exception:
                        logger.exception("synthesis wrap-up after normal completion failed")

                if executed_queries:
                    yield sse("executed_sql", {"queries": executed_queries})
                    yield sse("query_appendix", {"queries": executed_queries})
                yield await _emit_budget(len(executed_queries))
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
                yield sse("query_appendix", {"queries": executed_queries})
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
                async for chunk in _flush_checkpoint_answer_sse(agent, config, streamed_text):
                    yield chunk
                    streamed_text += _sse_token_text(chunk) or ""
                wrapup = await _try_synthesis_wrapup(
                    agent,
                    config,
                    wrapup_model,
                    harness_cfg,
                    executed_queries=executed_queries,
                    streamed_text=streamed_text,
                )
                if wrapup is not None:
                    async for chunk in wrapup:
                        yield chunk
                elif not streamed_text.strip():
                    async for chunk in _stream_wrapup_sse(wrapup_model, agent, config):
                        yield chunk
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
