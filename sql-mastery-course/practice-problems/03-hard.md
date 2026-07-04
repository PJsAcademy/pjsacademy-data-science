# 🔴 Hard — Problems 76–100

The interview-deciding tier: window functions, ranking, running totals, LAG/LEAD, top-N-per-group, gaps & islands, pivots, and recursion. This is where Snowflake's `QUALIFY` shines. Run [00-schema.sql](00-schema.sql) first.

> A few problems introduce a tiny extra table (given inline) for patterns the base schema can't show (e.g., logins for streaks).

---

### 76. Rank employees by salary (RANK)
```sql
-- A window function computes across a set of rows "related to" the current row.
-- RANK() OVER (ORDER BY salary DESC) numbers rows by salary; ties share a rank.
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;
```
❄️ **Snowflake:** identical.
💬 `RANK` leaves gaps after ties (1,2,2,4); `DENSE_RANK` doesn't (1,2,2,3); `ROW_NUMBER` is always unique (1,2,3,4).

---

### 77. Second highest salary (window-function way)
```sql
SELECT DISTINCT salary AS second_highest
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 2;
```
❄️ **Snowflake (cleaner with QUALIFY):**
```sql
SELECT DISTINCT salary
FROM employees
QUALIFY DENSE_RANK() OVER (ORDER BY salary DESC) = 2;
```
💬 `DENSE_RANK = 2` gives the 2nd distinct salary. `QUALIFY` filters window results without a subquery — a Snowflake superpower.

---

### 78. Nth highest salary (generalise to N=3)
```sql
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 3;
```
❄️ **Snowflake:** `... QUALIFY DENSE_RANK() OVER (ORDER BY salary DESC) = 3;`
💬 Change the number to get any Nth. Handles ties correctly via `DENSE_RANK`.

---

### 79. Highest-paid employee in each department (top-1-per-group)
```sql
SELECT dept_id, name, salary
FROM (
    SELECT dept_id, name, salary,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
) t
WHERE rn = 1;
```
❄️ **Snowflake:**
```sql
SELECT dept_id, name, salary
FROM employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1;
```
💬 `PARTITION BY dept_id` restarts the numbering per department — the key idea behind "per group" analytics.

---

### 80. Salary rank within each department
```sql
SELECT name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```
❄️ **Snowflake:** identical.

---

### 81. Each employee's salary vs their department average
```sql
-- AVG as a window keeps every row AND shows the group average alongside
SELECT name, dept_id, salary,
       ROUND(AVG(salary) OVER (PARTITION BY dept_id), 0) AS dept_avg,
       salary - AVG(salary) OVER (PARTITION BY dept_id) AS diff
FROM employees;
```
❄️ **Snowflake:** identical.
💬 Unlike `GROUP BY` (which collapses rows), a window aggregate **keeps every row** and attaches the group value — perfect for comparisons.

---

### 82. Top 2 earners per department
```sql
SELECT dept_id, name, salary
FROM (
    SELECT dept_id, name, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk <= 2;
```
❄️ **Snowflake:** `... QUALIFY DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 2;`
💬 The canonical "top-N-per-group" — memorise this shape; it appears in nearly every SQL interview.

---

### 83. Running total of revenue by order date
```sql
-- SUM as a window with ORDER BY accumulates row by row
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
       AS running_total
FROM orders;
```
❄️ **Snowflake:** identical.
💬 The frame `UNBOUNDED PRECEDING → CURRENT ROW` = "everything up to and including this row" = a running total.

---

### 84. Running total of spend per customer
```sql
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS cust_running
FROM orders;
```
❄️ **Snowflake:** identical.
💬 `PARTITION BY customer_id` resets the accumulation for each customer.

---

### 85. Month-over-month revenue change (LAG)
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS mth, SUM(amount) AS revenue
    FROM orders GROUP BY 1
)
SELECT mth, revenue,
       LAG(revenue) OVER (ORDER BY mth) AS prev_month,
       revenue - LAG(revenue) OVER (ORDER BY mth) AS change
FROM monthly;
```
❄️ **Snowflake:** identical (`DATE_TRUNC` is native).
💬 `LAG` grabs the previous row's value — the standard tool for period-over-period comparisons.

---

### 86. Days between each customer's consecutive orders (LAG on dates)
```sql
SELECT customer_id, order_date,
       LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order,
       DATEDIFF('day',
                LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date),
                order_date) AS days_since_prev
FROM orders;
```
❄️ **Snowflake:** identical. (Standard SQL: `order_date - LAG(order_date) OVER (...)` in Postgres.)

---

### 87. First and latest order per customer in one row (FIRST_VALUE / LAST_VALUE)
```sql
SELECT DISTINCT customer_id,
       FIRST_VALUE(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS first_order,
       LAST_VALUE(order_date)  OVER (PARTITION BY customer_id ORDER BY order_date
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order
FROM orders;
```
❄️ **Snowflake:** identical.
💬 ⚠️ `LAST_VALUE` needs the full-frame clause, else it only sees up to the current row (a classic bug).

---

### 88. Each category's share of total revenue (RATIO_TO_REPORT)
```sql
SELECT p.category,
       SUM(o.amount) AS revenue,
       ROUND(RATIO_TO_REPORT(SUM(o.amount)) OVER () * 100, 1) AS pct_of_total
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.category;
```
❄️ **Snowflake:** identical (`RATIO_TO_REPORT` is native).
💬 Standard-SQL fallback: `100.0 * SUM(...) / SUM(SUM(...)) OVER ()`.

---

### 89. Quartile (NTILE) of employees by salary
```sql
-- NTILE(4) splits rows into 4 roughly equal buckets
SELECT name, salary,
       NTILE(4) OVER (ORDER BY salary DESC) AS salary_quartile
FROM employees;
```
❄️ **Snowflake:** identical.

---

### 90. Cumulative % of employees (running count / total)
```sql
SELECT name, salary,
       ROUND(100.0 * ROW_NUMBER() OVER (ORDER BY salary DESC)
             / COUNT(*) OVER (), 1) AS cumulative_pct
FROM employees;
```
❄️ **Snowflake:** identical.
💬 `COUNT(*) OVER ()` (empty OVER) = grand total on every row — handy denominator.

---

### 91. Median salary
```sql
-- MEDIAN is a built-in ordered aggregate
SELECT MEDIAN(salary) AS median_salary FROM employees;
```
❄️ **Snowflake:** identical (`MEDIAN` native; also `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)`).
💬 Standard SQL (Postgres): `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)`.

---

### 92. Pivot: revenue per category as columns (conditional aggregation)
```sql
SELECT
  SUM(CASE WHEN p.category = 'Electronics' THEN o.amount ELSE 0 END) AS electronics,
  SUM(CASE WHEN p.category = 'Furniture'   THEN o.amount ELSE 0 END) AS furniture
FROM orders o JOIN products p ON o.product_id = p.product_id;
```
❄️ **Snowflake (native PIVOT):**
```sql
SELECT * FROM (
  SELECT p.category, o.amount FROM orders o JOIN products p ON o.product_id=p.product_id
) PIVOT (SUM(amount) FOR category IN ('Electronics','Furniture'));
```
💬 Conditional aggregation is the portable pivot; Snowflake's `PIVOT` is the native shortcut.

---

### 93. Consecutive login days per user — the "islands" problem
*(Add a small table for this classic)*
```sql
-- logins(user_id, login_date). Find streaks of consecutive days.
-- Trick: (date - ROW_NUMBER days) is constant within a consecutive run
WITH ranked AS (
  SELECT user_id, login_date,
         DATEADD('day',
                 -ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date),
                 login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end, COUNT(*) AS streak_len
FROM ranked
GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```
❄️ **Snowflake:** identical (`DATEADD` native). Postgres: `login_date - ROW_NUMBER() OVER(...) * INTERVAL '1 day'`.
💬 **Gaps-and-islands**: subtracting a row counter from a date makes consecutive dates map to the same constant — group by it to find streaks. A top interview pattern.

---

### 94. Find the gaps — missing IDs in a sequence
```sql
-- Where the next order_id jumps by more than 1, there's a gap
SELECT order_id + 1 AS gap_start,
       next_id - 1 AS gap_end
FROM (
  SELECT order_id,
         LEAD(order_id) OVER (ORDER BY order_id) AS next_id
  FROM orders
) t
WHERE next_id - order_id > 1;
```
❄️ **Snowflake:** identical.
💬 `LEAD` looks at the next row; a jump > 1 reveals missing IDs.

---

### 95. Employees earning the same salary as someone else (duplicates via window)
```sql
SELECT name, salary
FROM (
    SELECT name, salary,
           COUNT(*) OVER (PARTITION BY salary) AS same_sal_count
    FROM employees
) t
WHERE same_sal_count > 1;
```
❄️ **Snowflake:** `... QUALIFY COUNT(*) OVER (PARTITION BY salary) > 1;`
💬 A partitioned `COUNT(*)` tags every row with how many share its salary — filter > 1 to find duplicates.

---

### 96. Rank customers by spend and keep only the top 3 (dense)
```sql
WITH spend AS (
    SELECT customer_id, SUM(amount) AS total
    FROM orders GROUP BY customer_id
)
SELECT customer_id, total,
       DENSE_RANK() OVER (ORDER BY total DESC) AS rnk
FROM spend
QUALIFY rnk <= 3;   -- Snowflake
```
❄️ **Standard SQL:** wrap in a subquery and filter `WHERE rnk <= 3`.

---

### 97. Recursive CTE — the full management chain (org hierarchy)
```sql
-- Start at the CEO, then repeatedly join to find each person's reports
WITH RECURSIVE org AS (
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL          -- anchor: the top
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, o.level + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.emp_id   -- recursive step
)
SELECT level, name FROM org ORDER BY level, name;
```
❄️ **Snowflake:** identical (`WITH RECURSIVE` supported).
💬 Recursion = anchor (starting rows) + recursive member (rows built from the previous step) until nothing new is added. The tool for trees/hierarchies.

---

### 98. Recursive CTE — generate a number series 1..10
```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums;
```
❄️ **Snowflake:** identical. Useful for building calendars/date spines to fill gaps.

---

### 99. Fill missing months with zero revenue (date spine + LEFT JOIN)
```sql
WITH RECURSIVE months AS (
    SELECT DATE '2023-06-01' AS m
    UNION ALL
    SELECT DATEADD('month', 1, m) FROM months WHERE m < DATE '2023-08-01'
)
SELECT m,
       COALESCE(SUM(o.amount), 0) AS revenue
FROM months
LEFT JOIN orders o ON DATE_TRUNC('month', o.order_date) = m
GROUP BY m
ORDER BY m;
```
❄️ **Snowflake:** identical.
💬 Reporting must show months with **zero** activity — a generated date spine + `LEFT JOIN` + `COALESCE` does it. Common real-world requirement.

---

### 100. Year-over-year style growth % per month (LAG + calculation) — Capstone
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS mth, SUM(amount) AS revenue
    FROM orders GROUP BY 1
)
SELECT mth, revenue,
       LAG(revenue) OVER (ORDER BY mth) AS prev,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY mth))
             / NULLIF(LAG(revenue) OVER (ORDER BY mth), 0), 1) AS growth_pct
FROM monthly
ORDER BY mth;
```
❄️ **Snowflake:** identical.
💬 `NULLIF(x, 0)` guards against divide-by-zero when the previous month is 0/NULL. This single query combines CTEs, window functions, and safe math — everything from this tier.

---

## 🎓 You Finished All 100!
You've now practised every pattern SQL interviews throw at you: joins, subqueries, CTEs, all window functions, ranking, running totals, LAG/LEAD, gaps-and-islands, pivots, and recursion — in both standard SQL and Snowflake.

**Next steps:**
- Redo every problem you needed help on, one week later.
- Try the same patterns on a dataset *you* care about.
- Put "solved 100 SQL problems incl. window functions & recursion in SQL + Snowflake" on your resume.

⬅️ Back to [Easy](01-easy.md) · [Medium](02-medium.md) · [Problem Index](README.md)

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com) · hello@pjsacademy.com*
