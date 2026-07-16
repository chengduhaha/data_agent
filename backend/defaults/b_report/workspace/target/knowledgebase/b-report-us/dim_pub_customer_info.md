# DIM: US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy (`dim_us.dim_pub_customer_info`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dim_pub_customer_info.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dim_pub_customer_info.md`

## Business purpose

US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dim_us.dim_pub_customer_info` — DIM layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dim_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report order-line fact enrichment, `dws_disty_brpt_cust_mtd`, `pl_extend` customer labels. |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_customer_info` | `dim_us.dim_pub_customer_info` | overwrite / incremental | B Report contract `dim_pub_customer_info.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dim_us.dim_pub_customer_info` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dim_us.dim_pub_customer_info`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `mcust_no`, `cust_no`, `lead_id`, `resale_no`, `store_no`, `collector_id`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT mcust_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY mcust_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT mcust_no, cust_no, lead_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY mcust_no, cust_no, lead_id, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `outside_sales_rep` — outside sales rep
- `pending_amt` — pending amt
- `terr_email` — terr email

### Dimension and key columns

- `mcust_no` — mcust no
- `mcust_name` — mcust name
- `cust_no` — cust no
- `cust_name` — cust name
- `cust_type` — cust type
- `cust_type_descr` — cust type descr
- `cust_acct_type` — cust acct type
- `is_restricted` — is restricted
- `is_discontinued` — is discontinued
- `sales_terr` — sales terr
- `sales_terr_name` — sales terr name
- `sales_segment` — sales segment
- `division_desc` — division desc
- `lead_id` — lead id
- `profile_c` — profile c
- `outside_sales_rep_name` — outside sales rep name
- `bill_to_cust_addr` — bill to cust addr
- `bill_to_cust_zip` — bill to cust zip
- `bill_to_cust_city` — bill to cust city
- `bill_to_cust_state` — bill to cust state
- `bill_to_cust_country` — bill to cust country
- `bill_to_contact_name` — bill to contact name
- `bill_to_contact_email` — bill to contact email
- `bill_to_contact_phone` — bill to contact phone
- `bill_to_contact_title` — bill to contact title
- `resale_no` — resale no
- `store_no` — store no
- `default_terms` — default terms
- `currency` — currency
- `etl_timestamp` — etl timestamp

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dim_us.dim_pub_customer_info`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dim_us.dim_pub_customer_info"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_customer_info` | Primary catalog table documented from B Report contract |

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
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_customer_info.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dim_pub_customer_info.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 111 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dim_pub_customer_info.md`.*
