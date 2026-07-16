"""Chat streaming, resume (HITL), and thread management."""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.agent.factory import create_user_agent, get_checkpointer
from app.agent.harness.config import load_harness_config, recursion_limit
from app.agent.harness.context import reset_harness_context, set_harness_context
from app.agent.harness.middleware import reset_segment_state
from app.agent.harness.topic_detect import detect_topic_relation
from app.agent.harness.turn_summary import slice_messages_for_turn, summarize_turn
from app.agent.models import build_model
from app.agent.streaming import stream_agent_events
from app.deps import get_user_id
from app.store.chat_history import fold_checkpoint_messages
from app.store.threads import list_user_threads
from app.store.io import (
    append_turn_summary,
    delete_thread_meta,
    get_thread_meta_entry,
    increment_thread_run_segment,
    increment_thread_turn_index,
    load_threads_meta,
    load_user_config,
    make_thread_title,
    upsert_thread_meta,
)
from app.store.schemas import ChatResumeRequest, ChatStreamRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])


def _thread_config(
    thread_id: str,
    *,
    extended_run: bool = False,
    run_segment: int = 1,
) -> dict[str, Any]:
    return {
        "configurable": {
            "thread_id": thread_id,
            "run_segment": run_segment,
            "extended_run": extended_run,
        },
        "recursion_limit": recursion_limit(extended_run=extended_run),
    }


async def _resolve_run_segment(user_id: str, thread_id: str, continue_run: bool) -> int:
    meta = await load_threads_meta(user_id)
    entry = meta.get(thread_id) or {}
    segment = int(entry.get("run_segment") or 1)
    if continue_run:
        segment = await increment_thread_run_segment(user_id, thread_id)
        reset_segment_state(thread_id, segment)
    else:
        reset_segment_state(thread_id, segment)
    return segment


async def _maybe_summarize_last_turn(
    user_id: str,
    thread_id: str,
    agent: Any,
    config: dict[str, Any],
    cfg: Any,
) -> None:
    """Persist a rolling summary for the turn that just completed."""
    try:
        meta = await get_thread_meta_entry(user_id, thread_id)
        turn_index = int(meta.get("turn_index") or 1) - 1
        if turn_index < 0:
            return
        state = await agent.aget_state(config)
        values = getattr(state, "values", None) or {}
        messages = values.get("messages") or []
        turn_messages = slice_messages_for_turn(list(messages), turn_index)
        if not turn_messages:
            return
        model = build_model(cfg)
        summary = await summarize_turn(model, turn_messages)
        await append_turn_summary(
            user_id,
            thread_id,
            turn_index=turn_index,
            summary=summary,
        )
    except Exception:
        logger.debug("turn summary skipped", exc_info=True)


@router.post("/stream")
async def chat_stream(body: ChatStreamRequest, user_id: str = Depends(get_user_id)):
    uid = user_id
    thread_id = body.thread_id or str(uuid.uuid4())
    continue_run = body.continue_run

    if not continue_run and not (body.message or "").strip():
        raise HTTPException(status_code=400, detail="message required")

    run_segment = await _resolve_run_segment(uid, thread_id, continue_run)
    config = _thread_config(
        thread_id,
        extended_run=body.extended_run,
        run_segment=run_segment,
    )

    turn_index: int | None = None
    if not continue_run:
        turn_index = await increment_thread_turn_index(uid, thread_id)

    if continue_run:
        input_payload: Any = None
    else:
        input_payload = {"messages": [HumanMessage(content=body.message)]}
        title = make_thread_title(body.title or body.message)
        await upsert_thread_meta(
            uid, thread_id, title=title, run_segment=run_segment
        )

    async def event_gen():
        from app.agent.streaming import sse

        ctx_token = set_harness_context(
            thread_id=thread_id,
            run_segment=run_segment,
            user_id=uid,
            extended_run=body.extended_run,
        )
        yield sse(
            "meta",
            {
                "thread_id": thread_id,
                "user_id": uid,
                "run_segment": run_segment,
                "turn_index": turn_index,
            },
        )

        if not continue_run and body.message.strip():
            prior_meta = await get_thread_meta_entry(uid, thread_id)
            summaries = prior_meta.get("turn_summaries") or []
            prev_q = None
            if summaries:
                prev_q = str(summaries[-1].get("summary", ""))[:500]
            relation = detect_topic_relation(
                body.message,
                previous_question=prev_q,
                previous_summary=prev_q,
            )
            if relation.get("suggest_new_thread"):
                yield sse("topic_hint", relation)

        yield sse("status", {"text": "Initializing agent…", "phase": "init"})
        cfg = None
        wrapup_model = None
        try:
            cfg = await load_user_config(uid)
            wrapup_model = build_model(cfg)
            yield sse("status", {"text": "Loading tools & MCP…", "phase": "init"})
            agent = await create_user_agent(uid, cfg, extended_run=body.extended_run)
        except ValueError as exc:
            yield sse("error", {"message": str(exc)})
            reset_harness_context(ctx_token)
            return
        except Exception as exc:
            logger.exception("failed to create agent")
            yield sse("error", {"message": str(exc)})
            reset_harness_context(ctx_token)
            return

        yield sse(
            "status",
            {
                "text": "Continue run…" if continue_run else "Agent ready — starting…",
                "phase": "init",
            },
        )

        incomplete = False
        try:
            async for chunk in stream_agent_events(
                agent,
                input_payload,
                config,
                wrapup_model=wrapup_model,
            ):
                if "event: done" in chunk and '"incomplete": true' in chunk:
                    incomplete = True
                yield chunk
        finally:
            if cfg is not None and not incomplete:
                await _maybe_summarize_last_turn(uid, thread_id, agent, config, cfg)
            reset_harness_context(ctx_token)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Thread-Id": thread_id,
        },
    )


@router.post("/resume")
async def chat_resume(body: ChatResumeRequest, user_id: str = Depends(get_user_id)):
    """Resume after a HITL interrupt with approve/reject decisions."""
    uid = user_id
    thread_id = body.thread_id
    if not thread_id:
        raise HTTPException(status_code=400, detail="thread_id required")

    meta = await load_threads_meta(uid)
    run_segment = int((meta.get(thread_id) or {}).get("run_segment") or 1)
    config = _thread_config(thread_id, run_segment=run_segment)

    if body.decisions:
        decisions = body.decisions
    else:
        decisions = [{"type": "approve"}]

    resume_value: Any = {"decisions": decisions}
    input_payload = Command(resume=resume_value)

    async def event_gen():
        from app.agent.streaming import sse

        ctx_token = set_harness_context(
            thread_id=thread_id,
            run_segment=run_segment,
            user_id=uid,
        )
        yield sse("meta", {"thread_id": thread_id, "user_id": uid, "resumed": True})
        yield sse("status", {"text": "Resuming after approval…", "phase": "init"})
        cfg = None
        wrapup_model = None
        try:
            cfg = await load_user_config(uid)
            wrapup_model = build_model(cfg)
            agent = await create_user_agent(uid, cfg)
        except ValueError as exc:
            yield sse("error", {"message": str(exc)})
            reset_harness_context(ctx_token)
            return
        except Exception as exc:
            logger.exception("failed to create agent for resume")
            yield sse("error", {"message": str(exc)})
            reset_harness_context(ctx_token)
            return

        try:
            async for chunk in stream_agent_events(
                agent,
                input_payload,
                config,
                wrapup_model=wrapup_model,
            ):
                yield chunk
        finally:
            reset_harness_context(ctx_token)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Thread-Id": thread_id,
        },
    )


@router.get("/threads")
async def list_threads(user_id: str = Depends(get_user_id)):
    """List chat threads for the current user's workspace."""
    return {"threads": await list_user_threads(user_id)}


@router.get("/threads/{thread_id}")
async def get_thread(thread_id: str, user_id: str = Depends(get_user_id)):
    try:
        meta = await load_threads_meta(user_id)
        entry = meta.get(thread_id) or {}
        run_segment = int(entry.get("run_segment") or 1)
        agent = await create_user_agent(user_id)
        state = await agent.aget_state(
            _thread_config(thread_id, run_segment=run_segment)
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    values = getattr(state, "values", {}) or {}
    raw_messages = values.get("messages") or []
    serialized = fold_checkpoint_messages(list(raw_messages))

    interrupts = []
    for task in getattr(state, "tasks", None) or []:
        for intr in getattr(task, "interrupts", None) or []:
            interrupts.append(
                {
                    "id": getattr(intr, "id", None),
                    "value": getattr(intr, "value", None),
                }
            )

    harness = load_harness_config()
    return {
        "thread_id": thread_id,
        "messages": serialized,
        "interrupts": interrupts,
        "next": list(getattr(state, "next", ()) or []),
        "turn_index": int(entry.get("turn_index") or 0),
        "turn_summaries": entry.get("turn_summaries") or [],
        "run_segment": run_segment,
        "context_stats": {
            "message_count": len(raw_messages),
            "folded_turns": len(serialized),
            "summarization_trigger_tokens": max(
                8_000,
                harness.default_max_input_tokens - harness.summarization_buffer_tokens,
            ),
        },
    }


@router.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str, user_id: str = Depends(get_user_id)):
    """Delete all checkpoints for a thread from the sqlite checkpointer."""
    try:
        saver = await get_checkpointer(user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    try:
        if hasattr(saver, "adelete_thread"):
            await saver.adelete_thread(thread_id)
        elif hasattr(saver, "delete_thread"):
            saver.delete_thread(thread_id)
        else:
            raise HTTPException(
                status_code=501,
                detail="Checkpointer does not support thread deletion",
            )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("failed to delete thread %s", thread_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    await delete_thread_meta(user_id, thread_id)
    return {"ok": True, "thread_id": thread_id}
