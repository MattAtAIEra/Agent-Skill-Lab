# Themes

Each theme is a CSS file in `themes/` that overrides the base color tokens. The HTML structure is identical across themes — so you can swap themes without rebuilding TTS or scenes.

## Built-in themes

| Theme | Vibe | Use cases |
| --- | --- | --- |
| `government` | Deep green + warm cream | Gov training, compliance, public health |
| `product` | Indigo + sky blue | SaaS demos, product launches, sales enablement |
| `children` | Pink + yellow + mint | Kids' stories, picture books, school content |
| `corporate` | Navy + gray | B2B explainers, internal training, investor updates |

## Switching theme

```bash
python3 scripts/build_html.py --subs A.subs.json --scenes scenes.json --theme product
```

No re-narration, no rebuild of TTS, no scene changes. The CSS layer is fully independent.

## Customizing colors only (5 minutes)

Make a new theme file:

```css
/* themes/my-brand.css */
:root {
  --primary: #YOUR_BRAND_PRIMARY;
  --secondary: #YOUR_BRAND_SECONDARY;
  --accent: #YOUR_BRAND_ACCENT;
  --warn: #YOUR_BRAND_WARN;
  --cream: #YOUR_BG;
  --ink: #YOUR_TEXT;
  --dim: #YOUR_DIM_TEXT;
  --white: #ffffff;
  --display-font: "Your Font", sans-serif;
}
```

Then `--theme my-brand`. Done.

## Color guidance

| Token | What it controls | Pick by... |
| --- | --- | --- |
| `--primary` | Topbar, buttons, headlines | Brand primary; should be dark enough for white text contrast |
| `--secondary` | Card #2 backgrounds, hover states | Brand supporting color |
| `--accent` | Errors, "red light", urgent CTAs | High-contrast warning color (red/coral) |
| `--warn` | Amber highlights, "orange light", progress bar | Warning yellow/amber |
| `--cream` | Page background | Light, easy on eyes |
| `--ink` | Body text | Near-black with personality (warm gray, deep slate) |
| `--dim` | Secondary text | Mid-gray; ~AA contrast on cream |

### Accessibility

The base templates aim for WCAG AA:
- 4.5:1 contrast for body text on background
- 3:1 for large display text
- Subtitle bar has 16:1 (white on near-black)

When you swap colors, verify with a contrast checker. The `--dim` text on `--cream` background is the riskiest pair.

## Adding theme-specific scene CSS

Some themes (`children`) need bigger fonts. To customize beyond color tokens, just write regular CSS in your theme file targeting the existing class names:

```css
/* themes/children.css */
.subtitle-bar { font-size: 30px !important; }
.scene-title .display { font-size: 110px !important; }
.card, .panel { border-radius: 24px !important; }
```

Use `!important` sparingly — only when overriding the base. The template doesn't use `!important` itself, so single `!important`s win.

## Per-project custom theme

If a customer has strong brand requirements (logo, custom font hosted via CDN, weird layout asks), make a `themes/{customer}.css`. Commit it. Future builds for that customer use `--theme {customer}`.

## Roadmap

- [ ] Theme picker UI in the web admin (future)
- [ ] Auto-extract colors from customer logo
- [ ] Dark-mode variants of each theme
- [ ] RTL language support (Arabic, Hebrew)
