# Module 06 — Window Functions

> The skill that separates intermediate from advanced. Window functions answer "rank", "running total", "compare to previous row" — the hardest interview questions.

---

## 6.1 The Big Idea

A **window function** computes a value across a set of rows *related to the current row*, **without collapsing** them. Unlike `GROUP BY` (which reduces many rows to one), a window function **keeps every row** and adds a computed column.

```
GROUP BY: 7 rows → 3 rows (one per group)
WINDOW:   7 rows → 7 rows (+ a new column with the group value on each)
```

The syntax:
```sql
FUNCTION(...) OVER (PARTITION BY ... ORDER BY ...)
```
- `PARTITION BY` — split rows into groups (like GROUP BY, but rows stay).
- `ORDER BY` — order rows within each partition (needed for ranking/running totals).

## 6.2 Ranking Functions

```sql
SELECT name, dept_id, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
       RANK()       OVER (ORDER BY salary DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;
```
The difference (on ties):
| | ROW_NUMBER | RANK | DENSE_RANK |
|--|--|--|--|
| values | always unique | gaps after ties | no gaps |
| example | 1,2,3,4 | 1,2,2,4 | 1,2,2,3 |

## 6.3 PARTITION BY — Restart Per Group

```sql
-- Rank salaries WITHIN each department
SELECT name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```
The ranking restarts at 1 for each department. This `PARTITION BY` is the key to all "per group" analytics.

## 6.4 Top-N Per Group (the #1 interview pattern)

Wrap the window in a subquery/CTE and filter on the rank:
```sql
-- Top 2 earners per department
SELECT dept_id, name, salary FROM (
    SELECT dept_id, name, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk <= 2;
```
❄️ Snowflake makes this one line with `QUALIFY`:
```sql
SELECT dept_id, name, salary FROM employees
QUALIFY DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 2;
```

## 6.5 Aggregate Windows — Compare Each Row to Its Group

Aggregates can be windows too — every row keeps its value AND sees the group aggregate:
```sql
SELECT name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
       salary - AVG(salary) OVER (PARTITION BY dept_id) AS diff_from_avg
FROM employees;
```
This is impossible with plain `GROUP BY` (which would collapse the rows). Hugely useful.

## 6.6 Running Totals

Add `ORDER BY` inside `OVER` to accumulate:
```sql
SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
       AS running_total
FROM orders;
```
The **frame** `UNBOUNDED PRECEDING → CURRENT ROW` means "all rows up to and including this one". Partition it for per-group running totals:
```sql
SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date)
```

## 6.7 LAG & LEAD — Look at Other Rows

`LAG` = previous row's value, `LEAD` = next row's. Perfect for period-over-period comparisons:
```sql
-- Month-over-month revenue change
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date) AS mth, SUM(amount) AS rev
  FROM orders GROUP BY 1
)
SELECT mth, rev,
       LAG(rev) OVER (ORDER BY mth)          AS prev_month,
       rev - LAG(rev) OVER (ORDER BY mth)    AS change
FROM monthly;
```

## 6.8 FIRST_VALUE / LAST_VALUE / NTILE

```sql
-- Bucket employees into 4 salary quartiles
SELECT name, salary, NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
```
`FIRST_VALUE`/`LAST_VALUE` grab the first/last value in the window (mind the frame for LAST_VALUE — see the practice bank #87).

## 6.9 When to Use Windows vs GROUP BY

- Need **one row per group** (a summary table)? → `GROUP BY`.
- Need to **keep all rows** and add a comparison/rank/running value? → **window function**.
- "Rank", "top N per group", "running total", "vs previous/average" → **window function**, every time.

---

## ✅ Key Takeaways
1. Window functions compute across related rows **without collapsing** them: `FUNC() OVER (PARTITION BY … ORDER BY …)`.
2. `ROW_NUMBER` (unique), `RANK` (gaps), `DENSE_RANK` (no gaps) for ranking.
3. `PARTITION BY` restarts the calculation per group — the key to per-group analytics.
4. **Top-N-per-group** = rank in a subquery/CTE, filter the rank (or Snowflake `QUALIFY`).
5. Aggregate windows compare each row to its group average/total; add `ORDER BY` for running totals.
6. `LAG`/`LEAD` compare to previous/next rows (period-over-period).

## 🏋️ Exercises
1. Rank all employees by salary using `RANK` and `DENSE_RANK`; note the difference on ties.
2. Rank employees by salary **within each department**.
3. Return the top 2 earners per department.
4. Show each employee's salary next to their department average and the difference.
5. Compute a running total of `orders.amount` ordered by date.
6. Show month-over-month revenue change using `LAG`.

**Next:** [Module 07 — Advanced SQL →](module-07-advanced.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
