---
name: notebooklm-watermark-remover
description: Removes the "NotebookLM" watermark/logo that Google NotebookLM stamps in the bottom-right corner of every page of its exported PDFs. Use this whenever the user uploads a NotebookLM-generated PDF (slide decks, briefing docs, study guides, etc.) and asks to remove, erase, hide, clean up, or get rid of the NotebookLM logo, icon, watermark, or attribution — in English or Chinese (去掉 / 移除 / 清掉 / 拿掉 NotebookLM 浮水印 / 圖示 / icon / logo / 標記). Also trigger when the user just says "clean this NotebookLM PDF" without naming the watermark specifically, since that's almost always what they mean.
---

# NotebookLM watermark remover

NotebookLM exports PDFs with a small "NotebookLM" logo stamped in the bottom-right corner of every page. This skill removes that logo while preserving the rest of the page as vector content.

## When to use this skill

Trigger whenever a user hands you a NotebookLM-exported PDF and wants the logo gone. The signal can be explicit ("remove the NotebookLM icon", "去掉右下角的 NotebookLM"), or implicit when they say things like "clean this up" or "可以幫我處理一下這份 PDF 嗎" about a file that visibly came from NotebookLM. If you're unsure whether the file is from NotebookLM, it's fine to just try the script — on PDFs that don't have a watermark, the patch lands on an empty region and does no harm, but you can also check by looking for the logo on page 1 first.

## How it works

The script in `scripts/remove_watermark.py` does the following per page:

1. Renders the page as an image with pypdfium2.
2. Scans the bottom-right corner (last ~22% wide × ~8% tall) for dark pixels — the "NotebookLM" logo is near-black.
3. Takes the bounding box of those pixels as the logo region, with a sanity check: if the detected box is implausibly large (e.g. real page content extends into the search area), it falls back to a default rectangle sized relative to the page dimensions.
4. Samples the page background color from a small band just to the left of the logo, averaging several pixels for stability.
5. Uses PyMuPDF to draw a filled rectangle of that background color over the logo, plus a few points of padding on each side.

This is a vector overlay, not a raster re-render, so the rest of the page keeps its original text clarity and quality.

## How to invoke it

The script is self-contained and works both as a CLI and as an importable module. Prefer the CLI — it's one line.

```bash
python scripts/remove_watermark.py <input.pdf> -o <output.pdf>
```

Add `--verbose` when you want to see per-page detection results (useful when debugging a PDF that looks odd after cleaning):

```bash
python scripts/remove_watermark.py input.pdf -o output.pdf --verbose
```

If the output path is omitted, the script writes to `<input>_cleaned.pdf` alongside the input. On Claude.ai, save the output into `/mnt/user-data/outputs/` so the user can download it, then present the file with the `present_files` tool.

To use it from Python instead:

```python
from scripts.remove_watermark import clean_pdf
clean_pdf("input.pdf", "output.pdf", verbose=True)
```

`clean_pdf()` returns a dict with per-page info (detected vs. default box, sampled background color) that's handy for logging.

## Dependencies

The script needs three Python packages. If they're not already installed, run:

```bash
pip install pymupdf pypdfium2 pillow
```

On the Claude.ai container `pypdfium2` and `pillow` are already present; `pymupdf` usually needs one install (`pip install pymupdf --break-system-packages`).

## Edge cases and tuning

**Dark page content near the corner.** If a page has real content (e.g. a dark table border, a chart, or a dark filled block) that bleeds into the bottom-right corner, the pixel scan may grab that instead of the logo. The script guards against this with size-based sanity checks: if the detected bounding box is wider than ~18% of the page or taller than ~5%, it's discarded and the default rectangle is used. This was validated against mixed NotebookLM decks.

**Non-standard page sizes.** The defaults are expressed as fractions of page dimensions, so landscape slide decks (common from NotebookLM), portrait A4, and US Letter all work without changes.

**Pages where no watermark is present.** If no dark pixels are found in the search region, the script falls back to the default box and paints a tiny patch of matching background onto an empty area — visually a no-op. This means the script is safe to run on already-cleaned PDFs without damage.

**Visible seam on textured backgrounds.** The script samples from the immediate left of the logo, so if the page background has a strong gradient or pattern right where the logo sits, the patch may be slightly visible on close inspection. NotebookLM's default template uses a flat light-gray background where this isn't an issue, but if it comes up, the fix is to increase `PAD_X` / `PAD_Y` in the script or, in extreme cases, render the whole page to image and rebuild.

The tuning constants at the top of `scripts/remove_watermark.py` (`SEARCH_WIDTH_FRAC`, `DARK_PIXEL_THRESHOLD`, `MAX_LOGO_WIDTH_FRAC`, `DEFAULT_BOX_FRAC`, padding) are named and commented so adjustments stay obvious.
