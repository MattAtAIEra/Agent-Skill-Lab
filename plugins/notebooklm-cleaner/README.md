# notebooklm-cleaner

A Claude Code plugin that removes the **NotebookLM** watermark/logo that Google NotebookLM stamps in the bottom-right corner of every page of its exported PDFs.

## What's inside

```
notebooklm-cleaner/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── notebooklm-watermark-remover/
        ├── SKILL.md
        └── scripts/
            └── remove_watermark.py
```

One skill, one script. The script works both as a CLI and as an importable Python module, so it's useful outside Claude Code too.

## Install

### Claude Code (marketplace-style)

Drop the plugin folder into a Git repo that follows the [Claude Code plugin marketplace format](https://code.claude.com/docs/en/plugins), then:

```bash
/plugin marketplace add <user>/<repo>
/plugin install notebooklm-cleaner@<marketplace-name>
/reload-plugins
```

### Claude Code (local development)

Test without installing by pointing Claude Code at the folder:

```bash
claude --plugin-dir /path/to/notebooklm-cleaner
```

### Direct skill install (Claude.ai / Codex)

Skills in this plugin also work standalone. Copy `skills/notebooklm-watermark-remover/` into `~/.claude/skills/` and Claude will pick it up.

## Use it

Once the plugin is loaded, just ask:

- "Remove the NotebookLM icon from this PDF"
- "去掉右下角的 NotebookLM 浮水印"
- "Clean up this NotebookLM deck"

Claude will invoke the `notebooklm-watermark-remover` skill, which runs the bundled script.

Or run the script directly:

```bash
pip install pymupdf pypdfium2 pillow
python skills/notebooklm-watermark-remover/scripts/remove_watermark.py input.pdf -o cleaned.pdf --verbose
```

## How it works

For each page, the script:

1. Renders the page to a pixel image (pypdfium2).
2. Scans the bottom-right corner for dark pixels — the NotebookLM logo is near-black on a light background.
3. Takes the bounding box of those pixels as the logo region, with a sanity check: if the detected box is implausibly large (real page content extending into the corner), it falls back to a default rectangle sized relative to page dimensions.
4. Samples the background color from a small band just left of the logo.
5. Draws a filled rectangle of that color over the logo with PyMuPDF.

This is a **vector overlay**, not a raster re-render — the rest of the page retains its original text clarity.

## Requirements

- Python 3.9+
- `pymupdf`, `pypdfium2`, `pillow`

## License

MIT.
