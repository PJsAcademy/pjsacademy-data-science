# Module 03 — Aggregations & GROUP BY

> Going from raw rows to *summaries*: totals, averages, counts. This is where SQL starts answering business questions.

---

## 3.1 Aggregate Functions — Collapsing Many Rows into One

An aggregate takes many rows and returns a single value:

| Function | Returns |
|----------|---------|
| `COUNT(*)` | number of rows |
| `COUNT(col)` | number of **non-NULL** values in col |
| `SUM(col)` | total |
| `AVG(col)` | average |
| `MIN(col)` / `MAX(col)` | smallest / largest |

```sql
SELECT COUNT(*)     AS total_employees,
       AVG(salary)  AS avg_salary,
       MAX(salary)  AS highest,
       MIN(salary)  AS lowest,
       SUM(salary)  AS total_payroll
FROM employees;
```

## 3.2 COUNT(*) vs COUNT(column) — a Classic Gotcha

```sql
SELECT COUNT(*)      AS all_rows,      -- counts every row
       COUNT(email)  AS with_email     -- counts only non-NULL emails
FROM employees;
```
`COUNT(*)` counts rows; `COUNT(col)` ignores NULLs. Interviewers love this distinction.

## 3.3 GROUP BY — Aggregates *Per* Something

Without `GROUP BY`, an aggregate summarises the whole table. With it, you get **one row per group**:
```sql
-- Average salary PER department
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id;
```
Rule of thumb: whenever you say "**per** X" (per department, per month, per customer), X goes in `GROUP BY`.

```
Before GROUP BY (rows)        After GROUP BY dept_id
dept 1, 180000                dept 1 → avg 136666
dept 1, 120000        ───►    dept 2 → avg  82500
dept 1, 110000                dept 3 → avg  88000
dept 2,  95000
...
```

## 3.4 The GROUP BY Rule

Every column in `SELECT` must be either **in the GROUP BY** or **inside an aggregate**. This is illegal:
```sql
-- WRONG: name isn't grouped or aggregated
SELECT dept_id, name, AVG(salary) FROM employees GROUP BY dept_id;
```
Because a department has many names — which one would it show? Fix: group by it, or aggregate it, or remove it.

## 3.5 Grouping by Multiple Columns

```sql
-- Orders and revenue per customer per month
SELECT customer_id,
       EXTRACT(MONTH FROM order_date) AS mth,
       COUNT(*)    AS orders,
       SUM(amount) AS revenue
FROM orders
GROUP BY customer_id, EXTRACT(MONTH FROM order_date);
```
❄️ Snowflake: `MONTH(order_date)` is cleaner than `EXTRACT`.

## 3.6 HAVING — Filtering Groups

`WHERE` filters **rows**; `HAVING` filters **groups** (after aggregation). You can't use an aggregate in `WHERE`.
```sql
-- Departments with more than 1 employee
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 1;
```
```sql
-- Customers who spent over 50,000
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 50000;
```

## 3.7 WHERE + GROUP BY + HAVING Together

They run in this order: filter rows → group → filter groups.
```sql
-- Among 2023 orders, customers with 2+ orders
SELECT customer_id, COUNT(*) AS orders_2023
FROM orders
WHERE order_date >= '2023-01-01'      -- filter rows first
GROUP BY customer_id                  -- then group
HAVING COUNT(*) >= 2;                 -- then filter groups
```

## 3.8 Conditional Aggregation (a power move)

Count/sum rows meeting a condition *within* each group using `CASE`:
```sql
SELECT dept_id,
       COUNT(*) AS total,
       SUM(CASE WHEN salary >= 100000 THEN 1 ELSE 0 END) AS high_earners
FROM employees
GROUP BY dept_id;
```
❄️ Snowflake shortcut: `COUNT_IF(salary >= 100000)`.

## 3.9 Rounding & Readability

```sql
SELECT dept_id, ROUND(AVG(salary), 0) AS avg_salary
FROM employees GROUP BY dept_id;
```

## 3.10 The Full Logical Order (now complete)

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```
Memorise this — it explains almost every "why doesn't my query work?" question.

---

## ✅ Key Takeaways
1. Aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) collapse many rows into one value.
2. `COUNT(*)` counts rows; `COUNT(col)` ignores NULLs.
3. `GROUP BY X` gives one row per group — use it whenever you want results "per X".
4. Every selected column must be grouped or aggregated.
5. `WHERE` filters rows (before grouping); `HAVING` filters groups (after).
6. `SUM(CASE WHEN … THEN 1 ELSE 0 END)` = conditional counting within groups.

## 🏋️ Exercises
1. Count how many employees there are, and how many have an email.
2. Show the average salary per department.
3. Show total revenue per product category (join needed — or use `orders` alone by product_id).
4. List departments with an average salary above 90,000 (`HAVING`).
5. Count, per department, how many employees earn 100,000+ (conditional aggregation).
6. Show total order amount per customer, only for customers who spent over 20,000.

**Next:** [Module 04 — JOINs →](module-04-joins.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
