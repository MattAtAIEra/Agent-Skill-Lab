# How to write narration for TTS

Hard-won lessons from the Kaohsiung Health Bureau pilot (~110 mp3s, multiple rewrites). The rules below cut TTS retake rate from 30% to 0%.

## The core principle

**TTS reads exactly what you write — including the punctuation.** It cannot infer pauses, emphasis, or correct mispronunciation. Write for the ear, not the eye.

## Voice — three checkpoints

1. **Read aloud yourself.** If you can't say it cleanly in one breath, TTS won't either.
2. **First-person, second-person — pick one and stick with it.** "I'll show you" + "您可以" gets schizophrenic. For training, "您" (formal) works best in zh-TW; "you" works for English; for children stories, use the protagonist's name.
3. **No bullet-point voice.** "Three things: A, B, C" reads OK on a slide but feels robotic out loud. Make it: "We're going to cover three things — first..."

## Subtitle granularity rules

A subtitle = a TTS unit = a visible line. Each one becomes ONE mp3.

| Language | Target chars/subtitle | Reasoning |
| --- | --- | --- |
| zh-TW / zh-CN | 10–30 chars | At ~4 chars/sec → 2.5–7.5s of audio per sub. Comfortable read pace. |
| English | 6–18 words | At ~2.5 words/sec → 2.5–7s of audio. |
| Japanese | 15–40 chars | Slightly slower pace. |

**End each subtitle at a natural breath point**: a period (`。`), comma (`，`), conjunction (`但是`, `而且`, `因為`), semicolon, or em-dash. Never split in the middle of a noun phrase.

❌ Bad: "您需要打開廣告" → "文案的 PDF 檔案"
✅ Good: "您需要打開廣告文案的 PDF 檔案" (one sub) OR "您需要打開廣告文案，" → "它通常是 PDF 檔案" (two subs at the comma)

## Things that trip TTS up

| Problem | Fix |
| --- | --- |
| Acronyms — "PDF", "OCR", "AI", "URL" | Test once. If Voai says "P-D-F" correctly, leave it. If it says "pdef", write "P D F" with spaces. ElevenLabs almost always pronounces acronyms correctly; Voai depends on speaker. |
| Numbers in Chinese — "28 條" | Both engines say this OK. But "$3.14" or "1,234" can confuse. Spell out: "三點一四" or "一千兩百三十四". |
| Idioms / classical | Voai's `佑希` mispronounced "一疊" as "一爹" in the Kaohsiung pilot. Replace classical compounds with modern equivalents if possible. |
| English brand names in Chinese sentence | Often OK. If wrong, write phonetic Chinese: "Salesforce" → "Sales force" (with space). |
| Em-dash `—` | Both engines pause naturally at em-dash. Use it freely for emphasis. |
| Trailing comma (e.g. "於是，") | Treated as a 0.3s pause — good for setting up the next sub. |
| All caps "STOP" | TTS may spell it out. Use lowercase or sentence case. |

## Pacing rules

- **First sub of intro** = empty (`text: ""`) with `dur: 4`. Gives viewers 4 seconds to settle in before narration starts.
- **Last sub of outro** = empty with long `dur` (e.g. `dur: 30` for a CTA card the viewer should sit on). Or for a feedback form, even `dur: 600`.
- **Between scenes**: don't add silent pauses unless visually motivated. The natural pause at the end of a sentence is enough.
- **Same scene, multiple subs**: that's fine. The scene stays visible while several subs play in sequence.

## Style by audience

### Government / institutional (e.g. Kaohsiung)
- 您 (formal you)
- "我們" instead of "我" (institutional voice)
- Avoid hyperbole; legal phrasing OK
- Acknowledge officer's expertise: "AI 替您省下逐字比對的時間，讓您專心處理疑難案件" — NOT "AI 替您解決所有問題"

### Product / SaaS
- "您" or "你" both fine; pick by region
- Concrete benefit per subtitle, no marketing fluff
- Show, don't claim: replace "革命性的" with "比舊版本快三倍"

### Children's story
- Use the protagonist's name often
- Short subs (5–15 chars) so kids can follow each spoken line
- Onomatopoeia + dialogue work great: "小狗汪汪叫，「我要去找媽媽！」"
- Sensory details: smell, sound, touch

### Conference / talk
- Conversational, slightly casual
- Self-aware: "你可能會問..." sets up Q&A
- Personal: "我自己第一次用的時候..."

## How to convert extracted PPT bullets into narration

This is the **most common** Phase 2 task. You'll have an `outline.json` from `extract_pptx.py` with a slide like:

```json
{
  "title": "違規廣告的代價",
  "bullets": [
    "消費者誤信誇大療效",
    "可能延誤就醫、傷害健康",
    "品牌十年累積的信任，一夕崩盤"
  ]
}
```

Don't just read the bullets. Connect them with conversational glue:

```
Sub 1: 為什麼衛生局要推這個平台？
Sub 2: 因為違規廣告的代價，不只是裁罰。
Sub 3: 消費者誤信誇大療效，可能延誤就醫、傷害健康；
Sub 4: 一旦事件爆發，品牌十年累積的信任，一夕之間崩盤。
```

Sub 1 = your added question (the slide title alone is too dry). Sub 2 = setup. Subs 3-4 = the bullet content, but as flowing sentences.

## Speaker notes from PPT

`extract_pptx.py` pulls speaker notes when present. **These are gold** — they're often the original presenter's verbal script. Start there if available. Just clean up:
- Remove "errrm" / "對對對" / "anyway"
- Split run-on sentences at natural breath points
- Re-target if needed (if notes say "I", maybe rewrite to "we" for institutional voice)

## Reviewing before TTS

Final pre-TTS checklist:

- [ ] Read every sub aloud. Each fits one breath.
- [ ] Total length ≈ target (count subs × ~5s = total min).
- [ ] No bullet-list voice.
- [ ] Acronyms tested or pre-flagged.
- [ ] No idioms TTS will mispronounce.
- [ ] Tone consistent across subs.
- [ ] First sub is empty intro; last sub is empty outro.

Then run TTS. **First TTS pass is gold** for catching pronunciation issues — listen to every mp3 before approving.
