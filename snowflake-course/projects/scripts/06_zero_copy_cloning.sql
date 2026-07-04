-- ============================================================================
-- PJ's Academy · Snowflake Project 06 — Zero-Copy Dev/Test Factory
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: instant dev/test/staging environments cloned from production
--   with NO storage cost until they diverge. Plus point-in-time clones.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS production;
CREATE SCHEMA   IF NOT EXISTS production.public;
USE SCHEMA production.public;

CREATE OR REPLACE TABLE orders (id INT, customer STRING, amount NUMBER(12,2));
INSERT INTO orders VALUES (1,'Rahul',55000),(2,'Priya',1400),(3,'Arjun',8000);

-- 1) Clone a whole database in seconds — zero storage until changed ----------
CREATE OR REPLACE DATABASE dev_env  CLONE production;
CREATE OR REPLACE DATABASE test_env CLONE production;

-- Each clone is fully independent + writable. Verify dev has the data:
SELECT COUNT(*) AS dev_rows FROM dev_env.public.orders;

-- 2) Change the clone — production is untouched -----------------------------
INSERT INTO dev_env.public.orders VALUES (99,'DevTester',12345);
SELECT COUNT(*) AS dev_rows  FROM dev_env.public.orders;    -- 4
SELECT COUNT(*) AS prod_rows FROM production.public.orders; -- still 3

-- 3) Clone a single table (for a quick backup before a risky change) --------
CREATE OR REPLACE TABLE production.public.orders_backup CLONE production.public.orders;

-- 4) POINT-IN-TIME clone — combine cloning with Time Travel -----------------
-- Snapshot the table exactly as it was 10 minutes ago:
CREATE OR REPLACE TABLE orders_snapshot CLONE production.public.orders
  AT(OFFSET => -60*10);

-- 5) Self-service dev sandbox pattern (wrap in a stored proc for a team) -----
-- CREATE DATABASE sandbox_<username> CLONE production;  → per-developer full data

-- Cleanup ------------------------------------------------------------------
-- DROP DATABASE dev_env; DROP DATABASE test_env; DROP DATABASE production;
-- ============================================================================
-- LEARNED: CREATE ... CLONE (table/schema/database), independence of clones,
-- point-in-time cloning with AT(). Storage is only used for what changes.
-- REAL WORLD: every developer gets a full-prod sandbox instantly, for ~free.
-- NEXT: Project 08 — Snowpipe auto-ingestion.
-- ============================================================================
