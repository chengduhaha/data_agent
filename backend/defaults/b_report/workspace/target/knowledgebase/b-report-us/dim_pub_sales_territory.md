# DIM: US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy (`dim_us.dim_pub_sales_territory`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dim_pub_sales_territory.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dim_pub_sales_territory.md`

## Business purpose

US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dim_us.dim_pub_sales_territory` — DIM layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dim_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report `pl_extend` / `cust_mtd` pre-load, `dim_pub_customer_info` territory enrichment, territory serving marts (`dws_disty_brpt_terr_*`). |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_sales_territory` | `dim_us.dim_pub_sales_territory` | overwrite / incremental | B Report contract `dim_pub_sales_territory.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dim_us.dim_pub_sales_territory` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dim_us.dim_pub_sales_territory`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** `date_flag` — business date filter for B Report reporting (per contract).
- **Natural key:** `sales_terr`, `entry_id`, `cust_type`, `group_id`, `primary_id`, `backup_id1`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT sales_terr, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY sales_terr
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sales_terr, entry_id, cust_type, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY sales_terr, entry_id, cust_type, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `primary_pcnt` — primary pcnt
- `backup_pcnt1` — backup pcnt1
- `backup_pcnt2` — backup pcnt2
- `backup_pcnt3` — backup pcnt3
- `backup_pcnt4` — backup pcnt4
- `backup_pcnt5` — backup pcnt5
- `backup_pcnt6` — backup pcnt6
- `backup_pcnt7` — backup pcnt7

### Dimension and key columns

- `sales_terr` — sales territory id
- `terr_name` — territory display name
- `region` — region
- `start_date` — start date
- `end_date` — end date
- `reviewer` — reviewer
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `cust_type` — customer sales type
- `group_id` — territory group id
- `primary_id` — primary sales rep id
- `backup_id1` — backup sales rep id 1
- `backup_id2` — backup sales rep id 2
- `backup_id3` — backup sales rep id 3
- `sub_group_id` — sub group id
- `cred_analyst` — cred analyst
- `backup_id4` — backup sales rep id 4
- `backup_id5` — backup sales rep id 5
- `backup_id6` — backup sales rep id 6
- `backup_id7` — backup sales rep id 7
- `house` — house
- `etl_timestamp` — etl timestamp
- `sub_group_desc` — sub group desc
- `group_desc` — group desc
- `date_flag` — date flag

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dim_us.dim_pub_sales_territory`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dim_us.dim_pub_sales_territory"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_sales_territory` | Primary catalog table documented from B Report contract |

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
- Verify row count stability day-over-day on active Vertica snapshot (~2,800 territories; slow growth as CIS adds territories).
- Monitor duplicate-key risk on `sales_terr` — must be unique per `date_flag` snapshot.
- For `terr_name`, spot-check null rate (20 nulls observed) and duplicate labels mapping to multiple `sales_terr` values.
- When joining from facts on `cust_terr`, validate match rate against `date_flag`-aligned `dim_pub_sales_territory_df` for historical months.
- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.
- No active conflicts on dimension grain or key semantics as of 2026-06-26.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_sales_territory.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dim_pub_sales_territory.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 33 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dim_pub_sales_territory.md`.*
