# DIM: Vendor segment date-flag snapshot (`dim_${country_code}.dim_pub_vendor_segment_df`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_vendor_segment_df
- domain: vendor
- one_line_purpose: Partitioned daily snapshot of `dim_pub_vendor_segment` (vendor segment / class / type hierarchy and marketing attributes) for date-flagged loads.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vendor_segment_df` (script stem `dim_pub_vend_segment_df`; physical target uses `vendor` spelling)
- **Layer type:** DIM
- **Canonical / derived:** Derived snapshot — column copy from `dim_pub_vendor_segment` into `date_flag` partition
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per vendor (`vend_no`) within a `date_flag` partition — same as current `dim_pub_vendor_segment` (sibling KB)
- **Scope:** Country-scoped DIM via `${country_code}`
- **Partition:** `date_flag = ${date_flag}` — see L4
- **Natural key:** `vend_no` (+ partition `date_flag`)
- **Exclusions:** None in this script (no WHERE)

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_vendor_segment_df` | ETL INSERT OVERWRITE target |
| Vertica | pending for `_df` | `dim_${country_code}.dim_pub_vendor_segment` | US flow hive2vertica syncs non-`_df` `dim_pub_vendor_segment` — `public_vendor_dimension_us.flow:89-97` |

### Physical schema reference

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_vendor_segment_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_dim_us_dim_pub_vendor_segment_df.json` |
| **column_count** | pending (run ddl_seed_writer); sibling non-`_df` seed cites 17 columns |
| **partition_keys** | `date_flag` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vendor_segment_df schema" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_${country_code}.dim_pub_vendor_segment` — `dim_pub_vend_segment_df.sql:1-4`
- **downstream:** Sibling KB documents this as consumer of `dim_pub_vend_segment` build; Vertica sync uses non-`_df` table

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | `INSERT OVERWRITE` partition `date_flag=${date_flag}` |
| Schedule | Not documented at job level; flow-level schedule on `public_vendor_dimension_us.flow` |
| Parameters | `${country_code}`, `${date_flag}` (`query.parameter.date_flag` on flow job) |

---

## L2 Declarative Knowledge

### Business purpose
This job copies the current vendor segment dimension into a date-partitioned snapshot: vendor identity, master-vendor mapping, marketing name/rank, segment/class/type codes and names, EDI/ECE flags, report sequence, and catalog code. It supports date-flagged reuse of the segment classification built by `dim_pub_vend_segment.sql`.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Category / procurement** | Date-scoped vendor segment hierarchy |
| **Downstream ETL** | Partitioned copy of segment attributes |
| **Reporting (Vertica)** | Prefer synced `dim_pub_vendor_segment` (non-`_df`) per flow |

### Identifier search profile
- Primary lookup: `vend_no`
- Supporting: `master_vend_no`, `seg_code`, `class_code`, `type_code`, `catalog_code`
- Constrain Hive queries by `date_flag`

### Time field semantics
- **`date_flag`:** load partition from `${date_flag}` only (not selected as a column in the SQL list)

### Metrics served
| Category | Columns | Business reading |
|----------|---------|------------------|
| Measures | — | No measure columns in this ETL |

### Metric serving map
N/A — not a multi-period serving table.

### etl_metrics
No calculable metrics. Formula authority: [`source/contracts/vendor/metric-index.md`](../../source/contracts/vendor/metric-index.md).

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Filter `_df` by `date_flag`.
**Technical predicates (load only):** Partition clause only.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| None in this job | — | Single-table SELECT | `dim_pub_vend_segment_df.sql:4` |

### Key filters and ETL business logic
- **Technical (load only):** `PARTITION (date_flag=${date_flag})` — `dim_pub_vend_segment_df.sql:1`
- No WHERE / JOIN business predicates
- **Special logic applied in this ETL:** none beyond full partition overwrite from current DIM

### Standard time-filter SQL
```sql
SELECT *
FROM dim_${country_code}.dim_pub_vendor_segment_df
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. `dim_pub_vend_segment` builds `dim_pub_vendor_segment`.
2. `gen_date_parameter` supplies `${date_flag}`.
3. This script copies listed columns into `dim_pub_vendor_segment_df` partition `${date_flag}`.

```mermaid
flowchart LR
  SEG["dim_pub_vendor_segment"]
  DF["dim_pub_vendor_segment_df\npartition date_flag"]
  SEG -->|INSERT OVERWRITE passthrough| DF
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_${country_code}.dim_pub_vendor_segment` | Sole source |
| `dim_${country_code}.dim_pub_vendor_segment_df` | Target |

### Step-by-step logic
#### Step 1 — INSERT OVERWRITE partition from current vendor segment DIM
**Source:** `dim_${country_code}.dim_pub_vendor_segment`  
**Filter / joins:** none  
**Load:** listed columns into `dim_pub_vendor_segment_df` for `${date_flag}` — `dim_pub_vend_segment_df.sql:1-4`

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/vendor/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `vend_no` | `vend_no` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `discontinued` | `discontinued` | `discontinued` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `vend_name` | `vend_name` | `vend_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `master_vend_no` | `master_vend_no` | `master_vend_no` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `master_vend_name` | `master_vend_name` | `master_vend_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `mk_name` | `mk_name` | `mk_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `rank` | `rank` | — | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `seg_code` | `seg_code` | `seg_code` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `seg_name` | `seg_name` | `seg_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `class_code` | `class_code` | `class_code` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `class_name` | `class_name` | `class_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `type_code` | `type_code` | `type_code` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `type_name` | `type_name` | `type_name` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `edi_flag` | `edi_flag` | `edi_flag` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `ece_flag` | `ece_flag` | `ece_flag` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `report_seq` | `report_seq` | `report_seq` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |
| `catalog_code` | `catalog_code` | `catalog_code` | `dim_${country_code}.dim_pub_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:3` |

### Sentinel and code values
None redefined in this script — pass-through from `dim_pub_vendor_segment`.

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | Flow job `dim_pub_vend_segment_df` | dependsOn `dim_pub_vend_segment`, `gen_date_parameter`; `query.parameter.date_flag: ${date_flag}` — `public_vendor_dimension_us.flow:67-75` |
| 2 | INSERT | `PARTITION (date_flag=${date_flag})` — `dim_pub_vend_segment_df.sql:1` |

### Data quality checks
- Partition row count vs current `dim_pub_vendor_segment`
- Duplicate `vend_no` within partition

### Validation SQL
```sql
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_vendor_segment_df
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

SELECT
  (SELECT COUNT(*) FROM dim_${country_code}.dim_pub_vendor_segment) AS src_cnt,
  (SELECT COUNT(*) FROM dim_${country_code}.dim_pub_vendor_segment_df WHERE date_flag = '${partition_value}') AS df_cnt;

SELECT vend_no, date_flag, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_vendor_segment_df
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- Script filename uses `vend_segment`; target table uses `vendor_segment`.
- Vertica sync in US flow reads non-`_df` `dim_pub_vendor_segment`, not this snapshot.

### Conflicts and open questions
- Owner / SLA: Not documented in repository
- Whether any job syncs `_df` to Vertica: Not documented in repository for US flow

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| Partitioned snapshot | `dim_${country_code}.dim_pub_vendor_segment_df` | Not synced from `_df` in US flow | — | ETL SQL | pending |
| Reporting DIM (related) | `dim_${country_code}.dim_pub_vendor_segment` | `dim_${country_code}.dim_pub_vendor_segment` | hive2vertica overwrite | `public_vendor_dimension_us.flow:89-97` | pending |

### Access constraints
- `${country_code}` schema routing

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes (`date_flag`) |
| scan_risk_tier | low |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Snapshot consumers** | Date-partitioned vendor segment attributes |
| **Vertica reporting** | Use synced `dim_pub_vendor_segment` per flow |

### Representative query patterns
```sql
SELECT vend_no, vend_name, master_vend_no, seg_code, seg_name, class_code, type_code, catalog_code
FROM dim_${country_code}.dim_pub_vendor_segment_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_${country_code}.dim_pub_vendor_segment` | Sole SELECT source | `dim_pub_vend_segment_df.sql:4` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Flow job `dim_pub_vend_segment_df` orchestration | `public_vendor_dimension_us.flow:67-75` |
| Direct SQL consumers of `_df` FQN | Not documented in repository |

#### Not documented in repository
- `source/ref/vendor/special_logic.txt` / table relationship
- Owner / SLA
- DDL / MCP verification for `_df`

---

*Evidence: `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment_df.sql`; flow `source/etl/flows/public_order_scripts/public_vendor_dimension/public_vendor_dimension_us.flow`.*
