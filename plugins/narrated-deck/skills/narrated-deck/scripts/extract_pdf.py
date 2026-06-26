#!/usr/bin/env python3
"""extract_pdf.py — extract text from a PDF into a structured outline.

Tries text extraction first (works for text-based PDFs). For scanned/image PDFs,
falls back to a warning suggesting Tesseract OCR.

Outputs a JSON document:
  {
    "source": "deck.pdf",
    "page_count": N,
    "pages": [
      {
        "idx": 1,
        "text": "...",
        "title_guess": "First non-trivial line, used as scene title",
        "image_paths": ["extracted-images/page-1-img-0.png", ...]
      }
    ]
  }

Dependencies:
  pip install pdfplumber Pillow
"""

import argparse
import json
import re
import sys
from pathlib import Path


def guess_title(text):
    """Pick the first short non-empty line as a likely title."""
    if not text:
        return ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) <= 80 and not re.match(r"^\d+\s*$", line):
            return line
    return text[:60].strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf_path")
    ap.add_argument("--out", default="outline.json")
    ap.add_argument("--images-dir", default="extracted-images")
    ap.add_argument("--skip-images", action="store_true")
    args = ap.parse_args()

    try:
        import pdfplumber
    except ImportError:
        print("ERROR: need pdfplumber. Install with: pip install pdfplumber", file=sys.stderr)
        sys.exit(2)

    src = Path(args.pdf_path)
    if not src.exists():
        print(f"ERROR: file not found: {src}", file=sys.stderr)
        sys.exit(2)

    img_dir = Path(args.images_dir)
    if not args.skip_images:
        img_dir.mkdir(parents=True, exist_ok=True)

    pages_out = []
    empty_pages = 0

    with pdfplumber.open(str(src)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text() or "").strip()
            if not text:
                empty_pages += 1

            image_paths = []
            if not args.skip_images:
                for j, img in enumerate(page.images):
                    try:
                        x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                        bbox = (x0, top, x1, bottom)
                        cropped = page.crop(bbox).to_image(resolution=150)
                        fname = img_dir / f"page-{i:03d}-img-{j}.png"
                        cropped.save(str(fname), format="PNG")
                        image_paths.append(str(fname))
                    except Exception as e:
                        print(f"  warn: image extract failed page {i} img {j}: {e}", file=sys.stderr)

            pages_out.append({
                "idx": i,
                "text": text,
                "title_guess": guess_title(text),
                "image_paths": image_paths,
            })

    out_path = Path(args.out)
    out_path.write_text(json.dumps({
        "source": str(src),
        "page_count": len(pages_out),
        "pages": pages_out,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ Extracted {len(pages_out)} pages → {out_path}")
    if not args.skip_images:
        n_imgs = sum(len(p["image_paths"]) for p in pages_out)
        print(f"  Images: {n_imgs} → {img_dir}/")
    if empty_pages:
        print(f"  ⚠ {empty_pages} pages had no extractable text — likely scanned.")
        print("    Consider running OCR first:")
        print(f"    ocrmypdf {src} {src.stem}_ocr.pdf  &&  rerun on the _ocr.pdf")


if __name__ == "__main__":
    main()
