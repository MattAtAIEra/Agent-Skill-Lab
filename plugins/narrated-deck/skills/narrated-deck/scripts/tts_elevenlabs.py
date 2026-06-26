#!/usr/bin/env python3
"""tts_elevenlabs.py — ElevenLabs TTS batch generator for a subs.json file.

Use as multilingual fallback or when Voai.ai is unavailable. ElevenLabs has
better English pronunciation but less reliable Mandarin (often gets idioms
wrong — e.g. "一疊" misread as "一爹" in the Kaohsiung pilot).

Usage:
  ELEVENLABS_API_KEY=sk_xxx \\
  python3 tts_elevenlabs.py A1.subs.json --out audio/ \\
    --voice-id r6qgCCGI7RWKXCagm158 \\
    --model eleven_multilingual_v2

Docs: https://elevenlabs.io/docs/api-reference/text-to-speech
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

DEFAULT_VOICE_ID = "r6qgCCGI7RWKXCagm158"  # used in Kaohsiung pilot — replace with your own
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.55,
    "similarity_boost": 0.8,
    "style": 0.0,
    "use_speaker_boost": True,
}


def tts_call(api_key, text, voice_id, model, out_path, timeout=60):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    body = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": DEFAULT_VOICE_SETTINGS,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "accept": "audio/mpeg",
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

    if len(data) < 200 and data[:1] == b"{":
        raise RuntimeError(f"Got JSON error: {data.decode('utf-8', errors='replace')[:200]}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return len(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subs_json")
    ap.add_argument("--out", default="audio")
    ap.add_argument("--voice-id", default=DEFAULT_VOICE_ID)
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="eleven_multilingual_v2 / eleven_v3 / eleven_turbo_v2_5")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=float, default=0.3)
    args = ap.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: set ELEVENLABS_API_KEY env var", file=sys.stderr)
        sys.exit(2)

    data = json.loads(Path(args.subs_json).read_text(encoding="utf-8"))
    prefix = data["prefix"]
    subs = data["subs"]
    out_dir = Path(args.out)

    work = [s for s in subs if s.get("text", "").strip()]
    if args.only:
        work = [s for s in work if s["id"] == args.only]

    total_chars = sum(len(s["text"]) for s in work)
    print(f"▸ {prefix}: {len(work)} segments, {total_chars} chars total")
    print(f"  Engine: ElevenLabs  voice={args.voice_id}  model={args.model}")
    print(f"  Out:    {out_dir.absolute()}")
    print()

    done, skipped, failed, total_bytes = 0, 0, [], 0
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
                n = tts_call(api_key, text, args.voice_id, args.model, path)
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
    print(f"  Generated: {done}  Skipped: {skipped}  Failed: {len(failed)}")
    print(f"  Total size: {total_bytes/1024/1024:.2f} MB")
    if failed:
        for sid, err in failed:
            print(f"  - {sid}: {err[:120]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
