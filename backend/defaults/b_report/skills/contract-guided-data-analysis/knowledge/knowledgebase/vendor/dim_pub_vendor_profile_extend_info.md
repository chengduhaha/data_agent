# dim_pub_vendor_profile_extend_info.sql

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vendor_profile_extend_info
- domain: vendor
- one_line_purpose: This ETL builds an extended vendor profile dimension that flags whether each vendor is tagged for specific next-generation solution categories. It converts profile records into simple `Y` indicators per vendor for easier reporting and segme...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vendor_profile_extend_info`
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
| Hive | yes | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_vendor_profile_extend_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vendor_profile_extend_info schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_profile` | source for vendor profile tags |
| 2 | `ods_${country_code}.ods_cis_corp_profile_types` | active VEND/FIN profile type filter |
| 3 | `ods_${country_code}.ods_cis_corp_vend_master` | base vendor list for final grain |
| 4 | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | target table (overwrite load) |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This ETL builds an extended vendor profile dimension that flags whether each vendor is tagged for specific next-generation solution categories. It converts profile records into simple `Y` indicators per vendor for easier reporting and segmentation.

It helps procurement, vendor management, and business teams identify vendors by strategic capability categories such as cloud, data, IoT, security, and pcode.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (vendor)** | Uses `dim_${country_code}.dim_pub_vendor_profile_extend_info` for operational and reporting workflows documented below. |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql` |

### Key filters and ETL business logic
### Sources and joins
- Builds `vend_next_gen_flag_tmp` by joining vendor profile rows to active profile type metadata (`profile_segment='VEND'`, `profile_cat='FIN'`) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:1-13`).
- Left joins the temp flag set to vendor master so every vendor can appear in output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:25-27`).

### Filters and business rules
- Keeps only active profile type definitions in the profile type table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:10-12`).
- Maps profile types to output flags using conditional aggregation:
  - `IOT-V` -> `iot_v`
  - `Cloud-V` -> `cloud_v`
  - `PCODE` -> `pcode`
  - `Data-V` -> `data_v`
  - `Security-V` -> `security_v`
  (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Grain and deduplication
- Output grain is one row per `vend.vend_no` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:18`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:29`).
- Multiple matching profile rows per vendor/category are collapsed with `max(...)` into single `Y` flags (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `iot_v` | Vendor has IoT category flag | Set to `Y` if any matched profile type is `IOT-V` |
| `cloud_v` | Vendor has cloud category flag | Set to `Y` if any matched profile type is `Cloud-V` |
| `pcode` | Vendor has pcode category flag | Set to `Y` if any matched profile type is `PCODE` |
| `data_v` | Vendor has data category flag | Set to `Y` if any matched profile type is `Data-V` |
| `security_v` | Vendor has security category flag | Set to `Y` if any matched profile type is `Security-V` |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_${country_code}.dim_pub_vendor_profile_extend_info
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
- Builds `vend_next_gen_flag_tmp` by joining vendor profile rows to active profile type metadata (`profile_segment='VEND'`, `profile_cat='FIN'`) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:1-13`).
- Left joins the temp flag set to vendor master so every vendor can appear in output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:25-27`).

### Filters and business rules
- Keeps only active profile type definitions in the profile type table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:10-12`).
- Maps profile types to output flags using conditional aggregation:
  - `IOT-V` -> `iot_v`
  - `Cloud-V` -> `cloud_v`
  - `PCODE` -> `pcode`
  - `Data-V` -> `data_v`
  - `Security-V` -> `security_v`
  (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Grain and deduplication
- Output grain is one row per `vend.vend_no` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:18`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:29`).
- Multiple matching profile rows per vendor/category are collapsed with `max(...)` into single `Y` flags (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `iot_v` | Vendor has IoT category flag | Set to `Y` if any matched profile type is `IOT-V` |
| `cloud_v` | Vendor has cloud category flag | Set to `Y` if any matched profile type is `Cloud-V` |
| `pcode` | Vendor has pcode category flag | Set to `Y` if any matched profile type is `PCODE` |
| `data_v` | Vendor has data category flag | Set to `Y` if any matched profile type is `Data-V` |
| `security_v` | Vendor has security category flag | Set to `Y` if any matched profile type is `Security-V` |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[dim_pub_vendor_profile_extend_info]
  JOB --> TGT[dim_${country_code}.dim_pub_vendor_profile_extend_info]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_profile` | source for vendor profile tags |
| 2 | `ods_${country_code}.ods_cis_corp_profile_types` | active VEND/FIN profile type filter |
| 3 | `ods_${country_code}.ods_cis_corp_vend_master` | base vendor list for final grain |
| 4 | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | target table (overwrite load) |

### Step-by-step logic
### Sources and joins
- Builds `vend_next_gen_flag_tmp` by joining vendor profile rows to active profile type metadata (`profile_segment='VEND'`, `profile_cat='FIN'`) (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:1-13`).
- Left joins the temp flag set to vendor master so every vendor can appear in output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:25-27`).

### Filters and business rules
- Keeps only active profile type definitions in the profile type table (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:10-12`).
- Maps profile types to output flags using conditional aggregation:
  - `IOT-V` -> `iot_v`
  - `Cloud-V` -> `cloud_v`
  - `PCODE` -> `pcode`
  - `Data-V` -> `data_v`
  - `Security-V` -> `security_v`
  (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Grain and deduplication
- Output grain is one row per `vend.vend_no` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:18`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:29`).
- Multiple matching profile rows per vendor/category are collapsed with `max(...)` into single `Y` flags (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19-23`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `iot_v` | Vendor has IoT category flag | Set to `Y` if any matched profile type is `IOT-V` |
| `cloud_v` | Vendor has cloud category flag | Set to `Y` if any matched profile type is `Cloud-V` |
| `pcode` | Vendor has pcode category flag | Set to `Y` if any matched profile type is `PCODE` |
| `data_v` | Vendor has data category flag | Set to `Y` if any matched profile type is `Data-V` |
| `security_v` | Vendor has security category flag | Set to `Y` if any matched profile type is `Security-V` |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_vendor_profile` | `ods_${country_code}.ods_cis_corp_profile_types` | many:1 | `a.profile_type = b.profile_type and b.profile_segment='VEND' and b.active ='Y' and b.profile_cat ='FIN'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:1) |

`source/ref/vendor/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `vend.vend_no` | `vend_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:18` |
| `iot_v` | `max(case when next_gen_flag = 'IOT-V' then 'Y' end)` | `next_gen_flag`, `IOT`, `V`, `Y` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:19` |
| `cloud_v` | `max(case when next_gen_flag = 'Cloud-V' then 'Y' end)` | `next_gen_flag`, `Cloud`, `V`, `Y` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:20` |
| `pcode` | `max(case when next_gen_flag = 'PCODE' then 'Y' end)` | `next_gen_flag`, `PCODE`, `Y` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:21` |
| `data_v` | `max(case when next_gen_flag = 'Data-V' then 'Y' end)` | `next_gen_flag`, `Data`, `V`, `Y` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:22` |
| `security_v` | `max(case when next_gen_flag = 'Security-V' then 'Y'end )` | `next_gen_flag`, `Security`, `V`, `Y` | `ods_${country_code}.ods_cis_corp_vend_master`, `vend_next_gen_flag_tmp` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:23` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_vendor_profile_extend_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_vendor_profile_extend_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_vendor_profile_extend_info
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
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_vendor_profile_extend_info` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_vendor_profile_extend_info` in Vertica once MCP verification is completed for this document.

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
| `ods_${country_code}.ods_cis_corp_vendor_profile` | Source profile type per vendor | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:7` |
| `ods_${country_code}.ods_cis_corp_profile_types` | Restricts to active VEND/FIN profile types | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:8-12` |
| `ods_${country_code}.ods_cis_corp_vend_master` | Base vendor list and final grain | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:25` |

### Downs

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_${country_code}.dim_pub_vendor_profile_extend_info
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_vendor_profile` | Source profile type per vendor | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:7` |
| `ods_${country_code}.ods_cis_corp_profile_types` | Restricts to active VEND/FIN profile types | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:8-12` |
| `ods_${country_code}.ods_cis_corp_vend_master` | Base vendor list and final grain | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:25` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Not documented in repository | No downstream consumer reference is present in this script |

### Operational detail (verified)
- Full overwrite load into `dim_${country_code}.dim_pub_vendor_profile_extend_info` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql:16`).
- Partition strategy is not specified in this script.

### Not documented in repository
- Owner
- Schedule / cadence
- SLA / alerting
- Explicit downstream jobs or reports

### Related scripts (verified)
- Not documented in repository (no explicit related script path/name is referenced in this SQL).

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_profile_extend_info.sql`.*
