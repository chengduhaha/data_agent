# Parameter bootstrap: literal date parameters (`literal_parameters.sql`)

- artifact_type: etl_table
- artifact_id: literal_parameters.sql
- domain: marketing
- one_line_purpose: This is the Azkaban parameter bootstrap job used by all IDC delivery flows. It passes through the flow-level `start_date` value so downstream mail jobs can reference today's processing date in email subjects and headers.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `literal_parameters.sql`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** Not documented in repository
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository


### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `literal_parameters.sql` | ETL target / intermediate per evidence script |
| Vertica | pending | `literal_parameters.sql` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `literal_parameters.sql` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "marketing literal_parameters schema" --intent find_table_schema` |

### Lineage
See L6 Dependencies and notes.

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This is the Azkaban parameter bootstrap job used by all IDC delivery flows. It passes through the flow-level `start_date` value so downstream mail jobs can reference today's processing date in email subjects and headers.

---

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (marketing)** | Uses `literal_parameters.sql` for operational and reporting workflows documented below. |

### Fact key resolution
- Natural key: Not documented in repository
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/marketing/metric-index.md`](../../source/contracts/marketing/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/marketing/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql` |

### Key filters and ETL business logic
See step-by-step logic

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM literal_parameters.sql
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
```mermaid
flowchart LR
  CFG[flow config<br/>query.parameter.start_date] --> LP[literal_parameters.sql]
  LP --> MAIL[send-mail-monthly / send-mail-weekly]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|------------------|
| **Parameter pass-through** | Exposes `start_date` from flow config as a flow variable. |

**Parameters (input from flow config):**
- `start_date` = `date(from_utc_timestamp(current_timestamp(),'America/Los_Angeles'))` — today's date in Pacific Time

**Parameters (output):**
- `start_date` — same value, available as `${start_date}` to dependent jobs

---


### Base tables register
None identified in repository

### Step-by-step logic
None identified in repository

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/marketing/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `start_date` | `${start_date} AS start_date;` | `start_date` | — | partial | `source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql:2` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
#### Resolved data range

Trace how `start_date` is computed at runtime — it is the flow run's current calendar date in Pacific Time, not a fixed value.

| Step | Source | How `start_date` is determined |
|------|--------|--------------------------------|
| 1 — Flow config | `idc_delivery_*_data.flow` | `query.parameter.start_date: date(from_utc_timestamp(current_timestamp(),'America/Los_Angeles'))` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:14` |
| 2 — Bootstrap SQL | `literal_parameters.sql` | `SELECT ${start_date} AS start_date` — pass-through only — `source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql:1-2` |
| 3 — Mail consumers | `send-mail-monthly` | `mail.subject` and `mail.parameter.mail_header` interpolate `${start_date}` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:95-97` |
| 4 — Mail consumers | `send-mail-weekly` | Same pattern — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:110-111` |

**Plain language:** `start_date` is today's date in `America/Los_Angeles` when Azkaban evaluates the flow config at run time. It labels email subjects and headers only — it does **not** select which `month` or `week` data partition is loaded (that comes from SFTP folder paths; see `read_hdfs_monthly.md` and `read_hdfs.md`).

---

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM literal_parameters.sql WHERE partition_col = '${partition_value}' GROUP BY 1;
-- 2) metric sum by dimension (top N) - replace metric/dim from L2
-- 3) grain duplicate check on natural keys
```


### Caveats for interpretation
None identified in repository

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Not in Vertica** | *See script lineage* | *No Vertica mapping identified in repository* | - | *Add flow evidence when found* | no |

No queryable Vertica table has been confirmed for this script from current repository evidence.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | unknown |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| Flow config `query.parameter.start_date` | Input to SQL | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:14` |

### Downstream consumers (verified)

| Object | Evidence |
|--------|----------|
| `send-mail-monthly` mail subject/header | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:84-89` |
| `send-mail-weekly` mail subject/header | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:104-111` |

### Operational detail (verified)

- Job name in flows: `gen-date-parameters` (type `livy32`)
- Script path: `./hdfstohive/literal_parameters.sql` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_mon

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM literal_parameters.sql
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| Flow config `query.parameter.start_date` | Input to SQL | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:14` |

### Downstream consumers (verified)

| Object | Evidence |
|--------|----------|
| `send-mail-monthly` mail subject/header | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:84-89` |
| `send-mail-weekly` mail subject/header | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:104-111` |

### Operational detail (verified)

- Job name in flows: `gen-date-parameters` (type `livy32`)
- Script path: `./hdfstohive/literal_parameters.sql` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:17-20`

### Not documented in repository

- Whether `start_date` is used in SQL/Python ETL scripts (only verified in mail jobs)

### Related scripts (verified)

- All four IDC delivery flows use this bootstrap — `idc_delivery_month_data.flow`, `idc_delivery_week_data.flow`, and their `_init` variants

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql`.*

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/literal_parameters.sql`.*
