#!/usr/bin/env python3
"""build_html.py — assemble subs.json + scenes.json + theme into a single HTML.

Usage:
  python3 build_html.py \\
    --subs A1.subs.json \\
    --scenes scenes.json \\
    --theme government \\
    --out index.html

The output is self-contained (CSS inline, no CDN). Audio is referenced as
relative URLs (`audio/{prefix}-{id}.mp3`), so the folder layout the user ships is:

  out_folder/
    index.html       ← built here
    audio/           ← from tts_voai.py
      PROJ-001.mp3
      ...

The scenes.json schema is documented in references/scene_types.md. Each scene
entry has {id, type, props}; this script renders type-specific HTML using
built-in templates (title, painpoint, callout-stack, cards-3, browser-demo,
outro, generic). Unknown types fall back to a "generic" two-text layout.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
TEMPLATE_DIR = HERE.parent / "templates"
THEME_DIR = HERE.parent / "themes"

# ── Default labels (overridden by --lang or scenes.json.meta.labels) ──
LABELS = {
    "zh-Hant": {
        "play": "播放", "pause": "暫停",
        "prev": "上一段", "next": "下一段", "restart": "重播",
        "scene": "場景", "no_audio": "部分配音檔尚未產生（將以預估秒數播放靜音）",
    },
    "zh-Hans": {
        "play": "播放", "pause": "暂停",
        "prev": "上一段", "next": "下一段", "restart": "重播",
        "scene": "场景", "no_audio": "部分配音文件尚未生成（将以预估秒数播放静音）",
    },
    "en": {
        "play": "Play", "pause": "Pause",
        "prev": "Prev", "next": "Next", "restart": "Restart",
        "scene": "Scene", "no_audio": "Some audio missing — falling back to estimated timing",
    },
    "ja": {
        "play": "再生", "pause": "一時停止",
        "prev": "前へ", "next": "次へ", "restart": "最初から",
        "scene": "シーン", "no_audio": "一部の音声が未生成です（推定秒数で進行します）",
    },
}


def render_scene_title(scene):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    display = p.get("display", "")  # raw HTML allowed for accent spans
    tagline = escape(p.get("tagline", ""))
    series = escape(p.get("series", ""))
    return f'''
    <div class="scene scene-title" data-id="{scene["id"]}">
      <span class="blob b1"></span><span class="blob b2"></span>
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      <div class="display">{display}</div>
      <div class="ribbon"></div>
      {f'<div class="tagline">{tagline}</div>' if tagline else ''}
      {f'<div class="series">{series}</div>' if series else ''}
    </div>'''


def render_scene_outro(scene):
    p = scene["props"]
    display = p.get("display", "")
    nxt = escape(p.get("next", ""))
    return f'''
    <div class="scene scene-outro" data-id="{scene["id"]}">
      <span class="blob b1"></span><span class="blob b2"></span>
      <div class="display">{display}</div>
      {f'<div class="next">{nxt}</div>' if nxt else ''}
    </div>'''


def render_painpoint(scene):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    title = escape(p.get("title", ""))
    left = p.get("left_panel", {})
    right = p.get("right_panel", {})

    def panel(d, dark=False):
        cls = "panel dark" if dark else "panel"
        h = escape(d.get("title", ""))
        items = "".join(f"<li>{escape(b)}</li>" for b in d.get("bullets", []))
        stat_html = ""
        if d.get("stat"):
            stat_html = f'<div class="stat">{escape(d["stat"]["label"])}<span class="num">{escape(str(d["stat"]["value"]))}</span></div>'
        return f'<div class="{cls}"><h3>{h}</h3><ul>{items}</ul>{stat_html}</div>'

    return f'''
    <div class="scene" data-id="{scene["id"]}">
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      <div class="h1">{title}</div>
      <div class="painpoint">{panel(left)}{panel(right, dark=True)}</div>
    </div>'''


def render_cards(scene, n=3):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    title = escape(p.get("title", ""))
    cards = p.get("cards", [])
    tag = escape(p.get("tagline", ""))
    cls = f"cards-{n}"
    cards_html = ""
    for i, c in enumerate(cards):
        num = c.get("num", str(i+1))
        ccls = f"c{(i%4)+1}"
        cards_html += f'''
        <div class="card">
          <div class="card-num {ccls}">{escape(str(num))}</div>
          <div>
            <div class="card-title">{escape(c.get("title",""))}</div>
            <div class="card-body">{escape(c.get("body",""))}</div>
          </div>
        </div>'''
    tag_html = f'<div class="tagline-center">{tag}</div>' if tag else ''
    return f'''
    <div class="scene" data-id="{scene["id"]}">
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      <div class="h1">{title}</div>
      <div class="{cls}">{cards_html}</div>
      {tag_html}
    </div>'''


def render_callout_stack(scene):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    title = escape(p.get("title", ""))
    items = p.get("items", [])
    items_html = ""
    color_classes = ["cl-a", "cl-w", "cl-blue", "cl-p", "cl-s"]
    for i, it in enumerate(items):
        icon = escape(it.get("icon", str(i+1)))
        color = it.get("color")  # explicit override
        cls = "cl-" + color if color else color_classes[i % len(color_classes)]
        items_html += f'''
        <div class="callout">
          <div class="callout-icon {cls}">{icon}</div>
          <div>
            <div class="callout-title">{escape(it.get("title",""))}</div>
            <div class="callout-desc">{escape(it.get("desc",""))}</div>
          </div>
        </div>'''
    return f'''
    <div class="scene" data-id="{scene["id"]}">
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      <div class="h1">{title}</div>
      <div class="callout-stack">{items_html}</div>
    </div>'''


def render_browser_demo(scene):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    title = escape(p.get("title", ""))
    url = escape(p.get("url", "https://example.com"))
    body_html = p.get("body_html", "")  # raw HTML
    return f'''
    <div class="scene" data-id="{scene["id"]}">
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      <div class="h1">{title}</div>
      <div class="browser">
        <div class="browser-bar">
          <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="browser-url">{url}</span>
        </div>
        <div class="browser-body">{body_html}</div>
      </div>
    </div>'''


def render_generic(scene):
    p = scene["props"]
    eyebrow = escape(p.get("eyebrow", ""))
    title = escape(p.get("title", ""))
    lead = escape(p.get("lead", ""))
    body_html = p.get("body_html", "")
    return f'''
    <div class="scene" data-id="{scene["id"]}">
      {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
      {f'<div class="h1">{title}</div>' if title else ''}
      {f'<div class="lead">{lead}</div>' if lead else ''}
      {body_html}
    </div>'''


SCENE_RENDERERS = {
    "title": render_scene_title,
    "outro": render_scene_outro,
    "painpoint": render_painpoint,
    "cards-3": lambda s: render_cards(s, 3),
    "cards-2": lambda s: render_cards(s, 2),
    "callout-stack": render_callout_stack,
    "browser-demo": render_browser_demo,
    "generic": render_generic,
}


def render_scene(scene):
    fn = SCENE_RENDERERS.get(scene.get("type", "generic"), render_generic)
    return fn(scene)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subs", required=True, help="Path to {prefix}.subs.json")
    ap.add_argument("--scenes", required=True, help="Path to scenes.json")
    ap.add_argument("--theme", default="government",
                    help="Theme name (government / product / children / corporate)")
    ap.add_argument("--out", default="index.html")
    ap.add_argument("--lang", default="zh-Hant", help="Language code (zh-Hant / zh-Hans / en / ja)")
    ap.add_argument("--crumb", help="Top-bar breadcrumb text (default: title from subs.json)")
    ap.add_argument("--audio-dir", default="audio", help="Audio folder name relative to HTML")
    args = ap.parse_args()

    subs_data = json.loads(Path(args.subs).read_text(encoding="utf-8"))
    scenes_data = json.loads(Path(args.scenes).read_text(encoding="utf-8"))
    tmpl = (TEMPLATE_DIR / "player.html.tmpl").read_text(encoding="utf-8")

    # theme CSS
    theme_path = THEME_DIR / f"{args.theme}.css"
    if theme_path.exists():
        theme_css = theme_path.read_text(encoding="utf-8")
    else:
        print(f"  warn: theme '{args.theme}' not found; using built-in default", file=sys.stderr)
        theme_css = ""

    # render all scenes
    scenes_html = "\n".join(render_scene(s) for s in scenes_data["scenes"])

    # scene labels
    scene_labels = {s["id"]: s.get("label", s["id"]) for s in scenes_data["scenes"]}

    # subs json (only the array)
    subs_json_str = json.dumps(subs_data["subs"], ensure_ascii=False, indent=2)

    labels = LABELS.get(args.lang, LABELS["zh-Hant"])
    crumb = args.crumb or subs_data.get("title", "")

    out = tmpl
    replacements = {
        "{{LANG}}": args.lang,
        "{{TITLE}}": escape(subs_data.get("title", "")),
        "{{CRUMB}}": escape(crumb),
        "{{PREFIX}}": subs_data["prefix"],
        "{{AUDIO_DIR}}": args.audio_dir,
        "{{SUBS_JSON}}": subs_json_str,
        "{{SCENE_LABELS_JSON}}": json.dumps(scene_labels, ensure_ascii=False),
        "{{SCENES_HTML}}": scenes_html,
        "{{THEME_CSS}}": theme_css,
        "{{LBL_PLAY}}": labels["play"],
        "{{LBL_PAUSE}}": labels["pause"],
        "{{LBL_PREV}}": labels["prev"],
        "{{LBL_NEXT}}": labels["next"],
        "{{LBL_RESTART}}": labels["restart"],
        "{{LBL_SCENE}}": labels["scene"],
        "{{LBL_NO_AUDIO}}": labels["no_audio"],
    }
    for k, v in replacements.items():
        out = out.replace(k, v if isinstance(v, str) else str(v))

    Path(args.out).write_text(out, encoding="utf-8")
    print(f"✓ Built {args.out}")
    print(f"  Scenes: {len(scenes_data['scenes'])}")
    print(f"  Subs:   {len(subs_data['subs'])}")
    print(f"  Theme:  {args.theme}")
    print()
    print("  Next: place audio/ folder beside this HTML, then open in browser.")


if __name__ == "__main__":
    main()
