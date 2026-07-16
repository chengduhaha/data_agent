# DWD: US shipped POS order-line fact (`dw_us.dwd_disty_common_pos_di`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_pos_di.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_common_pos_di.md`

## Business purpose

US shipped POS order-line fact; driving table for Vertica RDS POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_common_pos_di` — DWD layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_common_pos_di` | `dw_us.dwd_disty_common_pos_di` | overwrite / incremental | POS contract `dwd_disty_common_pos_di.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_common_pos_di` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_common_pos_di`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_no`, `order_type`, `order_line_no`, `kit_line_no`, `synnex_po_no`, `mso_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_common_pos_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_common_pos_di
WHERE date_flag = '${partition_value}'
GROUP BY order_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_no, order_type, order_line_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_common_pos_di
WHERE date_flag = '${partition_value}'
GROUP BY order_no, order_type, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `ship_qty` — ship qty
- `unit_cost` — unit cost
- `extend_cost` — extend cost
- `base_cost` — base cost
- `extend_base_cost` — extend base cost
- `unit_price` — unit price
- `extend_price` — extend price
- `unit_sum_exp` — unit sum exp
- `extend_sum_exp` — extend sum exp
- `unit_net_price` — unit net price
- `extend_net_price` — extend net price
- `base_cost_shipment` — base cost shipment
- `extend_base_cost_shipment` — extend base cost shipment
- `base_cost_vpo` — base cost vpo
- `extend_base_cost_vpo` — extend base cost vpo
- `retail_price` — retail price
- `std_whls_price` — std whls price
- `gm_amt` — gm amt
- `ngm_amt` — ngm amt
- `oplgm_amt` — oplgm amt
- `base_cost_pocv` — base cost pocv
- `extend_cost_pocv` — extend cost pocv
- `order_qty` — order qty
- `tgm_amt` — tgm amt
- `spec_cost` — spec cost
- ... and 2 additional measure columns (see column register)

### Dimension and key columns

- `order_no` — order no
- `order_type` — order type
- `order_line_no` — order line no
- `kit_line_no` — kit line no
- `order_line_type` — order line type
- `synnex_po_no` — synnex po no
- `mso_no` — mso no
- `cpo_no` — cpo no
- `from_loc_no` — from loc no
- `from_loc_char` — from loc char
- `inv_type` — inv type
- `ship_method` — ship method
- `sku_no` — sku no
- `ship_date` — ship date
- `mfg_partno` — mfg partno
- `part_no` — part no
- `part_desc` — part desc
- `prod_code` — prod code
- `prod_type` — prod type
- `vpl_no` — vpl no
- `vpl_code` — vpl code
- `vpl_desc` — vpl desc
- `vend_no` — vend no
- `vend_name` — vend name
- `vend_currency` — vend currency
- `vend_segment` — vend segment
- `universal_vend_no` — universal vend no
- `universal_vend_name` — universal vend name
- `upc_code` — upc code
- `master_vpl_code` — master vpl code

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_common_pos_di`  
**Load pattern:** Not documented in repository

1. Upstream: Shipped order history and order detail sources via daily disty common POS ETL; enriches with customer, product, vendor, and territory attributes at load time
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), vendor/customer POS exports, SPA/SCM claim reports, serial/RMA tracing reports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_common_pos_di"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_common_pos_di` | Primary catalog table documented from POS contract |

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
- Confirm exact Azkaban flow name for daily POS hub load when reconciling SLA (next step: BAF schedule lookup).
- `unit_sum_exp` aggregation chain from SPA detail at ETL time vs report-time recalculation — confirm with report owner when amounts disagree.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_pos_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_common_pos_di.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), vendor/customer POS exports, SPA/SCM claim reports, serial/RMA tracing reports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 164 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_common_pos_di.md`.*
