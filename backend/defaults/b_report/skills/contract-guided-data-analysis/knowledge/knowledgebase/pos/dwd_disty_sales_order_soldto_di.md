# PRIMARY: POS enrichment partner table joined from hub (`dw_us.dwd_disty_sales_order_soldto_di`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_sales_order_soldto_di
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_sales_order_soldto_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dw_us.dwd_disty_sales_order_soldto_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_sales_order_soldto_di schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql`
- **upstream:** `dw_${country_code}.dwd_disty_sales_single_orders_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_history_soldto` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql`
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
- Reporting: Vertica `dw_us.dwd_disty_sales_order_soldto_di` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `a.date_flag>= '${start_date}' AND a.date_flag< '${end_date}' and a.order_type >0 and a.ship_qty <>0 and a.terr_status = 'n' and eu.delete_date is null ;` | Technical (load only) / Business | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["dw_${country_code}.dwd_disty_sales_single_orders_di"] --> T["dw_us.dwd_disty_sales_order_soldto_di"]
  S1["ods_${country_code}.ods_cis_corp_history_soldto"] --> T["dw_us.dwd_disty_sales_order_soldto_di"]
```

### Base tables register
| Object | Role |
|--------|------|
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_history_soldto` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dw_us.dwd_disty_sales_order_soldto_di` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `ods_${country_code}.ods_cis_corp_history_soldto` | many:1 | `a.order_no` = `eu.order_no`; `a.order_type` = `eu.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:22`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_disty_sales_order_soldto_di`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `eu.order_type` | `order_type` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:4` |
| `order_no` | `eu.order_no` | `order_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:5` |
| `to_acct_no` | `eu.to_acct_no` | `to_acct_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:6` |
| `to_loc_no` | `eu.to_loc_no` | `to_loc_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:7` |
| `frt_cust_no` | `eu.frt_cust_no` | `frt_cust_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:8` |
| `special_handle` | `eu.special_handle` | `special_handle` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:9` |
| `end_user_po` | `eu.end_user_po` | `end_user_po` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:10` |
| `ship_from_loc_no` | `eu.ship_from_loc_no` | `ship_from_loc_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:11` |
| `ship_to_phone` | `eu.ship_to_phone` | `ship_to_phone` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:12` |
| `entry_datetime` | `eu.entry_datetime` | `entry_datetime` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:13` |
| `entry_id` | `eu.entry_id` | `entry_id` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:14` |
| `from_ref_type` | `eu.from_ref_type` | `from_ref_type` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:15` |
| `big_deal_no` | `eu.big_deal_no` | `big_deal_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:16` |
| `warranty_convert_code` | `eu.warranty_convert_code` | `warranty_convert_code` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:17` |
| `sales_model` | `eu.sales_model` | `sales_model` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:18` |
| `reseller_cust_no` | `eu.reseller_cust_no` | `reseller_cust_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:19` |
| `date_flag` | `a.date_flag` | `date_flag` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `ods_${country_code}.ods_cis_corp_history_soldto` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql:20` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql` |
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
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql` |
| `ods_${country_code}.ods_cis_corp_history_soldto` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/load_disty_sales_order_soldto_di.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:202` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_sales_order_soldto_di.md` | `source/contracts/pos/tables/dwd_disty_sales_order_soldto_di.md:5` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:72` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_disty_sales_order_soldto_di/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_order_soldto_di.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_sales_order_soldto_di.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_sales_order_soldto_di` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_sales_order_soldto_di` | `dw_us.dwd_disty_sales_order_soldto_di` | overwrite / incremental | POS contract `dwd_disty_sales_order_soldto_di.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_sales_order_soldto_di` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_sales_order_soldto_di`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_type`, `order_no`, `to_acct_no`, `to_loc_no`, `frt_cust_no`, `ship_from_loc_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_sales_order_soldto_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_type, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_sales_order_soldto_di
WHERE date_flag = '${partition_value}'
GROUP BY order_type
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_type, order_no, to_acct_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_sales_order_soldto_di
WHERE date_flag = '${partition_value}'
GROUP BY order_type, order_no, to_acct_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- No measure-role columns tagged in POS contract; table may be dimension-only.

### Dimension and key columns

- `order_type` — order type
- `order_no` — order no
- `to_acct_no` — to acct no
- `to_loc_no` — to loc no
- `frt_cust_no` — frt cust no
- `special_handle` — special handle
- `end_user_po` — end user po
- `ship_from_loc_no` — ship from loc no
- `ship_to_phone` — ship to phone
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `from_ref_type` — from ref type
- `big_deal_no` — big deal no
- `warranty_convert_code` — warranty convert code
- `sales_model` — sales model
- `reseller_cust_no` — reseller cust no
- `date_flag` — date flag

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_sales_order_soldto_di`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_sales_order_soldto_di"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_sales_order_soldto_di` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_order_soldto_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_sales_order_soldto_di.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 17 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_sales_order_soldto_di.md`.*