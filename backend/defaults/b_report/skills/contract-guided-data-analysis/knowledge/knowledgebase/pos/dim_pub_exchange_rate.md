# DIM: `dim_pub_exchange_rate`

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_exchange_rate
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` loads `dim_${country_code}.dim_pub_exchange_rate` (layer `DIM`). Purpose inferred from SQL only.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_exchange_rate`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql`)
- **Partition:** `See L4 / ETL partition clause`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_exchange_rate` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_exchange_rate` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `See L4 / ETL partition clause` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_pub_exchange_rate schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql`
- **upstream:** `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` loads `dim_${country_code}.dim_pub_exchange_rate` (layer `DIM`). Purpose inferred from SQL only.

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
- Prefer querying the target `dim_${country_code}.dim_pub_exchange_rate` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate"] --> T["dim_${country_code}.dim_pub_exchange_rate"]
```

### Base tables register

| Object | Role |
|--------|------|
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dim_${country_code}.dim_pub_exchange_rate`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_${country_code}.dim_pub_exchange_rate`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `local_currency` | `currency` | `currency` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | rename | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:3` |
| `date_flag` | `to_date(`date`)` | — | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | udf | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:4` |
| `base_currency` | `base` | `base` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | rename | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:5` |
| `rate` | `rate` | `rate` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:1` |
| `rate2` | `rate2` | `rate2` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:7` |
| `rate3` | `rate3` | `rate3` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:8` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:9` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql:10` |

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
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` |
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
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_exchange_rate/dim_pub_exchange_rate.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:59` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_exchange_rate.md` | `source/contracts/pos/tables/dim_pub_exchange_rate.md:5` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_br.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_br.flow:115` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_ca.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_ca.flow:139` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_exchange_rate_us.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_exchange_rate_us.flow:27` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hycn.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hycn.flow:60` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyuk.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyuk.flow:115` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyus.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyus.flow:114` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyww.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_hyww.flow:115` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_us.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_us.flow:736` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_wcla.flow` | `source/etl/flows/public_order_scripts/public_common_dimension/public_common_dimension_wcla.flow:170` |
| ETL/script ref: `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql` | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:1` |
| KB / contract ref: `target/knowledgebase/common/public_common_dimension/dim_pub_exchange_rate.md` | `target/knowledgebase/common/public_common_dimension/dim_pub_exchange_rate.md:1` |
| KB / contract ref: `target/knowledgebase/common/public_common_dimension/dim_pub_exchange_rate_df.md` | `target/knowledgebase/common/public_common_dimension/dim_pub_exchange_rate_df.md:1` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:95` |

#### Operational detail (verified)
- Partition clause: `See L4 / ETL partition clause`

#### Not documented in repository
- Schedule, owner, SLA
