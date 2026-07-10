# -*- coding: utf-8 -*-
"""Premium PDF for SQL Mastery, using the shared premium book renderer."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))
from render_premium_book import render_course
import svg_diagrams as sd

BASE = Path(__file__).parent / "sql-mastery-course" / "notebooks_v2"
OUT = Path(__file__).parent / "sql-mastery-course" / "pdfs" / "SQL_Mastery_PREMIUM.pdf"

DIAGRAM_BUILDERS = {
 1: lambda: sd.layered_diagram([("Database", "A named collection of tables", sd.NAVY, "#fff"),
             ("Table", "Rows and columns — one entity type per table", sd.BLUEDK, "#fff"),
             ("SELECT", "Retrieves rows/columns you ask for, doesn't change the data", sd.GOLD, "#3A2F0E")]),
 3: lambda: sd.flow_diagram([("Rows", sd.GREY), ("GROUP BY\nkey", sd.GOLD),
             ("Aggregate function\n(SUM, COUNT, AVG)", sd.BLUE), ("One row\nper group", "#2E9E6B")],
             title="Aggregation collapses rows"),
 5: lambda: sd.flow_diagram([("Subquery /\nCTE runs first", sd.GOLD), ("Produces a\ntemporary result", sd.BLUE),
             ("Outer query\nuses that result", sd.BLUEDK), ("Final rows", "#2E9E6B")], title="Subqueries and CTEs"),
 6: lambda: sd.comparison_diagram("GROUP BY", "Collapses rows into one row per group",
             "Window function", "Keeps every row, computes using the group as context", vs_label="vs"),
}

PROMO = [
    {"title": "Snowflake Mastery — Complete Guide", "desc": "43 chapters, zero to Cortex AI, exam-mapped with real diagrams and hands-on labs."},
    {"title": "Machine Learning Mastery — Complete Guide", "desc": "30 chapters, foundations to production MLOps, with a 50-project portfolio vault."},
    {"title": "GenAI & Prompt Engineering Mastery — Complete Guide", "desc": "31 chapters: prompting, RAG, AI agents, and shipping safe production GenAI systems."},
    {"title": "Python Mastery — Complete Guide", "desc": "45 chapters, zero to GenAI engineer, with real executed code, outputs, and charts."},
]

if __name__ == "__main__":
    test_chapter = None
    if len(sys.argv) > 2 and sys.argv[1] == "--test":
        test_chapter = int(sys.argv[2])
    out = OUT if test_chapter is None else OUT.parent / f"Chapter{test_chapter:02d}_PREVIEW.pdf"
    render_course(
        BASE, out, book_title="SQL MASTERY GUIDE",
        kicker="SQL MASTERY SERIES", title_main="SQL Mastery", title_accent="Complete Guide",
        subtitle="The complete, exercise-driven system for mastering SQL — from your first SELECT to "
                 "advanced window functions and interview-ready query design.",
        badges=[("8 Modules", "3 Phases, Zero to Advanced"), ("40+ Notebooks", "Tutorials, Quizzes, Projects"),
                ("Interview-Ready", "Real Query Patterns")],
        unit_word="Module", default_lang="sql", test_chapter=test_chapter, promo_products=PROMO,
        diagram_builders=DIAGRAM_BUILDERS,
    )
