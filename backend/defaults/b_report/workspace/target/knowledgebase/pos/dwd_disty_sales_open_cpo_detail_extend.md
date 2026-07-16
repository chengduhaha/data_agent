# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_sales_open_cpo_detail_extend`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_open_cpo_detail_extend.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_sales_open_cpo_detail_extend.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_sales_open_cpo_detail_extend` — FACT layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dw_us` (US baseline documented as `dw_us` / `dim_us`).

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
| **Query for reporting** | `dw_us.dwd_disty_sales_open_cpo_detail_extend` | `dw_us.dwd_disty_sales_open_cpo_detail_extend` | overwrite / incremental | POS contract `dwd_disty_sales_open_cpo_detail_extend.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_sales_open_cpo_detail_extend` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_sales_open_cpo_detail_extend`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `cpo_id`, `cpo_line_no`, `cpo_sku_no`, `cpo_line_delete_id`, `swl_prog_id`, `cust_part_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_sales_open_cpo_detail_extend
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT cpo_id, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_sales_open_cpo_detail_extend
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT cpo_id, cpo_line_no, cpo_sku_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_sales_open_cpo_detail_extend
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id, cpo_line_no, cpo_sku_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `cpo_line_qty` — cpo line qty
- `cpo_allocated_qty` — cpo allocated qty
- `cpo_bo_qty` — cpo bo qty
- `cpo_so_qty` — cpo so qty
- `cpo_del_qty` — cpo del qty
- `cpo_ship_qty` — cpo ship qty
- `cpo_price` — cpo price
- `cpo_grid_price` — cpo grid price
- `cpo_unit_price` — cpo unit price
- `cpo_unit_cost` — cpo unit cost
- `cpo_extended_price` — cpo extended price
- `cpo_extended_cost` — cpo extended cost
- `cpo_gm_percent` — cpo gm percent
- `cpo_price_flag` — cpo price flag
- `cpo_grid_adj` — cpo grid adj
- `cis_unit_cost` — cis unit cost
- `cpo_extended_exp` — cpo extended exp
- `adj_amount` — adj amount
- `so_unit_price` — so unit price
- `gm` — gm
- `gm_net` — gm net
- `list_points` — list points
- `off_retail` — off retail
- `rebate_total` — rebate total
- `so_net_price` — so net price
- ... and 2 additional measure columns (see column register)

### Dimension and key columns

- `cpo_id` — cpo id
- `cpo_line_seq` — cpo line seq
- `cpo_line_no` — cpo line no
- `cpo_line_status` — cpo line status
- `cpo_sku_no` — cpo sku no
- `cpo_sku_inv_type` — cpo sku inv type
- `cpo_line_delete_id` — cpo line delete id
- `cpo_line_delete_name` — cpo line delete name
- `cpo_line_delete_datetime` — cpo line delete datetime
- `swl_prog_id` — swl prog id
- `cust_part_no` — cust part no
- `scm_no` — scm no
- `scm_desc` — scm desc
- `spa_no` — spa no
- `spa_ref_no` — spa ref no
- `spa_type` — spa type
- `etl_timestamp` — etl timestamp
- `cpo_change_id` — cpo change id
- `cpo_change_date` — cpo change date
- `cpo_entry_datetime` — cpo entry datetime
- `date_flag` — date flag
- `vrf` — vrf
- `contract_no` — contract no
- `wf_request_id` — wf request id

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_sales_open_cpo_detail_extend`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_sales_open_cpo_detail_extend"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_sales_open_cpo_detail_extend` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dw_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_open_cpo_detail_extend.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_sales_open_cpo_detail_extend.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 51 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_open_cpo_detail_extend.md`.*
