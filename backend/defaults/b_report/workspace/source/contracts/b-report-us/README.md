# B Report US contracts (`source/contracts/b-report-us`)

Vendored from `data_analysis_agent_brpt/knowledge/b-report-us` (contract v2.0.0).

## Purpose

US B Report (distributor P&L / profitability) table contracts, domain knowledge, metrics index, and golden eval cases. Use for B Report entity semantics, grain, joins, and metric definitions — not for POS/RDS report SQL (see `source/ref/pos/`).

## Layout

```
source/contracts/b-report-us/
├── domain-knowledge.md    # Entity ontology, disambiguation rules, layer naming
├── golden-questions.md    # Representative business questions
├── metric-index.md        # Metric catalog and definitions
├── tables/                # Per-table v2 contracts (101 tables)
└── eval/
    ├── golden_cases.yaml  # Golden evaluation cases (machine-readable)
    └── golden_cases.md    # Golden evaluation cases (human-readable)
```

Maintenance scripts from the source package live under [`tools/ingest/b-report-us/scripts/`](../../../tools/ingest/b-report-us/scripts/).

## Hub table

- **DWD detail:** `dw_us.dwd_disty_brpt_orders_pl_etl_mi` (shipped order line / B Report fact)
- **POS overlap:** `dw_us.dwd_disty_common_pos_di` is the POS RDS hub; B Report uses `dwd_disty_brpt_orders_pl_etl_mi` and related `dws_disty_brpt_*` / `dm_disty_brpt_*` serving tables.

## When to consult

| Need | Read |
|------|------|
| Vendor vs customer vs VPL vs territory disambiguation | `domain-knowledge.md` |
| Table grain, columns, filters | `tables/<table_stem>.md` |
| Metric meaning | `metric-index.md` |
| POS physical join paths | `source/ref/pos/table relationship.txt` |

## Provenance

| Field | Value |
|-------|-------|
| Origin repo | `data_analysis_agent_brpt` |
| Origin path | `knowledge/b-report-us` |
| Sync policy | Manual or bootstrap script |
