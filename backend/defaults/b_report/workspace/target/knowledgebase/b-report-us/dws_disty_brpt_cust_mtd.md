# DWS: Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain) (`dw_us.dws_disty_brpt_cust_mtd`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dws_disty_brpt_cust_mtd.md`

## Business purpose

Customer-level B Report P&L and goals MTD serving table (cust + territory + sales hierarchy grain)

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dws_disty_brpt_cust_mtd` — DWS layer table used in US B Report analytics (`US B Report baseline`). |
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
| **Query for reporting** | `dw_us.dws_disty_brpt_cust_mtd` | `dw_us.dws_disty_brpt_cust_mtd` | overwrite / incremental | B Report contract `dws_disty_brpt_cust_mtd.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dws_disty_brpt_cust_mtd` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dws_disty_brpt_cust_mtd`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** Not documented in repository
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_no, COUNT(*) AS row_cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY order_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_no, order_type, order_line_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dws_disty_brpt_cust_mtd
WHERE date_flag = '${partition_value}'
GROUP BY order_no, order_type, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- No measure-role columns tagged in contract; table may be dimension-only.

### Dimension and key columns

- See full column catalog in Dependencies section.

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dw_us.dws_disty_brpt_cust_mtd`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dw_us.dws_disty_brpt_cust_mtd"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dws_disty_brpt_cust_mtd` | Primary catalog table documented from B Report contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from B Report contract v2. ETL step-by-step logic is not present in this wiki repository.

**Default analysis filters (important):**

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For `dw_us.dwd_disty_brpt_orders_pl_etl_mi` profitability pulls, still apply `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

- Upstream serving tables already aggregate order-line P&L; do not re-apply `sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` unless the question explicitly requires those scopes.
- Goal join: `goal_type = 'NORMAL'`, `period = month_no`, `cust_no <> 0`; full join preserves goal-only customers.
- Goal join intentionally omits `terr_sub_group` / `terr_group` on join keys to avoid duplicate rows from dirty goal data (ETL comment in script).
- `mcust_no` for goal rows comes from `dim_pub_customer_info_df`, not the goal table.
- Technical sync: `hive2vertica` uses `where date_flag = '${date_flag}'` only — not a business filter.

---

## Caveats for interpretation

- Derived from B Report contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dw_us` documented as baseline.
- Entity disambiguation (vendor vs customer vs VPL): see `source/contracts/b-report-us/domain-knowledge.md`.
- Verify row counts and `date_flag` coverage after each monthly close (compare Hive vs Vertica tail dates).
- Check `cust_no` / `mcust_no` match rates against `dim_us.dim_pub_customer_info` on sample `date_flag`.
- Monitor null or sentinel `-3` rates on hierarchy keys (`sales_rep_id`, `terr_sub_group`) after dimension snapshot joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).
- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dws_disty_brpt_cust_mtd.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 0 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dws_disty_brpt_cust_mtd.md`.*
