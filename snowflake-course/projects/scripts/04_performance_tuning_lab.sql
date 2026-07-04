-- ============================================================================
-- PJ's Academy · Snowflake Project 04 — Performance Tuning Lab  (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: make slow queries fast. Clustering, search optimization,
--   materialized views, result cache — measured before/after.
-- HOW TO RUN: creates a larger table via GENERATOR so tuning is observable.
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS perf_demo;
CREATE SCHEMA   IF NOT EXISTS perf_demo.public;
USE SCHEMA perf_demo.public;

-- 1) Generate a big-ish table (5M rows) to make effects visible -------------
CREATE OR REPLACE TABLE events AS
SELECT SEQ8()                                   AS event_id,
       UNIFORM(1, 100000, RANDOM())             AS user_id,
       DATEADD('day', UNIFORM(0,730,RANDOM()), '2022-01-01') AS event_date,
       UNIFORM(1, 500, RANDOM())                AS product_id,
       UNIFORM(10, 5000, RANDOM())              AS amount
FROM TABLE(GENERATOR(ROWCOUNT => 5000000));

-- 2) BASELINE — a selective query. Note the time + check the Query Profile. -
SELECT COUNT(*), SUM(amount)
FROM events
WHERE event_date = '2023-06-15';
-- Open the Query Profile (Snowsight): look at "Partitions scanned / total".

-- 3) Check clustering health BEFORE adding a key ----------------------------
SELECT SYSTEM$CLUSTERING_INFORMATION('events', '(event_date)');

-- 4) Add a CLUSTERING KEY so date-filtered queries prune better -------------
ALTER TABLE events CLUSTER BY (event_date);
-- Reclustering is automatic + background; give it a moment on large tables.

-- Re-run the baseline query — partitions scanned should drop:
SELECT COUNT(*), SUM(amount) FROM events WHERE event_date = '2023-06-15';

-- 5) SEARCH OPTIMIZATION — for point lookups on high-cardinality columns ----
ALTER TABLE events ADD SEARCH OPTIMIZATION ON EQUALITY(user_id);
-- Now needle-in-haystack lookups are fast:
SELECT * FROM events WHERE user_id = 42137;

-- 6) MATERIALIZED VIEW — precompute an expensive aggregation (Enterprise+) --
CREATE OR REPLACE MATERIALIZED VIEW daily_totals AS
SELECT event_date, COUNT(*) AS cnt, SUM(amount) AS revenue
FROM events GROUP BY event_date;
-- Queries against daily_totals are instant + auto-maintained.
SELECT * FROM daily_totals WHERE event_date = '2023-06-15';

-- 7) RESULT CACHE — re-run an identical query; second run is ~instant, 0 compute
SELECT SUM(amount) FROM events;   -- run twice; second hits the result cache (24h)

-- 8) Find your most expensive queries (tuning targets) ----------------------
SELECT query_text, execution_time/1000 AS secs,
       partitions_scanned, partitions_total,
       bytes_spilled_to_local_storage
FROM TABLE(perf_demo.information_schema.query_history())
ORDER BY execution_time DESC LIMIT 10;

-- Cleanup: DROP DATABASE perf_demo;
-- ============================================================================
-- LEARNED: Query Profile, SYSTEM$CLUSTERING_INFORMATION, clustering keys,
-- Search Optimization Service, materialized views, result cache, query_history.
-- RULES: spilling -> scale up; concurrency -> scale out; selective filters on
-- big tables -> clustering/search optimization; repeated aggregates -> MV.
-- NEXT: Project 05 — Time Travel recovery.
-- ============================================================================
