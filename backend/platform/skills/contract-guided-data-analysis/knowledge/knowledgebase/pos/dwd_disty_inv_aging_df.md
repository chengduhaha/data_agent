# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_inv_aging_df`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_inv_aging_df
- domain: pos
- one_line_purpose: POS-domain fact table with load SQL now available under bitbucket-etl (see L3); prior contract narrative preserved below.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/
- related_etl_scripts:
- `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/load_dw_inv_aging_view_levels.py`

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_inv_aging_df`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below (POS contract narrative retained).

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes (per preserved POS contract) | Reporting path in preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dw_us.dwd_disty_inv_aging_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain (`date_flag` when documented) |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_inv_aging_df schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql`
- **upstream:** `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
- Parameters / date window: see ETL `${literal_*}` / `${date_flag}` in evidence script.
- Schedule: Not documented in repository

## L2 Declarative Knowledge

### Business purpose
See preserved **Business purpose** below (POS contract catalog + now linked ETL).

### Audience and use cases
See preserved **Who it helps** section.

### Fact key resolution
See preserved **Grain and keys**.

### Time field semantics
- Prefer partition / `date_flag` filters documented in preserved sections and L3 Key filters from ETL.

### Metrics served
See preserved Metrics / column groups when present.

### Metric serving map
N/A unless multi-period wide table (see preserved content).

### etl_metrics
No new metric-index formulas appended in this bitbucket-etl upgrade pass.

## L3 Procedural Knowledge

### Query and routing rules
- Reporting: Vertica `dw_us.dwd_disty_inv_aging_df` (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic
ETL WHERE / JOIN predicates are summarized via Relationship map provenance and Column derivations; full narrative retained in preserved sections.

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql
```

### End-to-end flow
```mermaid
flowchart LR
  ETL["dwd_disty_inv_aging_df bitbucket-etl"] --> TGT["dw_us.dwd_disty_inv_aging_df"]
```

### Base tables register
| Object | Role |
|--------|------|
| See Relationship map + preserved lineage | ETL sources / temps |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/`.
2. Apply date / business filters from ETL.
3. Write target `dw_us.dwd_disty_inv_aging_df` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_disty_inv_aging_df`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `view_level` | `view_level` | `view_level` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:2` |
| `view_key1` | `view_key1` | `view_key1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:3` |
| `view_key2` | `view_key2` | `view_key2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:4` |
| `view_key3` | `view_key3` | `view_key3` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:5` |
| `inv_type` | `inv_type` | `inv_type` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:6` |
| `sku_no` | `sku_no` | `sku_no` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:7` |
| `u_version` | `u_version` | `u_version` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:8` |
| `prod_code` | `prod_code` | `prod_code` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:9` |
| `vend_code` | `vend_code` | `vend_code` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:10` |
| `vend_name` | `vend_name` | `vend_name` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:11` |
| `vend_no` | `vend_no` | `vend_no` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:12` |
| `part_no` | `part_no` | `part_no` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:13` |
| `ave_cost` | `ave_cost` | `ave_cost` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:14` |
| `oh_cost` | `oh_cost` | `oh_cost` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:15` |
| `it_cost` | `it_cost` | `it_cost` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:16` |
| `ext_oh_cost` | `ext_oh_cost` | `ext_oh_cost` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:17` |
| `ext_it_cost` | `ext_it_cost` | `ext_it_cost` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:18` |
| `on_hand_qty` | `on_hand_qty` | `on_hand_qty` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:19` |
| `ohand_qty` | `ohand_qty` | `ohand_qty` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:20` |
| `intran_in` | `intran_in` | `intran_in` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:21` |
| `itran_qty` | `itran_qty` | `itran_qty` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:22` |
| `qty1_30` | `it_qty1` | `it_qty1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:23` |
| `qty31_60` | `it_qty2` | `it_qty2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:24` |
| `qty61_90` | `it_qty3` | `it_qty3` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:25` |
| `qty90_up` | `it_qty4` | `it_qty4` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:26` |
| `age1_30` | `age1` | `age1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:27` |
| `age31_60` | `age2` | `age2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:28` |
| `age61_90` | `age3` | `age3` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:28` |
| `age90_up` | `age4` | `age4` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:30` |
| `qty91_120` | `it_qty5e` | `it_qty5e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:31` |
| `qty121_150` | `it_qty6e` | `it_qty6e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:32` |
| `qty151_180` | `it_qty7e` | `it_qty7e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:33` |
| `qty180_up` | `nvl(it_qty8e,0) + nvl(it_qty9e,0) + nvl(it_qty10e,0)` | `it_qty8e`, `it_qty9e`, `it_qty10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | coalesce | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:34` |
| `qty240_up` | `nvl(it_qty9e,0) + nvl(it_qty10e,0)` | `it_qty9e`, `it_qty10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | coalesce | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:34` |
| `qty360_up` | `it_qty10e` | `it_qty10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:34` |
| `age91_120` | `age5e` | `age5e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:37` |
| `age121_150` | `age6e` | `age6e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:38` |
| `age151_180` | `age7e` | `age7e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:39` |
| `age180_up` | `nvl(age8e,0) + nvl(age9e,0) + nvl(age10e,0)` | `age8e`, `age9e`, `age10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | coalesce | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:40` |
| `age240_up` | `nvl(age9e,0) + nvl(age10e,0)` | `age9e`, `age10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | coalesce | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:40` |
| `age360_up` | `age10e` | `age10e` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:40` |
| `qty181_210` | `it_qty8e1` | `it_qty8e1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:43` |
| `qty211_240` | `it_qty8e2` | `it_qty8e2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:44` |
| `qty241_270` | `it_qty9e1` | `it_qty9e1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:45` |
| `qty271_300` | `it_qty9e2` | `it_qty9e2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:46` |
| `qty301_330` | `it_qty9e3` | `it_qty9e3` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:47` |
| `qty331_360` | `it_qty9e4` | `it_qty9e4` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:48` |
| `age181_210` | `age8e1` | `age8e1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:49` |
| `age211_240` | `age8e2` | `age8e2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:50` |
| `age241_270` | `age9e1` | `age9e1` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:51` |
| `age271_300` | `age9e2` | `age9e2` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:52` |
| `age301_330` | `age9e3` | `age9e3` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:53` |
| `age331_360` | `age9e4` | `age9e4` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:54` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | arithmetic | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:55` |
| `date_flag` | `date_format(date_flag,'yyyy-MM-dd')` | `date_flag`, `yyyy`, `MM`, `dd` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | arithmetic | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:56` |
| `company_no` | `company_no` | `company_no` | `${literal_source_db}.ods_dw_prod_dws_dw_inv_aging` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql:1` |

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
- Document upgraded additively from POS **contract** MD + **bitbucket-etl** SQL. Prior contract text is under **Preserved pre-L1-L6 content**.

### Conflicts and open questions
- Companion loader scripts may also be documented under `ap/` / `ar/` / `inventory/` domains (same stems); see `target/knowledgebase/pos/readme.md` cross-links.

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql` |
| Report | Vertica | preserved POS contract |

### Access constraints
Not documented in repository

### Query risk profile
- Always filter `date_flag` / documented partition keys before wide scans.

## L6 Access and Consumption

### Primary consumers and use cases
See preserved audience / POS report consumers.

### Representative query patterns
See preserved Validation SQL / contract examples.

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| ETL FROM/JOIN objects | load | `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/dwd_disty_inv_aging_df.sql` (see Relationship map) |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/b-report-us/A Dependent dataset of P&L Item 1.md` | `source/contracts/b-report-us/A Dependent dataset of P&L Item 1.md:32` |
| KB / contract ref: `source/contracts/b-report-us/A PL_ITEM_LOGIC 1.md` | `source/contracts/b-report-us/A PL_ITEM_LOGIC 1.md:998` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_1d/Product/sql/dws_disty_brpt_part_1d.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_1d/Product/sql/dws_disty_brpt_part_1d.py:8` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_mtd/Product/python/dws_disty_brpt_part_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_mtd/Product/python/dws_disty_brpt_part_mtd.py:16` |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:179` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_inv_aging_df.md` | `source/contracts/pos/tables/dwd_disty_inv_aging_df.md:5` |
| ETL/script ref: `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql` | `source/contracts/rds/starrocks_inventory/etl/inv_aging_eta_rio_open_po_rds_7806.sql:72` |
| ETL/script ref: `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql` | `source/contracts/rds/starrocks_inventory/etl/inv_qty_aging_runrate_rio_location_rds_5501.sql:249` |
| ETL/script ref: `source/contracts/rds/starrocks_vpo/etl/vpo_inventory_open_po_eta_rio_runrate_rds_7806.sql` | `source/contracts/rds/starrocks_vpo/etl/vpo_inventory_open_po_eta_rio_runrate_rds_7806.sql:72` |
| ETL/script ref: `source/contracts/rds/vertica_ap/etl/ap_average_balance_multisheet_rds_9163.sql` | `source/contracts/rds/vertica_ap/etl/ap_average_balance_multisheet_rds_9163.sql:58` |
| ETL/script ref: `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql` | `source/contracts/rds/vertica_b_report/etl/b_report_lightweight_orders_inventory_rio_rds_7500.sql:142` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_rio_alloc_rds_18605.sql` | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_rio_alloc_rds_18605.sql:43` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_so_alloc_rds_17343.sql` | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_so_alloc_rds_17343.sql:47` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_so_alloc_rds_17345.sql` | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_runrate_so_alloc_rds_17345.sql:39` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql` | `source/contracts/rds/vertica_inventory/etl/inv_aging_qty_vendor_filter_rds_17484.sql:53` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql` | `source/contracts/rds/vertica_inventory/etl/inv_qty_aging_runrate_rio_alloc_customer_rds_us13208.sql:760` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql` | `source/contracts/rds/vertica_inventory/etl/inv_rio_cws_location_rds_6800.sql:643` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql` | `source/contracts/rds/vertica_inventory/etl/inv_rollover_true_aging_rds_10968.sql:53` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:135` |
| ETL/script ref: `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_inventory_rio_runrate_rds_7500.sql` | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_inventory_rio_runrate_rds_7500.sql:142` |
| FLOW ref: `source/etl/flows/data_service/inventory/inv_aging_data_initialization_us.flow` | `source/etl/flows/data_service/inventory/inv_aging_data_initialization_us.flow:59` |
| FLOW ref: `source/etl/flows/data_service/inventory/inv_aging_load_br.flow` | `source/etl/flows/data_service/inventory/inv_aging_load_br.flow:299` |
| FLOW ref: `source/etl/flows/data_service/inventory/inv_aging_load_ca.flow` | `source/etl/flows/data_service/inventory/inv_aging_load_ca.flow:300` |
| FLOW ref: `source/etl/flows/data_service/inventory/inv_aging_load_us.flow` | `source/etl/flows/data_service/inventory/inv_aging_load_us.flow:299` |
| FLOW ref: `source/etl/flows/data_service/inventory/inv_aging_load_wcla.flow` | `source/etl/flows/data_service/inventory/inv_aging_load_wcla.flow:314` |
| FLOW ref: `source/etl/flows/data_service/inventory_switch/inv_aging_switch_br.flow` | `source/etl/flows/data_service/inventory_switch/inv_aging_switch_br.flow:155` |
| FLOW ref: `source/etl/flows/data_service/inventory_switch/inv_aging_switch_ca.flow` | `source/etl/flows/data_service/inventory_switch/inv_aging_switch_ca.flow:155` |
| FLOW ref: `source/etl/flows/data_service/inventory_switch/inv_aging_switch_us.flow` | `source/etl/flows/data_service/inventory_switch/inv_aging_switch_us.flow:155` |
| FLOW ref: `source/etl/flows/data_service/inventory_switch/inv_aging_switch_wcla.flow` | `source/etl/flows/data_service/inventory_switch/inv_aging_switch_wcla.flow:177` |
| ETL/script ref: `source/etl/sql/inventory/data_service/inventory/python/load_dw_inv_aging_view_levels.py` | `source/etl/sql/inventory/data_service/inventory/python/load_dw_inv_aging_view_levels.py:12` |
| ETL/script ref: `source/etl/sql/vendor/data_service/vpl_extract/python/load_dws_disty_brpt_extract_vpl_di.py` | `source/etl/sql/vendor/data_service/vpl_extract/python/load_dws_disty_brpt_extract_vpl_di.py:290` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_inventory/inv_aging_eta_rio_open_po_rds_7806.md` | `target/knowledgebase/RDS/starrocks_inventory/inv_aging_eta_rio_open_po_rds_7806.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_inventory/inv_qty_aging_runrate_rio_location_rds_5501.md` | `target/knowledgebase/RDS/starrocks_inventory/inv_qty_aging_runrate_rio_location_rds_5501.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/starrocks_vpo/vpo_inventory_open_po_eta_rio_runrate_rds_7806.md` | `target/knowledgebase/RDS/starrocks_vpo/vpo_inventory_open_po_eta_rio_runrate_rds_7806.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ap/ap_average_balance_multisheet_rds_9163.md` | `target/knowledgebase/RDS/vertica_ap/ap_average_balance_multisheet_rds_9163.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_b_report/b_report_lightweight_orders_inventory_rio_rds_7500.md` | `target/knowledgebase/RDS/vertica_b_report/b_report_lightweight_orders_inventory_rio_rds_7500.md:55` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_rio_alloc_rds_18605.md` | `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_rio_alloc_rds_18605.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_so_alloc_rds_17343.md` | `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_so_alloc_rds_17343.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_so_alloc_rds_17345.md` | `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_runrate_so_alloc_rds_17345.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_vendor_filter_rds_17484.md` | `target/knowledgebase/RDS/vertica_inventory/inv_aging_qty_vendor_filter_rds_17484.md:53` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_disty_inv_aging_df/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_aging_df.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_inv_aging_df.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_inv_aging_df` — FACT layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dw_us` (US baseline documented as `dw_us` / `dim_us`).

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
| **Query for reporting** | `dw_us.dwd_disty_inv_aging_df` | `dw_us.dwd_disty_inv_aging_df` | overwrite / incremental | POS contract `dwd_disty_inv_aging_df.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_inv_aging_df` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_inv_aging_df`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `sku_no`, `vend_no`, `part_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_inv_aging_df
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT sku_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_inv_aging_df
WHERE date_flag = '${partition_value}'
GROUP BY sku_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sku_no, vend_no, part_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_inv_aging_df
WHERE date_flag = '${partition_value}'
GROUP BY sku_no, vend_no, part_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `ave_cost` — ave cost
- `oh_cost` — oh cost
- `it_cost` — it cost
- `ext_oh_cost` — ext oh cost
- `ext_it_cost` — ext it cost
- `on_hand_qty` — on hand qty
- `ohand_qty` — ohand qty
- `itran_qty` — itran qty
- `qty1_30` — qty1 30
- `qty31_60` — qty31 60
- `qty61_90` — qty61 90
- `qty90_up` — qty90 up
- `age1_30` — age1 30
- `age31_60` — age31 60
- `age61_90` — age61 90
- `age90_up` — age90 up
- `qty91_120` — qty91 120
- `qty121_150` — qty121 150
- `qty151_180` — qty151 180
- `qty180_up` — qty180 up
- `qty240_up` — qty240 up
- `qty360_up` — qty360 up
- `age91_120` — age91 120
- `age121_150` — age121 150
- `age151_180` — age151 180
- ... and 15 additional measure columns (see column register)

### Dimension and key columns

- `view_level` — view level
- `view_key1` — view key1
- `view_key2` — view key2
- `view_key3` — view key3
- `inv_type` — inv type
- `sku_no` — sku no
- `u_version` — u version
- `prod_code` — prod code
- `vend_code` — vend code
- `vend_name` — vend name
- `vend_no` — vend no
- `part_no` — part no
- `intran_in` — intran in
- `date_flag` — date flag
- `company_no` — company no
- `etl_timestamp` — etl timestamp

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_inv_aging_df`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_inv_aging_df"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_inv_aging_df` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dw_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_aging_df.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_inv_aging_df.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 56 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_inv_aging_df.md`.*