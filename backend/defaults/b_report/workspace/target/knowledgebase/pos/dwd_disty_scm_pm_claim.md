# PRIMARY: POS enrichment partner table joined from hub (`dw_us.dwd_disty_scm_pm_claim`)

**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_scm_pm_claim.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_scm_pm_claim` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_scm_pm_claim` | `dw_us.dwd_disty_scm_pm_claim` | overwrite / incremental | POS contract `dwd_disty_scm_pm_claim.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_scm_pm_claim` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_scm_pm_claim`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `project_no`, `claim_no`, `vend_no`, `loc_no`, `pri_approv_ref_no`, `entry_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT project_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY project_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT project_no, claim_no, vend_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY project_no, claim_no, vend_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `budget_amount` — budget amount
- `actual_amount` — actual amount
- `pri_approv_amt` — pri approv amt
- `foreign_bug_amount` — foreign bug amount
- `foreign_act_amount` — foreign act amount
- `exp_amt` — exp amt
- `foreign_exp_amt` — foreign exp amt
- `foreign_approv_amt` — foreign approv amt
- `accrual_amt` — accrual amt
- `percentage` — percentage

### Dimension and key columns

- `project_no` — project no
- `claim_no` — claim no
- `claim_descr` — claim descr
- `claim_type` — claim type
- `expect_date` — expect date
- `posting_date` — posting date
- `vend_no` — vend no
- `loc_no` — loc no
- `pm_code` — pm code
- `pri_approv_ref_no` — pri approv ref no
- `doc_terms` — doc terms
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `entry_obj` — entry obj
- `delete_date` — delete date
- `delete_id` — delete id
- `delete_obj` — delete obj
- `contact_no` — contact no
- `inv_date` — inv date
- `vend_comments` — vend comments
- `vpl_no` — vpl no
- `vpc_group_id` — vpc group id
- `last_claim` — last claim
- `claim_start_date` — claim start date
- `claim_end_date` — claim end date
- `credit_note` — credit note
- `claim_code` — claim code
- `claim_curr` — claim curr
- `vend_src` — vend src
- `vend_src_ref_no` — vend src ref no

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_scm_pm_claim`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_scm_pm_claim"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_scm_pm_claim` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_scm_pm_claim.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 51 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md`.*
