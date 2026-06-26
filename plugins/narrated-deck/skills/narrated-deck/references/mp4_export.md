# Exporting to MP4 video

The HTML player is the primary deliverable, but sometimes you need an MP4 — for YouTube, LMS uploads (Moodle, SAP SuccessFactors), or LINE distribution.

## Method 1 — screen record (easiest)

### macOS
- QuickTime Player → File → New Screen Recording → select browser window
- Play HTML fullscreen → record
- Stop → save as `.mov` → convert to `.mp4` with ffmpeg:
  ```bash
  ffmpeg -i recording.mov -c:v libx264 -crf 23 -c:a aac out.mp4
  ```

### Windows
- Win+G (Game Bar) → Capture → Start Recording
- Play HTML → stop
- Output is mp4 directly

### Cross-platform
- [OBS Studio](https://obsproject.com/) — free, scriptable, more control
- Set canvas to 1920×1080
- Add Browser source → URL pointing to local HTML
- Record at 30fps, x264

## Method 2 — Playwright + ffmpeg (programmatic)

For batch processing (e.g. A1, A2, A3, A4 all at once).

```js
// scripts/record_mp4.js
const { chromium } = require('playwright');
const { spawn } = require('child_process');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: 'videos/', size: { width: 1920, height: 1080 } },
  });
  const page = await ctx.newPage();
  await page.goto(`file://${process.cwd()}/index.html`);
  await page.click('#playBtn');
  // wait for total duration (e.g. 720s = 12 min)
  await page.waitForTimeout(720_000);
  await ctx.close();
  await browser.close();
})();
```

Then ffmpeg the resulting webm → mp4:
```bash
ffmpeg -i videos/recording.webm -c:v libx264 -crf 22 out.mp4
```

**Caveat**: headless Chromium doesn't play audio. To capture audio you need ffmpeg's audio mixing — or run in headed mode with a virtual display (Xvfb).

## Method 3 — composite via ffmpeg from scratch (advanced)

If you have all the mp3s already, you can synthesize the video without a browser:

1. Render each scene as a PNG (via Playwright screenshot)
2. Concat MP3s in order with subtitle overlays
3. ffmpeg-concat the result

This is more brittle but gives byte-perfect output. Worth it for productized pipelines.

## File size targets

| Quality | Resolution | Bitrate | 12-min size |
| --- | --- | --- | --- |
| YouTube standard | 1920×1080 | 8 Mbps | ~720 MB |
| Internal review | 1280×720 | 4 Mbps | ~360 MB |
| Email-friendly | 1280×720 | 2 Mbps | ~180 MB |
| Storyboard preview | 854×480 | 1 Mbps | ~90 MB |

x264 CRF 22-25 hits a good quality/size sweet spot for explainer content (mostly static backgrounds + text).

## Subtitle handling for video

If exporting to YouTube, generate an SRT for closed captions:

```python
# scripts/subs_to_srt.py (TODO)
# Uses subs.json + actual mp3 durations to write SRT timing
```

Not yet shipped — file a feature request if needed.

## Why we still prefer HTML over MP4

| Aspect | HTML | MP4 |
| --- | --- | --- |
| Update one word | 20s | re-cut entire video |
| Mobile playback | ✅ adaptive | ✅ but larger file |
| Embed analytics | ✅ js hooks | ❌ (depends on host) |
| Accessibility | ✅ screen-reader friendly | depends on captions |
| Multi-language | swap subs.json | re-render entire video |
| Distribution | static URL | YouTube/Vimeo |

For most B2B uses, **publish the HTML on a Cloud Run / static host URL**. Reserve MP4 for cases where the destination platform requires it.
