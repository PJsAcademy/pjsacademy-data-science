# ============================================================================
# PJ's Academy · Snowflake Project 09 — Snowpark Feature Pipeline  (Advanced)
# ----------------------------------------------------------------------------
# WHAT YOU BUILD: feature engineering entirely in Snowpark Python — data never
#   leaves Snowflake. The DataFrame API looks like pandas but runs distributed.
# HOW TO RUN: Snowflake Notebook (get_active_session) or local Snowpark session.
#   pip install "snowflake-snowpark-python[pandas]"
# ============================================================================

from snowflake.snowpark import Session
from snowflake.snowpark.functions import (
    col, datediff, current_date, when, iff, lit, avg, count
)

# 1) Session (see Project 10 for CONNECTION dict) ---------------------------
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except Exception:
    from _connection import CONNECTION          # your local config
    session = Session.builder.configs(CONNECTION).create()

session.sql("CREATE DATABASE IF NOT EXISTS FEAT_DEMO").collect()
session.sql("CREATE SCHEMA IF NOT EXISTS FEAT_DEMO.PUBLIC").collect()
session.use_database("FEAT_DEMO"); session.use_schema("PUBLIC")

# 2) Source data ------------------------------------------------------------
session.sql("""
  CREATE OR REPLACE TABLE customers AS
  SELECT * FROM VALUES
    (1,'Rahul','2022-01-10', 8, 45000),
    (2,'Priya','2023-06-01', 2,  6000),
    (3,'Arjun','2021-03-15',20, 90000)
  AS t(customer_id, name, signup_date, num_orders, total_spend)
""").collect()

# 3) Build features with the DataFrame API (lazy — runs on .show/.save) ------
df = session.table("customers")
features = (df
    .with_column("tenure_days", datediff("day", col("signup_date"), current_date()))
    .with_column("avg_order_value",
                 iff(col("num_orders") > 0,
                     col("total_spend") / col("num_orders"), lit(0)))
    .with_column("value_tier",
                 when(col("total_spend") >= 50000, lit("high"))
                 .when(col("total_spend") >= 10000, lit("mid"))
                 .otherwise(lit("low")))
    .with_column("is_active", (col("num_orders") >= 5).cast("int"))
    .select("customer_id", "name", "tenure_days",
            "avg_order_value", "value_tier", "is_active"))

features.show()   # ACTION → executes in Snowflake

# 4) Aggregate features (group-level) ---------------------------------------
tier_stats = (features
    .group_by("value_tier")
    .agg(count("*").alias("customers"),
         avg("avg_order_value").alias("avg_aov")))
tier_stats.show()

# 5) Persist the feature table — ready for ML (Project 10) -------------------
features.write.mode("overwrite").save_as_table("customer_features")
print("Saved FEAT_DEMO.PUBLIC.CUSTOMER_FEATURES:",
      session.table("customer_features").count(), "rows")

# 6) Inspect the pushed-down plan (no data pulled to client) -----------------
features.explain()

# Cleanup: session.sql("DROP DATABASE FEAT_DEMO").collect()
# ============================================================================
# LEARNED: Snowpark session, DataFrame ops (with_column, when/iff, group_by/agg),
# lazy vs actions, save_as_table, explain(). ZERO data egress — it all runs
# on Snowflake compute. Feeds Project 10's in-warehouse model.
# NEXT: Project 11 — RBAC security framework.
# ============================================================================
