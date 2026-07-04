# 🥇 SnowPro Advanced: Architect — Prep Guide

**PJ's Academy · The expert-level Snowflake credential.**

The Architect exam (ARA-C01) proves you can **design end-to-end Snowflake platforms** — accounts, security, performance, cost governance, and data sharing at enterprise scale.

> **Prerequisite:** SnowPro Core certified.

---

## 📋 Exam At A Glance

| Item | Detail |
|------|--------|
| Exam code | ARA-C01 |
| Questions | ~65 |
| Duration | 115 minutes |
| Cost | $375 USD |
| Prerequisite | SnowPro Core |

### Domain Weightings

| # | Domain | Weight |
|---|--------|--------|
| 1 | Accounts & Security | 28% |
| 2 | Performance & Scalability | 20% |
| 3 | Data Engineering | 20% |
| 4 | Storage, Data Protection & Sharing | 16% |
| 5 | Snowflake Platform | 16% |

---

## 🏛️ Domain 1 — Accounts & Security (28%)

- **Multi-account architecture** — organizations, ORGADMIN, account provisioning across regions/clouds.
- **RBAC at scale** — functional vs access role separation, role explosion avoidance, role inheritance design.
- **Advanced security** — Tri-Secret Secure, customer-managed keys, network policies, private connectivity (PrivateLink/Private Service Connect).
- **Data governance** — tags, tag-based masking, classification, access history, `ACCESS_HISTORY` for auditing.
- **Authentication** — SSO/SAML, SCIM provisioning, key-pair, OAuth flows.

## ⚡ Domain 2 — Performance & Scalability (20%)

- Warehouse sizing & multi-cluster scaling policies for mixed workloads.
- Workload isolation — dedicated warehouses per team/workload.
- Clustering, search optimization, and materialized view trade-offs at scale.
- Query acceleration service.
- Concurrency and queuing design.

## 🔧 Domain 3 — Data Engineering (20%)

- Ingestion architecture — Snowpipe vs Snowpipe Streaming vs Kafka connector.
- Pipeline design — Streams+Tasks vs Dynamic Tables; when to use each.
- External tables, Iceberg, and data lake integration.
- Snowpark for large-scale transformation.

## 💾 Domain 4 — Storage, Protection & Sharing (16%)

- Time Travel/Fail-safe cost modelling.
- Replication, failover groups, business continuity / DR design (RPO/RTO).
- Secure Data Sharing architecture — shares, reader accounts, Data Exchange, Marketplace listings.
- Cross-cloud / cross-region sharing.

## 🌐 Domain 5 — Snowflake Platform (16%)

- Cost governance — resource monitors, org-level budgets, chargeback via ACCOUNT_USAGE.
- Native Apps framework & Streamlit in Snowflake.
- Cortex (AI/ML functions) at a high level.
- Partner ecosystem integration (dbt, Fivetran, Tableau).

---

## 🧠 High-Yield Architect Facts

- **Failover groups** replicate account objects for DR; **replication groups** replicate databases.
- **PrivateLink** provides private connectivity — no public internet.
- **ACCESS_HISTORY** shows who accessed what (column-level lineage) — key for governance.
- **Reader accounts** are provider-managed & billed to the provider — for non-Snowflake consumers.
- **Query Acceleration Service** offloads scan-heavy portions of queries.
- Design for **workload isolation**: separate warehouses prevent one team starving another.

---

## 📝 Practice Questions (8)

**Q1.** Which provides private, non-internet connectivity to Snowflake?
A) Network policy  B) PrivateLink  C) OAuth  D) SSO

**Q2.** Which replicates account-level objects for disaster recovery?
A) Replication group  B) Failover group  C) Share  D) Clone

**Q3.** To audit column-level data access you query:
A) QUERY_HISTORY  B) ACCESS_HISTORY  C) COPY_HISTORY  D) LOGIN_HISTORY

**Q4.** Reader accounts are billed to:
A) The consumer  B) The data provider  C) Snowflake  D) Split

**Q5.** Best practice to prevent one team's queries starving another:
A) One big warehouse  B) Workload isolation via separate warehouses  C) Bigger warehouse  D) More Time Travel

**Q6.** Tag-based masking allows:
A) Masking by IP  B) Applying masking policies via object tags at scale  C) Row filtering  D) Encryption

**Q7.** For non-Snowflake consumers of shared data, use:
A) Direct share  B) Reader account  C) Marketplace only  D) CSV export

**Q8.** Which offloads scan-heavy query portions to extra serverless compute?
A) Materialized view  B) Query Acceleration Service  C) Result cache  D) Clustering

### ✅ Answers
1-B · 2-B · 3-B · 4-B · 5-B · 6-B · 7-B · 8-B

---

## 🗓️ 4-Week Plan
- **Week 1:** Accounts & Security (RBAC design, governance).
- **Week 2:** Performance & Data Engineering (pipelines, isolation).
- **Week 3:** Storage/Sharing/DR + Platform features.
- **Week 4:** Full review + scenario practice, book the exam.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
