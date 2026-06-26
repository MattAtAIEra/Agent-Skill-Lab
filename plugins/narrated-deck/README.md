# narrated-deck

> Turn a PPT / PDF / outline into a self-contained, narrated HTML page — with scene-by-scene visuals, synced subtitles, and per-segment TTS audio.

**Built by IQT** to operationalize the "dynamic HTML + AI voice" production pipeline behind the Kaohsiung City Health Bureau training platform. Now packaged so any IQT colleague — or, later, any external customer — can hand Claude **one PPT / PDF / outline** and get back **one folder containing `index.html` + `audio/*.mp3`** that runs in any browser.

---

## What it produces

```
my-project/
├── index.html          ← self-contained player (CSS/JS inline, no CDN)
├── subs.json           ← single source of truth: scenes + subtitles
├── scenes.json         ← visual content per scene
└── audio/
    ├── PROJ-001.mp3    ← one mp3 per subtitle
    ├── PROJ-002.mp3
    └── ...
```

Open `index.html` in any browser → it plays like a video, with synced narration and subtitles. Drop the folder onto a static host (Cloud Run, S3, GitHub Pages, Cloudflare Pages) and share a link.

---

## Use cases (validated or planned)

| Domain | Example | Status |
| --- | --- | --- |
| **Government training** | 高雄市衛生局 廣告合規檢測智慧化服務平台 (A1/B1) | ✅ shipped |
| **Product walk-throughs** | SaaS onboarding tour, demo videos | ▢ ready |
| **Children's stories** | Bilingual picture books with TTS | ▢ ready |
| **Conference talks** | Hands-off rehearsed presentations | ▢ ready |
| **Internal training** | New-hire onboarding, compliance refreshers | ▢ ready |

---

## How it works (architecture)

```
        ┌──────────────┐
        │  PPT / PDF   │   user input
        │  / outline   │
        └──────┬───────┘
               │
               ▼
   ┌────────────────────────┐
   │  Phase 1: EXTRACT      │   scripts/extract_pptx.py | extract_pdf.py
   │  pptx / pdf → JSON     │
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │  Phase 2: SCRIPT       │   Claude writes narration from extracted slides
   │  outline → narration   │   (see references/narration_writing.md)
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │  Phase 3: SUBS         │   Claude breaks narration into one-thought subs
   │  narration → subs.json │   (each sub = 1 mp3 = 1 visible line)
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │  Phase 4: TTS          │   scripts/tts_voai.py (or tts_elevenlabs.py)
   │  subs.json → mp3/*     │   1 mp3 per subtitle (eliminates drift)
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │  Phase 5: BUILD HTML   │   scripts/build_html.py
   │  player + theme + subs │   single self-contained file
   │  + scenes → index.html │
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │  Phase 6: SHIP         │   open locally OR drop on static host
   │  open / host / record  │   OR record to mp4 with OBS
   └────────────────────────┘
```

---

## Quick start

In Claude Code or Cowork mode, say:

> "Use narrated-deck. Here's my PPT — turn it into a narrated explainer."

Claude reads the skill, asks 2–3 questions about audience, tone, and length, then runs the pipeline end-to-end and hands you a folder.

Detailed instructions live in `skills/narrated-deck/SKILL.md`. Reference docs:

- `references/pipeline.md` — the full 6-phase pipeline
- `references/narration_writing.md` — how to turn slides into TTS-friendly subtitles
- `references/voai_api.md` — Voai.ai API reference + recommended voices
- `references/scene_types.md` — visual patterns (title, painpoint, demo, FAQ, etc.)
- `references/themes.md` — 4 built-in themes + how to add custom

---

## Requirements

- Python 3.9+ (extract, TTS, build scripts)
- `pip install python-pptx pdfplumber Pillow` (extract)
- A TTS API key — one of:
  - **Voai.ai** (`VOAI_API_KEY`) — preferred for traditional Chinese; supports Mandarin, Taiwanese, English. The Kaohsiung project used `Neo` + `佑希` + `聊天`.
  - **ElevenLabs** (`ELEVENLABS_API_KEY`) — fallback / multilingual; English-first; expensive on Chinese pronunciation accuracy.

---

## License & commercialization

Current: **Proprietary**, all rights reserved, IQT Technology Inc.

Internal use within IQT: ✅ free for any colleague to ship customer projects with.

External commercialization plan:

1. **Tier A — Open-source the player + extractor** (MIT). Lower the funnel.
2. **Tier B — Charge per-build / per-minute for the IQT-hosted TTS gateway** (managed Voai + ElevenLabs credits, no key required).
3. **Tier C — Enterprise license** (private fork, on-prem deployment, theme customization, SLA).

See `LICENSE.md` for the current legal text.

---

## Project status

- [x] Pipeline proven on Kaohsiung Health Bureau (A1 + B1, ~12 min each, ~110 mp3s, 0 retake)
- [x] Plugin scaffold + skill files
- [x] Voai.ai TTS script (Python)
- [x] ElevenLabs TTS script (Python, multilingual fallback)
- [x] PDF + PPTX extractor
- [x] HTML player template (per-subtitle mp3 architecture)
- [x] 4 built-in themes (government / product / children / corporate)
- [ ] Hosted IQT gateway (Phase 2 commercialization)
- [ ] Web UI for non-engineer users (Phase 3)

---

**Maintainer:** Matt Jiang &lt;matt.jiang@gmail.com&gt;
**Internal users:** any IQT colleague — start in `skills/narrated-deck/SKILL.md`
