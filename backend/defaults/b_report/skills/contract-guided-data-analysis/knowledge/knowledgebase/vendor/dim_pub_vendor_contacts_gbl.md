# dim_pub_vendor_contacts_gbl.sql

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vendor_contacts
- domain: vendor
- one_line_purpose: This ETL creates a consolidated vendor contacts table by unioning country-level vendor contacts from US, CA, and WCLA, while assigning a fixed `sys_company_no` per source country. It provides a single multi-country contact dataset.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vendor_contacts`
- **Layer type:** DIM
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
| Hive | yes | `dim_${country_code}.dim_pub_vendor_contacts` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_${country_code}.dim_pub_vendor_contacts` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_vendor_contacts` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vendor_contacts_gbl schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `dim_us.dim_pub_vendor_contacts` | source branch (US) |
| 2 | `dim_ca.dim_pub_vendor_contacts` | source branch (CA) |
| 3 | `dim_wcla.dim_pub_vendor_contacts` | source branch (WCLA) |
| 4 | `dim_${country_code}.dim_pub_vendor_contacts` | target table (overwrite load) |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This ETL creates a consolidated vendor contacts table by unioning country-level vendor contacts from US, CA, and WCLA, while assigning a fixed `sys_company_no` per source country. It provides a single multi-country contact dataset.

It helps global operations and reporting teams consume vendor contacts across supported country dimensions in one place.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (vendor)** | Uses `dim_${country_code}.dim_pub_vendor_contacts` for operational and reporting workflows documented below. |

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/vendor/metric-index.md`](../../source/contracts/vendor/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/vendor/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql` |

### Key filters and ETL business logic
### Sources and joins
- Reads from three country dimension tables and combines records with `union all` (no joins) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).

### Filters and business rules
- No row-level filters are applied in the branches; all rows from each source table are included (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).
- Assigns fixed system company codes per source branch (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:8`).

### Grain and deduplication
- Grain is inherited from each source contact dimension row; `union all` preserves duplicates if they exist across inputs (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:7`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:9`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source system/country identifier | Hardcoded per source branch: 100/500/425 |
| `vend_no` | Vendor identifier | Copied from each source contact dimension |
| `contact_no` | Contact identifier | Copied from each source contact dimension |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
- Reads from three country dimension tables and combines records with `union all` (no joins) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).

### Filters and business rules
- No row-level filters are applied in the branches; all rows from each source table are included (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).
- Assigns fixed system company codes per source branch (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:8`).

### Grain and deduplication
- Grain is inherited from each source contact dimension row; `union all` preserves duplicates if they exist across inputs (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:7`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:9`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source system/country identifier | Hardcoded per source branch: 100/500/425 |
| `vend_no` | Vendor identifier | Copied from each source contact dimension |
| `contact_no` | Contact identifier | Copied from each source contact dimension |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[dim_pub_vendor_contacts_gbl]
  JOB --> TGT[dim_${country_code}.dim_pub_vendor_contacts]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `dim_us.dim_pub_vendor_contacts` | source branch (US) |
| 2 | `dim_ca.dim_pub_vendor_contacts` | source branch (CA) |
| 3 | `dim_wcla.dim_pub_vendor_contacts` | source branch (WCLA) |
| 4 | `dim_${country_code}.dim_pub_vendor_contacts` | target table (overwrite load) |

### Step-by-step logic
### Sources and joins
- Reads from three country dimension tables and combines records with `union all` (no joins) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).

### Filters and business rules
- No row-level filters are applied in the branches; all rows from each source table are included (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3-9`).
- Assigns fixed system company codes per source branch (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:8`).

### Grain and deduplication
- Grain is inherited from each source contact dimension row; `union all` preserves duplicates if they exist across inputs (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:7`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:9`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source system/country identifier | Hardcoded per source branch: 100/500/425 |
| `vend_no` | Vendor identifier | Copied from each source contact dimension |
| `contact_no` | Contact identifier | Copied from each source contact dimension |

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
| `sys_company_no` | `100` | — | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `vend_no` | `vend_no` | `vend_no` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `vend_name` | `vend_name` | `vend_name` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `loc_no` | `loc_no` | `loc_no` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `contact_no` | `contact_no` | `contact_no` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `contact_name` | `contact_name` | `contact_name` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `title` | `title` | `title` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `phone_no` | `phone_no` | `phone_no` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `phone_type` | `phone_type` | `phone_type` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `entry_id` | `entry_id` | `entry_id` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `delete_date` | `delete_date` | `delete_date` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `delete_id` | `delete_id` | `delete_id` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `email_address` | `email_address` | `email_address` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `stop_email` | `stop_email` | `stop_email` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `dept` | `dept` | `dept` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `fax` | `fax` | `fax` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `contact_type` | `contact_type` | `contact_type` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `email_type` | `email_type` | `email_type` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `biz_card_title` | `biz_card_title` | `biz_card_title` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |
| `comments` | `comments` | `comments` | `dim_us.dim_pub_vendor_contacts`, `dim_ca.dim_pub_vendor_contacts`, `dim_wcla.dim_pub_vendor_contacts` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:2` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

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
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_vendor_contacts` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_vendor_contacts` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_vendor_contacts` in Vertica once MCP verification is completed for this document.

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
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_vendor_contacts` | US branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3` |
| `dim_ca.dim_pub_vendor_contacts` | CA branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:6` |
| `dim_wcla.dim_pub_vendor_contacts` | WCLA branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:9` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Not documented in repository | No

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_us.dim_pub_vendor_contacts` | US branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:3` |
| `dim_ca.dim_pub_vendor_contacts` | CA branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:6` |
| `dim_wcla.dim_pub_vendor_contacts` | WCLA branch source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:9` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Not documented in repository | No downstream consumer reference is present in this script |

### Operational detail (verified)
- Full overwrite load into `dim_${country_code}.dim_pub_vendor_contacts` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:1`).
- Partition strategy is not specified in this script.

### Not documented in repository
- Owner
- Schedule / cadence
- SLA / alerting
- Why BR is excluded in this version

### Related scripts (verified)
- `dim_pub_vendor_contacts.sql` - builds country-level source table shape used by this union pattern - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:1-8`.
- `dim_gbl/dim_pub_vendor_contacts.sql` - similar global union script with additional BR branch and formatted phone number column - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:1-16`.

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql`.*
