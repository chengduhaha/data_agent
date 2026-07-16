from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Candidate:
    candidate_id: str
    score: float
    token_score: float
    graph_score: float
    reasons: List[str]


@dataclass
class CandidateSet:
    query: str
    top_k: int
    candidates: List[Candidate]


@dataclass
class LayerHit:
    candidate_id: str
    layer: str
    score: float
    source_file: str
    title: str


@dataclass
class RetrievalResult:
    intent: str
    layer_hits: Dict[str, List[LayerHit]]
    reranked: List[LayerHit]
