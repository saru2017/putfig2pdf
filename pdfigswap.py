# pdfigswap.py
# pip install pymupdf

import re
import sys
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF

PLACEHOLDER_RE = re.compile(r"Insert\s+Figure\s+(\d+)\s+here", re.IGNORECASE)


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

            m = PLACEHOLDER_RE.search(block_text)
            if not m or rect is None:
                continue

            fig_no = m.group(1)
            fig_pdf = base_dir / f"fig{fig_no}.pdf"

            if not fig_pdf.exists():
                print(f"WARNING: {fig_pdf.name} not found; skipping.")
                continue

            target_rect = find_enclosing_rect(page, rect)

            # Cover the original box and text with white
            page.draw_rect(
                target_rect,
                color=(1, 1, 1),
                fill=(1, 1, 1),
                overlay=True,
            )

            # Place the first page of fig#.pdf at the same position
            fig_doc = fitz.open(fig_pdf)
            page.show_pdf_page(
                target_rect,
                fig_doc,
                0,
                keep_proportion=True,
                overlay=True,
            )
            fig_doc.close()

            print(f"page {page.number + 1}: Insert Figure {fig_no} here -> {fig_pdf.name}")

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()

    print(f"Output: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdfigswap.py manuscript.pdf")
        sys.exit(1)

    replace_placeholders(sys.argv[1])
