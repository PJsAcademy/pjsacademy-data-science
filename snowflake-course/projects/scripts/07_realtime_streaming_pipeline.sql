-- ============================================================================
-- PJ's Academy · Snowflake Project 07 — Real-Time Streaming Pipeline (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a near-real-time ELT pipeline. New orders land in a RAW table;
--   Streams capture the changes; Tasks automatically clean & aggregate them
--   every minute — no external orchestrator (Airflow etc.) needed.
-- HOW TO RUN: run sections 1–5 once. Then run section 6 repeatedly to simulate
--   new data arriving, and watch the summary table update.
-- ============================================================================

USE WAREHOUSE analytics_wh;          -- from Project 01 (or create one)
CREATE DATABASE IF NOT EXISTS streaming_demo;
CREATE SCHEMA   IF NOT EXISTS streaming_demo.public;
USE SCHEMA streaming_demo.public;

-- 1) Landing (RAW) table — where raw orders arrive --------------------------
CREATE OR REPLACE TABLE raw_orders (
    order_id   INT,
    customer   STRING,
    amount     NUMBER(12,2),
    order_ts   TIMESTAMP_NTZ
);

-- 2) Target tables — cleaned rows + a daily summary -------------------------
CREATE OR REPLACE TABLE clean_orders (
    order_id   INT,
    customer   STRING,
    amount     NUMBER(12,2),
    order_ts   TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE daily_summary (
    order_day  DATE,
    total_rev  NUMBER(14,2),
    order_cnt  INT
);

-- 3) STREAM — tracks INSERTs/UPDATEs/DELETEs on raw_orders (Snowflake CDC) ---
CREATE OR REPLACE STREAM raw_orders_stream ON TABLE raw_orders;

-- 4) TASK 1 — clean new rows whenever the stream has data -------------------
CREATE OR REPLACE TASK clean_task
  WAREHOUSE = analytics_wh
  SCHEDULE  = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('raw_orders_stream')   -- only runs if new data
AS
  INSERT INTO clean_orders
  SELECT order_id, TRIM(customer), ABS(amount), order_ts
  FROM raw_orders_stream
  WHERE METADATA$ACTION = 'INSERT'      -- only newly inserted rows
    AND amount IS NOT NULL;

-- 5) TASK 2 — rebuild the daily summary AFTER cleaning (a task DAG) ----------
CREATE OR REPLACE TASK summary_task
  WAREHOUSE = analytics_wh
  AFTER clean_task                       -- chains after clean_task = a pipeline
AS
  MERGE INTO daily_summary d
  USING (
      SELECT DATE(order_ts) AS order_day,
             SUM(amount)     AS rev,
             COUNT(*)        AS cnt
      FROM clean_orders
      GROUP BY DATE(order_ts)
  ) s
  ON d.order_day = s.order_day
  WHEN MATCHED THEN UPDATE SET total_rev = s.rev, order_cnt = s.cnt
  WHEN NOT MATCHED THEN INSERT (order_day, total_rev, order_cnt)
       VALUES (s.order_day, s.rev, s.cnt);

-- Tasks are created SUSPENDED — resume the child first, then the root.
ALTER TASK summary_task RESUME;
ALTER TASK clean_task   RESUME;

-- ============================================================================
-- 6) SIMULATE LIVE DATA — run this block a few times, ~1 min apart.
--    The tasks will auto-process it. (Or run tasks manually with EXECUTE TASK.)
-- ============================================================================
INSERT INTO raw_orders VALUES
 (1,'Rahul', 55000, CURRENT_TIMESTAMP()),
 (2,'Priya ', 1400, CURRENT_TIMESTAMP()),   -- note trailing space → TRIM fixes it
 (3,'Arjun', -8000, CURRENT_TIMESTAMP());   -- negative → ABS fixes it

-- To process immediately without waiting for the schedule:
EXECUTE TASK clean_task;   -- runs clean_task, then summary_task via the DAG

-- 7) Inspect results ---------------------------------------------------------
SELECT * FROM clean_orders  ORDER BY order_ts DESC;   -- cleaned rows
SELECT * FROM daily_summary ORDER BY order_day DESC;  -- rolled-up totals

-- Monitor task runs
SELECT name, state, scheduled_time, error_message
FROM TABLE(streaming_demo.information_schema.task_history())
ORDER BY scheduled_time DESC LIMIT 10;

-- 8) Cleanup -----------------------------------------------------------------
-- ALTER TASK clean_task SUSPEND; ALTER TASK summary_task SUSPEND;
-- DROP DATABASE streaming_demo;

-- ============================================================================
-- WHAT YOU LEARNED: Streams (CDC), Tasks (scheduled + chained DAG),
-- SYSTEM$STREAM_HAS_DATA, METADATA$ACTION, MERGE upserts, task_history.
-- KEY GOTCHA: tasks start SUSPENDED — always RESUME (child before root).
-- NEXT: Project 10 — deploy an ML model as a SQL function (Snowpark).
-- ============================================================================
