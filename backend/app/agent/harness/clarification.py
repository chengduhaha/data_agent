"""User clarification tool — pauses the agent until the user responds."""

from __future__ import annotations

import json
from typing import Any, Literal

from langchain_core.tools import StructuredTool
from langgraph.types import interrupt
from pydantic import BaseModel, Field


class ClarificationOption(BaseModel):
    label: str = Field(description="Short option label shown to the user.")
    description: str = Field(
        default="",
        description="Optional one-line hint about this choice.",
    )


class ClarificationQuestion(BaseModel):
    question: str = Field(description="Clear question ending with ? when possible.")
    header: str = Field(
        default="",
        description="Very short chip label, e.g. 'Time range'.",
    )
    options: list[ClarificationOption] = Field(
        default_factory=list,
        description="2–6 choices for single/multi select. Omit for free-text only.",
    )
    multi_select: bool = Field(
        default=False,
        description="Allow multiple options when choices are not mutually exclusive.",
    )
    allow_free_text: bool = Field(
        default=True,
        description="Show a text box (always available when options are omitted).",
    )


class AskUserInput(BaseModel):
    questions: list[ClarificationQuestion] = Field(
        min_length=1,
        max_length=3,
        description="One focused clarification block. Prefer a single question.",
    )
    reason: str = Field(
        default="",
        description="One sentence on why clarification is required before proceeding.",
    )


def _normalize_questions(raw: list[ClarificationQuestion]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for q in raw:
        options = [
            {"label": o.label.strip(), "description": (o.description or "").strip()}
            for o in (q.options or [])
            if o.label.strip()
        ]
        out.append(
            {
                "question": q.question.strip(),
                "header": (q.header or q.question[:32]).strip(),
                "options": options,
                "multi_select": bool(q.multi_select),
                "allow_free_text": bool(q.allow_free_text),
            }
        )
    return out


def is_clarification_interrupt(value: Any) -> bool:
    if isinstance(value, dict) and value.get("type") == "clarification":
        return True
    if isinstance(value, list):
        return any(is_clarification_interrupt(item) for item in value)
    return False


def extract_clarification_payload(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        if value.get("type") == "clarification":
            return value
        nested = value.get("value")
        if nested is not value:
            found = extract_clarification_payload(nested)
            if found is not None:
                return found
    if isinstance(value, list):
        for item in value:
            found = extract_clarification_payload(item)
            if found is not None:
                return found
    return None


def make_ask_user_tool() -> StructuredTool:
    async def _run(
        questions: list[ClarificationQuestion],
        reason: str = "",
    ) -> str:
        payload = {
            "type": "clarification",
            "reason": (reason or "").strip(),
            "questions": _normalize_questions(questions),
        }
        if not payload["questions"]:
            return json.dumps({"ok": False, "error": "At least one question is required."})

        resume_value = interrupt(payload)
        if isinstance(resume_value, str):
            try:
                resume_value = json.loads(resume_value)
            except Exception:
                resume_value = {"answers": {"": resume_value}}
        if not isinstance(resume_value, dict):
            resume_value = {"answers": resume_value}

        answers = resume_value.get("answers")
        if not isinstance(answers, dict):
            answers = {"": str(resume_value)}

        return json.dumps(
            {
                "ok": True,
                "answers": answers,
                "note": "Continue with the user's choices; do not re-ask unless still blocked.",
            },
            ensure_ascii=False,
        )

    return StructuredTool.from_function(
        coroutine=_run,
        name="ask_user",
        description=(
            "Ask the user a focused clarification question before proceeding. "
            "Use only when ambiguity blocks routing or analysis (time range, entity, "
            "metric sense, grouping). Provide 2–4 options when helpful; otherwise ask "
            "for free text. Do not over-ask — proceed when the question is clear enough."
        ),
        args_schema=AskUserInput,
    )


CLARIFICATION_RESUME_KIND: Literal["clarification"] = "clarification"
