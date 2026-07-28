# RDS reference material (`source/ref/RDS`)

Curated table lists, relationships, and special logic for **RDS report SQL** packs, organized by engine and domain.

Ingested from `RDS_Workspace` via [`.cursor/skills/rds-knowledge-ingest`](../../../.cursor/skills/rds-knowledge-ingest/SKILL.md).

## Layout

```
source/ref/RDS/
├── README.md
├── vertica_ap/
├── vertica_ar/
├── vertica_b_report/
├── vertica_cpo/
├── vertica_inventory/
├── vertica_open_so_bo/
├── vertica_pos/
├── vertica_rma/
├── vertica_vpo/
├── starrocks_cpo/
├── starrocks_inventory/
├── starrocks_open_so_bo/
├── starrocks_pos/
└── starrocks_vpo/
```

Each pack folder contains (when present):

| File | Purpose |
|------|---------|
| `table list.txt` | Tables used by the domain reports |
| `table relationship.txt` | Join / relationship notes |
| `special_logic.txt` | Non-default reusable report patterns |

**Pack id:** `{engine}_{domain}` — e.g. `B_Report` → `b_report`, prefixed `vertica_` / `starrocks_`.

## Related trees

| Tree | Role |
|------|------|
| `source/contracts/rds/` | examples-index, metric-index, `etl/*.sql` |
| `target/knowledgebase/RDS/` | L1–L6 docs (authored by etl-knowledgebase-docs only) |
| `source/ref/pos/` | Legacy POS ref — **not** replaced by this tree |

## Citation

`source/ref/RDS/vertica_b_report/special_logic.txt:12`
