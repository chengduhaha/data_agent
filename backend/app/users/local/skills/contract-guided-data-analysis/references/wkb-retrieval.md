# WKB Retrieval for Contract-Guided Analysis

Use two-stage indexing under `/workspace/target/storage/wkb/` to short-list table/metric candidates before opening knowledgebase markdown. Run after [`special-logic-check.md`](special-logic-check.md).

---

## Storage locations

- Snapshots: `/workspace/target/storage/wkb/snapshots/_snapshot_id_template/`
- Sparse index: `/workspace/target/storage/wkb/indexes/sparse_prefilter/`
- Semantic layers: `/workspace/target/storage/wkb/indexes/semantic/l1_catalog|l2_usage|l3_code|l4_flow|l5_eval/`

---

## Storage layer (`l1_catalog`) metadata search

Before opening knowledgebase docs, search table/column metadata directly under `/workspace/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/`:

- Per-table JSON files (e.g. `vertica_dim_us_dim_pub_customer_info.json`) hold table-level metadata (FQN, grain, description).
- `columns.parquet` holds the column catalog across tables — use this to confirm a column exists/spelling/type before writing SQL, instead of guessing from memory.
- `entities.parquet` / `lineage_edges.parquet` support entity and lineage lookups within this layer only (no Bitbucket needed).

Use this metadata to confirm candidate tables/columns exist and to narrow the knowledgebase short-list; it is a fast local check, not a replacement for `run_query.py` reranking below.

---

## Commands

### Rebuild (when index stale)

```bash
python /workspace/target/storage/wkb/indexing/index_builder.py
```

Run from repository root.

### Retrieve candidates

```bash
python /workspace/target/storage/wkb/indexing/run_query.py \
  --query "<metric> <entity> <table cue>" \
  --intent nl2sql_metric \
  --prefilter-k 200 \
  --per-layer-k 8
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
3. Open `/workspace/target/knowledgebase/{domain}/{stem}.md` (same domain) — **NEVER** read `/workspace/source/contracts/{domain}/tables/*.md`

Maximum **3** knowledgebase table files per run.

---

## Layer usage

| Layer | Use for analysis |
|-------|------------------|
| L1 `l1_catalog` | FQN, column names, grain |
| L2 `l2_usage` | Metric serving, report context |
| L3 `l3_code` | Filter/join hints (verify in contract L3) |
| L4 `l4_flow` | Only when user asks lineage; local path required before Bitbucket |
| L5 `l5_eval` | Validation ideas; prefer `eval/golden_cases.md` when present |

Index output is a **short-list**, not proof. SQL must align with contract `metric-index.md` and knowledgebase table L3.

---

## Failure fallback

If `run_query.py` fails:

- Report index unavailable
- Resolve routing from `metric-index.md` + domain-knowledge only
- Do not broaden to `source/etl/**` grep or Bitbucket

If weak candidates:

- Refine query with metric alias, entity token, table stem
- Retry with `find_table_schema` or `nl2sql_metric`

---

## Example

```bash
python /workspace/target/storage/wkb/indexing/run_query.py \
  --query "net sales vendor ranking jan 2026" \
  --intent nl2sql_metric
```

Then open `/workspace/target/knowledgebase/b-report-us/dws_disty_brpt_vend_mtd.md` L3/L2 sections only.
