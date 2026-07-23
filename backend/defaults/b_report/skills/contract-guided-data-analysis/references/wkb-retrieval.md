# WKB Retrieval for Contract-Guided Analysis

Use two-stage indexing under `/knowledge/org/target/storage/wkb/` to short-list table/metric candidates before opening knowledgebase markdown. Run after [`special-logic-check.md`](special-logic-check.md).

---

## Storage locations

- Snapshots: `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/`
- Sparse index: `/knowledge/org/target/storage/wkb/indexes/sparse_prefilter/`
- Semantic layers: `/knowledge/org/target/storage/wkb/indexes/semantic/l1_catalog|l2_usage|l3_code|l4_flow|l5_eval/`

---

## Primary retrieval path

**Always prefer the `wkb_query` builtin tool** (server-side WKB index). Do **not** paginate `l1_catalog/*.json` with `read_file` offset loops — the platform harness blocks that pattern.

```text
wkb_query(query="<metric> <entity> <table cue>", intent="nl2sql_metric")
```

Shell fallback (when debugging index rebuild only):

```bash
cd "$DATA_AGENT_ORG_KNOWLEDGE" && python -m tools.wkb.indexing.run_query \
  --query "<metric> <entity> <table cue>" \
  --intent nl2sql_metric \
  --prefilter-k 200 \
  --per-layer-k 8
```

Shell `execute` does **not** resolve `/knowledge/org/` virtual paths. Use `$DATA_AGENT_ORG_KNOWLEDGE` (injected by data_agent). File tools (`read_file` / `ls` / `grep`) still use `/knowledge/org/...`.

### Rebuild (when index stale)

```bash
cd "$DATA_AGENT_ORG_KNOWLEDGE" && python -m tools.wkb.indexing.index_builder
```

---

## Intent mapping (this skill only)

| User shape | WKB intent |
|------------|------------|
| KPI / scalar / comparison / ranking / trend | `nl2sql_metric` |
| Table / grain discovery | `find_table_schema` |
| ETL / lineage (user explicitly asks) | `data_engineering` |

**Do not use** `incident_debug` in this skill.

---

## Map hits to knowledgebase

1. Take top reranked hits (`candidate_id`, `title`, `source_file`)
2. Resolve domain from hit metadata or [`domain-routing.md`](domain-routing.md)
3. Open `/knowledge/org/target/knowledgebase/{domain}/{stem}.md` (same domain) — **NEVER** read `/knowledge/org/source/contracts/{domain}/tables/*.md`

Maximum **3** knowledgebase table files per run.

---

## Layer usage

| Layer | Use for analysis |
|-------|------------------|
| L1 `l1_catalog` | FQN, column names, grain (via `wkb_query` hits, not JSON pagination) |
| L2 `l2_usage` | Metric serving, report context |
| L3 `l3_code` | Filter/join hints (verify in contract L3) |
| L4 `l4_flow` | Only when user asks lineage; local path required before Bitbucket |
| L5 `l5_eval` | Validation ideas; use metric-index routing checks only — do not read `eval/golden_cases.md` |

Index output is a **short-list**, not proof. SQL must align with contract `metric-index.md` and knowledgebase table L3.

---

## Failure fallback

If `wkb_query` (or `run_query.py`) fails:

- Report index unavailable
- Resolve routing from `metric-index.md` + domain-knowledge only
- Do **not** broaden to `source/etl/**` grep, Bitbucket, or `read_file` pagination of `l1_catalog` JSON

If weak candidates:

- Refine query with metric alias, entity token, table stem
- Retry with `find_table_schema` or `nl2sql_metric`

---

## Example

```text
wkb_query(query="net sales vendor ranking jan 2026", intent="nl2sql_metric")
```

Then open `/knowledge/org/target/knowledgebase/b-report-us/dws_disty_brpt_vend_mtd.md` L3/L2 sections only.
