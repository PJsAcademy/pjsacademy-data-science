# 🟢 Easy — Problems 1–35

Foundations: SELECT, WHERE, ORDER BY, LIMIT, basic aggregates, simple joins.
Run [00-schema.sql](00-schema.sql) first. Try each yourself before reading the solution.

---

### 1. Select all employees
**Task:** Return every column for all employees.
```sql
-- SELECT * returns all columns; FROM names the table
SELECT * FROM employees;
```
❄️ **Snowflake:** identical.
💬 The simplest query. `*` = all columns. In real code, list columns explicitly instead of `*` for clarity and speed.

---

### 2. Names and salaries only
**Task:** Return just the name and salary of every employee.
```sql
-- List the specific columns you want, comma-separated
SELECT name, salary FROM employees;
```
❄️ **Snowflake:** identical.
💬 Selecting specific columns is faster and clearer than `*`.

---

### 3. Employees earning more than 100000
```sql
-- WHERE filters rows; only rows where the condition is TRUE are returned
SELECT name, salary
FROM employees
WHERE salary > 100000;
```
❄️ **Snowflake:** identical.
💬 `WHERE` runs before the columns are returned — it decides *which rows* survive.

---

### 4. Employees in department 1
```sql
SELECT name FROM employees
WHERE dept_id = 1;   -- = tests exact equality
```
❄️ **Snowflake:** identical.

---

### 5. Employees NOT in department 2
```sql
SELECT name FROM employees
WHERE dept_id <> 2;  -- <> means "not equal" (!= also works)
```
❄️ **Snowflake:** identical.
💬 ⚠️ Rows where `dept_id` is NULL are **not** returned — NULL comparisons yield UNKNOWN, not TRUE.

---

### 6. Sort employees by salary (highest first)
```sql
SELECT name, salary FROM employees
ORDER BY salary DESC;   -- DESC = descending; default is ASC
```
❄️ **Snowflake:** identical.

---

### 7. Top 3 highest-paid employees
```sql
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 3;   -- LIMIT caps the number of rows returned
```
❄️ **Snowflake:** identical (`LIMIT 3` works; `FETCH FIRST 3 ROWS ONLY` also valid).
💬 Sort first, then limit — you get the top 3 by salary.

---

### 8. Count the employees
```sql
SELECT COUNT(*) AS total_employees
FROM employees;   -- COUNT(*) counts rows; AS renames the output column
```
❄️ **Snowflake:** identical.

---

### 9. Number of employees with an email
```sql
-- COUNT(column) ignores NULLs, so this counts only non-NULL emails
SELECT COUNT(email) AS with_email
FROM employees;
```
❄️ **Snowflake:** identical.
💬 Key distinction: `COUNT(*)` counts all rows; `COUNT(col)` counts non-NULLs. Nina's NULL email is excluded.

---

### 10. Highest and lowest salary
```sql
SELECT MAX(salary) AS highest,
       MIN(salary) AS lowest
FROM employees;
```
❄️ **Snowflake:** identical.

---

### 11. Average salary
```sql
SELECT AVG(salary) AS avg_salary
FROM employees;
```
❄️ **Snowflake:** identical.
💬 `AVG` ignores NULLs. Round it with `ROUND(AVG(salary), 2)`.

---

### 12. Total payroll
```sql
SELECT SUM(salary) AS total_payroll
FROM employees;
```
❄️ **Snowflake:** identical.

---

### 13. Employees hired after 2021
```sql
SELECT name, hire_date FROM employees
WHERE hire_date > '2021-12-31';  -- dates compare like numbers
```
❄️ **Snowflake:** identical. Tip: `WHERE YEAR(hire_date) > 2021` also works in Snowflake.

---

### 14. Employees hired in 2021
```sql
SELECT name FROM employees
WHERE hire_date BETWEEN '2021-01-01' AND '2021-12-31';
-- BETWEEN is inclusive on both ends
```
❄️ **Snowflake:** identical, or `WHERE YEAR(hire_date) = 2021`.

---

### 15. Employees whose name starts with 'A'
```sql
SELECT name FROM employees
WHERE name LIKE 'A%';   -- % = any sequence of characters
```
❄️ **Snowflake:** identical. Case-insensitive version: `WHERE name ILIKE 'a%'`.
💬 `%` = zero or more chars, `_` = exactly one char.

---

### 16. Salaries between 80000 and 120000
```sql
SELECT name, salary FROM employees
WHERE salary BETWEEN 80000 AND 120000;
```
❄️ **Snowflake:** identical.

---

### 17. Employees in departments 1 or 3
```sql
SELECT name, dept_id FROM employees
WHERE dept_id IN (1, 3);   -- IN = matches any value in the list
```
❄️ **Snowflake:** identical.
💬 `IN (1,3)` is cleaner than `dept_id = 1 OR dept_id = 3`.

---

### 18. Employees with no manager (the CEO)
```sql
SELECT name FROM employees
WHERE manager_id IS NULL;   -- use IS NULL, never = NULL
```
❄️ **Snowflake:** identical.
💬 ⚠️ `= NULL` never works — NULL isn't a value you can equal. Always `IS NULL` / `IS NOT NULL`.

---

### 19. Distinct departments that have employees
```sql
SELECT DISTINCT dept_id FROM employees;  -- DISTINCT removes duplicates
```
❄️ **Snowflake:** identical.

---

### 20. Rename salary to monthly (aliasing)
```sql
SELECT name, salary AS monthly_salary
FROM employees;
```
❄️ **Snowflake:** identical.

---

### 21. Employees ordered by department, then salary
```sql
SELECT name, dept_id, salary FROM employees
ORDER BY dept_id ASC, salary DESC;  -- sort by dept, then salary within dept
```
❄️ **Snowflake:** identical.

---

### 22. All customers from Mumbai
```sql
SELECT name FROM customers
WHERE city = 'Mumbai';
```
❄️ **Snowflake:** identical (`WHERE city ILIKE 'mumbai'` for case-insensitive).

---

### 23. Products cheaper than 10000
```sql
SELECT product_name, price FROM products
WHERE price < 10000;
```
❄️ **Snowflake:** identical.

---

### 24. Count products per category
```sql
-- GROUP BY collapses rows sharing a category into one group;
-- COUNT(*) then counts rows within each group
SELECT category, COUNT(*) AS num_products
FROM products
GROUP BY category;
```
❄️ **Snowflake:** identical.
💬 Whenever you aggregate "per something", that something goes in `GROUP BY`.

---

### 25. Average price per category
```sql
SELECT category, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category;
```
❄️ **Snowflake:** identical.

---

### 26. Number of employees per department
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id;
```
❄️ **Snowflake:** identical.

---

### 27. Total order amount per customer
```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id;
```
❄️ **Snowflake:** identical.

---

### 28. Departments with more than 1 employee
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 1;   -- HAVING filters GROUPS (WHERE filters rows)
```
❄️ **Snowflake:** identical.
💬 `WHERE` filters rows *before* grouping; `HAVING` filters *after* grouping. You can't use aggregates in `WHERE`.

---

### 29. List employees with their department name (JOIN)
```sql
-- JOIN matches each employee to its department via the shared dept_id
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```
❄️ **Snowflake:** identical.
💬 `e` and `d` are table aliases — shorthand so you can write `e.name` instead of `employees.name`.

---

### 30. Employees and their department location
```sql
SELECT e.name, d.location
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```
❄️ **Snowflake:** identical.

---

### 31. Orders with the customer's name
```sql
SELECT o.order_id, c.name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```
❄️ **Snowflake:** identical.

---

### 32. Orders with product names
```sql
SELECT o.order_id, p.product_name, o.quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id;
```
❄️ **Snowflake:** identical.

---

### 33. All departments, even those with no employees (LEFT JOIN)
```sql
-- LEFT JOIN keeps every department; employees with no match show as NULL
SELECT d.dept_name, e.name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id;
```
❄️ **Snowflake:** identical.
💬 A plain `JOIN` (inner) would drop departments with no employees. `LEFT JOIN` keeps the left table's rows regardless.

---

### 34. Count orders per product (including unordered products)
```sql
SELECT p.product_name, COUNT(o.order_id) AS times_ordered
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_name;
```
❄️ **Snowflake:** identical.
💬 `COUNT(o.order_id)` counts non-NULLs, so unordered products correctly show 0 (not 1).

---

### 35. Employees earning above the company average
```sql
-- The subquery computes one number (the average); the outer query compares to it
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
❄️ **Snowflake:** identical.
💬 A **scalar subquery** returns a single value you can compare against — your first taste of subqueries (Medium tier goes deeper).

---

➡️ Continue to [🟡 Medium — Problems 36–75](02-medium.md)

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
