# License

Copyright (c) 2026 IQT Technology Inc. All rights reserved.

## Internal use (IQT colleagues)

Any current employee or contractor of IQT Technology Inc. may use, modify, and ship this plugin as part of their work on IQT customer projects — including:

- Government engagements (e.g. Kaohsiung City Health Bureau)
- Internal training materials
- Customer demos & explainer videos
- Product walk-throughs in IQT-developed software

No additional permission is needed for internal use.

## External use

This software is **not yet open-sourced**. Third parties — including non-IQT customers, agencies, and partners — may **not** copy, distribute, or use this plugin without a written license from IQT Technology Inc.

To enquire about a commercial license, contact: matt.jiang@iqtechnology.ai

## Future licensing plan

The maintainer (Matt Jiang) intends to split this work into three tiers:

| Tier | Component | License (planned) |
| --- | --- | --- |
| **A** | HTML player + PPT/PDF extractor | MIT |
| **B** | Managed TTS gateway (no API key needed) | Per-minute SaaS pricing |
| **C** | Enterprise theme system + on-prem deployment | Annual commercial license |

This plan may change. Until tier-A is publicly released under MIT, **the default rule is: proprietary, IQT-internal only**.

## Third-party components

- **Voai.ai** TTS API — used at runtime; subject to Voai.ai's terms (https://www.voai.ai)
- **ElevenLabs** TTS API — optional; subject to ElevenLabs' terms (https://elevenlabs.io)
- **python-pptx** — MIT
- **pdfplumber** — MIT
- **Pillow** — HPND

No third-party source code is bundled. Only API calls are made.

---

For licensing questions: matt.jiang@iqtechnology.ai
