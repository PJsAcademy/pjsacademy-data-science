# ❄️ Snowflake Projects — Runnable Code (all 20)

These are the **actual runnable files** for the projects in the [Projects Vault](../README.md). Paste each `.sql` into a Snowflake worksheet, run the `.py` in a Snowflake Notebook / Snowpark session, and follow `.md` files for multi-file projects (dbt). Every file is commented line-by-line and ends with cleanup.

> Free **30-day Snowflake trial** ($400 credits): [signup.snowflake.com](https://signup.snowflake.com) — no card needed.

## All 20 project scripts

| # | File | Level | Teaches |
|---|------|-------|---------|
| 01 | [first_data_warehouse.sql](01_first_data_warehouse.sql) | ⭐ | Warehouses, star schema, JOIN analytics |
| 02 | [multi_source_loader.sql](02_multi_source_loader.sql) | ⭐⭐ | File formats, COPY INTO, error handling, VARIANT |
| 03 | [json_analytics.sql](03_json_analytics.sql) | ⭐⭐ | VARIANT, path notation, LATERAL FLATTEN |
| 04 | [performance_tuning_lab.sql](04_performance_tuning_lab.sql) | ⭐⭐⭐ | Clustering, search optimization, MV, result cache |
| 05 | [time_travel_recovery.sql](05_time_travel_recovery.sql) | ⭐⭐ | Time Travel AT/BEFORE, UNDROP |
| 06 | [zero_copy_cloning.sql](06_zero_copy_cloning.sql) | ⭐⭐⭐ | Zero-copy clones, point-in-time clones |
| 07 | [realtime_streaming_pipeline.sql](07_realtime_streaming_pipeline.sql) | ⭐⭐⭐⭐ | Streams + Tasks DAG, MERGE, CDC |
| 08 | [snowpipe_autoingest.sql](08_snowpipe_autoingest.sql) | ⭐⭐⭐ | Snowpipe, AUTO_INGEST, pipe monitoring |
| 09 | [snowpark_feature_pipeline.py](09_snowpark_feature_pipeline.py) | ⭐⭐⭐⭐ | Snowpark DataFrames, feature engineering |
| 10 | [in_warehouse_ml.py](10_in_warehouse_ml.py) | ⭐⭐⭐⭐ | Snowpark model → SQL UDF, ML from SQL |
| 11 | [rbac_framework.sql](11_rbac_framework.sql) | ⭐⭐⭐ | Access/functional roles, future grants |
| 12 | [data_masking_compliance.sql](12_data_masking_compliance.sql) | ⭐⭐⭐ | Masking + row-access policies (DPDP/GDPR) |
| 13 | [cost_dashboard.sql](13_cost_dashboard.sql) | ⭐⭐⭐ | Resource monitors, ACCOUNT_USAGE FinOps |
| 14 | [dbt_snowflake.md](14_dbt_snowflake.md) | ⭐⭐⭐⭐ | dbt staging→marts, tests, incremental |
| 15 | [cdc_data_vault.sql](15_cdc_data_vault.sql) | ⭐⭐⭐⭐ | Data Vault (Hub/Sat/Link) + CDC |
| 16 | [data_sharing.sql](16_data_sharing.sql) | ⭐⭐⭐ | Shares, secure views, reader accounts, Marketplace |
| 17 | [streamlit_dashboard.py](17_streamlit_dashboard.py) | ⭐⭐⭐⭐ | Streamlit in Snowflake |
| 18 | [fraud_detection.sql](18_fraud_detection.sql) | ⭐⭐⭐⭐⭐ | Real-time scoring with Streams + Tasks |
| 19 | [multi_region_dr.sql](19_multi_region_dr.sql) | ⭐⭐⭐⭐⭐ | Replication + failover groups (DR) |
| 20 | [end_to_end_platform.sql](20_end_to_end_platform.sql) | ⭐⭐⭐⭐⭐ | Full platform capstone |

## How to use
1. Open a Snowflake worksheet (or Notebook for `.py`).
2. Paste a script, read the comments, run section by section.
3. Observe the output, then run the cleanup at the bottom to save credits.

## ⚠️ Notes
- Written against current Snowflake syntax (2026). Some features (Dynamic Tables, Search Optimization, replication) need specific editions — scripts note this.
- Projects 08/16/19 have steps that need external cloud storage or a second account; those sections are marked and the learnable parts run standalone.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
