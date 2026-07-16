# PRIMARY: POS enrichment partner table joined from hub (`dw_us.dwd_pub_common_history_header_extend`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_pub_common_history_header_extend.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_pub_common_history_header_extend.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_pub_common_history_header_extend` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_pub_common_history_header_extend` | `dw_us.dwd_pub_common_history_header_extend` | overwrite / incremental | POS contract `dwd_pub_common_history_header_extend.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_pub_common_history_header_extend` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_pub_common_history_header_extend`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_type`, `order_no`, `from_acct_no`, `from_loc_no`, `from_contact_no`, `from_dept_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_pub_common_history_header_extend
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_type, COUNT(*) AS row_cnt
FROM dw_us.dwd_pub_common_history_header_extend
WHERE date_flag = '${partition_value}'
GROUP BY order_type
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_type, order_no, from_acct_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_pub_common_history_header_extend
WHERE date_flag = '${partition_value}'
GROUP BY order_type, order_no, from_acct_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `it_cost_code` — it cost code
- `sales_tax` — sales tax
- `total_order` — total order
- `total_cost` — total cost
- `sales_total` — sales total
- `head_exp_total` — head exp total
- `detail_exp_total` — detail exp total
- `total_weight` — total weight
- `detail_price_total` — detail price total
- `fx_total_order` — fx total order
- `fx_total_cost` — fx total cost
- `fx_sales_total` — fx sales total
- `fx_head_exp_total` — fx head exp total
- `fx_detail_exp_total` — fx detail exp total
- `fx_detail_price_total` — fx detail price total
- `frt` — frt
- `fds` — fds
- `fadd` — fadd
- `mof` — mof
- `cod` — cod
- `tax` — tax
- `taxc_all` — taxc all

### Dimension and key columns

- `order_type` — order type
- `order_no` — order no
- `from_acct_no` — from acct no
- `from_loc_no` — from loc no
- `from_contact_no` — from contact no
- `from_dept_no` — from dept no
- `from_inv_type` — from inv type
- `to_acct_no` — to acct no
- `to_loc_no` — to loc no
- `to_contact_no` — to contact no
- `to_dept_no` — to dept no
- `to_inv_type` — to inv type
- `ship_to_name` — ship to name
- `ship_to_addr` — ship to addr
- `ship_to_po_box` — ship to po box
- `ship_to_city` — ship to city
- `ship_to_state` — ship to state
- `ship_to_country` — ship to country
- `ship_to_zip` — ship to zip
- `account_rep` — account rep
- `mt_expense_code` — mt expense code
- `int_ref_no` — int ref no
- `int_ref_type` — int ref type
- `ext_ref` — ext ref
- `issue_date` — issue date
- `credit_rel_date` — credit rel date
- `pick_date` — pick date
- `manifest_date` — manifest date
- `ship_date` — ship date
- `invoice_date` — invoice date

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_pub_common_history_header_extend`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_pub_common_history_header_extend"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_pub_common_history_header_extend` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_pub_common_history_header_extend.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_pub_common_history_header_extend.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 145 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_pub_common_history_header_extend.md`.*
