#!/usr/bin/env python3
"""
Remove the NotebookLM watermark / logo that appears in the bottom-right
corner of every page of a PDF exported from Google NotebookLM.

Strategy:
    1. Render each page with pypdfium2 so we can inspect it as pixels.
    2. In the bottom-right search region, find the bounding box of the
       dark pixels that make up the "NotebookLM" text + icon.
    3. Sanity-check the detected box: if it is implausibly large (i.e.
       we hit real page content, not the watermark) fall back to a
       reasonable default rectangle sized relative to the page.
    4. Sample the page background color from a clean band just to the
       left of the watermark.
    5. Use PyMuPDF (fitz) to draw a filled rectangle of that color over
       the watermark. The rest of the page keeps its original vector
       quality — we only paint a small patch.

The script can be used as a library (``clean_pdf(...)``) or as a CLI.

Requires:
    pip install pymupdf pypdfium2 pillow
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import fitz  # PyMuPDF
import pypdfium2 as pdfium
from PIL import Image


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

# Fraction of the page used when searching for the watermark.
# NotebookLM places the logo in the bottom-right corner, so we look in
# a conservative slice of that region.
SEARCH_WIDTH_FRAC = 0.22   # last 22% of the page width
SEARCH_HEIGHT_FRAC = 0.08  # bottom 8% of the page height

# A pixel is considered part of the logo if all three channels are below
# this value. NotebookLM's logo is near-black on a light background, so
# this threshold is safe.
DARK_PIXEL_THRESHOLD = 110

# If the detected bounding box is wider/taller than these fractions of
# the page, we assume we hit real page content rather than the logo and
# fall back to the default rectangle.
MAX_LOGO_WIDTH_FRAC = 0.18
MAX_LOGO_HEIGHT_FRAC = 0.05

# Default watermark rectangle (used when detection fails), expressed as
# fractions of the page dimensions. Covers the bottom-right corner where
# the NotebookLM logo sits.
DEFAULT_BOX_FRAC = (0.86, 0.955, 1.0, 0.995)  # (x1, y1, x2, y2)

# Padding added around the detected bounding box, in PDF points.
PAD_X = 6
PAD_Y = 6


@dataclass
class Rect:
    """Rectangle in PDF-point coordinates, top-left origin."""
    x1: float
    y1: float
    x2: float
    y2: float

    def clamped(self, width: float, height: float) -> "Rect":
        return Rect(
            max(0.0, self.x1),
            max(0.0, self.y1),
            min(width, self.x2),
            min(height, self.y2),
        )


def _detect_logo_bbox(img: Image.Image) -> Optional[Rect]:
    """Find the bounding box of dark pixels in the bottom-right search region.

    Returns ``None`` if no dark pixels are found (page has no watermark),
    or if the detected box is too large to plausibly be a logo.
    """
    w, h = img.size
    search_w = int(w * SEARCH_WIDTH_FRAC)
    search_h = int(h * SEARCH_HEIGHT_FRAC)
    region = img.crop((w - search_w, h - search_h, w, h)).convert("RGB")
    pixels = region.load()
    rw, rh = region.size

    min_x, max_x = rw, 0
    min_y, max_y = rh, 0
    found = False
    for y in range(rh):
        for x in range(rw):
            r, g, b = pixels[x, y]
            if r < DARK_PIXEL_THRESHOLD and g < DARK_PIXEL_THRESHOLD and b < DARK_PIXEL_THRESHOLD:
                found = True
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y

    if not found:
        return None

    # Convert to full-image coordinates (same as PDF points because we
    # rendered at scale=1).
    abs_x1 = (w - search_w) + min_x
    abs_y1 = (h - search_h) + min_y
    abs_x2 = (w - search_w) + max_x
    abs_y2 = (h - search_h) + max_y

    # Sanity check: is the box plausibly a watermark?
    box_w = abs_x2 - abs_x1
    box_h = abs_y2 - abs_y1
    if box_w > w * MAX_LOGO_WIDTH_FRAC or box_h > h * MAX_LOGO_HEIGHT_FRAC:
        return None

    return Rect(abs_x1, abs_y1, abs_x2, abs_y2)


def _default_bbox(width: float, height: float) -> Rect:
    x1f, y1f, x2f, y2f = DEFAULT_BOX_FRAC
    return Rect(width * x1f, height * y1f, width * x2f, height * y2f)


# ---------------------------------------------------------------------------
# Background sampling
# ---------------------------------------------------------------------------

def _sample_background(img: Image.Image, logo: Rect) -> Tuple[float, float, float]:
    """Sample the background color just to the left of the logo.

    We average a handful of pixels to smooth over texture noise. Returns
    an RGB triple in the 0..1 range (the shape fitz expects).
    """
    w, h = img.size
    img = img.convert("RGB")
    # A small band just left of the logo, at the logo's vertical center.
    cy = (logo.y1 + logo.y2) / 2
    sample_xs = [
        max(0, int(logo.x1) - 20),
        max(0, int(logo.x1) - 40),
        max(0, int(logo.x1) - 60),
        max(0, int(logo.x1) - 80),
    ]
    sample_ys = [
        int(max(0, cy - 3)),
        int(min(h - 1, cy)),
        int(min(h - 1, cy + 3)),
    ]

    samples = []
    for sx in sample_xs:
        for sy in sample_ys:
            if 0 <= sx < w and 0 <= sy < h:
                samples.append(img.getpixel((sx, sy)))

    if not samples:
        # Extreme fallback — pale gray that usually matches NotebookLM's default.
        return (0.91, 0.92, 0.93)

    n = len(samples)
    avg = tuple(sum(s[c] for s in samples) / n / 255.0 for c in range(3))
    return avg


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def clean_pdf(
    input_path: str | Path,
    output_path: str | Path,
    verbose: bool = False,
) -> dict:
    """Remove the NotebookLM watermark from every page of a PDF.

    Returns a dict with per-page info for debugging / logging.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")

    # Open once for rendering (pypdfium2) and once for editing (fitz). They
    # are independent libraries with independent handles; this is normal.
    renderer = pdfium.PdfDocument(str(input_path))
    doc = fitz.open(str(input_path))

    if len(renderer) != len(doc):
        # Very unlikely, but guard anyway.
        renderer.close()
        doc.close()
        raise RuntimeError("Page count mismatch between renderers.")

    report = {"pages": [], "input": str(input_path), "output": str(output_path)}

    try:
        for i, page in enumerate(doc):
            pw, ph = page.rect.width, page.rect.height
            img = renderer[i].render(scale=1).to_pil()

            logo = _detect_logo_bbox(img)
            source = "detected"
            if logo is None:
                logo = _default_bbox(pw, ph)
                source = "default"

            bg = _sample_background(img, logo)

            # Add padding and clamp to page bounds.
            patch = Rect(
                logo.x1 - PAD_X,
                logo.y1 - PAD_Y,
                logo.x2 + PAD_X,
                logo.y2 + PAD_Y,
            ).clamped(pw, ph)

            page.draw_rect(
                fitz.Rect(patch.x1, patch.y1, patch.x2, patch.y2),
                color=bg,
                fill=bg,
                width=0,
                overlay=True,
            )

            page_info = {
                "page": i + 1,
                "source": source,
                "logo_bbox": [logo.x1, logo.y1, logo.x2, logo.y2],
                "patch_bbox": [patch.x1, patch.y1, patch.x2, patch.y2],
                "background_rgb": bg,
            }
            report["pages"].append(page_info)
            if verbose:
                print(
                    f"[page {i+1:>3}] {source:<8} "
                    f"box=({logo.x1:.1f},{logo.y1:.1f})-({logo.x2:.1f},{logo.y2:.1f}) "
                    f"bg=rgb({bg[0]:.2f},{bg[1]:.2f},{bg[2]:.2f})"
                )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output_path))
    finally:
        doc.close()
        renderer.close()

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="remove_watermark",
        description="Remove the NotebookLM watermark from a PDF.",
    )
    p.add_argument("input", help="Input PDF path")
    p.add_argument(
        "-o", "--output",
        help="Output PDF path (default: <input>_cleaned.pdf)",
    )
    p.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print per-page detection details.",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_cli().parse_args(argv)
    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else in_path.with_name(in_path.stem + "_cleaned.pdf")

    report = clean_pdf(in_path, out_path, verbose=args.verbose)
    n = len(report["pages"])
    detected = sum(1 for p in report["pages"] if p["source"] == "detected")
    print(f"Cleaned {n} pages ({detected} auto-detected, {n - detected} default box).")
    print(f"Output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
