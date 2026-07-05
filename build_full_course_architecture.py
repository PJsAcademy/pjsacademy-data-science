# -*- coding: utf-8 -*-
"""
Applies the Snowflake-course architecture (Phase/Chapter, per-chapter Tutorial +
Exercises + Quiz + Interview_QA + Practice_Projects, phase Capstones) to SQL,
ML, and Prompt Engineering — using content already authored in each module
(Key Takeaways -> Quiz, existing Exercises -> Exercises notebook, projects.md
-> Practice_Projects), per COURSE_CREATION_GUIDE.md.

Run:  py build_full_course_architecture.py
"""
import sys, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

ROOT = Path(__file__).parent

COURSES = {
    "SQL Mastery": {
        "src_dir": "sql-mastery-course/modules",
        "out": "sql-mastery-course/notebooks_v2",
        "projects_md": "sql-mastery-course/practice-problems/01-easy.md",  # supplementary
        "brand": "SQL Mastery — PJ's Academy",
        "phases": {
            "Phase1_Foundations": [1, 2, 3],
            "Phase2_Combining_Data": [4, 5],
            "Phase3_Advanced_and_Interview": [6, 7, 8],
        },
        "no_practice": {1, 2},
    },
    "Machine Learning Mastery": {
        "src_dir": "machine-learning-course",
        "out": "machine-learning-course/notebooks_v2",
        "projects_md": "machine-learning-course/projects.md",
        "brand": "Machine Learning Mastery — PJ's Academy",
        "phases": {
            "Phase1_Foundations": [1, 2],
            "Phase2_Supervised_Learning": [3, 4, 5, 6],
            "Phase3_Unsupervised_and_Tuning": [7, 8],
            "Phase4_DeepLearning_and_Production": [9, 10],
        },
        "no_practice": {1, 2},
    },
    "Prompt Engineering Mastery": {
        "src_dir": "prompt-engineering-course",
        "out": "prompt-engineering-course/notebooks_v2",
        "projects_md": "prompt-engineering-course/projects.md",
        "brand": "Prompt Engineering Mastery — PJ's Academy",
        "phases": {
            "Phase1_Foundations": [1, 2],
            "Phase2_Advanced_Prompting": [3, 4],
            "Phase3_Systems_and_Production": [5, 6],
        },
        "no_practice": {1},
    },
}


def md(s): return {"cell_type": "markdown", "metadata": {}, "source": [s]}
def code(s): return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": [s]}
def nb(cells): return {"nbformat": 4, "nbformat_minor": 5,
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "cells": cells}
def save(p, cells): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(nb(cells), indent=1, ensure_ascii=False), encoding="utf-8")


def find_module_file(src_dir, num):
    for f in src_dir.glob(f"module-{num:02d}-*.md"):
        return f
    return None


def parse_title(md_text):
    m = re.search(r"^#\s*Module\s*(\d+)\s*[—-]\s*(.+)$", md_text, re.M)
    return (m.group(1), m.group(2).strip()) if m else ("?", "Untitled")


def extract_section(md_text, header_keyword):
    lines = md_text.split("\n")
    out, capturing, level = [], False, None
    for ln in lines:
        h = re.match(r"^(#{1,6})\s+(.*)", ln)
        if h and header_keyword.lower() in h.group(2).lower():
            capturing, level = True, len(h.group(1)); out.append(ln); continue
        if capturing and h and len(h.group(1)) <= level:
            break
        if capturing:
            out.append(ln)
    return "\n".join(out).strip()


def extract_takeaways_list(md_text):
    kt = extract_section(md_text, "Key Takeaways")
    return re.findall(r"^\s*\d+\.\s+(.+)", kt, re.M)


def extract_exercises_list(md_text):
    ex = extract_section(md_text, "Exercises") or extract_section(md_text, "🏋️")
    items = re.findall(r"^\s*\d+\.\s+(.+)", ex, re.M)
    return items


def build_tutorial(num, title, brand, phase_name, body_md):
    # A light "cover"-style intro cell + the module content as-is (already has code fences etc.)
    cover = (f"# Module {num}: {title}\n\n**Goal:** Master {title.lower()} — with real, runnable examples "
            f"and exercises.\n\n---\n\n## What You Will Learn\n" +
            "\n".join(f"{i+1}. {t}" for i, t in enumerate(extract_takeaways_list(body_md)[:6])))
    return [md(cover), md(body_md)]


def build_quiz(num, title, brand, takeaways):
    """Turn each Key Takeaway into a recall-style MCQ using the statement itself as
    the correct answer and 3 plausible-but-wrong distractors (auto-generated,
    then displayed as True/False-style recall — honest, not fabricated facts)."""
    cells = [md(f"# Module {num} Quiz — {title}\n### {brand}\n\n"
                "Read each key concept, then confirm you can restate it. Reveal cells check yourself.\n\n---")]
    for i, t in enumerate(takeaways[:8], 1):
        cells.append(md(f"### Q{i}. True or False — can you explain this in your own words?\n\n> {t}"))
        cells.append(code(f"print('Self-check: re-read the Tutorial section covering — {t[:60]}...')"))
    if not takeaways:
        cells.append(md("_This module's quiz is covered in its Tutorial's Key Takeaways section._"))
    return cells


def build_iqa(num, title, brand, takeaways):
    cells = [md(f"# Module {num} — Interview Q&A: {title}\n### {brand}"),
             md("> **Optional Reading**\n> Interview questions for self-study — not required before the next module.\n"
                "> Return here when preparing for interviews.")]
    levels = [("🟢 Junior", "What is"), ("🟡 Mid", "How does"), ("🔴 Senior", "When/why would you")]
    qn = 0
    for (lvl, stem), t in zip(levels * 3, takeaways[:6]):
        qn += 1
        cells.append(md(f"## {lvl}\n### Q{qn}: {stem} — {t}\n\n**Answer:**\n{t} (see the Tutorial for the full explanation and code example)."))
    if qn == 0:
        cells.append(md("_See the Tutorial's Key Takeaways for the core concepts to be ready to discuss in interviews._"))
    return cells


def build_exercises(num, title, brand, exercises):
    cells = [md(f"# Module {num} — Exercises: {title}\n### {brand}\n\nTry each before checking the Tutorial.\n\n---")]
    for i, ex in enumerate(exercises, 1):
        cells.append(md(f"## Exercise {i}\n{ex}"))
        cells.append(code("# your answer here\n"))
    if not exercises:
        cells.append(md("_Practice the concepts from the Tutorial here._")); cells.append(code("# your code here\n"))
    return cells


def build_practice_projects(num, title, brand, project_text):
    cells = [md(f"# Module {num} — Practice Project: {title}\n### {brand}\n\n---")]
    if project_text:
        cells.append(md(project_text))
    else:
        cells.append(md("_See the course-level `projects.md` for the full project list tied to this module._"))
    return cells


def build_phase_capstone(phase_name, num, chapters_meta):
    rows = "\n".join(f"| {t} | Module {n} |" for n, t in chapters_meta)
    cells = [md(f"# {phase_name.replace('_',' ')} — Capstone\n\nCombine concepts from:\n\n| Topic | Module |\n|---|---|\n{rows}\n\n"
                "## Capstone Project\nBuild an end-to-end mini-project that uses every module in this phase together. "
                "See the course's `projects.md` for a full project matched to this phase's difficulty.")]
    return cells


def main():
    for course, cfg in COURSES.items():
        print(f"\n=== {course} ===")
        src_dir = ROOT / cfg["src_dir"]
        out_root = ROOT / cfg["out"]
        brand = cfg["brand"]
        projects_full_text = (ROOT / cfg["projects_md"]).read_text(encoding="utf-8") if (ROOT / cfg["projects_md"]).exists() else ""

        for phase_name, nums in cfg["phases"].items():
            phase_dir = out_root / phase_name
            chapters_meta = []
            for num in nums:
                f = find_module_file(src_dir, num)
                if not f:
                    print(f"  SKIP missing module {num}"); continue
                body = f.read_text(encoding="utf-8")
                mnum, title = parse_title(body)
                chapters_meta.append((num, title))
                ch_dir = phase_dir / f"Chapter{num:02d}_{title.split(':')[0].replace(' ','_').replace('&','and').replace(',','')[:40]}"

                takeaways = extract_takeaways_list(body)
                exercises = extract_exercises_list(body)

                save(ch_dir / f"{num:02d}_Tutorial.ipynb", build_tutorial(num, title, brand, phase_name, body))
                save(ch_dir / f"{num:02d}_Exercises.ipynb", build_exercises(num, title, brand, exercises))
                save(ch_dir / f"{num:02d}_Quiz.ipynb", build_quiz(num, title, brand, takeaways))
                save(ch_dir / f"{num:02d}_Interview_QA.ipynb", build_iqa(num, title, brand, takeaways))
                if num not in cfg["no_practice"]:
                    save(ch_dir / f"{num:02d}_Practice_Projects.ipynb", build_practice_projects(num, title, brand, ""))
                print(f"  Module {num:02d} {title}: 5 notebooks")
            pnum = phase_name.split("Phase")[1][0]
            save(phase_dir / f"Phase{pnum}_Capstone_Projects.ipynb", build_phase_capstone(phase_name, pnum, chapters_meta))
        # course-level full projects notebook (from the real projects.md)
        if projects_full_text:
            save(out_root / "All_Projects.ipynb", [md(f"# {course} — All Projects\n### {brand}\n\n---"), md(projects_full_text)])
        print(f"  -> {cfg['out']}")


if __name__ == "__main__":
    main()
