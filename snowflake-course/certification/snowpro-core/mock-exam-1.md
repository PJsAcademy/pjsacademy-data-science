# 🏆 SnowPro Core — Full Mock Exam 1 (60 Questions)

**PJ's Academy · Timed practice exam matching the real COF-C02 domain ratios.**

⏱️ **Time limit:** 70 minutes · **Pass mark:** 45/60 (75%) · **No notes.**

Domain mix mirrors the real exam: Architecture 14 Qs · Security 11 · Transformations 13 · Performance/Cost 8 · Loading 6 · Protection/Sharing 8.

> Answer all 60, then score with the key at the bottom. Review every wrong answer against the [main guide](README.md).

---

### Architecture & Features (Q1–Q14)

**Q1.** Snowflake's architecture is best described as:
A) Shared-disk  B) Shared-nothing  C) Multi-cluster shared-data  D) Single-node

**Q2.** Which layer manages metadata and query optimization?
A) Storage  B) Compute  C) Cloud Services  D) Warehouse

**Q3.** Data in Snowflake is physically stored as:
A) Row-based files  B) Compressed columnar micro-partitions  C) Plain CSV  D) B-tree indexes

**Q4.** A virtual warehouse of size Large uses how many credits/hour?
A) 2  B) 4  C) 8  D) 16

**Q5.** Multi-cluster warehouses primarily solve:
A) Slow single queries  B) Concurrency (many users)  C) Storage cost  D) Data loading

**Q6.** The result cache retains results for:
A) 1 hour  B) 24 hours  C) 7 days  D) Until warehouse suspends

**Q7.** Which cache is lost when a warehouse suspends?
A) Result cache  B) Metadata cache  C) Local (warehouse) cache  D) None

**Q8.** Which edition first offers 90-day Time Travel and materialized views?
A) Standard  B) Enterprise  C) Business Critical  D) VPS

**Q9.** Which is NOT a Snowflake-supported cloud?
A) AWS  B) Azure  C) GCP  D) Oracle Cloud

**Q10.** Micro-partitions are approximately what uncompressed size?
A) 16 MB  B) 50–500 MB  C) 1–2 GB  D) 10 GB

**Q11.** Pruning improves performance by:
A) Compressing data  B) Skipping partitions that can't match a filter  C) Caching results  D) Adding indexes

**Q12.** Snowsight is Snowflake's:
A) CLI  B) Web UI  C) Python connector  D) Driver

**Q13.** Which statement about storage and compute is TRUE?
A) They scale together  B) They are decoupled and scale independently  C) Compute includes storage  D) Storage requires a running warehouse

**Q14.** Auto-suspend is configured to:
A) Drop the warehouse  B) Pause a warehouse after idle time  C) Resize automatically  D) Cache queries

### Account Access & Security (Q15–Q25)

**Q15.** In RBAC, privileges are granted directly to:
A) Users  B) Roles  C) Warehouses  D) Sessions

**Q16.** Which role is at the top of the hierarchy?
A) SYSADMIN  B) SECURITYADMIN  C) ACCOUNTADMIN  D) USERADMIN

**Q17.** Custom roles should be created under which role by best practice?
A) ACCOUNTADMIN  B) SYSADMIN  C) PUBLIC  D) ORGADMIN

**Q18.** Which role does every user automatically have?
A) SYSADMIN  B) PUBLIC  C) SECURITYADMIN  D) USERADMIN

**Q19.** Dynamic data masking is applied via:
A) A view  B) A masking policy on a column  C) Encryption  D) A network policy

**Q20.** Row-level security is implemented with:
A) Masking policy  B) Row access policy  C) Secure view only  D) Tags

**Q21.** Data-at-rest encryption in Snowflake is:
A) Optional  B) Always on (AES-256)  C) Business Critical only  D) Manual

**Q22.** Tri-Secret Secure requires which edition?
A) Standard  B) Enterprise  C) Business Critical  D) All

**Q23.** Network policies control:
A) Query cost  B) Allowed/blocked IP addresses  C) Role hierarchy  D) Warehouse size

**Q24.** Which authentication method uses a public/private key?
A) Password  B) Key-pair authentication  C) OAuth  D) SAML

**Q25.** Encryption keys in Snowflake rotate automatically every:
A) 7 days  B) 30 days  C) 90 days  D) Never

### Data Transformations (Q26–Q38)

**Q26.** Which clause filters window-function results without a subquery?
A) HAVING  B) WHERE  C) QUALIFY  D) FILTER

**Q27.** Which type stores JSON natively?
A) TEXT  B) VARIANT  C) BLOB  D) STRING

**Q28.** To explode a JSON array into rows you use:
A) PIVOT  B) FLATTEN  C) UNNEST  D) EXPLODE

**Q29.** `APPROX_COUNT_DISTINCT` is based on which algorithm?
A) B-tree  B) HyperLogLog  C) Bloom filter  D) Hash join

**Q30.** To access a nested JSON field you use:
A) col.field  B) col->field  C) col:field  D) col[field]

**Q31.** Which reshapes rows into columns?
A) UNPIVOT  B) PIVOT  C) FLATTEN  D) LATERAL

**Q32.** A view that hides its definition and underlying data is a:
A) Standard view  B) Materialized view  C) Secure view  D) Temporary view

**Q33.** Materialized views are available in which edition and above?
A) Standard  B) Enterprise  C) Business Critical  D) VPS

**Q34.** `SAMPLE (10)` returns approximately:
A) 10 rows  B) 10% of rows  C) 10 partitions  D) Top 10

**Q35.** Which is a Snowflake scalar UDF language?
A) Python  B) Java  C) JavaScript  D) All of these

**Q36.** LATERAL FLATTEN is used with which data?
A) Structured only  B) Semi-structured (arrays/objects)  C) Binary  D) Numeric

**Q37.** `IFF(condition, a, b)` is:
A) A window function  B) A conditional (ternary) function  C) A join  D) An aggregate

**Q38.** To cast a VARIANT value to text you write:
A) ::STRING  B) TO_TEXT() only  C) CONVERT()  D) CAST optional

### Performance & Cost (Q39–Q46)

**Q39.** A warehouse spilling to remote disk indicates:
A) Too large  B) Too small for the workload  C) Bad clustering  D) Cache full

**Q40.** To cap monthly credit consumption use a:
A) Query timeout  B) Resource monitor  C) Network policy  D) Task

**Q41.** Search Optimization Service accelerates:
A) Full table scans  B) Selective point-lookup queries  C) Aggregations  D) Joins only

**Q42.** Clustering keys are most beneficial on:
A) Small tables  B) Very large tables with selective filters  C) All tables  D) Temporary tables

**Q43.** Which schema holds up to 365 days of account usage data?
A) INFORMATION_SCHEMA  B) ACCOUNT_USAGE  C) PUBLIC  D) METADATA

**Q44.** The cheapest way to avoid paying for an idle warehouse:
A) Drop it daily  B) Set a low AUTO_SUSPEND  C) Resize to XS  D) Use result cache

**Q45.** Which reduces storage cost for a scratch/staging table?
A) Permanent table  B) Transient table  C) Materialized view  D) External table

**Q46.** Where do you inspect why a query was slow?
A) Query Profile  B) Resource monitor  C) Network policy  D) Snowpipe

### Data Loading & Unloading (Q47–Q52)

**Q47.** Which command bulk-loads files into a table?
A) INSERT  B) COPY INTO <table>  C) PUT  D) MERGE

**Q48.** Snowpipe is best described as:
A) Bulk, warehouse-based  B) Continuous, serverless auto-load  C) A file format  D) A stage type

**Q49.** `@~` refers to which stage?
A) Table stage  B) Named stage  C) User stage  D) External stage

**Q50.** `ON_ERROR = 'CONTINUE'` during COPY will:
A) Abort  B) Skip the file  C) Skip bad rows, load the rest  D) Retry

**Q51.** Which is NOT a supported load format?
A) Parquet  B) Avro  C) JSON  D) DOCX

**Q52.** To unload query results to files you use:
A) COPY INTO <stage>  B) EXPORT  C) DUMP  D) UNLOAD

### Data Protection & Sharing (Q53–Q60)

**Q53.** Fail-safe lasts how long and is configurable?
A) 1 day, yes  B) 7 days, no  C) 90 days, yes  D) 24 hours, yes

**Q54.** `UNDROP TABLE` relies on:
A) Fail-safe  B) Time Travel  C) Cloning  D) Replication

**Q55.** Zero-copy cloning consumes storage:
A) Immediately  B) Only for changed data  C) Never  D) Double

**Q56.** Secure Data Sharing gives the consumer:
A) A full copy  B) Live query access, no copy  C) Metadata only  D) A reader license

**Q57.** To share data with a party lacking a Snowflake account:
A) Impossible  B) Create a reader account  C) Email CSVs  D) Grant ACCOUNTADMIN

**Q58.** The Snowflake Marketplace provides:
A) Compute credits  B) Third-party datasets & data products  C) Warehouses  D) Courses

**Q59.** Default Time Travel retention on Standard edition:
A) 0 days  B) 1 day  C) 7 days  D) 90 days

**Q60.** Database replication across regions is used for:
A) Cost saving  B) Disaster recovery / failover  C) Query speed  D) Masking

---

## ✅ Answer Key

| Q | A | Q | A | Q | A | Q | A | Q | A | Q | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C | 11 | B | 21 | B | 31 | B | 41 | B | 51 | D |
| 2 | C | 12 | B | 22 | C | 32 | C | 42 | B | 52 | A |
| 3 | B | 13 | B | 23 | B | 33 | B | 43 | B | 53 | B |
| 4 | C | 14 | B | 24 | B | 34 | B | 44 | B | 54 | B |
| 5 | B | 15 | B | 25 | B | 35 | D | 45 | B | 55 | B |
| 6 | B | 16 | C | 26 | C | 36 | B | 46 | A | 56 | B |
| 7 | C | 17 | B | 27 | B | 37 | B | 47 | B | 57 | B |
| 8 | B | 18 | B | 28 | B | 38 | A | 48 | B | 58 | B |
| 9 | D | 19 | B | 29 | B | 39 | B | 49 | C | 59 | B |
| 10 | B | 20 | B | 30 | C | 40 | B | 50 | C | 60 | B |

## 📊 Score Yourself
- **54–60 (90%+):** Exam-ready. Book it. 🎉
- **45–53 (75–89%):** Passing zone — review weak domains, retake.
- **Below 45:** Revisit the [main guide](README.md), redo practice tests 1 & 2, then retry.

## 🔁 Tricky Ones to Re-Read
Q6 (result cache 24h), Q7 (local cache lost on suspend), Q53 (fail-safe 7d fixed), Q55 (clone storage), Q39 (spilling = too small), Q17 (custom roles under SYSADMIN). These are the most-missed on the real exam.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com) · hello@pjsacademy.com*
