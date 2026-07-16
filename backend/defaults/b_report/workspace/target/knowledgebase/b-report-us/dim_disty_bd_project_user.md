# DIM: Shared dimension for B Report attribute enrichment and join lookups (`dim_us.dim_disty_bd_project_user`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dim_disty_bd_project_user.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dim_disty_bd_project_user.md`

## Business purpose

Shared dimension for B Report attribute enrichment and join lookups

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dim_us.dim_disty_bd_project_user` — DIM layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dim_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report semantic layer, dashboard queries, and BI users. |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_disty_bd_project_user` | `dim_us.dim_disty_bd_project_user` | overwrite / incremental | B Report contract `dim_disty_bd_project_user.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dim_us.dim_disty_bd_project_user` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dim_us.dim_disty_bd_project_user`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `project_no`, `task_no`, `bd_rep_id`, `bd_mgr_id`, `bd_dir_id`, `bd_vp_id`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_disty_bd_project_user
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT project_no, COUNT(*) AS row_cnt
FROM dim_us.dim_disty_bd_project_user
WHERE date_flag = '${partition_value}'
GROUP BY project_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT project_no, task_no, bd_rep_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_disty_bd_project_user
WHERE date_flag = '${partition_value}'
GROUP BY project_no, task_no, bd_rep_id, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- No measure-role columns tagged in contract; table may be dimension-only.

### Dimension and key columns

- `project_no` — project no
- `project_name` — project name
- `task_no` — task no
- `task_name` — task name
- `bd_rep_id` — bd rep id
- `bd_rep_name` — bd rep name
- `bd_mgr_id` — bd mgr id
- `bd_mgr_name` — bd mgr name
- `bd_dir_id` — bd dir id
- `bd_dir_name` — bd dir name
- `bd_vp_id` — bd vp id
- `bd_vp_name` — bd vp name
- `bd_svp_id` — bd svp id
- `bd_svp_name` — bd svp name
- `entry_datetime` — entry datetime

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dim_us.dim_disty_bd_project_user`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dim_us.dim_disty_bd_project_user"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_disty_bd_project_user` | Primary catalog table documented from B Report contract |

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
- US schema `dim_us` documented as baseline.
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
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_disty_bd_project_user.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dim_disty_bd_project_user.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 15 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dim_disty_bd_project_user.md`.*
