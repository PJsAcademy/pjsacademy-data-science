-- ============================================================================
-- PJ's Academy · Snowflake Project 03 — Semi-Structured JSON Analytics
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: analyse nested JSON e-commerce events with VARIANT, path
--   notation, and LATERAL FLATTEN — as fast as structured tables, no ETL.
-- HOW TO RUN: top-to-bottom in a worksheet.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS json_demo;
CREATE SCHEMA   IF NOT EXISTS json_demo.public;
USE SCHEMA json_demo.public;

-- 1) Raw events as VARIANT (a real feed would COPY these from JSON files) ----
CREATE OR REPLACE TABLE events (raw VARIANT);
INSERT INTO events
SELECT PARSE_JSON(column1) FROM VALUES
('{"user":"rahul","type":"purchase","ts":"2023-06-01T10:00:00",
   "cart":[{"sku":"A1","product":"Laptop","price":55000,"qty":1},
           {"sku":"A2","product":"Mouse","price":700,"qty":2}]}'),
('{"user":"priya","type":"purchase","ts":"2023-06-01T11:30:00",
   "cart":[{"sku":"B1","product":"Desk","price":8000,"qty":1}]}'),
('{"user":"arjun","type":"view","ts":"2023-06-01T12:00:00",
   "cart":[]}');

-- 2) Access nested fields with path notation + :: casting -------------------
SELECT raw:user::STRING       AS user_id,
       raw:type::STRING       AS event_type,
       raw:ts::TIMESTAMP      AS event_time,
       ARRAY_SIZE(raw:cart)   AS items_in_cart
FROM events;

-- 3) LATERAL FLATTEN — explode the cart array into one row per item ---------
SELECT e.raw:user::STRING     AS user_id,
       item.value:sku::STRING AS sku,
       item.value:product::STRING AS product,
       item.value:price::NUMBER   AS price,
       item.value:qty::INT        AS qty,
       item.value:price::NUMBER * item.value:qty::INT AS line_total
FROM events e,
     LATERAL FLATTEN(input => e.raw:cart) item;

-- 4) Aggregate over the flattened data — revenue per product ----------------
SELECT item.value:product::STRING AS product,
       SUM(item.value:price::NUMBER * item.value:qty::INT) AS revenue
FROM events e, LATERAL FLATTEN(input => e.raw:cart) item
WHERE e.raw:type::STRING = 'purchase'
GROUP BY product
ORDER BY revenue DESC;

-- 5) Useful semi-structured functions ---------------------------------------
SELECT OBJECT_KEYS(raw)  AS top_level_keys,   -- what keys exist
       IS_ARRAY(raw:cart) AS cart_is_array
FROM events LIMIT 1;

-- Cleanup: DROP DATABASE json_demo;
-- ============================================================================
-- LEARNED: VARIANT, path notation (col:field.sub::type), ARRAY_SIZE,
-- LATERAL FLATTEN (arrays -> rows), OBJECT_KEYS. Query JSON like a table.
-- NEXT: Project 04 — performance tuning lab.
-- ============================================================================
