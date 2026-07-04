# -*- coding: utf-8 -*-
"""
Build one branded, complete-book PDF per course from its markdown files.
- Concatenates a course's markdown (README -> modules -> projects -> practice)
- Renders Mermaid diagrams to real SVG (via mermaid.js) so they appear in the PDF
- Syntax-highlighted code, styled tables, PJ's Academy branding
- Outputs vector PDFs (selectable text) via Playwright's page.pdf()

Run:  py build_course_pdfs.py
Output: <course>/pdfs/<Course_Name>_Complete.pdf   (+ a copy in course-pdfs/)
"""
import re
import sys
from pathlib import Path
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent
BUNDLE = ROOT / "course-pdfs"
BUNDLE.mkdir(exist_ok=True)

# course_name -> (output filename, ordered list of markdown files)
COURSES = {
    "Machine Learning Mastery": ("Machine_Learning_Mastery_Complete", [
        "machine-learning-course/README.md",
        "machine-learning-course/module-01-what-is-ml.md",
        "machine-learning-course/module-02-data-prep.md",
        "machine-learning-course/module-03-regression.md",
        "machine-learning-course/module-04-classification.md",
        "machine-learning-course/module-05-ensembles.md",
        "machine-learning-course/module-06-evaluation.md",
        "machine-learning-course/module-07-unsupervised.md",
        "machine-learning-course/module-08-tuning.md",
        "machine-learning-course/module-09-neural-nets.md",
        "machine-learning-course/module-10-production.md",
        "machine-learning-course/projects.md",
        "machine-learning-course/practice.md",
    ]),
    "SQL Mastery": ("SQL_Mastery_Complete", [
        "sql-mastery-course/README.md",
        "sql-mastery-course/modules/module-01-databases-select.md",
        "sql-mastery-course/modules/module-02-filtering-sorting.md",
        "sql-mastery-course/modules/module-03-aggregations.md",
        "sql-mastery-course/modules/module-04-joins.md",
        "sql-mastery-course/modules/module-05-subqueries-ctes.md",
        "sql-mastery-course/modules/module-06-window-functions.md",
        "sql-mastery-course/modules/module-07-advanced.md",
        "sql-mastery-course/modules/module-08-interview-realwork.md",
        "sql-mastery-course/practice-problems/README.md",
        "sql-mastery-course/practice-problems/01-easy.md",
        "sql-mastery-course/practice-problems/02-medium.md",
        "sql-mastery-course/practice-problems/03-hard.md",
    ]),
    "Prompt Engineering Mastery": ("Prompt_Engineering_Mastery_Complete", [
        "prompt-engineering-course/README.md",
        "prompt-engineering-course/module-01-foundations.md",
        "prompt-engineering-course/module-02-core-techniques.md",
        "prompt-engineering-course/module-03-advanced-reasoning.md",
        "prompt-engineering-course/module-04-structured-outputs.md",
        "prompt-engineering-course/module-05-rag-context.md",
        "prompt-engineering-course/module-06-production-agents.md",
        "prompt-engineering-course/projects.md",
    ]),
}

CSS = """
@page { size: A4; margin: 18mm 15mm 16mm 15mm; }
* { box-sizing: border-box; }
body { font-family:'Segoe UI',Arial,sans-serif; color:#1a2233; font-size:11.5px; line-height:1.6; margin:0; }
.cover { text-align:center; padding:60mm 0; page-break-after:always; }
.cover .flake { font-size:60px; }
.cover h1 { font-size:34px; color:#0d2340; margin:16px 0 6px; }
.cover .sub { color:#29b5e8; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-size:13px; }
.cover .brand { margin-top:30px; font-weight:800; font-size:16px; color:#0d2340; }
.cover .brand em { color:#f0a500; font-style:normal; }
.brandbar { display:flex; align-items:center; gap:8px; padding:8px 0 10px; border-bottom:3px solid #f0a500; margin-bottom:16px; }
.brandbar .name { font-weight:800; font-size:13px; color:#0d2340; }
.brandbar .name em { color:#f0a500; font-style:normal; }
.brandbar .tag { margin-left:auto; font-size:9px; color:#29b5e8; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
h1 { font-size:24px; color:#0d2340; border-bottom:2px solid #eef2f7; padding-bottom:6px; margin:4px 0 12px; page-break-before:always; }
h1:first-of-type { page-break-before:avoid; }
h2 { font-size:17px; color:#134e8a; margin:20px 0 7px; padding-left:9px; border-left:4px solid #29b5e8; }
h3 { font-size:13.5px; color:#0d7ab5; margin:14px 0 5px; }
h4 { font-size:12px; color:#1a2233; margin:10px 0 4px; }
p { margin:5px 0; } a { color:#1356a2; text-decoration:none; }
ul,ol { margin:5px 0 5px 4px; padding-left:20px; } li { margin:2px 0; }
strong { color:#0d2340; }
blockquote { border-left:4px solid #f0a500; background:#fff9ec; margin:9px 0; padding:7px 13px; color:#5a4a20; border-radius:0 6px 6px 0; }
code { background:#eef4fb; color:#134e8a; padding:1px 5px; border-radius:4px; font-family:'Consolas',monospace; font-size:10px; }
pre { background:#0d2340; color:#e8eef6; padding:11px 13px; border-radius:8px; overflow-x:auto; font-size:9.5px; line-height:1.5; margin:9px 0; border-left:4px solid #29b5e8; page-break-inside:avoid; }
pre code { background:none; color:#e8eef6; padding:0; }
table { border-collapse:collapse; width:100%; margin:11px 0; font-size:10px; page-break-inside:avoid; }
th { background:#134e8a; color:#fff; padding:6px 9px; text-align:left; }
td { padding:5px 9px; border-bottom:1px solid #e3edf7; }
tr:nth-child(even) td { background:#f6faff; }
hr { border:none; border-top:1px solid #e3edf7; margin:16px 0; }
.mermaid { text-align:center; margin:14px 0; page-break-inside:avoid; }
.codehilite .k,.codehilite .kd,.codehilite .kn { color:#7cc7ff; font-weight:600; }
.codehilite .s,.codehilite .s1,.codehilite .s2 { color:#ffd479; }
.codehilite .c,.codehilite .c1,.codehilite .cm { color:#6b8299; font-style:italic; }
.codehilite .nf,.codehilite .nb { color:#8be9fd; }
.codehilite .mi,.codehilite .mf { color:#ff9d6b; }
.footer-note { margin-top:22px; padding-top:10px; border-top:2px solid #eef2f7; font-size:9px; color:#8892a4; text-align:center; }
"""

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"


def convert_markdown(md_text):
    """Extract mermaid blocks, convert markdown, reinsert as <pre class='mermaid'>."""
    blocks = []
    def stash(m):
        blocks.append(m.group(1))
        return f"\n\nMERMAIDPLACEHOLDER{len(blocks)-1}\n\n"
    md_text = re.sub(r"```mermaid\n(.*?)```", stash, md_text, flags=re.DOTALL)

    html = markdown.markdown(md_text, extensions=[
        "tables", "fenced_code", "sane_lists",
        CodeHiliteExtension(guess_lang=False, noclasses=False),
    ])
    for i, code in enumerate(blocks):
        # markdown wraps the lone placeholder line in <p>...</p>
        html = html.replace(f"<p>MERMAIDPLACEHOLDER{i}</p>",
                            f'<pre class="mermaid">{code.strip()}</pre>')
        html = html.replace(f"MERMAIDPLACEHOLDER{i}",
                            f'<pre class="mermaid">{code.strip()}</pre>')
    return html


def build_html(course_name, files):
    brand = ('<div class="brandbar"><span>&#10052;&#65039;</span>'
             '<span class="name">PJ&#39;s <em>Academy</em></span>'
             '<span class="tag">Complete Course</span></div>')
    cover = (f'<div class="cover"><div class="flake">&#10052;&#65039;</div>'
             f'<h1>{course_name}</h1><div class="sub">PJ&#39;s Academy</div>'
             f'<div class="brand">Complete Course Book</div></div>')
    body = []
    for rel in files:
        p = ROOT / rel
        if not p.exists():
            print(f"    SKIP missing {rel}"); continue
        body.append(convert_markdown(p.read_text(encoding="utf-8")))
    footer = ('<div class="footer-note">&#10052;&#65039; PJ&#39;s Academy &middot; '
              'pjsacademy.com &middot; hello@pjsacademy.com &middot; @pjsacademy.datascience</div>')
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style>"
            f"<script src='{MERMAID_CDN}'></script></head><body>"
            f"{cover}{brand}{''.join(body)}{footer}"
            "<script>mermaid.initialize({startOnLoad:true, theme:'neutral'});</script>"
            "</body></html>")


def main():
    from playwright.sync_api import sync_playwright
    made = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for course_name, (outname, files) in COURSES.items():
            print(f"Building: {course_name}")
            html = build_html(course_name, files)
            page.set_content(html, wait_until="networkidle")
            page.wait_for_timeout(2500)  # let mermaid render diagrams
            course_dir = ROOT / files[0].split("/")[0]
            (course_dir / "pdfs").mkdir(exist_ok=True)
            out1 = course_dir / "pdfs" / f"{outname}.pdf"
            page.pdf(path=str(out1), format="A4", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            # also drop a copy in the central bundle folder
            out2 = BUNDLE / f"{outname}.pdf"
            out2.write_bytes(out1.read_bytes())
            kb = out1.stat().st_size / 1024
            made.append((outname, kb))
            print(f"    [OK] {out1.relative_to(ROOT)}  ({kb:.0f} KB)")
        browser.close()
    print(f"\nBuilt {len(made)} course PDFs. Central copies in: course-pdfs/")


if __name__ == "__main__":
    main()
