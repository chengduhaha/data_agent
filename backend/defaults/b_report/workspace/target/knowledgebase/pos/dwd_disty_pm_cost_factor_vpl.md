# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_pm_cost_factor_vpl`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_pm_cost_factor_vpl.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_pm_cost_factor_vpl.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_pm_cost_factor_vpl` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_pm_cost_factor_vpl` | `dw_us.dwd_disty_pm_cost_factor_vpl` | overwrite / incremental | POS contract `dwd_disty_pm_cost_factor_vpl.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_pm_cost_factor_vpl` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_pm_cost_factor_vpl`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `month` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `vpl_no`, `pm_btl_scm_no`, `frt_in_scm_no`, `frt_out_scm_no`, `entry_id`, `safy_btl_scm_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT month, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_pm_cost_factor_vpl
WHERE month = '${partition_value}'
GROUP BY month;

-- 2) Metric sum by business dimension (top N)
SELECT vpl_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_pm_cost_factor_vpl
WHERE month = '${partition_value}'
GROUP BY vpl_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vpl_no, pm_btl_scm_no, frt_in_scm_no, month, COUNT(*) AS cnt
FROM dw_us.dwd_disty_pm_cost_factor_vpl
WHERE month = '${partition_value}'
GROUP BY vpl_no, pm_btl_scm_no, frt_in_scm_no, month
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `pm_btl_rate` — pm btl rate
- `sale_btl_rate` — sale btl rate
- `pdt_rate` — pdt rate
- `frt_in_cost_rate` — frt in cost rate
- `frt_in_load_rate` — frt in load rate
- `frt_out_load_rate` — frt out load rate
- `pm_pdt_rate` — pm pdt rate
- `inv_reserve_rate` — inv reserve rate
- `scm_risk_rate` — scm risk rate
- `max_btl_rate` — max btl rate
- `safty_btl_rate` — safty btl rate

### Dimension and key columns

- `month` — month
- `vpl_no` — vpl no
- `u_version` — u version
- `pm_btl_scm_no` — pm btl scm no
- `frt_in_scm_no` — frt in scm no
- `frt_out_scm_no` — frt out scm no
- `reason_code` — reason code
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `safy_btl_scm_no` — safy btl scm no

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_pm_cost_factor_vpl`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_pm_cost_factor_vpl"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_pm_cost_factor_vpl` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_pm_cost_factor_vpl.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_pm_cost_factor_vpl.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 21 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_pm_cost_factor_vpl.md`.*
