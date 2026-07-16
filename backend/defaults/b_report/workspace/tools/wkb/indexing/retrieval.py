from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from .contracts import Candidate, CandidateSet, LayerHit, RetrievalResult

SPARSE_INDEX_DIR = Path("target/storage/wkb/indexes/sparse_prefilter")
SEMANTIC_INDEX_DIR = Path("target/storage/wkb/indexes/semantic")
LAYERS = ["l1_catalog", "l2_usage", "l3_code", "l4_flow", "l5_eval"]
TOKEN_PATTERN = re.compile(r"[a-z0-9_\.]+")

INTENT_WEIGHTS = {
    "find_table_schema": {"l1_catalog": 1.0, "l2_usage": 0.35},
    "nl2sql_metric": {"l2_usage": 1.0, "l3_code": 0.9, "l1_catalog": 0.4, "l5_eval": 0.4},
    "data_engineering": {"l3_code": 1.0, "l4_flow": 0.9, "l2_usage": 0.2},
    "incident_debug": {"l4_flow": 1.0, "l2_usage": 0.4, "l5_eval": 0.2},
}


def _norm_tokens(text: str) -> List[str]:
    return [t for t in TOKEN_PATTERN.findall(text.lower()) if len(t) > 1]


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def prefilter_candidates(query: str, top_k: int = 200) -> CandidateSet:
    tokens = _norm_tokens(query)
    inverted = _load_json(SPARSE_INDEX_DIR / "token_inverted_index/index.json")
    graph = _load_json(SPARSE_INDEX_DIR / "graph_index/index.json")

    token_scores = defaultdict(float)
    for token in tokens:
        hits = inverted.get(token, [])
        # simple rarity boost
        rarity = 1.0 / max(len(hits), 1)
        for cid in hits:
            token_scores[cid] += 1.0 + rarity

    # Only snapshot-backed candidate_ids are valid retrieval targets.
    valid_candidate_ids = {cid for hits in inverted.values() for cid in hits}

    graph_scores = defaultdict(float)
    # expand one hop from top lexical hits
    lexical_roots = sorted(token_scores.items(), key=lambda x: x[1], reverse=True)[:100]
    for cid, score in lexical_roots:
        for n in graph.get(cid, []):
            if n not in valid_candidate_ids or n == cid:
                continue
            graph_scores[n] += score * 0.35

    merged = []
    all_ids = (set(token_scores.keys()) | set(graph_scores.keys())) & valid_candidate_ids
    for cid in all_ids:
        t = token_scores[cid]
        g = graph_scores[cid]
        reasons = []
        if t > 0:
            reasons.append("token")
        if g > 0:
            reasons.append("graph")
        merged.append(
            Candidate(
                candidate_id=cid,
                score=t + g,
                token_score=t,
                graph_score=g,
                reasons=reasons,
            )
        )

    merged.sort(key=lambda c: c.score, reverse=True)
    top_k = max(50, min(300, top_k))
    return CandidateSet(query=query, top_k=top_k, candidates=merged[:top_k])


def _query_vector(query: str, idf: dict) -> tuple[dict, float]:
    q_counts = defaultdict(int)
    for t in _norm_tokens(query):
        q_counts[t] += 1
    if not q_counts:
        return {}, 1.0

    max_tf = max(q_counts.values())
    weights = {}
    norm = 0.0
    for t, tf in q_counts.items():
        w = (tf / max_tf) * idf.get(t, 1.0)
        weights[t] = w
        norm += w * w
    return weights, math.sqrt(norm) if norm > 0 else 1.0


def semantic_retrieve(query: str, candidate_ids: List[str], per_layer_k: int = 8) -> Dict[str, List[LayerHit]]:
    # Hard anti-full-scan guard.
    if not candidate_ids:
        raise ValueError("Prefilter-first guard: candidate_ids is empty; semantic retrieval aborted.")

    cid_set = set(candidate_ids)
    results: Dict[str, List[LayerHit]] = {}
    for layer in LAYERS:
        layer_index = _load_json(SEMANTIC_INDEX_DIR / layer / "index.json")
        docs = layer_index.get("docs", [])
        idf = layer_index.get("idf", {})
        qv, qnorm = _query_vector(query, idf)
        hits = []
        for doc in docs:
            if doc["candidate_id"] not in cid_set:
                continue
            dot = 0.0
            for t, qw in qv.items():
                dot += qw * doc["weights"].get(t, 0.0)
            score = dot / (qnorm * doc.get("norm", 1.0))
            if score <= 0:
                continue
            hits.append(
                LayerHit(
                    candidate_id=doc["candidate_id"],
                    layer=layer,
                    score=score,
                    source_file=doc["source_file"],
                    title=doc["title"],
                )
            )
        hits.sort(key=lambda h: h.score, reverse=True)
        results[layer] = hits[:per_layer_k]
    return results


def rerank_by_intent(intent: str, layer_hits: Dict[str, List[LayerHit]], top_n: int = 20) -> List[LayerHit]:
    weights = INTENT_WEIGHTS.get(intent, {layer: 1.0 for layer in LAYERS})
    merged = []
    for layer, hits in layer_hits.items():
        w = weights.get(layer, 0.0)
        if w <= 0:
            continue
        for hit in hits:
            merged.append(
                LayerHit(
                    candidate_id=hit.candidate_id,
                    layer=hit.layer,
                    score=hit.score * w,
                    source_file=hit.source_file,
                    title=hit.title,
                )
            )
    merged.sort(key=lambda h: h.score, reverse=True)
    return merged[:top_n]


def retrieve(query: str, intent: str = "find_table_schema", prefilter_k: int = 200, per_layer_k: int = 8) -> RetrievalResult:
    candidates = prefilter_candidates(query, top_k=prefilter_k)
    layer_hits = semantic_retrieve(
        query=query,
        candidate_ids=[c.candidate_id for c in candidates.candidates],
        per_layer_k=per_layer_k,
    )
    reranked = rerank_by_intent(intent=intent, layer_hits=layer_hits)
    return RetrievalResult(intent=intent, layer_hits=layer_hits, reranked=reranked)
