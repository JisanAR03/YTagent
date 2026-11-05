# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown"]
# ///
"""make_pdf.py - turn a research brief (.md) into a PDF. Uses Microsoft Edge, which ships with Windows 11.

    uv run tools/make_pdf.py research/2026-11-05-cops.md             # -> output/2026-11-05-cops.pdf
    uv run tools/make_pdf.py research/2026-11-05-cops.md -o other.pdf

The .md stays the editable source; the PDF is the copy you read. Nothing is uploaded anywhere.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
EDGES = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
         r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

CSS = """
@page { size: A4; margin: 16mm 15mm; }
body { font: 10.5pt/1.5 "Segoe UI", Arial, sans-serif; color: #1a1a1a; }
h1 { font-size: 20pt; margin: 0 0 6pt; border-bottom: 2px solid #333; padding-bottom: 4pt; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; border-bottom: 1px solid #bbb; padding-bottom: 2pt; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 12pt 0 4pt; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #999; padding: 3pt 6pt; text-align: left; vertical-align: top; }
th { background: #eee; }
tr { break-inside: avoid; }
pre, code { font-family: Consolas, monospace; font-size: 9pt; }
pre { background: #f4f4f4; border: 1px solid #ddd; padding: 6pt; white-space: pre-wrap; word-wrap: break-word; break-inside: avoid; }
blockquote { margin: 8pt 0; padding: 4pt 10pt; border-left: 4px solid #888; background: #f7f7f7; }
ul { padding-left: 18pt; }
li { margin: 2pt 0; }
"""


LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


def blank_before_lists(text):
    # Python-Markdown only starts a list after a blank line; GitHub and most editors do not need one.
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and out and LIST_ITEM.match(line):
            prev = out[-1]
            if prev.strip() and not LIST_ITEM.match(prev) and not prev.startswith((" ", "\t", ">")):
                out.append("")
        out.append(line)
    return "\n".join(out)


def find_edge():
    for p in EDGES:
        if os.path.exists(p):
            return p
    sys.exit("Microsoft Edge not found. Open the .md in any editor and use Print > Save as PDF instead.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", help="the brief to convert")
    ap.add_argument("-o", "--out", help="PDF path (default: output/<same name>.pdf)")
    a = ap.parse_args()

    src = Path(a.md).resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    out = Path(a.out).resolve() if a.out else ROOT / "output" / (src.stem + ".pdf")
    out.parent.mkdir(parents=True, exist_ok=True)

    text = src.read_text(encoding="utf-8")
    text = re.sub(r"^(\s*[-*] )\[ \]", lambda m: m.group(1) + "\u2610", text, flags=re.M)      # task-list boxes
    text = re.sub(r"^(\s*[-*] )\[[xX]\]", lambda m: m.group(1) + "\u2611", text, flags=re.M)
    text = blank_before_lists(text)
    title = next((m.group(1) for m in re.finditer(r"^# (.+)$", text, re.M)), src.stem)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")

    edge = find_edge()
    # A throwaway profile on the same drive as the project: if Edge is already open, headless Edge with the
    # default profile hands off to that window and writes nothing. ignore_cleanup_errors: Edge may hold files briefly.
    with tempfile.TemporaryDirectory(prefix=".edge-", dir=ROOT, ignore_cleanup_errors=True) as tmp:
        page = Path(tmp) / "brief.html"
        page.write_text(html, encoding="utf-8")
        if out.exists():
            out.unlink()
        cmd = [edge, "--headless", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
               f"--user-data-dir={Path(tmp) / 'profile'}", f"--print-to-pdf={out}", page.as_uri()]
        try:
            subprocess.run(cmd, capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            sys.exit("Edge took more than 90 seconds and was stopped. Close all Edge windows and try again.")

    if not out.exists() or out.stat().st_size == 0 or out.read_bytes()[:5] != b"%PDF-":
        sys.exit("Edge did not write a valid PDF. Close all Edge windows and run it again.")
    print(f"{out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
