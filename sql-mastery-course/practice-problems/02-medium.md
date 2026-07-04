# 🟡 Medium — Problems 36–75

Multi-table joins, subqueries, CTEs, CASE, conditional aggregation, anti-joins, date/string logic — the bread and butter of SQL interviews. Run [00-schema.sql](00-schema.sql) first.

---

### 36. Employees who earn more than their manager
*(Classic interview Q — self join)*
```sql
-- Join employees to themselves: e = worker, m = their manager
SELECT e.name AS employee, e.salary, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```
❄️ **Snowflake:** identical.
💬 A **self join** treats one table as two. `m.emp_id = e.manager_id` links each worker to their boss.

---

### 37. Each employee with their manager's name (show CEO too)
```sql
-- LEFT JOIN so the CEO (manager_id NULL) still appears
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```
❄️ **Snowflake:** identical.
💬 With an inner join the CEO would vanish (no manager to match). `LEFT JOIN` keeps them, manager = NULL.

---

### 38. Customers who never placed an order
*(Classic — anti join)*
```sql
-- LEFT JOIN then keep only rows with no matching order
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```
❄️ **Snowflake:** identical.
💬 The unmatched customers get NULL order columns; filtering `IS NULL` isolates them. Alternative: `WHERE customer_id NOT IN (SELECT customer_id FROM orders)`.

---

### 39. Same, using NOT EXISTS
```sql
SELECT c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```
❄️ **Snowflake:** identical.
💬 `NOT EXISTS` is often the fastest anti-join and handles NULLs safely (unlike `NOT IN`).

---

### 40. Second highest salary
*(The most-asked SQL interview question)*
```sql
-- Highest salary that is strictly below the maximum
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```
❄️ **Snowflake:** identical. (Window-function version appears in Hard #77.)
💬 Robust even with ties. Returns NULL if there's no second value — usually the desired behaviour.

---

### 41. Departments and their total salary
```sql
SELECT d.dept_name, SUM(e.salary) AS total_salary
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name;
```
❄️ **Snowflake:** identical.

---

### 42. Department with the highest average salary
```sql
SELECT dept_id, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
ORDER BY avg_sal DESC
LIMIT 1;
```
❄️ **Snowflake:** identical.
💬 Group → average → sort → take one. (Ties broken arbitrarily; window functions handle ties better — Hard tier.)

---

### 43. Count employees hired per year
```sql
-- Extract the year, then group by it
SELECT EXTRACT(YEAR FROM hire_date) AS yr, COUNT(*) AS hires
FROM employees
GROUP BY EXTRACT(YEAR FROM hire_date)
ORDER BY yr;
```
❄️ **Snowflake:** `SELECT YEAR(hire_date) AS yr, COUNT(*) ... GROUP BY YEAR(hire_date)` — `YEAR()` is cleaner.

---

### 44. Label salaries as High / Medium / Low (CASE)
```sql
SELECT name, salary,
  CASE
    WHEN salary >= 120000 THEN 'High'
    WHEN salary >= 80000  THEN 'Medium'
    ELSE 'Low'
  END AS salary_band
FROM employees;
```
❄️ **Snowflake:** identical.
💬 `CASE` is SQL's if/else. Conditions checked top-down; first TRUE wins.

---

### 45. Count employees in each salary band (CASE + GROUP BY)
```sql
SELECT
  CASE WHEN salary >= 120000 THEN 'High'
       WHEN salary >= 80000  THEN 'Medium'
       ELSE 'Low' END AS band,
  COUNT(*) AS n
FROM employees
GROUP BY
  CASE WHEN salary >= 120000 THEN 'High'
       WHEN salary >= 80000  THEN 'Medium'
       ELSE 'Low' END;
```
❄️ **Snowflake:** identical (can also `GROUP BY band` — Snowflake allows grouping by alias).

---

### 46. Conditional aggregation — count high earners per department
```sql
-- SUM(CASE...) counts rows meeting a condition, per group
SELECT dept_id,
       SUM(CASE WHEN salary >= 100000 THEN 1 ELSE 0 END) AS high_earners,
       COUNT(*) AS total
FROM employees
GROUP BY dept_id;
```
❄️ **Snowflake:** identical (or `COUNT_IF(salary >= 100000)` — a Snowflake shortcut).
💬 `SUM(CASE WHEN cond THEN 1 ELSE 0 END)` is the universal "count rows matching a condition within a group" pattern.

---

### 47. Total revenue per product category
```sql
SELECT p.category, SUM(o.amount) AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```
❄️ **Snowflake:** identical.

---

### 48. Customers and their total spend, highest first
```sql
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name
ORDER BY total_spent DESC;
```
❄️ **Snowflake:** identical.

---

### 49. Customers who spent more than 50000
```sql
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name
HAVING SUM(o.amount) > 50000;
```
❄️ **Snowflake:** identical.
💬 Filter on an aggregate → `HAVING`, not `WHERE`.

---

### 50. Average order value per customer using a CTE
```sql
-- A CTE (WITH) is a named temporary result you can reference below
WITH customer_orders AS (
    SELECT customer_id, COUNT(*) AS num_orders, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, total / num_orders AS avg_order_value
FROM customer_orders;
```
❄️ **Snowflake:** identical.
💬 CTEs make queries readable — build the summary once, use it below.

---

### 51. Products never ordered
```sql
SELECT product_name FROM products
WHERE product_id NOT IN (SELECT product_id FROM orders);
```
❄️ **Snowflake:** identical.
💬 ⚠️ If the subquery could contain NULLs, `NOT IN` breaks — prefer `NOT EXISTS` there. Here product_id is never NULL, so it's safe.

---

### 52. Each department's employee count and average salary
```sql
SELECT d.dept_name,
       COUNT(e.emp_id) AS headcount,
       ROUND(AVG(e.salary), 0) AS avg_salary
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name;
```
❄️ **Snowflake:** identical.
💬 `LEFT JOIN` + `COUNT(e.emp_id)` → empty departments correctly show 0.

---

### 53. Orders above the average order amount (correlated idea)
```sql
SELECT order_id, amount FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders);
```
❄️ **Snowflake:** identical.

---

### 54. Each customer's most recent order date
```sql
SELECT customer_id, MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id;
```
❄️ **Snowflake:** identical.

---

### 55. Number of distinct products each customer bought
```sql
SELECT customer_id, COUNT(DISTINCT product_id) AS unique_products
FROM orders
GROUP BY customer_id;
```
❄️ **Snowflake:** identical.
💬 `COUNT(DISTINCT ...)` counts unique values — a customer buying the same product twice counts once.

---

### 56. Combine employee and customer names into one list (UNION)
```sql
-- UNION stacks two result sets and removes duplicates
SELECT name, 'employee' AS type FROM employees
UNION
SELECT name, 'customer' AS type FROM customers;
```
❄️ **Snowflake:** identical. Use `UNION ALL` to keep duplicates (faster — no dedupe).

---

### 57. Replace NULL email with a placeholder (COALESCE)
```sql
-- COALESCE returns the first non-NULL argument
SELECT name, COALESCE(email, 'no-email@pjs.com') AS email
FROM employees;
```
❄️ **Snowflake:** identical (`IFNULL` and `NVL` also work).

---

### 58. Employees whose name contains 'a' (case-insensitive)
```sql
SELECT name FROM employees
WHERE LOWER(name) LIKE '%a%';
```
❄️ **Snowflake:** `WHERE name ILIKE '%a%'` — `ILIKE` is built-in case-insensitive.

---

### 59. Length of each employee's name
```sql
SELECT name, LENGTH(name) AS name_length
FROM employees;
```
❄️ **Snowflake:** identical (`LENGTH` works; `LEN` also).

---

### 60. Uppercase department names
```sql
SELECT UPPER(dept_name) AS dept_upper FROM departments;
```
❄️ **Snowflake:** identical.

---

### 61. Extract domain from email
```sql
-- SUBSTRING from the char after '@' to the end
SELECT name,
       SUBSTRING(email FROM POSITION('@' IN email) + 1) AS domain
FROM employees
WHERE email IS NOT NULL;
```
❄️ **Snowflake:** `SPLIT_PART(email, '@', 2) AS domain` — far cleaner.
💬 Learn Snowflake's `SPLIT_PART` — it beats manual substring math.

---

### 62. Months an employee has been at the company
```sql
SELECT name,
       (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM hire_date)) * 12
       + (EXTRACT(MONTH FROM CURRENT_DATE) - EXTRACT(MONTH FROM hire_date)) AS months
FROM employees;
```
❄️ **Snowflake:** `DATEDIFF('month', hire_date, CURRENT_DATE) AS months` — one clean function.
💬 Snowflake's `DATEDIFF(part, start, end)` is a huge quality-of-life win over manual date math.

---

### 63. Orders placed in June 2023
```sql
SELECT order_id, order_date FROM orders
WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30';
```
❄️ **Snowflake:** identical, or `WHERE DATE_TRUNC('month', order_date) = '2023-06-01'`.

---

### 64. Revenue per month
```sql
SELECT EXTRACT(MONTH FROM order_date) AS mth, SUM(amount) AS revenue
FROM orders
GROUP BY EXTRACT(MONTH FROM order_date)
ORDER BY mth;
```
❄️ **Snowflake:** `SELECT DATE_TRUNC('month', order_date) AS mth, SUM(amount) ... GROUP BY 1` — `DATE_TRUNC` keeps the year too.

---

### 65. Departments where every employee earns > 60000 (NOT EXISTS)
```sql
SELECT d.dept_name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1 FROM employees e
    WHERE e.dept_id = d.dept_id AND e.salary <= 60000
)
AND EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id);
```
❄️ **Snowflake:** identical.
💬 "All employees satisfy X" = "no employee violates X". The extra `EXISTS` excludes empty departments.

---

### 66. Top 2 highest-paid employees per... (preview — full version in Hard)
```sql
-- Simple version: overall top 2 (per-group needs window functions, Hard #82)
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 2;
```
❄️ **Snowflake:** identical.

---

### 67. Customers with more than one order
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;
```
❄️ **Snowflake:** identical.

---

### 68. Average quantity per product category
```sql
SELECT p.category, AVG(o.quantity) AS avg_qty
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category;
```
❄️ **Snowflake:** identical.

---

### 69. Percentage of total revenue by category
```sql
SELECT p.category,
       SUM(o.amount) AS revenue,
       ROUND(100.0 * SUM(o.amount) / (SELECT SUM(amount) FROM orders), 1) AS pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category;
```
❄️ **Snowflake:** identical. (Window `RATIO_TO_REPORT` does this elegantly — Hard #88.)
💬 `100.0 *` (not `100 *`) forces decimal division — a common gotcha with integer math.

---

### 70. Employees in the same department as 'Ravi'
```sql
SELECT name FROM employees
WHERE dept_id = (SELECT dept_id FROM employees WHERE name = 'Ravi')
  AND name <> 'Ravi';
```
❄️ **Snowflake:** identical.

---

### 71. Manager and how many people they manage
```sql
SELECT m.name AS manager, COUNT(e.emp_id) AS reports
FROM employees m
JOIN employees e ON e.manager_id = m.emp_id
GROUP BY m.name
ORDER BY reports DESC;
```
❄️ **Snowflake:** identical.

---

### 72. Three-table join: customer, product, amount per order
```sql
SELECT o.order_id, c.name AS customer, p.product_name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id;
```
❄️ **Snowflake:** identical.
💬 Chain joins — each `JOIN ... ON` adds one more table on a matching key.

---

### 73. Categories with revenue above the average category revenue (CTE)
```sql
WITH cat_rev AS (
    SELECT p.category, SUM(o.amount) AS revenue
    FROM orders o JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
)
SELECT category, revenue FROM cat_rev
WHERE revenue > (SELECT AVG(revenue) FROM cat_rev);
```
❄️ **Snowflake:** identical.

---

### 74. First and last order date overall, and the span
```sql
SELECT MIN(order_date) AS first_order,
       MAX(order_date) AS last_order
FROM orders;
```
❄️ **Snowflake:** add `DATEDIFF('day', MIN(order_date), MAX(order_date)) AS span_days`.

---

### 75. Flag whether each employee is above or below company average (CASE + subquery)
```sql
SELECT name, salary,
  CASE WHEN salary > (SELECT AVG(salary) FROM employees)
       THEN 'Above average' ELSE 'Below average' END AS vs_avg
FROM employees;
```
❄️ **Snowflake:** identical.

---

➡️ Continue to [🔴 Hard — Problems 76–100](03-hard.md)

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
