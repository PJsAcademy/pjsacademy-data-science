# -*- coding: utf-8 -*-
"""
Premium PDF renderer for SQL / ML / Prompt Engineering — reuses the same design
system built for Snowflake (cover pages, section dividers, styled code cards,
callout boxes) but parses the "# Module N: Title" pattern these courses use.

Run:  py build_premium_pdf_generic.py            (all 3 courses)
      py build_premium_pdf_generic.py --course sql
"""
import sys, re, json, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

ROOT = Path(__file__).parent
NAVY, NAVY2, BLUE, SNOW, GOLD, GOLD2 = "#0d0d1a", "#0d2340", "#134e8a", "#29b5e8", "#f0a500", "#ffc542"

COURSES = {
    "sql": {"name": "SQL Mastery", "dir": "sql-mastery-course/notebooks_v2",
            "out": "sql-mastery-course/pdfs/SQL_Mastery_PREMIUM.pdf", "lang": "sql"},
    "ml": {"name": "Machine Learning Mastery", "dir": "machine-learning-course/notebooks_v2",
           "out": "machine-learning-course/pdfs/ML_Mastery_PREMIUM.pdf", "lang": "python"},
    "prompt": {"name": "Prompt Engineering Mastery", "dir": "prompt-engineering-course/notebooks_v2",
               "out": "prompt-engineering-course/pdfs/Prompt_Engineering_PREMIUM.pdf", "lang": "python"},
}

CALLOUTS = [
    (re.compile(r"^>\s*(.*)", re.I), "💡", "TIP", "tip"),
    (re.compile(r"^\*\*Real[ -]?World.*?\*\*:?\s*(.*)", re.I), "🏢", "REAL WORLD", "rw"),
    (re.compile(r"^\*\*(?:Warning|Caution)\*\*:?\s*(.*)", re.I), "⚠️", "WARNING", "warn"),
    (re.compile(r"^\*\*(?:Remember|Note)\*\*:?\s*(.*)", re.I), "📌", "REMEMBER", "note"),
]

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1a2233; font-size: 12px; line-height: 1.75; margin: 0; }}
.content-page {{ padding: 16mm 16mm 18mm; }}
.cover-page {{ width:210mm; height:297mm; background: linear-gradient(135deg,{NAVY},{NAVY2}); color:#fff;
  padding: 30mm 22mm; position: relative; page-break-after: always; }}
.cover-eyebrow {{ color:{SNOW}; font-size: 12px; font-weight:700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; }}
.cover-chnum {{ color:{GOLD}; font-size: 16px; font-weight: 800; letter-spacing: 4px; margin-bottom: 8px; }}
.cover-title {{ font-size: 38px; font-weight: 800; line-height: 1.15; margin-bottom: 18px; max-width: 150mm; color: #fff !important; }}
.cover-goal {{ font-size: 15px; color: #cfd8e6; max-width: 145mm; line-height: 1.7; margin-bottom: 28px; }}
.cover-learn {{ background: rgba(255,255,255,.05); border-left: 4px solid {GOLD}; border-radius: 0 10px 10px 0; padding: 16px 20px; max-width: 150mm; }}
.lo-hdr {{ font-size: 13px; font-weight: 800; color:{GOLD}; letter-spacing:1px; margin-bottom: 10px; }}
.lo-item {{ font-size: 13px; color: #e8eef6; margin-bottom: 6px; display:flex; gap:8px; }}
.ck {{ color: #2ecc71; font-weight: 900; }}
.cover-brand {{ position:absolute; bottom: 18mm; left: 22mm; font-size:11px; color:#7a8aa3; }}
.sec-divider {{ display:flex; align-items:center; gap:10px; margin: 26px 0 6px; }}
.sec-line {{ flex:1; height:2px; background: linear-gradient(90deg, transparent, {SNOW}, transparent); }}
.sec-label {{ font-size: 11px; font-weight: 800; color:{BLUE}; letter-spacing: 3px; white-space:nowrap; }}
h1 {{ font-size: 22px; color:{NAVY2}; margin: 18px 0 10px; }}
h2 {{ font-size: 18px; color:{NAVY2}; margin: 20px 0 10px; padding-bottom:6px; border-bottom:2px solid #eef2f7; }}
h3 {{ font-size: 14.5px; color:{BLUE}; margin: 16px 0 8px; font-weight:700; }}
p {{ margin: 8px 0; color: #2a3547; }}
strong {{ color:{NAVY2}; }}
a {{ color:{BLUE}; }}
ul, ol {{ margin: 8px 0 8px 20px; }}
li {{ margin: 4px 0; }}
table {{ border-collapse: collapse; width:100%; margin: 14px 0; font-size:11px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }}
th {{ background:{BLUE}; color:#fff; padding:8px 11px; text-align:left; }}
td {{ padding:7px 11px; border-bottom:1px solid #e3edf7; }}
tr:nth-child(even) td {{ background: #f6faff; }}
code {{ background:#eef4fb; color:{BLUE}; padding:1.5px 5px; border-radius:4px; font-family:'Consolas',monospace; font-size:11px; }}
.sql-card {{ margin: 16px 0; border-radius: 10px; overflow:hidden; box-shadow: 0 6px 18px rgba(13,35,64,.15); page-break-inside: avoid; }}
.sql-hdr {{ background: #1c2b45; padding: 8px 14px; display:flex; align-items:center; gap:7px; }}
.dot {{ width:9px; height:9px; border-radius:50%; display:inline-block; }}
.dot.r {{ background:#ff5f56; }} .dot.y {{ background:#ffbd2e; }} .dot.g {{ background:#27c93f; }}
.sql-title {{ margin-left:8px; color:#8aa0c2; font-size:10.5px; font-weight:700; letter-spacing:0.5px; }}
.sql-body {{ background:{NAVY2}; padding: 12px 16px 14px; }}
.sql-body pre {{ margin:0; background:none !important; }}
.sql-body .codehilite {{ background:none !important; }}
.sql-body code, .sql-body pre code {{ background:none; color:#e8eef6; font-size:11px; line-height:1.65; }}
.sql-body .codehilite .k, .sql-body .codehilite .kd, .sql-body .codehilite .kn {{ color:#7cc7ff; font-weight:600; }}
.sql-body .codehilite .s, .sql-body .codehilite .s1, .sql-body .codehilite .s2 {{ color:{GOLD2}; }}
.sql-body .codehilite .c, .sql-body .codehilite .c1, .sql-body .codehilite .cm {{ color:#6b8299; font-style:italic; }}
.sql-body .codehilite .nb, .sql-body .codehilite .nf {{ color:{SNOW}; }}
.sql-body .codehilite .mi, .sql-body .codehilite .mf {{ color:#ff9d6b; }}
.callout {{ margin: 14px 0; border-radius: 10px; overflow:hidden; page-break-inside: avoid; box-shadow: 0 3px 10px rgba(0,0,0,.06); }}
.co-hdr {{ padding: 8px 14px; font-size: 11px; font-weight: 800; letter-spacing: 1px; color:#fff; }}
.co-body {{ padding: 10px 14px 13px; font-size: 12px; background:#fff; }}
.callout.tip .co-hdr {{ background: #0e9b6b; }} .callout.tip {{ border:1px solid #0e9b6b; }} .callout.tip .co-body{{background:#eafcf5;}}
.callout.rw .co-hdr {{ background: {NAVY2}; }} .callout.rw {{ border:1px solid {NAVY2}; }} .callout.rw .co-body{{background:#eef2f8;}}
.callout.warn .co-hdr {{ background: #e07b00; }} .callout.warn {{ border:1px solid #e07b00; }} .callout.warn .co-body{{background:#fff6e8;}}
.callout.note .co-hdr {{ background: {BLUE}; }} .callout.note {{ border:1px solid {BLUE}; }} .callout.note .co-body{{background:#eef4fb;}}
img {{ max-width: 100%; border-radius: 8px; margin: 12px 0; display:block; }}
.brandbar {{ display:flex; align-items:center; gap:8px; padding:8px 0 10px; border-bottom:2px solid {GOLD}; margin-bottom:14px; }}
.brandbar .name {{ font-weight:800; font-size:12px; color:{NAVY2}; }}
.brandbar .name em {{ color:{GOLD}; font-style:normal; }}
.brandbar .tag {{ margin-left:auto; font-size:9px; color:{SNOW}; font-weight:700; letter-spacing:1px; text-transform:uppercase; }}
.footer-note {{ margin-top: 20px; padding-top: 10px; border-top: 2px solid #eef2f7; font-size: 9px; color: #8892a4; text-align:center; }}
.mermaid-wrap {{ text-align:center; margin: 16px 0; page-break-inside: avoid; }}
"""

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"

FENCE = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
LEADING_HR_RE = re.compile(r"^\s*-{3,}\s*\n+")


def render_code_card(code_text, lang):
    highlighter = markdown.Markdown(extensions=["fenced_code", CodeHiliteExtension(guess_lang=False, noclasses=False)])
    escaped = highlighter.convert(f"```{lang}\n{code_text}\n```")
    label = "SQL &middot; Run this" if lang == "sql" else "Python &middot; Run this"
    return (f'<div class="sql-card"><div class="sql-hdr">'
            f'<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>'
            f'<span class="sql-title">{label}</span></div><div class="sql-body">{escaped}</div></div>')


def split_paragraphs(md_text):
    lines = md_text.split("\n"); chunks, buf, in_fence = [], [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence; buf.append(ln); continue
        if in_fence:
            buf.append(ln); continue
        if ln.strip() == "" and buf:
            chunks.append("\n".join(buf)); buf = []
        else:
            buf.append(ln)
    if buf: chunks.append("\n".join(buf))
    return [c for c in chunks if c.strip()]


def render_markdown_with_code_and_callouts(md_text, lang, md_conv):
    """Split by fenced code -> styled code cards; plain text -> callout-aware markdown."""
    parts, pos = [], 0
    for m in FENCE.finditer(md_text):
        before = md_text[pos:m.start()]
        if before.strip():
            for chunk in split_paragraphs(before):
                parts.append(render_chunk(chunk, md_conv))
        code_lang, code_body = m.group(1) or lang, m.group(2).rstrip("\n")
        if code_lang.lower() == "mermaid":
            parts.append(f'<div class="mermaid-wrap"><pre class="mermaid">{html.escape(code_body)}</pre></div>')
        else:
            parts.append(render_code_card(code_body, code_lang if code_lang in ("sql", "python", "py") else lang))
        pos = m.end()
    tail = md_text[pos:]
    if tail.strip():
        for chunk in split_paragraphs(tail):
            parts.append(render_chunk(chunk, md_conv))
    return "".join(parts)


def render_chunk(chunk, md_conv):
    stripped = chunk.strip()
    for pattern, icon, label, cls in CALLOUTS:
        m = pattern.match(stripped)
        if m:
            body = m.group(1).strip() or stripped
            body_html = md_conv.convert(body); md_conv.reset()
            return f'<div class="callout {cls}"><div class="co-hdr">{icon} {label}</div><div class="co-body">{body_html}</div></div>'
    out = md_conv.convert(chunk); md_conv.reset()
    return out


def build_cover(num, title, phase_name, learn_items, brand_tag):
    items_html = "".join(f'<div class="lo-item"><span class="ck">&#10003;</span>{html.escape(x)}</div>' for x in learn_items[:6])
    n = int(num) if str(num).isdigit() else 5
    stars = min(5, max(1, 1 + n // 3))
    mins = 20 + (n % 6) * 5
    return f"""<div class="cover-page">
  <div class="cover-eyebrow">{html.escape(phase_name.replace('_',' '))}</div>
  <div class="cover-chnum">MODULE {num}</div>
  <h1 class="cover-title">{html.escape(title)}</h1>
  <div class="cover-goal">Master {html.escape(title.lower())} with runnable examples, exercises, and real-world context.</div>
  <div class="cover-learn"><div class="lo-hdr">🎯 YOU WILL LEARN</div>{items_html}</div>
  <div class="cover-brand">&#10052;&#65039; {brand_tag}</div>
</div>"""


def render_tutorial(nb_path, phase_name, brand_tag, lang):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    cells = nb["cells"]
    first_md = "".join(cells[0]["source"]) if cells else ""
    m = re.search(r"^#\s*Module\s*(\d+):?\s*(.+)$", first_md, re.M)
    num, title = (m.group(1), m.group(2).strip()) if m else ("?", "Untitled")
    learn_items = re.findall(r"^\d+\.\s+(.+)$", first_md, re.M)
    cover = build_cover(num, title, phase_name, learn_items, brand_tag)

    md_conv = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    body_parts = []
    for cell in cells[1:]:
        text = "".join(cell["source"]) if cell["cell_type"] == "markdown" else ""
        if cell["cell_type"] == "code":
            code_text = "".join(cell["source"]).strip()
            if code_text: body_parts.append(render_code_card(code_text, lang))
            continue
        if not text.strip(): continue
        stripped = LEADING_HR_RE.sub("", text)
        body_parts.append(render_markdown_with_code_and_callouts(stripped, lang, md_conv))

    brand = (f'<div class="brandbar"><span>&#10052;&#65039;</span><span class="name">PJ&#39;s <em>Academy</em></span>'
             f'<span class="tag">{html.escape(brand_tag)} &middot; Premium Edition</span></div>')
    body_html = f'<div class="content-page">{brand}{"".join(body_parts)}<div class="footer-note">PJ&#39;s Academy &middot; pjsacademy.com &middot; hello@pjsacademy.com</div></div>'
    has_mermaid = 'class="mermaid"' in body_html
    mermaid_tag = f"<script src='{MERMAID_CDN}'></script>" if has_mermaid else ""
    mermaid_init = "<script>mermaid.initialize({startOnLoad:true, theme:'neutral'});</script>" if has_mermaid else ""
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style>{mermaid_tag}</head><body>{cover}{body_html}{mermaid_init}</body></html>"


def main():
    from playwright.sync_api import sync_playwright
    from pypdf import PdfWriter, PdfReader

    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--course":
        only = sys.argv[2]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(); page = browser.new_page()
        for key, cfg in COURSES.items():
            if only and key != only: continue
            print(f"\n=== {cfg['name']} ===")
            src = ROOT / cfg["dir"]
            writer = PdfWriter()
            tmp = Path(__file__).parent / "_tmp_g.pdf"
            n = 0
            for phase in sorted(p for p in src.iterdir() if p.is_dir() and p.name.startswith("Phase")):
                for ch in sorted(d for d in phase.iterdir() if d.is_dir() and d.name.startswith("Chapter")):
                    tut = next(ch.glob("*_Tutorial.ipynb"), None)
                    if not tut: continue
                    html_out = render_tutorial(tut, phase.name, cfg["name"], cfg["lang"])
                    page.set_content(html_out, wait_until="networkidle")
                    if 'class="mermaid"' in html_out:
                        page.wait_for_timeout(1200)
                    page.pdf(path=str(tmp), format="A4", print_background=True,
                             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
                    for pg in PdfReader(str(tmp)).pages:
                        writer.add_page(pg)
                    n += 1; print(f"  [{n}] {ch.name}")
            tmp.unlink(missing_ok=True)
            out = ROOT / cfg["out"]; out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: writer.write(f)
            print(f"  Built {out.name}: {len(writer.pages)} pages ({out.stat().st_size/1024:.0f} KB)")
        browser.close()


if __name__ == "__main__":
    main()
