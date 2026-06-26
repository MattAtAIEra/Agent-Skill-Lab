#!/usr/bin/env python3
"""sync_subs.py — sync the inline SUBS array in a built index.html with the latest subs.json.

Use when you edit subs.json after building. Updates the inline `const SUBS = [...]`
literal in-place. The TTS scripts read subs.json directly; this keeps the player
HTML aligned.

Usage:
  python3 sync_subs.py index.html A1.subs.json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html_path")
    ap.add_argument("subs_json")
    args = ap.parse_args()

    html = Path(args.html_path).read_text(encoding="utf-8")
    data = json.loads(Path(args.subs_json).read_text(encoding="utf-8"))
    new_subs_json = json.dumps(data["subs"], ensure_ascii=False, indent=2)

    pat = re.compile(r"const SUBS = \[[\s\S]*?\];", re.MULTILINE)
    m = pat.search(html)
    if not m:
        print(f"ERROR: could not find `const SUBS = [...]` in {args.html_path}", file=sys.stderr)
        sys.exit(2)

    new_html = html[:m.start()] + f"const SUBS = {new_subs_json};" + html[m.end():]
    Path(args.html_path).write_text(new_html, encoding="utf-8")
    print(f"✓ Synced {args.html_path} ({len(data['subs'])} subs)")


if __name__ == "__main__":
    main()
