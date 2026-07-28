# DIM: GV User Type Reference Dimension (`dim_pub_gv_user_type`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_gv_user_type
- domain: order
- one_line_purpose: This job loads the **GV (Governance / Global Vendor) user type reference table** as a dimension. It is a direct passthrough from the ODS source table, providing a named lookup of every GV user type code and its description for use in report...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_gv_user_type`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per `gv_user_type` code — each GV user type code is unique in the source.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full table overwrite on each run. - resolved from pipeline (see L4)
- **Natural key:** `gv_user_type`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per `gv_user_type` code — each GV user type code is unique in the source.
- **Partition:** none — full table overwrite on each run.
- **Natural key:** `gv_user_type`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_pub_gv_user_type` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_pub_gv_user_type` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_gv_user_type` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full table overwrite on each run.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "order dim_pub_gv_user_type schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_gv_user_type` | Sole source — all GV user type reference data |
| `dim_${country_code}.dim_pub_gv_user_type` | **Target** — GV user type dimension |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code` |


---

## L2 Declarative Knowledge

### Business purpose
This job loads the **GV (Governance / Global Vendor) user type reference table** as a dimension. It is a direct passthrough from the ODS source table, providing a named lookup of every GV user type code and its description for use in reports, joins, and filtering across the order and profitability domains.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Report / BI developers** | Join `dim_pub_gv_user_type` on `gv_user_type` to display human-readable GV type descriptions alongside profitability and order line data. |
| **Sales & channel teams** | `gv_user_type` and `gv_user_typedesc` identify whether an order line belongs to a specific GV/SPA governance category, enabling channel-based segmentation. |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full table overwrite on each run.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/order/metric-index.md`](../../source/contracts/order/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/order/metric-index.md` are mapped on this table.

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and attributes

- `gv_user_type` — the GV user type code (join key to order and profitability tables)
- `gv_user_typedesc` — human-readable description of the GV user type
- `spa_type` — SPA (Special Pricing Agreement) type classification
- `parent_type` — parent GV user type code for hierarchical roll-up
- `sort` — display sort order

### Audit columns

- `entry_datetime`, `entry_id` — when and by whom the record was originally created

---

### etl_metrics

N/A - no calculable ETL formulas extracted from this document (passthrough / stored measures only, or formulas not documented).

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_gv_user_type`

**From:** `ods_${country_code}.ods_cis_corp_gv_user_type`

**Filter:** None — all rows are loaded.

**Pass-through columns:** `gv_user_type`, `gv_user_typedesc`, `entry_datetime`, `entry_id`, `spa_type`, `parent_type`, `sort`

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_pub_gv_user_type
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`
**Target table:** `dim_${country_code}.dim_pub_gv_user_type` — full overwrite, no partitioning.

1. Read all rows from `ods_cis_corp_gv_user_type`.
2. **INSERT OVERWRITE** all selected columns directly into `dim_pub_gv_user_type`.

```mermaid
flowchart LR
  SRC[ods_cis_corp_gv_user_type] --> INS[INSERT OVERWRITE
dim_pub_gv_user_type]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Full passthrough** | Reads all rows from `ods_cis_corp_gv_user_type` and writes them verbatim into the dimension table. No filtering, transformation, or deduplication is applied. |
| **Full overwrite** | Replaces the entire `dim_pub_gv_user_type` table on each run. |

**Parameters:** `country_code`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_${country_code}.ods_cis_corp_gv_user_type` | **Sole source.** Provides all GV user type codes, descriptions, and attributes. All rows selected; no filter. |

**Temporary tables (inside the job only):** None.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_gv_user_type`

**From:** `ods_${country_code}.ods_cis_corp_gv_user_type`

**Filter:** None — all rows are loaded.

**Pass-through columns:** `gv_user_type`, `gv_user_typedesc`, `entry_datetime`, `entry_id`, `spa_type`, `parent_type`, `sort`

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_gv_user_type` | `ods_${country_code}.ods_cis_corp_gv_user_type` | 1:1 source scan | — (no JOIN; single FROM) | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:3`) |


### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `gv_user_type` | `gv_user_type` | `gv_user_type` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:1` |
| `gv_user_typedesc` | `gv_user_typedesc` | `gv_user_typedesc` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |
| `spa_type` | `spa_type` | `spa_type` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |
| `parent_type` | `parent_type` | `parent_type` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |
| `sort` | `sort` | `sort` | `ods_${country_code}.ods_cis_corp_gv_user_type` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dimension/script/dim_pub_gv_user_type.sql:2` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| None documented. | This is a reference table; no sentinel values are applied in this script. |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_gv_user_type
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_gv_user_type
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_gv_user_type
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Full overwrite on every run** — no partition or incremental logic; the entire table is replaced.
- **No transformation** — all columns are passed through exactly as they appear in the ODS source. Any data quality issues in the source are reflected here.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_gv_user_type` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_gv_user_type` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_gv_user_type` in Vertica once MCP verification is completed for this document.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | unknown |
| scan_risk_tier | medium |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Report / BI developers** | Join `dim_pub_gv_user_type` on `gv_user_type` to display human-readable GV type descriptions alongside profitability and order line data. |
| **Sales & channel teams** | `gv_user_type` and `gv_user_typedesc` identify whether an order line belongs to a specific GV/SPA governance category, enabling channel-based segmentation. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_pub_gv_user_type
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_gv_user_type` | All columns, full table | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql:2-3` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| None identified in repository. | — |

### Operational detail (verified)

- Full overwrite: `INSERT OVERWRITE TABLE dim_${country_code}.dim_pub_gv_user_type` — `dim_pub_gv_user_type.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

---

*Document generated from `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dimension/script/dim_pub_gv_user_type.sql`.*
