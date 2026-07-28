"""Offline golden_cases sql_shape validation."""

from __future__ import annotations

from pathlib import Path

import yaml

CASES_PATH = (
    Path(__file__).resolve().parents[1]
    / "platform/skills/contract-guided-data-analysis/knowledge/contracts/b-report-us/eval/golden_cases.yaml"
)


def _sql_shape_pass(certified_sql: str, assertions: dict) -> bool:
    shape = assertions.get("sql_shape") or {}
    must = [s.lower() for s in shape.get("must_contain") or []]
    must_not = [s.lower() for s in shape.get("must_not_contain") or []]
    sql_lower = (certified_sql or "").lower()
    for token in must:
        if token not in sql_lower:
            return False
    for token in must_not:
        if token in sql_lower:
            return False
    return True


def test_golden_cases_yaml_loads() -> None:
    assert CASES_PATH.exists()
    raw = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
    assert len(raw.get("cases") or []) >= 10


def _is_substantive_sql(sql: str) -> bool:
    lowered = (sql or "").lower()
    return " from " in lowered or "\nfrom " in lowered


def test_routing_certified_sql_shapes_pass() -> None:
    raw = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    tested = 0
    for case in raw.get("cases") or []:
        if case.get("status") != "routing-certified":
            continue
        sql = case.get("certified_sql") or ""
        if not _is_substantive_sql(sql):
            continue
        tested += 1
        if not _sql_shape_pass(sql, case.get("assertions") or {}):
            failures.append(str(case.get("id")))
    assert tested > 0
    assert not failures, f"sql_shape failures: {failures[:10]}"
