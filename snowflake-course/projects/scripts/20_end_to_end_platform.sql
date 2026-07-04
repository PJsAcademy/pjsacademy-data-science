-- ============================================================================
-- PJ's Academy · Snowflake Project 20 — End-to-End Data Platform  (CAPSTONE)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a mini production platform tying together every skill:
--   ingestion (RAW) -> transform (Streams+Tasks) -> marts -> in-SQL logic ->
--   governance (masking) -> cost control (resource monitor).
-- This single project demonstrates every SnowPro Advanced domain.
-- HOW TO RUN: run top-to-bottom as ACCOUNTADMIN. ~5 min. Cleanup at the end.
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- 0) COST GUARDRAIL first — cap spend before anything else -------------------
CREATE RESOURCE MONITOR IF NOT EXISTS platform_budget
  WITH CREDIT_QUOTA = 10
  TRIGGERS ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;

CREATE WAREHOUSE IF NOT EXISTS platform_wh
  WAREHOUSE_SIZE='XSMALL' AUTO_SUSPEND=60 AUTO_RESUME=TRUE INITIALLY_SUSPENDED=TRUE;
ALTER WAREHOUSE platform_wh SET RESOURCE_MONITOR = platform_budget;
USE WAREHOUSE platform_wh;

CREATE DATABASE IF NOT EXISTS platform;
CREATE SCHEMA   IF NOT EXISTS platform.raw;
CREATE SCHEMA   IF NOT EXISTS platform.marts;
USE SCHEMA platform.raw;

-- 1) INGESTION LAYER — raw orders land here (would be Snowpipe from S3) ------
CREATE OR REPLACE TABLE raw.orders (
    order_id INT, customer STRING, email STRING,
    amount NUMBER(12,2), order_ts TIMESTAMP_NTZ
);

-- 2) TRANSFORM LAYER — Stream + Task clean into a curated table --------------
CREATE OR REPLACE TABLE marts.orders_clean (
    order_id INT, customer STRING, email STRING,
    amount NUMBER(12,2), order_ts TIMESTAMP_NTZ
);
CREATE OR REPLACE STREAM raw.orders_stream ON TABLE raw.orders;

CREATE OR REPLACE TASK raw.transform_task
  WAREHOUSE = platform_wh SCHEDULE = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_stream')
AS
  INSERT INTO marts.orders_clean
  SELECT order_id, TRIM(customer), LOWER(email), ABS(amount), order_ts
  FROM raw.orders_stream
  WHERE METADATA$ACTION='INSERT' AND amount IS NOT NULL;
ALTER TASK raw.transform_task RESUME;

-- 3) MART LAYER — a business-ready daily revenue view (Dynamic Table) --------
CREATE OR REPLACE DYNAMIC TABLE marts.daily_revenue
  TARGET_LAG = '1 minute'
  WAREHOUSE  = platform_wh
AS
  SELECT DATE(order_ts) AS order_day, COUNT(*) AS orders, SUM(amount) AS revenue
  FROM marts.orders_clean
  GROUP BY DATE(order_ts);

-- 4) GOVERNANCE LAYER — mask customer email in the curated table ------------
CREATE OR REPLACE MASKING POLICY marts.email_mask AS (v STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() = 'ACCOUNTADMIN' THEN v
       ELSE REGEXP_REPLACE(v, '.+@', '****@') END;
ALTER TABLE marts.orders_clean MODIFY COLUMN email SET MASKING POLICY marts.email_mask;

-- 5) IN-SQL LOGIC — a UDF for a simple "big order" flag ----------------------
CREATE OR REPLACE FUNCTION marts.is_big_order(amt NUMBER)
  RETURNS BOOLEAN AS $$ amt >= 50000 $$;

-- ============================================================================
-- 6) RUN THE PIPELINE — insert raw data, process, and see it flow through.
-- ============================================================================
INSERT INTO raw.orders VALUES
 (1,'Rahul','RAHUL@Mail.com', 55000, CURRENT_TIMESTAMP()),
 (2,'Priya ','priya@mail.com', 1400, CURRENT_TIMESTAMP()),
 (3,'Arjun','arjun@mail.com', -8000, CURRENT_TIMESTAMP());

EXECUTE TASK raw.transform_task;      -- process now (don't wait for schedule)

-- Curated data (email masked unless ACCOUNTADMIN), with the big-order flag
SELECT order_id, customer, email, amount,
       marts.is_big_order(amount) AS is_big_order
FROM marts.orders_clean
ORDER BY amount DESC;

-- Business mart (auto-maintained Dynamic Table)
SELECT * FROM marts.daily_revenue;

-- 7) OBSERVABILITY — task + cost visibility ---------------------------------
SELECT name, state, scheduled_time
FROM TABLE(platform.information_schema.task_history()) ORDER BY scheduled_time DESC LIMIT 5;

-- 8) CLEANUP -----------------------------------------------------------------
-- ALTER TASK raw.transform_task SUSPEND;
-- DROP DATABASE platform;
-- DROP RESOURCE MONITOR platform_budget;
-- DROP WAREHOUSE platform_wh;

-- ============================================================================
-- ARCHITECTURE:
--   RAW.orders --(Stream+Task)--> MARTS.orders_clean --(Dynamic Table)--> daily_revenue
--        with: masking (governance) + UDF (logic) + resource monitor (cost)
--
-- WHAT YOU PROVED: ingestion, CDC transformation, declarative marts, governance,
-- in-SQL logic, and cost control — a whole platform one person can run.
-- This is your portfolio centrepiece. Document it, screenshot the results,
-- and put it on your resume + GitHub.
-- ============================================================================
