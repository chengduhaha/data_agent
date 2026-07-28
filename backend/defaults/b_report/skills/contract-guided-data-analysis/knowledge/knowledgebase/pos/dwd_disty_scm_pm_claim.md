# PRIMARY: POS enrichment partner table joined from hub (`dw_us.dwd_disty_scm_pm_claim`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_scm_pm_claim
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_scm_pm_claim`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dw_us.dwd_disty_scm_pm_claim` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_scm_pm_claim schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql`
- **upstream:** `ods_${country}.ods_cis_corp_pm_claim` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql`
- **upstream:** `ods_${country}.ods_cis_corp_pm_claim_type` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql`
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
- Reporting: Vertica `dw_us.dwd_disty_scm_pm_claim` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["ods_${country}.ods_cis_corp_pm_claim"] --> T["dw_us.dwd_disty_scm_pm_claim"]
  S1["ods_${country}.ods_cis_corp_pm_claim_type"] --> T["dw_us.dwd_disty_scm_pm_claim"]
```

### Base tables register
| Object | Role |
|--------|------|
| `ods_${country}.ods_cis_corp_pm_claim` | source / temp (FROM/JOIN) |
| `ods_${country}.ods_cis_corp_pm_claim_type` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dw_us.dwd_disty_scm_pm_claim` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country}.ods_cis_corp_pm_claim` | `ods_${country}.ods_cis_corp_pm_claim_type` | many:1 (LEFT) | `pc.claim_type` = `pct.claim_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:5`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_disty_scm_pm_claim`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `project_no` | `pc.project_no` | `project_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_no` | `pc.claim_no` | `claim_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_descr` | `pc.claim_descr` | `claim_descr` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_type` | `pc.claim_type` | `claim_type` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `budget_amount` | `pc.budget_amount` | `budget_amount` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `actual_amount` | `pc.actual_amount` | `actual_amount` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `expect_date` | `pc.expect_date` | `expect_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `posting_date` | `pc.posting_date` | `posting_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vend_no` | `pc.vend_no` | `vend_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `loc_no` | `pc.loc_no` | `loc_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `pm_code` | `pc.pm_code` | `pm_code` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `pri_approv_ref_no` | `pc.pri_approv_ref_no` | `pri_approv_ref_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `pri_approv_amt` | `pc.pri_approv_amt` | `pri_approv_amt` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `doc_terms` | `pc.doc_terms` | `doc_terms` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `entry_datetime` | `pc.entry_datetime` | `entry_datetime` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `entry_id` | `pc.entry_id` | `entry_id` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `entry_obj` | `pc.entry_obj` | `entry_obj` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `delete_date` | `pc.delete_date` | `delete_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `delete_id` | `pc.delete_id` | `delete_id` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `delete_obj` | `pc.delete_obj` | `delete_obj` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `contact_no` | `pc.contact_no` | `contact_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `inv_date` | `pc.inv_date` | `inv_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vend_comments` | `pc.vend_comments` | `vend_comments` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `foreign_bug_amount` | `pc.foreign_bug_amount` | `foreign_bug_amount` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `foreign_act_amount` | `pc.foreign_act_amount` | `foreign_act_amount` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vpl_no` | `pc.vpl_no` | `vpl_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vpc_group_id` | `pc.vpc_group_id` | `vpc_group_id` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `last_claim` | `pc.last_claim` | `last_claim` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `exp_amt` | `pc.exp_amt` | `exp_amt` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_start_date` | `pc.claim_start_date` | `claim_start_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_end_date` | `pc.claim_end_date` | `claim_end_date` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `credit_note` | `pc.credit_note` | `credit_note` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `foreign_exp_amt` | `pc.foreign_exp_amt` | `foreign_exp_amt` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `foreign_approv_amt` | `pc.foreign_approv_amt` | `foreign_approv_amt` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `accrual_amt` | `pc.accrual_amt` | `accrual_amt` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_code` | `pc.claim_code` | `claim_code` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `claim_curr` | `pc.claim_curr` | `claim_curr` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vend_src` | `pc.vend_src` | `vend_src` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `vend_src_ref_no` | `pc.vend_src_ref_no` | `vend_src_ref_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `cust_no` | `pc.cust_no` | `cust_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:2` |
| `descr` | `pct.descr` | `descr` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `revenue_acct_no` | `pct.revenue_acct_no` | `revenue_acct_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `receive_acct_no` | `pct.receive_acct_no` | `receive_acct_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `pm_class` | `pct.pm_class` | `pm_class` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `program_type` | `pct.program_type` | `program_type` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `active` | `pct.active` | `active` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `dept` | `pct.dept` | `dept` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `percentage` | `pct.percentage` | `percentage` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `discretionary_fund` | `pct.discretionary_fund` | `discretionary_fund` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `profit_acct_no` | `pct.profit_acct_no` | `profit_acct_no` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |
| `internal` | `pct.internal` | `internal` | `ods_${country}.ods_cis_corp_pm_claim`, `ods_${country}.ods_cis_corp_pm_claim_type` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql:3` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql` |
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
| `ods_${country}.ods_cis_corp_pm_claim` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql` |
| `ods_${country}.ods_cis_corp_pm_claim_type` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/dwd_disty_scm_pm_claim.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:206` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_scm_pm_claim.md` | `source/contracts/pos/tables/dwd_disty_scm_pm_claim.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_b_report/etl/b_report_acq_cloud_legacy_invoice_rds_1241.sql` | `source/contracts/rds/vertica_b_report/etl/b_report_acq_cloud_legacy_invoice_rds_1241.sql:19` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_b_report/b_report_acq_cloud_legacy_invoice_rds_1241.md` | `target/knowledgebase/RDS/vertica_b_report/b_report_acq_cloud_legacy_invoice_rds_1241.md:53` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:73` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_disty_scm_pm_claim/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_scm_pm_claim.md`

## Business purpose

POS enrichment partner table joined from hub

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_scm_pm_claim` — PRIMARY layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_scm_pm_claim` | `dw_us.dwd_disty_scm_pm_claim` | overwrite / incremental | POS contract `dwd_disty_scm_pm_claim.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_scm_pm_claim` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_scm_pm_claim`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `project_no`, `claim_no`, `vend_no`, `loc_no`, `pri_approv_ref_no`, `entry_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT project_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY project_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT project_no, claim_no, vend_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_scm_pm_claim
WHERE date_flag = '${partition_value}'
GROUP BY project_no, claim_no, vend_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `budget_amount` — budget amount
- `actual_amount` — actual amount
- `pri_approv_amt` — pri approv amt
- `foreign_bug_amount` — foreign bug amount
- `foreign_act_amount` — foreign act amount
- `exp_amt` — exp amt
- `foreign_exp_amt` — foreign exp amt
- `foreign_approv_amt` — foreign approv amt
- `accrual_amt` — accrual amt
- `percentage` — percentage

### Dimension and key columns

- `project_no` — project no
- `claim_no` — claim no
- `claim_descr` — claim descr
- `claim_type` — claim type
- `expect_date` — expect date
- `posting_date` — posting date
- `vend_no` — vend no
- `loc_no` — loc no
- `pm_code` — pm code
- `pri_approv_ref_no` — pri approv ref no
- `doc_terms` — doc terms
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `entry_obj` — entry obj
- `delete_date` — delete date
- `delete_id` — delete id
- `delete_obj` — delete obj
- `contact_no` — contact no
- `inv_date` — inv date
- `vend_comments` — vend comments
- `vpl_no` — vpl no
- `vpc_group_id` — vpc group id
- `last_claim` — last claim
- `claim_start_date` — claim start date
- `claim_end_date` — claim end date
- `credit_note` — credit note
- `claim_code` — claim code
- `claim_curr` — claim curr
- `vend_src` — vend src
- `vend_src_ref_no` — vend src ref no

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_scm_pm_claim`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_scm_pm_claim"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_scm_pm_claim` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_scm_pm_claim.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 51 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_scm_pm_claim.md`.*