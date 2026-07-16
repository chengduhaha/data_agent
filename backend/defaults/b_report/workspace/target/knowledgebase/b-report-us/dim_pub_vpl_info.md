# DIM: Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group (`dim_us.dim_pub_vpl_info`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dim_pub_vpl_info.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dim_pub_vpl_info.md`

## Business purpose

Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dim_us.dim_pub_vpl_info` — DIM layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dim_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: `dim_pub_part_info`, `dws_disty_brpt_vpl_1d`, `pl_extend` VPL attributes. |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_vpl_info` | `dim_us.dim_pub_vpl_info` | overwrite / incremental | B Report contract `dim_pub_vpl_info.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dim_us.dim_pub_vpl_info` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dim_us.dim_pub_vpl_info`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `vpl_no`, `vend_no`, `entry_id`, `alt_vend_no`, `alt_vpl_no`, `vpc_group_id`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vpl_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY vpl_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vpl_no, vend_no, entry_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY vpl_no, vend_no, entry_id, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `bid_factor` — bid factor
- `retail_factor` — retail factor
- `dsv_min_amt` — dsv min amt

### Dimension and key columns

- `vpl_no` — vpl no
- `vend_no` — vend no
- `vpl_code` — vpl code
- `vpl_desc` — vpl desc
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `tax_code` — tax code
- `alt_vend_no` — alt vend no
- `alt_vpl_no` — alt vpl no
- `call_price` — call price
- `prod_type` — prod type
- `alt_seg_code` — alt seg code
- `active` — active
- `ec_flag` — ec flag
- `dsv_type` — dsv type
- `alt_seg_name` — alt seg name
- `vpc_group_id` — vpc group id
- `etl_timestamp` — etl timestamp
- `vpc_group_desc` — vpc group desc

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dim_us.dim_pub_vpl_info`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dim_us.dim_pub_vpl_info"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_vpl_info` | Primary catalog table documented from B Report contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from B Report contract v2. ETL step-by-step logic is not present in this wiki repository.

**Default analysis filters (important):**

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For `dw_us.dwd_disty_brpt_orders_pl_etl_mi` profitability pulls, still apply `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

---

## Caveats for interpretation

- Derived from B Report contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dim_us` documented as baseline.
- Entity disambiguation (vendor vs customer vs VPL): see `source/contracts/b-report-us/domain-knowledge.md`.
- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.
- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.
- No active conflicts on dimension grain or key semantics as of 2026-06-25.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_vpl_info.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dim_pub_vpl_info.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 22 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dim_pub_vpl_info.md`.*
