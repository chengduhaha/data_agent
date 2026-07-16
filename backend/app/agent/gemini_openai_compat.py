"""OpenAI-compatible Synnex Gemini gateway: round-trip thought_signature on tool calls.

Gemini 3 models accessed via the OpenAI chat-completions shim return
``extra_content.google.thought_signature`` on assistant ``tool_calls``. LangChain
and LangGraph often drop ``additional_kwargs`` when persisting streamed assistant
messages, which causes HTTP 400 on follow-up turns after tool execution.

We cache raw tool_call payloads by ``id`` on every model response and re-attach
them on outbound requests when missing.
"""

from __future__ import annotations

import copy
import logging
import threading
from typing import Any

from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage
from langchain_core.outputs import ChatGenerationChunk
from langchain_openai import ChatOpenAI

_lock = threading.Lock()
logger = logging.getLogger(__name__)
# tool_call_id -> raw OpenAI tool_call dict (includes extra_content.google.thought_signature)
_TOOL_CALL_CACHE: dict[str, dict[str, Any]] = {}


def _is_gemini_model(model_name: str) -> bool:
    return "gemini" in (model_name or "").lower()


def _has_thought_signature(tc: dict[str, Any]) -> bool:
    if tc.get("thought_signature"):
        return True
    extra = tc.get("extra_content") or {}
    google = extra.get("google") or {}
    return bool(google.get("thought_signature"))


def _cache_tool_calls(tool_calls: list[dict[str, Any]] | None) -> None:
    if not tool_calls:
        return
    with _lock:
        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            tid = tc.get("id")
            if tid and _has_thought_signature(tc):
                _TOOL_CALL_CACHE[tid] = copy.deepcopy(tc)


def _lookup_tool_call(tid: str | None) -> dict[str, Any] | None:
    if not tid:
        return None
    with _lock:
        cached = _TOOL_CALL_CACHE.get(tid)
        return copy.deepcopy(cached) if cached else None


def _raw_tool_calls_from_message(message_dict: dict[str, Any]) -> list[dict[str, Any]] | None:
    raw = message_dict.get("tool_calls")
    if not raw or not isinstance(raw, list):
        return None
    out = [copy.deepcopy(tc) for tc in raw if isinstance(tc, dict)]
    _cache_tool_calls(out)
    return out or None


def _merge_tool_call_extras(
    outbound: list[dict[str, Any]], stored: list[dict[str, Any]] | None
) -> list[dict[str, Any]]:
    if not outbound:
        return outbound
    by_id: dict[str, dict[str, Any]] = {}
    if stored:
        by_id = {
            tc.get("id"): tc for tc in stored if isinstance(tc, dict) and tc.get("id")
        }
    merged: list[dict[str, Any]] = []
    for i, tc in enumerate(outbound):
        out = dict(tc)
        tid = out.get("id")
        src = by_id.get(tid)
        if src is None:
            src = _lookup_tool_call(tid)
            if src is None and tid and not _has_thought_signature(out):
                logger.debug(
                    "gemini thought_signature cache miss for tool_call id=%s (cache_size=%d)",
                    tid,
                    len(_TOOL_CALL_CACHE),
                )
        if src is None and stored and i < len(stored) and isinstance(stored[i], dict):
            src = stored[i]
        if src:
            for key, val in src.items():
                if key not in ("id", "type", "function") and key not in out:
                    out[key] = val
        merged.append(out)
    return merged


def _patch_outbound_messages(
    payload_messages: list[dict[str, Any]], source_messages: list[BaseMessage]
) -> None:
    """Re-inject provider tool_call extras from message state or global cache."""
    src_ai = [m for m in source_messages if isinstance(m, AIMessage)]
    ai_idx = 0
    for out in payload_messages:
        if out.get("role") != "assistant":
            continue
        src = src_ai[ai_idx] if ai_idx < len(src_ai) else None
        ai_idx += 1
        if not out.get("tool_calls"):
            continue
        stored = None
        if src is not None:
            stored = (src.additional_kwargs or {}).get("tool_calls")
        out["tool_calls"] = _merge_tool_call_extras(out["tool_calls"], stored)


class GeminiThoughtSignatureChatOpenAI(ChatOpenAI):
    """ChatOpenAI subclass that preserves Gemini thought_signature across tool turns."""

    def _create_chat_result(self, response, generation_info=None):  # type: ignore[no-untyped-def]
        result = super()._create_chat_result(response, generation_info)
        if not _is_gemini_model(self.model_name):
            return result

        response_dict = (
            response
            if isinstance(response, dict)
            else response.model_dump(warnings=False)
        )
        choices = response_dict.get("choices") or []
        for i, gen in enumerate(result.generations):
            if i >= len(choices):
                break
            msg = gen.message
            if not isinstance(msg, AIMessage):
                continue
            raw_msg = choices[i].get("message") or {}
            stored = _raw_tool_calls_from_message(raw_msg)
            if stored:
                ak = dict(msg.additional_kwargs or {})
                ak["tool_calls"] = stored
                msg.additional_kwargs = ak
        return result

    def _get_request_payload(self, input_, *, stop=None, **kwargs):  # type: ignore[no-untyped-def]
        source_messages = self._convert_input(input_).to_messages()
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        if not _is_gemini_model(self.model_name):
            return payload
        messages = payload.get("messages")
        if isinstance(messages, list):
            _patch_outbound_messages(messages, source_messages)
        return payload

    def _convert_chunk_to_generation_chunk(  # type: ignore[no-untyped-def]
        self,
        chunk: dict,
        default_chunk_class: type,
        base_generation_info: dict | None,
    ) -> ChatGenerationChunk | None:
        gen_chunk = super()._convert_chunk_to_generation_chunk(
            chunk, default_chunk_class, base_generation_info
        )
        if (
            gen_chunk is None
            or not _is_gemini_model(self.model_name)
            or not isinstance(gen_chunk.message, AIMessageChunk)
        ):
            return gen_chunk

        choices = chunk.get("choices") or chunk.get("chunk", {}).get("choices") or []
        if not choices:
            return gen_chunk
        delta = choices[0].get("delta") or {}
        stored = _raw_tool_calls_from_message(delta)
        if stored:
            ak = dict(gen_chunk.message.additional_kwargs or {})
            prev = ak.get("tool_calls") or []
            ak["tool_calls"] = _merge_tool_call_extras(stored, prev)
            gen_chunk.message.additional_kwargs = ak
        return gen_chunk


def clear_tool_call_cache() -> None:
    """Test helper — reset cached Gemini tool_call signatures."""
    with _lock:
        _TOOL_CALL_CACHE.clear()
