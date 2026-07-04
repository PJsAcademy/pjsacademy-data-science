# Module 08 — SQL for Interviews & Real Work

> You know the syntax. This module makes you *fast, correct, and calm* — in interviews and on the job.

---

## 8.1 How to Attack Any SQL Problem

A repeatable method that works even on hard questions:
```
1. Restate the ask in one sentence. What's ONE row of the output?
2. Identify the tables and the keys that join them.
3. Decide the grain: per what? (per customer / per day / per order)
4. Build in layers (CTEs): filter → join → aggregate → rank → label.
5. Test each layer's output before adding the next.
6. Sanity-check: row counts, a known example, NULLs.
```
Interviewers care about your **approach** as much as the answer. Narrate it.

## 8.2 The Patterns That Cover 90% of Interviews

| Pattern | Tool |
|---------|------|
| Nth highest value | `DENSE_RANK`/`LIMIT OFFSET` |
| Top-N per group | window rank + filter (`QUALIFY`) |
| Rows with no match | `LEFT JOIN … IS NULL` / `NOT EXISTS` |
| Duplicates | `GROUP BY … HAVING COUNT(*)>1` or window count |
| Running total | `SUM() OVER (ORDER BY …)` |
| Period-over-period | `LAG`/`LEAD` |
| Consecutive streaks | gaps-and-islands (row_number trick) |
| Pivot | conditional aggregation / `PIVOT` |
| Hierarchy | recursive CTE |

Master these from the [100-problem bank](../practice-problems/README.md) and you'll recognise almost any question instantly.

## 8.3 Classic Questions (know these cold)

**Second-highest salary:**
```sql
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```
**Duplicate emails:**
```sql
SELECT email FROM employees GROUP BY email HAVING COUNT(*) > 1;
```
**Employees earning more than their manager:**
```sql
SELECT e.name FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```
**Customers who never ordered:**
```sql
SELECT c.name FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

## 8.4 Writing Readable SQL (real-world discipline)

- **Uppercase keywords**, lowercase identifiers.
- One clause per line; indent sub-parts.
- **Meaningful aliases** (`e` for employees, `o` for orders).
- **CTEs over deep nesting** — name each step.
- Comment the *why*, not the obvious *what*.
- Consistent formatting — your future self and teammates thank you.

## 8.5 Correctness Habits That Prevent Bugs

- After a join, ask: *could this duplicate rows?* If yes, `COUNT(DISTINCT …)`.
- With NULLs, prefer `NOT EXISTS` over `NOT IN`.
- Integer division truncates — use `100.0 * a / b` for percentages.
- Guard divide-by-zero with `NULLIF(denominator, 0)`.
- `HAVING` for aggregate filters, `WHERE` for row filters.
- Always test with an edge case (empty group, ties, a NULL).

## 8.6 Performance on the Job

- Select only needed columns; filter early.
- Understand your engine: **OLTP** (Postgres/MySQL) uses indexes; **Snowflake** uses pruning + warehouse sizing.
- Read the query plan (`EXPLAIN`) when something is slow.
- Aggregate at the right grain — don't join then dedupe if you can aggregate first.

## 8.7 SQL Across Engines

Core SQL is portable, but dialects differ:
| Task | Standard/Postgres | Snowflake |
|------|-------------------|-----------|
| Case-insensitive match | `ILIKE` (PG) | `ILIKE` |
| Date part | `EXTRACT(MONTH FROM d)` | `MONTH(d)` |
| Date diff | `d2 - d1` | `DATEDIFF('day', d1, d2)` |
| String split | `SPLIT_PART` (PG/SF) | `SPLIT_PART` |
| Filter window | subquery | `QUALIFY` |
| Limit | `LIMIT n` | `LIMIT n` / `FETCH FIRST n` |

Learn one dialect deeply (we teach standard + Snowflake); translating is then easy.

## 8.8 Your Practice Plan

1. Work the [100 problems](../practice-problems/README.md): Easy → Medium → Hard.
2. **Try before peeking.** The struggle is the learning.
3. Redo missed problems a week later.
4. Time yourself on Medium/Hard (interview simulation).
5. Explain your solution out loud — that's what interviews test.

---

## ✅ Key Takeaways
1. Attack problems with a **method**: restate → identify tables/grain → build in layers → test → sanity-check.
2. Learn the **9 core patterns** — they cover ~90% of interviews.
3. Know the **classic questions** (2nd-highest, duplicates, more-than-manager, never-ordered) cold.
4. Write **readable** SQL (CTEs, aliases, formatting) — it's judged.
5. Build **correctness habits**: dedupe after joins, `NOT EXISTS` for NULLs, decimal math, `NULLIF` guards.
6. Core SQL is portable; know your engine's dialect and performance model.

## 🏋️ Exercises
1. Write the second-highest salary query, then generalise it to Nth-highest.
2. Find all duplicate emails in `employees`.
3. Find employees earning more than their manager.
4. List customers who never ordered (two ways: `LEFT JOIN` and `NOT EXISTS`).
5. For each department, return the top earner (window function).
6. Pick 5 problems from the Hard bank and solve them timed.

## 🎓 Course Complete!
You now have the full SQL toolkit — from `SELECT` to recursion — plus the interview method. Next: grind the [100-problem bank](../practice-problems/README.md), then apply SQL in the **Snowflake** or **Data Science** courses.

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
