# 🥇 SnowPro Advanced: Administrator — Prep Guide

**PJ's Academy · Prove you can run Snowflake at enterprise scale.**

The Administrator exam (ADA-C01) validates that you can manage accounts, security, cost, performance, and data protection across an organization's Snowflake estate.

> **Prerequisite:** SnowPro Core certified.

---

## 📋 Exam At A Glance

| Item | Detail |
|------|--------|
| Exam code | ADA-C01 |
| Questions | ~65 |
| Duration | 115 minutes |
| Cost | $375 USD |
| Prerequisite | SnowPro Core |

### Domain Weightings

| # | Domain | Weight |
|---|--------|--------|
| 1 | Snowflake Security & Governance | 30% |
| 2 | Account Management & Data Governance | 25% |
| 3 | Performance & Cost Management | 25% |
| 4 | Data Protection, DR & Sharing | 20% |

---

## 🛡️ Domain 1 — Security & Governance (30%)

- **RBAC administration** — role hierarchies, functional vs access roles, `MANAGE GRANTS`, future grants.
- **User & session management** — `CREATE USER`, session policies, session timeouts.
- **Authentication** — SSO/SAML, SCIM provisioning, MFA enforcement, key-pair rotation.
- **Network security** — network policies, network rules, PrivateLink.
- **Governance** — masking policies, row access policies, tags, tag-based masking, object dependencies.
- **ACCESS_HISTORY** & **LOGIN_HISTORY** for auditing.

```sql
-- Future grants: auto-grant on new objects in a schema
GRANT SELECT ON FUTURE TABLES IN SCHEMA analytics.public TO ROLE reporter;
-- Session policy
CREATE SESSION POLICY strict_policy SESSION_IDLE_TIMEOUT_MINS = 30;
```

## 🏢 Domain 2 — Account Management & Data Governance (25%)

- **Organizations** — ORGADMIN, creating accounts, cross-region/cloud.
- **Resource monitors** — org & account level, credit quotas, triggers.
- **Parameters** — account/session/object parameter hierarchy.
- **ACCOUNT_USAGE vs ORGANIZATION_USAGE** schemas.
- **Replication & data governance** across accounts.

## ⚡ Domain 3 — Performance & Cost Management (25%)

- **Warehouse administration** — sizing, multi-cluster scaling policies (Standard vs Economy), auto-suspend/resume.
- **Cost attribution** — chargeback via ACCOUNT_USAGE, resource monitors, budgets.
- **Query performance** — Query Profile, clustering, search optimization, materialized views.
- **Warehouse utilization** — `WAREHOUSE_LOAD_HISTORY`, queuing, spilling.
- **Storage cost** — Time Travel/Fail-safe retention, transient tables.

```sql
-- Find idle-but-expensive warehouses
SELECT warehouse_name, SUM(credits_used) c
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time > DATEADD(day,-30,CURRENT_DATE())
GROUP BY 1 ORDER BY c DESC;
```

## 💾 Domain 4 — Data Protection, DR & Sharing (20%)

- **Time Travel & Fail-safe** administration, retention tuning.
- **Replication & failover groups** — DR design, RPO/RTO.
- **Cloning** for backup/dev strategies.
- **Secure Data Sharing** administration — shares, reader accounts, Data Exchange.
- **Encryption** — key rotation, Tri-Secret Secure, customer-managed keys.

---

## 🧠 High-Yield Facts

- **Future grants** auto-apply privileges to objects created later — key admin tool.
- **Economy** scaling policy conserves credits (fuller clusters) vs **Standard** (faster).
- **ORGADMIN** manages the organization & creates accounts.
- **ORGANIZATION_USAGE** aggregates usage across all accounts.
- **Resource monitors** can act at account OR warehouse level with NOTIFY/SUSPEND triggers.
- **Session policies** enforce idle timeouts; **network policies** restrict IPs.

---

## 📝 Practice Questions (10)

**Q1.** Which auto-grants privileges on objects created later in a schema?
A) GRANT ... ON ALL  B) GRANT ... ON FUTURE  C) MANAGE GRANTS  D) ROLE inheritance

**Q2.** Which scaling policy conserves credits by filling clusters?
A) Standard  B) Economy  C) Auto  D) Maximized

**Q3.** Which role manages the organization and creates accounts?
A) ACCOUNTADMIN  B) ORGADMIN  C) SECURITYADMIN  D) SYSADMIN

**Q4.** Cross-account usage is aggregated in:
A) ACCOUNT_USAGE  B) ORGANIZATION_USAGE  C) INFORMATION_SCHEMA  D) PUBLIC

**Q5.** A resource monitor can act at which levels?
A) Account only  B) Warehouse only  C) Account and warehouse  D) Query only

**Q6.** Which view audits who accessed which columns?
A) LOGIN_HISTORY  B) ACCESS_HISTORY  C) QUERY_HISTORY  D) COPY_HISTORY

**Q7.** For non-Snowflake data consumers, admins create:
A) A share only  B) A reader account  C) A clone  D) A stage

**Q8.** Which enforces a 30-minute idle logout?
A) Network policy  B) Session policy  C) Masking policy  D) Row policy

**Q9.** To restrict access to specific IP ranges:
A) Session policy  B) Network policy  C) Masking  D) Tag

**Q10.** Replicating account objects for DR uses:
A) Replication group  B) Failover group  C) Clone  D) Share

### ✅ Answers
1-B · 2-B · 3-B · 4-B · 5-C · 6-B · 7-B · 8-B · 9-B · 10-B

---

## 🗓️ 3-Week Plan
- **Week 1:** Security & governance (RBAC, policies, auditing).
- **Week 2:** Account mgmt + performance/cost.
- **Week 3:** DR/sharing + practice tests.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
