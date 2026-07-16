# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dws_disty_brpt_cust_mtd`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dws_disty_brpt_cust_mtd.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dws_disty_brpt_cust_mtd.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dws_disty_brpt_cust_mtd` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dws_disty_brpt_cust_mtd` | `dw_us.dws_disty_brpt_cust_mtd` | overwrite / incremental | POS contract `dws_disty_brpt_cust_mtd.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dws_disty_brpt_cust_mtd` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dws_disty_brpt_cust_mtd`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `month_no` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `cust_no`, `mcust_no`, `sales_rep_id`, `sales_sup_id`, `sales_mgr_id`, `sales_dir_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT month_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;

-- 2) Metric sum by business dimension (top N)
SELECT cust_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE month_no = '${partition_value}'
GROUP BY cust_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT cust_no, mcust_no, sales_rep_id, month_no, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE month_no = '${partition_value}'
GROUP BY cust_no, mcust_no, sales_rep_id, month_no
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `gross_sales` — gross sales
- `net_sales` — net sales
- `gross_cost` — gross cost
- `net_cost` — net cost
- `scm_usage` — scm usage
- `ds_sales` — ds sales
- `stock_sales` — stock sales
- `ds_cost` — ds cost
- `stock_cost` — stock cost
- `ds_scm_usage` — ds scm usage
- `stock_scm_usage` — stock scm usage
- `total_weight` — total weight
- `net_income` — net income
- `invest_capital` — invest capital
- `cgp` — cgp
- `total_btl` — total btl
- `tgm_amt` — tgm amt
- `gm_amt` — gm amt
- `ngm_amt` — ngm amt
- `oplgm_amt` — oplgm amt
- `bo_gross_sales` — bo gross sales
- `bo_gross_cost` — bo gross cost
- `bo_gm_amt` — bo gm amt
- `so_gross_sales` — so gross sales
- `so_gross_cost` — so gross cost
- ... and 92 additional measure columns (see column register)

### Dimension and key columns

- `month_no` — month no
- `cust_no` — cust no
- `cust_name` — cust name
- `mcust_no` — mcust no
- `mcust_name` — mcust name
- `cust_terr` — cust terr
- `terr_name` — terr name
- `cust_type` — cust type
- `cust_type_desc` — cust type desc
- `division` — division
- `division_desc` — division desc
- `terr_sub_group` — terr sub group
- `sub_group_desc` — sub group desc
- `terr_group` — terr group
- `terr_group_desc` — terr group desc
- `sales_rep_id` — sales rep id
- `sales_sup_id` — sales sup id
- `sales_mgr_id` — sales mgr id
- `sales_dir_id` — sales dir id
- `sales_vp_id` — sales vp id
- `company_no` — company no
- `total_unit` — total unit
- `bo_total_unit` — bo total unit
- `so_total_unit` — so total unit
- `rr_unit` — rr unit
- `etl_timestamp` — etl timestamp
- `goal_cust_cnt` — goal cust cnt
- `date_flag` — date flag

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dws_disty_brpt_cust_mtd`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dws_disty_brpt_cust_mtd"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dws_disty_brpt_cust_mtd` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dws_disty_brpt_cust_mtd.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dws_disty_brpt_cust_mtd.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 145 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dws_disty_brpt_cust_mtd.md`.*
