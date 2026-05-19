# putfig2pdf.py
# pip install pymupdf

import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF

# A leading "#" in the manuscript PDF is required; it is stripped when resolving
# the file on disk (e.g. "#fig1.pdf" in the PDF -> fig1.pdf next to the input).
# Text that looks like a filename but has no leading "#" is not replaced.
PLACEHOLDER_RE = re.compile(
    r"^#([A-Za-z0-9._-]+(?:\.pdf)?)$",
    re.IGNORECASE,
)


def find_enclosing_rect(page, text_rect, margin=4):
    """Find a rectangle that looks like a Word shape box around the text.

    If none is found, expand the text bounding box slightly.
    """
    candidates = []

    for d in page.get_drawings():
        r = d.get("rect")
        if not r:
            continue
        r = fitz.Rect(r)

        if (
            r.x0 <= text_rect.x0 + margin
            and r.y0 <= text_rect.y0 + margin
            and r.x1 >= text_rect.x1 - margin
            and r.y1 >= text_rect.y1 - margin
        ):
            area = r.get_area()
            if area > text_rect.get_area():
                candidates.append((area, r))

    if candidates:
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]

    # Fallback when no enclosing box is detected
    return text_rect + (-20, -20, 20, 20)


def replace_placeholders(input_pdf):
    input_pdf = Path(input_pdf).resolve()
    base_dir = input_pdf.parent
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = input_pdf.with_name(
        f"{input_pdf.stem}_fig_replaced_{ts}.pdf"
    )

    doc = fitz.open(input_pdf)

    for page in doc:
        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if block.get("type") != 0:
                continue

            block_text = ""
            rect = None

            for line in block["lines"]:
                for span in line["spans"]:
                    block_text += span["text"]
                    span_rect = fitz.Rect(span["bbox"])
                    rect = span_rect if rect is None else rect | span_rect

            text = unicodedata.normalize("NFKC", block_text.strip())
            m = PLACEHOLDER_RE.match(text)
            if not m or rect is None:
                continue

            fig_name = m.group(1)
            if not fig_name.lower().endswith(".pdf"):
                fig_name = f"{fig_name}.pdf"
            fig_pdf = base_dir / fig_name

            if not fig_pdf.exists():
                print(f"WARNING: {fig_pdf.name} not found; skipping.")
                continue

            target_rect = find_enclosing_rect(page, rect)

            # Remove the original placeholder box/text from the PDF.
            page.add_redact_annot(target_rect, fill=(1, 1, 1))
            page.apply_redactions()

            # Place the first page of the figure PDF at the same position
            fig_doc = fitz.open(fig_pdf)
            page.show_pdf_page(
                target_rect,
                fig_doc,
                0,
                keep_proportion=True,
                overlay=True,
            )
            fig_doc.close()

            placeholder = text
            print(f"page {page.number + 1}: {placeholder} -> {fig_pdf.name}")

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()

    print(f"Output: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python putfig2pdf.py manuscript.pdf")
        sys.exit(1)

    replace_placeholders(sys.argv[1])
