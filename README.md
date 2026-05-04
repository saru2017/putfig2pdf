# pdfigswap

**English** | [日本語](README.ja.md)

Replace “Insert Figure # here” placeholders in a manuscript PDF with `fig#.pdf` from the same folder—at the same position and size—without rasterizing figures. Vector PDF pages stay vector when embedded.

## Motivation

A typical workflow: export the Word document to PDF (e.g. via PrimoPDF), use **Insert → Shapes** in Word to place a rectangle labeled “Insert Figure # here”, then swap that box for the real figure PDF. This script automates that last step on the PDF so you avoid pasting mixed vector/raster artwork into Word and losing vector quality.

## Requirements

- Python 3
- [PyMuPDF](https://pymupdf.readthedocs.io/) (`pymupdf`)

```bash
pip install pymupdf
```

## Usage

```bash
python pdfigswap.py manuscript.pdf
```

### Layout

Put the manuscript and figure PDFs in the **same directory** as the input file, for example:

- `manuscript.pdf`
- `fig1.pdf`, `fig2.pdf`, `fig6.pdf`, …

Placeholders in the PDF must match (case-insensitive):

`Insert Figure <n> here`

—for example `Insert Figure 6 here` uses `fig6.pdf`.

### Output

The script writes `<stem>_fig_replaced_<YYYYMMDD_HHMMSS>.pdf` next to the input (e.g. `manuscript_fig_replaced_20260504_161052.pdf`). The timestamp is the run time, inserted immediately before the `.pdf` extension.

### Behavior

1. Detect placeholder text and its bounding box.
2. Prefer a drawing rectangle that encloses the text (Word-style shape); otherwise expand the text box slightly.
3. Draw a white rectangle to hide the placeholder box and text.
4. Overlay page 1 of `fig<n>.pdf` in that rectangle (`keep_proportion=True`).

Missing `fig<n>.pdf` files are skipped with a warning.

## License

Add your preferred license when you publish the repository.
