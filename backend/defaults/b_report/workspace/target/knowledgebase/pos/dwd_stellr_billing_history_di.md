# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_stellr_billing_history_di`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_stellr_billing_history_di.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_stellr_billing_history_di` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_stellr_billing_history_di` | `dw_us.dwd_stellr_billing_history_di` | overwrite / incremental | POS contract `dwd_stellr_billing_history_di.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_stellr_billing_history_di` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_stellr_billing_history_di`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `vend_no`, `eu_no`, `reseller_no`, `to_acct_no`, `subscription_id`, `customer_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vend_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY vend_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vend_no, eu_no, reseller_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, eu_no, reseller_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `order_qty` — order qty
- `msrp` — msrp
- `unit_cost` — unit cost
- `unit_price` — unit price
- `unit_tax` — unit tax
- `unit_rebate` — unit rebate
- `ext_price` — ext price
- `total_price` — total price
- `order_tax` — order tax
- `order_total` — order total
- `fx_msrp` — fx msrp
- `fx_unit_cost` — fx unit cost
- `fx_unit_price` — fx unit price
- `fx_unit_tax` — fx unit tax
- `fx_unit_rebate` — fx unit rebate
- `fx_ext_price` — fx ext price
- `fx_total_price` — fx total price
- `fx_order_tax` — fx order tax
- `fx_order_total` — fx order total
- `rate_to_usd` — rate to usd
- `usd_order_total` — usd order total
- `eu_price` — eu price
- `ext_eu_price` — ext eu price
- `fx_eu_price` — fx eu price
- `fx_ext_eu_price` — fx ext eu price
- ... and 2 additional measure columns (see column register)

### Dimension and key columns

- `vend_no` — vend no
- `vend_name` — vend name
- `eu_no` — eu no
- `eu_name` — eu name
- `reseller_no` — reseller no
- `reseller_name` — reseller name
- `to_acct_no` — to acct no
- `subscription_id` — subscription id
- `customer_id` — customer id
- `domain_name` — domain name
- `local_currency` — local currency
- `fx_currency` — fx currency
- `offer_type` — offer type
- `contract_no` — contract no
- `contract_type` — contract type
- `contract_line_no` — contract line no
- `bill_model` — bill model
- `billing_frequency` — billing frequency
- `fixed_bill_type` — fixed bill type
- `order_no` — order no
- `order_type` — order type
- `order_line_no` — order line no
- `sales_model` — sales model
- `invoice_date` — invoice date
- `close_date` — close date
- `billing_period` — billing period
- `billing_start_date` — billing start date
- `billing_end_date` — billing end date
- `sku_no` — sku no
- `sku_desc` — sku desc

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_stellr_billing_history_di`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_stellr_billing_history_di"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_stellr_billing_history_di` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_stellr_billing_history_di.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 100 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md`.*
