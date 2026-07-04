# 🥇 SnowPro Advanced: Data Analyst — Prep Guide

**PJ's Academy · Prove you can turn Snowflake data into decisions.**

The Data Analyst exam (DAA-C01) validates advanced analytics skills on Snowflake — complex SQL, data prep, visualization, and delivering trustworthy insights.

> **Prerequisite:** SnowPro Core certified.

---

## 📋 Exam At A Glance

| Item | Detail |
|------|--------|
| Exam code | DAA-C01 |
| Questions | ~65 |
| Duration | 115 minutes |
| Cost | $375 USD |
| Prerequisite | SnowPro Core |

### Domain Weightings

| # | Domain | Weight |
|---|--------|--------|
| 1 | Data Ingestion & Preparation | 25% |
| 2 | Data Analysis & Transformation | 30% |
| 3 | Reporting, Visualization & Delivery | 25% |
| 4 | Data Quality, Governance & Security | 20% |

---

## 📥 Domain 1 — Ingestion & Preparation (25%)

- Loading data for analysis: `COPY INTO`, stages, external tables, Marketplace datasets.
- Cleaning: dedup (`QUALIFY ROW_NUMBER()`), null handling, type casting, standardizing.
- Reshaping: `PIVOT` / `UNPIVOT`, `FLATTEN` for semi-structured.
- Joining & enriching with Marketplace data (weather, demographics).

## 📊 Domain 2 — Analysis & Transformation (30%)

### Advanced analytical SQL
- Window functions: `LAG`/`LEAD`, running totals, moving averages, `NTILE`, `PERCENT_RANK`.
- `QUALIFY` for top-N and dedup.
- `GROUP BY ROLLUP` / `CUBE` / `GROUPING SETS` for subtotals.
- `MATCH_RECOGNIZE` for funnels & sessionization.
- Recursive CTEs for hierarchies.
- Approximate functions (`APPROX_PERCENTILE`, `APPROX_COUNT_DISTINCT`) for speed.

```sql
-- Cohort retention with window functions
SELECT cohort_month, months_since,
       COUNT(DISTINCT user_id) AS active,
       ROUND(RATIO_TO_REPORT(COUNT(DISTINCT user_id))
             OVER (PARTITION BY cohort_month) * 100, 1) AS pct
FROM cohorts GROUP BY 1,2;
```

### Statistical functions
- `CORR`, `STDDEV`, `VARIANCE`, `REGR_*`, `MEDIAN`, percentiles.

## 📈 Domain 3 — Reporting, Visualization & Delivery (25%)

- **Streamlit in Snowflake** — build dashboards natively.
- **Snowflake Notebooks** — analysis + narrative.
- BI tools: Tableau, Power BI, Sigma connectivity + best practices.
- Materialized views & result caching for fast dashboards.
- Secure views & shares for delivering data to stakeholders.

## 🛡️ Domain 4 — Quality, Governance & Security (20%)

- Data quality checks, `GROUP BY` validation, anomaly spotting.
- Masking policies, row access policies (what an analyst sees).
- Understanding RBAC from a consumer's perspective.
- Lineage & trust: ACCESS_HISTORY, freshness checks.

---

## 🧠 High-Yield Facts

- **QUALIFY** replaces subqueries for filtering window results — memorize it.
- **ROLLUP/CUBE/GROUPING SETS** produce subtotals & grand totals in one query.
- **MATCH_RECOGNIZE** = funnels/sessionization; know the `PATTERN`/`DEFINE` skeleton.
- **RATIO_TO_REPORT** gives % of group without a self-join.
- **Streamlit in Snowflake** = dashboards with no external hosting.
- **Result cache** (24h) makes repeated dashboard queries free.

---

## 📝 Practice Questions (10)

**Q1.** Which produces subtotals AND a grand total in one query?
A) GROUP BY  B) GROUP BY ROLLUP  C) QUALIFY  D) PIVOT

**Q2.** Best clause to keep the top 3 rows per group inline?
A) HAVING  B) WHERE  C) QUALIFY  D) LIMIT

**Q3.** Which builds funnels/sessionization?
A) PIVOT  B) MATCH_RECOGNIZE  C) FLATTEN  D) CUBE

**Q4.** `RATIO_TO_REPORT` computes:
A) A running total  B) Value as % of a partition  C) A rank  D) A median

**Q5.** Fastest distinct count on billions of rows:
A) COUNT(DISTINCT)  B) APPROX_COUNT_DISTINCT  C) GROUP BY  D) DISTINCT

**Q6.** Native dashboarding inside Snowflake uses:
A) Tableau only  B) Streamlit in Snowflake  C) Excel  D) Power BI only

**Q7.** To remove duplicate rows keeping the latest, use:
A) DISTINCT  B) QUALIFY ROW_NUMBER()  C) GROUP BY  D) MERGE

**Q8.** Which reshapes rows into columns?
A) UNPIVOT  B) PIVOT  C) FLATTEN  D) LATERAL

**Q9.** Repeated identical dashboard queries are free due to:
A) Local cache  B) Result cache (24h)  C) Clustering  D) MV

**Q10.** An analyst sees masked PII because of:
A) A view  B) A masking policy  C) Encryption  D) A stage

### ✅ Answers
1-B · 2-C · 3-B · 4-B · 5-B · 6-B · 7-B · 8-B · 9-B · 10-B

---

## 🗓️ 3-Week Plan
- **Week 1:** Advanced analytical SQL (windows, ROLLUP, MATCH_RECOGNIZE).
- **Week 2:** Visualization & delivery (Streamlit, BI, caching).
- **Week 3:** Governance + practice tests.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
