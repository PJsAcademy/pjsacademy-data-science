-- ============================================================================
-- PJ's Academy · Snowflake Project 19 — Multi-Region DR Platform  (Expert)
-- ----------------------------------------------------------------------------
-- WHAT YOU BUILD: a disaster-recovery design with cross-region replication and
--   automated failover using replication + failover groups.
-- HOW TO RUN: requires Business Critical edition + a second account in another
--   region (features are account-level). Read as an architecture blueprint;
--   the commands are the real syntax you'd use.
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- ---------------------------------------------------------------------------
-- CONCEPTS
--   Replication group  = replicate DATABASES to another account/region.
--   Failover group     = replicate databases + ACCOUNT OBJECTS (roles, users,
--                        warehouses, policies) AND allow failover (promotion).
--   RPO = how much data you can lose (replication lag).
--   RTO = how long to recover (time to promote the secondary).
-- ---------------------------------------------------------------------------

-- 1) PRIMARY account — create a FAILOVER GROUP of what to protect -----------
CREATE FAILOVER GROUP dr_group
  OBJECT_TYPES = DATABASES, ROLES, WAREHOUSES, RESOURCE MONITORS, USERS
  ALLOWED_DATABASES = production, analytics
  ALLOWED_ACCOUNTS  = myorg.secondary_account     -- the DR target account
  REPLICATION_SCHEDULE = '10 MINUTE';             -- refresh every 10 min → RPO≈10m

-- 2) SECONDARY account (in another region) — create the replica -------------
-- (run these ON the secondary account)
/*
CREATE FAILOVER GROUP dr_group
  AS REPLICA OF myorg.primary_account.dr_group;

-- Pull the latest data on demand (or rely on the schedule):
ALTER FAILOVER GROUP dr_group REFRESH;
*/

-- 3) MONITOR replication lag (are we within our RPO?) -----------------------
SELECT * FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('DR_GROUP'))
ORDER BY phase_start_time DESC LIMIT 10;
-- Also: SHOW REPLICATION GROUPS;

-- 4) FAILOVER — promote the secondary to primary during a disaster ----------
-- (run ON the secondary account when the primary region is down)
/*
ALTER FAILOVER GROUP dr_group PRIMARY;   -- secondary becomes the new primary
-- Point apps at the secondary account. This is your RTO in action.
*/

-- 5) FAILBACK — after the primary region recovers ---------------------------
-- Re-sync and promote the original primary back when ready (reverse the steps).

-- ---------------------------------------------------------------------------
-- 6) A tested DR RUNBOOK (document this — interviewers love it)
--    1. Detect outage (monitoring/alerts on the primary).
--    2. Verify replication lag is acceptable (RPO check above).
--    3. Promote secondary: ALTER FAILOVER GROUP ... PRIMARY.
--    4. Repoint connection strings / DNS to the secondary account.
--    5. Communicate; validate critical queries run.
--    6. On recovery: re-replicate and fail back during a maintenance window.
--    Record measured RPO (data lost) and RTO (time to recover).
-- ---------------------------------------------------------------------------

-- ============================================================================
-- LEARNED: replication vs failover groups, cross-region/cloud replication,
-- REFRESH scheduling (RPO), promotion/failover (RTO), lag monitoring, and a
-- tested DR runbook. This is senior/architect-level business-continuity design.
-- NEXT: Project 20 — the end-to-end platform capstone (already built).
-- ============================================================================
