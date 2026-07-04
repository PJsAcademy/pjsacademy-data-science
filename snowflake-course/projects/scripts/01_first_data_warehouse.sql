-- ============================================================================
-- PJ's Academy · Snowflake Project 01 — Your First Data Warehouse  (Beginner)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a complete retail sales data warehouse (star schema),
--   load data, and run analytics queries.
-- HOW TO RUN: paste into a Snowflake worksheet and run top-to-bottom.
--   A free 30-day trial (app.snowflake.com/signup) has $400 of credits.
-- ============================================================================

-- 1) Compute: a small, cost-safe warehouse that auto-suspends when idle -------
CREATE WAREHOUSE IF NOT EXISTS analytics_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND   = 60        -- pause after 60s idle → you stop paying
  AUTO_RESUME    = TRUE
  INITIALLY_SUSPENDED = TRUE;

USE WAREHOUSE analytics_wh;

-- 2) Database + schema (a "star" schema: 1 fact table + dimension tables) -----
CREATE DATABASE IF NOT EXISTS retail_dw;
CREATE SCHEMA   IF NOT EXISTS retail_dw.star;
USE SCHEMA retail_dw.star;

-- 3) Dimension tables (the "who / what / when") ------------------------------
CREATE OR REPLACE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name        STRING,
    city        STRING,
    segment     STRING            -- e.g. Retail / Wholesale
);

CREATE OR REPLACE TABLE dim_product (
    product_id  INT PRIMARY KEY,
    name        STRING,
    category    STRING,
    price       NUMBER(10,2)
);

CREATE OR REPLACE TABLE dim_date (
    date_id  DATE PRIMARY KEY,
    year     INT,
    quarter  INT,
    month    INT,
    weekday  STRING
);

-- 4) Fact table (the measurable events — one row per sale) -------------------
CREATE OR REPLACE TABLE fact_sales (
    sale_id     INT PRIMARY KEY,
    customer_id INT,
    product_id  INT,
    date_id     DATE,
    quantity    INT,
    revenue     NUMBER(12,2)
);

-- 5) Load sample data (in real projects you'd COPY INTO from a stage) --------
INSERT INTO dim_customer VALUES
 (1,'Rahul','Mumbai','Retail'),(2,'Priya','Delhi','Wholesale'),
 (3,'Arjun','Bangalore','Retail'),(4,'Divya','Mumbai','Retail');

INSERT INTO dim_product VALUES
 (201,'Laptop','Electronics',55000),(202,'Mouse','Electronics',700),
 (203,'Desk','Furniture',8000),(204,'Chair','Furniture',4500);

INSERT INTO dim_date VALUES
 ('2023-06-01',2023,2,6,'Thursday'),('2023-06-10',2023,2,6,'Saturday'),
 ('2023-07-02',2023,3,7,'Sunday'),('2023-08-01',2023,3,8,'Tuesday');

INSERT INTO fact_sales VALUES
 (1,1,201,'2023-06-01',1,55000),(2,1,202,'2023-06-01',2,1400),
 (3,2,204,'2023-06-10',4,18000),(4,3,203,'2023-06-10',1,8000),
 (5,4,201,'2023-07-02',1,55000),(6,1,201,'2023-08-01',1,55000);

-- ============================================================================
-- ANALYTICS — the payoff. Join the fact to dimensions and answer questions.
-- ============================================================================

-- Q1) Total revenue by product category
SELECT p.category, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
-- Expected: Electronics 221400, Furniture 26000

-- Q2) Revenue by customer city
SELECT c.city, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC;

-- Q3) Monthly revenue trend
SELECT d.month, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.month
ORDER BY d.month;

-- Q4) Top customer by spend (window function preview)
SELECT c.name, SUM(f.revenue) AS spend,
       RANK() OVER (ORDER BY SUM(f.revenue) DESC) AS spend_rank
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.name;

-- 6) Cleanup (optional — saves storage on your trial)
-- DROP DATABASE retail_dw;
-- ALTER WAREHOUSE analytics_wh SUSPEND;

-- ============================================================================
-- WHAT YOU LEARNED: warehouses & auto-suspend, databases/schemas, star schema
-- (fact + dimensions), loading data, and analytical JOIN + GROUP BY queries.
-- NEXT: Project 07 — real-time streaming pipeline with Streams & Tasks.
-- ============================================================================
