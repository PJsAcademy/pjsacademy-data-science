-- ============================================================================
-- PJ's Academy · Snowflake Project 12 — Data Masking & Compliance (Advanced)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: India DPDP-style PII protection — dynamic column masking
--   (PAN, Aadhaar, email) + row-level security, so unauthorised roles never
--   see sensitive data. This is exactly what banks/fintechs require.
-- HOW TO RUN: run as ACCOUNTADMIN (or a role with the needed privileges).
-- ============================================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE analytics_wh;
CREATE DATABASE IF NOT EXISTS governance_demo;
CREATE SCHEMA   IF NOT EXISTS governance_demo.public;
USE SCHEMA governance_demo.public;

-- 1) Roles: a privileged compliance role vs a regular analyst ---------------
CREATE ROLE IF NOT EXISTS compliance_role;
CREATE ROLE IF NOT EXISTS analyst_role;
GRANT USAGE ON DATABASE governance_demo TO ROLE compliance_role;
GRANT USAGE ON DATABASE governance_demo TO ROLE analyst_role;
GRANT USAGE ON SCHEMA governance_demo.public TO ROLE compliance_role;
GRANT USAGE ON SCHEMA governance_demo.public TO ROLE analyst_role;

-- 2) Sensitive customer table -----------------------------------------------
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    name        STRING,
    email       STRING,
    pan         STRING,          -- Indian tax ID (like ABCDE1234F)
    aadhaar     STRING,          -- 12-digit national ID
    region      STRING
);
INSERT INTO customers VALUES
 (1,'Rahul','rahul@mail.com','ABCDE1234F','1234-5678-9012','South'),
 (2,'Priya','priya@mail.com','PQRST5678K','2345-6789-0123','North');

GRANT SELECT ON TABLE customers TO ROLE compliance_role;
GRANT SELECT ON TABLE customers TO ROLE analyst_role;

-- 3) MASKING POLICIES — compliance sees real values; everyone else masked ---
CREATE OR REPLACE MASKING POLICY pan_mask AS (val STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('COMPLIANCE_ROLE','ACCOUNTADMIN') THEN val
       ELSE 'XXXXX' || RIGHT(val, 4) END;          -- ABCDE1234F -> XXXXX234F

CREATE OR REPLACE MASKING POLICY aadhaar_mask AS (val STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('COMPLIANCE_ROLE','ACCOUNTADMIN') THEN val
       ELSE 'XXXX-XXXX-' || RIGHT(val, 4) END;

CREATE OR REPLACE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('COMPLIANCE_ROLE','ACCOUNTADMIN') THEN val
       ELSE REGEXP_REPLACE(val, '.+@', '****@') END;  -- rahul@mail.com -> ****@mail.com

-- Attach the policies to the columns
ALTER TABLE customers MODIFY COLUMN pan     SET MASKING POLICY pan_mask;
ALTER TABLE customers MODIFY COLUMN aadhaar SET MASKING POLICY aadhaar_mask;
ALTER TABLE customers MODIFY COLUMN email   SET MASKING POLICY email_mask;

-- 4) ROW ACCESS POLICY — analysts only see their own region ------------------
-- Map a role to the region(s) it may see
CREATE OR REPLACE TABLE role_region_map (role_name STRING, region STRING);
INSERT INTO role_region_map VALUES ('ANALYST_ROLE','South');  -- analyst = South only

CREATE OR REPLACE ROW ACCESS POLICY region_policy AS (region STRING) RETURNS BOOLEAN ->
  CURRENT_ROLE() IN ('COMPLIANCE_ROLE','ACCOUNTADMIN')        -- full access
  OR EXISTS (SELECT 1 FROM role_region_map m
             WHERE m.role_name = CURRENT_ROLE() AND m.region = region);

ALTER TABLE customers ADD ROW ACCESS POLICY region_policy ON (region);

-- ============================================================================
-- 5) TEST IT — switch roles and see the difference.
-- ============================================================================

-- As COMPLIANCE: sees everything, unmasked, all regions
USE ROLE compliance_role;
SELECT * FROM customers;      -- full PAN/Aadhaar/email, both rows

-- As ANALYST: PII masked AND only the South-region row visible
USE ROLE analyst_role;
SELECT * FROM customers;      -- pan=XXXXX234F, email=****@mail.com, only Rahul (South)

USE ROLE ACCOUNTADMIN;

-- 6) Audit — who accessed what (needs Enterprise; illustrative) --------------
-- SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY ORDER BY query_start_time DESC;

-- 7) Cleanup -----------------------------------------------------------------
-- DROP DATABASE governance_demo;
-- DROP ROLE compliance_role; DROP ROLE analyst_role;

-- ============================================================================
-- WHAT YOU LEARNED: dynamic masking policies (role-aware), row access policies
-- with a mapping table, and how one policy protects a column across ALL queries.
-- REAL WORLD: this is the exact pattern banks use for DPDP/GDPR compliance.
-- NEXT: Project 20 — end-to-end platform tying ingestion→ML→governance together.
-- ============================================================================
