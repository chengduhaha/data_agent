# RDS contracts (`source/contracts/rds`)

Contracts and report SQL for RDS curated examples, ingested from `RDS_Workspace`.

Companion skill: [`.cursor/skills/rds-knowledge-ingest`](../../../.cursor/skills/rds-knowledge-ingest/SKILL.md).  
Knowledgebase docs: [`.cursor/skills/etl-knowledgebase-docs`](../../../.cursor/skills/etl-knowledgebase-docs/SKILL.md) with `source_kind: rds_report_sql`.

## Layout

```
source/contracts/rds/
├── README.md
├── domain-knowledge.md          # shared business_term_aliases
├── {engine}_{domain}/
│   ├── examples-index.md        # catalog only — never KB
│   ├── metric-index.md          # append-only formulas
│   └── etl/
│       └── *.sql                # from typical_*.txt (prefix stripped)
```

## Packs (14)

| Engine | Domains |
|--------|---------|
| Vertica | ap, ar, b_report, cpo, inventory, open_so_bo, pos, rma, vpo |
| StarRocks | cpo, inventory, open_so_bo, pos, vpo |

**91** report SQL scripts under `**/etl/*.sql`.

## Rules

- `examples-index.md` is a **catalog only** — do not convert to `.sql` or Knowledgebase `.md`.
- Metric formulas: **append-only** in each pack `metric-index.md`.
- KB output path: `target/knowledgebase/RDS/{engine}_{domain}/<stem>.md`.

## Re-ingest

```bash
python -m tools.ingest.rds_workspace_to_contracts \
  --rds-source "<path-to-RDS_Workspace>" \
  --repo-root .
```

## Batch Knowledgebase (main skill)

```bash
python -m tools.ingest.rds_report_sql_to_knowledgebase
```
