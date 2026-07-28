# dim_pub_vendor_contacts.sql

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vendor_contacts
- domain: vendor
- one_line_purpose: This ETL creates a global vendor contacts table by unioning country-level vendor contact dimensions from US, CA, WCLA, and BR. It carries a source-system company number and retains a normalized phone number field.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql

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
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vendor_contacts schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `dim_us.dim_pub_vendor_contacts` | source branch (US) |
| 2 | `dim_ca.dim_pub_vendor_contacts` | source branch (CA) |
| 3 | `dim_wcla.dim_pub_vendor_contacts` | source branch (WCLA) |
| 4 | `dim_br.dim_pub_vendor_contacts` | source branch (BR) |
| 5 | `dim_${country_code}.dim_pub_vendor_contacts` | target table (overwrite load) |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This ETL creates a global vendor contacts table by unioning country-level vendor contact dimensions from US, CA, WCLA, and BR. It carries a source-system company number and retains a normalized phone number field.

It helps global data consumers and operational teams access a single multi-country vendor contact dataset with consistent columns.

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
| Metric | Definition | Typical use |
|--------|------------|-------------|
| Contacts by sys company | Count of rows by `sys_company_no` | Country/source coverage validation |
| Global contact volume | Total rows across four sources | Monitoring consolidated dataset size |
| Contacts with normalized phone | Share where `format_phone_no` is populated | Phone quality tracking across countries |

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

The script overwrites `dim_${country_code}.dim_pub_vendor_contacts` by unioning:
- `dim_us.dim_pub_vendor_contacts` with `sys_company_no = 100`
- `dim_ca.dim_pub_vendor_contacts` with `sys_company_no = 500`
- `dim_wcla.dim_pub_vendor_contacts` with `sys_company_no = 425`
- `dim_br.dim_pub_vendor_contacts` with `sys_company_no = 422`

Typical usage:
- Consolidated global contact search and analytics.
- Cross-country communication data quality monitoring including formatted phone number.

### etl_metrics

#### `sys_company_no`
- **Source:** [metric-index.md](../../source/contracts/vendor/metric-index.md#sys_company_no)
- **Business definition:** Hardcoded per branch: 100/500/425/422
```sql
Source country/system identifier
```

#### `format_phone_no`
- **Source:** [metric-index.md](../../source/contracts/vendor/metric-index.md#format_phone_no)
- **Business definition:** Copied from country-level source tables
```sql
Digits-only phone normalization
```


---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql` |

### Key filters and ETL business logic
### Sources and joins
- Performs four-source `union all` consolidation from country-level dimension tables; no joins are used (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4-16`).

### Filters and business rules
- No row-level filters are applied; each branch selects all rows from its source table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:8`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:12`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).
- Assigns fixed `sys_company_no` per branch: 100, 500, 425, 422 (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:6`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:10`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:14`).

### Grain and deduplication
- Grain is inherited from source contact dimensions; `union all` does not deduplicate between countries (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:13`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source country/system identifier | Hardcoded per branch: 100/500/425/422 |
| `format_phone_no` | Digits-only phone normalization | Copied from country-level source tables |
| `vend_no` | Vendor identifier | Copied from each source table |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_${country_code}.dim_pub_vendor_contacts
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
- Performs four-source `union all` consolidation from country-level dimension tables; no joins are used (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4-16`).

### Filters and business rules
- No row-level filters are applied; each branch selects all rows from its source table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:8`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:12`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).
- Assigns fixed `sys_company_no` per branch: 100, 500, 425, 422 (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:6`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:10`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:14`).

### Grain and deduplication
- Grain is inherited from source contact dimensions; `union all` does not deduplicate between countries (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:13`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source country/system identifier | Hardcoded per branch: 100/500/425/422 |
| `format_phone_no` | Digits-only phone normalization | Copied from country-level source tables |
| `vend_no` | Vendor identifier | Copied from each source table |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[dim_pub_vendor_contacts]
  JOB --> TGT[dim_${country_code}.dim_pub_vendor_contacts]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `dim_us.dim_pub_vendor_contacts` | source branch (US) |
| 2 | `dim_ca.dim_pub_vendor_contacts` | source branch (CA) |
| 3 | `dim_wcla.dim_pub_vendor_contacts` | source branch (WCLA) |
| 4 | `dim_br.dim_pub_vendor_contacts` | source branch (BR) |
| 5 | `dim_${country_code}.dim_pub_vendor_contacts` | target table (overwrite load) |

### Step-by-step logic
### Sources and joins
- Performs four-source `union all` consolidation from country-level dimension tables; no joins are used (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4-16`).

### Filters and business rules
- No row-level filters are applied; each branch selects all rows from its source table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:8`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:12`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).
- Assigns fixed `sys_company_no` per branch: 100, 500, 425, 422 (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:2`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:6`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:10`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:14`).

### Grain and deduplication
- Grain is inherited from source contact dimensions; `union all` does not deduplicate between countries (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:5`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:13`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `sys_company_no` | Source country/system identifier | Hardcoded per branch: 100/500/425/422 |
| `format_phone_no` | Digits-only phone normalization | Copied from country-level source tables |
| `vend_no` | Vendor identifier | Copied from each source table |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_vend_contacts` | `ods_${country_code}.ods_cis_corp_vend_master` | many:1 | `c.vend_no = v.vend_no;` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:1) |

`source/ref/vendor/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `c.vend_no` | `vend_no` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `vend_name` | `v.vend_name` | `vend_name` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `loc_no` | `c.loc_no` | `loc_no` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `contact_no` | `c.contact_no` | `contact_no` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `contact_name` | `c.contact_name` | `contact_name` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `title` | `c.title` | `title` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `phone_no` | `c.phone_no` | `phone_no` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `phone_type` | `c.phone_type` | `phone_type` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `entry_datetime` | `c.entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `entry_id` | `c.entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `delete_date` | `c.delete_date` | `delete_date` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `delete_id` | `c.delete_id` | `delete_id` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `email_address` | `c.email_address` | `email_address` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `stop_email` | `c.stop_email` | `stop_email` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `dept` | `c.dept` | `dept` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `fax` | `c.fax` | `fax` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `contact_type` | `c.contact_type` | `contact_type` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `email_type` | `c.email_type` | `email_type` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `biz_card_title` | `c.biz_card_title` | `biz_card_title` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `comments` | `c.comments` | `comments` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |
| `format_phone_no` | `(CASE WHEN phone_no is not null THEN regexp_replace(phone_no,'[^0-9]','') END)` | `phone_no`, `regexp_replace` | `ods_${country_code}.ods_cis_corp_vend_contacts`, `ods_${country_code}.ods_cis_corp_vend_master` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:2` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql` |

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
| `dim_us.dim_pub_vendor_contacts` | US source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4` |
| `dim_ca.dim_pub_vendor_contacts` | CA source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:8` |
| `dim_wcla.dim_pub_vendor_contacts` | WCLA source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:12` |
| `dim_br.dim_pub_vendor_contacts` | BR source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest

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
| `dim_us.dim_pub_vendor_contacts` | US source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:4` |
| `dim_ca.dim_pub_vendor_contacts` | CA source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:8` |
| `dim_wcla.dim_pub_vendor_contacts` | WCLA source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:12` |
| `dim_br.dim_pub_vendor_contacts` | BR source branch | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:16` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Not documented in repository | No downstream consumer reference is present in this script |

### Operational detail (verified)
- Full overwrite load into `dim_${country_code}.dim_pub_vendor_contacts` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql:1`).
- Partition strategy is not specified in this script.

### Not documented in repository
- Owner
- Schedule / cadence
- SLA / alerting
- Consumer list for this global output

### Related scripts (verified)
- `dim_pub_vendor_contacts.sql` - builds country-level contacts with normalized phone used by global union - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts.sql:1-8`.
- `dim_pub_vendor_contacts_gbl.sql` - alternate global union variant (US/CA/WCLA only, without BR branch) - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_contacts_gbl.sql:1-9`.

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_gbl/dim_pub_vendor_contacts.sql`.*
