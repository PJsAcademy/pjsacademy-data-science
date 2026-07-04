# -*- coding: utf-8 -*-
"""
Build the PJ's Academy Snowflake concept-infographic PDF (Instagram carousel style).
Same layout engine as the Python Data Science infographics, rebranded:
  - PJ's Academy brand + gold accent
  - Snowflake blue phase palette
  - @pjsacademy.datascience handle, DM "SNOWFLAKE"
Run:  py build_snowflake_infographic.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from snowflake_concepts import CONCEPTS
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUT_DIR = Path(__file__).parent
OUT_PDF = OUT_DIR / "PJs_Academy_Snowflake_Concepts.pdf"
TMP = Path.home() / "AppData" / "Local" / "Temp" / "snow_concept_pages"
TMP.mkdir(parents=True, exist_ok=True)

# Snowflake blue palette per phase
PHASE_COLORS = {
    "Phase 1": "#1a73c2",   # snow blue
    "Phase 2": "#0e9bd6",   # bright cyan-blue
    "Phase 3": "#2563a8",   # deep blue
    "Phase 4": "#0d7ab5",   # ocean
    "Phase 5": "#134e8a",   # navy blue
}
GOLD = "#f0a500"

def phase_color(p):
    for k, v in PHASE_COLORS.items():
        if k in p:
            return v
    return "#1a73c2"

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#eef4fb; font-family:'Segoe UI',Arial,sans-serif; }
.page { width:1200px; background:#eef4fb; display:flex; flex-direction:column; }
.brand-bar { display:flex; align-items:center; gap:10px; padding:9px 26px 7px; border-bottom:1.5px solid rgba(0,0,0,.08); background:#fff; }
.brand-name { font-weight:800; color:#111; font-size:13px; }
.brand-name em { color:%GOLD%; font-style:normal; }
.series-pill { color:white; font-size:10px; font-weight:700; letter-spacing:.8px; padding:3px 12px; border-radius:10px; }
.body-wrap { display:flex; flex:1; }
.col-left  { width:420px; flex-shrink:0; background:#f6faff; padding:17px 22px 0; border-right:2px solid rgba(0,0,0,.06); display:flex; flex-direction:column; }
.col-right { flex:1; background:#fff; padding:17px 24px 0; display:flex; flex-direction:column; }
.pg-num { width:52px; height:52px; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; font-size:11px; font-weight:900; color:white; line-height:1.15; text-align:center; position:absolute; top:0; right:0; }
.title-wrap { position:relative; margin-bottom:10px; }
.main-title { font-size:46px; font-weight:900; line-height:1.02; color:#111; letter-spacing:-2px; white-space:pre-line; padding-right:58px; }
.description { font-size:11px; color:#444; line-height:1.65; margin-bottom:12px; }
.sec-hdr { display:flex; align-items:center; gap:8px; font-size:9.5px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; margin-bottom:6px; }
.sec-rule { flex:1; height:1.5px; background:currentColor; opacity:.22; }
.why-list { display:flex; flex-direction:column; gap:4px; margin-bottom:12px; }
.why-item { display:flex; align-items:flex-start; gap:6px; font-size:10.5px; color:#222; line-height:1.5; }
.ck { font-weight:900; font-size:12px; flex-shrink:0; margin-top:1px; }
.types-wrap { display:flex; flex-direction:column; gap:5px; margin-bottom:12px; }
.type-row { display:flex; align-items:flex-start; gap:8px; }
.type-icon { font-size:16px; flex-shrink:0; }
.type-body strong { font-size:11px; color:#111; display:block; }
.type-body small { font-size:9.5px; color:#555; }
.quote-card { background:white; border-radius:8px; padding:13px 15px 11px; font-size:12px; line-height:1.65; color:#222; box-shadow:3px 5px 14px rgba(0,0,0,.10); margin-bottom:12px; position:relative; white-space:pre-line; }
.quote-mark { font-size:48px; color:#cfe0f2; line-height:0; font-family:Georgia,serif; position:absolute; top:20px; left:10px; }
.quote-inner { padding-left:28px; }
.quote-by { font-size:9.5px; color:#aaa; margin-top:6px; letter-spacing:.5px; text-transform:uppercase; }
.big-picture { background:%GOLD%; border-radius:6px; padding:12px 13px; box-shadow:2px 4px 12px rgba(0,0,0,.12); margin-bottom:12px; }
.bp-hdr { font-size:9.5px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; color:#333; margin-bottom:8px; }
.bp-flow { display:flex; align-items:center; gap:3px; flex-wrap:wrap; }
.bp-box { background:white; border-radius:4px; padding:6px 8px; text-align:center; font-size:9.5px; font-weight:700; color:#111; line-height:1.3; box-shadow:1px 2px 4px rgba(0,0,0,.10); min-width:56px; white-space:pre-line; }
.bp-arr { font-size:13px; color:#555; }
.bp-note { font-size:9.5px; color:#555; font-style:italic; margin-top:6px; }
.glance-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:5px; margin-bottom:12px; }
.glance-cell { background:white; border-radius:5px; padding:8px 9px; box-shadow:1px 2px 5px rgba(0,0,0,.06); }
.glance-emoji { font-size:16px; display:block; margin-bottom:3px; }
.glance-label { font-size:8.5px; color:#888; text-transform:uppercase; letter-spacing:.5px; display:block; }
.glance-val { font-size:10px; font-weight:700; color:#111; display:block; }
.rw-grid { display:grid; grid-template-columns:1fr 1fr; gap:5px; margin-bottom:12px; }
.rw-card { background:white; border-radius:6px; padding:9px 11px; box-shadow:1px 2px 5px rgba(0,0,0,.06); }
.rw-top { display:flex; align-items:center; gap:8px; margin-bottom:3px; }
.rw-logo { width:34px; height:34px; border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:17px; flex-shrink:0; }
.rw-company { font-size:11px; font-weight:800; color:#111; }
.rw-desc { font-size:9.5px; color:#555; line-height:1.4; }
.dyk-box { background:%GOLD%; border-radius:6px; padding:10px 12px; margin-bottom:12px; }
.dyk-hdr { font-size:9.5px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; color:#333; margin-bottom:7px; }
.dyk-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:5px; }
.dyk-cell { background:white; border-radius:5px; padding:8px 9px; font-size:9.5px; color:#333; line-height:1.45; }
.dyk-emoji { font-size:16px; display:block; margin-bottom:4px; }
.cta-banner { background:#0d2340; color:white; padding:12px 15px; margin:auto -22px 0; }
.cta-inner { display:flex; align-items:flex-start; gap:10px; }
.cta-gift { font-size:22px; }
.cta-text-block { flex:1; }
.cta-title { font-size:11.5px; font-weight:800; color:%GOLD%; letter-spacing:.3px; margin-bottom:2px; }
.cta-body { font-size:9.5px; color:#bbb; line-height:1.5; }
.cta-dm { text-align:center; border-radius:6px; padding:9px 11px; flex-shrink:0; min-width:110px; }
.cta-dm-label { font-size:8.5px; color:rgba(255,255,255,.8); text-transform:uppercase; letter-spacing:.5px; margin-bottom:2px; }
.cta-dm-val { font-size:12px; font-weight:900; color:white; }
.how-steps-h { display:flex; align-items:flex-start; gap:5px; margin-top:7px; margin-bottom:14px; }
.how-step-h { flex:1; display:flex; flex-direction:column; align-items:center; text-align:center; }
.how-num-circle { width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:17px; font-weight:900; color:white; margin-bottom:5px; }
.how-card-r { background:#eef4fb; border-radius:7px; width:100%; padding:10px 5px; display:flex; flex-direction:column; align-items:center; gap:3px; min-height:84px; justify-content:center; }
.how-big-icon { font-size:26px; }
.how-label { font-size:9.5px; font-weight:800; text-transform:uppercase; letter-spacing:.5px; color:#111; margin-top:2px; }
.how-desc { font-size:9px; color:#555; line-height:1.4; white-space:pre-line; }
.how-connector { padding-top:50px; color:#ccdcef; font-size:17px; font-weight:900; flex-shrink:0; }
.ex-flow { display:flex; align-items:stretch; gap:5px; margin-top:7px; margin-bottom:14px; }
.ex-card { flex:1; background:#f6faff; border-radius:6px; padding:10px 8px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:3px; }
.ex-icon { font-size:21px; }
.ex-label { font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:.4px; }
.ex-val { font-size:9.5px; color:#333; font-family:monospace; line-height:1.4; white-space:pre-line; }
.ex-arr { font-size:13px; color:#ccc; flex-shrink:0; align-self:center; }
.grid3 { display:flex; border:1.5px solid #e3edf7; border-radius:6px; overflow:hidden; background:white; margin-bottom:10px; }
.gcol { flex:1; padding:9px 11px; border-right:1.5px solid #eef4fb; }
.gcol:last-child { border-right:none; }
.gcol-hdr { font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:1.1px; padding-bottom:5px; margin-bottom:5px; border-bottom:1.5px solid #eef4fb; }
.gi { font-size:9.5px; color:#222; line-height:1.5; margin-bottom:2px; padding-left:11px; position:relative; }
.gi::before { content:'›'; position:absolute; left:0; font-weight:900; }
.gi2 { display:flex; align-items:flex-start; gap:5px; font-size:9.5px; color:#222; line-height:1.5; margin-bottom:2px; }
.insight-bar { border-radius:6px; padding:9px 14px; color:white; font-size:11px; font-style:italic; font-weight:600; line-height:1.5; margin-bottom:10px; display:flex; align-items:center; gap:8px; }
.qr-wrap { border:1.5px solid #e3edf7; border-radius:6px; overflow:hidden; margin-bottom:10px; flex:1; align-self:stretch; }
.qr-grid { display:grid; grid-template-columns:1fr 1fr; }
.qr-section { border-right:1.5px solid #e3edf7; border-bottom:1.5px solid #e3edf7; }
.qr-section:nth-child(2n) { border-right:none; }
.qr-section:nth-child(3), .qr-section:nth-child(4) { border-bottom:none; }
.qr-hdr { padding:6px 11px; font-size:8.5px; font-weight:800; text-transform:uppercase; letter-spacing:.9px; color:white; }
.qr-row { display:flex; align-items:flex-start; gap:6px; padding:4px 11px; border-bottom:1px solid #f2f7fc; }
.qr-row:last-child { border-bottom:none; }
.qr-term { font-family:monospace; font-size:9px; font-weight:700; white-space:nowrap; min-width:110px; flex-shrink:0; }
.qr-desc { font-size:9.5px; color:#444; line-height:1.4; }
.next-up { background:#0d2340; color:white; border-radius:7px; padding:12px 16px; margin-bottom:10px; display:flex; align-items:center; gap:12px; }
.next-left { flex:1; }
.next-label { font-size:8.5px; text-transform:uppercase; letter-spacing:1.2px; color:#7fa8d4; margin-bottom:3px; }
.next-title { font-size:14px; font-weight:900; color:white; margin-bottom:3px; }
.next-desc { font-size:9.5px; color:#aac4e2; line-height:1.4; }
.next-right { display:flex; flex-direction:column; align-items:center; gap:2px; flex-shrink:0; }
.next-pg { font-size:26px; font-weight:900; }
.next-pg-label { font-size:8.5px; color:#7fa8d4; text-transform:uppercase; letter-spacing:.5px; }
.bottom-bar { background:#0d2340; color:white; padding:9px 0; display:flex; justify-content:center; align-items:stretch; margin:0 -24px; }
.bb-item { padding:0 20px; font-size:9px; font-weight:700; letter-spacing:.8px; text-transform:uppercase; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px; border-right:1px solid #1c3a5e; }
.bb-item:last-child { border-right:none; }
.bb-sub { font-size:8px; font-weight:400; opacity:.5; text-transform:none; letter-spacing:0; }
.bb-icon { font-size:14px; margin-bottom:2px; }
.bonus-bar { background:#0d2340; color:white; padding:8px 24px; display:flex; align-items:center; gap:12px; margin:0 -24px; }
.key-tips { border-radius:7px; padding:11px 15px; margin-bottom:10px; border:1.5px solid var(--ac); }
.kt-hdr { font-size:9.5px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; margin-bottom:7px; color:var(--ac); }
.kt-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; }
.kt-cell { background:#f6faff; border-radius:5px; padding:8px 10px; border-left:3px solid var(--ac); }
.kt-num { font-size:18px; font-weight:900; color:var(--ac); line-height:1; margin-bottom:3px; }
.kt-text { font-size:9.5px; color:#333; line-height:1.45; }
.bonus-label { font-size:9.5px; font-weight:800; color:%GOLD%; white-space:nowrap; }
.bonus-items { display:flex; align-items:center; gap:14px; flex:1; }
.bonus-item { font-size:9px; color:#ccc; display:flex; align-items:center; gap:5px; }
.bonus-check { color:#27ae60; font-weight:900; font-size:10px; }
""".replace("%GOLD%", GOLD)


def bp_html(boxes):
    out = []
    for i, b in enumerate(boxes):
        out.append(f'<div class="bp-box">{b}</div>')
        if i < len(boxes) - 1:
            out.append('<span class="bp-arr">&#10230;</span>')
    return ''.join(out)


def gcol_html(title, items, ac):
    rows = []
    for it in items:
        if isinstance(it, tuple):
            rows.append(f'<div class="gi2"><span>{it[0]}</span><span>{it[1]}</span></div>')
        else:
            rows.append(f'<div class="gi">{it}</div>')
    return f'<div class="gcol"><div class="gcol-hdr" style="color:{ac}">{title}</div>{"".join(rows)}</div>'


def render(c, total):
    ac = phase_color(c['phase'])
    num = c['num']
    total_s = str(total)

    why_html = ''.join(f'<div class="why-item"><span class="ck" style="color:{ac}">&#10003;</span>{w}</div>' for w in c['why'])
    types_html = ''.join(f'<div class="type-row"><div class="type-icon">{ic}</div><div class="type-body"><strong>{nm}</strong><small>{ds}</small></div></div>' for ic, nm, ds in c['types'])

    how_html = ''
    for i, (ic, nm, ds) in enumerate(c['how']):
        how_html += f'<div class="how-step-h"><div class="how-num-circle" style="background:{ac}">{i+1}</div><div class="how-card-r"><div class="how-big-icon">{ic}</div><div class="how-label">{nm}</div><div class="how-desc">{ds}</div></div></div>'
        if i < len(c['how']) - 1:
            how_html += '<div class="how-connector">&#10230;</div>'

    ex_html = ''
    for i, (ic, lb, vl) in enumerate(c['ex_cards']):
        ex_html += f'<div class="ex-card"><div class="ex-icon">{ic}</div><div class="ex-label" style="color:{ac}">{lb}</div><div class="ex-val">{vl}</div></div>'
        if i < len(c['ex_cards']) - 1:
            ex_html += '<div class="ex-arr">&#10230;</div>'

    g1_html = ''.join(gcol_html(t, items, ac) for t, items in c['g1'])
    g2_html = ''.join(gcol_html(t, items, ac) for t, items in c['g2'])
    glance_html = ''.join(f'<div class="glance-cell"><span class="glance-emoji">{em}</span><span class="glance-label">{lbl}</span><span class="glance-val">{val}</span></div>' for em, lbl, val in c.get('at_a_glance', []))

    rw_colors = [ac, "#0d2340", "#0e9bd6", "#134e8a"]
    rw_html = ''.join(f'<div class="rw-card"><div class="rw-top"><div class="rw-logo" style="background:{rw_colors[i%4]}22">{em}</div><span class="rw-company">{co}</span></div><div class="rw-desc">{desc}</div></div>' for i, (em, co, desc) in enumerate(c.get('real_world', [])))
    dyk_html = ''.join(f'<div class="dyk-cell"><span class="dyk-emoji">{em}</span>{txt}</div>' for em, txt in c.get('did_you_know', []))

    qr_html = ''
    for title, rows in c.get('quick_ref', []):
        rows_html = ''.join(f'<div class="qr-row"><span class="qr-term" style="color:{ac}">{t}</span><span class="qr-desc">{d}</span></div>' for t, d in rows)
        qr_html += f'<div class="qr-section"><div class="qr-hdr" style="background:{ac}">{title}</div>{rows_html}</div>'

    next_title = c.get('next_up', 'Keep Building!')
    next_desc = c.get('next_desc', '')
    try:
        next_num = str(int(num) + 1).zfill(2) if int(num) < total else '01'
    except ValueError:
        next_num = '01'

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{CSS}
:root{{--ac:{ac};}}
.gi::before{{color:{ac};}}
</style></head><body>
<div class="page">
  <div class="brand-bar">
    <span style="font-size:16px">&#10052;&#65039;</span>
    <span class="brand-name">PJ's <em>Academy</em> &nbsp;&middot;&nbsp; @pjsacademy.datascience</span>
    <span style="flex:1"></span>
    <span class="series-pill" style="background:{ac}">{c['phase'].upper()}</span>
  </div>
  <div class="body-wrap">
    <div class="col-left">
      <div class="title-wrap">
        <div class="pg-num" style="background:{ac}">{num}<br>/{total_s}</div>
        <h1 class="main-title">{c['title']}</h1>
      </div>
      <p class="description">{c['description']}</p>
      <div class="sec-hdr" style="color:{ac}">{c['why_title']} <div class="sec-rule"></div></div>
      <div class="why-list">{why_html}</div>
      <div class="sec-hdr" style="color:{ac}">{c['types_title']} <div class="sec-rule"></div></div>
      <div class="types-wrap">{types_html}</div>
      <div class="quote-card"><span class="quote-mark">&ldquo;</span><div class="quote-inner">{c['quote']}<div class="quote-by">&mdash; PJ's Academy</div></div></div>
      <div class="big-picture"><div class="bp-hdr">&#9889; THE BIG PICTURE</div><div class="bp-flow">{bp_html(c['bp_boxes'])}</div><div class="bp-note">{c['bp_note']}</div></div>
      <div class="sec-hdr" style="color:{ac}">AT A GLANCE <div class="sec-rule"></div></div>
      <div class="glance-grid">{glance_html}</div>
      <div class="sec-hdr" style="color:{ac}">REAL WORLD EXAMPLES <div class="sec-rule"></div></div>
      <div class="rw-grid">{rw_html}</div>
      <div class="dyk-box"><div class="dyk-hdr">&#128161; DID YOU KNOW?</div><div class="dyk-grid">{dyk_html}</div></div>
      <div class="cta-banner"><div class="cta-inner"><span class="cta-gift">&#10052;&#65039;</span><div class="cta-text-block"><div class="cta-title">SNOWFLAKE MASTERY AWAITS...</div><div class="cta-body">12 visual concepts &middot; 20 projects &middot; full SnowPro Core cert prep</div></div><div class="cta-dm" style="background:{ac}"><div class="cta-dm-label">DM</div><div class="cta-dm-val">"SNOWFLAKE"</div></div></div></div>
    </div>
    <div class="col-right">
      <div class="sec-hdr" style="color:{ac}">{c['how_title']} <div class="sec-rule"></div></div>
      <div class="how-steps-h">{how_html}</div>
      <div class="sec-hdr" style="color:{ac}">{c['ex_title']} <div class="sec-rule"></div></div>
      <div class="ex-flow">{ex_html}</div>
      <div class="grid3">{g1_html}</div>
      <div class="grid3">{g2_html}</div>
      <div class="key-tips">
        <div class="kt-hdr">&#127919; KEY TAKEAWAYS</div>
        <div class="kt-grid">{"".join(f'<div class="kt-cell"><div class="kt-num">0{i+1}</div><div class="kt-text">{tip}</div></div>' for i, tip in enumerate(c["why"][:3]))}</div>
      </div>
      <div class="insight-bar" style="background:{ac}">&#9889; &nbsp;<em>{c['footer']}</em></div>
      <div class="sec-hdr" style="color:{ac}">QUICK REFERENCE <div class="sec-rule"></div></div>
      <div class="qr-wrap"><div class="qr-grid">{qr_html}</div></div>
      <div class="next-up">
        <div class="next-left"><div class="next-label">NEXT UP IN THE SERIES</div><div class="next-title">{next_title}</div><div class="next-desc">{next_desc}</div></div>
        <div class="next-right"><div class="next-pg" style="color:{ac}">{next_num}</div><div class="next-pg-label">/{total_s}</div></div>
      </div>
      <div class="bottom-bar">
        <div class="bb-item"><div class="bb-icon">&#128278;</div>SAVE IT<div class="bb-sub">Save for later</div></div>
        <div class="bb-item"><div class="bb-icon">&#8599;&#65039;</div>SHARE IT<div class="bb-sub">Help others learn</div></div>
        <div class="bb-item"><div class="bb-icon">&#128100;</div>FOLLOW<div class="bb-sub">@pjsacademy.datascience</div></div>
        <div class="bb-item"><div class="bb-icon">&#10052;&#65039;</div>LEARN. BUILD. CERTIFY.<div class="bb-sub">Snowflake, mastered.</div></div>
      </div>
      <div class="bonus-bar">
        <div class="bonus-label">&#127873; BONUS RESOURCE</div>
        <div class="bonus-items">
          <div class="bonus-item"><span class="bonus-check">&#10003;</span>60+ SnowPro Practice Qs</div>
          <div class="bonus-item"><span class="bonus-check">&#10003;</span>20 Hands-On Projects</div>
          <div class="bonus-item"><span class="bonus-check">&#10003;</span>SnowPro Core Cheatsheet</div>
        </div>
        <span style="font-size:8px;color:#88a">pjsacademy.com</span>
      </div>
    </div>
  </div>
</div>
</body></html>"""


from playwright.sync_api import sync_playwright
from PIL import Image

total = len(CONCEPTS)
png_paths = []
print(f"Rendering {total} Snowflake concept pages...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1200, "height": 1600})
    pg = ctx.new_page()
    for i, c in enumerate(CONCEPTS):
        html = render(c, total)
        tmp_html = TMP / f"p{i:02d}.html"
        tmp_html.write_text(html, encoding='utf-8')
        pg.goto(f"file:///{tmp_html.as_posix()}")
        pg.wait_for_load_state("networkidle")
        h = pg.evaluate("document.querySelector('.page').scrollHeight")
        pg.set_viewport_size({"width": 1200, "height": h})
        out = TMP / f"p{i:02d}.png"
        pg.screenshot(path=str(out), full_page=False, clip={"x": 0, "y": 0, "width": 1200, "height": h})
        png_paths.append(out)
        print(f"  [{c['num']}/{total}] {c['title'].replace(chr(10),' ')} ({h}px)")
    browser.close()

print(f"\nMerging {len(png_paths)} pages into PDF...")
imgs = [Image.open(p).convert('RGB') for p in png_paths]
imgs[0].save(str(OUT_PDF), save_all=True, append_images=imgs[1:], resolution=150)
print(f"Done -> {OUT_PDF}  ({OUT_PDF.stat().st_size/1024:.0f} KB)")
for p in png_paths:
    p.unlink(missing_ok=True)
