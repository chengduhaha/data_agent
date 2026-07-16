"""Thread listing: merge per-user threads_meta with LangGraph checkpointer."""

from __future__ import annotations

import logging
from typing import Any

from app.store.io import load_threads_meta

logger = logging.getLogger(__name__)


def _thread_row(
    thread_id: str,
    entry: dict[str, Any] | None = None,
    *,
    checkpoint_ts: Any = None,
) -> dict[str, Any]:
    entry = entry or {}
    updated = entry.get("updated_at") or checkpoint_ts
    return {
        "thread_id": thread_id,
        "title": entry.get("title") or f"{thread_id[:8]}…",
        "updated_at": updated,
        "created_at": entry.get("created_at"),
    }


async def list_user_threads(user_id: str) -> list[dict[str, Any]]:
    """List chat threads for sidebar — meta is primary, checkpointer enriches."""
    meta = await load_threads_meta(user_id)
    by_id: dict[str, dict[str, Any]] = {
        tid: _thread_row(tid, entry) for tid, entry in meta.items()
    }

    try:
        from app.agent.factory import get_checkpointer

        saver = await get_checkpointer(user_id)
        seen: set[str] = set()
        if hasattr(saver, "alist"):
            async for item in saver.alist(None, limit=200):  # type: ignore[arg-type]
                cfg = getattr(item, "config", None) or {}
                tid = (cfg.get("configurable") or {}).get("thread_id")
                if not tid or tid in seen:
                    continue
                seen.add(tid)
                entry = meta.get(tid) or {}
                checkpoint_ts = getattr(item, "ts", None)
                if tid in by_id:
                    row = by_id[tid]
                    if not row.get("updated_at") and checkpoint_ts:
                        row["updated_at"] = checkpoint_ts
                else:
                    by_id[tid] = _thread_row(tid, entry, checkpoint_ts=checkpoint_ts)
        elif hasattr(saver, "list"):
            for item in saver.list(None, limit=200):  # type: ignore[arg-type]
                cfg = getattr(item, "config", None) or {}
                tid = (cfg.get("configurable") or {}).get("thread_id")
                if not tid or tid in by_id:
                    continue
                entry = meta.get(tid) or {}
                by_id[tid] = _thread_row(tid, entry)
    except Exception:
        logger.debug("checkpointer thread listing failed", exc_info=True)

    threads = list(by_id.values())
    threads.sort(
        key=lambda t: str(t.get("updated_at") or t.get("created_at") or ""),
        reverse=True,
    )
    return threads
