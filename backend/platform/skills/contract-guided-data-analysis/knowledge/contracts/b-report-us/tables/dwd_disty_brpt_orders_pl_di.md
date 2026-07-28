# dw_us.dwd_disty_brpt_orders_pl_di

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dw_us.dwd_disty_brpt_orders_pl_di
- domain: b-report-us
- one_line_purpose: US B Report shipped-order profitability and performance analytics

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dw_us.dwd_disty_brpt_orders_pl_di`
- Layer: DWD
- Canonical/Derived: Canonical fact base
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dw_us.dwd_disty_brpt_orders_pl_di`

### Grain, Scope, Exclusions

- Grain: order line
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive (`dw_us`/`dm_us`/`dim_us`): table family present; prefer canonical name without suffix variants.
- Vertica: same schema families mirrored; Vertica may lag Hive by several days on detail facts.
- Reconciliation: compare `MIN(date_flag)`, `MAX(date_flag)`, row counts when auditing cross-engine parity.

### Column Catalog (100% columns)

- documented_column_count: 134
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| virtual_type | int | engine metadata not exposed | — | 1 | data virtual type: 0-normal order data, 1-virtual line data | dimension | data virtual type: 0-normal order data, 1-virtual line data | integer | domain_value_check_recommended | data virtual type: 0-normal order data, 1-virtual line data; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| order_type | int | engine metadata not exposed | — | 2 | Order Type | dimension | Order Type | integer | domain_value_check_recommended | Order Type; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_order_type.order_type` |
| order_no | int | engine metadata not exposed | — | 3 | Order No. | key | Order No. | integer | not_null_expected|dim_fk_check_recommended | Order No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| order_line_no | int | engine metadata not exposed | — | 4 | Order Line No. | key | Order Line No. | integer | not_null_expected|dim_fk_check_recommended | Order Line No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| cust_no | int | engine metadata not exposed | — | 5 | Customer No. | key | Customer No. | integer | not_null_expected|dim_fk_check_recommended | Customer No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_customer_info.cust_no` |
| mcust_no | int | engine metadata not exposed | — | 6 | master customer No. | key | master customer No. | integer | not_null_expected|dim_fk_check_recommended | master customer No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| cust_terr | int | engine metadata not exposed | — | 7 | customer territory | dimension | customer territory | integer | domain_value_check_recommended | customer territory; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_type | int | engine metadata not exposed | — | 8 | cust type | dimension | cust type | integer | domain_value_check_recommended | cust type; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| sales_rep | int | engine metadata not exposed | — | 9 | Sales Representative | dimension | Sales Representative | integer | domain_value_check_recommended | Sales Representative; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_sales_hierarchy_by_terr_user_role.sales_rep_id` |
| from_loc_no | int | engine metadata not exposed | — | 10 | From Location Addr No. | key | From Location Addr No. | integer | not_null_expected|dim_fk_check_recommended | From Location Addr No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| terms | string | engine metadata not exposed | — | 11 | Customer Credit Level | dimension | Customer Credit Level | categorical_or_expression_text | domain_value_check_recommended | Customer Credit Level; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| gv_user_type | string | engine metadata not exposed | — | 12 | Government User Type | dimension | Government User Type | categorical_or_expression_text | domain_value_check_recommended | Government User Type; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| sku_no | int | engine metadata not exposed | — | 13 | SKU(Stock Keeping Unit) No. | key | SKU(Stock Keeping Unit) No. | integer | not_null_expected|dim_fk_check_recommended | SKU(Stock Keeping Unit) No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_part_info.sku_no` |
| prod_code | int | engine metadata not exposed | — | 14 | Product Code | dimension | Product Code | integer | domain_value_check_recommended | Product Code; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| vpl_no | int | engine metadata not exposed | — | 15 | vendor product line No. | key | vendor product line No. | integer | not_null_expected|dim_fk_check_recommended | vendor product line No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_vpl_info.vpl_no` |
| vend_no | int | engine metadata not exposed | — | 16 | Vendor No. | key | Vendor No. | integer | not_null_expected|dim_fk_check_recommended | Vendor No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_vendor_info.vend_no` |
| inv_type | int | engine metadata not exposed | — | 17 | Invoice Type | dimension | Invoice Type | integer | domain_value_check_recommended | Invoice Type; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| base_cost | decimal(19,4) | engine metadata not exposed | — | 18 | Base Cost | measure | Base Cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Base Cost; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| sales_cost | decimal(19,4) | engine metadata not exposed | — | 19 | Sales cost | measure | Sales cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Sales cost; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| ship_qty | int | engine metadata not exposed | — | 20 | Ship Quantity | measure | Ship Quantity | integer | non_negative_expected|outlier_check_recommended | Ship Quantity; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| u_price | decimal(19,4) | engine metadata not exposed | — | 21 | Unit Price | measure | Unit Price | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Unit Price; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| u_cost | decimal(19,4) | engine metadata not exposed | — | 22 | Unit Cost | measure | Unit Cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Unit Cost; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| u_sum_expense | decimal(19,4) | engine metadata not exposed | — | 23 | Unit Sum Expense | measure | Unit Sum Expense | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Unit Sum Expense; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| l_weight | decimal(19,4) | engine metadata not exposed | — | 24 | line weight | measure | line weight | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | line weight; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| sales_total | decimal(19,4) | engine metadata not exposed | — | 25 | sales total = (u_price + u_sum_expense) * ship_qty | measure | sales total = (u_price + u_sum_expense) * ship_qty | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | sales total = (u_price + u_sum_expense) * ship_qty; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| cust_program_id | int | engine metadata not exposed | — | 26 | The id of b report cust Program | key | The id of b report cust Program | integer | not_null_expected|dim_fk_check_recommended | The id of b report cust Program; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| ap_finance | decimal(19,4) | engine metadata not exposed | — | 27 | One of the PL items (AP finance expense) | measure | One of the PL items (AP finance expense) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (AP finance expense); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| inv_cost | decimal(19,4) | engine metadata not exposed | — | 28 | One of the PL items (Inventory aging expense) | measure | One of the PL items (Inventory aging expense) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (Inventory aging expense); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| inv_reserve | decimal(19,4) | engine metadata not exposed | — | 29 | One of the PL items (Inventory reserve value) | measure | One of the PL items (Inventory reserve value) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (Inventory reserve value); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cr_risk_cterm | decimal(19,4) | engine metadata not exposed | — | 30 | Credit Risk Cost Associated with a Certain Customer | measure | Credit Risk Cost Associated with a Certain Customer | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Credit Risk Cost Associated with a Certain Customer; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| flr_synnex | decimal(19,4) | engine metadata not exposed | — | 31 | Flooring Charges fee Paid by SYNNEX | measure | Flooring Charges fee Paid by SYNNEX | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Flooring Charges fee Paid by SYNNEX; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| direct_credit | decimal(19,4) | engine metadata not exposed | — | 32 | Credit card processing expense with specific pay terms | measure | Credit card processing expense with specific pay terms | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Credit card processing expense with specific pay terms; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| csgn_edi_fee | decimal(19,4) | engine metadata not exposed | — | 33 | Consignment Business EDI Fee charged by SYNNEX | measure | Consignment Business EDI Fee charged by SYNNEX | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Consignment Business EDI Fee charged by SYNNEX; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| corporate | decimal(19,4) | engine metadata not exposed | — | 34 | One of the PL items (Corporate overhead expense) | measure | One of the PL items (Corporate overhead expense) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (Corporate overhead expense); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| sfs | decimal(19,4) | engine metadata not exposed | — | 35 | One of the PL items (SFS) | measure | One of the PL items (SFS) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (SFS); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_risk | decimal(19,4) | engine metadata not exposed | — | 36 | One of the PL items (Risk accrual for incorrect SCM usage) | measure | One of the PL items (Risk accrual for incorrect SCM usage) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (Risk accrual for incorrect SCM usage); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| flr_vendor | decimal(19,4) | engine metadata not exposed | — | 37 | FLR_VENDOR | measure | FLR_VENDOR | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | FLR_VENDOR; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_finance_sales | decimal(19,4) | engine metadata not exposed | — | 38 | CUST_FINANCE_SALES | measure | CUST_FINANCE_SALES | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | CUST_FINANCE_SALES; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_pmt_disc | decimal(19,4) | engine metadata not exposed | — | 39 | Early payment discounts offered to and taken by customers (based on discounted payment terms) | measure | Early payment discounts offered to and taken by customers (based on discounted payment terms) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Early payment discounts offered to and taken by customers (based on discounted payment terms); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cvr_rm | decimal(19,4) | engine metadata not exposed | — | 40 | Remainder sweep, it was combined into CUST_REBATE | measure | Remainder sweep, it was combined into CUST_REBATE | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Remainder sweep, it was combined into CUST_REBATE; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ar_fin_recovery | decimal(19,4) | engine metadata not exposed | — | 41 | Charge back to software products which cost is raised due to long term payment like one year | measure | Charge back to software products which cost is raised due to long term payment like one year | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Charge back to software products which cost is raised due to long term payment like one year; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| mfg_oh | decimal(19,4) | engine metadata not exposed | — | 42 | The expense in GL(cost for headcount(PERSONNEL) + OVERHEAD)  -  total cost on orders & inventory | measure | The expense in GL(cost for headcount(PERSONNEL) + OVERHEAD)  -  total cost on orders & inventory | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | The expense in GL(cost for headcount(PERSONNEL) + OVERHEAD)  -  total cost on orders & inventory; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_finance | decimal(19,4) | engine metadata not exposed | — | 43 | Cost to SYNNEX to Finance Receivables from Customers | measure | Cost to SYNNEX to Finance Receivables from Customers | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Cost to SYNNEX to Finance Receivables from Customers; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| rma | decimal(19,4) | engine metadata not exposed | — | 44 | RMA return cost, variable RMA Cost with 2% of RMA amount plus fixed RMA Cost with $5 each RMA | measure | RMA return cost, variable RMA Cost with 2% of RMA amount plus fixed RMA Cost with $5 each RMA | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | RMA return cost, variable RMA Cost with 2% of RMA amount plus fixed RMA Cost with $5 each RMA; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_sales | decimal(19,4) | engine metadata not exposed | — | 45 | Headcount expense from Sales Team | measure | Headcount expense from Sales Team | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Headcount expense from Sales Team; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| order_overhead | decimal(19,4) | engine metadata not exposed | — | 46 | China BPO team Support Invoiced to US/CA | measure | China BPO team Support Invoiced to US/CA | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | China BPO team Support Invoiced to US/CA; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| margin_share | decimal(19,4) | engine metadata not exposed | — | 47 | Iron Bow share profilt | measure | Iron Bow share profilt | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Iron Bow share profilt; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ap_adj | decimal(19,4) | engine metadata not exposed | — | 48 | the AP will as SYNNEX margin and apportioned to P&L by vendor | measure | the AP will as SYNNEX margin and apportioned to P&L by vendor | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | the AP will as SYNNEX margin and apportioned to P&L by vendor; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| pdt | decimal(19,4) | engine metadata not exposed | — | 49 | Early payment credits taken from vendors (based on discounted payment terms) | measure | Early payment credits taken from vendors (based on discounted payment terms) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Early payment credits taken from vendors (based on discounted payment terms); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_cost | decimal(19,4) | engine metadata not exposed | — | 50 | SCM aging expense,53bps of the SCM ($) not processed | measure | SCM aging expense,53bps of the SCM ($) not processed | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | SCM aging expense,53bps of the SCM ($) not processed; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| infrastructure | decimal(19,4) | engine metadata not exposed | — | 51 | Profit from Vendor used to offset SYNNEX internal headcount costs for channel development and so on | measure | Profit from Vendor used to offset SYNNEX internal headcount costs for channel development and so on | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Profit from Vendor used to offset SYNNEX internal headcount costs for channel development and so on; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| marketing | decimal(19,4) | engine metadata not exposed | — | 52 | Revenue from marketing activities (ex. Commercial Conference) sponsored by vendor as SYNNEX Margin | measure | Revenue from marketing activities (ex. Commercial Conference) sponsored by vendor as SYNNEX Margin | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Revenue from marketing activities (ex. Commercial Conference) sponsored by vendor as SYNNEX Margin; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| coop | decimal(19,4) | engine metadata not exposed | — | 53 | rebates from vendor for marketing eventsand headcount support | measure | rebates from vendor for marketing eventsand headcount support | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | rebates from vendor for marketing eventsand headcount support; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| one_time_btl | decimal(19,4) | engine metadata not exposed | — | 54 | One of the PL items (Behind-the-line rebates offered from vendors booked at the end of the month) | measure | One of the PL items (Behind-the-line rebates offered from vendors booked at the end of the month) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | One of the PL items (Behind-the-line rebates offered from vendors booked at the end of the month); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hbtl | decimal(19,4) | engine metadata not exposed | — | 55 | It is a special case of 1 time BTL, it is submitted by VCM when a SCM is closed | measure | It is a special case of 1 time BTL, it is submitted by VCM when a SCM is closed | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | It is a special case of 1 time BTL, it is submitted by VCM when a SCM is closed; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_profit_adj | decimal(19,4) | engine metadata not exposed | — | 56 | A special HBTL that PM cannot control,Profit of Operation related SCM which is closed 30days before | measure | A special HBTL that PM cannot control,Profit of Operation related SCM which is closed 30days before | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | A special HBTL that PM cannot control,Profit of Operation related SCM which is closed 30days before; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_pm | decimal(19,4) | engine metadata not exposed | — | 57 | Headcount expense from PM Team | measure | Headcount expense from PM Team | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Headcount expense from PM Team; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_bd | decimal(19,4) | engine metadata not exposed | — | 58 | Headcount expense from Marketing Team(BD Projects) | measure | Headcount expense from Marketing Team(BD Projects) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Headcount expense from Marketing Team(BD Projects); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl | decimal(19,4) | engine metadata not exposed | — | 59 | Behind-the-line rebates offered from vendors | measure | Behind-the-line rebates offered from vendors | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Behind-the-line rebates offered from vendors; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl_sales | decimal(19,4) | engine metadata not exposed | — | 60 | Behind-the-line rebates offered from vendors and credited to Sales OPL | measure | Behind-the-line rebates offered from vendors and credited to Sales OPL | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Behind-the-line rebates offered from vendors and credited to Sales OPL; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl_backout | decimal(19,4) | engine metadata not exposed | — | 61 | Exceptions to behind-the-line rebates offered and credited to Sales OPL | measure | Exceptions to behind-the-line rebates offered and credited to Sales OPL | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Exceptions to behind-the-line rebates offered and credited to Sales OPL; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_rebate | decimal(19,4) | engine metadata not exposed | — | 62 | Accrued customer rebate (for rebates not deducted from the invoice price, but rather paid out at a later date) | measure | Accrued customer rebate (for rebates not deducted from the invoice price, but rather paid out at a later date) | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Accrued customer rebate (for rebates not deducted from the invoice price, but rather paid out at a later date); order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| mof | decimal(19,4) | engine metadata not exposed | — | 63 | Minimum Order Fee charged to customers, based on the MOF fee policy set-up and maintained by Sales | measure | Minimum Order Fee charged to customers, based on the MOF fee policy set-up and maintained by Sales | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Minimum Order Fee charged to customers, based on the MOF fee policy set-up and maintained by Sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_out_load | decimal(19,4) | engine metadata not exposed | — | 64 | Credit to P&L to offset any "Freight Out" loads built into the "system cost" of the product. | measure | Credit to P&L to offset any "Freight Out" loads built into the "system cost" of the product. | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Credit to P&L to offset any "Freight Out" loads built into the "system cost" of the product.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_out_exp | decimal(19,4) | engine metadata not exposed | — | 65 | Amount of freight expense pre-paid and discounted from the customer invoice | measure | Amount of freight expense pre-paid and discounted from the customer invoice | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Amount of freight expense pre-paid and discounted from the customer invoice; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| whoh_pack | decimal(19,4) | engine metadata not exposed | — | 66 | The warehouse expense associated with the handling and processing of an order | measure | The warehouse expense associated with the handling and processing of an order | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | The warehouse expense associated with the handling and processing of an order; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_ob_recovery | decimal(19,4) | engine metadata not exposed | — | 67 | Recovery FRT Out Expense for Apptis ( The amount SYNNEX saves due to customer bear the freight charge) , it was combined in FRT_OUT_EXP | measure | Recovery FRT Out Expense for Apptis ( The amount SYNNEX saves due to customer bear the freight charge) , it was combined in FRT_OUT_EXP | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Recovery FRT Out Expense for Apptis ( The amount SYNNEX saves due to customer bear the freight charge) , it was combined in FRT_OUT_EXP; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_ib_recovery | decimal(19,4) | engine metadata not exposed | — | 68 | Credit to P&L to offset any "In Bound Freight Loads" built into the "system cost" of the product for vendor drop ship orders that vendors shipp products to our customer directly | measure | Credit to P&L to offset any "In Bound Freight Loads" built into the "system cost" of the product for vendor drop ship orders that vendors shipp products to our customer directly | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Credit to P&L to offset any "In Bound Freight Loads" built into the "system cost" of the product for vendor drop ship orders that vendors shipp products to our customer directly; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| others | decimal(19,4) | engine metadata not exposed | — | 69 | SGW/CAST expense | measure | SGW/CAST expense | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | SGW/CAST expense; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| others_sales | decimal(19,4) | engine metadata not exposed | — | 70 | CAST expense | measure | CAST expense | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | CAST expense; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_disc | decimal(19,4) | engine metadata not exposed | — | 71 | SCM_DISC | measure | SCM_DISC | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | SCM_DISC; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_ndisc | decimal(19,4) | engine metadata not exposed | — | 72 | SCM_NDISC | measure | SCM_NDISC | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | SCM_NDISC; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_in | decimal(19,4) | engine metadata not exposed | — | 73 | FRT_IN | measure | FRT_IN | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | FRT_IN; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| trans_btl | decimal(19,4) | engine metadata not exposed | — | 74 | TRANS_BTL | measure | TRANS_BTL | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | TRANS_BTL; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| trans_btl_sales | decimal(19,4) | engine metadata not exposed | — | 75 | TRANS_BTL_SALES | measure | TRANS_BTL_SALES | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | TRANS_BTL_SALES; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ngm_amt | decimal(19,4) | engine metadata not exposed | — | 76 | Net Gross Margin, the final P&L to evaluate SYNNEX profit ability | measure | Net Gross Margin, the final P&L to evaluate SYNNEX profit ability | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | Net Gross Margin, the final P&L to evaluate SYNNEX profit ability; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| oplgm_amt | decimal(19,4) | engine metadata not exposed | — | 77 | OPLGM, used for sales commission, it is GM plus the direct cost/expense about this SO | measure | OPLGM, used for sales commission, it is GM plus the direct cost/expense about this SO | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | OPLGM, used for sales commission, it is GM plus the direct cost/expense about this SO; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| ap_finance_calcproc | string | engine metadata not exposed | — | 78 | calculation process of item ap_finance | technical | calculation process of item ap_finance | categorical_or_expression_text | expression_parseable_check | calculation process of item ap_finance; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| inv_cost_calcproc | string | engine metadata not exposed | — | 79 | calculation process of item inv_cost | technical | calculation process of item inv_cost | categorical_or_expression_text | expression_parseable_check | calculation process of item inv_cost; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| inv_reserve_calcproc | string | engine metadata not exposed | — | 80 | calculation process of item inv_reserve | technical | calculation process of item inv_reserve | categorical_or_expression_text | expression_parseable_check | calculation process of item inv_reserve; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cr_risk_cterm_calcproc | string | engine metadata not exposed | — | 81 | calculation process of item cr_risk_cterm | technical | calculation process of item cr_risk_cterm | categorical_or_expression_text | expression_parseable_check | calculation process of item cr_risk_cterm; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| flr_synnex_calcproc | string | engine metadata not exposed | — | 82 | calculation process of item flr_synnex | technical | calculation process of item flr_synnex | categorical_or_expression_text | expression_parseable_check | calculation process of item flr_synnex; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| direct_credit_calcproc | string | engine metadata not exposed | — | 83 | calculation process of item direct_credit | technical | calculation process of item direct_credit | categorical_or_expression_text | expression_parseable_check | calculation process of item direct_credit; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| csgn_edi_fee_calcproc | string | engine metadata not exposed | — | 84 | calculation process of item csgn_edi_fee | technical | calculation process of item csgn_edi_fee | categorical_or_expression_text | expression_parseable_check | calculation process of item csgn_edi_fee; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| corporate_calcproc | string | engine metadata not exposed | — | 85 | calculation process of item corporate | technical | calculation process of item corporate | categorical_or_expression_text | expression_parseable_check | calculation process of item corporate; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| sfs_calcproc | string | engine metadata not exposed | — | 86 | calculation process of item sfs | technical | calculation process of item sfs | categorical_or_expression_text | expression_parseable_check | calculation process of item sfs; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_risk_calcproc | string | engine metadata not exposed | — | 87 | calculation process of item scm_risk | technical | calculation process of item scm_risk | categorical_or_expression_text | expression_parseable_check | calculation process of item scm_risk; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| flr_vendor_calcproc | string | engine metadata not exposed | — | 88 | calculation process of item flr_vendor | technical | calculation process of item flr_vendor | categorical_or_expression_text | expression_parseable_check | calculation process of item flr_vendor; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_finance_sales_calcproc | string | engine metadata not exposed | — | 89 | calculation process of item cust_finance_sales | technical | calculation process of item cust_finance_sales | categorical_or_expression_text | expression_parseable_check | calculation process of item cust_finance_sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_pmt_disc_calcproc | string | engine metadata not exposed | — | 90 | calculation process of item cust_pmt_disc | technical | calculation process of item cust_pmt_disc | categorical_or_expression_text | expression_parseable_check | calculation process of item cust_pmt_disc; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cvr_rm_calcproc | string | engine metadata not exposed | — | 91 | calculation process of item cvr_rm | technical | calculation process of item cvr_rm | categorical_or_expression_text | expression_parseable_check | calculation process of item cvr_rm; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ar_fin_recovery_calcproc | string | engine metadata not exposed | — | 92 | calculation process of item ar_fin_recovery | technical | calculation process of item ar_fin_recovery | categorical_or_expression_text | expression_parseable_check | calculation process of item ar_fin_recovery; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| mfg_oh_calcproc | string | engine metadata not exposed | — | 93 | calculation process of item mfg_oh | technical | calculation process of item mfg_oh | categorical_or_expression_text | expression_parseable_check | calculation process of item mfg_oh; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_finance_calcproc | string | engine metadata not exposed | — | 94 | calculation process of item cust_finance | technical | calculation process of item cust_finance | categorical_or_expression_text | expression_parseable_check | calculation process of item cust_finance; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| rma_calcproc | string | engine metadata not exposed | — | 95 | calculation process of item rma | technical | calculation process of item rma | categorical_or_expression_text | expression_parseable_check | calculation process of item rma; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_sales_calcproc | string | engine metadata not exposed | — | 96 | calculation process of item hc_sales | technical | calculation process of item hc_sales | categorical_or_expression_text | expression_parseable_check | calculation process of item hc_sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| order_overhead_calcproc | string | engine metadata not exposed | — | 97 | calculation process of item order_overhead | technical | calculation process of item order_overhead | categorical_or_expression_text | expression_parseable_check | calculation process of item order_overhead; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| margin_share_calcproc | string | engine metadata not exposed | — | 98 | calculation process of item margin_share | technical | calculation process of item margin_share | categorical_or_expression_text | expression_parseable_check | calculation process of item margin_share; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ap_adj_calcproc | string | engine metadata not exposed | — | 99 | calculation process of item ap_adj | technical | calculation process of item ap_adj | categorical_or_expression_text | expression_parseable_check | calculation process of item ap_adj; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| pdt_calcproc | string | engine metadata not exposed | — | 100 | calculation process of item pdt | technical | calculation process of item pdt | categorical_or_expression_text | expression_parseable_check | calculation process of item pdt; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_cost_calcproc | string | engine metadata not exposed | — | 101 | calculation process of item scm_cost | technical | calculation process of item scm_cost | categorical_or_expression_text | expression_parseable_check | calculation process of item scm_cost; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| infrastructure_calcproc | string | engine metadata not exposed | — | 102 | calculation process of item infrastructure | technical | calculation process of item infrastructure | categorical_or_expression_text | expression_parseable_check | calculation process of item infrastructure; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| marketing_calcproc | string | engine metadata not exposed | — | 103 | calculation process of item marketing | technical | calculation process of item marketing | categorical_or_expression_text | expression_parseable_check | calculation process of item marketing; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| coop_calcproc | string | engine metadata not exposed | — | 104 | calculation process of item coop | technical | calculation process of item coop | categorical_or_expression_text | expression_parseable_check | calculation process of item coop; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| one_time_btl_calcproc | string | engine metadata not exposed | — | 105 | calculation process of item one_time_btl | technical | calculation process of item one_time_btl | categorical_or_expression_text | expression_parseable_check | calculation process of item one_time_btl; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hbtl_calcproc | string | engine metadata not exposed | — | 106 | calculation process of item hbtl | technical | calculation process of item hbtl | categorical_or_expression_text | expression_parseable_check | calculation process of item hbtl; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_profit_adj_calcproc | string | engine metadata not exposed | — | 107 | calculation process of item scm_profit_adj | technical | calculation process of item scm_profit_adj | categorical_or_expression_text | expression_parseable_check | calculation process of item scm_profit_adj; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_pm_calcproc | string | engine metadata not exposed | — | 108 | calculation process of item hc_pm | technical | calculation process of item hc_pm | categorical_or_expression_text | expression_parseable_check | calculation process of item hc_pm; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| hc_bd_calcproc | string | engine metadata not exposed | — | 109 | calculation process of item hc_bd | technical | calculation process of item hc_bd | categorical_or_expression_text | expression_parseable_check | calculation process of item hc_bd; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl_calcproc | string | engine metadata not exposed | — | 110 | calculation process of item btl | technical | calculation process of item btl | categorical_or_expression_text | expression_parseable_check | calculation process of item btl; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl_sales_calcproc | string | engine metadata not exposed | — | 111 | calculation process of item btl_sales | technical | calculation process of item btl_sales | categorical_or_expression_text | expression_parseable_check | calculation process of item btl_sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| btl_backout_calcproc | string | engine metadata not exposed | — | 112 | calculation process of item btl_backout | technical | calculation process of item btl_backout | categorical_or_expression_text | expression_parseable_check | calculation process of item btl_backout; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| cust_rebate_calcproc | string | engine metadata not exposed | — | 113 | calculation process of item cust_rebate | technical | calculation process of item cust_rebate | categorical_or_expression_text | expression_parseable_check | calculation process of item cust_rebate; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| mof_calcproc | string | engine metadata not exposed | — | 114 | calculation process of item mof | technical | calculation process of item mof | categorical_or_expression_text | expression_parseable_check | calculation process of item mof; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_out_load_calcproc | string | engine metadata not exposed | — | 115 | calculation process of item frt_out_load | technical | calculation process of item frt_out_load | categorical_or_expression_text | expression_parseable_check | calculation process of item frt_out_load; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_out_exp_calcproc | string | engine metadata not exposed | — | 116 | calculation process of item frt_out_exp | technical | calculation process of item frt_out_exp | categorical_or_expression_text | expression_parseable_check | calculation process of item frt_out_exp; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| whoh_pack_calcproc | string | engine metadata not exposed | — | 117 | calculation process of item whoh_pack | technical | calculation process of item whoh_pack | categorical_or_expression_text | expression_parseable_check | calculation process of item whoh_pack; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_ob_recovery_calcproc | string | engine metadata not exposed | — | 118 | calculation process of item frt_ob_recovery | technical | calculation process of item frt_ob_recovery | categorical_or_expression_text | expression_parseable_check | calculation process of item frt_ob_recovery; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_ib_recovery_calcproc | string | engine metadata not exposed | — | 119 | calculation process of item frt_ib_recovery | technical | calculation process of item frt_ib_recovery | categorical_or_expression_text | expression_parseable_check | calculation process of item frt_ib_recovery; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| others_calcproc | string | engine metadata not exposed | — | 120 | calculation process of item others | technical | calculation process of item others | categorical_or_expression_text | expression_parseable_check | calculation process of item others; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| others_sales_calcproc | string | engine metadata not exposed | — | 121 | calculation process of item others_sales | technical | calculation process of item others_sales | categorical_or_expression_text | expression_parseable_check | calculation process of item others_sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_disc_calcproc | string | engine metadata not exposed | — | 122 | calculation process of item scm_disc | technical | calculation process of item scm_disc | categorical_or_expression_text | expression_parseable_check | calculation process of item scm_disc; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| scm_ndisc_calcproc | string | engine metadata not exposed | — | 123 | calculation process of item scm_ndisc | technical | calculation process of item scm_ndisc | categorical_or_expression_text | expression_parseable_check | calculation process of item scm_ndisc; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| frt_in_calcproc | string | engine metadata not exposed | — | 124 | calculation process of item frt_in | technical | calculation process of item frt_in | categorical_or_expression_text | expression_parseable_check | calculation process of item frt_in; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| trans_btl_calcproc | string | engine metadata not exposed | — | 125 | calculation process of item trans_btl | technical | calculation process of item trans_btl | categorical_or_expression_text | expression_parseable_check | calculation process of item trans_btl; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| trans_btl_sales_calcproc | string | engine metadata not exposed | — | 126 | calculation process of item trans_btl_sales | technical | calculation process of item trans_btl_sales | categorical_or_expression_text | expression_parseable_check | calculation process of item trans_btl_sales; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| ngm_amt_calcproc | string | engine metadata not exposed | — | 127 | calculation process of ngm_amt | technical | calculation process of ngm_amt | categorical_or_expression_text | expression_parseable_check | calculation process of ngm_amt; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| oplgm_amt_calcproc | string | engine metadata not exposed | — | 128 | calculation process of oplgm_amt | technical | calculation process of oplgm_amt | categorical_or_expression_text | expression_parseable_check | calculation process of oplgm_amt; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| company_no | int | engine metadata not exposed | — | 129 | Company No. | key | Company No. | integer | not_null_expected|dim_fk_check_recommended | Company No.; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| etl_timestamp | timestamp | engine metadata not exposed | — | 130 | etl current time | technical | etl current time | categorical_or_expression_text | expression_parseable_check | etl current time; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| oplgm_plus_amt | decimal(20,8) | engine metadata not exposed | — | 131 | opl plus amount | measure | opl plus amount | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | opl plus amount; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | engine metadata not exposed |
| oplgm_plus_amt_calcproc | string | engine metadata not exposed | — | 132 | calculation process of oplgm_plus_amt | technical | calculation process of oplgm_plus_amt | categorical_or_expression_text | expression_parseable_check | calculation process of oplgm_plus_amt; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |
| date_flag | date | engine metadata not exposed | — | 133 | date flag | key | date flag | YYYY-MM-DD | not_null_expected|dim_fk_check_recommended | date flag; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | `dim_us.dim_pub_date.date_flag` |
| adjust_flag | int | engine metadata not exposed | — | 134 | data adjust flag: 0-normal data, 1-adjust data | dimension | data adjust flag: 0-normal data, 1-adjust data | integer | domain_value_check_recommended | data adjust flag: 0-normal data, 1-adjust data; order-line P&L base fact on `dw_us.dwd_disty_brpt_orders_pl_di`. | — |


### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_*` / pub order ODS layer
    hop: 1
    relation_type: source_sync
    via_job_or_view: disty B-report order P&L load chain (Sybase legacy → Hive ODS → `dwd_disty_brpt_orders_pl_di`)
  - table_fqn: `dim_us.dim_pub_order_type`
    hop: 1
    relation_type: filter_join
    via_job_or_view: shipped-order scope (`sales = 'Y'`)
- downstream_n_hops:
  - table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi`
    hop: 1
    relation_type: enrich_derive
    via_job_or_view: `disty_b_rpt_addition_task_us` (dimension enrichment + calcproc)
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: `dws_disty_brpt_pl_extend_1d.py`
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high (BAF pl_extend chain + etl_mi upstream reference)


### Column Lineage and Derivation

- Order keys (`order_no`, `order_line_no`, `order_type`): pass-through from shipped order ODS.
- Unit economics (`u_price`, `u_cost`, `u_sum_expense`, `ship_qty`, `sales_total`): base sales/cost components at order-line grain.
- P&L component columns (`btl`, `pdt`, `ngm_amt`, `oplgm_amt`, etc.): allocated expense/rebate/inventory charges per B-report P&L rules.
- `*_calcproc` columns: textual audit trail of allocation logic per P&L item.
- `virtual_type`: `0` normal lines, `1` virtual lines; B Report default filters `virtual_type = 0`.
- `adjust_flag` partition: `0` normal load, `1` adjustment rows.


### Freshness and Load Path

- Producer: disty B-report common / addition flows writing Hive partition (`date_flag`, `adjust_flag`).
- Vertica: not mirrored as primary table; use `dwd_disty_brpt_orders_pl_etl_mi` on Vertica for BI consumption.
- Expected completion window: 02:30-04:00 PT (before pl_extend serving build).
- Freshness confidence: medium.


## L2 Declarative Knowledge

### Business Definitions

- Domain: US disty B Report order-line P&L **base fact** (pre-enrichment sibling of `dwd_disty_brpt_orders_pl_etl_mi`).
- Trust tier: governed fact base.
- Grain: one row per order line per `date_flag` and `adjust_flag`.
- Core measures: P&L components feeding `ngm_amt`, `oplgm_amt`, `oplgm_plus_amt`; see `metric-index.md` for formulas on enriched fact.



### Dimension Keys and Lookup Reference

- `cust_no` → `dim_us.dim_pub_customer_info` (`cust_name`, `cust_type`, `sales_terr`)
- `vend_no` → `dim_us.dim_pub_vendor_info` (`vend_name`, `master_vend_no`, `vend_seg_code`)
- `sku_no` → `dim_us.dim_pub_part_info` (`part_no`, `short_desc`, `vpl_no`)
- `vpl_no` → `dim_us.dim_pub_vpl_info` (`vpl_code`, `vpl_desc`, `vend_no`)
- `pm_id` → `dim_us.dim_pub_vpl_hierarchy_info` (PM/Buyer hierarchy attributes)

### Time Field Semantics

- `date_flag`: business date; primary filter field for natural-month and as-of-date queries.
- `month_no`: internal fiscal period index from `dim_us.dim_pub_date.m`; **not** YYYYMM — map via date dimension.
- `*_mtd`/`*_comb_mtd` columns: month-to-date cumulative values through `date_flag`; for month-total reporting use month-end `date_flag` row only.
- `*_1d` columns: single-day snapshot values for `date_flag`.
- `*_wtd` columns: week-to-date cumulative through `date_flag`.

### Metrics Served

- net_sales: canonical formula in `metric-index.md`
- gross_sales: canonical formula in `metric-index.md`
- gm_amt: canonical formula in `metric-index.md`
- tgm_amt: canonical formula in `metric-index.md`
- ngm_amt: canonical formula in `metric-index.md`
- oplgm_amt: canonical formula in `metric-index.md`
- oplgm_plus_amt: canonical formula in `metric-index.md`
- total_btl: canonical formula in `metric-index.md`

## L3 Procedural Knowledge

### Query and Routing Rules

- Prefer this table when required dimensions and time suffix match the question grain.
- Fall back to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` for order-line recalculation or missing dimensions.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary keys: —
- Common join keys: date_flag/order_no/order_line_no and business entity keys
- High-risk join pitfalls: Key type mismatch and duplicate-key expansion.

### Key Filters and ETL Business Logic

- By default, do **not** apply `dim_us.dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1`.
- Apply the order-type / shipped-order join (`sales = 'Y'`) **only when the question explicitly says shipped orders only** (or equivalent).
- Apply `virtual_type = 0` or a specific `order_type` **only when the question explicitly requests that scope**.
- For profitability metrics on this table, always filter `segment_exclude = 'N'` (see `source/ref/b-report-us/special_logic.txt`).
- Technical sync predicates (partition/date load guards) are not business filters.

### Standard Time-Filter SQL (3 snippets)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dw_us.dwd_disty_brpt_orders_pl_di
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dw_us.dwd_disty_brpt_orders_pl_di
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
GROUP BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dw_us.dwd_disty_brpt_orders_pl_di
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_trunc('MM', date_flag) AS month_start, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= add_months(current_date, -6)
GROUP BY date_trunc('MM', date_flag)
ORDER BY month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row counts and `date_flag` coverage after each monthly close.
- Check dimension key match rates for `cust_no`, `vend_no`, `sku_no` joins.
- Monitor null rates on key measures (`ngm_amt`, `net_sales`).

### Metric Recompute Spot-Checks

- Recompute `net_sales`, `ngm_amt`, `oplgm_amt` from DWD for sample `date_flag` and compare to serving table aggregates.
- DWD gold validation (2026-06-09): 117,868 rows, zero mismatches at 0.01 tolerance.

### Conflicts and Open Questions

- Conflict item:
  - claim_a: —
  - claim_b: —
  - status: Needs Clarification
  - user_decision: awaiting governed routing precedence confirmation
- Open: PM/Buyer hierarchy unmatched-rate baseline across full month window not yet decomposed by fallback branch.

## L5 Runtime View

### Query Path and Engine Preference

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access Constraints

- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

## L6 Access and Consumption

### Primary Consumers and Use Cases

- Consumers: B Report semantic layer, dashboard queries, and BI users.
- Use cases: profitability tracking, vendor/customer ranking, PM performance, YoY trend analysis, executive dashboards.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: audit
table_fqn: dw_us.dwd_disty_brpt_orders_pl_di
anti_use: daily date_flag scan only; not routing_certified; do not copy for ranking
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt, SUM(net_sales) AS net_sales
FROM dw_us.dwd_disty_brpt_orders_pl_di
WHERE date_flag >= '2026-01-01' AND date_flag < '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```