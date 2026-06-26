#!/usr/bin/env python3
"""tts_voai.py — Voai.ai TTS batch generator for a subs.json file.

Reads {prefix}.subs.json, calls Voai.ai TTS for each non-empty subtitle, writes
audio/{prefix}-{id}.mp3. Resumable (skips existing files). Battle-tested on the
Kaohsiung City Health Bureau training project (~110 mp3s, 0 retake).

Usage:
  VOAI_API_KEY=iq-xxx \\
  python3 tts_voai.py A1.subs.json --out audio/ [--only 015] [--force]

Voai docs: https://www.voai.ai/api

Recommended defaults:
  --version Neo       # newest model (use "Sota" for legacy)
  --speaker 佑希       # warm female voice; great for zh-TW training material
  --style 聊天         # conversational; alternatives: 客服 / 旁白 / 故事 / 廣告
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

VOAI_URL = "https://connect.voai.ai/TTS/Speech"

DEFAULT_VERSION = "Neo"
DEFAULT_SPEAKER = "佑希"
DEFAULT_STYLE = "聊天"
DEFAULT_PARAMS = {
    "speed": 1,
    "pitch_shift": 0,
    "style_weight": 0.5,
    "breath_pause": 0,
}
OUTPUT_FORMAT = "mp3"


def tts_call(api_key, text, out_path, version, speaker, style, timeout=60):
    body = json.dumps({
        "version": version,
        "text": text,
        "speaker": speaker,
        "style": style,
        **DEFAULT_PARAMS,
    }).encode("utf-8")
    req = urllib.request.Request(
        VOAI_URL,
        data=body,
        headers={
            "x-api-key": api_key,
            "x-output-format": OUTPUT_FORMAT,
            "Content-Type": "application/json",
            "accept": "*/*",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body_text[:300]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e

    # Voai sometimes returns JSON error with HTTP 200
    if len(data) < 200 and data[:1] == b"{":
        raise RuntimeError(f"Got JSON error: {data.decode('utf-8', errors='replace')[:200]}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return len(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subs_json", help="Path to {prefix}.subs.json")
    ap.add_argument("--out", default="audio", help="Output directory (default: audio/)")
    ap.add_argument("--only", help="Only regenerate this id (e.g. '015')")
    ap.add_argument("--force", action="store_true", help="Regenerate even if file exists")
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=float, default=0.3, help="Sleep between requests")
    ap.add_argument("--version", default=DEFAULT_VERSION, help="Voai model version (Neo / Sota)")
    ap.add_argument("--speaker", default=DEFAULT_SPEAKER, help="Speaker name (Chinese)")
    ap.add_argument("--style", default=DEFAULT_STYLE, help="Style (聊天 / 客服 / 旁白 / 故事 / 廣告)")
    args = ap.parse_args()

    api_key = os.environ.get("VOAI_API_KEY")
    if not api_key:
        print("ERROR: set VOAI_API_KEY env var", file=sys.stderr)
        sys.exit(2)

    data = json.loads(Path(args.subs_json).read_text(encoding="utf-8"))
    prefix = data["prefix"]
    subs = data["subs"]
    out_dir = Path(args.out)

    work = [s for s in subs if s.get("text", "").strip()]
    if args.only:
        work = [s for s in work if s["id"] == args.only]
        if not work:
            print(f"ERROR: id {args.only} not found or has empty text", file=sys.stderr)
            sys.exit(2)

    total_chars = sum(len(s["text"]) for s in work)
    print(f"▸ {prefix}: {len(work)} segments, {total_chars} chars total")
    print(f"  Engine: Voai.ai  ver={args.version}  spk={args.speaker}  style={args.style}")
    print(f"  Out:    {out_dir.absolute()}")
    print()

    done = 0
    skipped = 0
    failed = []
    total_bytes = 0
    started = time.time()

    for s in work:
        path = out_dir / f"{prefix}-{s['id']}.mp3"
        if path.exists() and not args.force:
            skipped += 1
            continue

        text = s["text"]
        line = f"[{s['id']}] {text[:38]}{'…' if len(text)>38 else ''}"
        print(f"  {line:<58}", end="", flush=True)

        for attempt in range(args.retries):
            try:
                n = tts_call(api_key, text, path, args.version, args.speaker, args.style)
                total_bytes += n
                done += 1
                print(f" ✓ {n//1024} KB")
                break
            except Exception as e:
                if attempt < args.retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                print(f" ✗ {e}")
                failed.append((s["id"], str(e)))
        time.sleep(args.sleep)

    elapsed = time.time() - started
    print()
    print(f"━━━ Done in {elapsed:.1f}s ━━━")
    print(f"  Generated: {done}")
    print(f"  Skipped (exists): {skipped}")
    print(f"  Failed: {len(failed)}")
    print(f"  Total size: {total_bytes/1024/1024:.2f} MB")
    if failed:
        print()
        print("Failed segments:")
        for sid, err in failed:
            print(f"  - {sid}: {err[:120]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
