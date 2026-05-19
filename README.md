# putfig2pdf

**English** | [日本語](README.ja.md)

Replace filename-only placeholders that **start with `#`** (for example `#fig6.pdf`) in a manuscript PDF with the matching PDF from the same folder—at the same position and size—without rasterizing figures. Vector PDF pages stay vector when embedded. The leading `#` is not part of the file name on disk. Bare filenames such as `fig6.pdf` (no `#`) are **not** treated as placeholders and are left unchanged.

## Motivation

A typical workflow: export the Word document to PDF (e.g. via PrimoPDF), use **Insert → Shapes** in Word to place a rectangle labeled only with a placeholder such as `#fig6.pdf`, then swap that box for the real figure PDF. This script automates that last step on the PDF so you avoid pasting mixed vector/raster artwork into Word and losing vector quality.

## Requirements

- Python 3
- [PyMuPDF](https://pymupdf.readthedocs.io/) (`pymupdf`)

```bash
pip install pymupdf
```

## Usage

```bash
python putfig2pdf.py manuscript.pdf
```

### Layout

Put the manuscript and figure PDFs in the **same directory** as the input file, for example:

- `manuscript.pdf`
- `fig1.pdf`, `fig2.pdf`, `my-plot.pdf`, …

Placeholders in the PDF must be `#` followed by the file name only (case-insensitive). The `#` marks the slot for replacement; it is not part of the file name on disk. The same text **without** `#` is ignored (no replacement).

Examples:

- `#fig6` -> `fig6.pdf`
- `#fig6.pdf` -> `fig6.pdf`
- `#fig1.pdf` -> `fig1.pdf`
- `#my-plot.pdf` -> `my-plot.pdf`
- `fig6.pdf` (no `#`) -> not replaced

### Output

The script writes `<stem>_fig_replaced_<YYYYMMDD_HHMMSS>.pdf` next to the input (e.g. `manuscript_fig_replaced_20260504_161052.pdf`). The timestamp is the run time, inserted immediately before the `.pdf` extension.

### Behavior

1. Detect placeholder text and its bounding box.
2. Prefer a drawing rectangle that encloses the text (Word-style shape); otherwise expand the text box slightly.
3. Delete placeholder content in that rectangle using PDF redaction.
4. Overlay page 1 of the matched target PDF in that rectangle (`keep_proportion=True`).

Missing target PDF files are skipped with a warning.

## License

Add your preferred license when you publish the repository.
