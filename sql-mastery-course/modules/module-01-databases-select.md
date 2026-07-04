# Module 01 — Databases & SELECT Basics

> Start from zero: what a database is, and how to ask it for data. By the end you'll confidently read any table.

---

## 1.1 What Is a Database?

A **database** is an organised collection of data. The kind we query with SQL is a **relational database** — data lives in **tables**, which are just like spreadsheets:

- A **table** = a grid (e.g., `employees`).
- A **row** = one record (one employee).
- A **column** = one attribute (name, salary, hire_date).
- Each column has a **type** (text, number, date).

```
employees
┌────────┬───────┬─────────┬────────┐
│ emp_id │ name  │ dept_id │ salary │   ← columns
├────────┼───────┼─────────┼────────┤
│   1    │ Asha  │    1    │ 180000 │   ← a row
│   2    │ Ravi  │    1    │ 120000 │
└────────┴───────┴─────────┴────────┘
```

**SQL** (Structured Query Language) is how we talk to the database — ask questions, get answers.

## 1.2 The Sample Database (used all course)

We use 5 related tables: `employees`, `departments`, `customers`, `products`, `orders`. Run the [schema](../practice-problems/00-schema.sql) once to create them. Relationships:
- Each employee belongs to a department (`employees.dept_id → departments.dept_id`).
- Each order belongs to a customer and a product.

## 1.3 SELECT — Asking for Data

The `SELECT` statement retrieves rows. The simplest form:
```sql
SELECT * FROM employees;
```
- `SELECT` = "give me"
- `*` = "all columns"
- `FROM employees` = "from the employees table"

## 1.4 Choosing Columns

`*` is fine for exploring, but in real code you name the columns you want — it's clearer and faster:
```sql
SELECT name, salary FROM employees;
```
Order the columns however you like:
```sql
SELECT salary, name FROM employees;   -- salary first
```

## 1.5 Aliases — Renaming Output

Give a column a friendlier name in the result with `AS`:
```sql
SELECT name AS employee_name,
       salary AS monthly_salary
FROM employees;
```
`AS` is optional (`salary monthly_salary` works) but always write it — clarity wins.

## 1.6 Calculated Columns

You can compute new columns on the fly:
```sql
SELECT name,
       salary AS monthly,
       salary * 12 AS annual        -- arithmetic
FROM employees;
```
Combine text with concatenation (`||` in standard SQL / Snowflake):
```sql
SELECT name || ' works in dept ' || dept_id AS description
FROM employees;
```

## 1.7 DISTINCT — Unique Values

Remove duplicate rows from the result:
```sql
SELECT DISTINCT dept_id FROM employees;   -- each department once
```

## 1.8 LIMIT — Just a Few Rows

Return only the first N rows (great for peeking at big tables):
```sql
SELECT * FROM employees LIMIT 5;
```
❄️ Snowflake also supports `FETCH FIRST 5 ROWS ONLY`.

## 1.9 Comments — Notes in Your SQL

```sql
-- This is a single-line comment
SELECT name        -- you can comment at the end of a line too
FROM employees;
/* This is a
   multi-line comment */
```

## 1.10 Reading a Query (order it runs)

You *write* `SELECT` first, but the database *runs* `FROM` first (get the table), then `SELECT` (pick columns). This matters more later with `WHERE` and `GROUP BY` — keep it in mind.

---

## ✅ Key Takeaways
1. A relational database stores data in **tables** (rows × columns), each column has a type.
2. `SELECT columns FROM table` retrieves data; `*` means all columns.
3. Use `AS` to **alias** (rename) output columns.
4. You can compute **calculated columns** (`salary * 12`) and concatenate text (`||`).
5. `DISTINCT` removes duplicates; `LIMIT` caps the number of rows.
6. The database runs `FROM` before `SELECT`.

## 🏋️ Exercises
1. Select all columns from `products`.
2. Select just `name` and `salary` from `employees`, salary first.
3. Show each product's `name` and its price × 1.18 (with GST) as `price_with_gst`.
4. List the distinct `city` values from `customers`.
5. Show the first 3 rows of `orders`.

**Next:** [Module 02 — Filtering, Sorting & Operators →](module-02-filtering-sorting.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
