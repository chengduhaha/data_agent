# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_ar_cust_doc_df`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_ar_cust_doc_df
- domain: pos
- one_line_purpose: POS-domain fact table with load SQL now available under bitbucket-etl (see L3); prior contract narrative preserved below.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/
- related_etl_scripts:
- `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_ar_cust_doc_df.sql`

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_ar_cust_doc_df`
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
| **entity_id** | `dw_us.dwd_disty_ar_cust_doc_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain (`date_flag` when documented) |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_ar_cust_doc_df schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_terms_file` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_manager` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_order_type` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `temp_orders` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_etl_order_comments_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_customer_header` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_cust_xref` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_cust_profile` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_etl_order_header_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_etl_order_soldto_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_territory` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_cust_type` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_division` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `temp_analyst` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_etl_order_detail_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_part_master` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_vend_master` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_etl_order_exp_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
- **upstream:** `${literal_source_db}.ods_cis_corp_project_info` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`
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
- Reporting: Vertica `dw_us.dwd_disty_ar_cust_doc_df` (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic
ETL WHERE / JOIN predicates are summarized via Relationship map provenance and Column derivations; full narrative retained in preserved sections.

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql
```

### End-to-end flow
```mermaid
flowchart LR
  ETL["dwd_disty_ar_cust_doc_df bitbucket-etl"] --> TGT["dw_us.dwd_disty_ar_cust_doc_df"]
```

### Base tables register
| Object | Role |
|--------|------|
| See Relationship map + preserved lineage | ETL sources / temps |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/`.
2. Apply date / business filters from ETL.
3. Write target `dw_us.dwd_disty_ar_cust_doc_df` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_terms_file` | many:1 (LEFT) | trim(cd.terms) = trim(tf.doc_terms) | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:27`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_manager` | many:1 (LEFT) | `cd.entry_id` = `mg.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:29`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_order_type` | many:1 (LEFT) | `cd.order_type` = `ot.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:31`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_comments_all` | many:1 | `cd.order_no` = `b.order_no`; `cd.order_type` = `b.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:55`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_customer_header` | many:1 | `cd.cust_no` = `ch.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:76`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_cust_xref` | many:1 (LEFT) | `cd.cust_no` = `cx.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:78`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_cust_xref` | many:1 (LEFT) | `cd.cust_no` = `cx1.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:80`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_cust_profile` | many:1 (LEFT) | `cd.cust_no` = `cp.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:82`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_header_all` | many:1 | `cd.order_type` = `hh.order_type`; `cd.order_no` = `hh.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:110`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_soldto_all` | many:1 | `cd.order_type` = `os.order_type`; `cd.order_no` = `os.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:132`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_territory` | many:1 | `ch.sales_terr` = `t.sales_terr` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:150`) |
| `${literal_source_db}.ods_cis_corp_territory` | `${literal_source_db}.ods_cis_corp_cust_type` | many:1 | `t.cust_type` = `ct.cust_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:152`) |
| `${literal_source_db}.ods_cis_corp_cust_type` | `${literal_source_db}.ods_cis_corp_division` | many:1 | `di.division` = `ct.division` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:154`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_customer_header` | many:1 | `a.cust_no` = `cd.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:177`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_territory` | many:1 (LEFT) | `a.sales_terr` = `b.sales_terr` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:179`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_cust_xref` | many:1 (LEFT) | `a.cust_no` = `c.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:181`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_cust_xref` | many:1 (LEFT) | `a.cust_no` = `d.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:185`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_manager` | many:1 (LEFT) | `mg.userid` = `a.credit_analyst` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:206`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_manager` | many:1 (LEFT) | `mg1.userid` = `a.service_analyst` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:208`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_manager` | many:1 (LEFT) | `mg2.userid` = `a.collector_id` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:210`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_manager` | many:1 (LEFT) | `mg3.userid` = `a.program_analyst` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:212`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_detail_all` | many:1 | `cd.order_type` = `b.order_type`; `cd.order_no` = `b.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:233`) |
| `temp_cust_doc` | `${literal_source_db}.ods_cis_corp_part_master` | many:1 | `b.sku_no` = `pm.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:235`) |
| `${literal_source_db}.ods_cis_corp_part_master` | `${literal_source_db}.ods_cis_corp_vend_master` | many:1 | `pm.vend_no` = `vm.vend_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:237`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_exp_all` | many:1 | `cd.order_no` = `he.order_no`; `cd.order_type` = `he.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:250`) |
| `${literal_source_db}.ods_etl_order_exp_all` | `${literal_source_db}.ods_cis_corp_project_info` | many:1 | `he.project_no` = `p.proj_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:252`) |
| `${literal_source_db}.ods_cis_corp_project_info` | `${literal_source_db}.ods_cis_corp_no_ctrl` | many:1 | `p.var_no` = `nc.doc_num` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:255`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_etl_order_profile_all` | many:1 | `cd.order_no` = `op.order_no`; `cd.order_type` = `op.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:276`) |
| `${literal_source_db}.ods_dw_prod_dws_history_cust_doc` | `${literal_source_db}.ods_cis_corp_cust_doc_profile` | many:1 | `cd.order_no` = `op.order_no`; `cd.order_type` = `op.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:290`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_cust_doc` | many:1 (LEFT) | `a.date_flag` = `b.date_flag`; `a.order_type` = `b.order_type`; `a.order_no` = `b.order_no`; `a.cust_no` = `b.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:405`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_contact_name` | many:1 (LEFT) | `a.order_type` = `c.order_type`; `a.order_no` = `c.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:407`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_cust_details` | many:1 (LEFT) | `a.order_type` = `d.order_type`; `a.order_no` = `d.order_no`; `a.cust_no` = `d.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:409`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_ship_details` | many:1 (LEFT) | `a.order_type` = `e.order_type`; `a.order_no` = `e.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:411`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_end_user_pos` | many:1 (LEFT) | `a.order_type` = `f.order_type`; `a.order_no` = `f.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:413`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_terr_details` | many:1 (LEFT) | `a.cust_no` = `g.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:415`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_analyst_details` | many:1 (LEFT) | `a.order_type` = `h.order_type`; `a.order_no` = `h.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:417`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_order_detail_vend_info` | many:1 (LEFT) | `a.order_type` = `vi.order_type`; `a.order_no` = `vi.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:419`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_order_exp_info` | many:1 (LEFT) | `a.order_type` = `ei.order_type`; `a.order_no` = `ei.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:421`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_order_profile_info` | many:1 (LEFT) | `a.order_type` = `pi.order_type`; `a.order_no` = `pi.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:423`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_cust_doc_profile_info` | many:1 (LEFT) | `a.order_type` = `cdp.order_type`; `a.order_no` = `cdp.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:425`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_cust_doc_nf_info` | many:1 (LEFT) | `a.order_type` = `cdf.order_type`; `a.order_no` = `cdf.order_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:427`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `${literal_source_db}.ods_cis_corp_cust_profile` | many:1 (LEFT) | `a.cust_no` = `cp2.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:429`) |
| `${literal_source_db}.ods_cis_corp_customer_header` | `temp_company_2lc_profile_info` | many:1 (LEFT) | `a.company_no` = `cpp2.company_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:431`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_disty_ar_cust_doc_df`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `a.order_type` | `order_type` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:196` |
| `order_no` | `a.order_no` | `order_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:195` |
| `u_version` | `a.u_version` | `u_version` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:326` |
| `cust_no` | `a.cust_no` | `cust_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:178` |
| `cust_name` | `d.cust_name` | `cust_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:328` |
| `loc_no` | `a.loc_no` | `loc_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:329` |
| `amount` | `a.amount` | `amount` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:330` |
| `amt_current` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `doc_date` | `a.doc_date` | `doc_date` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:332` |
| `close_date` | `a.close_date` | `close_date` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:333` |
| `applied` | `a.applied` | `applied` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:334` |
| `due_date` | `a.due_date` | `due_date` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:335` |
| `reference` | `a.reference` | `reference` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:336` |
| `terms` | `a.terms` | `terms` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:337` |
| `terms_desc` | `b.terms_desc` | `terms_desc` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:338` |
| `terms_days` | `b.terms_days` | `terms_days` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:339` |
| `disc_percent` | `b.disc_percent` | `disc_percent` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:340` |
| `disc_days` | `b.disc_days` | `disc_days` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:341` |
| `terms_type` | `b.terms_type` | `terms_type` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:342` |
| `terms_group` | `b.terms_group` | `terms_group` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:343` |
| `entry_datetime` | `a.entry_datetime` | `entry_datetime` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:344` |
| `entry_id` | `a.entry_id` | `entry_id` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:345` |
| `entry_name` | `b.entry_name` | `entry_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:346` |
| `me_applied` | `a.me_applied` | `me_applied` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:347` |
| `credit_code` | `a.credit_code` | `credit_code` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:348` |
| `snap_date` | `a.snap_date` | `snap_date` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:349` |
| `usd_amt` | `a.usd_amt` | `usd_amt` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:350` |
| `usd_applied` | `a.usd_applied` | `usd_applied` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:351` |
| `reference2` | `a.reference2` | `reference2` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:352` |
| `company_no` | `a.company_no` | `company_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:353` |
| `fx_currency` | `a.fx_currency` | `fx_currency` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:354` |
| `disc_amt_used` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `usd_disc_amt_used` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `due_date_agedays` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `doc_date_agedays` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `finance_mcust_no` | `d.finance_mcust_no` | `finance_mcust_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:359` |
| `mcust_no` | `d.mcust_no` | `mcust_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:360` |
| `sales_terr` | `g.sales_terr` | `sales_terr` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:361` |
| `terr_name` | `g.terr_name` | `terr_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:362` |
| `cust_type` | `g.cust_type` | `cust_type` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:363` |
| `cust_type_desc` | `g.cust_type_descr` | `cust_type_descr` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:364` |
| `division` | `g.division` | `division` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:365` |
| `division_desc` | `g.division_desc` | `division_desc` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:366` |
| `default_terms` | `d.default_terms` | `default_terms` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:367` |
| `region` | `g.region` | `region` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:368` |
| `credit_analyst` | `h.credit_analyst` | `credit_analyst` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:369` |
| `credit_analyst_name` | `h.credit_analyst_name` | `credit_analyst_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:370` |
| `program_analyst` | `h.program_analyst` | `program_analyst` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:371` |
| `program_analyst_name` | `h.program_analyst_name` | `program_analyst_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:372` |
| `service_analyst` | `h.service_analyst` | `service_analyst` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:373` |
| `service_analyst_name` | `h.service_analyst_name` | `service_analyst_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:374` |
| `collector_id` | `h.collector_id` | `collector_id` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:375` |
| `collector_name` | `h.collector_name` | `collector_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:376` |
| `release_code` | `d.release_code` | `release_code` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:377` |
| `credit_limit` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `next_review` | `d.next_review` | `next_review` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:379` |
| `pending_amt` | `NULL` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `order_type_desc` | `b.order_type_descr` | `order_type_descr` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:381` |
| `contact_name` | `c.contact_name` | `contact_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:382` |
| `cust_currency` | `d.cust_currency` | `cust_currency` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:383` |
| `ship_to_name` | `e.ship_to_name` | `ship_to_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:384` |
| `ship_to_addr` | `e.ship_to_addr` | `ship_to_addr` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:385` |
| `ship_to_state` | `e.ship_to_state` | `ship_to_state` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:386` |
| `ship_to_country` | `e.ship_to_country` | `ship_to_country` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:387` |
| `ship_to_city` | `e.ship_to_city` | `ship_to_city` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:388` |
| `ship_to_zip` | `e.ship_to_zip` | `ship_to_zip` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:389` |
| `from_loc_no` | `e.from_loc_no` | `from_loc_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:390` |
| `drop_ship` | `e.drop_ship` | `drop_ship` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:391` |
| `end_user_po` | `f.end_user_po` | `end_user_po` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:392` |
| `vend_no` | `vi.vend_no` | `vend_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:393` |
| `vend_name` | `vi.vend_name` | `vend_name` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:394` |
| `commission_amt` | `ei.commission_amt` | `commission_amt` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:395` |
| `fx_rate` | `pi.fx_rate` | `fx_rate` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:396` |
| `gl_account` | `case when cp2.profile_i is not null then 136012 else 110000 end` | `profile_i` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | case | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:397` |
| `payment_expected_date` | `cdp.payment_expected_date` | `payment_expected_date` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:398` |
| `nf_no` | `cdf.nf_no` | `nf_no` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:399` |
| `amount_2lc` | `null` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `applied_2lc` | `null` | — | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:58` |
| `currency_2lc` | `cpp2.currency_2lc` | `currency_2lc` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:402` |
| `date_flag` | `date_format(a.date_flag,'yyyy-MM-dd')` | `date_flag`, `yyyy`, `MM`, `dd` | `${literal_source_db}.ods_dw_prod_dws_history_cust_doc`, `temp_cust_doc`, `temp_contact_name`, `temp_cust_details`, `temp_ship_details`, `temp_end_user_pos`, `temp_terr_details`, `temp_analyst_details`, `temp_order_detail_vend_info`, `temp_order_exp_info`, `temp_order_profile_info`, `temp_cust_doc_profile_info` | arithmetic | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql:403` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql` |
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
| ETL FROM/JOIN objects | load | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/dwd_disty_ar_cust_doc_df.sql` (see Relationship map) |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/b-report-us/A Dependent dataset of P&L Item 1.md` | `source/contracts/b-report-us/A Dependent dataset of P&L Item 1.md:137` |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:144` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_ar_cust_doc_df.md` | `source/contracts/pos/tables/dwd_disty_ar_cust_doc_df.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_ar/etl/ar_discount_payment_timing_rds_19383.sql` | `source/contracts/rds/vertica_ar/etl/ar_discount_payment_timing_rds_19383.sql:56` |
| ETL/script ref: `source/contracts/rds/vertica_ar/etl/ar_long_aged_365_500_multisheet_rds_9041.sql` | `source/contracts/rds/vertica_ar/etl/ar_long_aged_365_500_multisheet_rds_9041.sql:23` |
| ETL/script ref: `source/contracts/rds/vertica_ar/etl/ar_open_aging_customer_activity_credit_limit_rds_11417.sql` | `source/contracts/rds/vertica_ar/etl/ar_open_aging_customer_activity_credit_limit_rds_11417.sql:56` |
| ETL/script ref: `source/contracts/rds/vertica_ar/etl/ar_pos_rma_credit_reason_trace_rds_5576.sql` | `source/contracts/rds/vertica_ar/etl/ar_pos_rma_credit_reason_trace_rds_5576.sql:102` |
| KB / contract ref: `source/contracts/rds/vertica_ar/examples-index.md` | `source/contracts/rds/vertica_ar/examples-index.md:15` |
| FLOW ref: `source/etl/flows/data_service/ar/ar_aging_load_br.flow` | `source/etl/flows/data_service/ar/ar_aging_load_br.flow:371` |
| FLOW ref: `source/etl/flows/data_service/ar/ar_aging_load_ca.flow` | `source/etl/flows/data_service/ar/ar_aging_load_ca.flow:371` |
| FLOW ref: `source/etl/flows/data_service/ar/ar_aging_load_us.flow` | `source/etl/flows/data_service/ar/ar_aging_load_us.flow:371` |
| FLOW ref: `source/etl/flows/data_service/ar/ar_aging_load_wcla.flow` | `source/etl/flows/data_service/ar/ar_aging_load_wcla.flow:371` |
| FLOW ref: `source/etl/flows/data_service/ar/ar_data_initialization_us.flow` | `source/etl/flows/data_service/ar/ar_data_initialization_us.flow:39` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/python/ar_cust_sum_age_temp.py` | `source/etl/sql/ar/data_service/ar/python/ar_cust_sum_age_temp.py:27` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/sql/dm_disty_ar_aging_summary_df.sql` | `source/etl/sql/ar/data_service/ar/sql/dm_disty_ar_aging_summary_df.sql:7` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/sql/dwd_ar_cust_doc_df.sql` | `source/etl/sql/ar/data_service/ar/sql/dwd_ar_cust_doc_df.sql:2` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/sql/dwd_disty_credit_cust_doc_profile_df.sql` | `source/etl/sql/ar/data_service/ar/sql/dwd_disty_credit_cust_doc_profile_df.sql:149` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/sql/dws_ar_cust_sum_age_df.sql` | `source/etl/sql/ar/data_service/ar/sql/dws_ar_cust_sum_age_df.sql:102` |
| ETL/script ref: `source/etl/sql/ar/data_service/ar/sql/dws_ar_cust_sum_age_dso_df.sql` | `source/etl/sql/ar/data_service/ar/sql/dws_ar_cust_sum_age_dso_df.sql:7` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ar/ar_discount_payment_timing_rds_19383.md` | `target/knowledgebase/RDS/vertica_ar/ar_discount_payment_timing_rds_19383.md:52` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ar/ar_long_aged_365_500_multisheet_rds_9041.md` | `target/knowledgebase/RDS/vertica_ar/ar_long_aged_365_500_multisheet_rds_9041.md:51` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ar/ar_open_aging_customer_activity_credit_limit_rds_11417.md` | `target/knowledgebase/RDS/vertica_ar/ar_open_aging_customer_activity_credit_limit_rds_11417.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ar/ar_pos_rma_credit_reason_trace_rds_5576.md` | `target/knowledgebase/RDS/vertica_ar/ar_pos_rma_credit_reason_trace_rds_5576.md:54` |
| KB / contract ref: `target/knowledgebase/ar/ar_cust_sum_age_temp.md` | `target/knowledgebase/ar/ar_cust_sum_age_temp.md:6` |
| KB / contract ref: `target/knowledgebase/ar/dm_disty_ar_aging_summary_df.md` | `target/knowledgebase/ar/dm_disty_ar_aging_summary_df.md:59` |
| KB / contract ref: `target/knowledgebase/ar/dwd_ar_cust_doc_df.md` | `target/knowledgebase/ar/dwd_ar_cust_doc_df.md:1` |
| KB / contract ref: `target/knowledgebase/ar/dwd_disty_credit_cust_doc_profile_df.md` | `target/knowledgebase/ar/dwd_disty_credit_cust_doc_profile_df.md:6` |
| KB / contract ref: `target/knowledgebase/ar/dws_ar_cust_sum_age_df.md` | `target/knowledgebase/ar/dws_ar_cust_sum_age_df.md:62` |
| KB / contract ref: `target/knowledgebase/ar/dws_ar_cust_sum_age_dso_df.md` | `target/knowledgebase/ar/dws_ar_cust_sum_age_dso_df.md:59` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:53` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_disty_ar_cust_doc_df/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_cust_doc_df.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_ar_cust_doc_df.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_ar_cust_doc_df` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_ar_cust_doc_df` | `dw_us.dwd_disty_ar_cust_doc_df` | overwrite / incremental | POS contract `dwd_disty_ar_cust_doc_df.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_ar_cust_doc_df` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_ar_cust_doc_df`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `order_type`, `order_no`, `cust_no`, `loc_no`, `entry_id`, `finance_mcust_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_ar_cust_doc_df
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT order_type, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_ar_cust_doc_df
WHERE date_flag = '${partition_value}'
GROUP BY order_type
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT order_type, order_no, cust_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_ar_cust_doc_df
WHERE date_flag = '${partition_value}'
GROUP BY order_type, order_no, cust_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `amount` — amount
- `amt_current` — amt current
- `applied` — applied
- `disc_percent` — disc percent
- `me_applied` — me applied
- `usd_amt` — usd amt
- `usd_applied` — usd applied
- `disc_amt_used` — disc amt used
- `usd_disc_amt_used` — usd disc amt used
- `credit_limit` — credit limit
- `pending_amt` — pending amt
- `commission_amt` — commission amt
- `fx_rate` — fx rate
- `amount_2lc` — amount 2lc
- `applied_2lc` — applied 2lc

### Dimension and key columns

- `order_type` — order type
- `order_no` — order no
- `u_version` — u version
- `cust_no` — cust no
- `cust_name` — cust name
- `loc_no` — loc no
- `doc_date` — doc date
- `close_date` — close date
- `due_date` — due date
- `reference` — reference
- `terms` — terms
- `terms_desc` — terms desc
- `terms_days` — terms days
- `disc_days` — disc days
- `terms_type` — terms type
- `terms_group` — terms group
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `entry_name` — entry name
- `credit_code` — credit code
- `snap_date` — snap date
- `reference2` — reference2
- `company_no` — company no
- `fx_currency` — fx currency
- `due_date_agedays` — due date agedays
- `doc_date_agedays` — doc date agedays
- `finance_mcust_no` — finance mcust no
- `mcust_no` — mcust no
- `sales_terr` — sales terr
- `terr_name` — terr name

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_ar_cust_doc_df`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_ar_cust_doc_df"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_ar_cust_doc_df` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_cust_doc_df.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_ar_cust_doc_df.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 82 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_cust_doc_df.md`.*