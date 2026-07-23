# DIM: Shared dimension for POS attribute enrichment (`dim_us.dim_pub_sku_xref_all`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_sku_xref_all
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_sku_xref_all`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dim_us.dim_pub_sku_xref_all` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_pub_sku_xref_all schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_sku_xref` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`
- **upstream:** `ods_${country_code}.ods_his_corp_sku_xref` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_part_master` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
- Parameters / date window: see ETL `${literal_*}` / `${date_flag}` / `${start_date}` in evidence script.
- Schedule: Not documented in repository

## L2 Declarative Knowledge

### Business purpose
See preserved **Business purpose** below when present (POS contract catalog + linked ETL).

### Audience and use cases
See preserved **Who it helps** section when present.

### Fact key resolution
See preserved **Grain and keys** when present.

### Time field semantics
- Prefer partition / `date_flag` filters documented in preserved sections and L3 Key filters from ETL.

### Metrics served
See preserved Metrics / column groups when present; otherwise L3 column derivations.

### Metric serving map
N/A unless multi-period wide table (see preserved content).

### etl_metrics
No new metric-index formulas appended in this bitbucket-etl upgrade pass.

## L3 Procedural Knowledge

### Query and routing rules
- Reporting: Vertica `dim_us.dim_pub_sku_xref_all` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `t2.sku_no is null )a )aa where aa.rn=1;` | Business | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["ods_${country_code}.ods_cis_corp_sku_xref"] --> T["dim_us.dim_pub_sku_xref_all"]
  S1["ods_${country_code}.ods_his_corp_sku_xref"] --> T["dim_us.dim_pub_sku_xref_all"]
  S2["ods_${country_code}.ods_cis_corp_part_master"] --> T["dim_us.dim_pub_sku_xref_all"]
```

### Base tables register
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_sku_xref` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_his_corp_sku_xref` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_part_master` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dim_us.dim_pub_sku_xref_all` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_his_corp_sku_xref` | `ods_${country_code}.ods_cis_corp_part_master` | many:1 (LEFT) | `t1.sku_no` = `t2.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:30`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_us.dim_pub_sku_xref_all`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `sku_no` | `sku_no` | `sku_no` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:3` |
| `xref_type` | `xref_type` | `xref_type` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:4` |
| `xref_no` | `xref_no` | `xref_no` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:5` |
| `u_version` | `u_version` | `u_version` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:6` |
| `xref` | `xref` | `xref` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:1` |
| `active` | `active` | `active` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:8` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:9` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:10` |
| `data_source` | `data_source` | `data_source` | `ods_${country_code}.ods_cis_corp_sku_xref`, `ods_${country_code}.ods_his_corp_sku_xref`, `ods_${country_code}.ods_cis_corp_part_master` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql:11` |

### Sentinel and code values
See preserved content and ETL CASE expressions in column derivations.

## L4 Validation

### Resolved partition value
- Partition / date parameters from ETL literals — concrete calendar values Not documented in repository (resolve via Azkaban when flow evidence exists).

### Data quality checks
See preserved Validation SQL when present.

### Validation SQL
Prefer preserved Vertica validation bundle when present; MCP business SQL not re-run during documentation.

### Caveats for interpretation
- Document upgraded additively from POS **contract** MD + **bitbucket-etl** SQL. Prior contract text is under **Preserved pre-L1-L6 content** when present.

### Conflicts and open questions
- Companion loader scripts may also appear under other domain KB folders; see `target/knowledgebase/pos/readme.md` cross-links.

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql` |
| Report | Vertica | preserved POS contract when present |

### Access constraints
Not documented in repository

### Query risk profile
- Always filter `date_flag` / documented partition keys before wide scans.

## L6 Access and Consumption

### Primary consumers and use cases
See preserved audience / POS report consumers when present.

### Representative query patterns
See preserved Validation SQL / contract examples when present.

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_sku_xref` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql` |
| `ods_${country_code}.ods_his_corp_sku_xref` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql` |
| `ods_${country_code}.ods_cis_corp_part_master` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/ods_etl_sku_xref_all.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:97` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_sku_xref_all.md` | `source/contracts/pos/tables/dim_pub_sku_xref_all.md:5` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_br.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_br.flow:381` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_ca.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_ca.flow:385` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hycn.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hycn.flow:278` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyuk.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyuk.flow:280` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyus.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyus.flow:279` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyww.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_hyww.flow:281` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_us.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_us.flow:387` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_wcla.flow` | `source/etl/flows/public_order_scripts/public_part_dimension/public_part_dimension_wcla.flow:400` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:40` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dim_pub_sku_xref_all/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dim_pub_sku_xref_all.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dim_pub_sku_xref_all.md`

## Business purpose

Shared dimension for POS attribute enrichment

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dim_us.dim_pub_sku_xref_all` — DIM layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dim_us` (US baseline documented as `dw_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **POS / RDS reporting** | Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1) |
| **Sales analytics** | Order, customer, product, and margin attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to POS hub and downstream exports. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_sku_xref_all` | `dim_us.dim_pub_sku_xref_all` | overwrite / incremental | POS contract `dim_pub_sku_xref_all.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dim_us.dim_pub_sku_xref_all` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dim_us.dim_pub_sku_xref_all`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `sku_no`, `xref_no`, `entry_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sku_xref_all
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT sku_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sku_xref_all
WHERE date_flag = '${partition_value}'
GROUP BY sku_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sku_no, xref_no, entry_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_sku_xref_all
WHERE date_flag = '${partition_value}'
GROUP BY sku_no, xref_no, entry_id, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- No measure-role columns tagged in POS contract; table may be dimension-only.

### Dimension and key columns

- `sku_no` — sku no
- `xref_type` — xref type
- `xref_no` — xref no
- `u_version` — u version
- `xref` — xref
- `active` — active
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `data_source` — data source

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dim_us.dim_pub_sku_xref_all`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dim_us.dim_pub_sku_xref_all"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dim_us.dim_pub_sku_xref_all` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dim_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dim_pub_sku_xref_all.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dim_pub_sku_xref_all.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 9 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dim_pub_sku_xref_all.md`.*