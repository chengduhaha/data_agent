# DWS: B Report combined-month profitability serving slice (bd_vend_comb_mtd) (`dw_us.dws_disty_brpt_bd_vend_comb_mtd`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dws_disty_brpt_bd_vend_comb_mtd.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dws_disty_brpt_bd_vend_comb_mtd.md`

## Business purpose

B Report combined-month profitability serving slice (bd_vend_comb_mtd)

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dws_disty_brpt_bd_vend_comb_mtd` — DWS layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dw_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

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
| **Query for reporting** | `dw_us.dws_disty_brpt_bd_vend_comb_mtd` | `dw_us.dws_disty_brpt_bd_vend_comb_mtd` | overwrite / incremental | B Report contract `dws_disty_brpt_bd_vend_comb_mtd.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dws_disty_brpt_bd_vend_comb_mtd` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dws_disty_brpt_bd_vend_comb_mtd`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** `month_no` — business date filter for B Report reporting (per contract).
- **Natural key:** `project_no`, `task_no`, `company_no`, `vend_no`, `master_vend_no`, `date_flag`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT month_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_bd_vend_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY month_no;

-- 2) Metric sum by business dimension (top N)
SELECT project_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_bd_vend_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY project_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT project_no, task_no, company_no, month_no, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_bd_vend_comb_mtd
WHERE month_no = '${partition_value}'
GROUP BY project_no, task_no, company_no, month_no
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `d_sales` — d sales
- `d_cost` — d cost
- `d_unit` — d unit
- `d_gm` — d gm
- `d_ngm` — d ngm
- `d_opl` — d opl
- `d_scm_usage` — d scm usage
- `d_tgm` — d tgm
- `d_cgp` — d cgp
- `d_total_btl` — d total btl
- `w_sales` — w sales
- `w_cost` — w cost
- `w_unit` — w unit
- `w_gm` — w gm
- `w_ngm` — w ngm
- `w_opl` — w opl
- `w_scm_usage` — w scm usage
- `w_tgm` — w tgm
- `w_cgp` — w cgp
- `w_total_btl` — w total btl
- `m_sales` — m sales
- `m_cost` — m cost
- `m_unit` — m unit
- `m_gm` — m gm
- `m_ngm` — m ngm
- ... and 105 additional measure columns (see column register)

### Dimension and key columns

- `month_no` — month no
- `project_no` — project no
- `project_name` — project name
- `task_no` — task no
- `task_name` — task name
- `company_no` — company no
- `vend_no` — vend no
- `vend_name` — vend name
- `master_vend_no` — master vend no
- `master_vend_name` — master vend name
- `seg_code` — seg code
- `etl_timestamp` — etl timestamp
- `b33_flag` — b33 flag
- `date_flag` — date flag

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dw_us.dws_disty_brpt_bd_vend_comb_mtd`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dw_us.dws_disty_brpt_bd_vend_comb_mtd"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dws_disty_brpt_bd_vend_comb_mtd` | Primary catalog table documented from B Report contract |

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
- US schema `dw_us` documented as baseline.
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
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dws_disty_brpt_bd_vend_comb_mtd.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dws_disty_brpt_bd_vend_comb_mtd.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 144 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dws_disty_brpt_bd_vend_comb_mtd.md`.*
