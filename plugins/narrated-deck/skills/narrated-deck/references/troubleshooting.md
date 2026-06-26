# Troubleshooting

Symptoms → fixes, ordered by frequency of occurrence in real projects.

## Audio plays but subtitles don't appear

**Cause:** `subs.json` was edited after `index.html` was built; the inline SUBS in HTML is stale.

**Fix:** `python3 scripts/sync_subs.py index.html A1.subs.json`

Or rebuild from scratch: `python3 scripts/build_html.py ...`

---

## Audio missing for one segment

Browser console shows `audio error for 023`.

**Cause:** `audio/PROJ-023.mp3` doesn't exist on disk.

**Fix:**
```bash
# regenerate just that one
VOAI_API_KEY=xxx python3 scripts/tts_voai.py A1.subs.json --only 023
```

The player has a graceful fallback (silent timer based on estimated duration), but the viewer will see "部分配音檔尚未產生" — fix before shipping.

---

## TTS gives wrong pronunciation (e.g. "一疊" → "一爹")

Pure Voai limitation; the speaker model doesn't know all idioms.

**Fix:**
1. Edit the sub text to use a more common synonym ("一疊" → "一堆")
2. Regenerate: `--only NNN --force`

For systemic mispronunciation across a project, consider switching to a different `--speaker`.

---

## Voai returns HTTP 200 but the mp3 is tiny (< 200 bytes)

**Cause:** Voai returned a JSON error body in a 200 response (their API quirk).

**Fix:** The `tts_voai.py` script catches this and raises. If it still slips through, delete the tiny file and rerun:
```bash
find audio -name "*.mp3" -size -1k -delete
VOAI_API_KEY=xxx python3 scripts/tts_voai.py A1.subs.json
```

---

## Voai error "Version not found" or "Speaker not found"

**Cause:** `Neo` and `Sota` must be exactly capitalized; speaker names must match Voai's catalog exactly.

**Fix:** Check `references/voai_api.md` for verified names. Use exact strings.

---

## All audio loads slowly (multi-second delays between subs)

**Cause:** mp3s are large (high bitrate) and / or remote host has high latency.

**Fix:**
1. Verify mp3s are < 100KB each on average for typical sub length. Voai returns ~64kbps mp3 by default — should be ~10-30KB per 5-sec clip.
2. The player has a preloader for the next sub. Should be seamless if the static host is reasonable.
3. If hosted, check CDN cache headers (`Cache-Control: public, max-age=86400`).

---

## Subtitle text overlaps with footer controls

**Cause:** Subtitle bar's `bottom: 88px` puts it just above the 64px control bar with some gap. If you've customized the layout, this can break.

**Fix:** Adjust `.subtitle-bar { bottom: ... }` in the theme CSS.

---

## Build script fails with `KeyError: 'scenes'`

**Cause:** `scenes.json` is malformed — likely missing the top-level `"scenes": [...]` array.

**Fix:** Ensure structure is:
```json
{ "scenes": [ { "id": "s01", "type": "title", "props": {...} }, ... ] }
```

---

## Browser shows broken Chinese characters

**Cause:** HTML saved with wrong encoding, or font fallback chain missing CJK fonts.

**Fix:**
- `build_html.py` writes UTF-8 by default. Verify with `file index.html` → should say "UTF-8 Unicode text".
- The base template includes `<meta charset="utf-8">` — verify it's there.
- Check the `--display-font` chain in the theme; on Windows make sure "Microsoft JhengHei" is first.

---

## Audio plays but volume is too low

**Cause:** Voai's default output is normalized to about -16 LUFS. Some browsers / speakers underplay it.

**Fix:** Post-process with ffmpeg:
```bash
for f in audio/*.mp3; do
  ffmpeg -i "$f" -af "loudnorm=I=-14:LRA=11:TP=-2" "$f.tmp.mp3" && mv "$f.tmp.mp3" "$f"
done
```

---

## "Voai.ai rate limit exceeded"

**Cause:** Burst of API calls beyond Voai's per-minute quota.

**Fix:** The script has `--sleep 0.3` by default. If still hitting limits, increase: `--sleep 1.0`.

For large batches (200+ subs), run during off-hours.

---

## Cloud Run 403 Forbidden serving the HTML

(Same lesson as the Kaohsiung deploy.)

**Cause:** OneDrive sync or other tools set files to mode 600. nginx runs as a non-root user and can't read.

**Fix:** In Dockerfile, after `COPY`:
```dockerfile
RUN find /usr/share/nginx/html/ -type d -exec chmod 755 {} \; && \
    find /usr/share/nginx/html/ -type f -exec chmod 644 {} \;
```

---

## Player works locally but breaks when hosted

**Common causes:**
1. **Audio not uploaded** — verify `audio/` folder was included in the upload
2. **CORS** — if audio is on a different domain, set CORS headers
3. **Case sensitivity** — Linux is case-sensitive. `PROJ-001.mp3` ≠ `proj-001.mp3`. Match the `prefix` in subs.json exactly.

---

## I want to swap audio engines mid-project

Voai → ElevenLabs or vice versa: just rerun the other script. Existing mp3s are skipped, so use `--force` to overwrite all:

```bash
ELEVENLABS_API_KEY=xxx python3 scripts/tts_elevenlabs.py A1.subs.json --force
```

The HTML player doesn't care which engine produced the mp3s.

---

## Where do I file new issues?

This is an internal IQT plugin. Slack `@matt` or update this file with the symptom and the fix once you find it.
