# PRIMARY: POS enrichment partner table joined from hub (`dw_us.dwd_disty_common_cpo_header`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_cpo_header.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_common_cpo_header.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_common_cpo_header` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_common_cpo_header` | `dw_us.dwd_disty_common_cpo_header` | overwrite / incremental | POS contract `dwd_disty_common_cpo_header.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_common_cpo_header` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_common_cpo_header`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `cpo_id`, `mcust_no`, `cust_no`, `cpo_no`, `cpo_entry_id`, `cpo_change_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_common_cpo_header
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT cpo_id, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_common_cpo_header
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT cpo_id, mcust_no, cust_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_common_cpo_header
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id, mcust_no, cust_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `cpo_total_taxable` — cpo total taxable
- `cpo_total_notax` — cpo total notax
- `cpo_sales_tax` — cpo sales tax
- `cpo_freight` — cpo freight
- `cpo_other` — cpo other
- `cpo_so_total` — cpo so total
- `cpo_bo_total` — cpo bo total
- `po_total` — po total

### Dimension and key columns

- `cpo_id` — cpo id
- `mcust_no` — mcust no
- `mcust_name` — mcust name
- `cust_no` — cust no
- `cust_name` — cust name
- `cpo_no` — cpo no
- `cpo_sales_terr` — cpo sales terr
- `cpo_priority` — cpo priority
- `cpo_status` — cpo status
- `cpo_date` — cpo date
- `cpo_pay_terms` — cpo pay terms
- `cpo_from_ref_type` — cpo from ref type
- `cpo_entry_id` — cpo entry id
- `created_by` — created by
- `cpo_entry_datetime` — cpo entry datetime
- `cpo_change_id` — cpo change id
- `cpo_change_date` — cpo change date
- `cpo_delete_id` — cpo delete id
- `cpo_delete_datetime` — cpo delete datetime
- `cpo_ship_method` — cpo ship method
- `cpo_ship_loc_type` — cpo ship loc type
- `end_user_po_no` — end user po no
- `special_handle` — special handle
- `ship_name1` — ship name1
- `ship_addr1` — ship addr1
- `ship_addr2` — ship addr2
- `ship_zipcode` — ship zipcode
- `ship_country` — ship country
- `ship_city` — ship city
- `ship_contact` — ship contact

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_common_cpo_header`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_common_cpo_header"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_common_cpo_header` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_cpo_header.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_common_cpo_header.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 62 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_cpo_header.md`.*
