# DLAKE: Inventory RIO request detail used by supplemental POS inventory reports (`dlake_dg.dwd_disty_inv_rio_request_header`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_rio_request_header.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_inv_rio_request_header.md`

## Business purpose

Inventory RIO request detail used by supplemental POS inventory reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dlake_dg.dwd_disty_inv_rio_request_header` — DLAKE layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dlake_dg` (US baseline documented as `dw_us` / `dim_us`).

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
| **Query for reporting** | `dlake_dg.dwd_disty_inv_rio_request_header` | `dlake_dg.dwd_disty_inv_rio_request_header` | overwrite / incremental | POS contract `dwd_disty_inv_rio_request_header.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dlake_dg.dwd_disty_inv_rio_request_header` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dlake_dg.dwd_disty_inv_rio_request_header`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `rio_req_no`, `sku_no`, `loc_no`, `cust_no`, `agent_no`, `hold_auth_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dlake_dg.dwd_disty_inv_rio_request_header
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT rio_req_no, COUNT(*) AS row_cnt
FROM dlake_dg.dwd_disty_inv_rio_request_header
WHERE date_flag = '${partition_value}'
GROUP BY rio_req_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT rio_req_no, sku_no, loc_no, date_flag, COUNT(*) AS cnt
FROM dlake_dg.dwd_disty_inv_rio_request_header
WHERE date_flag = '${partition_value}'
GROUP BY rio_req_no, sku_no, loc_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `req_qty` — req qty
- `approved_qty` — approved qty
- `pending_qty` — pending qty

### Dimension and key columns

- `rio_req_no` — rio req no
- `sku_no` — sku no
- `loc_no` — loc no
- `cust_no` — cust no
- `agent_no` — agent no
- `hold_auth_no` — hold auth no
- `entry_id` — entry id
- `entry_datetime` — entry datetime
- `reason` — reason
- `status` — status
- `type` — type
- `approve_id` — approve id
- `approve_datetime` — approve datetime
- `expected_inv_date` — expected inv date
- `end_date` — end date
- `vpl_no` — vpl no
- `reject_reason` — reject reason
- `kit_flag` — kit flag
- `update_enddate_flag` — update enddate flag
- `group_id` — group id
- `rio_parent_id` — rio parent id
- `ref_descr` — ref descr
- `forecast_source` — forecast source
- `update_id` — update id
- `update_reason` — update reason
- `company_no` — company no
- `region_no` — region no

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dlake_dg.dwd_disty_inv_rio_request_header`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dlake_dg.dwd_disty_inv_rio_request_header"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dlake_dg.dwd_disty_inv_rio_request_header` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dlake_dg` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_rio_request_header.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_inv_rio_request_header.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 30 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_rio_request_header.md`.*
