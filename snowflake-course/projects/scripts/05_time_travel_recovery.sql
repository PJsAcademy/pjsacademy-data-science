-- ============================================================================
-- PJ's Academy · Snowflake Project 05 — Time Travel Recovery System
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a "data undo" — recover from bad UPDATEs, DELETEs, and DROPs
--   using Time Travel (AT/BEFORE) and UNDROP.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS tt_demo;
CREATE SCHEMA   IF NOT EXISTS tt_demo.public;
USE SCHEMA tt_demo.public;

CREATE OR REPLACE TABLE accounts (id INT, name STRING, balance NUMBER(12,2));
INSERT INTO accounts VALUES (1,'Rahul',10000),(2,'Priya',25000),(3,'Arjun',5000);

-- 1) DISASTER: a bad UPDATE with no WHERE zeroes every balance --------------
UPDATE accounts SET balance = 0;     -- oops
SELECT * FROM accounts;              -- all zero

-- 2) RECOVER with Time Travel — query the table as it was 5 minutes ago -----
SELECT * FROM accounts AT(OFFSET => -60*5);   -- 5 minutes ago (original values)

-- 3) Or recover to just BEFORE the bad statement (grab its query_id from
--    the History tab, then:)
-- SELECT * FROM accounts BEFORE(STATEMENT => '<bad_update_query_id>');

-- 4) Restore the good data ---------------------------------------------------
CREATE OR REPLACE TABLE accounts_restored AS
  SELECT * FROM accounts AT(OFFSET => -60*5);
-- Or overwrite in place:
-- INSERT OVERWRITE INTO accounts SELECT * FROM accounts AT(OFFSET => -60*5);
SELECT * FROM accounts_restored;

-- 5) DROP disaster + UNDROP --------------------------------------------------
DROP TABLE accounts;
SELECT '...someone dropped the table...' AS status;
UNDROP TABLE accounts;               -- instantly back
SELECT COUNT(*) AS rows_back FROM accounts;

-- 6) Configure retention (Enterprise supports up to 90 days) ----------------
ALTER TABLE accounts SET DATA_RETENTION_TIME_IN_DAYS = 30;

-- 7) See what Time Travel is available -------------------------------------
SHOW TABLES LIKE 'accounts';   -- retention_time column shows the window

-- Cleanup: DROP DATABASE tt_demo;
-- ============================================================================
-- LEARNED: AT(OFFSET/TIMESTAMP), BEFORE(STATEMENT), UNDROP TABLE,
-- DATA_RETENTION_TIME_IN_DAYS. Fail-safe (7 more days) is support-only.
-- REAL WORLD: turns "we lost data" into "one query fixes it".
-- NEXT: Project 06 — zero-copy dev/test factory.
-- ============================================================================
