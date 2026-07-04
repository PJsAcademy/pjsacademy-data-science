# 🏆 SnowPro Core Certification — Complete Prep Guide

**PJ's Academy · Everything you need to pass. No external resources required.**

This guide covers **100% of the SnowPro Core (COF-C02) exam** with detailed notes per domain, memory aids, 60+ practice questions with explanations, and a full mock exam.

---

## 📋 Exam At A Glance

| Item | Detail |
|------|--------|
| Exam code | COF-C02 |
| Questions | ~100 (multiple choice / multiple select) |
| Duration | 115 minutes |
| Passing score | ~750 / 1000 (scaled) |
| Cost | $175 USD |
| Validity | 2 years |
| Format | Online proctored or test centre |

### Domain Weightings (memorise these)

| # | Domain | Weight |
|---|--------|--------|
| 1 | Snowflake AI Data Cloud Features & Architecture | 24% |
| 2 | Account Access & Security | 18% |
| 3 | Performance & Cost Optimization | 14% |
| 4 | Data Loading & Unloading | 10% |
| 5 | Data Transformations | 22% |
| 6 | Data Protection & Data Sharing | 12% |

> 🎯 **Strategy:** Domains 1 + 5 = 46% of the exam. Master those first.

---

## 🏗️ Domain 1 — Architecture & Features (24%)

### The 3-Layer Architecture
1. **Cloud Services Layer** — the "brain." Authentication, access control, query parsing & optimisation, metadata management, infrastructure management. Runs on Snowflake-managed compute.
2. **Query Processing (Compute) Layer** — virtual warehouses (MPP compute clusters). Independent, elastic.
3. **Database Storage Layer** — data stored in compressed, columnar **micro-partitions** on cloud object storage (S3/Azure Blob/GCS).

**Key exam fact:** Storage and compute are **decoupled** — scale independently, pay separately.

### Micro-Partitions
- Automatic — Snowflake creates them (50–500 MB uncompressed each).
- Columnar storage within each partition.
- Metadata stored per partition (min/max/count) → enables **pruning**.
- **Clustering** = how well data is sorted across partitions.

### Virtual Warehouses
- Sizes: XS, S, M, L, XL, 2XL … 6XL. **Each size up = 2× credits/hour** and 2× compute.
- **Multi-cluster warehouses** (Enterprise+) auto-scale OUT for concurrency (more clusters), not up.
- **Scaling UP** (resize) = bigger warehouse for complex queries.
- **Scaling OUT** (multi-cluster) = more clusters for more concurrent users.
- `AUTO_SUSPEND` / `AUTO_RESUME` control cost.

### The 3 Caches (common exam trap)
| Cache | Where | What it stores | Lifespan |
|-------|-------|----------------|----------|
| Result Cache | Cloud Services | Full query results | 24 hours |
| Metadata Cache | Cloud Services | Table metadata/stats | persistent |
| Warehouse (local) Cache | Compute | Micro-partition data | until WH suspends |

**Result cache** serves identical queries with **zero compute** if underlying data hasn't changed.

### Editions
Standard → Enterprise (multi-cluster, materialized views, 90-day Time Travel) → Business Critical (HIPAA, PCI, customer-managed keys) → VPS (isolated).

### Connectivity / Ecosystem
SnowSQL (CLI), Snowsight (UI), connectors (Python, Spark, JDBC/ODBC, Kafka), Snowpark, partner tools (dbt, Tableau, Power BI).

---

## 🔐 Domain 2 — Account Access & Security (18%)

### RBAC — the core model
- Privileges are granted to **roles**, roles granted to **users** (and to other roles → hierarchy).
- **System-defined roles:** `ORGADMIN`, `ACCOUNTADMIN`, `SECURITYADMIN`, `USERADMIN`, `SYSADMIN`, `PUBLIC`.
- Hierarchy: `ACCOUNTADMIN` sits on top; `SYSADMIN` + `SECURITYADMIN` under it; `PUBLIC` is inherited by everyone.
- **Best practice:** create custom roles under `SYSADMIN`; don't use `ACCOUNTADMIN` for daily work.

### Access control models
- **DAC** (Discretionary): object owner grants access.
- **RBAC** (Role-Based): privileges via roles. Snowflake uses **both**.

### Authentication & network
- MFA (Duo), SSO/SAML, key-pair auth, OAuth.
- **Network policies** — allow/block IP ranges.
- Federated authentication for enterprise SSO.

### Data security
- Encryption **at rest** (AES-256) and **in transit** (TLS) — always on, automatic.
- **Tri-Secret Secure** (Business Critical) — customer-managed key + Snowflake key.
- **Key rotation** — automatic every 30 days.

---

## ⚡ Domain 3 — Performance & Cost Optimization (14%)

### Reducing cost
- Right-size warehouses; `AUTO_SUSPEND` low (e.g. 60s).
- Use **resource monitors** with credit quotas + triggers (NOTIFY/SUSPEND).
- Prefer transient/temporary tables where Time Travel isn't needed (less storage).

### Improving performance
- **Clustering keys** on very large tables (>1 TB) with selective filters.
- **Search Optimization Service** — point-lookup queries on large tables.
- **Materialized views** — precompute expensive aggregations (Enterprise+).
- **Query Profile** in Snowsight — find bottlenecks (spilling, poor pruning).
- Warehouse **spilling to disk** = warehouse too small → scale up.

### Monitoring
- `ACCOUNT_USAGE` schema (up to 365 days, ~45 min latency).
- `INFORMATION_SCHEMA` (real-time, shorter history).
- `QUERY_HISTORY`, `WAREHOUSE_METERING_HISTORY`, `STORAGE_USAGE`.

---

## 📥 Domain 4 — Data Loading & Unloading (10%)

### Stages
- **User stage** (`@~`), **Table stage** (`@%table`), **Named internal stage** (`@stage`), **External stage** (S3/Azure/GCS).

### Loading
- **`COPY INTO <table>`** — bulk load. Uses a warehouse.
- **Snowpipe** — continuous/auto load via `AUTO_INGEST` + cloud notifications. **Serverless** (no warehouse).
- File formats: CSV, JSON, Avro, ORC, Parquet, XML.
- `ON_ERROR` options: ABORT_STATEMENT (default), CONTINUE, SKIP_FILE.
- `VALIDATION_MODE` to dry-run.

### Unloading
- **`COPY INTO <stage>`** from a table/query → files.
- Default output = compressed (gzip) CSV; can specify format.
- `SINGLE = TRUE` for one file; default splits into multiple.

### Semi-structured
- **`VARIANT`** column type stores JSON/Avro/etc.
- Access with `col:path.to.field::type`.
- **`FLATTEN`** table function explodes arrays into rows.

---

## 🔄 Domain 5 — Data Transformations (22%)

### Semi-structured querying (heavily tested)
```sql
SELECT v:name::STRING, v:address.city::STRING,
       f.value:sku::STRING
FROM orders, LATERAL FLATTEN(input => v:items) f;
```

### Estimation functions
- `APPROX_COUNT_DISTINCT` (HyperLogLog), `APPROX_PERCENTILE`, `APPROX_TOP_K`.

### Useful functions
- Window functions + **`QUALIFY`** (filter window results).
- `PIVOT` / `UNPIVOT`.
- `LATERAL` joins.
- Date/time, string, conditional (`IFF`, `DECODE`, `CASE`) functions.

### Views
- **Standard view** — logical, recomputed each query.
- **Secure view** — hides definition + underlying data (for sharing).
- **Materialized view** — stored, auto-maintained, costs storage + compute (Enterprise+).

### Sampling
```sql
SELECT * FROM t SAMPLE (10);            -- 10% of rows
SELECT * FROM t SAMPLE (1000 ROWS);     -- ~1000 rows
```

### UDFs / Stored Procedures / Snowpark
- UDFs (SQL, JavaScript, Python, Java, Scala) — return values, used in queries.
- Stored procedures — procedural logic, can do DDL/DML.
- External functions — call external APIs.

---

## 🛡️ Domain 6 — Data Protection & Sharing (12%)

### Time Travel
- Query/restore historical data. Retention: 1 day (Standard, default), up to **90 days** (Enterprise).
- `AT` / `BEFORE` (timestamp, offset, or statement id).
- `UNDROP TABLE | SCHEMA | DATABASE`.

### Fail-safe
- **7 days** after Time Travel expires. **Snowflake-managed only** — you cannot query it; only Snowflake support can recover. Not configurable.

### Cloning (Zero-Copy)
- `CREATE ... CLONE` — instant, metadata-only, no storage until data diverges.
- Clone tables, schemas, databases.

### Data Sharing
- **Secure Data Sharing** — share live data, no copying. Provider creates a **share**; consumer queries it.
- **Reader accounts** — for consumers without Snowflake.
- **Snowflake Marketplace** — public datasets & data products.
- **Data Exchange** — private hub for a group of accounts.

### Replication
- Database replication across regions/clouds; **failover groups** for DR (Business Critical).

---

## 🧠 Memory Aids (last-night cram)

- **"Storage, Compute, Services"** = the 3 layers (bottom → top).
- **Fail-safe = 7 days, non-configurable, support only.**
- **Time Travel = up to 90 days (Enterprise), 1 day default.**
- **Snowpipe = serverless, continuous. COPY = warehouse, bulk.**
- **Result cache = 24 hours, zero compute.**
- **Scale UP = bigger (complex query). Scale OUT = more clusters (concurrency).**
- **ACCOUNTADMIN > SECURITYADMIN + SYSADMIN > custom roles > PUBLIC.**
- **VARIANT + FLATTEN = semi-structured querying.**

---

## 📝 Practice Test 1 — 20 Questions (answers below)

**Q1.** Which layer is responsible for query optimization?
A) Storage  B) Compute  C) Cloud Services  D) Metadata

**Q2.** How long is Fail-safe, and can it be configured?
A) 1 day, yes  B) 7 days, no  C) 90 days, yes  D) 24 hours, no

**Q3.** You need to load files continuously as they arrive in S3. Best option?
A) COPY INTO on a schedule  B) Snowpipe with AUTO_INGEST  C) INSERT  D) External table

**Q4.** Which is TRUE about the result cache?
A) Lives in the warehouse  B) Lasts 7 days  C) Serves identical queries with no compute for 24h  D) Must be enabled manually

**Q5.** To handle a spike in **concurrent users**, you should:
A) Scale up (resize)  B) Use a multi-cluster warehouse  C) Add clustering keys  D) Increase AUTO_SUSPEND

**Q6.** Maximum Time Travel retention on Enterprise edition?
A) 1 day  B) 7 days  C) 30 days  D) 90 days

**Q7.** Which role is at the TOP of the default hierarchy?
A) SYSADMIN  B) SECURITYADMIN  C) ACCOUNTADMIN  D) PUBLIC

**Q8.** Zero-copy cloning consumes storage:
A) Immediately, equal to source  B) Never  C) Only for changed/new data  D) Double the source

**Q9.** Which function gives an approximate distinct count?
A) COUNT(DISTINCT)  B) APPROX_COUNT_DISTINCT  C) HLL_ESTIMATE  D) DISTINCT_APPROX

**Q10.** A warehouse is spilling to local/remote disk. This means:
A) It's too large  B) It's too small for the query  C) Clustering is bad  D) Cache is full

**Q11.** Which view type hides both its definition and underlying data?
A) Standard  B) Materialized  C) Secure  D) Temporary

**Q12.** Snowpipe uses which compute?
A) Your virtual warehouse  B) Serverless Snowflake-managed compute  C) Cloud Services only  D) The ACCOUNTADMIN's warehouse

**Q13.** `QUALIFY` is used to:
A) Filter groups like HAVING  B) Filter window function results  C) Qualify column names  D) Grant privileges

**Q14.** Which is a semi-structured data type?
A) TEXT  B) VARIANT  C) NUMBER  D) BINARY

**Q15.** Data-at-rest encryption in Snowflake is:
A) Optional add-on  B) Business Critical only  C) Always on, automatic  D) Manual per table

**Q16.** To cap monthly credit spend, use:
A) AUTO_SUSPEND  B) Resource Monitor  C) Query timeout  D) Network policy

**Q17.** `UNDROP TABLE` works because of:
A) Fail-safe  B) Time Travel  C) Cloning  D) Replication

**Q18.** Multi-cluster warehouses are available starting in which edition?
A) Standard  B) Enterprise  C) Business Critical  D) VPS

**Q19.** Which stage is referenced by `@~`?
A) Table stage  B) Named stage  C) User stage  D) External stage

**Q20.** Secure Data Sharing copies data to the consumer:
A) Yes, full copy  B) No — consumer queries live data  C) Only metadata  D) Only on first query

### ✅ Answers & Explanations — Test 1
1. **C** — Cloud Services layer parses and optimizes queries.
2. **B** — Fail-safe is 7 days, non-configurable, Snowflake-support-only.
3. **B** — Snowpipe + AUTO_INGEST is the continuous-load pattern.
4. **C** — Result cache = 24h, zero compute for identical queries on unchanged data.
5. **B** — Multi-cluster scales OUT for concurrency.
6. **D** — 90 days on Enterprise.
7. **C** — ACCOUNTADMIN is top.
8. **C** — Clones only consume storage for divergent/new data.
9. **B** — APPROX_COUNT_DISTINCT (HyperLogLog).
10. **B** — Spilling = warehouse too small; scale up.
11. **C** — Secure views hide definition + data.
12. **B** — Snowpipe is serverless.
13. **B** — QUALIFY filters window-function output.
14. **B** — VARIANT.
15. **C** — Always on, automatic (AES-256).
16. **B** — Resource Monitor with credit quota.
17. **B** — UNDROP relies on Time Travel.
18. **B** — Enterprise.
19. **C** — `@~` = user stage.
20. **B** — Sharing = live query access, no copy.

---

## 📝 Practice Test 2 — 20 Questions

**Q1.** Which cache survives a warehouse suspend?
A) Local warehouse cache  B) Result cache  C) Neither  D) Both

**Q2.** Micro-partitions are approximately what size (uncompressed)?
A) 1–5 MB  B) 50–500 MB  C) 1–10 GB  D) Fixed 128 MB

**Q3.** Which is NOT a system-defined role?
A) SYSADMIN  B) USERADMIN  C) DATAADMIN  D) ORGADMIN

**Q4.** To share data with a party that has NO Snowflake account:
A) Impossible  B) Create a reader account  C) Email an export  D) Grant them ACCOUNTADMIN

**Q5.** `COPY INTO` with `ON_ERROR = 'CONTINUE'` will:
A) Abort on first error  B) Skip the whole file  C) Skip bad rows, load the rest  D) Retry the file

**Q6.** Scaling a warehouse from Medium to Large:
A) Doubles credits/hour  B) Halves credits  C) No cost change  D) Adds a cluster

**Q7.** Which service accelerates selective point-lookup queries?
A) Materialized views  B) Search Optimization Service  C) Result cache  D) Clustering only

**Q8.** VARIANT max compressed size per row?
A) 1 MB  B) 8 MB  C) 16 MB  D) 128 MB

**Q9.** Which lets you query data "as of" 2 hours ago?
A) Fail-safe  B) Time Travel with AT(OFFSET => -7200)  C) Cloning  D) Replication

**Q10.** A Standard-edition account's default Time Travel is:
A) 0 days  B) 1 day  C) 7 days  D) 90 days

**Q11.** Which object is billed as serverless compute?
A) Virtual warehouse  B) Snowpipe  C) Result cache  D) Materialized view refresh — (trick: MV refresh IS serverless too)

**Q12.** Best practice: daily development work should use:
A) ACCOUNTADMIN  B) A custom role under SYSADMIN  C) SECURITYADMIN  D) PUBLIC

**Q13.** `FLATTEN` is used to:
A) Compress data  B) Explode arrays/objects into rows  C) Remove nulls  D) Merge tables

**Q14.** Tri-Secret Secure is available in:
A) Standard  B) Enterprise  C) Business Critical  D) All editions

**Q15.** Which stores query results for reuse across users?
A) Local cache  B) Result cache  C) Metadata cache  D) Snowpipe

**Q16.** To reduce storage from Time Travel on a staging table you rarely need to recover:
A) Use a transient table  B) Increase retention  C) Add clustering  D) Use a materialized view

**Q17.** Which is TRUE about micro-partition pruning?
A) Requires manual config  B) Uses partition metadata to skip data  C) Only works with clustering keys  D) Slows queries

**Q18.** External functions let Snowflake:
A) Run on external warehouses  B) Call external APIs/services  C) Share data  D) Replicate

**Q19.** In RBAC, privileges are granted directly to:
A) Users  B) Roles  C) Warehouses  D) Databases

**Q20.** Snowflake Marketplace provides:
A) Compute credits  B) Third-party/public datasets & data products  C) Training courses  D) Warehouses

### ✅ Answers & Explanations — Test 2
1. **B** — Result cache is in Cloud Services, survives WH suspend; local cache is lost.
2. **B** — 50–500 MB uncompressed.
3. **C** — DATAADMIN is not system-defined.
4. **B** — Reader accounts serve non-Snowflake consumers.
5. **C** — CONTINUE skips bad rows.
6. **A** — Each size step doubles credits/hour.
7. **B** — Search Optimization Service.
8. **C** — VARIANT max 16 MB compressed.
9. **B** — Time Travel AT(OFFSET => -7200 seconds).
10. **B** — 1 day default (Standard).
11. **B/D** — Snowpipe and MV refresh are serverless; primary answer **B**.
12. **B** — Custom role under SYSADMIN.
13. **B** — Explodes nested structures into rows.
14. **C** — Business Critical.
15. **B** — Result cache (shared across users on same account).
16. **A** — Transient tables have no Fail-safe and minimal Time Travel → less storage.
17. **B** — Pruning uses metadata to skip partitions automatically.
18. **B** — External functions call external services/APIs.
19. **B** — Roles (then roles → users).
20. **B** — Marketplace = datasets/data products.

---

## 🎯 Full Mock Exam
A **60-question timed mock** (matching the real 100-question ratio across domains) is in [mock-exam-1.md](mock-exam-1.md). Give yourself 70 minutes, no notes.

## 🗓️ 4-Week Study Plan
- **Week 1:** Domains 1 + 2 (architecture, security). Do Practice Test 1.
- **Week 2:** Domains 5 + 4 (transformations, loading). Hands-on labs.
- **Week 3:** Domains 3 + 6 (performance/cost, protection/sharing). Do Practice Test 2.
- **Week 4:** Full mock exam, review weak areas, re-take. Book the exam.

## 💡 Exam-Day Tips
- Flag-and-return: don't burn time on hard questions.
- Watch for "select TWO" / "select all" — partial credit isn't given.
- Eliminate obviously wrong options first.
- Trust the memory aids above for the trap questions (Fail-safe, caches, scaling).

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com) · hello@pjsacademy.com*
