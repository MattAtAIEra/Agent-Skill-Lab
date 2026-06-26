# Voai.ai TTS — API reference & voice selection

## Endpoint

```
POST https://connect.voai.ai/TTS/Speech
```

## Headers

```
x-api-key: iq-xxx
x-output-format: mp3      # or wav
Content-Type: application/json
accept: */*
```

## Request body

```json
{
  "version": "Neo",
  "speaker": "佑希",
  "style": "聊天",
  "text": "您要朗讀的文字。",
  "speed": 1.0,
  "pitch_shift": 0,
  "style_weight": 0.5,
  "breath_pause": 0
}
```

## Versions

| Version | Use case |
| --- | --- |
| `Neo` (recommended) | Latest model. Best quality, natural intonation. |
| `Sota` | Previous stable. Use if Neo has issues for your speaker. |

(Older `Echo` is deprecated.)

## Speakers (verified for Mandarin TW)

| Speaker | Voice profile | Best for |
| --- | --- | --- |
| **佑希** | Warm female, mid-20s | Training, customer-service, story telling — most versatile |
| **沛文** | Mature male | Authority, news, formal announcements |
| **語安** | Soft female, calm | Bedtime stories, meditation, gentle explainers |
| **凡凡** | Energetic young female | Product launches, marketing, social videos |
| **小波** | Friendly male, casual | Podcasts, conversational explainers |

Browse the full speaker list at [voai.ai/speakers](https://www.voai.ai). They add new ones often.

## Styles (per speaker, may vary)

| Style | When to pick |
| --- | --- |
| **聊天** | Conversational. Default for training & explainers. |
| **客服** | Customer service — slightly more formal & even. |
| **旁白** | Narrator — measured pace, good for documentaries. |
| **故事** | Storytelling — varied intonation, expressive. Best for kids' books. |
| **廣告** | Energetic, marketing tone. Good for promo videos. |

## Style weight & speed

- `style_weight: 0.5` (default) — moderate stylization. Move up (0.7) for more dramatic; down (0.3) for more neutral.
- `speed: 1.0` (default) — try 1.05 if pacing feels slow. Going > 1.2 makes Mandarin choppy.
- `pitch_shift: 0` — leave at 0 unless you have a specific reason.
- `breath_pause: 0` — set to 1 if you want explicit breath sounds between subs (rarely used).

## Recommended presets for Kaohsiung-style training

```python
{
  "version": "Neo",
  "speaker": "佑希",
  "style": "聊天",
  "speed": 1.0,
  "style_weight": 0.5
}
```

This is what the Kaohsiung Health Bureau A1/B1 modules use. Audience reports the voice "sounds like a calm senior colleague explaining things" — exactly the target.

## Recommended for children's stories

```python
{
  "version": "Neo",
  "speaker": "語安",
  "style": "故事",
  "speed": 0.95,
  "style_weight": 0.7
}
```

## Pricing & quota

- Voai has a free tier (a few thousand chars).
- Beyond that, see voai.ai pricing — roughly NT$ 0.001 / char for Neo at time of writing.
- Per-subtitle calls are cheap. A 12-min explainer = ~5,000 chars = NT$ 5.

## Known issues & workarounds

| Symptom | Fix |
| --- | --- |
| "一疊" pronounced as "一爹" | Swap to "一堆" or rewrite the sentence |
| Acronyms slurred | Add spaces: "PDF" → "P D F" |
| First call returns HTTP 200 with JSON error | Retry — usually transient. The included `tts_voai.py` retries 3× automatically. |
| Voice cuts off final char | Add a period at the end of the text |
| Pause too short between sentences | End sub with "。" not "，"; or add a trailing space |
| "Sota" or "Neo" must be capitalized | Use exact strings; lowercase fails silently |

## Comparing Voai vs ElevenLabs

| Feature | Voai.ai | ElevenLabs |
| --- | --- | --- |
| zh-TW pronunciation | ★★★★★ (best in class) | ★★★ (multilingual but slipups) |
| English | ★★★ | ★★★★★ |
| Japanese | ★★★ | ★★★★ |
| Voice variety | ~15 named speakers | 1000s (custom clones) |
| Cost | Cheap (NT$ pricing) | More expensive |
| Latency | ~1–2s per sub | ~1–3s per sub |
| API stability | Good (occasional JSON-on-200 quirks) | Excellent |

For Chinese-language Taiwan projects, default to Voai. For multilingual or English-primary, use ElevenLabs.
