# Scene types — reusable visual patterns

`build_html.py` ships with 8 built-in scene types. Each has a `type` and `props` JSON shape. Use these as building blocks; fall back to `generic` with raw `body_html` for anything custom.

---

## 1. `title` — opening / hero scene

Big gradient background, oversized display text. Use as the very first scene.

```json
{
  "id": "s01",
  "type": "title",
  "label": "Opening",
  "props": {
    "eyebrow": "MODULE A1 ‧ INSPECTOR TRAINING",
    "display": "Audit smarter,<br><span class='accent'>not harder</span>",
    "tagline": "Spend 5 minutes per case, not 30.",
    "series": "Kaohsiung Health Bureau"
  }
}
```

`display` accepts raw HTML so you can highlight a word with `<span class="accent">`.

---

## 2. `painpoint` — two-column problem/solution

Light panel left (current state), dark panel right (better state). Bullets + optional stat.

```json
{
  "id": "s02",
  "type": "painpoint",
  "label": "The problem",
  "props": {
    "eyebrow": "WHY THIS MATTERS",
    "title": "The cost of getting it wrong",
    "left_panel": {
      "title": "Today",
      "bullets": [
        "Manual cross-checking",
        "30 minutes per case",
        "Risk of missed violations"
      ],
      "stat": {"label": "avg time / case", "value": "30 min"}
    },
    "right_panel": {
      "title": "With AI",
      "bullets": [
        "Automatic violation detection",
        "5 minutes per case",
        "Three-color signal highlights"
      ],
      "stat": {"label": "avg time / case", "value": "5 min"}
    }
  }
}
```

---

## 3. `cards-3` / `cards-2` — N-step or N-takeaway grid

Use for "what you'll learn", "the 3 steps", "top takeaways".

```json
{
  "id": "s05",
  "type": "cards-3",
  "label": "Three steps",
  "props": {
    "eyebrow": "THE WORKFLOW",
    "title": "Three steps, end-to-end",
    "cards": [
      {"num": "1", "title": "Upload PDF", "body": "Scan or drag-drop the case file."},
      {"num": "2", "title": "AI analyzes", "body": "OCR + violation detection in 30s."},
      {"num": "3", "title": "You review", "body": "Focus on highlighted segments only."}
    ],
    "tagline": "Five minutes, end-to-end."
  }
}
```

---

## 4. `callout-stack` — vertical list of points

Used for the 3-color signal explanation in Kaohsiung A1 (red / orange / blue rows). Each row has an icon circle + title + description.

```json
{
  "id": "s09",
  "type": "callout-stack",
  "label": "Three-color signal",
  "props": {
    "eyebrow": "AI VIOLATION REPORT",
    "title": "Red / Orange / Blue",
    "items": [
      {
        "icon": "紅",
        "color": "a",
        "title": "Red — defined violation",
        "desc": "Phrasing explicitly listed as illegal by regulation."
      },
      {
        "icon": "橘",
        "color": "w",
        "title": "Orange — similar precedent",
        "desc": "Similar to violations with prior penalty cases."
      },
      {
        "icon": "藍",
        "color": "blue",
        "title": "Blue — conditional",
        "desc": "Violation only in specific context."
      }
    ]
  }
}
```

Color codes (suffix after `cl-`): `p` (primary), `s` (secondary), `a` (accent/red), `w` (warn/amber), `blue` (signal blue).

---

## 5. `browser-demo` — browser frame with custom body

A faux browser chrome (3 dots + URL bar) wrapping any HTML you want. Use for product walk-throughs, screen mockups.

```json
{
  "id": "s10",
  "type": "browser-demo",
  "label": "Demo: case list",
  "props": {
    "eyebrow": "AFTER LOGIN",
    "title": "Your case dashboard",
    "url": "platform.example.com/cases",
    "body_html": "<h4>5 cases pending review</h4><div class='case-row'>Case #2026-001 <span class='badge'>HIGH RISK</span></div><div class='case-row'>Case #2026-002 <span class='badge'>LOW RISK</span></div>"
  }
}
```

`body_html` is raw HTML — use any tag, including styled `<div>`s. Build images as `<svg>` inline for fully self-contained portability.

---

## 6. `outro` — closing scene

Same gradient look as title; just a display message + optional "next" line.

```json
{
  "id": "s18",
  "type": "outro",
  "label": "Closing",
  "props": {
    "display": "Thanks for <span class='accent'>watching</span>",
    "next": "Module A2 — handling complex cases — coming next week."
  }
}
```

---

## 7. `generic` — escape hatch

When the 6 patterns above don't fit. Provide raw HTML for the body.

```json
{
  "id": "s17",
  "type": "generic",
  "label": "Custom layout",
  "props": {
    "eyebrow": "OPTIONAL",
    "title": "Anything you want",
    "lead": "Optional lead text",
    "body_html": "<div style='padding:20px'>Your HTML here</div>"
  }
}
```

You can mix any of the built-in CSS classes inside `body_html`: `.callout`, `.card`, `.panel`, etc.

---

## Custom scene types

To add a new type:

1. Write a new renderer function in `scripts/build_html.py` (e.g. `render_timeline`).
2. Add it to the `SCENE_RENDERERS` dict.
3. Add CSS in `templates/player.html.tmpl` (in the `<style>` block) or in your theme CSS.
4. Document the new type here.

## Choosing scene types from extracted slides

| Slide content | Suggested type |
| --- | --- |
| Title slide | `title` |
| Problem / agitation | `painpoint` |
| 3 bullets / 3 steps | `cards-3` |
| 2-column comparison | `painpoint` or `cards-2` |
| Sequential list (5-7 items) | `callout-stack` |
| Product screenshot | `browser-demo` |
| Stat or quote | `generic` (with custom body) |
| FAQ row | `cards-2` |
| Closing / CTA | `outro` |

Don't over-design. **2-3 scene types repeating** beats 10 unique types — viewer expectation builds momentum.
