# FACT: Supplemental fact/context table used by select POS reports (`dm_us.dm_disty_sales_rio_sku_inv_loc`)

- artifact_type: etl_table
- artifact_id: dm_us.dm_disty_sales_rio_sku_inv_loc
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dm_us.dm_disty_sales_rio_sku_inv_loc`
- **Layer type:** DM
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dm_us.dm_disty_sales_rio_sku_inv_loc` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dm_disty_sales_rio_sku_inv_loc schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `dim_${country_code}.dim_pub_part_info` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `ods_${country_code}.ods_cis_corp_order_detail_hudi_rt` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `ods_${country_code}.ods_cis_corp_order_header_hudi_rt` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `all_alloc_sku` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `ods_${country_code}.ods_cis_corp_cws_cop_ship_progress` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `alloc_sku` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
- **upstream:** `rio_sku` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`
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
- Reporting: Vertica `dm_us.dm_disty_sales_rio_sku_inv_loc` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `oh.delete_date IS NULL AND od.delete_date IS NULL AND oh.ship_date IS NULL ) ,alloc_sku as (SELECT sku_no ,inv_type ,loc_no ,prod_type ,bundle_kit ,sum(CASE WHEN alloc_name = 'so_alloc_qty' THEN nv...` | Business | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `ccsp.order_type = 18` | Business | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `not EXISTS (SELECT 1 FROM alloc_sku alloc WHERE alloc.sku_no=rio.sku_no AND alloc.inv_type=rio.inv_type AND alloc.loc_no=rio.loc_no AND alloc.prod_type=rio.prod_type AND nvl(alloc.bundle_kit,'')=nv...` | Business | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py
```

### End-to-end flow
```mermaid
flowchart LR
  S0["dim_${country_code}.dim_pub_part_info"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S1["ods_${country_code}.ods_cis_corp_order_detail_hudi_rt"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S2["ods_${country_code}.ods_cis_corp_order_header_hudi_rt"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S3["all_alloc_sku"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S4["ods_${country_code}.ods_cis_corp_cws_cop_ship_progress"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S5["alloc_sku"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  S6["rio_sku"] --> T["dm_us.dm_disty_sales_rio_sku_inv_loc"]
```

### Base tables register
| Object | Role |
|--------|------|
| `dim_${country_code}.dim_pub_part_info` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_order_detail_hudi_rt` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_order_header_hudi_rt` | source / temp (FROM/JOIN) |
| `all_alloc_sku` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_cws_cop_ship_progress` | source / temp (FROM/JOIN) |
| `alloc_sku` | source / temp (FROM/JOIN) |
| `rio_sku` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dm_us.dm_disty_sales_rio_sku_inv_loc` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dim_${country_code}.dim_pub_part_info` | `ods_${country_code}.ods_cis_corp_order_detail_hudi_rt` | many:1 | `pm.sku_no` = `od.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:36`) |
| `ods_${country_code}.ods_cis_corp_order_detail_hudi_rt` | `ods_${country_code}.ods_cis_corp_order_header_hudi_rt` | many:1 | `oh.order_type` = `od.order_type`; `oh.order_no` = `od.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:37`) |
| `ods_${country_code}.ods_cis_corp_cws_cop_ship_progress` | `dim_${country_code}.dim_pub_part_info` | many:1 | `ccsp.sku_no` = `pm.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:83`) |
| `a` | `rio_sku` | many:1 (LEFT) | `a.sku_no` = `b.sku_no`; `a.inv_type` = `b.inv_type`; `a.loc_no` = `b.loc_no`; `a.prod_type` = `b.prod_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:104`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dm_us.dm_disty_sales_rio_sku_inv_loc`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sku_no` | `a.sku_no` | `sku_no` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:97` |
| `inv_type` | `a.inv_type` | `inv_type` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:98` |
| `loc_no` | `a.loc_no` | `loc_no` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:99` |
| `prod_type` | `a.prod_type` | `prod_type` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:100` |
| `bundle_kit` | `a.bundle_kit` | `bundle_kit` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:101` |
| `alloc_so` | `a.alloc_so` | `alloc_so` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:102` |
| `alloc_rio` | `a.alloc_rio` | `alloc_rio` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:103` |
| `alloc_kwo` | `a.alloc_kwo` | `alloc_kwo` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:104` |
| `avail_qty` | `a.avail_qty` | `avail_qty` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:105` |
| `rio_qty` | `b.rio_qty` | `rio_qty` | `alloc_sku`, `rio_sku` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:106` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `alloc_sku`, `rio_sku` | arithmetic | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py:107` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
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
| `dim_${country_code}.dim_pub_part_info` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `ods_${country_code}.ods_cis_corp_order_detail_hudi_rt` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `ods_${country_code}.ods_cis_corp_order_header_hudi_rt` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `all_alloc_sku` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `ods_${country_code}.ods_cis_corp_cws_cop_ship_progress` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `alloc_sku` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |
| `rio_sku` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/dm_disty_sales_rio_sku_inv_loc.py` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:136` |
| KB / contract ref: `source/contracts/pos/tables/dm_disty_sales_rio_sku_inv_loc.md` | `source/contracts/pos/tables/dm_disty_sales_rio_sku_inv_loc.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_rio_alloc_rds_18605.sql` | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_rio_alloc_rds_18605.sql:85` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:860` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_rio_alloc_rds_18605.md` | `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_rio_alloc_rds_18605.md:55` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.md` | `target/knowledgebase/RDS/vertica_inventory/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.md:166` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:50` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dm_disty_sales_rio_sku_inv_loc/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_rio_sku_inv_loc.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dm_disty_sales_rio_sku_inv_loc.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_disty_sales_rio_sku_inv_loc` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dm_us.dm_disty_sales_rio_sku_inv_loc` | `dm_us.dm_disty_sales_rio_sku_inv_loc` | overwrite / incremental | POS contract `dm_disty_sales_rio_sku_inv_loc.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_disty_sales_rio_sku_inv_loc` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_disty_sales_rio_sku_inv_loc`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `sku_no`, `loc_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_sales_rio_sku_inv_loc
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT sku_no, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_sales_rio_sku_inv_loc
WHERE date_flag = '${partition_value}'
GROUP BY sku_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sku_no, loc_no, order_line_no, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_sales_rio_sku_inv_loc
WHERE date_flag = '${partition_value}'
GROUP BY sku_no, loc_no, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `avail_qty` — avail qty
- `rio_qty` — rio qty

### Dimension and key columns

- `sku_no` — sku no
- `inv_type` — inv type
- `loc_no` — loc no
- `prod_type` — prod type
- `bundle_kit` — bundle kit
- `alloc_so` — alloc so
- `alloc_rio` — alloc rio
- `alloc_kwo` — alloc kwo
- `etl_timestamp` — etl timestamp

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_disty_sales_rio_sku_inv_loc`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dm_us.dm_disty_sales_rio_sku_inv_loc"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_disty_sales_rio_sku_inv_loc` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_rio_sku_inv_loc.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dm_disty_sales_rio_sku_inv_loc.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 11 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_sales_rio_sku_inv_loc.md`.*