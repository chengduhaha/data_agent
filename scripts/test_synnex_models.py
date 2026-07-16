#!/usr/bin/env python3
"""Smoke-test every Synnex catalog model via build_model()."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(ROOT))

from app.agent.model_catalog import list_profiles  # noqa: E402
from app.agent.models import build_model  # noqa: E402
from app.store.schemas import ModelConfig  # noqa: E402


def test_one(model_id: str) -> tuple[bool, str]:
    cfg = ModelConfig(provider="synnex", model=model_id, temperature=0.1, max_tokens=8192)
    try:
        llm = build_model(cfg)
        # Non-streaming invoke for a crisp pass/fail
        msg = llm.invoke("Reply with exactly: OK")
        text = getattr(msg, "content", None) or str(msg)
        if isinstance(text, list):
            text = "".join(
                (c.get("text") if isinstance(c, dict) else getattr(c, "text", str(c))) for c in text
            )
        text = (text or "").strip()
        preview = text[:200].replace("\n", " ")
        return True, preview or "(empty content)"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main() -> int:
    results = []
    for p in list_profiles():
        print(f"=== Testing {p.id} ({p.provider_type}) ===", flush=True)
        print(f"  base={p.api_base}", flush=True)
        ok, detail = test_one(p.id)
        status = "PASS" if ok else "FAIL"
        print(f"  {status}: {detail}\n", flush=True)
        results.append((p.id, ok, detail))

    print("\n=== SUMMARY ===")
    for mid, ok, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}\t{mid}\t{detail[:120]}")
    failed = sum(1 for _, ok, _ in results if not ok)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
