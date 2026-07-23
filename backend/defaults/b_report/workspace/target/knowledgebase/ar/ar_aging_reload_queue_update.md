# Utility: AR Aging Reload Queue Cleanup (`dim_disty_ar_aging_reload_queue_hudi_cow` — DELETE)

- artifact_type: etl_table
- artifact_id: dim_us.dim_disty_ar_aging_reload_queue_hudi_cow
- domain: ar
- one_line_purpose: This Python script removes a specific date entry from the AR aging reload queue Hudi table after that date has been processed. It is the cleanup counterpart to `ar_aging_reload_queue.py` and ensures that processed reload dates do not remain...
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_disty_ar_aging_reload_queue_hudi_cow`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** Not documented in repository
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Target:** `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` (Hudi COW DELETE operation).

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_disty_ar_aging_reload_queue_hudi_cow` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_disty_ar_aging_reload_queue_hudi_cow` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_disty_ar_aging_reload_queue_hudi_cow` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "ar ar_aging_reload_queue_update schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` | Target queue table (Hudi COW) |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `date_flag`, `target_db`, `flow_name`, `biz_unit`, `country` |


---

## L2 Declarative Knowledge

### Business purpose
This Python script removes a specific date entry from the AR aging reload queue Hudi table after
that date has been processed. It is the cleanup counterpart to `ar_aging_reload_queue.py` and
ensures that processed reload dates do not remain in the queue and trigger redundant re-processing.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **ETL / data operations** | Clears processed entries from the reload queue, preventing double-processing |
| **Data engineering** | Maintains an accurate queue of pending reload dates |

---

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

**Formula authority:** [`source/contracts/ar/metric-index.md`](../../source/contracts/ar/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/ar/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py` |

### Key filters and ETL business logic
### Step 1 — DELETE from Hudi queue

```sql
DELETE FROM dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE reload_date_flag = '${date_flag}';
```

Removes all rows where `reload_date_flag` matches the run date.

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_disty_ar_aging_reload_queue_hudi_cow
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `date_flag`, `country`
**Target table:** `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow`.

1. Execute a Hudi `DELETE FROM` for `reload_date_flag = '${date_flag}'`.

```mermaid
flowchart LR
  INP["date_flag parameter"] --> DEL["DELETE FROM
dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE reload_date_flag = date_flag"]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Delete queue entry** | Remove the row for `reload_date_flag = '${date_flag}'` from the Hudi COW queue table |

**Parameters:** `date_flag`, `target_db`, `flow_name`, `biz_unit`, `country`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` | The queue table; the target of the DELETE |

---

### Step-by-step logic
### Step 1 — DELETE from Hudi queue

```sql
DELETE FROM dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE reload_date_flag = '${date_flag}';
```

Removes all rows where `reload_date_flag` matches the run date.

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/ar/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| — | — | — | — | — | No derivations parsed from ETL SQL (`source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py`) — Not documented in repository |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- This script issues a Hudi `DELETE` — behaviour depends on the Hudi table version and merge config in the cluster.
- If run before AR aging for `date_flag` has actually completed, the queue entry will be removed prematurely and the date may not be re-processed.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` in Vertica once MCP verification is completed for this document.

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
| Audience | How they benefit |
|----------|-----------------|
| **ETL / data operations** | Clears processed entries from the reload queue, preventing double-processing |
| **Data engineering** | Maintains an accurate queue of pending reload dates |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_disty_ar_aging_reload_queue_hudi_cow
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_${country}.dim_disty_ar_aging_reload_queue_hudi_cow` | Table to clean | `source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py:22` |

### Downstream consumers (verified)

None identified in repository.

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

### Related scripts (verified)

- `ar_aging_reload_queue.py` — Companion that populates this queue — `source/etl/sql/ar/data_service/ar/python/`

---

*Document generated from `source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/ar/data_service/ar/python/ar_aging_reload_queue_update.py`.*
