"""Generic request-constraint extraction and answer completeness checks.

No business vocabulary or domain-specific rules — only dates, counts, sort
direction, evidence presence, and obvious planning-only answers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.agent.harness.wrapup import (
    looks_like_substantial_answer,
    looks_truncated,
    messages_for_current_turn,
)

_DATE_PATTERNS = (
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"\b(\d{4}/\d{2}/\d{2})\b"),
    re.compile(r"\b(\d{4}\.\d{2}\.\d{2})\b"),
)

_TOP_N_PATTERNS = (
    re.compile(r"(?:top|first)\s+(\d+)", re.I),
    re.compile(r"\blist\s+(?:top\s+)?(\d+)", re.I),
    re.compile(r"\b(\d+)\s+items?\b", re.I),
    re.compile(r"\btop\s*(\d+)\b", re.I),
)

_SORT_DESC = re.compile(
    r"\b(?:descending|desc|largest|highest|most\s+negative|biggest|top\s+by)\b",
    re.I,
)
_SORT_ASC = re.compile(
    r"\b(?:ascending|asc|smallest|lowest|least|bottom\s+by)\b",
    re.I,
)

_PLANNING_MARKERS = (
    re.compile(r"\blet me\b", re.I),
    re.compile(r"\bi(?:'ll| will)\b", re.I),
    re.compile(r"\bnow (?:let me|i)\b", re.I),
    re.compile(r"\bnext,? i\b", re.I),
    re.compile(r"\bchecking\b", re.I),
    re.compile(r"\brunning (?:a )?query\b", re.I),
)


@dataclass
class RequestConstraints:
    """Generic form constraints parsed from the user message."""

    dates: list[str] = field(default_factory=list)
    top_n: int | None = None
    sort_direction: str | None = None  # "asc" | "desc"
    requested_phrases: list[str] = field(default_factory=list)
    language_hint: str | None = None


@dataclass
class CompletenessReport:
    complete: bool
    missing_constraints: list[str] = field(default_factory=list)
    evidence_present: bool = False
    needs_followup: bool = False
    reason: str = ""


def _cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    return cjk / max(len(text), 1)


def extract_constraints(user_message: str) -> RequestConstraints:
    """Extract generic constraints from the user's question text."""
    text = (user_message or "").strip()
    if not text:
        return RequestConstraints()

    dates: list[str] = []
    for pat in _DATE_PATTERNS:
        for m in pat.finditer(text):
            d = m.group(1).replace("/", "-").replace(".", "-")
            if d not in dates:
                dates.append(d)

    top_n: int | None = None
    for pat in _TOP_N_PATTERNS:
        m = pat.search(text)
        if m:
            try:
                n = int(m.group(1))
                if 1 <= n <= 500:
                    top_n = n
                    break
            except (ValueError, IndexError):
                continue

    sort_direction: str | None = None
    if _SORT_DESC.search(text):
        sort_direction = "desc"
    elif _SORT_ASC.search(text):
        sort_direction = "asc"

    language_hint: str | None = None
    if _cjk_ratio(text) >= 0.15:
        language_hint = "zh"
    elif re.search(r"[a-zA-Z]", text):
        language_hint = "en"

    requested_phrases: list[str] = []
    for pat in (
        re.compile(r"\binclude\s+([a-z][a-z0-9_]{2,30})\b", re.I),
        re.compile(r"\bwith\s+([a-z][a-z0-9_]{2,30})\b", re.I),
    ):
        for m in pat.finditer(text):
            phrase = m.group(1).strip().lower()
            if phrase and phrase not in requested_phrases:
                requested_phrases.append(phrase)

    return RequestConstraints(
        dates=dates,
        top_n=top_n,
        sort_direction=sort_direction,
        requested_phrases=requested_phrases[:6],
        language_hint=language_hint,
    )


def _count_result_rows(answer: str) -> int:
    """Count identifiable result rows in tables or numbered lists."""
    text = (answer or "").strip()
    if not text:
        return 0

    table_rows = 0
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or "|" not in stripped:
            in_table = False
            continue
        if re.match(r"^\|?\s*:?-{2,}", stripped):
            in_table = True
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) >= 2 and any(cells):
            if in_table or stripped.startswith("|"):
                table_rows += 1
                in_table = True

    numbered = len(re.findall(r"(?:^|\n)\s*\d+\.\s+\S", text))

    # Some models emit tab-separated tables instead of Markdown tables. Count
    # rows only when the first field is numeric-like, so prose with tabs is not
    # mistaken for result data.
    tabular = 0
    for line in text.splitlines():
        fields = [field.strip() for field in line.split("\t")]
        if len(fields) >= 2 and re.match(r"^-?\d[\d,]*$", fields[0]):
            tabular += 1

    return max(table_rows, numbered, tabular)


def _answer_contains_date(answer: str, date_str: str) -> bool:
    a = (answer or "").lower()
    variants = {date_str.lower(), date_str.replace("-", "/"), date_str.replace("-", ".")}
    return any(v in a for v in variants)


def _parse_table_numeric_column(answer: str) -> list[float] | None:
    """Try to parse the last numeric column from a markdown table."""
    rows: list[list[str]] = []
    for line in (answer or "").splitlines():
        stripped = line.strip()
        if "|" not in stripped or re.match(r"^\|?\s*:?-{2,}", stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) >= 2:
            rows.append(cells)

    if len(rows) < 2:
        return None

    nums: list[float] = []
    for row in rows:
        last = row[-1]
        cleaned = re.sub(r"[^\d.\-]", "", last.replace(",", ""))
        if not cleaned:
            continue
        try:
            nums.append(float(cleaned))
        except ValueError:
            continue

    return nums if len(nums) >= 2 else None


def _sort_violation(nums: list[float], direction: str) -> bool:
    if len(nums) < 2:
        return False
    if direction == "desc":
        violations = sum(1 for i in range(len(nums) - 1) if nums[i] < nums[i + 1])
    else:
        violations = sum(1 for i in range(len(nums) - 1) if nums[i] > nums[i + 1])
    return violations > max(1, len(nums) // 3)


def _looks_planning_only(answer: str) -> bool:
    t = (answer or "").strip()
    if not t:
        return True
    if looks_like_substantial_answer(t):
        return False
    if len(t) < 80 and any(p.search(t) for p in _PLANNING_MARKERS):
        return True
    markers = sum(1 for p in _PLANNING_MARKERS if p.search(t))
    if markers >= 2 and not re.search(r"\|.*\|", t):
        return True
    lower = t.lower()
    if lower.startswith(("let me ", "i'll ", "i will ", "now let me ")):
        return True
    return False


def assess_completeness(
    user_message: str,
    answer: str,
    *,
    query_count: int = 0,
    research_tool_count: int = 0,
    tool_error: bool = False,
) -> CompletenessReport:
    """Return a structured completeness report for the current answer."""
    combined = (answer or "").strip()
    constraints = extract_constraints(user_message)
    evidence_present = query_count > 0 or research_tool_count > 0

    if tool_error and not combined:
        return CompletenessReport(
            complete=False,
            missing_constraints=["answer"],
            evidence_present=evidence_present,
            needs_followup=False,
            reason="tool_error_without_answer",
        )

    if not evidence_present:
        if combined and looks_like_substantial_answer(combined):
            return CompletenessReport(
                complete=True,
                evidence_present=False,
                reason="no_evidence_but_substantial_text",
            )
        return CompletenessReport(
            complete=bool(combined) and not _looks_planning_only(combined),
            evidence_present=False,
            needs_followup=False,
            reason="no_evidence",
        )

    missing: list[str] = []

    if _looks_planning_only(combined):
        missing.append("final_answer_not_planning")

    if looks_truncated(combined):
        missing.append("truncated_answer")

    for d in constraints.dates:
        if not _answer_contains_date(combined, d):
            missing.append(f"date:{d}")

    if constraints.top_n is not None:
        row_count = _count_result_rows(combined)
        if row_count < constraints.top_n:
            missing.append(f"top_n:{constraints.top_n} (found {row_count})")

    if constraints.sort_direction and combined:
        nums = _parse_table_numeric_column(combined)
        if nums is None:
            missing.append(f"sort:{constraints.sort_direction}:unknown")
        elif _sort_violation(nums, constraints.sort_direction):
            missing.append(f"sort:{constraints.sort_direction}:violation")

    for phrase in constraints.requested_phrases:
        if phrase not in combined.lower():
            missing.append(f"phrase:{phrase}")

    # Drop sort:unknown from blocking completeness when other checks pass
    blocking_missing = [
        m
        for m in missing
        if not m.startswith("sort:") or m.endswith(":violation")
    ]

    complete = (
        bool(combined)
        and not _looks_planning_only(combined)
        and not looks_truncated(combined)
        and not blocking_missing
        and looks_like_substantial_answer(combined)
    )

    needs_followup = (
        evidence_present
        and not complete
        and bool(blocking_missing or _looks_planning_only(combined) or looks_truncated(combined))
    )

    reason = "complete" if complete else ("incomplete:" + ",".join(missing[:5]) if missing else "incomplete")

    return CompletenessReport(
        complete=complete,
        missing_constraints=missing,
        evidence_present=evidence_present,
        needs_followup=needs_followup,
        reason=reason,
    )


def last_human_text(messages: list[Any]) -> str:
    """Latest user/human message text from checkpoint messages."""
    scoped = messages_for_current_turn(list(messages))
    for msg in reversed(scoped):
        role = getattr(msg, "type", None) or getattr(msg, "role", "")
        if str(role).lower() not in ("human", "user"):
            continue
        content = getattr(msg, "content", "")
        if isinstance(content, str) and content.strip():
            return content.strip()
        if isinstance(content, list):
            parts = [
                str(b.get("text", ""))
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
            text = "".join(parts).strip()
            if text:
                return text
    return ""


def build_finalization_human(
    report: CompletenessReport,
    constraints: RequestConstraints,
    *,
    draft_answer: str,
) -> str:
    """Human prompt for a single bounded finalization pass."""
    gaps = "\n".join(f"- {m}" for m in report.missing_constraints) or "- incomplete coverage"
    constraint_lines: list[str] = []
    if constraints.dates:
        constraint_lines.append(f"Dates requested: {', '.join(constraints.dates)}")
    if constraints.top_n is not None:
        constraint_lines.append(f"Requested count: top/first {constraints.top_n}")
    if constraints.sort_direction:
        constraint_lines.append(f"Sort direction: {constraints.sort_direction}")
    constraint_block = "\n".join(constraint_lines) or "(no explicit numeric constraints detected)"

    draft = (draft_answer or "").strip()
    draft_preview = draft[:12000] + ("…" if len(draft) > 12000 else "")

    return (
        "The agent run finished but the answer may not fully satisfy the user's request.\n"
        "Produce ONE final user-facing answer that fixes only the gaps below.\n\n"
        f"### Detected gaps\n{gaps}\n\n"
        f"### Request constraints\n{constraint_block}\n\n"
        f"### Current draft answer\n{draft_preview}\n\n"
        "Revise or extend the draft so it satisfies every explicit constraint. "
        "Use only evidence already in the transcript — do not invent numbers. "
        "When the evidence contains N returned rows and the user requested top N, "
        "preserve all N rows in the final answer; do not summarize or omit rows."
    )
