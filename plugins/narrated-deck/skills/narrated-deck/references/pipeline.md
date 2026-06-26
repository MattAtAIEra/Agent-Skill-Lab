# Full pipeline reference

The pipeline has 6 phases. Each is a single command with a single input → single output. If anything breaks, you know exactly which step.

## Phase 1 — EXTRACT

### Input: `deck.pptx` or `doc.pdf`

### Command
```bash
# pptx
python3 scripts/extract_pptx.py deck.pptx --out outline.json

# pdf
python3 scripts/extract_pdf.py doc.pdf --out outline.json
```

### Output: `outline.json`
- `slides` or `pages` array
- For each: title, bullets, speaker notes, image paths

### Validation
- Open outline.json, scan slide titles — does the deck structure make sense?
- If speaker notes exist, you've got 80% of the script already.

### Skip when
- User gave a written brief instead of a deck. Move directly to Phase 2.

---

## Phase 2 — SCRIPT

### Input: `outline.json` + audience/tone brief

### Command
None — this is Claude writing prose. Save to `script.md`.

### Output: `script.md`
- Markdown document, scene-by-scene
- Each scene heading = a `## s01` style header
- Below each header: prose paragraphs that will become subtitles

### Validation
- Read aloud once. Catches 90% of awkward phrasing.
- Show to user. Get changes BEFORE TTS.

### Common mistakes
- Bullet-point voice (read like a list)
- Inconsistent person (你/您 mixed)
- Untested acronyms or numbers

See `narration_writing.md` for the full rules.

---

## Phase 3 — SUBS

### Input: `script.md` + project prefix (e.g. "A1", "ORDER-DEMO", "BEDTIME")

### Command
None — this is Claude splitting the script into subs. Save to `{prefix}.subs.json`.

### Output: `{prefix}.subs.json`
```json
{
  "prefix": "A1",
  "title": "Module title",
  "subs": [
    { "id": "001", "scene": "s01", "text": "", "dur": 4 },
    { "id": "002", "scene": "s02", "text": "First spoken line." }
  ]
}
```

### Conventions
- `id` = zero-padded 3-digit, monotonically increasing
- `scene` = scene id; subs sharing a scene play in the same visual frame
- Empty `text` + `dur` = silent gap (useful for intro/outro/feedback)
- Non-empty `text` = will get TTS-ed to `audio/{prefix}-{id}.mp3`

### Validation
```bash
# count subs per scene
jq '.subs | group_by(.scene) | map({scene: .[0].scene, count: length})' A1.subs.json
```

---

## Phase 4 — TTS

### Input: `{prefix}.subs.json` + TTS API key

### Command
```bash
# Voai (default for zh-TW)
VOAI_API_KEY=iq-xxx \
  python3 scripts/tts_voai.py A1.subs.json --out audio/

# ElevenLabs (multilingual/English)
ELEVENLABS_API_KEY=sk_xxx \
  python3 scripts/tts_elevenlabs.py A1.subs.json --out audio/
```

### Output: `audio/{prefix}-NNN.mp3` (one per non-empty sub)

### Resumability
- Already-existing mp3s are skipped on re-run.
- `--only 015` regenerates just sub 015 (use after editing one line).
- `--force` regenerates everything (last resort — eats API quota).

### Validation
**Listen to every mp3** before moving on. Watch for:
- Mispronounced words → fix the sub text, rerun with `--only`
- Cut-off endings → add a period at sub end
- Robotic pacing → break the sub at a comma, add a follow-up sub

---

## Phase 5 — BUILD HTML

### Input: `{prefix}.subs.json` + `scenes.json` + theme name

### Authoring `scenes.json`
This is the visual layer. For each scene id used in subs.json, define how it looks:

```json
{
  "scenes": [
    {"id": "s01", "type": "title",   "label": "Intro",   "props": {...}},
    {"id": "s02", "type": "painpoint","label": "Problem", "props": {...}},
    {"id": "s03", "type": "cards-3", "label": "Steps",   "props": {...}}
  ]
}
```

See `scene_types.md` for all built-in types and props.

### Command
```bash
python3 scripts/build_html.py \
  --subs A1.subs.json \
  --scenes scenes.json \
  --theme government \
  --out index.html
```

### Output: `index.html` (self-contained — opens directly)

### Themes
`government`, `product`, `children`, `corporate`. See `themes.md`.

### Validation
```bash
open index.html
```
Press play. Watch first 30 seconds. Look for:
- Visuals matching subtitles
- Smooth transitions
- Subtitle font readable
- Audio sync (audio + subtitle text appear simultaneously)

---

## Phase 6 — SHIP

### Modes

**Local viewing**: just `open index.html`. Audio plays from local files via relative URLs.

**Static hosting**:
```bash
# GCS
gsutil -m cp -r index.html audio/ gs://my-bucket/projects/A1/
# Vercel
vercel deploy
# Cloudflare Pages
wrangler pages publish .
# Cloud Run (containerized)
# See examples/cloudrun/ for a nginx Dockerfile that adds a feedback form backend
```

**MP4 export**:
```bash
# OBS Studio — record the browser playing fullscreen
# Or headless via Playwright + ffmpeg:
node scripts/record_mp4.js index.html out.mp4
```

---

## Iteration patterns (post-ship)

### Change one word
1. Edit `subs.json` at the relevant id
2. `tts_voai.py A1.subs.json --only 015 --force`
3. Refresh browser. Done.

### Add a scene
1. Insert new subs in `subs.json` (renumber following ids? NO — use `015a`, `015b` style; player doesn't care)
2. Run TTS (only new subs generate)
3. Add a scene entry in `scenes.json`
4. Rebuild HTML

### Change theme
```bash
python3 scripts/build_html.py --subs A1.subs.json --scenes scenes.json --theme product
```
~1 second. No re-narration.

### Translate
1. Copy `A1.subs.json` to `A1.en.subs.json`
2. Translate texts in-place (keep ids and scenes the same)
3. TTS with English engine
4. Build with `--lang en`
5. Result: parallel English HTML/audio that uses the SAME visual scenes

### Update factual content (e.g. regulation changed)
1. Find affected subs (search subs.json for keyword)
2. Edit text
3. Rerun TTS `--only` for those ids
4. Visual layer untouched — visitors can refresh and see/hear the update without you touching `scenes.json` or theme

This decoupled architecture is the whole point. Compare to traditional video production where any change means re-cutting the entire video.
