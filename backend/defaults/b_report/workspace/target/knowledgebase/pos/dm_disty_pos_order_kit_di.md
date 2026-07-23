# PRIMARY: POS enrichment partner table joined from hub (`dm_us.dm_disty_pos_order_kit_di`)

- artifact_type: etl_table
- artifact_id: dm_us.dm_disty_pos_order_kit_di
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/
- related_etl_scripts:
- `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit_hyve.sql`

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dm_us.dm_disty_pos_order_kit_di`
- **Layer type:** DM
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dm_us.dm_disty_pos_order_kit_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dm_disty_pos_order_kit_di schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `dw_${country}.dwd_disty_sales_single_orders_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `dim_${country}.dim_pub_part_info` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `dw_${country}.dwd_disty_brpt_orders_pl_etl_mi` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `dw_${country}.dwd_disty_sales_comp_orders_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `order_list` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `temp_tgm_amt` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
- **upstream:** `temp_order_details` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`
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
- Reporting: Vertica `dm_us.dm_disty_pos_order_kit_di` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `part.prod_type in ('A','K') and fact.terr_status='n' and fact.date_flag BETWEEN '${start_date}' and '${end_date}' ) , temp_tgm_amt ( select pl.date_flag ,pl.dt_month ,pl.order_type ,pl.order_no ,pl...` | Technical (load only) / Business | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["dw_${country}.dwd_disty_sales_single_orders_di"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S1["dim_${country}.dim_pub_part_info"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S2["dw_${country}.dwd_disty_brpt_orders_pl_etl_mi"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S3["dw_${country}.dwd_disty_sales_comp_orders_di"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S4["order_list"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S5["temp_tgm_amt"] --> T["dm_us.dm_disty_pos_order_kit_di"]
  S6["temp_order_details"] --> T["dm_us.dm_disty_pos_order_kit_di"]
```

### Base tables register
| Object | Role |
|--------|------|
| `dw_${country}.dwd_disty_sales_single_orders_di` | source / temp (FROM/JOIN) |
| `dim_${country}.dim_pub_part_info` | source / temp (FROM/JOIN) |
| `dw_${country}.dwd_disty_brpt_orders_pl_etl_mi` | source / temp (FROM/JOIN) |
| `dw_${country}.dwd_disty_sales_comp_orders_di` | source / temp (FROM/JOIN) |
| `order_list` | source / temp (FROM/JOIN) |
| `temp_tgm_amt` | source / temp (FROM/JOIN) |
| `temp_order_details` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dm_us.dm_disty_pos_order_kit_di` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dw_${country}.dwd_disty_sales_single_orders_di` | `dim_${country}.dim_pub_part_info` | many:1 | `fact.sku_no` = `part.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:13`) |
| `dw_${country}.dwd_disty_sales_comp_orders_di` | `dim_${country}.dim_pub_part_info` | many:1 | `com.sku_no` = `part.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:75`) |
| `dw_${country}.dwd_disty_sales_comp_orders_di` | `order_list` | many:1 | `com.order_type` = `ol.order_type`; `com.order_no` = `ol.order_no`; `com.kit_line_no` = `ol.order_line_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:77`) |
| `dw_${country}.dwd_disty_sales_comp_orders_di` | `temp_tgm_amt` | many:1 | `com.order_type` = `tta.order_type`; `com.order_no` = `tta.order_no`; `com.order_line_no` = `tta.order_line_no`; `com.date_flag` = `tta.date_flag` | etl_sql (`source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:81`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dm_us.dm_disty_pos_order_kit_di`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `order_type` | `order_type` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:7` |
| `order_no` | `order_no` | `order_no` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:8` |
| `order_line_no` | `order_line_no` | `order_line_no` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:9` |
| `extend_net_price` | `fact.ship_qty * (fact.u_price + nvl (fact.u_sum_expense, 0))` | `ship_qty`, `u_price`, `u_sum_expense` | `order_list`, `temp_order_details` | coalesce | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:10` |
| `ship_qty` | `ship_qty` | `ship_qty` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:10` |
| `NGM_amt` | `NGM_amt` | `NGM_amt` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:26` |
| `oplgm_amt` | `oplgm_amt` | `oplgm_amt` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:27` |
| `tgm_amt` | `tgm_amt` | `tgm_amt` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:19` |
| `ngm_percent` | `ngm_percent` | `ngm_percent` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:52` |
| `oplgm_percent` | `oplgm_percent` | `oplgm_percent` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:53` |
| `tgm_percent` | `tgm_percent` | `tgm_percent` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:54` |
| `base_cost` | `base_cost` | `base_cost` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:55` |
| `extend_base_cost` | `extend_base_cost` | `extend_base_cost` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:56` |
| `base_cost_shipment` | `base_cost_shipment` | `base_cost_shipment` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:60` |
| `extend_base_cost_shipment` | `extend_base_cost_shipment` | `extend_base_cost_shipment` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:64` |
| `base_cost_vpo` | `base_cost_vpo` | `base_cost_vpo` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:67` |
| `base_cost_pocv` | `base_cost_pocv` | `base_cost_pocv` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:68` |
| `extend_cost_vpo` | `extend_cost_vpo` | `extend_cost_vpo` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:71` |
| `extend_cost_pocv` | `extend_cost_pocv` | `extend_cost_pocv` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:72` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `temp_order_details` | arithmetic | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:117` |
| `oplgm_plus_amt` | `oplgm_plus_amt` | `oplgm_plus_amt` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:37` |
| `date_flag` | `date_flag` | `date_flag` | `temp_order_details` | passthrough | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql:6` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
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
| `dw_${country}.dwd_disty_sales_single_orders_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `dim_${country}.dim_pub_part_info` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `dw_${country}.dwd_disty_brpt_orders_pl_etl_mi` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `dw_${country}.dwd_disty_sales_comp_orders_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `order_list` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `temp_tgm_amt` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |
| `temp_order_details` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/loading_pos_order_kit.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:118` |
| KB / contract ref: `source/contracts/pos/tables/dm_disty_pos_order_kit_di.md` | `source/contracts/pos/tables/dm_disty_pos_order_kit_di.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:409` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql:409` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md:175` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md:175` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:46` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dm_disty_pos_order_kit_di/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pos_order_kit_di.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dm_disty_pos_order_kit_di.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dm_us.dm_disty_pos_order_kit_di` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dm_us.dm_disty_pos_order_kit_di` | `dm_us.dm_disty_pos_order_kit_di` | overwrite / incremental | POS contract `dm_disty_pos_order_kit_di.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dm_us.dm_disty_pos_order_kit_di` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dm_us.dm_disty_pos_order_kit_di`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_type`, `order_no`, `order_line_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_pos_order_kit_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_type, COUNT(*) AS row_cnt
FROM dm_us.dm_disty_pos_order_kit_di
WHERE date_flag = '${partition_value}'
GROUP BY order_type
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_type, order_no, order_line_no, date_flag, COUNT(*) AS cnt
FROM dm_us.dm_disty_pos_order_kit_di
WHERE date_flag = '${partition_value}'
GROUP BY order_type, order_no, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `extend_net_price` — extend net price
- `ship_qty` — ship qty
- `ngm_amt` — ngm amt
- `oplgm_amt` — oplgm amt
- `tgm_amt` — tgm amt
- `ngm_percent` — ngm percent
- `oplgm_percent` — oplgm percent
- `tgm_percent` — tgm percent
- `base_cost` — base cost
- `extend_base_cost` — extend base cost
- `base_cost_shipment` — base cost shipment
- `extend_base_cost_shipment` — extend base cost shipment
- `base_cost_vpo` — base cost vpo
- `base_cost_pocv` — base cost pocv
- `extend_cost_vpo` — extend cost vpo
- `extend_cost_pocv` — extend cost pocv
- `oplgm_plus_amt` — oplgm plus amt

### Dimension and key columns

- `order_type` — order type
- `order_no` — order no
- `order_line_no` — order line no
- `etl_timestamp` — etl timestamp
- `date_flag` — date flag

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dm_us.dm_disty_pos_order_kit_di`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dm_us.dm_disty_pos_order_kit_di"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dm_us.dm_disty_pos_order_kit_di` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pos_order_kit_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dm_disty_pos_order_kit_di.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 22 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dm_disty_pos_order_kit_di.md`.*