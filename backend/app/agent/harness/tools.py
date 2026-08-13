"""Harness builtin tools: knowledge search and WKB query."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from contextlib import contextmanager
from typing import Any, Literal

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field

from app.store.paths import ORG_KNOWLEDGE_DIR


class SearchKnowledgeInput(BaseModel):
    pattern: str = Field(description="Literal text pattern to search for.")
    path_prefix: str = Field(
        default="/knowledge/org",
        description="Virtual path prefix to search under (/knowledge/org or /workspace).",
    )
    glob: str | None = Field(
        default=None,
        description="Optional glob filter, e.g. '*.md' or '*.json'.",
    )
    output_mode: Literal["content", "files_with_matches"] = Field(
        default="content",
        description="Return matching lines or file paths only.",
    )
    head_limit: int = Field(default=40, ge=1, le=200, description="Max matches to return.")


class WkbQueryInput(BaseModel):
    query: str = Field(description="Metric/entity/table cue for WKB retrieval.")
    intent: Literal["nl2sql_metric", "find_table_schema", "data_engineering"] = Field(
        default="nl2sql_metric",
        description="WKB intent (contract-guided analysis only).",
    )
    prefilter_k: int = Field(default=200, ge=1, le=500)
    per_layer_k: int = Field(default=8, ge=1, le=20)


@contextmanager
def _wkb_cwd():
    root = ORG_KNOWLEDGE_DIR.resolve()
    if not root.exists():
        raise FileNotFoundError(f"Org knowledge root missing: {root}")
    prev = os.getcwd()
    path_added = False
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
        path_added = True
    try:
        os.chdir(root_str)
        yield
    finally:
        os.chdir(prev)
        if path_added:
            try:
                sys.path.remove(root_str)
            except ValueError:
                pass


def _truncate_text(text: str, limit: int = 12000) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit] + "\n…[truncated]", True


async def _backend_grep(
    backend: Any,
    pattern: str,
    path_prefix: str,
    glob: str | None,
    output_mode: Literal["content", "files_with_matches"],
) -> str:
    """Call backend grep/agrep with signature-compatible kwargs."""
    grep_fn = getattr(backend, "agrep", None) or getattr(backend, "grep", None)
    if grep_fn is None:
        raise RuntimeError("Backend does not support grep")

    async def _call(**kwargs: Any) -> Any:
        if hasattr(backend, "agrep"):
            return await backend.agrep(pattern, **kwargs)
        result = grep_fn(pattern, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result

    base_kwargs: dict[str, Any] = {"path": path_prefix}
    if glob:
        base_kwargs["glob"] = glob

    if output_mode == "files_with_matches":
        try:
            raw = await _call(**base_kwargs, output_mode="files_with_matches")
        except TypeError:
            raw = await _call(**base_kwargs)
            text = raw if isinstance(raw, str) else str(raw)
            paths: list[str] = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if ":" in line and not line.startswith("/"):
                    path_part = line.split(":", 1)[0].strip()
                    if path_part:
                        paths.append(path_part)
                else:
                    paths.append(line)
            return "\n".join(paths)
        return raw if isinstance(raw, str) else str(raw)

    try:
        raw = await _call(**base_kwargs, output_mode="content")
    except TypeError:
        raw = await _call(**base_kwargs)
    return raw if isinstance(raw, str) else str(raw)


def make_search_knowledge_tool(backend: Any) -> BaseTool:
    """Bind agent filesystem backend for scoped grep/glob."""

    async def _run(
        pattern: str,
        path_prefix: str = "/knowledge/org",
        glob: str | None = None,
        output_mode: Literal["content", "files_with_matches"] = "content",
        head_limit: int = 40,
    ) -> str:
        head_limit = max(1, min(head_limit, 200))
        try:
            text = await _backend_grep(
                backend, pattern, path_prefix, glob, output_mode
            )
        except Exception as exc:
            return json.dumps({"error": str(exc), "matches": []})

        truncated = False
        if output_mode == "content":
            lines = text.splitlines()
            if len(lines) > head_limit:
                text = "\n".join(lines[:head_limit])
                truncated = True
        else:
            lines = [ln for ln in text.splitlines() if ln.strip()]
            if len(lines) > head_limit:
                text = "\n".join(lines[:head_limit])
                truncated = True

        payload = {
            "pattern": pattern,
            "path_prefix": path_prefix,
            "output_mode": output_mode,
            "truncated": truncated,
            "hint": "Open at most 1–3 best paths with read_file(limit<=200); do not offset-loop.",
            "results": text,
        }
        return json.dumps(payload, ensure_ascii=False)

    return StructuredTool.from_function(
        coroutine=_run,
        name="search_knowledge",
        description=(
            "Search org or workspace knowledge by literal pattern. "
            "Prefer this over read_file pagination for /knowledge/org/."
        ),
        args_schema=SearchKnowledgeInput,
    )


def make_wkb_query_tool() -> BaseTool:
    async def _run(
        query: str,
        intent: Literal["nl2sql_metric", "find_table_schema", "data_engineering"] = "nl2sql_metric",
        prefilter_k: int = 200,
        per_layer_k: int = 8,
    ) -> str:
        try:
            with _wkb_cwd():
                from tools.wkb.indexing.retrieval import retrieve  # type: ignore[import-untyped]

                result = retrieve(
                    query=query,
                    intent=intent,
                    prefilter_k=prefilter_k,
                    per_layer_k=per_layer_k,
                )
                hits = [
                    {
                        "candidate_id": h.candidate_id,
                        "layer": h.layer,
                        "score": round(h.score, 6),
                        "title": h.title,
                        "source_file": h.source_file,
                    }
                    for h in result.reranked[:per_layer_k]
                ]
                return json.dumps(
                    {
                        "ok": True,
                        "query": query,
                        "intent": intent,
                        "hits": hits,
                        "hint": "Open ≤3 /knowledge/org/target/knowledgebase/{domain}/{stem}.md files.",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception as exc:
            return json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "hint": "Fall back to metric-index.md routing; do not paginate l1_catalog JSON.",
                },
                ensure_ascii=False,
            )

    return StructuredTool.from_function(
        coroutine=_run,
        name="wkb_query",
        description=(
            "Run org WKB index retrieval (contract-guided data analysis). "
            "Returns reranked table/metric candidates — use before opening knowledgebase md."
        ),
        args_schema=WkbQueryInput,
    )


def wkb_available() -> bool:
    """True when the current org bundle ships a WKB retrieval index."""
    return ORG_KNOWLEDGE_DIR.exists()


# Registry of org/extension tool factories keyed by the tool name a skill can
# declare in its `extensions.tools` frontmatter list. Agent Core never
# hardcodes these names; `factory.py` only instantiates a tool here when a
# non-disabled skill's manifest requests it (see `CapabilityRegistry`).
EXTENSION_TOOL_FACTORIES: dict[str, Any] = {
    "wkb_query": make_wkb_query_tool,
}

EXTENSION_TOOL_AVAILABILITY: dict[str, Any] = {
    "wkb_query": wkb_available,
}
