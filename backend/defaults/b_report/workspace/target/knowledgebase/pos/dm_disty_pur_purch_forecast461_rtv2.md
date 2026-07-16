# FACT: Supplemental fact/context table used by select POS reports (`dm_us.dm_disty_pur_purch_forecast461_rtv2`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pur_purch_forecast461_rtv2.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dm_disty_pur_purch_forecast461_rtv2.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_disty_pur_purch_forecast461_rtv2` — FACT layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dm_us` (US baseline documented as `dw_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **POS / RDS reporting** | Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1) |
| **Sales analytics** | Order, customer, product, and margin attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to POS hub and downstream exports. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_us.dm_disty_pur_purch_forecast461_rtv2` | `dm_us.dm_disty_pur_purch_forecast461_rtv2` | overwrite / incremental | POS contract `dm_disty_pur_purch_forecast461_rtv2.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_disty_pur_purch_forecast461_rtv2` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_disty_pur_purch_forecast461_rtv2`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `vend_no`, `vpl_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_pur_purch_forecast461_rtv2
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vend_no, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_pur_purch_forecast461_rtv2
WHERE date_flag = '${partition_value}'
GROUP BY vend_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vend_no, vpl_no, order_line_no, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_pur_purch_forecast461_rtv2
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, vpl_no, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `rec_mtd` — rec mtd
- `ap_ttl` — ap ttl

### Dimension and key columns

- `date_flag` — date flag
- `vend_no` — vend no
- `vpl_no` — vpl no
- `prod_code` — prod code
- `load_type` — load type

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_disty_pur_purch_forecast461_rtv2`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dm_us.dm_disty_pur_purch_forecast461_rtv2"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_disty_pur_purch_forecast461_rtv2` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dm_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pur_purch_forecast461_rtv2.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dm_disty_pur_purch_forecast461_rtv2.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 7 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pur_purch_forecast461_rtv2.md`.*
