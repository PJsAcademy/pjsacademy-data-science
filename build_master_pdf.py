# -*- coding: utf-8 -*-
"""
Combine every course's PDF into one master 'PJ's Academy Complete Library' PDF,
with a cover page and per-course section dividers. Reuses the already-built
per-course PDFs (no re-render needed).

Run:  py build_master_pdf.py
Output: course-pdfs/PJs_Academy_Complete_Library.pdf
"""
import sys
from pathlib import Path
from pypdf import PdfWriter, PdfReader

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent
OUT = ROOT / "course-pdfs"
OUT.mkdir(exist_ok=True)

# Course PDFs to include, in order (title -> pdf path)
SECTIONS = [
    ("SQL Mastery",               "sql-mastery-course/pdfs/SQL_Mastery_Complete.pdf"),
    ("Prompt Engineering Mastery","prompt-engineering-course/pdfs/Prompt_Engineering_Mastery_Complete.pdf"),
    ("Machine Learning Mastery",  "machine-learning-course/pdfs/Machine_Learning_Mastery_Complete.pdf"),
    ("Snowflake — Course",        "snowflake-course/pdfs/01_Snowflake_Course_Overview.pdf"),
    ("Snowflake — Advanced Tutorials", "snowflake-course/pdfs/02_Advanced_Tutorials.pdf"),
    ("Snowflake — Projects Vault","snowflake-course/pdfs/03_Snowflake_Projects_Vault.pdf"),
    ("Snowflake — SnowPro Core Study Guide", "snowflake-course/pdfs/11_SnowPro_Core_Study_Guide.pdf"),
    ("Snowflake — SnowPro Core Mock Exam",   "snowflake-course/pdfs/12_SnowPro_Core_Mock_Exam.pdf"),
]


def make_cover(title, subtitle):
    """Render a simple cover page to a 1-page PDF via Playwright."""
    from playwright.sync_api import sync_playwright
    html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>
    @page {{ size:A4; margin:0; }}
    body {{ margin:0; height:297mm; display:flex; flex-direction:column;
           align-items:center; justify-content:center; font-family:'Segoe UI',Arial;
           background:linear-gradient(135deg,#0d0d1a,#13132b); color:#fff; }}
    .flake {{ font-size:70px; }}
    h1 {{ font-size:40px; margin:14px 40px 6px; text-align:center; }}
    h1 em {{ color:#f0a500; font-style:normal; }}
    .sub {{ color:#29b5e8; letter-spacing:3px; text-transform:uppercase; font-size:14px; }}
    .foot {{ position:absolute; bottom:40px; color:#8892a4; font-size:12px; }}
    </style></head><body>
    <div class='flake'>&#10052;&#65039;</div>
    <h1>{title}</h1><div class='sub'>{subtitle}</div>
    <div class='foot'>PJ&#39;s Academy &middot; pjsacademy.com &middot; hello@pjsacademy.com</div>
    </body></html>"""
    tmp = OUT / "_cover_tmp.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(html, wait_until="networkidle")
        pg.pdf(path=str(tmp), format="A4", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    return tmp


def main():
    writer = PdfWriter()

    # Master cover
    cover = make_cover("PJ's Academy<br><em>Complete Library</em>", "All-Access Course Bundle")
    for pg in PdfReader(str(cover)).pages:
        writer.add_page(pg)

    included, missing = [], []
    for title, rel in SECTIONS:
        pdf = ROOT / rel
        if not pdf.exists():
            missing.append(rel); continue
        # section divider
        div = make_cover(title, "Course Section")
        for pg in PdfReader(str(div)).pages:
            writer.add_page(pg)
        div.unlink(missing_ok=True)
        # the course pages, with a bookmark/outline entry
        start = len(writer.pages)
        reader = PdfReader(str(pdf))
        for pg in reader.pages:
            writer.add_page(pg)
        writer.add_outline_item(title, start)
        included.append((title, len(reader.pages)))

    cover.unlink(missing_ok=True)
    out = OUT / "PJs_Academy_Complete_Library.pdf"
    with open(out, "wb") as f:
        writer.write(f)

    print("Master library built:", out)
    print(f"  Total pages: {len(writer.pages)}  ({out.stat().st_size/1024:.0f} KB)")
    for t, n in included:
        print(f"   - {t}: {n} pages")
    if missing:
        print("  Missing (skipped):", missing)


if __name__ == "__main__":
    main()
