-- ============================================================================
-- PJ's Academy · Snowflake Project 08 — Snowpipe Auto-Ingestion  (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: files dropped in cloud storage auto-load within seconds via
--   Snowpipe + event notifications — serverless, no warehouse, no schedule.
-- HOW TO RUN: the pipe/notification steps require an external stage (S3/Azure/
--   GCS) with event notifications. The manual-refresh path works on any stage.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS pipe_demo;
CREATE SCHEMA   IF NOT EXISTS pipe_demo.public;
USE SCHEMA pipe_demo.public;

CREATE OR REPLACE FILE FORMAT ff_csv TYPE='CSV' SKIP_HEADER=1;
CREATE OR REPLACE TABLE sales (id INT, product STRING, amount NUMBER(12,2));

-- 1) External stage pointing to your bucket (fill in your details) ----------
/*
CREATE OR REPLACE STAGE ext_stage
  URL = 's3://my-bucket/incoming/'
  STORAGE_INTEGRATION = my_s3_integration     -- created once by an admin
  FILE_FORMAT = ff_csv;
*/

-- 2) CREATE the PIPE with AUTO_INGEST — Snowflake loads new files on arrival -
/*
CREATE OR REPLACE PIPE sales_pipe
  AUTO_INGEST = TRUE
AS
  COPY INTO sales FROM @ext_stage FILE_FORMAT = ff_csv;

-- Get the notification channel ARN and wire it to your bucket's events
-- (S3 -> SNS/SQS, Azure Event Grid, or GCS Pub/Sub):
SELECT SYSTEM$PIPE_STATUS('sales_pipe');
SHOW PIPES;   -- copy the notification_channel value into your cloud event config
*/

-- 3) MANUAL alternative (works on any stage, no events) — call REFRESH ------
CREATE OR REPLACE STAGE int_stage FILE_FORMAT = ff_csv;
-- PUT file:///path/sales1.csv @int_stage;   (from SnowSQL)
CREATE OR REPLACE PIPE sales_pipe_manual AS
  COPY INTO sales FROM @int_stage FILE_FORMAT = ff_csv;
-- ALTER PIPE sales_pipe_manual REFRESH;      -- ingest files currently staged

-- 4) MONITOR ingestion -------------------------------------------------------
-- SELECT SYSTEM$PIPE_STATUS('sales_pipe');            -- pending/executed counts
SELECT * FROM TABLE(pipe_demo.information_schema.copy_history(
    table_name=>'SALES', start_time=>DATEADD(hour,-1,CURRENT_TIMESTAMP())));

-- 5) Alert on ingestion lag (a monitoring pattern) --------------------------
-- Compare file arrival time vs load time; alert if the gap grows.

-- Cleanup: DROP DATABASE pipe_demo;
-- ============================================================================
-- LEARNED: external stages + storage integration, CREATE PIPE AUTO_INGEST,
-- SYSTEM$PIPE_STATUS, event notifications, ALTER PIPE REFRESH, copy_history.
-- KEY FACT: Snowpipe is SERVERLESS (no warehouse) and continuous.
-- NEXT: Project 09 — Snowpark feature-engineering pipeline.
-- ============================================================================
