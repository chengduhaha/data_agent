#!/usr/bin/env python3
"""Quick live checks for harness SSE events (run with backend up)."""

from __future__ import annotations

import json
import sys
import urllib.request


def _parse_sse(raw: str) -> list[tuple[str, dict]]:
    events: list[tuple[str, dict]] = []
    event_name = "message"
    for line in raw.split("\n"):
        if line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            payload = line[5:].strip()
            if payload:
                events.append((event_name, json.loads(payload)))
            event_name = "message"
    return events


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    print(f"==> health {base}/health")
    with urllib.request.urlopen(f"{base}/health", timeout=10) as resp:
        print(resp.read().decode())

    print(f"==> threads {base}/api/chat/threads")
    with urllib.request.urlopen(f"{base}/api/chat/threads", timeout=10) as resp:
        print(resp.read().decode()[:500])

    print(f"==> chat stream (expect budget + error without model config)")
    req = urllib.request.Request(
        f"{base}/api/chat/stream",
        data=json.dumps({"message": "ping harness test"}).encode(),
        headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode()
    events = _parse_sse(body)
    names = [e[0] for e in events]
    print("events:", names)
    assert "meta" in names, "missing meta"
    if "budget" in names:
        print("OK: budget SSE present")
    elif "error" in names:
        print("note: budget skipped — agent failed before run (configure model in Settings)")
    else:
        assert "budget" in names, "missing budget SSE (harness)"
    if "continue_prompt" in names:
        print("OK: continue_prompt present")
    if "wrapup_done" in names:
        print("OK: wrapup_done present")
    if "token" in names:
        print("OK: token stream present")
    if "error" in names:
        err = next(d for n, d in events if n == "error")
        print("error (expected without model):", err.get("message", "")[:120])
    print("PASS: harness live smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
