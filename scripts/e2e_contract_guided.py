#!/usr/bin/env python3
"""Contract-guided E2E harness — POST :6641/api/chat/stream and score answers."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

BASE = "http://127.0.0.1:6641"
USER = "local"
TIMEOUT_S = 600


@dataclass
class RunResult:
    qid: str
    thread_id: str | None = None
    answer: str = ""
    sqls: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    passed: bool = False
    notes: list[str] = field(default_factory=list)


QUESTIONS = {
    "Q1": (
        "Using contract-guided data analysis: show Customer NGM month-over-month "
        "Top 10 comparing March 2026 vs April 2026, where March NGM > $1000."
    ),
    "Q2": (
        "Using contract-guided data analysis: for vendor #13208 in April 2026, "
        "show P&L items in NGM with MoM% and YoY%."
    ),
    "Q3": (
        "Using contract-guided data analysis: company-wide top 5 P&L items by "
        "absolute NGM MoM variance comparing April 2026 vs March 2026."
    ),
}


def _parse_sse(raw: str) -> list[tuple[str, dict[str, Any]]]:
    events: list[tuple[str, dict[str, Any]]] = []
    buf_event: str | None = None
    buf_data: list[str] = []
    for line in raw.splitlines():
        if line.startswith("event:"):
            buf_event = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            buf_data.append(line.split(":", 1)[1].strip())
        elif line == "" and buf_event is not None:
            data_str = "\n".join(buf_data)
            try:
                data = json.loads(data_str) if data_str else {}
            except json.JSONDecodeError:
                data = {"raw": data_str}
            events.append((buf_event, data))
            buf_event = None
            buf_data = []
    return events


def run_question(qid: str, message: str) -> RunResult:
    url = f"{BASE}/api/chat/stream?user_id={USER}"
    body = json.dumps({"message": message, "user_id": USER}).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    result = RunResult(qid=qid)
    chunks: list[str] = []
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            while True:
                line = resp.readline()
                if not line:
                    break
                chunks.append(line.decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        result.errors.append(f"HTTP {e.code}: {e.read().decode()[:500]}")
        return result
    except Exception as e:
        result.errors.append(str(e))
        return result

    text = "".join(chunks)
    events = _parse_sse(text)
    tokens: list[str] = []
    for ev, data in events:
        if ev == "meta":
            result.thread_id = data.get("thread_id")
        elif ev == "token":
            tokens.append(data.get("text") or "")
        elif ev == "tool_start":
            tool = data.get("tool") or ""
            inp = data.get("input")
            if tool == "run_query_safely" and isinstance(inp, dict):
                q = inp.get("query") or inp.get("sql")
                if q:
                    result.sqls.append(str(q))
        elif ev == "error":
            result.errors.append(data.get("message") or str(data))
    result.answer = "".join(tokens)
    return result


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower())


def score_q1(r: RunResult) -> None:
    a = _norm(r.answer)
    sql = _norm(" ".join(r.sqls))
    if "771932" in a or "771932" in sql:
        r.notes.append("cust_no 771932 present")
    if re.search(r"2023|2,?023", a):
        r.notes.append("MoM ~-2023% present")
    if "dws_disty_brpt_cust_mtd" in sql:
        r.notes.append("uses cust_mtd")
    if "dim_pub_date" in sql:
        r.notes.append("uses dim_pub_date")
    if "group by" in sql and "cust_no" in sql:
        r.notes.append("GROUP BY cust_no")
    if "month_flag" in sql and "'y'" in sql:
        r.notes.append("FAIL: month_flag=Y")
    r.passed = (
        ("771932" in a or "771932" in sql)
        and "dws_disty_brpt_cust_mtd" in sql
        and "group by" in sql
        and "cust_no" in sql
        and "month_flag" not in sql
    )


def score_q2(r: RunResult) -> None:
    a = _norm(r.answer)
    sql = _norm(" ".join(r.sqls))
    if re.search(r"7[,.]?0{3}[,.]?395|7040395", a.replace(",", "")):
        r.notes.append("ngm_apr ~7.04M")
    if "1.35" in a:
        r.notes.append("MoM +1.35%")
    if "12.84" in a:
        r.notes.append("YoY -12.84%")
    comps = ["gm_amt", "btl", "ap_finance", "cust_rebate"]
    comp_hits = sum(1 for c in comps if c in a or c in sql)
    if comp_hits >= 2:
        r.notes.append(f"P&L components mentioned ({comp_hits})")
    if "dws_disty_brpt_vend_mtd" in sql:
        r.notes.append("uses vend_mtd")
    if "group by" in sql and "vend_no" in sql:
        r.notes.append("GROUP BY vend_no")
    if "pl_item" in sql:
        r.notes.append("FAIL: pl_item in SQL")
    if "union all" in sql:
        r.notes.append("WARN: UNION ALL in SQL")
    r.passed = (
        "dws_disty_brpt_vend_mtd" in sql
        and "13208" in sql
        and comp_hits >= 2
        and "pl_item" not in sql
        and ("7,040,395" in a or "7040395" in a.replace(",", "").replace(".", ""))
    )


def score_q3(r: RunResult) -> None:
    a = _norm(r.answer)
    sql = _norm(" ".join(r.sqls))
    top_items = ["ap_finance", "cust_rebate", "one_time_btl", "gm_amt", "cust_finance"]
    hits = [c for c in top_items if c in a or c in sql]
    if len(hits) >= 3:
        r.notes.append(f"top P&L items ({len(hits)}): {', '.join(hits)}")
    if re.search(r"91[,.]?2|91200000|91\.22", a.replace(",", "")):
        r.notes.append("NGM Mar ~91.22M")
    if re.search(r"88[,.]?6|88600000|88\.60", a.replace(",", "")):
        r.notes.append("NGM Apr ~88.60M")
    if "dws_disty_brpt_pl_extend_mtd" in sql:
        r.notes.append("uses pl_extend_mtd")
    if "pl_item" in sql:
        r.notes.append("FAIL: pl_item in SQL")
    r.passed = (
        "dws_disty_brpt_pl_extend_mtd" in sql
        and len(hits) >= 3
        and "pl_item" not in sql
    )


SCORERS = {"Q1": score_q1, "Q2": score_q2, "Q3": score_q3}


def main() -> int:
    qids = sys.argv[1:] if len(sys.argv) > 1 else list(QUESTIONS)
    results: list[RunResult] = []
    for qid in qids:
        if qid not in QUESTIONS:
            print(f"Unknown question {qid}", file=sys.stderr)
            continue
        print(f"\n{'='*60}\nRunning {qid}…", flush=True)
        t0 = time.time()
        r = run_question(qid, QUESTIONS[qid])
        SCORERS[qid](r)
        elapsed = time.time() - t0
        status = "PASS" if r.passed else "FAIL"
        print(f"{qid} {status} ({elapsed:.0f}s) thread={r.thread_id}")
        if r.errors:
            print("  errors:", "; ".join(r.errors[:3]))
        if r.notes:
            print("  notes:", "; ".join(r.notes))
        if r.sqls:
            print(f"  sql_count={len(r.sqls)} last_sql_preview={r.sqls[-1][:200]}…")
        results.append(r)

    print(f"\n{'='*60}\nSUMMARY")
    passed = sum(1 for r in results if r.passed)
    for r in results:
        print(f"  {'PASS' if r.passed else 'FAIL'}\t{r.qid}\tthread={r.thread_id}")
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
