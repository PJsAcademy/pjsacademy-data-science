# -*- coding: utf-8 -*-
"""
PDF verification suite — checks every PDF in the repo and lets you eyeball them.

For each PDF it:
  - confirms it's a valid, non-empty PDF (correct header, readable pages)
  - records page count + file size
  - renders PAGE 1 to a PNG thumbnail (in pdf-tests/thumbnails/) for visual review
  - writes a pass/fail TEST_REPORT.md you can open to verify everything

Run:  py pdf-tests/verify_pdfs.py
"""
import sys
from pathlib import Path
import fitz  # pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).parent
ROOT = HERE.parent
THUMBS = HERE / "thumbnails"
THUMBS.mkdir(exist_ok=True)


def find_pdfs():
    return sorted(p for p in ROOT.rglob("*.pdf") if ".git" not in p.parts)


def check(pdf: Path):
    result = {"file": str(pdf.relative_to(ROOT)), "ok": False,
              "pages": 0, "kb": round(pdf.stat().st_size / 1024),
              "thumb": "", "error": ""}
    try:
        # 1) valid PDF header
        with open(pdf, "rb") as f:
            if f.read(5) != b"%PDF-":
                raise ValueError("missing %PDF- header")
        # 2) open + count pages
        doc = fitz.open(pdf)
        result["pages"] = doc.page_count
        if doc.page_count == 0:
            raise ValueError("zero pages")
        # 3) render page 1 to a thumbnail
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=90)
        thumb = THUMBS / (pdf.stem + ".png")
        pix.save(str(thumb))
        result["thumb"] = str(thumb.relative_to(HERE))
        doc.close()
        result["ok"] = True
    except Exception as e:
        result["error"] = str(e)
    return result


def main():
    pdfs = find_pdfs()
    print(f"Verifying {len(pdfs)} PDFs...\n")
    results = [check(p) for p in pdfs]

    passed = sum(1 for r in results if r["ok"])
    failed = len(results) - passed

    # console summary
    for r in results:
        status = "PASS" if r["ok"] else "FAIL"
        print(f"  [{status}] {r['file']}  ({r['pages']}p, {r['kb']}KB)"
              + (f"  ERROR: {r['error']}" if r["error"] else ""))
    print(f"\n{passed}/{len(results)} passed, {failed} failed.")

    # markdown report
    lines = ["# 🧪 PDF Verification Report — PJ's Academy\n",
             f"**{passed}/{len(results)} PDFs passed** · {failed} failed.\n",
             "Thumbnails of page 1 are in `thumbnails/` — open them to eyeball each PDF.\n",
             "| Status | PDF | Pages | Size | Page-1 Thumbnail |",
             "|--------|-----|-------|------|------------------|"]
    for r in results:
        icon = "✅" if r["ok"] else "❌"
        thumb = f"[view]({r['thumb']})" if r["thumb"] else (r["error"] or "-")
        lines.append(f"| {icon} | `{r['file']}` | {r['pages']} | {r['kb']} KB | {thumb} |")
    lines.append("\n---\n*Run `py pdf-tests/verify_pdfs.py` anytime to re-verify.*")
    (HERE / "TEST_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport: pdf-tests/TEST_REPORT.md   Thumbnails: pdf-tests/thumbnails/")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
