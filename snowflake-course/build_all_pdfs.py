# -*- coding: utf-8 -*-
"""
Convert every Snowflake course & certification markdown guide into a branded PDF.
Uses `markdown` (with tables, fenced code, syntax highlighting) + Playwright's
native vector PDF printing (crisp, selectable text — not screenshots).

Run:  py build_all_pdfs.py
Output: snowflake-course/pdfs/*.pdf
"""
import sys
from pathlib import Path
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
OUT = ROOT / "pdfs"
OUT.mkdir(exist_ok=True)

# Markdown files to convert -> output PDF name
DOCS = [
    ("README.md", "01_Snowflake_Course_Overview"),
    ("advanced-tutorials/README.md", "02_Advanced_Tutorials"),
    ("projects/README.md", "03_Snowflake_Projects_Vault"),
    ("certification/README.md", "10_Certification_Overview"),
    ("certification/snowpro-core/README.md", "11_SnowPro_Core_Study_Guide"),
    ("certification/snowpro-core/mock-exam-1.md", "12_SnowPro_Core_Mock_Exam"),
    ("certification/snowpro-advanced-architect/README.md", "13_Advanced_Architect"),
    ("certification/snowpro-advanced-administrator/README.md", "14_Advanced_Administrator"),
    ("certification/snowpro-advanced-data-engineer/README.md", "15_Advanced_Data_Engineer"),
    ("certification/snowpro-advanced-data-scientist/README.md", "16_Advanced_Data_Scientist"),
    ("certification/snowpro-advanced-data-analyst/README.md", "17_Advanced_Data_Analyst"),
    ("certification/snowpro-specialty-gen-ai/README.md", "18_Specialty_Gen_AI"),
    ("certification/snowpro-specialty-snowpark/README.md", "19_Specialty_Snowpark"),
]

PAGE_CSS = """
@page { size: A4; margin: 20mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #1a2233; font-size: 11.5px;
       line-height: 1.6; margin: 0; }
.brandbar { display:flex; align-items:center; gap:10px; padding:10px 0 12px;
            border-bottom:3px solid #f0a500; margin-bottom:22px; }
.brandbar .flake { font-size:20px; }
.brandbar .name { font-weight:800; font-size:15px; color:#0d2340; }
.brandbar .name em { color:#f0a500; font-style:normal; }
.brandbar .tag { margin-left:auto; font-size:10px; color:#29b5e8; font-weight:700;
                 letter-spacing:1px; text-transform:uppercase; }
h1 { font-size:26px; color:#0d2340; border-bottom:2px solid #eef2f7; padding-bottom:8px;
     margin:6px 0 14px; letter-spacing:-0.5px; }
h2 { font-size:18px; color:#134e8a; margin:22px 0 8px; padding-left:10px;
     border-left:4px solid #29b5e8; }
h3 { font-size:14px; color:#0d7ab5; margin:16px 0 6px; }
h4 { font-size:12.5px; color:#1a2233; margin:12px 0 4px; }
p { margin:6px 0; }
a { color:#1356a2; text-decoration:none; }
ul, ol { margin:6px 0 6px 4px; padding-left:20px; }
li { margin:2px 0; }
strong { color:#0d2340; }
blockquote { border-left:4px solid #f0a500; background:#fff9ec; margin:10px 0;
             padding:8px 14px; color:#5a4a20; border-radius:0 6px 6px 0; }
code { background:#eef4fb; color:#134e8a; padding:1px 5px; border-radius:4px;
       font-family:'Consolas','Courier New',monospace; font-size:10.5px; }
pre { background:#0d2340; color:#e8eef6; padding:12px 14px; border-radius:8px;
      overflow-x:auto; font-size:10px; line-height:1.5; margin:10px 0;
      border-left:4px solid #29b5e8; }
pre code { background:none; color:#e8eef6; padding:0; }
table { border-collapse:collapse; width:100%; margin:12px 0; font-size:10.5px; }
th { background:#134e8a; color:#fff; padding:7px 10px; text-align:left; font-weight:700; }
td { padding:6px 10px; border-bottom:1px solid #e3edf7; }
tr:nth-child(even) td { background:#f6faff; }
hr { border:none; border-top:1px solid #e3edf7; margin:18px 0; }
/* pygments code highlighting (dark) */
.codehilite pre { background:#0d2340; }
.codehilite .k, .codehilite .kd, .codehilite .kn { color:#7cc7ff; font-weight:600; }
.codehilite .s, .codehilite .s1, .codehilite .s2 { color:#ffd479; }
.codehilite .c, .codehilite .c1, .codehilite .cm { color:#6b8299; font-style:italic; }
.codehilite .nb, .codehilite .nf { color:#8be9fd; }
.codehilite .mi, .codehilite .mf { color:#ff9d6b; }
.codehilite .o { color:#ff79c6; }
.footer-note { margin-top:28px; padding-top:12px; border-top:2px solid #eef2f7;
               font-size:9.5px; color:#8892a4; text-align:center; }
"""

BRAND = (
    '<div class="brandbar"><span class="flake">&#10052;&#65039;</span>'
    '<span class="name">PJ&#39;s <em>Academy</em></span>'
    '<span class="tag">Snowflake Mastery</span></div>'
)
FOOTER = (
    '<div class="footer-note">&#10052;&#65039; Snowflake Mastery &mdash; '
    "PJ&#39;s Academy &middot; pjsacademy.com &middot; hello@pjsacademy.com "
    "&middot; @pjsacademy.datascience</div>"
)


def md_to_html(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=[
            "tables", "fenced_code", "toc", "sane_lists",
            CodeHiliteExtension(guess_lang=False, noclasses=False),
        ],
    )
    return (
        f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{PAGE_CSS}</style></head><body>{BRAND}{html_body}{FOOTER}</body></html>"
    )


def main():
    from playwright.sync_api import sync_playwright

    made = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for rel, outname in DOCS:
            src = ROOT / rel
            if not src.exists():
                print(f"  SKIP (missing): {rel}")
                continue
            html = md_to_html(src)
            page.set_content(html, wait_until="networkidle")
            pdf_path = OUT / f"{outname}.pdf"
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )
            kb = pdf_path.stat().st_size / 1024
            made.append((outname, kb))
            print(f"  [OK] {outname}.pdf  ({kb:.0f} KB)")
        browser.close()

    print(f"\nBuilt {len(made)} PDFs -> {OUT}")
    print("Certification & course guides are now available as branded PDFs.")


if __name__ == "__main__":
    main()
