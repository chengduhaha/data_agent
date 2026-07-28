# Marketing domain — Knowledgebase index

Documentation for IDC (International Data Corporation) distributor delivery ETL from `BAF/marketing_dw` → `hdfstohive/`.

**Source location:** `source/etl/sql/marketing/marketing_dw/hdfstohive/` (synced from Bitbucket `refs/heads/master`)  
**Bitbucket repo:** `BAF/marketing_dw`

## ETL scripts

| Knowledgebase doc | Source script | Target / role | Vertica query table |
|-------------------|---------------|---------------|---------------------|
| [ods_etl_marketing_idc_raw_data_month.md](ods_etl_marketing_idc_raw_data_month.md) | `script/ods_etl_marketing_idc_raw_data_month.sql` | `ods_gbl.ods_etl_marketing_idc_raw_data_month` | `dm_gbl.dm_idc_raw_data_month` |
| [ods_etl_marketing_idc_raw_data_week.md](ods_etl_marketing_idc_raw_data_week.md) | `script/ods_etl_marketing_idc_raw_data_week.sql` | `ods_gbl.ods_etl_marketing_idc_raw_data_week` | `dm_gbl.dm_idc_raw_data_week` |
| [read_hdfs_monthly.md](read_hdfs_monthly.md) | `read_hdfs_monthly.py` | `ods_ext_marketing_idc_raw_data_month_v1` | Hive-only (staging) |
| [read_hdfs.md](read_hdfs.md) | `read_hdfs.py` | `ods_ext_marketing_idc_raw_data_week_v1` | Hive-only (staging) |
| [literal_parameters.md](literal_parameters.md) | `literal_parameters.sql` | Parameter bootstrap (`start_date`) | N/A |
| [status_output.md](status_output.md) | `status_output.sql` | Overall upload status for email | N/A |

## Azkaban flows

| Knowledgebase doc | Flow file | Schedule | Vertica query table |
|-------------------|-----------|----------|---------------------|
| [idc_delivery_month_data.md](idc_delivery_month_data.md) | `idc_delivery_month_data.flow` | 13:30 CST daily | `dm_gbl.dm_idc_raw_data_month` |
| [idc_delivery_month_data_init.md](idc_delivery_month_data_init.md) | `idc_delivery_month_data_init.flow` | Manual | `dm_gbl.dm_idc_raw_data_month` |
| [idc_delivery_week_data.md](idc_delivery_week_data.md) | `idc_delivery_week_data.flow` | 13:30 CST daily | `dm_gbl.dm_idc_raw_data_week` |
| [idc_delivery_week_data_init.md](idc_delivery_week_data_init.md) | `idc_delivery_week_data_init.flow` | Manual | `dm_gbl.dm_idc_raw_data_week` |

## Bitbucket DDL ingest (latest run)

Bitbucket MCP (`user-gateway-bitbucket-prod`) was queried for marketing IDC table DDL at `refs/heads/master`:

| Qualified table | Repo browsed | Result |
|-----------------|--------------|--------|
| `ods_gbl.ods_etl_marketing_idc_raw_data_week` | `HIVE/snxhive` | Not found under `ods_gbl/table/` |
| `ods_gbl.ods_etl_marketing_idc_raw_data_month` | `HIVE/snxhive` | Not found under `ods_gbl/table/` |
| `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | `HIVE/snxhive` | Not found under `ods_gbl/table/` |
| `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | `HIVE/snxhive` | Not found under `ods_gbl/table/` |
| `dm_gbl.dm_idc_raw_data_week` | `VERTICA/vcdisty` | Not found under `dm_gbl/table/` |
| `dm_gbl.dm_idc_raw_data_month` | `VERTICA/vcdisty` | Not found under `dm_gbl/table/` |

**WKB L1/L3/L6 snapshot seeds (this run):**

| Seed file | Qualified table | Source | Columns |
|-----------|-----------------|--------|---------|
| `vertica_dm_gbl_dm_idc_raw_data_week.json` | `dm_gbl.dm_idc_raw_data_week` | Vertica MCP `get_table_structure` (metadata-only fallback) | 23 |
| `vertica_dm_gbl_dm_idc_raw_data_month.json` | `dm_gbl.dm_idc_raw_data_month` | Vertica MCP `get_table_structure` (metadata-only fallback) | 21 |

**Hive L1/L3/L6 seeds:** skipped — no CREATE TABLE DDL in `HIVE/snxhive` at `refs/heads/master`. Legacy Knowledgebase-derived seed `marketing_ods_etl_marketing_idc_raw_data_week.json` (L1/L2) remains unchanged.

**Vertica reporting schema** is indexed from live metadata; Hive staging/ODS column lists still await Bitbucket DDL publication.
