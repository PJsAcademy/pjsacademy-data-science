-- ============================================================================
-- PJ's Academy · Snowflake Project 15 — CDC Data Vault 2.0  (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a Data Vault model (Hubs, Links, Satellites) with change
--   data capture via Streams — the enterprise gold standard for full history.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS dv_demo;
CREATE SCHEMA   IF NOT EXISTS dv_demo.public;
USE SCHEMA dv_demo.public;

-- Source (raw) system table --------------------------------------------------
CREATE OR REPLACE TABLE src_customers (
    customer_code STRING, name STRING, city STRING, updated_ts TIMESTAMP_NTZ
);

-- ---------------------------------------------------------------------------
-- DATA VAULT COMPONENTS
--   HUB       = unique business keys (the stable identity)
--   SATELLITE = descriptive attributes + full history of changes
--   LINK      = relationships between hubs (not shown: needs 2 hubs)
-- ---------------------------------------------------------------------------

-- HUB: one row per unique business key, with a hash key -----------------------
CREATE OR REPLACE TABLE hub_customer (
    customer_hk   STRING,               -- hash of the business key
    customer_code STRING,               -- business key
    load_ts       TIMESTAMP_NTZ,
    record_source STRING
);

-- SATELLITE: attributes + history (a new row on every change) ----------------
CREATE OR REPLACE TABLE sat_customer (
    customer_hk STRING,
    load_ts     TIMESTAMP_NTZ,
    hash_diff   STRING,                 -- hash of attributes → detect changes
    name        STRING,
    city        STRING,
    record_source STRING
);

-- STREAM on the source captures inserts/updates ------------------------------
CREATE OR REPLACE STREAM src_customers_stream ON TABLE src_customers;

-- ---------------------------------------------------------------------------
-- LOAD LOGIC (run after new data lands; wrap in a Task for automation)
-- ---------------------------------------------------------------------------

-- 1) Load the HUB — only NEW business keys (idempotent) ----------------------
CREATE OR REPLACE PROCEDURE load_vault()
RETURNS STRING LANGUAGE SQL AS
$$
BEGIN
  -- HUB: insert business keys not already present
  INSERT INTO hub_customer
  SELECT MD5(customer_code), customer_code, CURRENT_TIMESTAMP(), 'src_customers'
  FROM src_customers_stream s
  WHERE METADATA$ACTION = 'INSERT'
    AND NOT EXISTS (SELECT 1 FROM hub_customer h
                    WHERE h.customer_code = s.customer_code);

  -- SATELLITE: insert a new version only when attributes actually changed
  INSERT INTO sat_customer
  SELECT MD5(customer_code), CURRENT_TIMESTAMP(),
         MD5(name || '|' || city) AS hash_diff, name, city, 'src_customers'
  FROM src_customers_stream s
  WHERE s.name IS NOT NULL
    AND NOT EXISTS (
        SELECT 1 FROM sat_customer sat
        WHERE sat.customer_hk = MD5(s.customer_code)
          AND sat.hash_diff   = MD5(s.name || '|' || s.city));
  RETURN 'loaded';
END;
$$;

-- ---------------------------------------------------------------------------
-- TEST: insert, change, and see history build up
-- ---------------------------------------------------------------------------
INSERT INTO src_customers VALUES ('C1','Rahul','Mumbai', CURRENT_TIMESTAMP());
CALL load_vault();

UPDATE src_customers SET city='Pune', updated_ts=CURRENT_TIMESTAMP() WHERE customer_code='C1';
INSERT INTO src_customers SELECT 'C1','Rahul','Pune',CURRENT_TIMESTAMP();  -- change event
CALL load_vault();

-- The satellite now has TWO rows for C1 → full history of the city change
SELECT h.customer_code, s.name, s.city, s.load_ts
FROM hub_customer h JOIN sat_customer s USING (customer_hk)
ORDER BY s.load_ts;

-- Current view (latest row per customer) ------------------------------------
SELECT customer_hk, name, city
FROM sat_customer
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_hk ORDER BY load_ts DESC) = 1;

-- Cleanup: DROP DATABASE dv_demo;
-- ============================================================================
-- LEARNED: Data Vault (Hub/Satellite/Link), hash keys, hash_diff change
-- detection, Streams for CDC, and a stored procedure loader. Full auditable
-- history — every change ever, queryable. Add a Task to automate it.
-- NEXT: Project 16 — data sharing & Marketplace.
-- ============================================================================
