# Domain Knowledge Contract Header

- contract_version: v2.0.0
- artifact_type: domain-knowledge
- artifact_id: POS
- domain: POS

# Domain Knowledge — POS

## Domain Scope

- **Domain name:** POS
- **Business scope:** Shipped Point-of-Sale (POS) order reporting — vendor/customer sales exports, SPA/SCM claim detail, serial/RMA tracing, credit protection, and related Vertica RDS custom reports.
- **Geographic scope:** US-primary (`dw_us`, `dm_us`, `dim_us`). Multi-region usage exists (US 367, CA 124, MX 7, BR 1 RDS scripts); regional schema names mirror US with `_ca`, `_mx`, `_br` suffix patterns.
- **Driving table:** `dw_us.dwd_disty_common_pos_di` — all POS reports LEFT JOIN from this hub at order-line grain.

## Grain Standards

| Grain | Keys | Usage |
|-------|------|-------|
| POS order header | `order_no`, `order_type` | Header-level attributes only |
| POS order line | `order_no`, `order_type`, `order_line_no` | Default report grain |
| Time filter | `date_flag` | Primary business date for period filters |

## Cross-Table Routing Rules

1. **Start at hub:** Always anchor POS queries on `dw_us.dwd_disty_common_pos_di`.
2. **LEFT JOIN enrichment:** Preserve POS rows; enrichment tables join LEFT.
3. **One-to-many partners:** SPA/SCM detail, serial numbers, EU custom fields, freight detail — pre-aggregate (ROW_NUMBER, pivot, LISTAGG) before final output when grain must stay order-line.
4. **DWD/DIM first:** Use curated warehouse tables before ODS unless required field is unavailable.
5. **Metric routing:** Use `metric-index.md` for formula authority; do not recalculate hub metrics from enrichment tables unless report explicitly requires SPA/SCM expense inclusion.

## Shared POS Business Rules (16 rules)

1. **Component lines:** Default `order_line_type <> 'Comp'`. Include Comp only for kit/component/bundle detail reports.
2. **Credit orders:** `order_type = 114` is credit/price-protection — exclude from standard sales revenue unless adjustment report requested.
3. **RMA tracing:** Use `int_ref_type` (1 = original SO, 9 = RMA) and `int_ref_no` before relying on `order_no` alone.
4. **SPA/SCM multiplication:** Never direct-join one-to-many SPA tables without pre-aggregation at order-line grain.
5. **Net sales with expense:** Recalculate `(unit_price + COALESCE(unit_sum_exp,0)) * ship_qty` only when report requires expense-inclusive pricing; otherwise use `extend_net_price`.
6. **Serial/tracking:** Aggregate serial/tracking values (LISTAGG) at order-line grain; use serial-level grain only when report requires one row per serial.
7. **End-user fields:** Prefer hub EU columns; join `dwd_disty_sales_eu_custom_di` only when mapped attributes missing on hub.
8. **Drop ship:** Derive from `from_loc_no = 98` when `drop_ship` flag absent; enrich from history header when needed.
9. **Freight/FDS:** Hub may not carry all freight components — join history expense or freight detail tables when requested.
10. **Currency:** Keep source currency from hub (`vend_currency`); do not convert without explicit exchange-rate logic.
11. **VPC/VPG/ASC606:** Use latest-row selection (ROW_NUMBER by sku, entry_datetime DESC) for product grouping attributes.
12. **Sales hierarchy:** Hub captures shipped transaction territory; use hierarchy dimension for current role enrichment — filter to avoid row multiplication.
13. **AR/credit reports:** Join AR/doc tables by cust/invoice/doc keys; keep sales metrics separate from AR balance metrics.
14. **Inventory context:** Join inventory/RIO/run-rate only when report asks on-hand/aging/RIO metrics; join on `sku_no` + warehouse.
15. **ODS fallback:** Use ODS only when DWD/DIM gap exists — see ODS deferred inventory below.
16. **UNION branches:** Confirm compatible grain and columns before UNION ALL across serial/non-serial or current/historical sources.

## Join Policy Summary

- POS hub → header extend: `order_no`, `order_type`
- POS hub → line detail: `order_no`, `order_type`, `order_line_no`
- POS hub → dimensions: `cust_no`, `sku_no`, `vend_no`, `vpl_no`, `sales_terr`, `order_type`, etc.
- Employee IDs (`entry_id`, `sales_rep_id`, `buyer_id`, …): join `dim_us.dim_pub_manager` on `userid`

## Shared Tables with Other Domains

Several DIM and DWD table names overlap with B Report and other disty domains (e.g. `dim_pub_customer_info`, `dwd_disty_brpt_orders_pl_etl_mi`). POS documentation captures **POS-specific join keys and report use cases** only. Shared column semantics follow platform dimension definitions.

## ODS Deferred Inventory (46 tables)

Full L1–L6 documentation deferred to a future ODS enrich pass. Tables are used as gap-fill sources when DWD/DIM lack required fields:

`ods_cis_corp_asset_tag`, `ods_cis_corp_carton_header`, `ods_cis_corp_cpo_profile`, `ods_cis_corp_cust_change_log`, `ods_cis_corp_eu_custom_map`, `ods_cis_corp_history_detail`, `ods_cis_corp_history_eu_custom`, `ods_cis_corp_history_exp`, `ods_cis_corp_history_header`, `ods_cis_corp_history_profile`, `ods_cis_corp_history_serial_nbr`, `ods_cis_corp_inv_qty`, `ods_cis_corp_list_box_detail`, `ods_cis_corp_mc_order_ref`, `ods_cis_corp_order_detail`, `ods_cis_corp_order_detail_date`, `ods_cis_corp_order_eu_custom`, `ods_cis_corp_order_header`, `ods_cis_corp_part_prod_detail`, `ods_cis_corp_proj_usage_budget`, `ods_cis_corp_rma_details`, `ods_cis_corp_scm_auto_claim_log`, `ods_cis_corp_serial_nbr`, `ods_cis_corp_spa_detail`, `ods_cis_corp_spa_header`, `ods_cis_corp_vend_user_matrix`, `ods_dw_prod_dws_dw_param_xref`, `ods_cis_corp_cpo_comments`, `ods_cis_corp_cpo_eu_custom`, `ods_cis_corp_cpo_header`, `ods_cis_corp_cust_doc`, `ods_cis_corp_cust_part_no`, `ods_cis_corp_customer_header`, `ods_cis_corp_history_carton_header`, `ods_cis_corp_history_comments`, `ods_cis_corp_history_cpo_comments`, `ods_cis_corp_history_cpo_eu_custom`, `ods_cis_corp_history_cpo_profile`, `ods_cis_corp_no_ctrl`, `ods_cis_corp_order_comments`, `ods_cis_corp_order_eu_common`, `ods_cis_corp_order_exp`, `ods_cis_corp_order_profile`, `ods_cis_corp_part_master`, `ods_cis_corp_pm_claim`, `ods_cis_corp_pm_claim_type`, `ods_cis_corp_prod_code_detail`, `ods_cis_corp_service_contract_profile`, `ods_cis_corp_tc_attribute_en`, `ods_cis_corp_tc_part_technotes_en`, `ods_cis_corp_tc_value_en`, `ods_cis_corp_vend_doc`, `ods_cis_corp_vend_master`, `ods_cis_corp_vend_master_etc`, `ods_dw_prod_dws_edi214`

**Common ODS join patterns:**
- Order header/detail: `order_no`, `order_type` [, `order_line_no`]
- CPO: `cpo_no`
- SPA: `spa_no`, `scm_no`
- RMA: `rma_no` linked via hub `int_ref_type = 9`
- Config/param: `code_type`/`code_value` or param name/value

## Completion Gate (locked 2026-06-23)

| Item | Status |
|------|--------|
| DWD/DM/DIM table files | **81/81** complete (L1–L6, v2.0.0) |
| ODS full docs | **0/46** deferred (inventory listed above — accepted) |
| Contract version | v2.0.0 on all 84 markdown artifacts |
| Validation | `scripts/validate_v2.py` PASS |
| Metric-index sync | 9 core POS metrics registered |

**Open questions (domain-level):**
- Exact Azkaban job name and SLA for `dwd_disty_common_pos_di` daily load — confirm via BAF schedule lookup.
- CA/MX/BR schema-level column drift vs US — spot-check if multi-region POS reports fail.
