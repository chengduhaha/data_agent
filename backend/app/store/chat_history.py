"""Fold LangGraph checkpoint messages into UI-friendly chat turns."""

from __future__ import annotations

from typing import Any


def _message_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text" and block.get("text"):
                    parts.append(str(block["text"]))
                elif "text" in block and block["text"]:
                    parts.append(str(block["text"]))
            elif hasattr(block, "text") and getattr(block, "text"):
                parts.append(str(block.text))
        return "".join(parts).strip()
    return str(content).strip()


def _role_of(msg: Any) -> str:
    role = getattr(msg, "type", None) or getattr(msg, "role", None) or ""
    return str(role).lower()


def _tool_calls_of(msg: Any) -> list[dict[str, Any]]:
    raw = getattr(msg, "tool_calls", None) or []
    out: list[dict[str, Any]] = []
    for tc in raw:
        if isinstance(tc, dict):
            out.append(
                {
                    "id": str(tc.get("id") or ""),
                    "tool": str(tc.get("name") or tc.get("tool") or "tool"),
                    "input": tc.get("args") or tc.get("input"),
                    "status": "done",
                }
            )
        else:
            out.append(
                {
                    "id": str(getattr(tc, "id", "") or ""),
                    "tool": str(getattr(tc, "name", None) or "tool"),
                    "input": getattr(tc, "args", None),
                    "status": "done",
                }
            )
    return out


def fold_checkpoint_messages(messages: list[Any]) -> list[dict[str, Any]]:
    """Collapse LangGraph turns into user/assistant bubbles for the chat UI.

    Intermediate AIMessages that only contain tool_calls (empty text) are merged
    into the following assistant turn as Steps, so the sidebar does not show
    empty ``AGENT …`` placeholders.
    """
    folded: list[dict[str, Any]] = []
    pending_tools: list[dict[str, Any]] = []
    tool_outputs: dict[str, Any] = {}

    def flush_assistant(content: str, msg_id: Any = None) -> None:
        nonlocal pending_tools
        tools = list(pending_tools)
        for t in tools:
            tid = t.get("id")
            if tid and tid in tool_outputs:
                t["output"] = tool_outputs[tid]
        pending_tools = []
        if not content and not tools:
            return
        folded.append(
            {
                "id": msg_id,
                "role": "assistant",
                "content": content,
                "tools": tools or None,
            }
        )

    for msg in messages:
        role = _role_of(msg)
        msg_id = getattr(msg, "id", None)

        if role in ("human", "user"):
            # Flush any orphan tool steps before the next user turn.
            if pending_tools:
                flush_assistant("")
            text = _message_text(getattr(msg, "content", ""))
            if text:
                folded.append(
                    {
                        "id": msg_id,
                        "role": "user",
                        "content": text,
                    }
                )
            continue

        if role in ("tool",):
            tid = str(getattr(msg, "tool_call_id", None) or getattr(msg, "id", "") or "")
            output = getattr(msg, "content", None)
            if hasattr(output, "content"):
                output = output.content
            if tid:
                tool_outputs[tid] = output
            # Attach output onto the most recent pending tool with matching id.
            for t in reversed(pending_tools):
                if tid and t.get("id") == tid and "output" not in t:
                    t["output"] = output
                    break
            continue

        if role in ("ai", "assistant"):
            text = _message_text(getattr(msg, "content", ""))
            tools = _tool_calls_of(msg)
            if tools:
                pending_tools.extend(tools)
            if text:
                flush_assistant(text, msg_id)
            # tool-only AI turn: keep pending_tools for the next text turn
            continue

        # Ignore system / other roles for chat display.

    if pending_tools:
        flush_assistant("")

    return folded
