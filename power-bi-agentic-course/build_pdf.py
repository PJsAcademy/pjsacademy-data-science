#!/usr/bin/env python3
"""Build a single PDF from the Power BI agentic prep course markdown.

Pipeline: pandoc MD -> HTML fragments, swap mermaid code blocks for divs,
inline mermaid.min.js, render with headless chromium.
"""
import subprocess, sys, re, shutil, html as htmllib
from pathlib import Path

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "pdfs"
OUT_DIR.mkdir(exist_ok=True)
OUT_HTML = OUT_DIR / "PowerBI_2027_Prep.html"
OUT_PDF = OUT_DIR / "PowerBI_2027_Prep.pdf"

MERMAID_JS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/tmp/claude-0/-home-user-pjsacademy-data-science/3bb2a8ac-2b23-5733-b8e6-20c05f19833c/scratchpad/mermaid.min.js"
)

FILES = [
    "README.md",
    "01-tmdl-view.md",
    "02-udfs.md",
    "03-pbip-git.md",
    "04-mcp-ai-agents.md",
    "05-copilot-fabric-iq.md",
    "06-service-and-ux.md",
    "07-roadmap-and-skill-stack.md",
]

CSS = r"""
@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
html, body { background: #ffffff; }
body {
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color: #1a2233;
  font-size: 11pt;
  line-height: 1.55;
  margin: 0;
}
.cover {
  page-break-after: always;
  height: 260mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20mm;
  background: linear-gradient(135deg, #0d0d1a 0%, #1a1a3a 55%, #2d1b5e 100%);
  color: #ffffff;
  margin: -18mm -16mm 0 -16mm;
}
.cover .eyebrow { color: #a78bfa; letter-spacing: 3px; font-size: 11pt; font-weight: 700; margin-bottom: 18mm; }
.cover h1 { font-size: 42pt; line-height: 1.1; margin: 0 0 10mm 0; color: #ffffff; }
.cover .sub { font-size: 15pt; color: #c4b5fd; max-width: 150mm; }
.cover .footer { margin-top: auto; color: #a78bfa; font-size: 10pt; }
.module { page-break-before: always; }
.module:first-of-type { page-break-before: auto; }
h1 { color: #1e1b4b; font-size: 22pt; border-bottom: 3px solid #7c3aed; padding-bottom: 4px; margin-top: 6mm; }
h2 { color: #312e81; font-size: 15pt; margin-top: 8mm; border-left: 4px solid #7c3aed; padding-left: 8px; }
h3 { color: #4338ca; font-size: 12pt; margin-top: 6mm; }
h4 { color: #4338ca; font-size: 11pt; margin-top: 4mm; }
p, li { font-size: 10.5pt; }
code { font-family: 'JetBrains Mono', 'Consolas', 'Menlo', monospace; font-size: 9pt; background: #f1f0fb; color: #4c1d95; padding: 1px 5px; border-radius: 3px; }
pre { background: #0f172a; color: #e2e8f0; padding: 10px 14px; border-radius: 6px; overflow-x: auto; font-size: 8.5pt; line-height: 1.45; page-break-inside: avoid; }
pre code { background: transparent; color: inherit; padding: 0; font-size: inherit; }
blockquote { border-left: 4px solid #a78bfa; background: #faf5ff; margin: 4mm 0; padding: 3mm 5mm; color: #4c1d95; font-style: italic; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; margin: 4mm 0; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #cbd5e1; padding: 5px 8px; text-align: left; vertical-align: top; }
th { background: #ede9fe; color: #312e81; }
tr:nth-child(even) td { background: #faf5ff; }
.mermaid { background: #ffffff; padding: 4mm; margin: 4mm 0; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; page-break-inside: avoid; }
.mermaid svg { max-width: 100%; height: auto; }
a { color: #6d28d9; text-decoration: none; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 6mm 0; }
ul, ol { padding-left: 6mm; }
li { margin: 1mm 0; }
"""

MERMAID_INIT = r"""
<script>
window.MERMAID_READY = false;
document.addEventListener("DOMContentLoaded", async () => {
  try {
    mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose',
      themeVariables: { primaryColor: '#ede9fe', primaryTextColor: '#312e81',
        primaryBorderColor: '#7c3aed', lineColor: '#6d28d9', fontSize: '13px' } });
    await mermaid.run({ querySelector: '.mermaid' });
  } catch (e) { console.error('mermaid error', e); }
  window.MERMAID_READY = true;
  document.title = (document.title || '') + ' [READY]';
});
</script>
"""

def md_to_html_fragment(md_path: Path) -> str:
    result = subprocess.run(
        ["pandoc", "--from=gfm+pipe_tables", "--to=html5", "--no-highlight", str(md_path)],
        capture_output=True, text=True, check=True,
    )
    frag = result.stdout
    # Swap pandoc's <pre><code class="mermaid"> blocks for <div class="mermaid">.
    def swap(m):
        inner = htmllib.unescape(m.group(1))
        return f'<div class="mermaid">\n{inner}\n</div>'
    frag = re.sub(
        r'<pre><code class="mermaid">(.*?)</code></pre>',
        swap, frag, flags=re.DOTALL,
    )
    # Pandoc 3.1 sometimes emits <pre class="mermaid"><code>...</code></pre>; cover that too.
    frag = re.sub(
        r'<pre class="mermaid"><code>(.*?)</code></pre>',
        swap, frag, flags=re.DOTALL,
    )
    return frag

def build_html():
    fragments = []
    for i, name in enumerate(FILES):
        frag = md_to_html_fragment(ROOT / name)
        cls = "module" if i > 0 else "module first"
        fragments.append(f'<section class="{cls}">\n{frag}\n</section>')

    cover = """
    <section class="cover">
      <div class="eyebrow">POWER BI DEVELOPMENT &middot; PJs ACADEMY</div>
      <h1>Power BI 2027 Prep</h1>
      <div class="sub">Agentic, AI-ready development.
        TMDL, UDFs, PBIP+Git, MCP, Copilot, Fabric IQ &mdash; in the order
        you should learn them.</div>
      <div class="footer">A 7-module tutorial course</div>
    </section>
    """

    mermaid_js = MERMAID_JS.read_text(encoding="utf-8")
    body = cover + "\n".join(fragments)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Power BI 2027 Prep</title>
<style>{CSS}</style>
<script>{mermaid_js}</script>
{MERMAID_INIT}
</head>
<body>
{body}
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[html] {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")

def build_pdf():
    chromium = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    cmd = [
        chromium, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
        OUT_HTML.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"[pdf]  {OUT_PDF} ({OUT_PDF.stat().st_size:,} bytes)")

if __name__ == "__main__":
    build_html()
    build_pdf()
