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


# ---------- per-chapter notebook set ----------------------------------------
def build_chapter(chapter_dir, num, title, md_path, brand):
    md = md_path.read_text(encoding="utf-8")

    # Tutorial = the whole lesson
    write_nb(chapter_dir / f"{num}_Tutorial.ipynb", md_to_cells(md))

    # Exercises = the exercises section + empty solution cells
    ex = extract_section(md, "Exercises")
    ex_cells = [md_cell(f"# Chapter {num} — Exercises: {title}\n### {brand}\n\n"
                        "Try each yourself in the empty code cell before checking the tutorial.\n\n---")]
    if ex:
        # split exercises into individual items and give each an empty cell
        ex_cells.append(md_cell(ex))
        for item in re.findall(r"^\s*\d+\.\s+.*", ex, re.MULTILINE)[:8]:
            ex_cells.append(md_cell(f"**{item.strip()}**"))
            ex_cells.append(code_cell("# your solution here\n"))
    else:
        ex_cells.append(md_cell("_Practice the concepts from the tutorial here._"))
        ex_cells.append(code_cell("# your code here\n"))
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
                build_chapter(ch_dir, num, title, md_path, brand)
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
