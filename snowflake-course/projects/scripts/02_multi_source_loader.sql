-- ============================================================================
-- PJ's Academy · Snowflake Project 02 — Multi-Source Data Loader  (Beginner+)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: load data from CSV, JSON and Parquet into one schema, with
--   file formats, error handling, and a rejection report.
-- HOW TO RUN: sections that COPY from a real stage need files in cloud storage;
--   the inline INSERTs let you learn the mechanics without external files.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS loader_demo;
CREATE SCHEMA   IF NOT EXISTS loader_demo.public;
USE SCHEMA loader_demo.public;

-- 1) FILE FORMATS — one per source type -------------------------------------
CREATE OR REPLACE FILE FORMAT ff_csv
  TYPE='CSV' FIELD_DELIMITER=',' SKIP_HEADER=1
  NULL_IF=('NULL','null','') FIELD_OPTIONALLY_ENCLOSED_BY='"';

CREATE OR REPLACE FILE FORMAT ff_json  TYPE='JSON' STRIP_OUTER_ARRAY=TRUE;
CREATE OR REPLACE FILE FORMAT ff_parquet TYPE='PARQUET';

-- 2) A named internal stage to hold uploaded files --------------------------
CREATE OR REPLACE STAGE my_stage;
-- Upload from SnowSQL:  PUT file:///path/sales.csv @my_stage;

-- 3) Target table + a rejection table for bad rows --------------------------
CREATE OR REPLACE TABLE sales (
    sale_id INT, product STRING, amount NUMBER(12,2), sale_date DATE
);
CREATE OR REPLACE TABLE sales_rejects (
    error STRING, line INT, raw STRING
);

-- 4) COPY INTO with error handling ------------------------------------------
--    ON_ERROR='CONTINUE' skips bad rows and keeps the rest.
--    VALIDATION_MODE lets you dry-run to preview errors first.
/*
COPY INTO sales
  FROM @my_stage/sales.csv
  FILE_FORMAT = ff_csv
  ON_ERROR = 'CONTINUE';

-- Preview what WOULD fail, without loading:
COPY INTO sales FROM @my_stage/sales.csv FILE_FORMAT=ff_csv
  VALIDATION_MODE='RETURN_ERRORS';
*/

-- 5) Learn the mechanics without external files (inline) ---------------------
INSERT INTO sales VALUES
 (1,'Laptop',55000,'2023-06-01'),(2,'Mouse',700,'2023-06-02');

-- 6) Load semi-structured JSON into a VARIANT, then query it ----------------
CREATE OR REPLACE TABLE raw_json (v VARIANT);
INSERT INTO raw_json
  SELECT PARSE_JSON('{"id":10,"product":"Desk","price":8000,"tags":["wood","office"]}');

SELECT v:id::INT        AS id,
       v:product::STRING AS product,
       v:price::NUMBER   AS price,
       v:tags[0]::STRING AS first_tag
FROM raw_json;

-- 7) Reconciliation report — loaded vs rejected -----------------------------
SELECT (SELECT COUNT(*) FROM sales)         AS loaded_rows,
       (SELECT COUNT(*) FROM sales_rejects) AS rejected_rows;

-- 8) See the load history (what COPY did) -----------------------------------
SELECT * FROM TABLE(loader_demo.information_schema.copy_history(
    table_name=>'SALES', start_time=>DATEADD(hour,-1,CURRENT_TIMESTAMP())));

-- Cleanup: DROP DATABASE loader_demo;
-- ============================================================================
-- LEARNED: file formats (CSV/JSON/Parquet), stages, COPY INTO + ON_ERROR +
-- VALIDATION_MODE, VARIANT for JSON, copy_history auditing.
-- NEXT: Project 03 — deep semi-structured JSON analytics.
-- ============================================================================
