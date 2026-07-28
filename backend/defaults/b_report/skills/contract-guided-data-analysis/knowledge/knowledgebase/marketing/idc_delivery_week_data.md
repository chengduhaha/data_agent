# Azkaban flow: IDC weekly delivery (`idc_delivery_week_data`)

- artifact_type: etl_table
- artifact_id: flow_marketing.idc_delivery_week_data
- domain: marketing
- one_line_purpose: Scheduled daily flow that ingests IDC weekly distributor delivery files from SFTP, loads Hive staging, promotes to ODS, syncs to Vertica, updates CIS product category and vendor brand reference tables, and emails upload status to stakeholde...
- layer_type: FLOW
- source_kind: etl_sql
- evidence_source: source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `flow_marketing.idc_delivery_week_data`
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
| Hive | yes | `idc_delivery_week_data` | ETL target / intermediate per evidence script |
| Vertica | pending | `idc_delivery_week_data` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `flow_marketing.idc_delivery_week_data` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "marketing idc_delivery_week_data schema" --intent find_table_schema` |

### Lineage
See L6 Dependencies and notes.

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | See preserved schedule subsection below |
| Parameters | See source script / flow parameters |

#### Schedule detail (preserved)

| Setting | Value | Evidence |
|---------|-------|----------|
| `schedule-cron` | `0 30 13 * * ? *` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:8` |
| `schedule-timezone` | `Asia/Shanghai` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:9` |

**Resolved run time:** 13:30 CST daily.

---

---

## L2 Declarative Knowledge

### Business purpose
Scheduled daily flow that ingests IDC weekly distributor delivery files from SFTP, loads Hive staging, promotes to ODS, syncs to Vertica, updates CIS product category and vendor brand reference tables, and emails upload status to stakeholders.

---

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (marketing)** | Uses `idc_delivery_week_data` for operational and reporting workflows documented below. |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow` |

### Key filters and ETL business logic
See step-by-step logic

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM idc_delivery_week_data
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
```mermaid
flowchart TD
  GEN[gen-date-parameters] --> MAIL[send-mail-weekly]
  SFTP[idc_week_data_sftp_to_hdfs] -->|files| READ[read_hdfs.py]
  SFTP -->|no files| NOSYNC[not-sync-file-job]
  READ --> ODS[ods_etl_marketing_idc_raw_data_week.sql]
  ODS --> VRT[hive2vertica dm_idc_raw_data_week]
  ODS --> CIS1[CIS.idc_prod_category]
  ODS --> CIS2[CIS.idc_vend_brand]
  READ --> STAT[gen-data-file_status]
  READ --> FSTAT[final_status_message]
  STAT --> MAIL
  FSTAT --> MAIL
  VRT --> MAIL
  CIS1 --> MAIL
  CIS2 --> MAIL
  MAIL --> FINAL[final-job]
```

---


#### High-level stages (preserved)

| Stage | Job name | Business meaning |
|-------|----------|------------------|
| **Parameter bootstrap** | `gen-date-parameters` | Sets `start_date` for notifications |
| **SFTP ingest** | `idc_week_data_sftp_to_hdfs` | Copies weekly IDC CSV folders to HDFS |
| **CSV parse** | `read_hdfs` | Schema validation + Hive staging load |
| **ODS promote** | `ods_etl_marketing_idc_raw_data_week` | Latest week to ODS ETL |
| **Vertica sync** | `hive2vertica-overwrite-ods_marketing_idc_raw_data_week` | Full overwrite Vertica table |
| **CIS product categories** | `hive2mysql-insert-CIS-idc_prod_category` | Insert distinct product hierarchy to CIS |
| **CIS vendor brands** | `hive2mysql-insert-CIS-idc_vend_brand` | Insert distinct brands to CIS |
| **Notification** | `send-mail-weekly` | Email with per-file status |

---


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
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dm_gbl.dm_idc_raw_data_week
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dm_gbl.dm_idc_raw_data_week
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dm_gbl.dm_idc_raw_data_week
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
#### SFTP path configuration (preserved)

| Setting | Value |
|---------|-------|
| Source base | `/idc-knowledge-platform-gtdc-sftp/Synnex/IDC_Delivery/` |
| Path pattern | `YYYY-Wnn/` or `YYYY-Wnn/YYYY/` ISO week folders |
| HDFS target | `/apps/data/ods_gbl/externalfile/ods_ext_marketing_idc_raw_data_week` |

Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:24-28`

---

#### CIS sync detail (verified) (preserved from legacy doc)

### `CIS.idc_prod_category`

- **Mode:** insert with conflict on `(product_group, product_category, product_name, product_detail)`
- **Source:** distinct non-null product hierarchy from `dm_gbl.dm_idc_raw_data_weekly_view`
- Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:78-89`

### `CIS.idc_vend_brand`

- **Mode:** insert with conflict on `brand_name`
- **Source:** distinct `brand_name` grouped by `UPPER(brand_name)`
- Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:91-102`

---

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_gbl.dm_idc_raw_data_weekly_view` | `dm_gbl.dm_idc_raw_data_week` | overwrite | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:73-74` | yes (Vertica metadata fallback) |
| **Hive alternative** | `ods_gbl.ods_etl_marketing_idc_raw_data_week` | `dm_gbl.dm_idc_raw_data_week` | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:46-52` | - |
| **ETL internal** | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | Not synced to Vertica | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/read_hdfs.py` | - |

Business users should query **`dm_gbl.dm_idc_raw_data_week`** in Vertica for weekly IDC reporting (23 columns; WKB seed `vertica_dm_gbl_dm_idc_raw_data_week.json`). Sync target verified from flow.

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
### Scripts in this flow

| Script | Evidence |
|--------|----------|
| `read_hdfs.py` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:43` |
| `ods_etl_marketing_idc_raw_data_week.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:51` |
| `literal_parameters.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:20` |
| `status_output.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:64` |

### Downstream targets (verified)

| Target | Evidence |
|--------|----------|
| `dm_gbl.dm_idc_raw_data_week` (Vertica) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:73-74` |
| `CIS.idc_prod_category` (MySQL) | `source/etl/sql/marketing/mar

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM idc_delivery_week_data
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Scripts in this flow

| Script | Evidence |
|--------|----------|
| `read_hdfs.py` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:43` |
| `ods_etl_marketing_idc_raw_data_week.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:51` |
| `literal_parameters.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:20` |
| `status_output.sql` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:64` |

### Downstream targets (verified)

| Target | Evidence |
|--------|----------|
| `dm_gbl.dm_idc_raw_data_week` (Vertica) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:73-74` |
| `CIS.idc_prod_category` (MySQL) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:87` |
| `CIS.idc_vend_brand` (MySQL) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:100` |

### Not documented in repository

- Hive view `dm_idc_raw_data_weekly_view` DDL
- CIS table schemas
- Bitbucket DDL for marketing IDC Hive tables — not in `HIVE/snxhive` at `refs/heads/master`; Hive WKB seeds skipped. Vertica reporting table `dm_gbl.dm_idc_raw_data_week` seeded via metadata fallback (`vertica_dm_gbl_dm_idc_raw_data_week.json`).

### Related flows (verified)

- `idc_delivery_week_data_init.flow` — same without SFTP (backfill/manual)

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow`.*

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow`.*
