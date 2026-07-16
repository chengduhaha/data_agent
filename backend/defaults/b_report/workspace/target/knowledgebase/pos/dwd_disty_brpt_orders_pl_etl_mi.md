# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_brpt_orders_pl_etl_mi`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_brpt_orders_pl_etl_mi.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_brpt_orders_pl_etl_mi.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | overwrite / incremental | POS contract `dwd_disty_brpt_orders_pl_etl_mi.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_brpt_orders_pl_etl_mi`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_type`, `order_no`, `order_line_no`, `cust_no`, `mcust_no`, `from_loc_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_type, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = '${partition_value}'
GROUP BY order_type
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_type, order_no, order_line_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag = '${partition_value}'
GROUP BY order_type, order_no, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `base_cost` — base cost
- `sales_cost` — sales cost
- `ship_qty` — ship qty
- `u_price` — u price
- `u_cost` — u cost
- `u_sum_expense` — u sum expense
- `l_weight` — l weight
- `sales_total` — sales total
- `ap_finance` — ap finance
- `inv_cost` — inv cost
- `inv_reserve` — inv reserve
- `cr_risk_cterm` — cr risk cterm
- `flr_synnex` — flr synnex
- `direct_credit` — direct credit
- `csgn_edi_fee` — csgn edi fee
- `corporate` — corporate
- `sfs` — sfs
- `scm_risk` — scm risk
- `flr_vendor` — flr vendor
- `cust_finance_sales` — cust finance sales
- `cust_pmt_disc` — cust pmt disc
- `cvr_rm` — cvr rm
- `ar_fin_recovery` — ar fin recovery
- `mfg_oh` — mfg oh
- `cust_finance` — cust finance
- ... and 54 additional measure columns (see column register)

### Dimension and key columns

- `date_flag` — date flag
- `virtual_type` — virtual type
- `order_type` — order type
- `order_no` — order no
- `order_line_no` — order line no
- `cust_no` — cust no
- `mcust_no` — mcust no
- `cust_terr` — cust terr
- `cust_type` — cust type
- `sales_rep` — sales rep
- `from_loc_no` — from loc no
- `terms` — terms
- `gv_user_type` — gv user type
- `sku_no` — sku no
- `prod_code` — prod code
- `vpl_no` — vpl no
- `vend_no` — vend no
- `inv_type` — inv type
- `cust_program_id` — cust program id
- `ap_finance_calcproc` — ap finance calcproc
- `inv_reserve_calcproc` — inv reserve calcproc
- `cr_risk_cterm_calcproc` — cr risk cterm calcproc
- `flr_synnex_calcproc` — flr synnex calcproc
- `direct_credit_calcproc` — direct credit calcproc
- `csgn_edi_fee_calcproc` — csgn edi fee calcproc
- `corporate_calcproc` — corporate calcproc
- `sfs_calcproc` — sfs calcproc
- `scm_risk_calcproc` — scm risk calcproc
- `flr_vendor_calcproc` — flr vendor calcproc
- `cust_finance_sales_calcproc` — cust finance sales calcproc

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_brpt_orders_pl_etl_mi`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_brpt_orders_pl_etl_mi.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_brpt_orders_pl_etl_mi.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 172 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_brpt_orders_pl_etl_mi.md`.*
