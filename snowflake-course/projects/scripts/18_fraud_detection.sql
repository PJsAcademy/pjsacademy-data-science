-- ============================================================================
-- PJ's Academy · Snowflake Project 18 — Real-Time Fraud Detection  (Expert)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: transactions stream in, features are computed, a scoring
--   function flags suspicious ones, and a Task moves alerts — all inside
--   Snowflake, sub-minute. (Pairs with the Snowpark ML UDF from Project 10.)
-- ============================================================================

USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS fraud_demo;
CREATE SCHEMA   IF NOT EXISTS fraud_demo.public;
USE SCHEMA fraud_demo.public;

-- 1) Incoming transactions (would be Snowpipe/Streaming in production) -------
CREATE OR REPLACE TABLE transactions (
    txn_id INT, customer_id INT, amount NUMBER(12,2),
    country STRING, txn_ts TIMESTAMP_NTZ
);
CREATE OR REPLACE STREAM txn_stream ON TABLE transactions;

-- 2) Alert table -------------------------------------------------------------
CREATE OR REPLACE TABLE fraud_alerts (
    txn_id INT, customer_id INT, amount NUMBER(12,2),
    risk_score FLOAT, reason STRING, flagged_ts TIMESTAMP_NTZ
);

-- 3) A rule-based risk score (swap for the Project-10 ML UDF for real ML) ----
--    Real systems combine rules + an ML model. Here: transparent rules.
CREATE OR REPLACE FUNCTION risk_score(amount NUMBER, country STRING, cust_avg NUMBER)
RETURNS FLOAT AS
$$
  (IFF(amount > 100000, 0.4, 0)                       -- very large amount
 + IFF(country NOT IN ('IN'), 0.3, 0)                 -- foreign transaction
 + IFF(cust_avg > 0 AND amount > 5 * cust_avg, 0.4, 0)-- 5x the customer's norm
  )
$$;

-- 4) TASK — score new transactions the moment they arrive -------------------
CREATE OR REPLACE TASK score_task
  WAREHOUSE = analytics_wh
  SCHEDULE  = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('txn_stream')
AS
  INSERT INTO fraud_alerts
  SELECT s.txn_id, s.customer_id, s.amount,
         risk_score(s.amount, s.country, c.avg_amount) AS score,
         'auto-scored' AS reason, CURRENT_TIMESTAMP()
  FROM txn_stream s
  LEFT JOIN (SELECT customer_id, AVG(amount) AS avg_amount
             FROM transactions GROUP BY customer_id) c
         ON s.customer_id = c.customer_id
  WHERE s.METADATA$ACTION = 'INSERT'
    AND risk_score(s.amount, s.country, c.avg_amount) >= 0.6;  -- only flag risky
ALTER TASK score_task RESUME;

-- ---------------------------------------------------------------------------
-- TEST: seed history, then fire suspicious transactions
-- ---------------------------------------------------------------------------
INSERT INTO transactions VALUES        -- normal history for customer 1
 (1,1,2000,'IN',CURRENT_TIMESTAMP()),(2,1,2500,'IN',CURRENT_TIMESTAMP());

INSERT INTO transactions VALUES        -- suspicious new ones
 (3,1,150000,'IN',CURRENT_TIMESTAMP()),  -- huge + 5x norm
 (4,2,3000,'US',CURRENT_TIMESTAMP()),    -- foreign
 (5,1,1800,'IN',CURRENT_TIMESTAMP());    -- normal → NOT flagged

EXECUTE TASK score_task;                 -- process now

-- 5) Review the alerts -------------------------------------------------------
SELECT * FROM fraud_alerts ORDER BY risk_score DESC;
-- Expect txn 3 (huge/5x) and txn 4 (foreign) flagged; txn 5 not.

-- 6) Dashboard-ready summary -------------------------------------------------
SELECT DATE(flagged_ts) AS day, COUNT(*) AS alerts,
       ROUND(AVG(risk_score),2) AS avg_risk, MAX(amount) AS biggest
FROM fraud_alerts GROUP BY 1;

-- Cleanup: ALTER TASK score_task SUSPEND; DROP DATABASE fraud_demo;
-- ============================================================================
-- LEARNED: streaming ingestion + Stream, a scoring UDF, a Task that flags risky
-- transactions in near real-time, alert tables. Sub-minute fraud detection
-- fully inside Snowflake — no external ML infra. Swap risk_score() for the
-- Project-10 ML UDF for a real model.
-- NEXT: Project 19 — multi-region DR platform.
-- ============================================================================
