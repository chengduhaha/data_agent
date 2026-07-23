# Azkaban flow: IDC weekly delivery init (`idc_delivery_week_data_init`)

- artifact_type: etl_table
- artifact_id: flow_marketing.idc_delivery_week_data_init
- domain: marketing
- one_line_purpose: Manual or backfill variant of the weekly IDC delivery pipeline. Skips SFTP ingest and assumes weekly CSV files are already on HDFS. Used for initial loads or reprocessing.
- layer_type: FLOW
- source_kind: etl_sql
- evidence_source: source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `flow_marketing.idc_delivery_week_data_init`
- **Layer type:** FLOW
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
| Hive | yes | `idc_delivery_week_data_init` | ETL target / intermediate per evidence script |
| Vertica | pending | `idc_delivery_week_data_init` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `flow_marketing.idc_delivery_week_data_init` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "marketing idc_delivery_week_data_init schema" --intent find_table_schema` |

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
Manual or backfill variant of the weekly IDC delivery pipeline. Skips SFTP ingest and assumes weekly CSV files are already on HDFS. Used for initial loads or reprocessing.

---

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (marketing)** | Uses `idc_delivery_week_data_init` for operational and reporting workflows documented below. |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow` |

### Key filters and ETL business logic
See step-by-step logic

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM idc_delivery_week_data_init
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
None identified in repository


### Base tables register
None identified in repository

### Step-by-step logic
None identified in repository

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM idc_delivery_week_data_init WHERE partition_col = '${partition_value}' GROUP BY 1;
-- 2) metric sum by dimension (top N) - replace metric/dim from L2
-- 3) grain duplicate check on natural keys
```


### Caveats for interpretation
None identified in repository

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.
#### Job chain (preserved)

1. `gen-date-parameters`
2. `read_hdfs` → `read_hdfs.py`
3. `ods_etl_marketing_idc_raw_data_week`
4. `hive2vertica-overwrite-ods_marketing_idc_raw_data_week`
5. `hive2mysql-insert-CIS-idc_prod_category`
6. `hive2mysql-insert-CIS-idc_vend_brand`
7. `send-mail-weekly`
8. `final-job`

---


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
| scan_risk_tier | medium |

---

## L6 Access and Consumption

### Primary consumers and use cases
### Related flows (verified)

- `idc_delivery_week_data.flow` — scheduled production variant — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow`

### Not documented in repository

- Production trigger procedure for init flow

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow`.*

---

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM idc_delivery_week_data_init
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Related flows (verified)

- `idc_delivery_week_data.flow` — scheduled production variant — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow`

### Not documented in repository

- Production trigger procedure for init flow

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow`.*

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data_init.flow`.*
