# 🧩 100 SQL Practice Problems — PJ's Academy

LeetCode-style problems. Every solution comes in **standard SQL** AND **Snowflake**, with line-by-line comments explaining the *why*, not just the *what*.

> First, run the [shared schema](00-schema.sql) to create the sample tables (employees, departments, customers, products, orders).

---

## 📚 The Bank

| Tier | Problems | Focus | File |
|------|----------|-------|------|
| 🟢 **Easy** | 1–35 | SELECT, WHERE, ORDER BY, basic aggregates, simple joins | [01-easy.md](01-easy.md) |
| 🟡 **Medium** | 36–75 | Multi-joins, subqueries, CTEs, GROUP BY + HAVING, CASE | [02-medium.md](02-medium.md) |
| 🔴 **Hard** | 76–100 | Window functions, recursion, top-N-per-group, gaps & islands | [03-hard.md](03-hard.md) |

## 🎯 How To Practice
1. Read the problem. **Try it yourself first** (cover the solution).
2. Compare with the standard-SQL solution + comments.
3. Study the **Snowflake** version — note where it differs (e.g., `QUALIFY`, date functions).
4. Mark problems you missed. **Redo them in a week.**

## 🧠 SQL vs Snowflake — quick orientation
Most SQL is identical across engines. Snowflake adds power features you'll see used here:
- **`QUALIFY`** — filter window-function results without a subquery (Snowflake gem).
- **`DATEDIFF`, `DATEADD`, `DATE_TRUNC`** — clean date math.
- **`ILIKE`** — case-insensitive matching.
- **`LISTAGG`** — string aggregation.
- **`::type`** — casting shorthand.
Where a problem's solution is identical in both, we note *"Snowflake: identical"* and just add any idiomatic tip.

---

*🗄️ SQL Mastery — [PJ's Academy](https://pjsacademy.com)*
