"""Lightweight new-topic detection for multi-question threads."""

from __future__ import annotations

import re
from typing import Any


_FOLLOWUP_MARKERS = (
    "继续",
    "接着",
    "同上",
    "刚才",
    "上面",
    "之前",
    "that",
    "same",
    "continue",
    "follow up",
    "follow-up",
    "also",
    "what about",
    "how about",
)


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[\w\u4e00-\u9fff]{2,}", text.lower())
    return set(words)


def detect_topic_relation(
    new_message: str,
    previous_question: str | None,
    *,
    previous_summary: str | None = None,
) -> dict[str, Any]:
    """Classify whether a new user message is a follow-up or a new topic."""
    msg = (new_message or "").strip()
    if not msg:
        return {"relation": "empty", "suggest_new_thread": False}
    if not previous_question and not previous_summary:
        return {"relation": "first", "suggest_new_thread": False}

    lower = msg.lower()
    for marker in _FOLLOWUP_MARKERS:
        if marker in lower:
            return {"relation": "followup", "suggest_new_thread": False}

    prev = (previous_question or "").strip()
    if prev:
        overlap = len(_tokens(msg) & _tokens(prev))
        union = len(_tokens(msg) | _tokens(prev)) or 1
        jaccard = overlap / union
        if jaccard >= 0.25:
            return {"relation": "followup", "suggest_new_thread": False, "score": jaccard}
        if jaccard < 0.08 and len(msg) > 20:
            return {
                "relation": "new_topic",
                "suggest_new_thread": True,
                "score": jaccard,
                "message": (
                    "This looks like a new topic in the same chat. "
                    "For best results, start a new thread — or continue here with narrower scope."
                ),
            }

    return {"relation": "unknown", "suggest_new_thread": False}
