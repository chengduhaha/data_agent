# DWD: Close CPO Header Duplicate Detection (`dwd_disty_sales_close_duplicate_cpo_header_df`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_sales_close_duplicate_cpo_header_df
- domain: cpo
- one_line_purpose: This job detects **closed CPO headers that appear in more than one date partition** in the main closed CPO header table. Because the close CPO header ETL partitions by `to_date(trans_datetime)`, if a CPO is re-processed across multiple date...
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_sales_close_duplicate_cpo_header_df`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per `(cpo_id, last_date_flag)` — a CPO that exists in more than one partition, recording the older (earlier) partition date as `last_date_flag`.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** `date_flag = '${date_flag}'` — the run date; marks which deduplication pass this belongs to. - resolved from pipeline (see L4)
- **Natural key:** `cpo_id`, `last_date_flag` within a `date_flag` partition.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per `(cpo_id, last_date_flag)` — a CPO that exists in more than one partition, recording the older (earlier) partition date as `last_date_flag`.
- **Partition:** `date_flag = '${date_flag}'` — the run date; marks which deduplication pass this belongs to.
- **Natural key:** `cpo_id`, `last_date_flag` within a `date_flag` partition.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dwd_disty_sales_close_duplicate_cpo_header_df` | ETL target / intermediate per evidence script |
| Vertica | pending | `dwd_disty_sales_close_duplicate_cpo_header_df` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_us.dwd_disty_sales_close_duplicate_cpo_header_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag = '${date_flag}'` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "cpo dwd_disty_sales_close_duplicate_cpo_header_df schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | Source — scanned for duplicates |
| `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | **Target** — duplicate header partition registry |

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
This job detects **closed CPO headers that appear in more than one date partition** in the main closed CPO header table. Because the close CPO header ETL partitions by `to_date(trans_datetime)`, if a CPO is re-processed across multiple date windows it can accumulate duplicate rows in different `date_flag` partitions. This job identifies those "extra" partition appearances and records the duplicate `date_flag` values so the fix scripts can remove them.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Data engineering** | Input to `fix_dwd_disty_sales_close_cpo_header_extend_di.sql` and `fix_duplicate_close_cpo_header_di_vertica.sql` — tells the fix scripts exactly which partitions contain duplicate header rows. |

---

### Fact key resolution
- Natural key: `cpo_id`, `last_date_flag` within a `date_flag` partition.
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** `date_flag = '${date_flag}'` — the run date; marks which deduplication pass this belongs to.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/cpo/metric-index.md`](../../source/contracts/cpo/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/cpo/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE`

**Source:** Inner subquery from `dwd_disty_sales_close_cpo_header_extend_di`

**Filter:** `date_flag >= add_months('${date_flag}', -36)` — 36-month rolling lookback.

**Ranking:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `seq` | `ROW_NUMBER() OVER (PARTITION BY cpo_id ORDER BY date_flag DESC)` | `1` = most recent partition for this CPO. `> 1` = the CPO exists in an older partition too — a duplicate. |

**Output columns:**
- `cpo_id` — the CPO with a duplicate
- `last_date_flag` = `t.date_flag` — the **older** duplicate partition's date
- `date_flag` = literal `'${date_flag}'` — the run date (partition key)

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dwd_disty_sales_close_duplicate_cpo_header_df
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`, `date_flag`
**Target table:** `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df`, partitioned by **`date_flag`**.

1. Read `dwd_disty_sales_close_cpo_header_extend_di` for the last 36 months (`date_flag >= add_months('${date_flag}', -36)`).
2. Apply `ROW_NUMBER() OVER (PARTITION BY cpo_id ORDER BY date_flag DESC)` — the most recent partition gets `seq=1`; older partitions get `seq>1`.
3. Filter to `seq > 1` — these are the duplicate (older) partition appearances.
4. **INSERT OVERWRITE** writing `cpo_id`, `date_flag AS last_date_flag` (the duplicate's own older partition date), and literal `'${date_flag}'` as the target partition.

```mermaid
flowchart LR
  SRC[dwd_disty_sales_close_cpo_header_extend_di
last 36 months] --> RN[ROW_NUMBER over cpo_id
ORDER BY date_flag DESC]
  RN --> F[Filter seq > 1]
  F --> INS[INSERT dwd_disty_sales_close_duplicate_cpo_header_df
PARTITION date_flag=date_flag param]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Scan close CPO header** | Reads the last 36 months of `dwd_disty_sales_close_cpo_header_extend_di`, applying `ROW_NUMBER()` over `cpo_id` ordered by `date_flag DESC`. |
| **Identify duplicates** | Rows with `seq > 1` are duplicate appearances — the same CPO exists in an earlier partition as well as a later one. |
| **Record duplicate dates** | Writes the `cpo_id`, its earliest (`last_date_flag`) appearance, and the run date (`date_flag`) to the duplicate table. |

**Parameters:** `country_code`, `date_flag`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | Source — scanned for CPO IDs with multiple `date_flag` partitions over the last 36 months. |

**Temporary tables:** None.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE`

**Source:** Inner subquery from `dwd_disty_sales_close_cpo_header_extend_di`

**Filter:** `date_flag >= add_months('${date_flag}', -36)` — 36-month rolling lookback.

**Ranking:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `seq` | `ROW_NUMBER() OVER (PARTITION BY cpo_id ORDER BY date_flag DESC)` | `1` = most recent partition for this CPO. `> 1` = the CPO exists in an older partition too — a duplicate. |

**Output columns:**
- `cpo_id` — the CPO with a duplicate
- `last_date_flag` = `t.date_flag` — the **older** duplicate partition's date
- `date_flag` = literal `'${date_flag}'` — the run date (partition key)

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/cpo/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cpo_id` | `t.cpo_id` | `cpo_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql:3` |
| `last_date_flag` | `t.date_flag` | `date_flag` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | rename | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql:4` |
| `date_flag` | `'${date_flag}'` | `date_flag` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | literal | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql:5` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `seq > 1` | A CPO header row in a partition that is not its most recent — i.e. it is a duplicate. |
| `add_months('${date_flag}', -36)` | Rolling 36-month lookback boundary. |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **`last_date_flag` is the OLDER partition** — the one that should be removed. `seq=1` (the latest) is kept; `seq>1` rows identify what to delete.
- **36-month window** — CPOs with duplicates outside this window are not detected.
- **Partition overwrite** — each run replaces the `date_flag = '${date_flag}'` partition of this table.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` in Vertica once MCP verification is completed for this document.

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
| **Data engineering** | Input to `fix_dwd_disty_sales_close_cpo_header_extend_di.sql` and `fix_duplicate_close_cpo_header_di_vertica.sql` — tells the fix scripts exactly which partitions contain duplicate header rows. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dwd_disty_sales_close_duplicate_cpo_header_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | Scanned for duplicate cpo_id / date_flag combinations | `dwd_disty_sales_close_duplicate_cpo_header_df.sql:10-13` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| `fix_dwd_disty_sales_close_cpo_header_extend_di.sql` — reads this table to determine which partitions to repair | `fix_dwd_disty_sales_close_cpo_header_extend_di.sql:4` |
| `fix_duplicate_close_cpo_header_di_vertica.sql` — uses `dwd_disty_sales_close_duplicate_cpo_header` (Vertica sync of this data) for Vertica DELETE | `fix_duplicate_close_cpo_header_di_vertica.sql:10` |

### Operational detail (verified)

- Partition overwrite: `INSERT OVERWRITE TABLE dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df PARTITION (date_flag)` — `dwd_disty_sales_close_duplicate_cpo_header_df.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

---

*Document generated from `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql`.*
