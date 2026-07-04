-- ============================================================================
-- PJ's Academy · Snowflake Project 11 — RBAC Security Framework  (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a proper enterprise role hierarchy — functional roles +
--   access roles, least-privilege, future grants, and an audit query.
-- HOW TO RUN: as ACCOUNTADMIN / SECURITYADMIN.
-- ============================================================================

USE ROLE SECURITYADMIN;   -- best practice for managing grants
CREATE DATABASE IF NOT EXISTS company;
CREATE SCHEMA   IF NOT EXISTS company.analytics;

-- 1) ACCESS ROLES — grant privileges on objects (the "what") ----------------
CREATE ROLE IF NOT EXISTS ar_analytics_read;
CREATE ROLE IF NOT EXISTS ar_analytics_write;

GRANT USAGE ON DATABASE company TO ROLE ar_analytics_read;
GRANT USAGE ON SCHEMA company.analytics TO ROLE ar_analytics_read;
GRANT SELECT ON ALL TABLES IN SCHEMA company.analytics TO ROLE ar_analytics_read;
-- FUTURE grant: auto-applies to tables created LATER (key admin tool)
GRANT SELECT ON FUTURE TABLES IN SCHEMA company.analytics TO ROLE ar_analytics_read;

GRANT ar_analytics_read TO ROLE ar_analytics_write;   -- write inherits read
GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA company.analytics
      TO ROLE ar_analytics_write;

-- 2) FUNCTIONAL ROLES — map to job functions (the "who") --------------------
CREATE ROLE IF NOT EXISTS fr_analyst;
CREATE ROLE IF NOT EXISTS fr_engineer;

GRANT ar_analytics_read  TO ROLE fr_analyst;    -- analysts read
GRANT ar_analytics_write TO ROLE fr_engineer;   -- engineers read+write

-- 3) Give functional roles a warehouse to run queries ----------------------
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE fr_analyst;
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE fr_engineer;

-- 4) Put functional roles under SYSADMIN (best-practice hierarchy) ----------
GRANT ROLE fr_analyst  TO ROLE SYSADMIN;
GRANT ROLE fr_engineer TO ROLE SYSADMIN;

-- 5) Assign roles to users ---------------------------------------------------
-- GRANT ROLE fr_analyst TO USER some_analyst;
-- GRANT ROLE fr_engineer TO USER some_engineer;

-- 6) TEST — create a table as engineer, read it as analyst ------------------
USE ROLE fr_engineer; USE WAREHOUSE analytics_wh;
CREATE OR REPLACE TABLE company.analytics.metrics (day DATE, value NUMBER);
INSERT INTO company.analytics.metrics VALUES ('2023-06-01', 100);

USE ROLE fr_analyst;
SELECT * FROM company.analytics.metrics;   -- works (future grant gave read)
-- INSERT INTO company.analytics.metrics VALUES ('2023-06-02', 200);  -- DENIED

-- 7) AUDIT — what can each role do? -----------------------------------------
USE ROLE SECURITYADMIN;
SHOW GRANTS TO ROLE fr_analyst;
SHOW GRANTS ON SCHEMA company.analytics;
-- Map users -> roles:
-- SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS WHERE deleted_on IS NULL;

-- Cleanup: DROP DATABASE company; DROP ROLE fr_analyst; ... etc.
-- ============================================================================
-- LEARNED: access vs functional roles, role inheritance, FUTURE grants,
-- least-privilege design, SHOW GRANTS auditing. Never use ACCOUNTADMIN daily.
-- NEXT: Project 13 — cost optimization dashboard.
-- ============================================================================
