# putfig2pdf demo

**English** | [日本語](README.ja.md)

This folder contains a minimal end-to-end example for [putfig2pdf](../README.md): a manuscript PDF with `#figN.pdf` placeholders and separate figure PDFs to embed.

## Quick start

From the repository root (with [PyMuPDF](https://pymupdf.readthedocs.io/) installed):

```bash
cd demo
python ../putfig2pdf.py sample.pdf
```

The script looks for `fig1.pdf`, `fig2.pdf`, and `fig3.pdf` in the **same directory** as `sample.pdf` (this folder). It writes a timestamped file such as `sample_fig_replaced_YYYYMMDD_HHMMSS.pdf`.

An example output is already included: `sample_fig_replaced_20260519_130734.pdf`.

## Files

| File | Role |
|------|------|
| `sample.docx` | **Recommended workflow.** Word manuscript with three shape boxes labeled `#fig1.pdf`, `#fig2.pdf`, and `#fig3.pdf` only (no embedded figure images). |
| `sample.pdf` | PDF exported from `sample.docx` (e.g. via PrimoPDF). Use this as input to `putfig2pdf.py`. |
| `fig1.pdf`, `fig2.pdf`, `fig3.pdf` | Figure PDFs referenced by the placeholders. Page 1 of each file is overlaid at the matching box. |
| `figs.pptx` | PowerPoint source used to create `fig1.pdf`–`fig3.pdf`. |
| `sample_fig1.pdf`, `sample_fig2.pdf`, `sample_fig3.pdf` | Copies of the three figure PDFs (same content as `fig1.pdf`–`fig3.pdf`) kept in the demo folder for convenience. |
| `sample_fig_replaced_20260519_130734.pdf` | Example result of running `putfig2pdf` on `sample.pdf`. |
| `sample_broken.docx` | **Contrast / anti-pattern.** Word file where the three figures are embedded as vector images (EMF) inside the document instead of filename-only placeholders. |
| `sample_broken.pdf` | PDF exported from `sample_broken.docx`. Illustrates problems you get when figures are baked into Word before PDF export (large file, not suitable for automated swap). |

## What to compare

1. Open `sample.pdf` and note the three boxes showing `#fig1.pdf`, `#fig2.pdf`, `#fig3.pdf`.
2. Run `putfig2pdf` on `sample.pdf` and open the output PDF: placeholders are removed and replaced with the vector figures.
3. Open `sample_broken.pdf`: figures are already inside the page; `putfig2pdf` is not meant for this layout.

## Ligatures (`fi` → `ﬁ`)

Some PDF exporters turn `fig` into a ligature so the text stream reads `#ﬁg1.pdf` instead of `#fig1.pdf`. The current `putfig2pdf.py` normalizes text with Unicode NFKC before matching, so placeholders like `#fig1.pdf` still match when the PDF uses `ﬁ` (U+FB01).

If matching fails on your own PDF, export again with ligatures disabled if possible, or confirm the placeholder is plain `#filename` text in a shape box (as in `sample.docx`), not an embedded picture.

## Recreating the example output

```bash
cd demo
python ../putfig2pdf.py sample.pdf
```

Output name pattern: `sample_fig_replaced_<YYYYMMDD_HHMMSS>.pdf`.

[← Back to main README](../README.md)
