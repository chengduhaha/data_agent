# PRIMARY: POS enrichment partner table joined from hub (`dm_us.dm_disty_sales_open_cpo`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_open_cpo.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dm_disty_sales_open_cpo.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_disty_sales_open_cpo` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dm_us` (US baseline documented as `dw_us` / `dim_us`).

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
| **Query for reporting** | `dm_us.dm_disty_sales_open_cpo` | `dm_us.dm_disty_sales_open_cpo` | overwrite / incremental | POS contract `dm_disty_sales_open_cpo.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_disty_sales_open_cpo` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_disty_sales_open_cpo`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `cpo_id`, `cpo_no`, `cpo_cust_no`, `cpo_entry_id`, `end_user_po_no`, `ship_to_phone_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_sales_open_cpo
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT cpo_id, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_sales_open_cpo
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT cpo_id, cpo_no, cpo_cust_no, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_sales_open_cpo
WHERE date_flag = '${partition_value}'
GROUP BY cpo_id, cpo_no, cpo_cust_no, date_flag
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
- `probability` — probability
- `cpo_line_qty` — cpo line qty
- `cpo_allocated_qty` — cpo allocated qty
- `cpo_bo_qty` — cpo bo qty
- `cpo_so_qty` — cpo so qty
- `cpo_del_qty` — cpo del qty
- `cpo_ship_qty` — cpo ship qty
- `cpo_price` — cpo price
- `cpo_grid_price` — cpo grid price
- `cpo_unit_price` — cpo unit price
- `cpo_unit_cost` — cpo unit cost
- `cpo_extended_price` — cpo extended price
- `cpo_extended_cost` — cpo extended cost
- `cpo_gm_percent` — cpo gm percent
- `cpo_price_flag` — cpo price flag
- `cpo_grid_adj` — cpo grid adj
- `cis_unit_cost` — cis unit cost
- ... and 2 additional measure columns (see column register)

### Dimension and key columns

- `cpo_id` — cpo id
- `cpo_no` — cpo no
- `cpo_cust_no` — cpo cust no
- `cpo_cust_name` — cpo cust name
- `cpo_sales_terr` — cpo sales terr
- `cpo_entry_id` — cpo entry id
- `cpo_entry_name` — cpo entry name
- `cpo_entry_datetime` — cpo entry datetime
- `cpo_from_ref_type` — cpo from ref type
- `cpo_from_ref_type_desc` — cpo from ref type desc
- `system_type` — system type
- `cpo_pay_meth` — cpo pay meth
- `cpo_ship_method` — cpo ship method
- `cpo_ship_loc_type` — cpo ship loc type
- `end_user_po_no` — end user po no
- `special_handle` — special handle
- `ship_to_name` — ship to name
- `ship_to_addr1` — ship to addr1
- `ship_to_addr2` — ship to addr2
- `ship_to_zipcode` — ship to zipcode
- `ship_to_country` — ship to country
- `ship_to_city` — ship to city
- `ship_to_state` — ship to state
- `ship_to_contact` — ship to contact
- `ship_to_phone_no` — ship to phone no
- `frt_pay_type` — frt pay type
- `convert_datetime` — convert datetime
- `convert_user` — convert user
- `convert_user_name` — convert user name
- `sales_model` — sales model

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_disty_sales_open_cpo`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dm_us.dm_disty_sales_open_cpo"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_disty_sales_open_cpo` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dm_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_open_cpo.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dm_disty_sales_open_cpo.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 122 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_open_cpo.md`.*
