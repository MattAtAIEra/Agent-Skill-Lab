---
name: narrated-deck
description: Turn a PPT, PDF, or written outline into a self-contained narrated HTML page — per-subtitle TTS audio, scene-based visual transitions, built-in player. Use when the user wants to make a training video, product walk-through, children's story, conference talk, onboarding explainer, compliance refresher, or any "voice + slides on auto-pilot" deliverable. Triggers include: "make a narrated explainer from this PPT", "turn this PDF into a video", "voice-over my slides", "create a kid's bedtime story page with narration", "automate this product demo", "build a 教育訓練 page from my deck".
---

# narrated-deck — the production pipeline

You are running the **narrated-deck** skill. The user has given you raw source material (PPT, PDF, or written outline) and wants the final deliverable: a self-contained `index.html` + `audio/*.mp3` folder that plays a narrated, scene-based explainer in any browser.

## Phase 0 — prerequisites & intake (do this BEFORE the pipeline)

### 0a. Confirm a TTS API key is available — FIRST, before anything else

Phase 4 spends real money on TTS and **hard-fails without a key**. Before writing a single line of narration, confirm the user has ONE of these and that it's set as the exact env var named:

- **Voai.ai** (default, best for zh-TW) — env var `VOAI_API_KEY`, format `iq-...`. Get one at https://voai.ai (docs: https://www.voai.ai/api).
- **ElevenLabs** (multilingual / English fallback) — env var `ELEVENLABS_API_KEY`, format `sk_...`. Get one at https://elevenlabs.io/app/developers/api-keys.

If the user hasn't supplied a key, **STOP and ask** them to either paste it into the chat or grab one from the links above. Never invent or guess a key. (Full note: `CLAUDE.md` at the plugin root.)

### 0b. Ingest the source, understand it, then reflect it back

When the user pastes text / a PDF / a PPT / any copy file, do **NOT** jump straight to generic questions. First READ it and form a point of view — like a designer doing intake — then confirm with the user the way Claude's design intake works:

1. **Read the material end to end.** For PDF/PPT, run the Phase 1 extractor first; for pasted prose, read it directly.
2. **Reflect back what you understood** in 3–5 bullets: who this seems to be FOR, what it's trying to ACHIEVE, the core messages, and the tone the source already carries. This proves you read it and surfaces wrong assumptions cheaply.
3. **Propose, don't just interrogate.** Use `AskUserQuestion` to lock the brief, but **pre-fill each question's options with YOUR recommendation** (label the best guess "(Recommended)") drawn from what you just read — so the user mostly confirms or tweaks rather than starting from blank. Always leave the "Other" path open for free-text input. Cover these dimensions:
   - **Audience & tone** — your best guess from the content (government inspectors? consumers? children? engineers? B2B buyers?) — determines voice, vocabulary, formality.
   - **Purpose / call-to-action** — train / persuade / onboard / entertain / inform — shapes structure and the closing scene.
   - **Expression approach** — story-driven vs. step-by-step explainer vs. problem→solution pitch — shapes scene patterns and pacing.
   - **Target length** — 3 / 8 / 15 min — determines subtitle count.
   - **Theme** — `government` (serious, official) / `product` (modern, marketing) / `children` (playful, big fonts) / `corporate` (B2B professional) / `custom`.
   - **Output language** — zh-TW / zh-CN / en / ja — affects TTS voice selection.

`AskUserQuestion` takes up to 4 questions per call, so lead with the load-bearing ones — **audience, purpose, expression approach, theme** — and state safe defaults for the rest (e.g. 8 min, zh-TW) for the user to override. **Getting audience/purpose wrong wastes hours of TTS regeneration; this intake is the cheapest place to be right.**

Lock the brief only after the user confirms, then proceed.

## The six-phase pipeline

Run these in strict order. Each phase has its own script and outputs the input to the next phase.

### Phase 1 — EXTRACT (PPT/PDF → outline)

If user gave PPT:
```bash
python3 skills/narrated-deck/scripts/extract_pptx.py path/to/deck.pptx --out outline.json
```

If user gave PDF:
```bash
python3 skills/narrated-deck/scripts/extract_pdf.py path/to/file.pdf --out outline.json
```

If user gave a written outline / brief — skip this phase, you'll synthesize from the prose directly in Phase 2.

The extracted JSON gives you: `{scenes: [{id, title, text, image_paths}]}`. Read it, summarize what's there to the user in plain language, and confirm the scene order before continuing.

### Phase 2 — SCRIPT (outline → narration)

YOU write the narration as Markdown, scene by scene. Read `references/narration_writing.md` BEFORE writing. Key rules baked in there:

- **Conversational**, not bullet-point. TTS reads what you write — punctuation included.
- **No jargon explosions.** Define terms on first use.
- **One thought per sentence.** This becomes the subtitle granularity.
- **Numbers + acronyms** — spell out problematic ones (PDF → `P D F` if Voai mispronounces).

Save to `script.md`. Show the user, ask for revisions. **Cheap to iterate here**; expensive after TTS.

### Phase 3 — SUBS (script → subs.json)

Convert the approved script into the canonical `subs.json` structure:

```json
{
  "prefix": "PROJ",
  "title": "Project title shown in topbar + browser tab",
  "subs": [
    { "id": "001", "scene": "s01", "text": "", "dur": 4 },
    { "id": "002", "scene": "s02", "text": "First spoken line." },
    { "id": "003", "scene": "s02", "text": "Second line — same scene." }
  ]
}
```

Rules:
- `id` is a zero-padded 3-digit string, monotonically increasing.
- `scene` groups subtitles that share a visual frame; advancing to the next scene triggers the slide transition.
- `text: ""` with `dur: N` = silent frame (used for intro/outro/feedback-form scenes).
- Each non-empty `text` becomes ONE mp3 file: `audio/{prefix}-{id}.mp3`.
- Aim for 10–30 Chinese chars / 6–18 English words per subtitle. End at natural breath points (commas, periods, conjunctions).

Save to `{prefix}.subs.json`. Show the user. Confirm. **Last chance before TTS spend.**

### Phase 4 — TTS (subs.json → audio/)

Default to **Voai.ai** (best for traditional Chinese). Fall back to **ElevenLabs** for multilingual or if user prefers.

```bash
# Voai.ai (default)
VOAI_API_KEY=iq-xxx \
  python3 skills/narrated-deck/scripts/tts_voai.py \
    {prefix}.subs.json \
    --out audio/ \
    --version Neo \
    --speaker 佑希 \
    --style 聊天
```

```bash
# ElevenLabs (multilingual fallback)
ELEVENLABS_API_KEY=sk_xxx \
  python3 skills/narrated-deck/scripts/tts_elevenlabs.py \
    {prefix}.subs.json \
    --out audio/ \
    --voice-id r6qgCCGI7RWKXCagm158 \
    --model eleven_multilingual_v2
```

Both scripts are **resumable** — already-generated mp3s are skipped on rerun. Use `--only 015` to regenerate one segment after editing its text. Use `--force` to nuke and regenerate everything.

See `references/voai_api.md` for voice selection guidance.

### Phase 5 — BUILD HTML (subs.json + scenes.json + theme → index.html)

YOU first author `scenes.json` — the visual content for each scene. Read `references/scene_types.md` for the reusable scene patterns (title, painpoint, demo-browser, callout-stack, FAQ-grid, takeaway-row, outro, feedback-form). Choose a pattern per scene; fill in the content.

```json
{
  "scenes": [
    {
      "id": "s01",
      "type": "title",
      "props": {
        "eyebrow": "EDUCATIONAL ‧ MODULE A1",
        "display": "Title <span class='accent'>highlight</span>",
        "tagline": "One-line description",
        "series": "PROJ ‧ Phase 1"
      }
    },
    {
      "id": "s02",
      "type": "painpoint",
      "props": { "title": "...", "left_panel": {...}, "right_panel": {...} }
    }
  ]
}
```

Then build:
```bash
python3 skills/narrated-deck/scripts/build_html.py \
  --subs {prefix}.subs.json \
  --scenes scenes.json \
  --theme government \
  --out index.html
```

The output is a single self-contained HTML file. Subtitles are inlined; mp3s are referenced via relative URLs (`audio/PROJ-001.mp3`).

### Phase 6 — SHIP

Three ship modes — pick based on user need:

**Local:** "Just open the HTML in my browser." Done — `open index.html`.

**Static host:** Copy folder to GCP Cloud Run / Vercel / Cloudflare Pages / S3. The Kaohsiung Health Bureau project's nginx Dockerfile is a good template (single-container, nginx serving static + optional Flask backend for feedback form).

**MP4 export:** Record the browser playing the HTML via OBS Studio or QuickTime. About 12 min → ~300MB at 1080p. Or use Playwright + ffmpeg for headless automation (see `references/mp4_export.md`).

---

## Iterating on a shipped project

When the user comes back later to revise:

- **Wrong wording in subtitle 015** → edit `subs.json` → rerun TTS with `--only 015` → reload browser. ~20 seconds.
- **Add a new scene** → edit `subs.json` + `scenes.json` → rerun TTS (new ids only, others skip) → rebuild HTML. ~2 minutes.
- **Change theme** → rerun build with `--theme product`. ~1 second. **No re-narration needed.** This is the whole point of the decoupled architecture.
- **Translate** → duplicate `subs.json` to `subs.en.json`, translate texts, rerun TTS with English voice, rebuild with the same scenes. The visual layer is language-agnostic.

---

## When NOT to use this skill

- User wants a slide deck for a *live* presentation (use the `pptx` skill).
- User wants a static report or article (use the `docx` skill).
- User wants an interactive web app (this is a player, not an app — use generic React skills).
- User wants an audiobook with no visuals (just the TTS scripts are useful — skip the HTML phase).

---

## Reference docs (read on demand)

| File | When to read |
| --- | --- |
| `references/pipeline.md` | Full pipeline detail — read once when starting |
| `references/narration_writing.md` | Before Phase 2 (script writing) |
| `references/voai_api.md` | Before Phase 4 (TTS) — voice selection guide |
| `references/scene_types.md` | Before Phase 5 (scenes.json) — visual patterns |
| `references/themes.md` | Before Phase 5 — picking or customizing theme |
| `references/mp4_export.md` | When user asks for video export |
| `references/troubleshooting.md` | When something breaks (TTS rate limit, drift, etc.) |

---

## Key principle: content / voice / visuals are decoupled

`subs.json` is the **single source of truth** for narration timing.
`scenes.json` is the **single source of truth** for visuals.
`themes/*.css` is the **single source of truth** for styling.

Any of these three can change without touching the other two. This is the "Java microservice" architecture for explainer videos — and it's what makes this 10x cheaper than traditional video production.
