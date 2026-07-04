-- ============================================================================
-- PJ's Academy · Snowflake Project 13 — Cost Optimization Dashboard (FinOps)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: FinOps queries to track credit usage, find expensive queries
--   and idle warehouses, plus a resource monitor to cap spend.
-- HOW TO RUN: as ACCOUNTADMIN (ACCOUNT_USAGE needs the privilege). Data has
--   ~45 min latency and up to 365 days of history.
-- ============================================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE analytics_wh;

-- 1) HARD BUDGET GUARDRAIL — cap monthly credits ----------------------------
CREATE OR REPLACE RESOURCE MONITOR monthly_budget
  WITH CREDIT_QUOTA = 100
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 75 PERCENT DO NOTIFY
           ON 90 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND
           ON 110 PERCENT DO SUSPEND_IMMEDIATE;
ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = monthly_budget;

-- 2) Credits by warehouse (last 30 days) — who is spending? ------------------
SELECT warehouse_name,
       ROUND(SUM(credits_used), 2)            AS credits,
       ROUND(SUM(credits_used) * 3.0, 2)      AS approx_usd   -- ~$3/credit est.
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time > DATEADD(day, -30, CURRENT_DATE())
GROUP BY warehouse_name
ORDER BY credits DESC;

-- 3) Most expensive queries (tuning targets) --------------------------------
SELECT query_id, LEFT(query_text, 80) AS query,
       warehouse_name,
       ROUND(total_elapsed_time/1000, 1) AS secs,
       ROUND(credits_used_cloud_services, 4) AS cloud_credits,
       partitions_scanned, partitions_total
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time > DATEADD(day, -7, CURRENT_DATE())
ORDER BY total_elapsed_time DESC
LIMIT 20;

-- 4) Idle-but-costly warehouses (low queries, high credits) -----------------
WITH usage AS (
  SELECT warehouse_name, SUM(credits_used) AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
  WHERE start_time > DATEADD(day,-30,CURRENT_DATE()) GROUP BY 1
), q AS (
  SELECT warehouse_name, COUNT(*) AS queries
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE start_time > DATEADD(day,-30,CURRENT_DATE()) GROUP BY 1
)
SELECT u.warehouse_name, u.credits, COALESCE(q.queries,0) AS queries,
       ROUND(u.credits / NULLIF(q.queries,0), 3) AS credits_per_query
FROM usage u LEFT JOIN q USING (warehouse_name)
ORDER BY credits_per_query DESC NULLS LAST;

-- 5) Storage cost by database -----------------------------------------------
SELECT database_name,
       ROUND(AVG(average_database_bytes)/POWER(1024,3), 2) AS avg_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
WHERE usage_date > DATEADD(day,-30,CURRENT_DATE())
GROUP BY database_name ORDER BY avg_gb DESC;

-- 6) Cost anomaly detector — days that spiked vs the 30-day average ----------
WITH daily AS (
  SELECT DATE(start_time) AS d, SUM(credits_used) AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
  WHERE start_time > DATEADD(day,-30,CURRENT_DATE()) GROUP BY 1
)
SELECT d, credits,
       ROUND(AVG(credits) OVER (), 2) AS avg_credits,
       IFF(credits > 1.5 * AVG(credits) OVER (), '⚠️ SPIKE', 'ok') AS flag
FROM daily ORDER BY d DESC;

-- ============================================================================
-- LEARNED: resource monitors (NOTIFY/SUSPEND), ACCOUNT_USAGE views
-- (WAREHOUSE_METERING_HISTORY, QUERY_HISTORY, STORAGE), cost attribution,
-- and a simple anomaly detector. This is the skill that gets you promoted.
-- NEXT: Project 14 — dbt + Snowflake transformations.
-- ============================================================================
