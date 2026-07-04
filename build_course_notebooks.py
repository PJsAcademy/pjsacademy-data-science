# -*- coding: utf-8 -*-
"""
Convert markdown-based courses into the Data Science Mastery notebook structure:

  <CourseName>_Notebooks/
    PhaseN_Name/
      ChapterNN_Topic/
        NN_Tutorial.ipynb          (the full lesson; python blocks are runnable cells)
        NN_Exercises.ipynb         (exercises + empty solution cells)
        NN_Quiz.ipynb              (knowledge-check questions from the chapter)
      PhaseN_Capstone_Projects.ipynb
      PhaseN_Interview_QA.ipynb

Run:  py build_course_notebooks.py
"""
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent


# ---------- notebook helpers ------------------------------------------------
def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": _lines(text)}


def code_cell(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": _lines(text)}


def _lines(text):
    text = text.rstrip("\n")
    parts = text.split("\n")
    return [p + "\n" for p in parts[:-1]] + [parts[-1]] if parts else [""]


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4, "nbformat_minor": 5,
    }


def write_nb(path, cells):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook(cells), indent=1, ensure_ascii=False),
                    encoding="utf-8")


# ---------- markdown -> cells (python fences become runnable code cells) ----
FENCE = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)


def md_to_cells(md_text):
    cells, pos = [], 0
    for m in FENCE.finditer(md_text):
        before = md_text[pos:m.start()].strip()
        if before:
            cells.append(md_cell(before))
        lang, code = m.group(1).lower(), m.group(2).rstrip("\n")
        if lang in ("python", "py"):
            cells.append(code_cell(code))          # only real python is runnable
        else:
            # keep sql/yaml/bash/mermaid as a fenced markdown block (won't error)
            cells.append(md_cell(f"```{lang}\n{code}\n```"))
        pos = m.end()
    tail = md_text[pos:].strip()
    if tail:
        cells.append(md_cell(tail))
    return cells


def extract_section(md_text, header_keyword):
    """Return the markdown of the section whose header contains header_keyword."""
    lines = md_text.split("\n")
    out, capturing, level = [], False, None
    for ln in lines:
        h = re.match(r"^(#{1,6})\s+(.*)", ln)
        if h and header_keyword.lower() in h.group(2).lower():
            capturing, level = True, len(h.group(1))
            out.append(ln); continue
        if capturing and h and len(h.group(1)) <= level:
            break
        if capturing:
            out.append(ln)
    return "\n".join(out).strip()


def extract_takeaways(md_text):
    return extract_section(md_text, "Key Takeaways") or extract_section(md_text, "Takeaways")


# ---------- runnable SQL sandbox (in-notebook SQLite) -----------------------
SQL_SANDBOX = '''# ── SQL Sandbox — run this cell first ──────────────────────────────
# Creates an in-memory database with the sample tables so you can run the
# queries in this chapter. Use run("SELECT ...") and it returns a DataFrame.
# (SQLite supports SELECT/JOIN/GROUP BY/CTEs/window functions. A few Snowflake-
#  only bits — QUALIFY, DATE_TRUNC, SPLIT_PART — won't run here; those are noted.)
import sqlite3, pandas as pd
conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE departments (dept_id INT, dept_name TEXT, location TEXT);
CREATE TABLE employees (emp_id INT, name TEXT, dept_id INT, manager_id INT,
                        salary INT, hire_date TEXT, email TEXT);
CREATE TABLE customers (customer_id INT, name TEXT, city TEXT, signup_date TEXT);
CREATE TABLE products (product_id INT, product_name TEXT, category TEXT, price REAL);
CREATE TABLE orders (order_id INT, customer_id INT, product_id INT, quantity INT,
                     order_date TEXT, amount REAL);
INSERT INTO departments VALUES
 (1,'Engineering','Bangalore'),(2,'Sales','Mumbai'),(3,'Marketing','Delhi'),(4,'HR','Bangalore');
INSERT INTO employees VALUES
 (1,'Asha',1,NULL,180000,'2019-03-01','asha@pjs.com'),
 (2,'Ravi',1,1,120000,'2020-06-15','ravi@pjs.com'),
 (3,'Meera',2,1,95000,'2021-01-20','meera@pjs.com'),
 (4,'Kiran',2,3,70000,'2022-07-11','kiran@pjs.com'),
 (5,'Sana',3,1,88000,'2021-09-05','sana@pjs.com'),
 (6,'Vijay',1,2,110000,'2023-02-28','vijay@pjs.com'),
 (7,'Nina',4,1,60000,'2020-11-30',NULL);
INSERT INTO customers VALUES
 (101,'Rahul','Mumbai','2023-01-10'),(102,'Priya','Delhi','2023-02-14'),
 (103,'Arjun','Bangalore','2023-03-22'),(104,'Divya','Mumbai','2023-05-01');
INSERT INTO products VALUES
 (201,'Laptop','Electronics',55000),(202,'Mouse','Electronics',700),
 (203,'Desk','Furniture',8000),(204,'Chair','Furniture',4500),(205,'Monitor','Electronics',15000);
INSERT INTO orders VALUES
 (1,101,201,1,'2023-06-01',55000),(2,101,202,2,'2023-06-01',1400),
 (3,102,205,2,'2023-06-05',30000),(4,103,203,1,'2023-06-10',8000),
 (5,103,204,4,'2023-06-10',18000),(6,104,201,1,'2023-07-02',55000),
 (7,102,202,1,'2023-07-15',700),(8,101,205,1,'2023-08-01',15000);
""")
def run(sql):
    "Run a SQL query against the sample database and return a DataFrame."
    return pd.read_sql_query(sql, conn)

run("SELECT * FROM employees")  # try it — edit and re-run!'''


# ---------- per-chapter notebook set ----------------------------------------
def build_chapter(chapter_dir, num, title, md_path, brand, sandbox=None):
    md = md_path.read_text(encoding="utf-8")

    # Tutorial = the whole lesson (+ runnable sandbox at the top for SQL)
    tut_cells = []
    if sandbox:
        tut_cells.append(md_cell(f"## 🧪 Interactive Sandbox\nRun the setup cell, "
                                 f"then try any query from this chapter with `run(\"...\")`."))
        tut_cells.append(code_cell(sandbox))
    tut_cells += md_to_cells(md)
    write_nb(chapter_dir / f"{num}_Tutorial.ipynb", tut_cells)

    # Exercises = the exercises section + empty solution cells
    ex = extract_section(md, "Exercises")
    ex_cells = [md_cell(f"# Chapter {num} — Exercises: {title}\n### {brand}\n\n"
                        "Try each yourself in the empty code cell before checking the tutorial.\n\n---")]
    if sandbox:
        ex_cells.append(md_cell("Run the sandbox, then answer with `run(\"SELECT ...\")`."))
        ex_cells.append(code_cell(sandbox))
    if ex:
        # split exercises into individual items and give each an empty cell
        ex_cells.append(md_cell(ex))
        for item in re.findall(r"^\s*\d+\.\s+.*", ex, re.MULTILINE)[:8]:
            ex_cells.append(md_cell(f"**{item.strip()}**"))
            ex_cells.append(code_cell("# your solution here\n"))
    else:
        ex_cells.append(md_cell("_Practice the concepts from the tutorial here._"))
        ex_cells.append(code_cell('run("# your query here")\n' if sandbox else "# your code here\n"))
    write_nb(chapter_dir / f"{num}_Exercises.ipynb", ex_cells)

    # Quiz = knowledge check built from Key Takeaways
    kt = extract_takeaways(md)
    quiz = [md_cell(f"# Chapter {num} — Quiz: {title}\n### {brand}\n\n"
                    "Answer from memory, then re-read the tutorial to check.\n\n---")]
    points = re.findall(r"^\s*\d+\.\s+(.*)", kt, re.MULTILINE) if kt else []
    if points:
        for i, p in enumerate(points, 1):
            # turn a takeaway statement into a recall prompt
            quiz.append(md_cell(f"**Q{i}.** Explain in your own words: {p}"))
    else:
        quiz.append(md_cell("**Q1.** Summarise the three most important ideas from this chapter."))
    quiz.append(md_cell("---\n*Check your answers against the tutorial's Key Takeaways.*"))
    write_nb(chapter_dir / f"{num}_Quiz.ipynb", quiz)


def build_phase_extras(phase_dir, phase_name, projects_md, brand):
    if projects_md and projects_md.exists():
        cells = [md_cell(f"# {phase_name} — Capstone Projects\n### {brand}\n\n---")]
        cells += md_to_cells(projects_md.read_text(encoding="utf-8"))
        write_nb(phase_dir / f"{phase_name}_Capstone_Projects.ipynb", cells)


# ---------- course definitions ---------------------------------------------
COURSES = {
    "Machine Learning Mastery": {
        "brand": "PJ's Academy · Machine Learning Mastery",
        "out": "machine-learning-course/notebooks",
        "projects": "machine-learning-course/projects.md",
        "phases": {
            "Phase1_Foundations": [
                ("01", "What Machine Learning Is", "machine-learning-course/module-01-what-is-ml.md"),
                ("02", "Data & Feature Engineering", "machine-learning-course/module-02-data-prep.md"),
            ],
            "Phase2_Supervised_Learning": [
                ("03", "Regression", "machine-learning-course/module-03-regression.md"),
                ("04", "Classification", "machine-learning-course/module-04-classification.md"),
                ("05", "Ensembles", "machine-learning-course/module-05-ensembles.md"),
                ("06", "Model Evaluation", "machine-learning-course/module-06-evaluation.md"),
            ],
            "Phase3_Unsupervised_and_Tuning": [
                ("07", "Unsupervised Learning", "machine-learning-course/module-07-unsupervised.md"),
                ("08", "Feature Selection & Tuning", "machine-learning-course/module-08-tuning.md"),
            ],
            "Phase4_DeepLearning_and_Production": [
                ("09", "Neural Networks", "machine-learning-course/module-09-neural-nets.md"),
                ("10", "ML in Production", "machine-learning-course/module-10-production.md"),
            ],
        },
    },
    "SQL Mastery": {
        "brand": "PJ's Academy · SQL Mastery",
        "out": "sql-mastery-course/notebooks",
        "projects": "sql-mastery-course/practice-problems/README.md",
        "sql": True,     # inject the runnable SQLite sandbox
        "phases": {
            "Phase1_Foundations": [
                ("01", "Databases & SELECT Basics", "sql-mastery-course/modules/module-01-databases-select.md"),
                ("02", "Filtering, Sorting & Operators", "sql-mastery-course/modules/module-02-filtering-sorting.md"),
                ("03", "Aggregations & GROUP BY", "sql-mastery-course/modules/module-03-aggregations.md"),
            ],
            "Phase2_Combining_Data": [
                ("04", "JOINs", "sql-mastery-course/modules/module-04-joins.md"),
                ("05", "Subqueries & CTEs", "sql-mastery-course/modules/module-05-subqueries-ctes.md"),
            ],
            "Phase3_Advanced_and_Interview": [
                ("06", "Window Functions", "sql-mastery-course/modules/module-06-window-functions.md"),
                ("07", "Advanced SQL", "sql-mastery-course/modules/module-07-advanced.md"),
                ("08", "SQL for Interviews & Real Work", "sql-mastery-course/modules/module-08-interview-realwork.md"),
            ],
        },
    },
    "Prompt Engineering Mastery": {
        "brand": "PJ's Academy · Prompt Engineering Mastery",
        "out": "prompt-engineering-course/notebooks",
        "projects": "prompt-engineering-course/projects.md",
        "phases": {
            "Phase1_Foundations": [
                ("01", "Foundations: How LLMs Work", "prompt-engineering-course/module-01-foundations.md"),
                ("02", "Core Techniques", "prompt-engineering-course/module-02-core-techniques.md"),
            ],
            "Phase2_Advanced_Prompting": [
                ("03", "Advanced Reasoning", "prompt-engineering-course/module-03-advanced-reasoning.md"),
                ("04", "Structured Outputs & Tools", "prompt-engineering-course/module-04-structured-outputs.md"),
            ],
            "Phase3_Systems_and_Production": [
                ("05", "RAG & Context Engineering", "prompt-engineering-course/module-05-rag-context.md"),
                ("06", "Production, Evaluation & Agents", "prompt-engineering-course/module-06-production-agents.md"),
            ],
        },
    },
}


def main():
    for course, cfg in COURSES.items():
        print(f"\n=== {course} ===")
        out_root = ROOT / cfg["out"]
        brand = cfg["brand"]
        for phase_name, chapters in cfg["phases"].items():
            phase_dir = out_root / phase_name
            for num, title, md_rel in chapters:
                md_path = ROOT / md_rel
                if not md_path.exists():
                    print(f"  SKIP missing {md_rel}"); continue
                ch_dir = phase_dir / f"Chapter{num}_{title.split(':')[0].replace(' ', '_').replace('&','and')}"
                build_chapter(ch_dir, num, title, md_path, brand,
                              sandbox=SQL_SANDBOX if cfg.get("sql") else None)
                print(f"  [OK] {phase_name}/{ch_dir.name}  (Tutorial+Exercises+Quiz)")
            build_phase_extras(phase_dir, phase_name, ROOT / cfg["projects"], brand)
        # course-level README pointing at the notebooks
        (out_root / "README.md").write_text(
            f"# {course} — Notebook Edition\n\n"
            f"Same structure as Data Science Mastery: Phase → Chapter → "
            f"Tutorial / Exercises / Quiz notebooks, plus phase Capstone Projects.\n\n"
            f"Open any `*_Tutorial.ipynb` in Jupyter/VS Code/Colab and run the cells.\n\n"
            f"*{brand} · pjsacademy.com*\n", encoding="utf-8")
        print(f"  -> {cfg['out']}")


if __name__ == "__main__":
    main()
