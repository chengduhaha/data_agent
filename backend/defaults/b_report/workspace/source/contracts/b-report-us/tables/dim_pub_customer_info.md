# dim_us.dim_pub_customer_info

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_customer_info
- domain: b-report-us
- one_line_purpose: US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_customer_info`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_customer_info`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_customer_info` verified present.
- Vertica: `dim_us.dim_pub_customer_info` verified present.
- Row count (Vertica, 2026-06-25): 391,646 rows.
- Key cardinality: `cust_no` unique; `cust_name` 332,236 distinct (~59k duplicate names); `mcust_no` 351,465 distinct; `mcust_name` 308,636 distinct.
- Snapshot variant: `dim_pub_customer_info_df` for as-of `date_flag` customer attributes.

### Column Catalog (100% columns)

- documented_column_count: 111
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mcust_no | int | engine metadata not exposed | — | 1 | the customer master no,from xref_no of ods_cis_dbo_cust_xref | key | mcust no | integer | not_null_expected|dim_fk_check_recommended | mcust no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | `dim_us.dim_pub_customer_info.cust_no` |
| mcust_name | varchar(200) | engine metadata not exposed | — | 2 | the customer master name,from cust_name of ods_cis_dbo_customer_header | dimension | mcust name | categorical_or_expression_text | domain_value_check_recommended | mcust name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_no | int | engine metadata not exposed | — | 3 | the customer no,from cust_no of ods_cis_dbo_customer_header | key | cust no | integer | not_null_expected|dim_fk_check_recommended | cust no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | `dim_us.dim_pub_customer_info.cust_no` |
| cust_name | varchar(200) | engine metadata not exposed | — | 4 | the customer name,from cust_name of ods_cis_dbo_customer_header | dimension | cust name | categorical_or_expression_text | domain_value_check_recommended | cust name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_type | int | engine metadata not exposed | — | 5 | Customer type | dimension | cust type | integer | domain_value_check_recommended | cust type; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_type_descr | varchar(200) | engine metadata not exposed | — | 6 | the customer type description,from cust_type_descr of ods_cis_dbo_cust_type | dimension | cust type descr | categorical_or_expression_text | domain_value_check_recommended | cust type descr; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_acct_type | varchar(80) | engine metadata not exposed | — | 7 | Reseller/End User | dimension | cust acct type | categorical_or_expression_text | domain_value_check_recommended | cust acct type; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| is_restricted | varchar(4) | engine metadata not exposed | — | 8 | whether the customer is restricted | dimension | is restricted | categorical_or_expression_text | domain_value_check_recommended | is restricted; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| is_discontinued | varchar(4) | engine metadata not exposed | — | 9 | whether the customer is discontinued | dimension | is discontinued | categorical_or_expression_text | domain_value_check_recommended | is discontinued; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| sales_terr | int | engine metadata not exposed | — | 10 | the territory of sales | dimension | sales terr | integer | domain_value_check_recommended | sales terr; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| sales_terr_name | varchar(200) | engine metadata not exposed | — | 11 | the territory name of sales,from terr_name of ods_cis_dbo_territory | dimension | sales terr name | categorical_or_expression_text | domain_value_check_recommended | sales terr name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| sales_segment | varchar(200) | engine metadata not exposed | — | 12 | the segment of sales | dimension | sales segment | categorical_or_expression_text | domain_value_check_recommended | sales segment; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| division_desc | varchar(200) | engine metadata not exposed | — | 13 | the description of division,from division_desc of ods_cis_dbo_division | dimension | division desc | categorical_or_expression_text | domain_value_check_recommended | division desc; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| lead_id | int | engine metadata not exposed | — | 14 | Lead ID | key | lead id | integer | not_null_expected|dim_fk_check_recommended | lead id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| profile_c | varchar(200) | engine metadata not exposed | — | 15 | Primary Customer Focus,from profile_c of ods_cis_dbo_cust_profile | dimension | profile c | categorical_or_expression_text | domain_value_check_recommended | profile c; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| outside_sales_rep | int | engine metadata not exposed | — | 16 | outside_sales_rep | measure | outside sales rep | integer | non_negative_expected|outlier_check_recommended | outside sales rep; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| outside_sales_rep_name | varchar(200) | engine metadata not exposed | — | 17 | outside_sales_rep_name | dimension | outside sales rep name | categorical_or_expression_text | domain_value_check_recommended | outside sales rep name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_cust_addr | varchar(200) | engine metadata not exposed | — | 18 | Bill To Customer Address | dimension | bill to cust addr | categorical_or_expression_text | domain_value_check_recommended | bill to cust addr; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_cust_zip | varchar(200) | engine metadata not exposed | — | 19 | Bill To Customer Zip | dimension | bill to cust zip | categorical_or_expression_text | domain_value_check_recommended | bill to cust zip; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_cust_city | varchar(200) | engine metadata not exposed | — | 20 | Bill To Customer City | dimension | bill to cust city | categorical_or_expression_text | domain_value_check_recommended | bill to cust city; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_cust_state | varchar(200) | engine metadata not exposed | — | 21 | Bill To Customer State | dimension | bill to cust state | categorical_or_expression_text | domain_value_check_recommended | bill to cust state; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_cust_country | varchar(200) | engine metadata not exposed | — | 22 | Bill To Customer Country | dimension | bill to cust country | categorical_or_expression_text | domain_value_check_recommended | bill to cust country; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_contact_name | varchar(200) | engine metadata not exposed | — | 23 | Bill To Contact Name | dimension | bill to contact name | categorical_or_expression_text | domain_value_check_recommended | bill to contact name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_contact_email | varchar(200) | engine metadata not exposed | — | 24 | Bill To Contact Email | dimension | bill to contact email | categorical_or_expression_text | domain_value_check_recommended | bill to contact email; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_contact_phone | varchar(200) | engine metadata not exposed | — | 25 | Bill To Contact Phone | dimension | bill to contact phone | categorical_or_expression_text | domain_value_check_recommended | bill to contact phone; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| bill_to_contact_title | varchar(200) | engine metadata not exposed | — | 26 | Bill To Contact Title | dimension | bill to contact title | categorical_or_expression_text | domain_value_check_recommended | bill to contact title; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| resale_no | varchar(200) | engine metadata not exposed | — | 27 | resale_no | key | resale no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | resale no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| store_no | varchar(200) | engine metadata not exposed | — | 28 | store_no | key | store no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | store no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| default_terms | varchar(200) | engine metadata not exposed | — | 29 | default_terms | dimension | default terms | categorical_or_expression_text | domain_value_check_recommended | default terms; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| currency | varchar(200) | engine metadata not exposed | — | 30 | currency | dimension | currency | categorical_or_expression_text | domain_value_check_recommended | currency; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 31 | ETL datetime | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| finance_master | int | engine metadata not exposed | — | 32 | Get the field xref_no that source from CIS..cust_xref and xref_type is FINAN_SUB | dimension | finance master | integer | domain_value_check_recommended | finance master; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| division | int | engine metadata not exposed | — | 33 | Department id | dimension | division | integer | domain_value_check_recommended | division; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| region | int | engine metadata not exposed | — | 34 | The region of customer | dimension | region | integer | domain_value_check_recommended | region; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst | int | engine metadata not exposed | — | 35 | credit analyst id that it is a job position | dimension | credit analyst | integer | domain_value_check_recommended | credit analyst; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| program_analyst | varchar(200) | engine metadata not exposed | — | 36 | program analyst name  that it is a job position | dimension | program analyst | categorical_or_expression_text | domain_value_check_recommended | program analyst; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| service_analyst | varchar(200) | engine metadata not exposed | — | 37 | service analyst name  that it is a job position | dimension | service analyst | categorical_or_expression_text | domain_value_check_recommended | service analyst; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_id | int | engine metadata not exposed | — | 38 | Account Receivable collector id | key | collector id | integer | not_null_expected|dim_fk_check_recommended | collector id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_name | varchar(200) | engine metadata not exposed | — | 39 | Account Receivable collector name | dimension | collector name | categorical_or_expression_text | domain_value_check_recommended | collector name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| release_code | varchar(200) | engine metadata not exposed | — | 40 | Credit release code | dimension | release code | categorical_or_expression_text | domain_value_check_recommended | release code; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_limit | int | engine metadata not exposed | — | 41 | Limit of credit source from CIS..customer_credit | dimension | credit limit | integer | domain_value_check_recommended | credit limit; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reviewer | int | engine metadata not exposed | — | 42 | Credit Collector  that assigned  this account (employee user id) source from CIS..cusomter_header | dimension | reviewer | integer | domain_value_check_recommended | reviewer; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| next_review | timestamp | engine metadata not exposed | — | 43 | Next  review date | dimension | next review | categorical_or_expression_text | domain_value_check_recommended | next review; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| pending_amt | int | engine metadata not exposed | — | 44 | Pending amout that source from CIS..customer_credit | measure | pending amt | integer | non_negative_expected|outlier_check_recommended | pending amt; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_channel | varchar(100) | engine metadata not exposed | — | 45 | Get the field profile_c that source from CIS..cust_profile and profile_type is CHANNEL and  profile_cat is CUST | dimension | cust channel | categorical_or_expression_text | domain_value_check_recommended | cust channel; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| varnex_members | varchar(100) | engine metadata not exposed | — | 46 | Get the field profile_c that source from CIS..cust_profile and profile_type is VARNEX | dimension | varnex members | categorical_or_expression_text | domain_value_check_recommended | varnex members; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| customer_entry_datetime | timestamp | engine metadata not exposed | — | 47 | Date record was inserted to mycis system,that source from CIS..customer_header | dimension | customer entry datetime | categorical_or_expression_text | domain_value_check_recommended | customer entry datetime; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| program_analyst_id | int | engine metadata not exposed | — | 48 | program analyst id that it is a job position | key | program analyst id | integer | not_null_expected|dim_fk_check_recommended | program analyst id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| service_analyst_id | int | engine metadata not exposed | — | 49 | service analyst id  that it is a job position | key | service analyst id | integer | not_null_expected|dim_fk_check_recommended | service analyst id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_manager_id | int | engine metadata not exposed | — | 50 | Account Receivable collector manager id | key | collector manager id | integer | not_null_expected|dim_fk_check_recommended | collector manager id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_manager_name | varchar(66) | engine metadata not exposed | — | 51 | Account Receivable collector manager name | dimension | collector manager name | categorical_or_expression_text | domain_value_check_recommended | collector manager name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_director_id | int | engine metadata not exposed | — | 52 | Account Receivable collector director id | key | collector director id | integer | not_null_expected|dim_fk_check_recommended | collector director id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_director_name | varchar(32) | engine metadata not exposed | — | 53 | Account Receivable collector director name | dimension | collector director name | categorical_or_expression_text | domain_value_check_recommended | collector director name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_vp_id | int | engine metadata not exposed | — | 54 | Account Receivable collector Vice President id | key | collector vp id | integer | not_null_expected|dim_fk_check_recommended | collector vp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_vp_name | varchar(24) | engine metadata not exposed | — | 55 | Account Receivable collector Vice President name | dimension | collector vp name | categorical_or_expression_text | domain_value_check_recommended | collector vp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_name | varchar(70) | engine metadata not exposed | — | 56 | credit analyst name | dimension | credit analyst name | categorical_or_expression_text | domain_value_check_recommended | credit analyst name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_manager_id | int | engine metadata not exposed | — | 57 | credit analyst manager id | key | credit analyst manager id | integer | not_null_expected|dim_fk_check_recommended | credit analyst manager id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_manager_name | varchar(50) | engine metadata not exposed | — | 58 | credit analyst manager name | dimension | credit analyst manager name | categorical_or_expression_text | domain_value_check_recommended | credit analyst manager name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_director_id | int | engine metadata not exposed | — | 59 | credit analyst director id | key | credit analyst director id | integer | not_null_expected|dim_fk_check_recommended | credit analyst director id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_director_name | varchar(32) | engine metadata not exposed | — | 60 | credit analyst director name | dimension | credit analyst director name | categorical_or_expression_text | domain_value_check_recommended | credit analyst director name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_vp_id | int | engine metadata not exposed | — | 61 | credit analyst Vice President id | key | credit analyst vp id | integer | not_null_expected|dim_fk_check_recommended | credit analyst vp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_vp_name | varchar(24) | engine metadata not exposed | — | 62 | credit analyst Vice President name | dimension | credit analyst vp name | categorical_or_expression_text | domain_value_check_recommended | credit analyst vp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| buying_group_no | int | engine metadata not exposed | — | 63 | buying group number | key | buying group no | integer | not_null_expected|dim_fk_check_recommended | buying group no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| price_grid | varchar(22) | engine metadata not exposed | — | 64 | grid price | dimension | price grid | categorical_or_expression_text | domain_value_check_recommended | price grid; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| finance_cust_name | varchar(120) | engine metadata not exposed | — | 65 | customer name for finace | dimension | finance cust name | categorical_or_expression_text | domain_value_check_recommended | finance cust name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| ec_contact_no | int | engine metadata not exposed | — | 66 | ec contact no | key | ec contact no | integer | not_null_expected|dim_fk_check_recommended | ec contact no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| ec_contact_name | varchar(200) | engine metadata not exposed | — | 67 | ec contact name | dimension | ec contact name | categorical_or_expression_text | domain_value_check_recommended | ec contact name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| ec_contact_phone_no | varchar(42) | engine metadata not exposed | — | 68 | ec contact phone no | key | ec contact phone no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | ec contact phone no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| ec_contact_email_address | varchar(100) | engine metadata not exposed | — | 69 | ec contact email address | dimension | ec contact email address | categorical_or_expression_text | domain_value_check_recommended | ec contact email address; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| customer_delete_datetime | timestamp | engine metadata not exposed | — | 70 | Entry date stamp when the record was deleted/deactivated in CIS | dimension | customer delete datetime | categorical_or_expression_text | domain_value_check_recommended | customer delete datetime; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| customer_update_datetime | timestamp | engine metadata not exposed | — | 71 | Entry date stamp when the acct was updated in CIS | dimension | customer update datetime | categorical_or_expression_text | domain_value_check_recommended | customer update datetime; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_supervisor_id | int | engine metadata not exposed | — | 72 | Account Receivable collector supervisor id | key | collector supervisor id | integer | not_null_expected|dim_fk_check_recommended | collector supervisor id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_supervisor_name | varchar(100) | engine metadata not exposed | — | 73 | Account Receivable collector supervisor name | dimension | collector supervisor name | categorical_or_expression_text | domain_value_check_recommended | collector supervisor name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_senior_manager_id | int | engine metadata not exposed | — | 74 | Account Receivable senior manager id | key | collector senior manager id | integer | not_null_expected|dim_fk_check_recommended | collector senior manager id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_senior_manager_name | varchar(100) | engine metadata not exposed | — | 75 | Account Receivable senior manager id | dimension | collector senior manager name | categorical_or_expression_text | domain_value_check_recommended | collector senior manager name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_svp_id | int | engine metadata not exposed | — | 76 | Account Receivable Senior Vice President id | key | collector svp id | integer | not_null_expected|dim_fk_check_recommended | collector svp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_svp_name | varchar(100) | engine metadata not exposed | — | 77 | Account Receivable Senior Vice President name | dimension | collector svp name | categorical_or_expression_text | domain_value_check_recommended | collector svp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_supervisor_id | int | engine metadata not exposed | — | 78 | credit analyst supervisor id | key | credit analyst supervisor id | integer | not_null_expected|dim_fk_check_recommended | credit analyst supervisor id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_supervisor_name | varchar(100) | engine metadata not exposed | — | 79 | credit analyst supervisor name | dimension | credit analyst supervisor name | categorical_or_expression_text | domain_value_check_recommended | credit analyst supervisor name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_senior_manager_id | int | engine metadata not exposed | — | 80 | credit analyst senior manager id | key | credit analyst senior manager id | integer | not_null_expected|dim_fk_check_recommended | credit analyst senior manager id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_senior_manager_name | varchar(100) | engine metadata not exposed | — | 81 | credit analyst senior manager name | dimension | credit analyst senior manager name | categorical_or_expression_text | domain_value_check_recommended | credit analyst senior manager name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_svp_id | int | engine metadata not exposed | — | 82 | credit analyst Senior Vice President id | key | credit analyst svp id | integer | not_null_expected|dim_fk_check_recommended | credit analyst svp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_svp_name | varchar(100) | engine metadata not exposed | — | 83 | credit analyst Senior Vice President name | dimension | credit analyst svp name | categorical_or_expression_text | domain_value_check_recommended | credit analyst svp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| stop_mailing | timestamp | engine metadata not exposed | — | 84 | stop send email to this loc | dimension | stop mailing | categorical_or_expression_text | domain_value_check_recommended | stop mailing; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_app | timestamp | engine metadata not exposed | — | 85 | Date the customer completed an application | dimension | credit app | categorical_or_expression_text | domain_value_check_recommended | credit app; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| website_address | varchar(100) | engine metadata not exposed | — | 86 | Customers website address | dimension | website address | categorical_or_expression_text | domain_value_check_recommended | website address; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| last_update_comb | timestamp | engine metadata not exposed | — | 87 | Combined last update time of record | dimension | last update comb | categorical_or_expression_text | domain_value_check_recommended | last update comb; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| company_code | varchar(100) | engine metadata not exposed | — | 88 | Company code such as cis_us/cis_ca | dimension | company code | categorical_or_expression_text | domain_value_check_recommended | company code; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| company_no | int | engine metadata not exposed | — | 89 | Company number | key | company no | integer | not_null_expected|dim_fk_check_recommended | company no; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| cust_seg_id | int | engine metadata not exposed | — | 90 | Customer segment id | key | cust seg id | integer | not_null_expected|dim_fk_check_recommended | cust seg id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| customer_alias_name | varchar(100) | engine metadata not exposed | — | 91 | Customer alias name | dimension | customer alias name | categorical_or_expression_text | domain_value_check_recommended | customer alias name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| currency_profile | varchar(100) | engine metadata not exposed | — | 92 | Currency profile | dimension | currency profile | categorical_or_expression_text | domain_value_check_recommended | currency profile; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reseller_contact | varchar(200) | engine metadata not exposed | — | 93 | reseller contact name | dimension | reseller contact | categorical_or_expression_text | domain_value_check_recommended | reseller contact; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reseller_contact_country | varchar(200) | engine metadata not exposed | — | 94 | reseller contact country | dimension | reseller contact country | categorical_or_expression_text | domain_value_check_recommended | reseller contact country; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reseller_contact_email | varchar(200) | engine metadata not exposed | — | 95 | reseller contact email id | dimension | reseller contact email | categorical_or_expression_text | domain_value_check_recommended | reseller contact email; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reseller_contact_fax | varchar(60) | engine metadata not exposed | — | 96 | reseller contact fax | dimension | reseller contact fax | categorical_or_expression_text | domain_value_check_recommended | reseller contact fax; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| reseller_contact_phone | varchar(60) | engine metadata not exposed | — | 97 | reseller contact phone no | dimension | reseller contact phone | categorical_or_expression_text | domain_value_check_recommended | reseller contact phone; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| is_share_credit_limit | varchar(100) | engine metadata not exposed | — | 98 | share Credit limit Flag | dimension | is share credit limit | categorical_or_expression_text | domain_value_check_recommended | is share credit limit; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| terr_email | varchar(200) | engine metadata not exposed | — | 99 | territory email | measure | terr email | categorical_or_expression_text | non_negative_expected|outlier_check_recommended | terr email; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| logo_url | varchar(2000) | engine metadata not exposed | — | 100 | logo url | dimension | logo url | categorical_or_expression_text | domain_value_check_recommended | logo url; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| company_summary | varchar(5000) | engine metadata not exposed | — | 101 | company summary | dimension | company summary | categorical_or_expression_text | domain_value_check_recommended | company summary; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| customer_communities | varchar(2000) | engine metadata not exposed | — | 102 | Customer community information | dimension | customer communities | categorical_or_expression_text | domain_value_check_recommended | customer communities; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| data_source | varchar(100) | engine metadata not exposed | — | 103 | Indicate the source of the data eg:CIS or HIS | dimension | data source | categorical_or_expression_text | domain_value_check_recommended | data source; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_senior_director_id | int | engine metadata not exposed | — | 104 | collector senior director id | key | collector senior director id | integer | not_null_expected|dim_fk_check_recommended | collector senior director id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_senior_director_name | varchar(100) | engine metadata not exposed | — | 105 | collector senior director name | dimension | collector senior director name | categorical_or_expression_text | domain_value_check_recommended | collector senior director name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_evp_id | int | engine metadata not exposed | — | 106 | collector evp id | key | collector evp id | integer | not_null_expected|dim_fk_check_recommended | collector evp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| collector_evp_name | varchar(100) | engine metadata not exposed | — | 107 | ollector evp name | dimension | collector evp name | categorical_or_expression_text | domain_value_check_recommended | collector evp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_senior_director_id | int | engine metadata not exposed | — | 108 | credit analyst senior director id | key | credit analyst senior director id | integer | not_null_expected|dim_fk_check_recommended | credit analyst senior director id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_senior_director_name | varchar(100) | engine metadata not exposed | — | 109 | credit analyst senior  director name | dimension | credit analyst senior director name | categorical_or_expression_text | domain_value_check_recommended | credit analyst senior director name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_evp_id | int | engine metadata not exposed | — | 110 | credit analyst evp id | key | credit analyst evp id | integer | not_null_expected|dim_fk_check_recommended | credit analyst evp id; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |
| credit_analyst_evp_name | varchar(100) | engine metadata not exposed | — | 111 | credit analyst evp name | dimension | credit analyst evp name | categorical_or_expression_text | domain_value_check_recommended | credit analyst evp name; Customer master attribute on `dim_us.dim_pub_customer_info`; join on `cust_no` or `mcust_no`. | — |

### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_cis_corp_customer` (and related CIS customer ODS tables)
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_customer_dimension_us.dim_pub_customer_info` (`dim_pub_customer_info_disty.sql`)
  - table_fqn: `dim_us.dim_pub_sales_territory`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: territory name / hierarchy enrichment in customer dimension build
- downstream_n_hops:
  - table_fqn: `dw_us.dwd_disty_brpt_orders_pl_etl_mi`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: B Report order-line fact (`cust_no` lookup)
  - table_fqn: `dw_us.dws_disty_brpt_cust_mtd`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: customer serving mart label enrichment
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: extended P&L slice (`cust_name`, `mcust_name` denormalized)
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high (pub_dw customer dimension flow + B Report consumption)


### Column Lineage and Derivation

- `cust_no` / `mcust_no`: business keys from CIS customer master; one row per sub-customer with master-customer hierarchy.
- `cust_name`, `mcust_name`, territory and analyst attributes: denormalized labels from customer master and related reference tables during `dim_pub_customer_info` load.
- Credit/collector hierarchy IDs and names: derived from organizational assignment tables in customer dimension ETL.
- No measure columns; attributes are current-state dimension descriptors.


### Freshness and Load Path

- Producer flow: `public_customer_dimension_us` job `dim_pub_customer_info` (daily) with optional `dim_pub_customer_info_df` date-keyed snapshot for as-of joins.
- Vertica sync: `hive2vertica_dim_pub_customer_info`.
- Expected completion window: 02:00-04:00 PT (before B Report common load).
- Freshness confidence: medium (schedule-derived).


## L2 Declarative Knowledge

### Business Definitions

- Domain: US customer master dimension for B Report and pub order analytics.
- Trust tier: governed reference (shared `pub_dw` customer dimension).
- Grain: one row per `cust_no` (sub-customer); `mcust_no` groups master-customer families.
- Primary use in B Report: enrich `cust_no`/`mcust_no` with names, territory, type, division, and credit hierarchy attributes.



### Dimension Keys and Lookup Reference

- Sub-customer key: `cust_no` (int) — primary fact join key.
- Master customer key: `mcust_no` (int) — groups sub-customers under a master account family.
- Labels: `cust_name` (sub-customer display), `mcust_name` (master customer display); `customer_alias_name` for alternate search.
- Master customer filter: use `mcust_name` (not `master_cust_name`).
- Sub-customer breakdown under a master: filter `mcust_name` or `mcust_no`, then `GROUP BY cust_no` with `MAX(cust_name)` for display.

### Dimension Lookup / Join Reference

- `mcust_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.mcust_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `cust_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.cust_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `lead_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.lead_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `outside_sales_rep` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.outside_sales_rep = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `resale_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.resale_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `store_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.store_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `pending_amt` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.pending_amt = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `program_analyst_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.program_analyst_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `service_analyst_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.service_analyst_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_manager_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_manager_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_director_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_director_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_vp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_vp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_manager_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_manager_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_director_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_director_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_vp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_vp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `buying_group_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.buying_group_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `ec_contact_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.ec_contact_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `ec_contact_phone_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.ec_contact_phone_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_supervisor_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_supervisor_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_senior_manager_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_senior_manager_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_svp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_svp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_supervisor_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_supervisor_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_senior_manager_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_senior_manager_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_svp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_svp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `company_no` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.company_no = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `cust_seg_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.cust_seg_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `terr_email` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.terr_email = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_senior_director_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_senior_director_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `collector_evp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.collector_evp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_senior_director_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_senior_director_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `credit_analyst_evp_id` → `dim_us.dim_pub_customer_info` | join: `dim_pub_customer_info.credit_analyst_evp_id = dim_us.dim_pub_customer_info` | lookup labels: `*_name` | cardinality: many:1 | confidence: high (KB-wide ref index)

### Identifier Search Profile

- searchable_identifier_columns:
  - column: `cust_name`
    data_type: varchar
    match_mode: exact then contains_like (`ILIKE '%token%'`)
  - column: `mcust_name`
    data_type: varchar
    match_mode: exact then contains_like
  - column: `customer_alias_name`
    data_type: varchar
    match_mode: exact then contains_like
  - column: `finance_cust_name`
    data_type: varchar
    match_mode: contains_like
- non_searchable_key_columns: `cust_no`, `mcust_no`, `sales_terr`, `company_no` — do not compare alphanumeric user tokens to integer keys
- user_facing_aliases: `customer`, `master customer`, `account` → search `cust_name` / `mcust_name`; `CDW` style tokens → `mcust_name` ILIKE
- resolution_flow: user customer name token → exact/`ILIKE` on `mcust_name` (master scope) or `cust_name` (sub-customer) → obtain `mcust_no` or `cust_no` → join facts on `fact.cust_no = dim.cust_no` or filter master via `mcust_no`

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| cust_no | 391646 | 391646 | unique | yes | business key / sub-customer id |
| cust_name | 332236 | 391646 | non_unique | no | display only; duplicate names common |
| mcust_no | 351465 | 391646 | non_unique | filter_ok | master key |
| mcust_name | 308636 | 391646 | non_unique | no | master filter when mcust_no unknown |

### Time Field Semantics

- Current-state dimension (no `date_flag` on base table); use `dim_us.dim_pub_customer_info_df` when as-of `date_flag` snapshot is required by serving ETL.
- For historical customer attributes at a business date, join `_df` snapshot on `cust_no` and `date_flag`.

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use for customer name → `cust_no`/`mcust_no` resolution when serving tables lack denormalized names.
- Master-customer questions: filter `mcust_name` (or `mcust_no`), aggregate at `cust_no` for sub-customer breakdown — see golden `cdw-sub-customer-ranking`.
- Sub-customer questions: resolve `cust_name` → `cust_no`; never `GROUP BY cust_name` alone when keys are available.
- Facts carry `cust_no` (int); they do **not** reliably carry `cust_name` at all grains — join this dimension or use `dws_disty_brpt_cust_mtd` when names are denormalized.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary key: `cust_no`
- Fact join: `fact.cust_no = dim_pub_customer_info.cust_no`
- Master roll-up: `fact.mcust_no = dim_pub_customer_info.mcust_no` (many sub-customers per master)
- Territory context: `sales_terr` links to `dim_pub_sales_territory` for rep hierarchy
- As-of join: `dim_pub_customer_info_df` on `cust_no` AND `date_flag`
- High-risk pitfalls: `GROUP BY cust_name` (duplicate names); filtering integer `cust_no` with text tokens

### Key Filters and ETL Business Logic

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard Time-Filter SQL (3 snippets)

Time-filter snippets below apply to **fact/serving tables** joined to this dimension for metric questions. This dimension has no `date_flag`; use `*_df` snapshot variants when as-of attributes are required.

1) Natural month (month-end snapshot)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_customer_info
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
table_fqn: dim_us.dim_pub_customer_info
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
table_fqn: dim_us.dim_pub_customer_info
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

- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.

### Metric Recompute Spot-Checks

- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.

### Conflicts and Open Questions

- No active conflicts on dimension grain or key semantics as of 2026-06-25.

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

- Consumers: B Report order-line fact enrichment, `dws_disty_brpt_cust_mtd`, `pl_extend` customer labels.
- Use cases: customer name resolution, master/sub-customer hierarchy, territory and credit analyst attributes.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: illustrative
intent: scalar_lookup
table_fqn: dim_us.dim_pub_customer_info
anti_use: lookup only; aggregate metrics on dws_disty_brpt_cust_mtd or dm tables
-->
```sql
SELECT cust_no, cust_name, mcust_no, mcust_name, sales_terr, sales_terr_name
FROM dim_us.dim_pub_customer_info
WHERE mcust_name ILIKE '%CDW LOGISTICS%'
ORDER BY cust_no
LIMIT 20;
```

Certified sub-customer ranking under a master customer: `golden-questions.md` → `cdw-sub-customer-ranking`.
