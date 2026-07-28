from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from .paths import SNAPSHOT_DIR, SPARSE_INDEX_DIR, SEMANTIC_INDEX_DIR, LAYERS
TOKEN_PATTERN = re.compile(r"[a-z0-9_\.]+")


def _norm_tokens(text: str) -> List[str]:
    return [t for t in TOKEN_PATTERN.findall(text.lower()) if len(t) > 1]


def _flatten_text(value: object) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, (int, float, bool)):
        yield str(value)
        return
    if isinstance(value, dict):
        for k, v in value.items():
            yield str(k)
            yield from _flatten_text(v)
        return
    if isinstance(value, list):
        for item in value:
            yield from _flatten_text(item)


def _candidate_id(payload: dict, path: Path) -> str:
    return payload.get("entity_id") or payload.get("seed_id") or path.stem


def _title(payload: dict, path: Path) -> str:
    return (
        payload.get("qualified_name")
        or payload.get("source_folder")
        or payload.get("seed_id")
        or payload.get("entity_id")
        or path.name
    )


def _layer_docs() -> Dict[str, List[dict]]:
    docs: Dict[str, List[dict]] = {layer: [] for layer in LAYERS}
    for layer in LAYERS:
        layer_dir = SNAPSHOT_DIR / layer
        if not layer_dir.exists():
            continue
        for json_path in sorted(layer_dir.glob("*.json")):
            if json_path.name in {"stats.json", "equivalence_rules.json"}:
                continue
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            cid = _candidate_id(payload, json_path)
            texts = list(_flatten_text(payload))
            token_counts = Counter()
            for text in texts:
                token_counts.update(_norm_tokens(text))
            docs[layer].append(
                {
                    "candidate_id": cid,
                    "layer": layer,
                    "source_file": str(json_path).replace("\\", "/"),
                    "title": _title(payload, json_path),
                    "tokens": dict(token_counts),
                    "raw": payload,
                }
            )
    return docs


def _parse_lineage_edge(raw_edge: str) -> Tuple[str, str] | None:
    if "->" not in raw_edge:
        return None
    left, right = raw_edge.split("->", 1)
    return left.strip(), right.strip()


def _add_undirected_neighbor(graph: Dict[str, set], left: str, right: str) -> None:
    # Prevent self-links; they create artificial self-boost during graph expansion.
    if not left or not right or left == right:
        return
    graph[left].add(right)
    graph[right].add(left)


def build_indexes() -> None:
    docs_by_layer = _layer_docs()
    all_docs = [d for items in docs_by_layer.values() for d in items]

    inverted: Dict[str, set] = defaultdict(set)
    graph: Dict[str, set] = defaultdict(set)

    for doc in all_docs:
        cid = doc["candidate_id"]
        for token in doc["tokens"].keys():
            inverted[token].add(cid)

        raw = doc["raw"]
        for edge in raw.get("lineage_edges", []):
            parsed = _parse_lineage_edge(edge)
            if not parsed:
                continue
            src, dst = parsed
            _add_undirected_neighbor(graph, cid, src)
            _add_undirected_neighbor(graph, cid, dst)

        for key in ["downstream_consumers", "probe_targets"]:
            for neighbor in raw.get(key, []):
                n = str(neighbor).strip()
                if n:
                    _add_undirected_neighbor(graph, cid, n)

    SPARSE_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    (SPARSE_INDEX_DIR / "token_inverted_index").mkdir(parents=True, exist_ok=True)
    (SPARSE_INDEX_DIR / "graph_index").mkdir(parents=True, exist_ok=True)

    inverted_out = {k: sorted(v) for k, v in inverted.items()}
    graph_out = {k: sorted(v) for k, v in graph.items()}
    (SPARSE_INDEX_DIR / "token_inverted_index/index.json").write_text(
        json.dumps(inverted_out, indent=2), encoding="utf-8"
    )
    (SPARSE_INDEX_DIR / "graph_index/index.json").write_text(
        json.dumps(graph_out, indent=2), encoding="utf-8"
    )

    semantic_meta = {"layers": {}, "total_docs": len(all_docs)}
    SEMANTIC_INDEX_DIR.mkdir(parents=True, exist_ok=True)

    for layer, docs in docs_by_layer.items():
        layer_dir = SEMANTIC_INDEX_DIR / layer
        layer_dir.mkdir(parents=True, exist_ok=True)
        df = Counter()
        for doc in docs:
            for token in doc["tokens"].keys():
                df[token] += 1
        n_docs = max(len(docs), 1)
        idf = {t: math.log((1 + n_docs) / (1 + c)) + 1.0 for t, c in df.items()}

        doc_vectors = []
        for doc in docs:
            weights = {}
            max_tf = max(doc["tokens"].values()) if doc["tokens"] else 1
            norm = 0.0
            for token, tf in doc["tokens"].items():
                w = (tf / max_tf) * idf.get(token, 1.0)
                weights[token] = w
                norm += w * w
            doc_vectors.append(
                {
                    "candidate_id": doc["candidate_id"],
                    "source_file": doc["source_file"],
                    "title": doc["title"],
                    "weights": weights,
                    "norm": math.sqrt(norm) if norm > 0 else 1.0,
                }
            )

        (layer_dir / "index.json").write_text(
            json.dumps({"layer": layer, "docs": doc_vectors, "idf": idf}, indent=2),
            encoding="utf-8",
        )
        semantic_meta["layers"][layer] = {"doc_count": len(docs)}

    (SPARSE_INDEX_DIR / "metadata.json").write_text(
        json.dumps(
            {
                "stage": "sparse_prefilter",
                "token_count": len(inverted_out),
                "graph_node_count": len(graph_out),
                "candidate_count": len({d["candidate_id"] for d in all_docs}),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (SEMANTIC_INDEX_DIR / "metadata.json").write_text(
        json.dumps(semantic_meta, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    build_indexes()
