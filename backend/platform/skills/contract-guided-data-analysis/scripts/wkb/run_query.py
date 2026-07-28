from __future__ import annotations

import argparse
import json

from .index_builder import build_indexes
from .retrieval import prefilter_candidates, retrieve


def main() -> None:
    parser = argparse.ArgumentParser(description="Two-stage retrieval for WKB storage indexes")
    parser.add_argument("--query", required=True, help="User query text")
    parser.add_argument(
        "--intent",
        default="find_table_schema",
        choices=["find_table_schema", "nl2sql_metric", "data_engineering", "incident_debug"],
    )
    parser.add_argument("--prefilter-k", type=int, default=200)
    parser.add_argument("--per-layer-k", type=int, default=8)
    parser.add_argument("--rebuild", action="store_true", help="Rebuild indexes before querying")
    args = parser.parse_args()

    if args.rebuild:
        build_indexes()

    candidate_set = prefilter_candidates(args.query, top_k=args.prefilter_k)
    result = retrieve(
        query=args.query,
        intent=args.intent,
        prefilter_k=args.prefilter_k,
        per_layer_k=args.per_layer_k,
    )

    print("=== Prefilter Candidates ===")
    for c in candidate_set.candidates[:20]:
        print(f"{c.candidate_id} | score={c.score:.4f} token={c.token_score:.4f} graph={c.graph_score:.4f}")

    print("\n=== Reranked Hits ===")
    out = [
        {
            "candidate_id": h.candidate_id,
            "layer": h.layer,
            "score": round(h.score, 6),
            "title": h.title,
            "source_file": h.source_file,
        }
        for h in result.reranked
    ]
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
