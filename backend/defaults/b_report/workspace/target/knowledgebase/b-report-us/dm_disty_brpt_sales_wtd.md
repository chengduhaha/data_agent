# DM: B Report profitability serving aggregation (wtd) by business slice (`dm_us.dm_disty_brpt_sales_wtd`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dm_disty_brpt_sales_wtd.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dm_disty_brpt_sales_wtd.md`

## Business purpose

B Report profitability serving aggregation (wtd) by business slice

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_disty_brpt_sales_wtd` — DM layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dm_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: PM, Sales, Buyer, BD and executive analysis views. |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_us.dm_disty_brpt_sales_wtd` | `dm_us.dm_disty_brpt_sales_wtd` | overwrite / incremental | B Report contract `dm_disty_brpt_sales_wtd.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_disty_brpt_sales_wtd` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_disty_brpt_sales_wtd`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** `date_flag` — business date filter for B Report reporting (per contract).
- **Natural key:** `week_no`, `sales_rep_id`, `sales_sup_id`, `sales_mgr_id`, `sales_dir_id`, `sales_vp_id`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_brpt_sales_wtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT week_no, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_brpt_sales_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT week_no, sales_rep_id, sales_sup_id, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_brpt_sales_wtd
WHERE date_flag = '${partition_value}'
GROUP BY week_no, sales_rep_id, sales_sup_id, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `terr_sub_group` — terr sub group
- `terr_group` — terr group
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
- `total_unit` — total unit
- `total_weight` — total weight
- `cgp` — cgp
- `total_btl` — total btl
- `tgm_amt` — tgm amt
- `gm_amt` — gm amt
- `ngm_amt` — ngm amt
- `oplgm_amt` — oplgm amt
- `bo_gross_sales` — bo gross sales
- `bo_gross_cost` — bo gross cost
- `bo_total_unit` — bo total unit
- `bo_gm_amt` — bo gm amt
- ... and 76 additional measure columns (see column register)

### Dimension and key columns

- `week_no` — week no
- `date_flag` — date flag
- `sales_rep_id` — sales rep id
- `sales_rep_name` — sales rep name
- `sales_sup_id` — sales sup id
- `sales_sup_name` — sales sup name
- `sales_mgr_id` — sales mgr id
- `sales_mgr_name` — sales mgr name
- `sales_dir_id` — sales dir id
- `sales_dir_name` — sales dir name
- `sales_vp_id` — sales vp id
- `sales_vp_name` — sales vp name
- `company_no` — company no
- `cust_terr` — cust terr
- `cust_type` — cust type
- `division` — division
- `etl_timestamp` — etl timestamp
- `dt_week` — dt week

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_disty_brpt_sales_wtd`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dm_us.dm_disty_brpt_sales_wtd"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_disty_brpt_sales_wtd` | Primary catalog table documented from B Report contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from B Report contract v2. ETL step-by-step logic is not present in this wiki repository.

**Default analysis filters (important):**

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For `dw_us.dwd_disty_brpt_orders_pl_etl_mi` profitability pulls, still apply `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

---

## Caveats for interpretation

- Derived from B Report contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dm_us` documented as baseline.
- Entity disambiguation (vendor vs customer vs VPL): see `source/contracts/b-report-us/domain-knowledge.md`.
- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).
- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.
- Conflict item:

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dm_disty_brpt_sales_wtd.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dm_disty_brpt_sales_wtd.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 119 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dm_disty_brpt_sales_wtd.md`.*
