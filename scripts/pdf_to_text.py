"""
PDF-to-Text converter for the SRS-to-TestCases skill.

Kiro cannot handle large PDFs dragged directly into chat — the API rejects
the request because the inlined page content (images) creates a JSON body
that's too large to deserialize (2M+ characters).

This script extracts the text from a PDF and saves it as a .txt file.
You then reference the .txt file with #File in chat instead of dragging the PDF.

Usage:
    python scripts/pdf_to_text.py <path_to_pdf>

Example:
    python scripts/pdf_to_text.py "C:/Users/MySRS.pdf"
    -> creates C:/Users/MySRS.txt

Requirements:
    pip install pymupdf
"""

import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF is not installed. Install it with:  pip install pymupdf")
    sys.exit(1)


def convert_pdf_to_text(pdf_path):
    """Extract all text from a PDF and return it as a single string."""
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    print(f"Reading PDF: {pdf_path} ({page_count} pages)")

    text_parts = []
    for i, page in enumerate(doc, 1):
        page_text = page.get_text()
        text_parts.append(f"--- Page {i} ---\n{page_text}")
        if i % 10 == 0:
            print(f"  ...processed {i}/{page_count} pages")

    doc.close()
    full_text = "\n\n".join(text_parts)
    print(f"  Done. Extracted {len(full_text):,} characters from {page_count} pages.")
    return full_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/pdf_to_text.py <path_to_pdf>")
        print("Example: python scripts/pdf_to_text.py \"C:/Users/MySRS.pdf\"")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if not pdf_path.lower().endswith(".pdf"):
        print(f"Error: Not a PDF file: {pdf_path}")
        sys.exit(1)

    text = convert_pdf_to_text(pdf_path)

    # Output path: same name as PDF but with .txt extension
    txt_path = os.path.splitext(pdf_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nText saved to: {txt_path}")
    print(f"File size: {os.path.getsize(txt_path):,} bytes")
    print(f"\nNext step: In Kiro chat, type  #{os.path.basename(txt_path)}")
    print("Then ask: 'Generate test cases from this SRS'")


if __name__ == "__main__":
    main()
