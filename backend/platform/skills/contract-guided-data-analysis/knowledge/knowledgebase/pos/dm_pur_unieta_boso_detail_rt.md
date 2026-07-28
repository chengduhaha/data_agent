# FACT: Supplemental fact/context table used by select POS reports (`dm_us.dm_pur_unieta_boso_detail_rt`)

- artifact_type: etl_table
- artifact_id: dm_us.dm_pur_unieta_boso_detail_rt
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/
- related_etl_scripts:
- `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_pur_unieta_boso_detail_hf.sql`

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dm_us.dm_pur_unieta_boso_detail_rt`
- **Layer type:** DM
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dm_us.dm_pur_unieta_boso_detail_rt` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dm_pur_unieta_boso_detail_rt schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql`
- **upstream:** `PATH` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
- Parameters / date window: see ETL `${literal_*}` / `${date_flag}` / `${start_date}` in evidence script.
- Schedule: Not documented in repository

## L2 Declarative Knowledge

### Business purpose
See preserved **Business purpose** below when present (POS contract catalog + linked ETL).

### Audience and use cases
See preserved **Who it helps** section when present.

### Fact key resolution
See preserved **Grain and keys** when present.

### Time field semantics
- Prefer partition / `date_flag` filters documented in preserved sections and L3 Key filters from ETL.

### Metrics served
See preserved Metrics / column groups when present; otherwise L3 column derivations.

### Metric serving map
N/A unless multi-period wide table (see preserved content).

### etl_metrics
No new metric-index formulas appended in this bitbucket-etl upgrade pass.

## L3 Procedural Knowledge

### Query and routing rules
- Reporting: Vertica `dm_us.dm_pur_unieta_boso_detail_rt` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["PATH"] --> T["dm_us.dm_pur_unieta_boso_detail_rt"]
```

### Base tables register
| Object | Role |
|--------|------|
| `PATH` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dm_us.dm_pur_unieta_boso_detail_rt` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dm_us.dm_pur_unieta_boso_detail_rt`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| — | — | — | — | — | No SELECT-list derivations parsed from `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql` |


### Sentinel and code values
See preserved content and ETL CASE expressions in column derivations.

## L4 Validation

### Resolved partition value
- Partition / date parameters from ETL literals — concrete calendar values Not documented in repository (resolve via Azkaban when flow evidence exists).

### Data quality checks
See preserved Validation SQL when present.

### Validation SQL
Prefer preserved Vertica validation bundle when present; MCP business SQL not re-run during documentation.

### Caveats for interpretation
- Document upgraded additively from POS **contract** MD + **bitbucket-etl** SQL. Prior contract text is under **Preserved pre-L1-L6 content** when present.

### Conflicts and open questions
- Companion loader scripts may also appear under other domain KB folders; see `target/knowledgebase/pos/readme.md` cross-links.

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql` |
| Report | Vertica | preserved POS contract when present |

### Access constraints
Not documented in repository

### Query risk profile
- Always filter `date_flag` / documented partition keys before wide scans.

## L6 Access and Consumption

### Primary consumers and use cases
See preserved audience / POS report consumers when present.

### Representative query patterns
See preserved Validation SQL / contract examples when present.

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `PATH` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/dm_us.dm_pur_unieta_boso_detail_rt.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:138` |
| ETL/script ref: `source/contracts/pos/bitbucket-etl/dwd_disty_sales_open_order_detail/loading_open_orders_data.sql` | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_open_order_detail/loading_open_orders_data.sql:455` |
| KB / contract ref: `source/contracts/pos/tables/dm_pur_unieta_boso_detail_rt.md` | `source/contracts/pos/tables/dm_pur_unieta_boso_detail_rt.md:5` |
| ETL/script ref: `source/contracts/rds/starrocks_cpo/etl/cpo_open_order_eta_ship_complete_contacts_rds_6560.sql` | `source/contracts/rds/starrocks_cpo/etl/cpo_open_order_eta_ship_complete_contacts_rds_6560.sql:27` |
| ETL/script ref: `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql` | `source/contracts/rds/starrocks_cpo/etl/cpo_order_status_eta_hideampl_expense_rds_19257.sql:70` |
| ETL/script ref: `source/contracts/rds/starrocks_inventory/etl/inv_consignment_address_default_wh_rds_7026.sql` | `source/contracts/rds/starrocks_inventory/etl/inv_consignment_address_default_wh_rds_7026.sql:228` |
| ETL/script ref: `source/contracts/rds/starrocks_inventory/etl/inv_multisheet_dos_bo_rds_14059.sql` | `source/contracts/rds/starrocks_inventory/etl/inv_multisheet_dos_bo_rds_14059.sql:178` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_basic_bo_unieta_inventory_rds_5987.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_basic_bo_unieta_inventory_rds_5987.sql:57` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_brpt_snapshot_profile_rds_8700.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_brpt_snapshot_profile_rds_8700.sql:12` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_customer_sku_serial_inventory_rds_14053.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_customer_sku_serial_inventory_rds_14053.sql:102` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_multisheet_eta_expense_rds_6143.sql:40` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_open_shipped_tracking_rds_8775.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_open_shipped_tracking_rds_8775.sql:11` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_rio_allocation_inventory_rds_6302.sql:343` |
| ETL/script ref: `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_status_eu_custom_vpo_chain_rds_17936.sql` | `source/contracts/rds/starrocks_open_so_bo/etl/open_so_bo_status_eu_custom_vpo_chain_rds_17936.sql:231` |
| ETL/script ref: `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_eta_sapid_shipped_open_rds_17695.sql` | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_eta_sapid_shipped_open_rds_17695.sql:21` |
| KB / contract ref: `source/contracts/rds/vertica_open_so_bo/examples-index.md` | `source/contracts/rds/vertica_open_so_bo/examples-index.md:31` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_cpo/cpo_open_order_eta_ship_complete_contacts_rds_6560.md` | `target/knowledgebase/RDS/starrocks_cpo/cpo_open_order_eta_ship_complete_contacts_rds_6560.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_cpo/cpo_order_status_eta_hideampl_expense_rds_19257.md` | `target/knowledgebase/RDS/starrocks_cpo/cpo_order_status_eta_hideampl_expense_rds_19257.md:51` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_inventory/inv_consignment_address_default_wh_rds_7026.md` | `target/knowledgebase/RDS/starrocks_inventory/inv_consignment_address_default_wh_rds_7026.md:178` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_inventory/inv_multisheet_dos_bo_rds_14059.md` | `target/knowledgebase/RDS/starrocks_inventory/inv_multisheet_dos_bo_rds_14059.md:55` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_basic_bo_unieta_inventory_rds_5987.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_basic_bo_unieta_inventory_rds_5987.md:56` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_brpt_snapshot_profile_rds_8700.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_brpt_snapshot_profile_rds_8700.md:51` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_customer_sku_serial_inventory_rds_14053.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_customer_sku_serial_inventory_rds_14053.md:60` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_multisheet_eta_expense_rds_6143.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_multisheet_eta_expense_rds_6143.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_open_shipped_tracking_rds_8775.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_open_shipped_tracking_rds_8775.md:51` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_rio_allocation_inventory_rds_6302.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_rio_allocation_inventory_rds_6302.md:184` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_status_eu_custom_vpo_chain_rds_17936.md` | `target/knowledgebase/RDS/starrocks_open_so_bo/open_so_bo_status_eu_custom_vpo_chain_rds_17936.md:173` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_eta_sapid_shipped_open_rds_17695.md` | `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_eta_sapid_shipped_open_rds_17695.md:52` |
| KB / contract ref: `target/knowledgebase/pos/dwd_disty_sales_open_order_detail.md` | `target/knowledgebase/pos/dwd_disty_sales_open_order_detail.md:206` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:51` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dm_pur_unieta_boso_detail_rt/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_pur_unieta_boso_detail_rt.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dm_pur_unieta_boso_detail_rt.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_pur_unieta_boso_detail_rt` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dm_us.dm_pur_unieta_boso_detail_rt` | `dm_us.dm_pur_unieta_boso_detail_rt` | overwrite / incremental | POS contract `dm_pur_unieta_boso_detail_rt.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_pur_unieta_boso_detail_rt` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_pur_unieta_boso_detail_rt`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `order_no`, `order_type`, `order_line_no`, `loc_no`, `sub_kit_line_no`, `sku_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_pur_unieta_boso_detail_rt
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_no, COUNT(*) AS row_cnt
FROM dm_us.dm_pur_unieta_boso_detail_rt
WHERE date_flag = '${partition_value}'
GROUP BY order_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_no, order_type, order_line_no, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_pur_unieta_boso_detail_rt
WHERE date_flag = '${partition_value}'
GROUP BY order_no, order_type, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `order_qty` — order qty
- `eta_qty` — eta qty

### Dimension and key columns

- `order_no` — order no
- `order_type` — order type
- `order_line_no` — order line no
- `loc_no` — loc no
- `inv_type` — inv type
- `sub_kit_line_no` — sub kit line no
- `sku_no` — sku no
- `eta_code` — eta code
- `track_no` — track no
- `ship_eta` — ship eta
- `deliver_eta` — deliver eta
- `eta` — eta
- `deliver_date` — deliver date
- `po_no` — po no
- `po_type` — po type
- `po_line_no` — po line no
- `eta_source` — eta source
- `ship_date` — ship date
- `rec_date` — rec date
- `sched_date` — sched date
- `sus_date` — sus date
- `rf_date` — rf date
- `alf_date` — alf date
- `inv_date` — inv date
- `status` — status
- `etl_timestamp` — etl timestamp
- `ai_log` — ai log
- `work_type` — work type

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_pur_unieta_boso_detail_rt`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dm_us.dm_pur_unieta_boso_detail_rt"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_pur_unieta_boso_detail_rt` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_pur_unieta_boso_detail_rt.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dm_pur_unieta_boso_detail_rt.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

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

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_pur_unieta_boso_detail_rt.md`.*