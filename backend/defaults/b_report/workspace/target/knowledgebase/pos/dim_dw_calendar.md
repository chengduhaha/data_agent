# DIM: `dim_dw_calendar`

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_dw_calendar
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` loads `dim_${country_code}.dim_dw_calendar` (layer `DIM`). Purpose inferred from SQL only.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_dw_calendar/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_dw_calendar`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql`)
- **Partition:** `See L4 / ETL partition clause`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_dw_calendar` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_dw_calendar` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `See L4 / ETL partition clause` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_dw_calendar schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_dw_calendar` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` loads `dim_${country_code}.dim_dw_calendar` (layer `DIM`). Purpose inferred from SQL only.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| Data / BI consumers | Use target table produced by this ETL |
| Data Engineering | Maintain load logic in evidence script |

### Fact key resolution
- Keys follow target INSERT column list / GROUP BY in evidence SQL.

### Time field semantics
- Partition / date fields: `See L4 / ETL partition clause`

### Metrics served
- See L3 column derivations for measure expressions when present.

### Metric serving map
N/A — not a multi-period wide serving table (or not documented).

### etl_metrics
No calculable business metrics registered in metric-index for this create run.

## L3 Procedural Knowledge

### Query and routing rules
- Prefer querying the target `dim_${country_code}.dim_dw_calendar` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["ods_${country_code}.ods_cis_corp_dw_calendar"] --> T["dim_${country_code}.dim_dw_calendar"]
```

### Base tables register

| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dim_${country_code}.dim_dw_calendar`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_${country_code}.dim_dw_calendar`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `date_flag` | `date_flag` | `date_flag` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:4` |
| `u_version` | `u_version` | `u_version` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:5` |
| `q` | `q` | `q` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:6` |
| `fq` | `fq` | `fq` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:7` |
| `m` | `m` | `m` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:2` |
| `w` | `w` | `w` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:2` |
| `d` | `d` | `d` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:2` |
| `year` | `year` | `year` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:11` |
| `qtr` | `qtr` | `qtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:12` |
| `month` | `month` | `month` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:13` |
| `week` | `week` | `week` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:14` |
| `day` | `day` | `day` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:15` |
| `doy` | `doy` | `doy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:16` |
| `fyear` | `fyear` | `fyear` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:17` |
| `fqtr` | `fqtr` | `fqtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:18` |
| `fdoy` | `fdoy` | `fdoy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:19` |
| `dow` | `dow` | `dow` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:20` |
| `dname` | `dname` | `dname` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:21` |
| `bonuswk` | `bonuswk` | `bonuswk` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:22` |
| `holiday` | `holiday` | `holiday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:23` |
| `payroll` | `payroll` | `payroll` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:24` |
| `sales` | `sales` | `sales` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:25` |
| `comment` | `comment` | `comment` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:26` |
| `weekday` | `weekday` | `weekday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql:27` |

### Sentinel and code values
Not documented in repository beyond CASE/exp_code predicates in ETL SQL.

## L4 Validation

### Resolved partition value
- Partition expression from ETL: `See L4 / ETL partition clause`
- Runtime values: Not documented in repository (resolve via Azkaban params when flow evidence exists).

### Data quality checks
Not documented in repository

### Validation SQL
N/A — Vertica MCP not executed during documentation (Vertica no-run policy).

### Caveats for interpretation
- Generated from ETL SQL evidence only; business definitions may need `source/ref` enrichment.

### Conflicts and open questions
None identified in repository

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` |
| Serving | Vertica (when synced) | Not documented in repository |

### Access constraints
Not documented in repository

### Query risk profile
- Scan risk depends on partition pruning; always filter partition keys when present.

## L6 Access and Consumption

### Primary consumers and use cases
Not documented in repository

### Representative query patterns
Not documented in repository

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_dw_calendar/dim_dw_calendar.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:20` |
| KB / contract ref: `source/contracts/pos/tables/dim_dw_calendar.md` | `source/contracts/pos/tables/dim_dw_calendar.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_ap/etl/ap_multiregion_aging_detail_rds_8443.sql` | `source/contracts/rds/vertica_ap/etl/ap_multiregion_aging_detail_rds_8443.sql:393` |
| FLOW ref: `source/etl/flows/public_order_scripts/dim_pub_date/dim_pub_date_ca.flow` | `source/etl/flows/public_order_scripts/dim_pub_date/dim_pub_date_ca.flow:38` |
| FLOW ref: `source/etl/flows/public_order_scripts/dim_pub_date/dim_pub_date_us.flow` | `source/etl/flows/public_order_scripts/dim_pub_date/dim_pub_date_us.flow:37` |
| ETL/script ref: `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql` | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:2` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ap/ap_multiregion_aging_detail_rds_8443.md` | `target/knowledgebase/RDS/vertica_ap/ap_multiregion_aging_detail_rds_8443.md:182` |
| KB / contract ref: `target/knowledgebase/common/dim_pub_date/dim_dw_calendar.md` | `target/knowledgebase/common/dim_pub_date/dim_dw_calendar.md:1` |
| KB / contract ref: `target/knowledgebase/common/dim_pub_date/dim_pub_date.md` | `target/knowledgebase/common/dim_pub_date/dim_pub_date.md:505` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:90` |

#### Operational detail (verified)
- Partition clause: `See L4 / ETL partition clause`

#### Not documented in repository
- Schedule, owner, SLA
