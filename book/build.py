#!/usr/bin/env python3
"""Build the book: content/*.md -> dist/book.html -> dist/Network-Engineer-Placements-2027.pdf"""
import re, subprocess, pathlib, html, datetime

ROOT = pathlib.Path(__file__).resolve().parent
import sys
ONLY = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
CONTENT = sorted((ROOT / "content").glob((ONLY + "*") if ONLY else "*.md"))
OUT = ("preview-" + ONLY) if ONLY else "Network-Engineer-Placements-2027"
DIST = ROOT / "dist"; DIST.mkdir(exist_ok=True)

def pandoc(md: str) -> str:
    return subprocess.run(
        ["pandoc", "-f", "markdown+fenced_divs+bracketed_spans+pipe_tables+raw_html-smart+smart",
         "-t", "html5", "--highlight-style=pygments", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True).stdout

toc, body = [], []
for f in CONTENT:
    md = f.read_text()
    for m in re.finditer(r"^# (.+?) \{#([\w-]+)\}", md, re.M):
        num = re.search(r"\[(\w+)\]\{\.num\}", md)
        toc.append((num.group(1) if num else "", m.group(1), m.group(2)))
    h = pandoc(md)
    k = f.stem.replace('-', '')
    h = re.sub(r'(id="|href="#)(fn(?:ref)?\d+)', lambda m: m.group(1) + k + m.group(2), h)
    body.append(h)

joined = ''.join(body)
ids = set(re.findall(r'id="([^"]+)"', joined))
def _fix(m):
    return m.group(0) if m.group(2) in ids else m.group(0).replace('class="ref"', '')
joined = re.sub(r'<a href="#([^"]*)"[^>]*>', lambda m: m.group(0) if m.group(1) in ids else re.sub(r'\s*class="ref"', '', m.group(0)), joined)
body = [joined]
today = datetime.date.today().strftime("%d %B %Y")
cover = f"""<div class="cover p0"><div><div class="k">Placement edition · 2027</div>
<h1>Network Engineer<br>Placements 2027</h1>
<div class="sub">From first principles to the offer: networks, routing, systems, code and interviews for Cisco, Qualcomm, Google, Microsoft, Amazon, Juniper, Arista, Nokia and Broadcom.</div>
<div class="bar"></div></div><div class="foot">Working edition · built {today} · information correct as of this date</div></div>"""
toc_html = '<section class="p0"><div class="part-label">Contents</div><h1>Contents</h1><div class="toc-book"><ol>' + "".join(
    f'<li><a href="#{i}"><span style="display:inline-block;width:10mm;color:#5F6670">{html.escape(n)}</span>{html.escape(t)}</a></li>'
    for n, t, i in toc) + "</ol></div></section>"

page = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Network Engineer Placements 2027</title>
<style>{(ROOT/"css/book.css").read_text()}</style><script>window.PagedConfig={{auto:true}};</script>
<script src="../vendor/paged.polyfill.min.js"></script></head><body>{cover}{toc_html}{''.join(body)}</body></html>"""
(DIST / f"{OUT}.html").write_text(page)
subprocess.run(["node", str(ROOT / "render.mjs"), OUT], check=True, cwd=ROOT)
print("built", DIST / f"{OUT}.pdf")
