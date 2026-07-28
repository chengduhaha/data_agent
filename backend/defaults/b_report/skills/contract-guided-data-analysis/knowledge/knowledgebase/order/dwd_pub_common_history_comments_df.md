# DWD: History Order Comments — Daily Snapshot (`dwd_pub_common_history_comments_df`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_pub_common_history_comments_df
- domain: order
- one_line_purpose: This job creates a **daily point-in-time snapshot of all settled/archived order comments** from the history comments table. It is a full passthrough of `ods_cis_corp_history_comments` with no filtering — providing a dated copy of every comm...
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_pub_common_history_comments_df.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_pub_common_history_comments_df`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per `(order_type, order_no, order_comment_no)` — a unique comment record on a historical order.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** `date_flag = '${date_flag}'` — literal run date; the entire partition is replaced on each run. - resolved from pipeline (see L4)
- **Natural key:** `order_type`, `order_no`, `order_comment_no` within a `date_flag` partition.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per `(order_type, order_no, order_comment_no)` — a unique comment record on a historical order.
- **Partition:** `date_flag = '${date_flag}'` — literal run date; the entire partition is replaced on each run.
- **Natural key:** `order_type`, `order_no`, `order_comment_no` within a `date_flag` partition.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dwd_pub_common_history_comments_df` | ETL target / intermediate per evidence script |
| Vertica | pending | `dwd_pub_common_history_comments_df` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dwd_pub_common_history_comments_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag = '${date_flag}'` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "order dwd_pub_common_history_comments_df schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_history_comments` | Sole source — all history order comments |
| `dw_${country_code}.dwd_pub_common_history_comments_df` | **Target** — daily snapshot of history comments |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code`, `date_flag` |


---

## L2 Declarative Knowledge

### Business purpose
This job creates a **daily point-in-time snapshot of all settled/archived order comments** from the history comments table. It is a full passthrough of `ods_cis_corp_history_comments` with no filtering — providing a dated copy of every comment record (customer comments, delete reasons, EC notes, and other comment types) attached to historical orders. The snapshot enables reporting and auditing workflows that need a stable, dated version of order comment data.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Audit / compliance** | Dated snapshot of order comments for historical review — comments cannot be back-modified in the snapshot. |
| **Customer service** | Access to all comment types (`comment_type`) attached to settled orders for dispute resolution and order history review. |
| **BI / reporting** | A stable, queryable daily copy of the history comments table without needing to hit the live ODS source. |

---

### Fact key resolution
- Natural key: `order_type`, `order_no`, `order_comment_no` within a `date_flag` partition.
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** `date_flag = '${date_flag}'` — literal run date; the entire partition is replaced on each run.
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

### Identifiers

- `order_type`, `order_no`, `order_comment_no`, `order_line_no`

### Comment attributes

- `comment` — the comment text
- `comment_type` — type code classifying the comment (e.g. `'CC'` for customer comment, `'OX'` for delete reason, `'EX'` for EC comment)
- `comment_loc` — location/context of the comment (e.g. `'O'` for order-level)

### Audit columns

- `entry_datetime`, `entry_id` — who and when the comment was created
- `delete_date`, `delete_id` — soft-delete tracking (when the comment was deleted and by whom)

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_pub_common_history_comments_df.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dwd_pub_common_history_comments_df`

**From:** `ods_${country_code}.ods_cis_corp_history_comments`

**Filter:** None — all rows are loaded.

**Pass-through columns:** `order_type`, `order_no`, `order_comment_no`, `order_line_no`, `comment`, `comment_type`, `comment_loc`, `entry_datetime`, `entry_id`, `delete_date`, `delete_id`

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dwd_pub_common_history_comments_df
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`, `date_flag`
**Target table:** `dw_${country_code}.dwd_pub_common_history_comments_df`, partitioned by **`date_flag = '${date_flag}'`** (literal).

1. Read all rows from `ods_cis_corp_history_comments` — no filter.
2. **INSERT OVERWRITE** into `dwd_pub_common_history_comments_df PARTITION (date_flag='${date_flag}')`.

```mermaid
flowchart LR
  SRC[ods_cis_corp_history_comments
no filter] --> INS[INSERT OVERWRITE
dwd_pub_common_history_comments_df
PARTITION date_flag=param]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Full passthrough** | Reads all rows from `ods_cis_corp_history_comments` and writes them verbatim into the daily partition. No filtering, transformation, or deduplication is applied. |
| **Daily partition overwrite** | Overwrites the `date_flag = '${date_flag}'` partition with the complete current state of the history comments table. |

**Parameters:** `country_code`, `date_flag`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_${country_code}.ods_cis_corp_history_comments` | **Sole source.** All settled/archived order comments. All rows selected; no filter. |

**Temporary tables (inside the job only):** None.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dwd_pub_common_history_comments_df`

**From:** `ods_${country_code}.ods_cis_corp_history_comments`

**Filter:** None — all rows are loaded.

**Pass-through columns:** `order_type`, `order_no`, `order_comment_no`, `order_line_no`, `comment`, `comment_type`, `comment_loc`, `entry_datetime`, `entry_id`, `delete_date`, `delete_id`

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_history_comments` | `ods_${country_code}.ods_cis_corp_history_comments` | 1:1 source scan | — (no JOIN; single FROM) | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:3`) |


### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `order_type` | `order_type` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `order_no` | `order_no` | `order_no` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `order_comment_no` | `order_comment_no` | `order_comment_no` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `order_line_no` | `order_line_no` | `order_line_no` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `comment` | `comment` | `comment` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:1` |
| `comment_type` | `comment_type` | `comment_type` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `comment_loc` | `comment_loc` | `comment_loc` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `delete_date` | `delete_date` | `delete_date` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |
| `delete_id` | `delete_id` | `delete_id` | `ods_${country_code}.ods_cis_corp_history_comments` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_pub_common_history_comments_df.sql:2` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `comment_type = 'CC'` | Customer-facing comment |
| `comment_type = 'OX'` | Delete / cancel reason |
| `comment_type = 'EX'` | EC (enterprise channel) comment |
| `comment_loc = 'O'` | Order-level comment (not line-level) |
| `delete_date IS NOT NULL` | Soft-deleted comment — the record exists but was marked as deleted |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_pub_common_history_comments_df.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dw_${country_code}.dwd_pub_common_history_comments_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dw_${country_code}.dwd_pub_common_history_comments_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dw_${country_code}.dwd_pub_common_history_comments_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Full snapshot on every run** — the entire `ods_cis_corp_history_comments` table is loaded into the target partition each time. There is no incremental logic.
- **Includes deleted records** — `delete_date IS NOT NULL` rows are included. Filter on `delete_date IS NULL` for active-only comment analysis.
- **Partition is a run-date marker, not a comment date** — `date_flag` is the parameter passed at run time and does not represent the comment's `entry_datetime` or the order's ship date.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dw_${country_code}.dwd_pub_common_history_comments_df` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dw_${country_code}.dwd_pub_common_history_comments_df` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dw_${country_code}.dwd_pub_common_history_comments_df` in Vertica once MCP verification is completed for this document.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Audit / compliance** | Dated snapshot of order comments for historical review — comments cannot be back-modified in the snapshot. |
| **Customer service** | Access to all comment types (`comment_type`) attached to settled orders for dispute resolution and order history review. |
| **BI / reporting** | A stable, queryable daily copy of the history comments table without needing to hit the live ODS source. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dwd_pub_common_history_comments_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_history_comments` | All history comments; full table | `dwd_pub_common_history_comments_df.sql:2-3` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| None identified in repository. | — |

### Operational detail (verified)

- Partition overwrite: `INSERT OVERWRITE TABLE dw_${country_code}.dwd_pub_common_history_comments_df PARTITION (date_flag='${date_flag}')` — `dwd_pub_common_history_comments_df.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

---

*Document generated from `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_pub_common_history_comments_df.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_pub_common_history_comments_df.sql`.*
