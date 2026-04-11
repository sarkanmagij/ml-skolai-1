#!/usr/bin/env python3
"""
Export Jupyter notebook(s) to PDF via nbconvert WebPDF (headless Chromium).

This avoids the LaTeX/xelatex stack that Cursor's built-in "Export to PDF" uses,
which often fails on BasicTeX (e.g. missing rsfs fonts).

Usage:
  python3 export_notebook_pdf.py                    # default notebook in this repo
  python3 export_notebook_pdf.py mynotebook.ipynb
  python3 export_notebook_pdf.py a.ipynb b.ipynb

One-time setup:
  pip install 'nbconvert[webpdf]' playwright
  python3 -m playwright install chromium
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _export_one(nb_path: Path) -> Path:
    import nbformat
    from nbconvert.exporters import WebPDFExporter

    nb_path = nb_path.resolve()
    if not nb_path.is_file():
        raise FileNotFoundError(nb_path)

    with nb_path.open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    exporter = WebPDFExporter()
    pdf_bytes, _ = exporter.from_notebook_node(nb)

    out_path = nb_path.with_suffix(".pdf")
    out_path.write_bytes(pdf_bytes)
    return out_path


def main() -> int:
    default_nb = Path(__file__).parent / "05_LinearRegression_AutoMPG_unsolved.ipynb"
    parser = argparse.ArgumentParser(description="Export notebook(s) to PDF (WebPDF, no LaTeX).")
    parser.add_argument(
        "notebooks",
        nargs="*",
        type=Path,
        help="Notebook path(s). Default: 05_LinearRegression_AutoMPG_unsolved.ipynb",
    )
    args = parser.parse_args()
    notebooks = list(args.notebooks) if args.notebooks else []
    if not notebooks and default_nb.is_file():
        notebooks = [default_nb]
    if not notebooks:
        print("No notebook specified and default not found.", file=sys.stderr)
        return 1

    try:
        import nbformat  # noqa: F401
        from nbconvert.exporters import WebPDFExporter  # noqa: F401
    except ImportError as e:
        print(
            "Missing packages. Install with:\n"
            "  pip install 'nbconvert[webpdf]' nbformat playwright\n"
            "  python3 -m playwright install chromium",
            file=sys.stderr,
        )
        print(e, file=sys.stderr)
        return 1

    for nb in notebooks:
        try:
            out = _export_one(nb)
            print(f"Wrote {out}")
        except Exception as e:
            err = str(e).lower()
            if "playwright" in err or "chromium" in err or "browser" in err:
                print(
                    "WebPDF needs Chromium. Run:\n  python3 -m playwright install chromium",
                    file=sys.stderr,
                )
            print(f"Failed {nb}: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
