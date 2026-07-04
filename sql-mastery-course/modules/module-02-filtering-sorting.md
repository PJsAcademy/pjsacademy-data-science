# Module 02 — Filtering, Sorting & Operators

> Rarely do you want *all* rows. This module is about asking for exactly the rows you need, in the order you want.

---

## 2.1 WHERE — Keeping Only the Rows You Want

`WHERE` filters rows by a condition. Only rows where the condition is **TRUE** are returned.
```sql
SELECT name, salary FROM employees
WHERE salary > 100000;
```
`WHERE` runs after `FROM` but before `SELECT` picks columns — it decides which rows survive.

## 2.2 Comparison Operators

| Operator | Meaning |
|----------|---------|
| `=` | equal |
| `<>` or `!=` | not equal |
| `>` `<` `>=` `<=` | greater/less than (or equal) |

```sql
SELECT name FROM employees WHERE dept_id = 1;
SELECT name FROM employees WHERE salary >= 90000;
SELECT name FROM employees WHERE dept_id <> 2;
```

## 2.3 Combining Conditions: AND, OR, NOT

```sql
-- Both must be true
SELECT name FROM employees WHERE dept_id = 1 AND salary > 100000;
-- Either can be true
SELECT name FROM employees WHERE dept_id = 1 OR dept_id = 3;
-- Negate
SELECT name FROM employees WHERE NOT dept_id = 2;
```
> ⚠️ `AND` binds tighter than `OR`. Use parentheses to be explicit:
> `WHERE (dept_id = 1 OR dept_id = 2) AND salary > 90000`.

## 2.4 BETWEEN — Ranges

Inclusive on both ends:
```sql
SELECT name, salary FROM employees
WHERE salary BETWEEN 80000 AND 120000;   -- 80000 and 120000 included
```

## 2.5 IN — Match a List

Cleaner than many `OR`s:
```sql
SELECT name FROM employees WHERE dept_id IN (1, 3);
-- same as: WHERE dept_id = 1 OR dept_id = 3
SELECT name FROM employees WHERE dept_id NOT IN (2, 4);
```

## 2.6 LIKE — Pattern Matching

For partial text matches. Wildcards:
- `%` = any sequence of characters (including none)
- `_` = exactly one character

```sql
SELECT name FROM employees WHERE name LIKE 'A%';    -- starts with A
SELECT name FROM employees WHERE name LIKE '%a';    -- ends with a
SELECT name FROM employees WHERE name LIKE '%in%';  -- contains "in"
SELECT name FROM employees WHERE name LIKE '_a%';   -- 2nd letter is a
```
❄️ Snowflake: `ILIKE` is case-insensitive (`WHERE name ILIKE 'a%'`).

## 2.7 NULL — the Absence of a Value

`NULL` means "unknown / no value" — it is **not** zero or empty string. You **cannot** compare it with `=`:
```sql
-- WRONG: returns nothing, ever
SELECT name FROM employees WHERE email = NULL;
-- RIGHT:
SELECT name FROM employees WHERE email IS NULL;
SELECT name FROM employees WHERE email IS NOT NULL;
```
> ⚠️ Any comparison with NULL yields UNKNOWN (not TRUE), so those rows are excluded. This trips up everyone at first — remember `IS NULL` / `IS NOT NULL`.

## 2.8 ORDER BY — Sorting Results

```sql
SELECT name, salary FROM employees
ORDER BY salary DESC;    -- highest first; ASC (default) = lowest first
```
Sort by multiple columns (tie-breakers):
```sql
SELECT name, dept_id, salary FROM employees
ORDER BY dept_id ASC, salary DESC;   -- by dept, then salary within dept
```
You can order by a column you didn't select, or by position (`ORDER BY 2` = 2nd selected column — handy but less readable).

## 2.9 LIMIT with ORDER BY — Top-N

The classic "top N" pattern: sort, then limit.
```sql
-- Top 3 highest-paid employees
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 3;
```

## 2.10 Order of Operations (mental model)

```
FROM      → get the table
WHERE     → filter rows
SELECT    → pick/compute columns
ORDER BY  → sort
LIMIT     → cap rows
```
This is why you can't use a `SELECT` alias in `WHERE` (WHERE runs first) but often can in `ORDER BY` (which runs after SELECT).

---

## ✅ Key Takeaways
1. `WHERE` filters rows using comparison operators (`=`, `<>`, `>`, …).
2. Combine conditions with `AND`/`OR`/`NOT`; use parentheses to control precedence.
3. `BETWEEN` (ranges), `IN` (lists), `LIKE` (patterns with `%` and `_`).
4. `NULL` is unknown — use `IS NULL` / `IS NOT NULL`, never `= NULL`.
5. `ORDER BY col DESC/ASC` sorts; add columns for tie-breakers.
6. Sort + `LIMIT` = the top-N pattern. Remember the FROM→WHERE→SELECT→ORDER BY→LIMIT order.

## 🏋️ Exercises
1. List employees earning more than 90,000, highest salary first.
2. Find employees in departments 1 or 4 (use `IN`).
3. Find employees whose name contains the letter "a".
4. Find employees with no email (`IS NULL`).
5. Show the 2 cheapest products.
6. List employees hired between '2021-01-01' and '2021-12-31' (use `BETWEEN`).

**Next:** [Module 03 — Aggregations & GROUP BY →](module-03-aggregations.md)

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
