# 🔬 Snowflake Advanced Tutorials — PJ's Academy

Deep, hands-on tutorials on the topics that separate senior Snowflake engineers from beginners. Each is copy-paste runnable in a Snowflake worksheet or Snowpark session.

---

## 1. Dynamic Tables — Declarative Pipelines

Dynamic Tables auto-refresh to a **target lag** — the modern replacement for many Streams+Tasks pipelines.

```sql
-- Raw → cleaned, refreshed automatically to within 1 minute of source
CREATE OR REPLACE DYNAMIC TABLE clean_orders
  TARGET_LAG = '1 minute'
  WAREHOUSE = etl_wh
AS
SELECT order_id, TRIM(customer) AS customer,
       ABS(amount) AS amount, order_ts
FROM raw_orders
WHERE amount IS NOT NULL;

-- Chain another dynamic table on top — it auto-maintains the DAG
CREATE OR REPLACE DYNAMIC TABLE daily_revenue
  TARGET_LAG = '5 minutes'
  WAREHOUSE = etl_wh
AS
SELECT DATE(order_ts) AS dt, SUM(amount) AS revenue
FROM clean_orders GROUP BY 1;

-- Inspect refresh history
SELECT * FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY())
ORDER BY refresh_start_time DESC;
```

**When to use vs Streams+Tasks:** Dynamic Tables for declarative transforms (you describe the result); Streams+Tasks for imperative/complex control flow. **Know both — it's a common exam and interview question.**

---

## 2. Performance Tuning Masterclass

### Diagnose with Query Profile programmatically
```sql
-- Find queries that spilled to disk (warehouse too small)
SELECT query_id, query_text, warehouse_size,
       bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage,
       execution_time/1000 AS secs
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE bytes_spilled_to_remote_storage > 0
  AND start_time > DATEADD(day,-7,CURRENT_DATE())
ORDER BY bytes_spilled_to_remote_storage DESC;
```

### Clustering — measure before you cluster
```sql
-- Check clustering health BEFORE adding a key
SELECT SYSTEM$CLUSTERING_INFORMATION('big_events', '(event_date)');
-- Add a clustering key only if average_depth is high & table is large
ALTER TABLE big_events CLUSTER BY (event_date);
```

### Search Optimization for point lookups
```sql
ALTER TABLE customers ADD SEARCH OPTIMIZATION ON EQUALITY(customer_id, email);
-- Great for needle-in-haystack lookups on huge tables
```

**Golden rules:** spilling → scale **up**; concurrency queuing → scale **out** (multi-cluster); selective filters on huge tables → **clustering** or **search optimization**; repeated aggregations → **materialized view**.

---

## 3. End-to-End RAG with Cortex (GenAI)

Build a question-answering system over your documents — entirely in Snowflake.

```sql
-- 1. Managed hybrid search over a knowledge base
CREATE OR REPLACE CORTEX SEARCH SERVICE kb_search
  ON content
  ATTRIBUTES title, url
  WAREHOUSE = search_wh
  TARGET_LAG = '1 hour'
AS SELECT content, title, url FROM knowledge_base;

-- 2. Retrieve + generate a grounded answer
WITH ctx AS (
  SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'kb_search',
    '{"query": "What is our refund policy?", "limit": 3}'
  ) AS results
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
  'llama3.1-70b',
  CONCAT('Answer using ONLY this context: ', results,
         '\nQuestion: What is our refund policy?')
) AS answer
FROM ctx;
```

**This is the exact pattern behind enterprise AI assistants** — retrieval grounds the LLM so it can't hallucinate.

---

## 4. Real-Time CDC Pipeline (Streams + Tasks)

```sql
CREATE STREAM orders_stream ON TABLE raw_orders SHOW_INITIAL_ROWS = TRUE;

CREATE OR REPLACE TASK process_orders
  WAREHOUSE = etl_wh
  SCHEDULE = '1 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('orders_stream')
AS
  MERGE INTO orders_summary t
  USING (SELECT DATE(order_ts) dt, SUM(amount) amt
         FROM orders_stream WHERE METADATA$ACTION = 'INSERT' GROUP BY 1) s
  ON t.dt = s.dt
  WHEN MATCHED THEN UPDATE SET amt = t.amt + s.amt
  WHEN NOT MATCHED THEN INSERT (dt, amt) VALUES (s.dt, s.amt);

ALTER TASK process_orders RESUME;   -- tasks start suspended
```

**Key gotcha:** tasks are created **suspended** — always `RESUME`. Use `METADATA$ACTION` / `METADATA$ISUPDATE` to distinguish inserts/updates/deletes in a stream.

---

## 5. In-Warehouse ML with Snowpark + Model Registry

```python
from snowflake.ml.modeling.ensemble import RandomForestClassifier
from snowflake.ml.registry import Registry

# Train distributed inside Snowflake
model = RandomForestClassifier(
    input_cols=["tenure","monthly_charges","contract"],
    label_cols=["churn"], output_cols=["prediction"])
model.fit(train_df)

# Register + version the model
reg = Registry(session)
mv = reg.log_model(model, model_name="churn_model", version_name="v1",
                   metrics={"roc_auc": 0.91})

# Now score in pure SQL:
#   SELECT churn_model!PREDICT(tenure, monthly_charges, contract) FROM customers;
```

**Zero data egress** — training, registry, and inference all live in Snowflake.

---

## 6. Cost Governance Automation

```sql
-- Org-wide budget guardrail
CREATE RESOURCE MONITOR org_budget WITH
  CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 90 PERCENT DO NOTIFY
    ON 100 PERCENT DO SUSPEND
    ON 110 PERCENT DO SUSPEND_IMMEDIATE;

-- Chargeback report: credits per team (by warehouse naming convention)
SELECT SPLIT_PART(warehouse_name,'_',1) AS team,
       SUM(credits_used) AS credits,
       ROUND(SUM(credits_used) * 3.0, 2) AS approx_usd   -- ~$3/credit
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time > DATEADD(month,-1,CURRENT_DATE())
GROUP BY 1 ORDER BY credits DESC;
```

---

## 7. Secure Data Sharing + Marketplace Enrichment

```sql
-- Share live data with a partner (no copy)
CREATE SHARE sales_share;
GRANT USAGE ON DATABASE analytics TO SHARE sales_share;
GRANT SELECT ON TABLE analytics.public.sales_summary TO SHARE sales_share;
ALTER SHARE sales_share ADD ACCOUNTS = partner_acct;

-- Enrich internal data with a free Marketplace dataset via a live join
SELECT s.region, s.revenue, w.avg_temp
FROM sales s
JOIN weather_marketplace.public.daily w
  ON s.region = w.region AND s.dt = w.date;
```

---

## 🎯 How to Practice
Spin up a **free Snowflake trial** (30 days, $400 credits), create the objects above, and run each tutorial. Hands-on beats reading every time — and these are the exact scenarios the Advanced certs test.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
