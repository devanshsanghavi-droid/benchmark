"""Render paper/paper.md (+ paper/references.bib) to paper/build/paper.pdf.

Pipeline: pandoc (citeproc, MathML) -> standalone HTML with paper/style.css -> Chromium print-to-PDF.
Requires: pip install pypandoc_binary playwright ; a Chromium binary (PLAYWRIGHT chromium or CHROMIUM_PATH).
"""

import glob
import os
import sys

import pypandoc
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
BUILD = os.path.join(PAPER, "build")


def find_chromium():
    env = os.environ.get("CHROMIUM_PATH")
    if env and os.path.isfile(env):
        return env
    for cand in ["/opt/pw-browsers/chromium"] + sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")):
        if os.path.isfile(cand):
            return cand
    return None  # fall back to Playwright's own managed browser


def main():
    os.makedirs(BUILD, exist_ok=True)
    html_path = os.path.join(BUILD, "paper.html")
    pdf_path = os.path.join(BUILD, "paper.pdf")
    args = [
        "--standalone",
        "--mathml",
        "--citeproc",
        "--number-sections",
        f"--bibliography={os.path.join(PAPER, 'references.bib')}",
        f"--css={os.path.join(PAPER, 'style.css')}",
        "--embed-resources",
        f"--resource-path={PAPER}",
        "--metadata=link-citations:true",
    ]
    csl = os.path.join(PAPER, "acm.csl")
    if os.path.exists(csl):
        args.append(f"--csl={csl}")
    pypandoc.convert_file(os.path.join(PAPER, "paper.md"), "html5", extra_args=args, outputfile=html_path)

    with sync_playwright() as p:
        exe = find_chromium()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page()
        page.goto("file://" + html_path)
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=pdf_path,
            format="Letter",
            margin={"top": "0.8in", "bottom": "0.8in", "left": "0.85in", "right": "0.85in"},
            print_background=True,
            display_header_footer=True,
            header_template="<span></span>",
            footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#555">'
            '<span class="pageNumber"></span></div>',
        )
        browser.close()
    print(pdf_path, os.path.getsize(pdf_path), "bytes")


if __name__ == "__main__":
    sys.exit(main())
