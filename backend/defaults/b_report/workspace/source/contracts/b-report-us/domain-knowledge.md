# Domain Knowledge - b-report-us

- contract_version: v2.0.0
- artifact_type: domain-knowledge
- artifact_id: b-report-us

## Domain Scope

- Domain name: b-report-us
- Geographic scope: US (`dw_us` / `dm_us` / `dim_us` schema baseline)
- Business scope: B Report shipped-order profitability and operating performance analytics.

## Business Perspective

- analytical_stance: US disty B Report analytics from the **TD SYNNEX distributor lens** — metrics reflect shipped-order profitability through our channel (who we buy from and who we sell to), not OEM or end-customer financial statements.
- customer_semantics: `customer` / `cust_*` means **channel reseller or partner** (who TD SYNNEX sells to). It is **not** the end user or consumer, and **not** an upstream OEM brand token (for example CISCO, Dell, HP used alone in a sales/trend question).
- end_customer_semantics: terminal buyers are distinguished on customer master via attributes such as `cust_acct_type` (for example Reseller vs End User). End-customer scope requires explicit account-type or end-user intent; do not infer end customer from bare manufacturer brand tokens.
- vendor_semantics: `vendor` / `vend_*` means **upstream OEM or manufacturer** (Cisco, Dell, HP, etc.) — who we buy from. Resolve brand tokens on `dim_us.dim_pub_vendor_info` (`vend_name`, `master_vend_name`, `universal_vend_name`).
- vpl_semantics: VPL / VPC is a **vendor product line or category** under a vendor (finer grain than vendor). Examples: product line codes, `vpc_group_desc`, VPC-named categories.
- product_semantics: `product` / part identifiers (`sku_no`, `part_no`, `mfg_partno`) are sellable SKUs under vendor lines — distinct from vendor brand and from VPL category labels.
- territory_semantics: `territory` / `sales_terr` / `cust_terr` means **TD SYNNEX sales territory assignment** for customer geography and sales-hierarchy rollups — not vendor region, not shipping address, and not end-customer location unless explicitly scoped via customer master attributes.
- order_semantics: `order` / `order_no` means a **shipped order header** at order-line grain on `dw_us.dwd_disty_brpt_orders_pl_etl_mi`; order-scoped questions route to DWD row detail, not DWS/DM aggregates.
- disambiguation_rules: bare OEM brand token plus sales/revenue/trend language → **prefer vendor** over vpl or customer; explicit VPC/VPL/product-line wording → **prefer vpl**; territory/terr/sales-territory wording → **prefer territory** over bare customer name; never map well-known OEM brands to `customer`; ranking/breakdown uses integer join keys (`vend_no`, `cust_no`, `vpl_no`, `sales_terr`) not name columns alone.

## Entity Ontology

- entity_type: `vendor` | business_role: upstream OEM/manufacturer (buy-side) | join_key: `vend_no` | dim_fqn: `dim_us.dim_pub_vendor_info` | filter_key_label: `vendor_label` | filter_key_integer: `vend_no` | default_prior: 0.80 | over_entity_types: `vpl`, `product` | exclude_when: user explicitly scopes VPC/VPL/product line, or token is a part/SKU identifier
- entity_type: `customer` | business_role: channel reseller/partner (sell-side) | join_key: `cust_no` | dim_fqn: `dim_us.dim_pub_customer_info` | filter_key_label: `customer_label` | filter_key_integer: `cust_no` | default_prior: 0.70 | over_entity_types: — | exclude_when: token matches known OEM/manufacturer brand, or user scopes vendor/VPL/product/part explicitly
- entity_type: `vpl` | business_role: vendor product line / VPC category under vendor | join_key: `vpl_no` | dim_fqn: `dim_us.dim_pub_vpl_info` | filter_key_label: `vpl_label` | filter_key_integer: `vpl_no` | default_prior: 0.55 | over_entity_types: `product` | exclude_when: bare OEM brand with sales/trend and no VPC/VPL/product-line cue; prefer vendor in that case
- entity_type: `product` | business_role: sellable SKU/part under vendor line | join_key: `sku_no` | dim_fqn: `dim_us.dim_pub_part_info` | filter_key_label: `part_identifier` | filter_key_integer: — | default_prior: 0.65 | over_entity_types: — | exclude_when: user scopes vendor brand only without part/SKU token, or scopes VPL/VPC category without part number
- entity_type: `pm` | business_role: product manager hierarchy owner | join_key: `pm_id` | dim_fqn: `dim_us.dim_pub_vpl_hierarchy_info` | filter_key_label: — | filter_key_integer: `pm_id` | default_prior: 0.60 | over_entity_types: — | exclude_when: user scopes customer, vendor, part, or VPL without PM id/token
- entity_type: `territory` | business_role: sales territory / geography for customer assignment and sales-org rollups | join_key: `sales_terr` | dim_fqn: `dim_us.dim_pub_sales_territory` | filter_key_label: `territory_label` | filter_key_integer: `sales_terr` | default_prior: 0.55 | over_entity_types: `customer` | exclude_when: user scopes master/sub customer name only without territory cues, or asks for vendor/VPL/product/part explicitly
- entity_type: `order` | business_role: shipped order header at order-line grain | join_key: `order_no` | dim_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | filter_key_label: — | filter_key_integer: `order_no` | default_prior: 0.90 | over_entity_types: — | exclude_when: user asks scalar KPI or ranking without order#, list, or order-line audit cues

## Shared Definitions

- Naming convention: `[dw layer]_[biz unit]_[biz domain]_[biz group]_[date granularity]`.
- Layer semantics: DWD=detail, DWS=summary, DM=data mart serving, DIM=shared dimensions.
- Date suffix semantics:
  - `1d`: daily snapshot for the business date
  - `wtd`: week-to-date cumulative
  - `mtd`: month-to-date cumulative
  - `comb_mtd`: combined monthly view with cm/pm/ppm/lm period columns (month-end snapshot semantics)

## month_no Encoding

- `month_no` is an **internal fiscal period index**, not natural YYYYMM.
- Always map calendar/fiscal intent through `dim_us.dim_pub_date` joined on `date_flag`.
- Anti-pattern: `month_no = 202601` without verifying encoding for the target table family.

## comb_mtd Semantics

- `*_comb_mtd` tables expose current month (cm), prior month (pm), prior-prior month (ppm), and last month (lm) metric columns on a single row per dimension grain.
- Values are typically **month-end snapshots** (last `date_flag` in the period), not naive sums across all days unless the specific metric family documents cumulative behavior.
- Do not sum comb_mtd columns across unrelated period labels in one aggregation without confirming metric semantics in `metric-index.md`.

## Cross-Engine Presence

- Hive and Vertica both contain `disty_brpt` table families under `dw_us`, `dm_us`, and `dim_us`.
- Prefer canonical table names without `_bkp` / `_temp` suffix unless troubleshooting historical loads.
- Known lag: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` Vertica max `date_flag` can run ahead of Hive (observed June 2026: Vertica 2026-06-20 vs Hive 2026-06-09). Reconcile cross-engine reports with explicit as-of engine choice.


## dim_pub_date Fiscal Column Mapping

- Table: `dim_us.dim_pub_date` (see `tables/dim_pub_date.md` in this domain).
- Verified Vertica columns for fiscal filtering (do **not** use `fiscal_year` / `fiscal_period`):
  - `fyear`: fiscal year integer
  - `month`: calendar month integer (1–12)
  - `m`: internal fiscal month index (maps to `month_no` on serving tables)
  - `fqtr`: fiscal quarter integer
  - `date_flag`: join key to facts and serving tables
- Prefer natural-month filters via `date_flag` ranges when fiscal period semantics are ambiguous.
- Customer master/sub breakdown: prefer `dw_us.dws_disty_brpt_cust_mtd`; filter master via `mcust_name`; **GROUP BY `cust_no`** for sub-customer ranking; use `cust_name` as display label only (see Entity Key Registry and golden `cdw-sub-customer-ranking`).
- Vendor ranking by net sales: prefer `dw_us.dws_disty_brpt_vend_mtd`; filter month via month-end `date_flag`; **GROUP BY `vend_no`**; use `vend_name` as display only (golden `jan-vendor-top5-ranking`).
- Territory-scoped metrics: prefer `dw_us.dws_disty_brpt_cust_mtd` when customer+territory grain matches (`cust_terr`, denormalized `terr_name`); Phase-1 resolve labels on `dim_us.dim_pub_sales_territory` (`terr_name`, `group_desc`, `sub_group_desc`); join facts on `cust_terr` = `sales_terr`; extended P&L dimensions → `dw_us.dws_disty_brpt_pl_extend_mtd` (see `tables/dim_pub_sales_territory.md`).

## Entity Key Registry

- customer join key: `cust_no` (int) | searchable labels: `cust_name`, `mcust_name` (varchar on `dim_us.dim_pub_customer_info`) | master key: `mcust_no` | display labels: `cust_name` (sub-customer), `mcust_name` (master customer)
- customer label aliases: `customer`, `account`, `master customer` → resolve via `dim_us.dim_pub_customer_info`; master scope via `mcust_name`; sub-customer via `cust_name`; never compare alphanumeric tokens to `cust_no` (integer); end-user scope via `cust_acct_type`, not bare OEM brands
- vendor join key: `vend_no` (int) | searchable labels: `vend_name`, `master_vend_name`, `universal_vend_name` (varchar on `dim_us.dim_pub_vendor_info`) | display labels: `vend_name`, `master_vend_name`
- vendor label aliases: `vendor`, `manufacturer`, `mfr`, OEM brand tokens (Cisco, Dell, HP, etc.) → resolve via `dim_us.dim_pub_vendor_info`; roll up via `master_vend_no` / `universal_vend_no` when brand-family scope; never compare alphanumeric tokens to `vend_no` (integer)
- product join key: `sku_no` (int) | searchable labels: `part_no`, `mfg_partno` (varchar on `dim_us.dim_pub_part_info` and denormalized on `dw_us.dws_disty_brpt_part_*`) | display labels: `short_desc`, `long_desc`
- product label aliases: `mfg_part_no`, `mfr_part_no`, `manufacturer part` → physical column `mfg_partno`; user token "part X" may match `part_no` or `mfg_partno` — never compare alphanumeric tokens to `sku_no` or `prod_code` (integer)
- vpl join key: `vpl_no` (int) | searchable labels: `vpl_code`, `vpl_desc`, `vpc_group_desc` (varchar on `dim_us.dim_pub_vpl_info` and denormalized on `dw_us.dws_disty_brpt_vpl_*`) | display labels: `vpl_code`, `vpc_group_desc`
- vpl label aliases: `VPC`, `vendor product code`, `product line`, `vpl` → resolve via `dim_us.dim_pub_vpl_info`; user token "VPC X" or "for X" with vpc/vpl context may match `vpc_group_desc`, `vpl_desc`, or `vpl_code` — never compare alphanumeric tokens to `vpl_no` (integer)
- vpc disambiguation: in questions like "revenue for VPC Scanners", `VPC` names the **dimension** (vendor product category / `vpc_group_desc`), not a literal code value; the entity search token is `Scanners`, not `VPC Scanners`; strip leading `VPC ` / `VPL ` per `label_prefix_strip` before Phase-1 dim search
- vpc group key: `vpc_group_id` (int) | label: `vpc_group_desc` | searchable on dim and serving `dws_disty_brpt_vpl_*`
- rule: `vpl_code` is not unique — always resolve to `vpl_no` before joining facts when multiple matches; disambiguate with `vend_no` when needed
- rule: breakdown/ranking `GROUP BY` must use business keys (`*_no`, `*_id` when integer); `*_name` and varchar label columns are for filter/display only
- rule: routing-certified SQL must come from `golden-questions.md` with matching `golden_ref`; do not invent L6 representative SQL during enrich
- territory join key: `sales_terr` (int) | fact alias: `cust_terr` on order-line and serving tables | searchable labels: `terr_name`, `group_desc`, `sub_group_desc` (varchar on `dim_us.dim_pub_sales_territory`) | display labels: `terr_name`, `group_desc`, `sub_group_desc`
- territory label aliases: `territory`, `sales territory`, `terr` → resolve via `dim_us.dim_pub_sales_territory`; on customer master also `sales_terr_name` (varchar on `dim_us.dim_pub_customer_info`); never compare alphanumeric tokens to `sales_terr` or `cust_terr` (integer)
- cust_terr alias rule: fact/serving column `cust_terr` joins `dim_us.dim_pub_sales_territory.sales_terr` (same integer key, different physical column name on facts)
- order join key: `order_no` (int) | searchable labels: — (numeric token only) | display labels: — | grain: order-line on `dw_us.dwd_disty_brpt_orders_pl_etl_mi`


## Reference Dimension Scope Policy

- reference_dimension_semantics: when the user **explicitly names a reference dimension cue** listed in Reference Dimension Lookup Index plus a value, scope is a **dimension filter** on `filter_label` — not vendor/customer/VPL entity anchoring.
- disambiguation_override: explicit dimension cues from the index **override** bare-token entity disambiguation (for example OEM brand → vendor) for the value token.
- progressive_load: read only the matched index row at scope planning; use `read_kb_file` on `table_ref` (and `serving_ref` when present) before evidence SQL — do not copy column catalogs into answers from memory.

## Reference Dimension Lookup Index

- cue_keywords: order_type, order type, order_type_descr, order type descr | join_key: order_type | filter_label: order_type_descr | dim_fqn: `dim_us.dim_pub_order_type` | table_ref: tables/dim_pub_order_type.md
- cue_keywords: cust_type, cust type, cust_type_descr, cust type descr | join_key: cust_type | filter_label: cust_type_descr | dim_fqn: `dim_us.dim_pub_sales_cust_type` | table_ref: tables/dim_pub_sales_cust_type.md | serving_ref: tables/dws_disty_brpt_cust_type_comb_mtd.md
- cue_keywords: division, division_desc, division desc | join_key: division | filter_label: division_desc | dim_fqn: `dim_us.dim_pub_sales_division` | table_ref: tables/dim_pub_sales_division.md | serving_ref: tables/dws_disty_brpt_division_comb_mtd.md

## Person and Organization Scope Policy

- Bare person-name tokens (for example `First Last`) are **ambiguous** across PM, sales hierarchy, buyer, and other org lookup families until Phase-1 identifier validation on the correct dimension table.
- Do **not** bind alphanumeric person names to integer keys (`pm_id`, `sales_rep_id`, `buyer_id`, …) before Phase-1 succeeds.
- Read `Person Organization Lookup Index` below, then `read_kb_file` the referenced table doc `### Identifier Search Profile` and `role_binding_columns` before choosing a role column.
- When one person name matches multiple role columns on the same hierarchy table, surface matches in evidence or ask which role level applies.
- Multiple person names in one question: resolve each token independently, then combine scopes per planner judgment.

## Person Organization Lookup Index

- lookup_family: sales_hierarchy_primary_role_by_terr_view | dim_fqn: `dim_us.dim_pub_sales_hierarchy_primary_role_by_terr_view` | primary_join_key: `sales_rep_id` | table_ref: tables/dim_pub_sales_hierarchy_primary_role_by_terr_view.md | probe_mode: multi_column

## Entity Filter Key Routing

- filter_key: `vendor_label` | entity: vendor | search_token: label
- filter_key: `customer_label` | entity: customer | search_token: label
- filter_key: `mcust_name` | entity: customer | search_token: label
- filter_key: `cust_no` | entity: customer | search_token: integer_key
- filter_key: `mcust_no` | entity: customer | search_token: integer_key
- filter_key: `vend_no` | entity: vendor | search_token: integer_key
- filter_key: `vpc_group_label` | entity: vpl | search_token: label
- filter_key: `vpl_label` | entity: vpl | search_token: label
- filter_key: `vpl_code` | entity: vpl | search_token: label
- filter_key: `vpl_no` | entity: vpl | search_token: integer_key
- filter_key: `part_identifier` | entity: product | search_token: label
- filter_key: `pm_id` | entity: pm | search_token: integer_key
- filter_key: `territory_label` | entity: territory | search_token: label
- filter_key: `sales_terr` | entity: territory | search_token: integer_key
- filter_key: `order_no` | entity: order | search_token: integer_key

## Entity Resolution Assembly

- pattern_id: dim_scope_latest_period
- scope_cte_suffix: scope
- latest_period_month_trunc: DATE_TRUNC('MONTH', MAX(date_flag))
- scope_time_predicate: t.date_flag >= lp.month_start
- phase1_probe_limit: 20
- scope_cte_limit: 200
- margin_pct_expression: ROUND(SUM(t.ngm_amt) / NULLIFZERO(SUM(t.net_sales)) * 100, 2) AS margin_pct
- period_label_expression: TO_CHAR(MAX(t.date_flag), 'YYYY-MM') AS period_label
- label_prefix_strip: vpl: vpc
- metric_select: net_sales | expression: SUM(t.net_sales) AS revenue
- metric_select: ngm_amt | expression: SUM(t.ngm_amt) AS margin_amt
- pattern_id: dim_scope_calendar_month_ends
- month_ends_cte: month_ends
- month_end_join: t.date_flag = m.date_flag
- period_start_param: {{period_start}}
- data_through_param: {{data_through}}
- month_ends_source_fqn: dim_us.dim_pub_date
- scope_time_predicate: t.date_flag >= {{period_start}} AND t.date_flag <= {{data_through}}
- period_label_expression: TO_CHAR(t.date_flag, 'YYYY-MM') AS period_label
- pattern_id: phase1_ranking_policy
- ranking_keys: exact_label_match, master_roll_up, volume_tie_break
- forbid_arbitrary_limit_one: yes

## Time Scope Ontology

- scope_kind: calendar_year | user_cue: YYYY年, year YYYY, calendar year YYYY | preferred_filter_field: date_flag | completion_semantics: partial_through_data_available | default_when_ambiguous: natural calendar year via date_flag range, not fiscal year unless user says FY/fiscal
- scope_kind: fiscal_year | user_cue: FY2026, fiscal year, 财年 | preferred_filter_field: fyear via dim_us.dim_pub_date join | completion_semantics: partial_through_data_available
- scope_kind: calendar_month | user_cue: January 2026, 2026年1月, Jan 2026 | preferred_filter_field: date_flag month-end snapshot
- scope_kind: relative | user_cue: last month, 上个月, recent N months | preferred_filter_field: date_flag from runtime anchor (`data_freshness_through` or MAX(date_flag) subquery) | sql_pattern: prefer table L3 `time_filter_pattern`; on `*_comb_mtd` use `lm_*` physical columns with month-end `date_flag` snapshot, not `SUM(net_sales)` over a calendar range
- scope_kind: as_of | user_cue: as of date, 截至 | preferred_filter_field: date_flag <= anchor
- data_through rule: for trend/sequence intents without full_period_required, upper bound = MIN(period_end, table/domain MAX(date_flag)); in-progress periods are valid; zero rows must not default to period-not-ended

## Forbidden Column Aliases

- wrong: `vpl_id` | canonical: `vpl_no` | entity: vpl
- wrong: `vpl_name` | canonical: `vpl_code` | entity: vpl
- wrong: `vpc_id` | canonical: `vpc_group_id` | entity: vpl
- wrong: `master_cust_name` | canonical: `mcust_name` | entity: customer
- wrong: `master_cust_no` | canonical: `mcust_no` | entity: customer
- wrong: `fiscal_year` | canonical: `fyear` | entity: calendar
- wrong: `fiscal_period` | canonical: `month` | entity: calendar
- wrong: `territory_id` | canonical: `sales_terr` | entity: territory
- wrong: `terr_id` | canonical: `sales_terr` | entity: territory
- wrong: `territory_name` | canonical: `terr_name` | entity: territory
- wrong: `sales_territory_name` | canonical: `sales_terr_name` | entity: territory

## Retrieval Table Boosts

- filter_key: `pm_id` | filename_patterns: pm_mtd, _pm_ | filename_regex: brpt_pm_(mtd|wtd|1d) | exclude_filename_contains: comb
- filter_key: `pmid` | filename_patterns: pm_mtd, _pm_ | filename_regex: brpt_pm_(mtd|wtd|1d) | exclude_filename_contains: comb
- filter_key: `vend_no` | filename_patterns: vend
- filter_key: `vendor_id` | filename_patterns: vend
- filter_key: `vendor_label` | filename_patterns: vend, dim_pub_vendor
- filter_key: `vend_name` | filename_patterns: vend, dim_pub_vendor
- filter_key: `master_vend_name` | filename_patterns: vend, dim_pub_vendor
- filter_key: `cust_no` | filename_patterns: cust, dim_pub_customer
- filter_key: `customer_id` | filename_patterns: cust
- filter_key: `mcust_no` | filename_patterns: cust, dim_pub_customer
- filter_key: `mcust_name` | filename_patterns: cust, dim_pub_customer
- filter_key: `master_customer` | filename_patterns: brpt_cust | exclude_filename_contains: cust_type | boost_score: 60
- filter_key: `mcust` | filename_patterns: brpt_cust | exclude_filename_contains: cust_type | boost_score: 60
- filter_key: `order_no` | filename_patterns: orders_pl, orders_pl_etl
- filter_key: `part_identifier` | filename_patterns: part, dim_pub_part_info
- filter_key: `part_no` | filename_patterns: part, dim_pub_part_info
- filter_key: `mfg_partno` | filename_patterns: part, dim_pub_part_info
- filter_key: `product_identifier` | filename_patterns: part, dim_pub_part_info
- filter_key: `sku_label` | filename_patterns: part, dim_pub_part_info
- filter_key: `vpl_no` | filename_patterns: vpl, dim_pub_vpl
- filter_key: `vpl_code` | filename_patterns: vpl, dim_pub_vpl
- filter_key: `vpc_group_label` | filename_patterns: vpl, dim_pub_vpl
- filter_key: `vpl_label` | filename_patterns: vpl, dim_pub_vpl
- filter_key: `territory_label` | filename_patterns: sales_territory, dim_pub_sales_territory, brpt_cust, pl_extend
- filter_key: `sales_terr` | filename_patterns: sales_territory, dim_pub_sales_territory, brpt_cust
- filter_key: `terr_name` | filename_patterns: sales_territory, dim_pub_sales_territory, brpt_cust, pl_extend

## Entity NL Extraction Patterns

- pattern: `\b(?:for|of)\s+((?:VPC|VPL|vpc|vpl)(?:\s+[A-Za-z0-9][A-Za-z0-9_./&\s-]*)?)\b` | filter_key: vpc_group_label | value_group: 1 | flags: ignorecase
- pattern: `\b(?:vpc\s+group)\s+([A-Za-z0-9][A-Za-z0-9_./&\s-]+)` | filter_key: vpc_group_label | value_group: 1 | flags: ignorecase
- pattern: `\b(?:vpl\s+code|product\s+line)\s+([A-Za-z0-9][A-Za-z0-9_./&\s-]+)` | filter_key: vpl_code | value_group: 1 | flags: ignorecase
- pattern: `\b(VPC\s+[A-Za-z][A-Za-z0-9_./&\s-]*Scanner[s]?)\b` | filter_key: vpc_group_label | value_group: 1 | flags: ignorecase
- pattern: `\b(?:for|of)\s+([A-Za-z][A-Za-z0-9_./&\s-]+?)(?:\s*[?.!]|$)` | filter_key: vpc_group_label | value_group: 1 | flags: ignorecase | when_value_contains: scanner,vpc,vpl | when_value_excludes_year: true
- pattern: `\b(?:part|sku|product|item|mfg_part|mfr_part|manufacturer\s+part)\s*#?\s*([A-Za-z][A-Za-z0-9][A-Za-z0-9_./-]*)\b` | filter_key: part_identifier | value_group: 1 | flags: ignorecase
- pattern: `\bvpl\s*#\s*(\d+)\b` | filter_key: vpl_no | value_group: 1 | flags: ignorecase
- pattern: `\bvpl\s+code\s+([A-Za-z0-9][A-Za-z0-9_./-]*)\b` | filter_key: vpl_code | value_group: 1 | flags: ignorecase
- pattern: `\border\s*#\s*(\d+)\b` | filter_key: order_no | value_group: 1 | flags: ignorecase
- pattern: `\border\s+no\.?\s*#?\s*(\d+)\b` | filter_key: order_no | value_group: 1 | flags: ignorecase
- pattern: `\b(?:cust|customer)\s*#\s*(\d+)\b` | filter_key: cust_no | value_group: 1 | flags: ignorecase
- pattern: `\b(?:vend|vendor)\s*#\s*(\d+)\b` | filter_key: vend_no | value_group: 1 | flags: ignorecase
- pattern: `\b(?:sales\s+terr|sales_terr|terr)\s*#?\s*(\d+)\b` | filter_key: sales_terr | value_group: 1 | flags: ignorecase
- pattern: `\b(?:territory|sales\s+territory|terr)\s+([A-Za-z][A-Za-z0-9_./&\s-]+?)(?:\s*[?.!]|$)` | filter_key: territory_label | value_group: 1 | flags: ignorecase | when_value_excludes_year: true
- pattern: `\b(?:master\s+customer|mcust)\s+([A-Za-z][A-Za-z0-9_./&\s-]+?)(?:\s*[?.!]|$)` | filter_key: mcust_name | value_group: 1 | flags: ignorecase

## Entity Filter Column Mapping

Maps `entity_filters` keys to physical columns when they differ on specific tables.

- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | filter_key: `pm_id` | column: `dim_pm_id`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | filter_key: `pmid` | column: `dim_pm_id`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | filter_key: `vend_no` | column: `dim_vend_no`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | filter_key: `sales_terr` | column: `cust_terr`
- table_fqn: `dw_us.dws_disty_brpt_cust_mtd` | filter_key: `sales_terr` | column: `cust_terr`
- table_fqn: `dw_us.dws_disty_brpt_pl_extend_mtd` | filter_key: `sales_terr` | column: `cust_terr`

## Computed Metric SQL Expansions

Logical metrics absent as physical columns on specific tables; used by sql_repair metric expansion.

- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | metric: `net_sales` | expression: `nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0))`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | metric: `gross_sales` | expression: `nvl(ship_qty,0) * nvl(u_price,0)`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | metric: `gm_amt` | expression: `(nvl(u_price,0) - nvl(CASE WHEN sales_cost IS NULL THEN u_cost ELSE sales_cost END, 0)) * nvl(ship_qty,0)`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi` | metric: `tgm_amt` | expression: `((nvl(u_price,0) - nvl(CASE WHEN sales_cost IS NULL THEN u_cost ELSE sales_cost END, 0)) * nvl(ship_qty,0) + nvl(btl,0) + nvl(trans_btl,0) + nvl(one_time_btl,0) + nvl(hbtl,0) + nvl(scm_profit_adj,0) + nvl(btl_backout,0) + nvl(pdt,0))`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_di` | metric: `net_sales` | expression: `nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0))`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_di` | metric: `gross_sales` | expression: `nvl(ship_qty,0) * nvl(u_price,0)`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_di` | metric: `gm_amt` | expression: `(nvl(u_price,0) - nvl(CASE WHEN sales_cost IS NULL THEN u_cost ELSE sales_cost END, 0)) * nvl(ship_qty,0)`
- table_fqn: `dw_us.dwd_disty_brpt_orders_pl_di` | metric: `tgm_amt` | expression: `((nvl(u_price,0) - nvl(CASE WHEN sales_cost IS NULL THEN u_cost ELSE sales_cost END, 0)) * nvl(ship_qty,0) + nvl(btl,0) + nvl(trans_btl,0) + nvl(one_time_btl,0) + nvl(hbtl,0) + nvl(scm_profit_adj,0) + nvl(btl_backout,0) + nvl(pdt,0))`

## Order-Line vs Aggregate Routing

- **Scalar KPI** (`metric_lookup`): one number for a metric + time + optional entity filter → DWS/DM month-end snapshot or `metric_lookup` tool; use `SUM(metric)` without dimensional `GROUP BY` for the final answer.
- **Ranking / top-N / order listing** (`ranking`): row-level detail at order-line grain → `dw_us.dwd_disty_brpt_orders_pl_etl_mi` with `date_flag` equality, optional `ngm_amt < 0`, `ORDER BY` + `LIMIT`.
- Questions mentioning orders, list, top N, or negative margin are **not** scalar `metric_lookup` even when a metric name (for example NGM) appears.

## Cross-table Routing Rules

- Prefer DWS/DM serving tables for dashboard and metric retrieval when dimensions and grain match.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for recalculation, reconciliation, and edge-case investigations.
- Do not merge metrics across inconsistent grains in one step; aggregate from a common grain first.
- PM-scoped questions: prefer `dm_us.dm_disty_brpt_pm_mtd` or `dm_us.dm_disty_brpt_pm_comb_mtd` per `metric-index.md` selection rules.
- Part/product-scoped questions (user provides part number, SKU label, or manufacturer part): prefer `dw_us.dws_disty_brpt_part_mtd` (or sibling `*_part_*` slice); resolve alphanumeric identifiers on `part_no` / `mfg_partno` via `dim_us.dim_pub_part_info` when not denormalized on serving table; see golden `part-enn-525-revenue-margin`.
- VPL/VPC-scoped questions (user provides vpl code, product line label, vpc group, or multi-word category like "VPC Scanners"): prefer `dw_us.dws_disty_brpt_vpl_mtd` (or sibling `*_vpl_*` slice); Phase-1 resolve labels on `dim_us.dim_pub_vpl_info` (`vpl_code`, `vpl_desc`, `vpc_group_desc`) then join facts on `vpl_no`; when `vpc_group_desc` is denormalized on serving table, filter serving directly after Phase-1 validation; use `latest_period` when time not specified; never join `dim_pub_vpl_hierarchy_info` for VPL label lookup.
- Territory-scoped questions (user provides territory name, terr group/sub-group, or `sales_terr`/`terr#` integer): prefer `dw_us.dws_disty_brpt_cust_mtd` when customer+territory grain matches; `terr_name` often denormalized on serving; Phase-1 on `dim_us.dim_pub_sales_territory` (`terr_name`, `group_desc`, `sub_group_desc`) then filter/join on `cust_terr` = `sales_terr`; extended dimension cuts → `dw_us.dws_disty_brpt_pl_extend_mtd`; primary rep/mgr hierarchy on territory → `dim_pub_sales_hierarchy_primary_role_by_terr_view` (see `tables/dim_pub_sales_territory.md`).
- Order-scoped questions (`order_no`, order#, negative NGM on one order): route to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` at order-line grain per **Order-Line vs Aggregate Routing**; not scalar `metric_lookup`.

## Shared Metric Semantics

- Core profitability set: `net_sales`, `gross_sales`, `gm_amt`, `tgm_amt`, `ngm_amt`, `oplgm_amt`, `oplgm_plus_amt`, `total_btl`.
- Canonical formulas and verification status: `metric-index.md`.
- OPL and OPL+ use dedicated `*_for_opl` field variants in detailed computation chains.

## Shared Dimensions

- Customer: `cust_no`, `mcust_no`, `cust_terr`, `cust_type`, `division`
- Territory: `sales_terr` (dim key; facts use `cust_terr`), `terr_name`, `group_desc`, `sub_group_desc`, `terr_sub_group`, `terr_group`
- Product/Vendor: `sku_no`, `vpl_no`, `vend_no`, `seg_code`
- Organization: PM/Buyer/Sales/BD hierarchy IDs (`pm_id`, `buyer_id`, `sales_rep`, BD project/task keys)

## Schema Routing

- schema_prefixes: dw_us, dm_us, dim_us
- always_allowed_tables: dim_us.dim_pub_date, v_catalog.columns
- stem_prefix: dim_ -> dim_us
- stem_prefix: dm_ -> dm_us
- stem_prefix: dws_ -> dw_us
- stem_prefix: dwd_ -> dw_us
- dm_layer_rewrite: true

## SQL Artifact Validation Policy

- strict_artifact_table: dws_disty_brpt_cust_mtd.md
- strict_artifact_table: dws_disty_brpt_vend_mtd.md
- strict_artifact_table: dm_disty_brpt_pm_mtd.md
- strict_artifact_table: dwd_disty_brpt_orders_pl_etl_mi.md
- strict_artifact_table: dim_pub_date.md
- strict_artifact_table: dim_pub_sales_territory.md

## Stewardship

- Per-table owner teams are not registered in the metadata catalog; route governance questions through the B Report platform team.
