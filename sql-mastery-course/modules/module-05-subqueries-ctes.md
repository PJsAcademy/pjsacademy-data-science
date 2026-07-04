# Module 05 — Subqueries & CTEs

> Queries inside queries. Once you can nest and name sub-results, you can express almost any question.

---

## 5.1 What Is a Subquery?

A **subquery** is a `SELECT` inside another query. The inner query runs first; the outer query uses its result.

```sql
-- Employees earning above the company average
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
Here `(SELECT AVG(salary) FROM employees)` returns one number; the outer query compares each salary to it.

## 5.2 Three Shapes of Subquery

**1) Scalar** — returns a single value; use it like a value:
```sql
WHERE salary > (SELECT AVG(salary) FROM employees)
```

**2) List** — returns a column of values; use with `IN`:
```sql
SELECT name FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE location = 'Bangalore');
```

**3) Table** — returns rows/columns; use it in `FROM` (a "derived table"):
```sql
SELECT dept_id, avg_sal
FROM (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) t
WHERE avg_sal > 90000;
```

## 5.3 Correlated Subqueries

A **correlated** subquery references the outer row — it re-runs for each outer row:
```sql
-- Employees earning above THEIR department's average
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees
                  WHERE dept_id = e.dept_id);   -- references e.dept_id
```
Powerful, but can be slow (runs per row) — a window function often does this better (Module 06).

## 5.4 EXISTS / NOT EXISTS

Tests whether a subquery returns **any** rows. Great for "has / has not" questions and safe with NULLs:
```sql
-- Customers who HAVE ordered
SELECT c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Customers who have NOT ordered
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
`SELECT 1` is a convention — EXISTS only cares *whether* rows exist, not what's in them.

## 5.5 NOT IN vs NOT EXISTS (a NULL trap)

```sql
-- ⚠️ If the subquery returns any NULL, NOT IN returns NO rows (surprising!)
WHERE customer_id NOT IN (SELECT customer_id FROM orders)   -- risky if NULLs
-- ✅ NOT EXISTS handles NULLs correctly
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
```
Prefer `NOT EXISTS` for anti-joins when NULLs are possible.

## 5.6 CTEs — Common Table Expressions (WITH)

A **CTE** is a named, temporary result you define up front with `WITH`, then use below. It makes complex queries **readable**:
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, d.avg_sal
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_sal;
```
Read it top-to-bottom: "first compute `dept_avg`, then use it." Much clearer than a nested subquery.

## 5.7 Multiple & Chained CTEs

You can define several, and later ones can use earlier ones:
```sql
WITH
spend AS (
    SELECT customer_id, SUM(amount) AS total
    FROM orders GROUP BY customer_id
),
ranked AS (
    SELECT customer_id, total,
           total > (SELECT AVG(total) FROM spend) AS above_avg
    FROM spend
)
SELECT * FROM ranked WHERE above_avg;
```

## 5.8 CTE vs Subquery — Which?

- **CTE** — when the logic is complex, reused, or you want readability. Default choice for anything non-trivial.
- **Subquery** — for quick, one-off inline values.
They're often interchangeable; CTEs just read better.

## 5.9 Building Up Complex Queries

The pro workflow: solve it in **layers**. Each CTE is one clear step (clean → aggregate → rank → filter). Build and test one layer at a time. This is how you tackle hard interview questions calmly.

---

## ✅ Key Takeaways
1. A **subquery** is a SELECT inside another query — scalar (a value), list (with `IN`), or table (in `FROM`).
2. **Correlated** subqueries reference the outer row and run per-row (often replaceable by window functions).
3. `EXISTS` / `NOT EXISTS` test for the presence of rows — the safe way to do anti-joins.
4. Prefer `NOT EXISTS` over `NOT IN` when NULLs are possible.
5. **CTEs (`WITH`)** name intermediate results for readability; chain several to build complex logic in layers.
6. Solve hard queries **one layer at a time**.

## 🏋️ Exercises
1. Find employees earning more than the company average (scalar subquery).
2. Find employees in departments located in 'Bangalore' (list subquery with `IN`).
3. Find employees earning above their own department's average (correlated subquery).
4. Find customers who have never ordered, using `NOT EXISTS`.
5. Rewrite exercise 3 using a CTE that computes department averages.
6. Using two chained CTEs, list customers who spent above the average customer spend.

**Next:** [Module 06 — Window Functions →](module-06-window-functions.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
