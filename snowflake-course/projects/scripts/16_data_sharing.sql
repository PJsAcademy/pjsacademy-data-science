-- ============================================================================
-- PJ's Academy · Snowflake Project 16 — Secure Data Sharing & Marketplace
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: share live data with a partner (no copy) and consume a
--   Marketplace dataset to enrich your own — via live joins.
-- HOW TO RUN: as ACCOUNTADMIN. Adding a real account to a share needs a
--   second Snowflake account; the share objects work on any account.
-- ============================================================================

USE ROLE ACCOUNTADMIN;
CREATE DATABASE IF NOT EXISTS analytics;
CREATE SCHEMA   IF NOT EXISTS analytics.public;
USE SCHEMA analytics.public;

CREATE OR REPLACE TABLE sales_summary (region STRING, revenue NUMBER(14,2));
INSERT INTO sales_summary VALUES ('South',500000),('North',350000);

-- 1) PROVIDER side — create a SHARE and grant objects to it ------------------
CREATE OR REPLACE SHARE partner_share;
GRANT USAGE  ON DATABASE analytics                 TO SHARE partner_share;
GRANT USAGE  ON SCHEMA   analytics.public          TO SHARE partner_share;
GRANT SELECT ON TABLE    analytics.public.sales_summary TO SHARE partner_share;

-- Add a consumer account (they then see your data LIVE — no copy, no ETL):
-- ALTER SHARE partner_share ADD ACCOUNTS = <consumer_account_locator>;
SHOW SHARES;

-- 2) SECURE VIEW — share only some rows/columns safely ----------------------
CREATE OR REPLACE SECURE VIEW analytics.public.sales_public AS
  SELECT region, revenue FROM sales_summary WHERE region <> 'Secret';
GRANT SELECT ON VIEW analytics.public.sales_public TO SHARE partner_share;

-- 3) READER ACCOUNT — for consumers who don't have Snowflake ----------------
-- CREATE MANAGED ACCOUNT partner_reader
--   ADMIN_NAME='padmin', ADMIN_PASSWORD='<strong>', TYPE=READER;
-- (You provision + pay for it; they log in and query your shared data.)

-- 4) CONSUMER side — mount a share you received into a database -------------
-- CREATE DATABASE from_partner FROM SHARE provider_account.their_share;
-- SELECT * FROM from_partner.public.some_table;   -- live, always current

-- 5) MARKETPLACE ENRICHMENT — join free public data to yours -----------------
-- After adding a free Marketplace listing (e.g. weather/demographics) it
-- appears as a database you can join live:
/*
SELECT s.region, s.revenue, w.avg_temp
FROM sales_summary s
JOIN weather_share.public.daily w ON s.region = w.region;
*/

-- Cleanup: DROP SHARE partner_share; DROP DATABASE analytics;
-- ============================================================================
-- LEARNED: CREATE SHARE + GRANT ... TO SHARE, secure views for sharing,
-- reader accounts (non-Snowflake consumers), consuming shares, and Marketplace
-- enrichment via live joins. Sharing = live query access, ZERO copying.
-- NEXT: Project 17 — Streamlit-in-Snowflake dashboard.
-- ============================================================================
