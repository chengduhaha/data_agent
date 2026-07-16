# DWD: US B Report shipped-order profitability and performance analytics (`dw_us.dwd_disty_brpt_orders_pl_di`)

**Domain:** b-report-us  
**Source contract:** `source/contracts/b-report-us/tables/dwd_disty_brpt_orders_pl_di.md`  
**Knowledgebase path:** `target/knowledgebase/b-report-us/dwd_disty_brpt_orders_pl_di.md`

## Business purpose

US B Report shipped-order profitability and performance analytics

This document is derived from the B Report US table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_brpt_orders_pl_di` — DWD layer table used in US B Report analytics (`US B Report baseline`). |
| **Consumption** | Queried from Vertica/Hive for profitability, P&L, and operating performance reporting. |

**Parameters:** Country schema pattern `dw_us` (US baseline documented as `dw_us` / `dm_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report semantic layer, dashboard queries, and BI users. |
| **Sales / PM / finance** | Shipped-order metrics, margin components, and dimension attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to B Report hub `dw_us.dwd_disty_brpt_orders_pl_etl_mi`. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dw_us.dwd_disty_brpt_orders_pl_di` | `dw_us.dwd_disty_brpt_orders_pl_di` | overwrite / incremental | B Report contract `dwd_disty_brpt_orders_pl_di.md:L1` | yes (B Report contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_brpt_orders_pl_di` | same as reporting table | - | B Report contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_brpt_orders_pl_di`** in Vertica for B Report reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from B Report contract column catalog.
- **Partition:** `date_flag` — business date filter for B Report reporting (per contract).
- **Natural key:** `order_no`, `order_line_no`, `cust_no`, `mcust_no`, `from_loc_no`, `sku_no`
- **Exclusions (reporting):** None documented in B Report contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_brpt_orders_pl_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_brpt_orders_pl_di
WHERE date_flag = '${partition_value}'
GROUP BY order_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_no, order_line_no, cust_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_brpt_orders_pl_di
WHERE date_flag = '${partition_value}'
GROUP BY order_no, order_line_no, cust_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `base_cost` — Base Cost
- `sales_cost` — Sales cost
- `ship_qty` — Ship Quantity
- `u_price` — Unit Price
- `u_cost` — Unit Cost
- `u_sum_expense` — Unit Sum Expense
- `l_weight` — line weight
- `sales_total` — sales total = (u_price + u_sum_expense) * ship_qty
- `ap_finance` — One of the PL items (AP finance expense)
- `inv_cost` — One of the PL items (Inventory aging expense)
- `inv_reserve` — One of the PL items (Inventory reserve value)
- `cr_risk_cterm` — Credit Risk Cost Associated with a Certain Customer
- `flr_synnex` — Flooring Charges fee Paid by SYNNEX
- `direct_credit` — Credit card processing expense with specific pay terms
- `csgn_edi_fee` — Consignment Business EDI Fee charged by SYNNEX
- `corporate` — One of the PL items (Corporate overhead expense)
- `sfs` — One of the PL items (SFS)
- `scm_risk` — One of the PL items (Risk accrual for incorrect SCM usage)
- `flr_vendor` — FLR_VENDOR
- `cust_finance_sales` — CUST_FINANCE_SALES
- `cust_pmt_disc` — Early payment discounts offered to and taken by customers (based on discounted payment terms)
- `cvr_rm` — Remainder sweep, it was combined into CUST_REBATE
- `ar_fin_recovery` — Charge back to software products which cost is raised due to long term payment like one year
- `mfg_oh` — The expense in GL(cost for headcount(PERSONNEL) + OVERHEAD)  -  total cost on orders & inventory
- `cust_finance` — Cost to SYNNEX to Finance Receivables from Customers
- ... and 35 additional measure columns (see column register)

### Dimension and key columns

- `virtual_type` — data virtual type: 0-normal order data, 1-virtual line data
- `order_type` — Order Type
- `order_no` — Order No.
- `order_line_no` — Order Line No.
- `cust_no` — Customer No.
- `mcust_no` — master customer No.
- `cust_terr` — customer territory
- `cust_type` — cust type
- `sales_rep` — Sales Representative
- `from_loc_no` — From Location Addr No.
- `terms` — Customer Credit Level
- `gv_user_type` — Government User Type
- `sku_no` — SKU(Stock Keeping Unit) No.
- `prod_code` — Product Code
- `vpl_no` — vendor product line No.
- `vend_no` — Vendor No.
- `inv_type` — Invoice Type
- `cust_program_id` — The id of b report cust Program
- `ap_finance_calcproc` — calculation process of item ap_finance
- `inv_cost_calcproc` — calculation process of item inv_cost
- `inv_reserve_calcproc` — calculation process of item inv_reserve
- `cr_risk_cterm_calcproc` — calculation process of item cr_risk_cterm
- `flr_synnex_calcproc` — calculation process of item flr_synnex
- `direct_credit_calcproc` — calculation process of item direct_credit
- `csgn_edi_fee_calcproc` — calculation process of item csgn_edi_fee
- `corporate_calcproc` — calculation process of item corporate
- `sfs_calcproc` — calculation process of item sfs
- `scm_risk_calcproc` — calculation process of item scm_risk
- `flr_vendor_calcproc` — calculation process of item flr_vendor
- `cust_finance_sales_calcproc` — calculation process of item cust_finance_sales

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the B Report contract catalog (see **Data you can fetch** above). See also `source/contracts/b-report-us/metric-index.md` for metric definitions.

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_brpt_orders_pl_di`  
**Load pattern:** Not documented in repository

1. Upstream: Not documented in repository
2. Table available in Hive and Vertica for B Report consumption.
3. Downstream: B Report serving tables, dashboards, and exports

```mermaid
flowchart LR
  upstream[Upstream B Report or DIM loads]
  tgt["dw_us.dwd_disty_brpt_orders_pl_di"]
  brpt[B Report consumers]
  upstream --> tgt
  tgt --> brpt
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_brpt_orders_pl_di` | Primary catalog table documented from B Report contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from B Report contract v2. ETL step-by-step logic is not present in this wiki repository.

**Default analysis filters (important):**

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For `dw_us.dwd_disty_brpt_orders_pl_etl_mi` profitability pulls, still apply `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

---

## Caveats for interpretation

- Derived from B Report contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dw_us` documented as baseline.
- Entity disambiguation (vendor vs customer vs VPL): see `source/contracts/b-report-us/domain-knowledge.md`.
- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).
- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.
- Conflict item:

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract source | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dwd_disty_brpt_orders_pl_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| B Report consumers | `dwd_disty_brpt_orders_pl_di.md:L6` — see contract L6 |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 134 (B Report contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from B Report contract `source/contracts/b-report-us/tables/dwd_disty_brpt_orders_pl_di.md`.*
