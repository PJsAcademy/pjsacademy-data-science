# Module 07 — Advanced SQL

> Pivots, set operations, recursion, dates, and performance — the toolkit that handles any real-world request.

---

## 7.1 CASE — Conditional Logic

SQL's if/else. Use it for labels, bucketing, and conditional aggregation:
```sql
SELECT name, salary,
  CASE WHEN salary >= 120000 THEN 'High'
       WHEN salary >= 80000  THEN 'Medium'
       ELSE 'Low' END AS band
FROM employees;
```
Conditions are checked top-down; the first TRUE wins. Add `ELSE` for the fallback (else you get NULL).

## 7.2 Pivoting — Rows into Columns

Turn category rows into columns with conditional aggregation:
```sql
-- Revenue per category as columns
SELECT
  SUM(CASE WHEN category = 'Electronics' THEN amount ELSE 0 END) AS electronics,
  SUM(CASE WHEN category = 'Furniture'   THEN amount ELSE 0 END) AS furniture
FROM orders o JOIN products p ON o.product_id = p.product_id;
```
❄️ Snowflake has a native `PIVOT` clause; the `CASE` method works everywhere.

## 7.3 Set Operations — Stacking Results

Combine the results of two queries (same columns):
```sql
SELECT name FROM employees
UNION            -- removes duplicates
SELECT name FROM customers;

SELECT name FROM employees
UNION ALL        -- keeps duplicates (faster)
SELECT name FROM customers;
```
- `UNION` / `UNION ALL` — stack rows.
- `INTERSECT` — rows in both.
- `EXCEPT` (or `MINUS`) — rows in the first but not the second.

## 7.4 Subtotals — ROLLUP / CUBE / GROUPING SETS

Get group subtotals AND a grand total in one query:
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY ROLLUP(dept_id);   -- rows per dept + a grand-total row (dept_id NULL)
```
`CUBE` gives all combinations; `GROUPING SETS` lets you pick exactly which subtotals.

## 7.5 Date & Time Functions

The bread and butter of analytics:
```sql
-- Standard SQL
EXTRACT(YEAR FROM order_date)          -- pull a part
order_date + INTERVAL '7 days'         -- date math (Postgres)
-- Snowflake (cleaner)
YEAR(order_date), MONTH(order_date)
DATEADD('day', 7, order_date)
DATEDIFF('day', start_date, end_date)
DATE_TRUNC('month', order_date)        -- floor to the month
```
Truncating to month/week is the key trick for time-series grouping.

## 7.6 String Functions

```sql
UPPER(name), LOWER(name), LENGTH(name)
TRIM(name)                              -- strip whitespace
SUBSTRING(email, 1, 5)                  -- extract part
REPLACE(phone, '-', '')                 -- swap text
-- Snowflake gem:
SPLIT_PART(email, '@', 2)               -- domain from email
LISTAGG(name, ', ')                     -- concatenate a group into one string
```

## 7.7 Recursive CTEs — Hierarchies & Series

For trees (org charts, categories) and generated sequences:
```sql
-- Full management chain from the CEO down
WITH RECURSIVE org AS (
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL       -- anchor: the top
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, o.level + 1
    FROM employees e JOIN org o ON e.manager_id = o.emp_id  -- recursive step
)
SELECT level, name FROM org ORDER BY level;
```
Recursion = an **anchor** (starting rows) + a **recursive member** (rows built from the previous step) until nothing new is produced.

## 7.8 NULL Handling Functions

```sql
COALESCE(email, 'no-email')     -- first non-NULL argument
NULLIF(a, b)                    -- NULL if a = b (guards divide-by-zero)
-- Safe division:
revenue / NULLIF(orders, 0)     -- avoids /0 error when orders is 0
```

## 7.9 Query Performance (practical intuition)

You don't need to be a DBA, but know the basics:
- **Filter early** — a selective `WHERE` reduces work downstream.
- **Indexes** (in OLTP DBs like Postgres/MySQL) speed up lookups on filtered/joined columns.
- **Avoid `SELECT *`** in production — read only what you need.
- **Beware functions on filtered columns** — `WHERE YEAR(date)=2023` can prevent index use; prefer `WHERE date >= '2023-01-01' AND date < '2024-01-01'`.
- In Snowflake, performance is about **pruning** (clustering) and **warehouse size**, not indexes.
- Read the **query plan** (`EXPLAIN`) to see what's slow.

## 7.10 Putting It Together

Advanced SQL is mostly **combining** these tools: a CTE that cleans → a window that ranks → a CASE that labels → a pivot that reshapes. Build in layers, test each step.

---

## ✅ Key Takeaways
1. `CASE` = conditional logic; powers labels, bucketing, and pivots (rows→columns).
2. Set ops: `UNION`(/ALL), `INTERSECT`, `EXCEPT` stack/compare result sets.
3. `ROLLUP`/`CUBE`/`GROUPING SETS` add subtotals and grand totals.
4. Master **date functions** (`DATE_TRUNC`, `DATEDIFF`) and **string functions** (`SPLIT_PART`, `LISTAGG`).
5. **Recursive CTEs** handle hierarchies and generated series (anchor + recursive step).
6. `COALESCE`/`NULLIF` handle NULLs and guard divide-by-zero; filter early and avoid functions on filtered columns for speed.

## 🏋️ Exercises
1. Label each employee's salary as High/Medium/Low with `CASE`.
2. Pivot: show total revenue for Electronics vs Furniture as two columns.
3. Use `UNION` to list all employee and customer names in one column.
4. Use `ROLLUP` to show headcount per department plus a grand total.
5. Extract the email domain of each employee (`SPLIT_PART` or `SUBSTRING`).
6. Write a recursive CTE that lists numbers 1 to 10.

**Next:** [Module 08 — SQL for Interviews & Real Work →](module-08-interview-realwork.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
