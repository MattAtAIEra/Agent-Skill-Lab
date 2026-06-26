# narrated-deck 播放器：手機版控制列 開發紀錄

> 目的：把「手機版按鈕只顯示 icon」與「修正手機版 Safari 控制列消失」兩項處理整理成可套用到 skill 的變更說明。
> 設計原則：**全部採漸進降級（graceful degradation）**，對非 Safari、舊瀏覽器、桌機皆無副作用。
> 已在三大引擎驗證：Blink（Chrome/Edge）、WebKit（Safari）、Gecko（Firefox）。

---

## 變更範圍

只動到一個檔案：**`templates/player.html.tmpl`**（播放器模板）。
主題 CSS、build script、字幕/場景 JSON 結構皆**不需更動**。

共 5 處變更，分屬兩個功能（外加一個附帶 UX 變更，可選）。

---

## 功能一：手機版按鈕只顯示 icon

### 問題
原本按鈕文字是「icon + 中文」寫在同一個 textContent（例如 `▶ 播放`）。在窄螢幕（手機）上文字換行成上下兩排、且按鈕過寬，把右側的時間（`0:00 / 2:00`）與段落提示（`x / N ‧ 標題`）擠出邊界。

### 做法
把 icon 與文字拆成獨立 `<span>`，手機版只隱藏文字、放大 icon。

**(A) 按鈕 HTML —— icon / label 拆成 span**

```html
<!-- before -->
<button class="btn warn"  id="playBtn">▶ {{LBL_PLAY}}</button>
<button class="btn ghost" id="prevBtn">⏮ {{LBL_PREV}}</button>
<button class="btn ghost" id="nextBtn">⏭ {{LBL_NEXT}}</button>
<button class="btn ghost" id="restartBtn">⟲ {{LBL_RESTART}}</button>

<!-- after -->
<button class="btn warn"  id="playBtn"><span class="ticon">▶</span><span class="tlabel">{{LBL_PLAY}}</span></button>
<button class="btn ghost" id="prevBtn"><span class="ticon">⏮</span><span class="tlabel">{{LBL_PREV}}</span></button>
<button class="btn ghost" id="nextBtn"><span class="ticon">⏭</span><span class="tlabel">{{LBL_NEXT}}</span></button>
<button class="btn ghost" id="restartBtn"><span class="ticon">⟲</span><span class="tlabel">{{LBL_RESTART}}</span></button>
```

**(B) JS —— 播放鍵改用 `setPlayBtn()` 更新 span（取代直接覆寫 textContent）**

因為 play/pause 會切換播放鍵的圖示與文字，原本是 `playBtn.textContent = '⏸ {{LBL_PAUSE}}'`，會把 span 結構洗掉。改成只更新對應 span：

```js
// 新增 helper
function setPlayBtn(playing){
  var ic = playBtn.querySelector('.ticon'), lb = playBtn.querySelector('.tlabel');
  if (ic) ic.textContent = playing ? '⏸' : '▶';
  if (lb) lb.textContent = playing ? '{{LBL_PAUSE}}' : '{{LBL_PLAY}}';
  playBtn.classList.toggle('is-playing', playing);   // 供 CTA 脈動判斷（見附帶變更）
}

// play() / pause() 改用 helper
function play()  { isPlaying = true;  setPlayBtn(true);  playCurrent(); }
function pause() { isPlaying = false; setPlayBtn(false); clearTimers(); player.pause(); }
```

`advance()` 播放結束的分支也要一起改（原本同樣是 `playBtn.textContent = '▶ {{LBL_PLAY}}'`）：

```js
// 結束、停在最後一幕時
isPlaying = false;
setPlayBtn(false);          // 原本是 playBtn.textContent = '▶ {{LBL_PLAY}}';
player.pause();
render(durOf(s));
```

> 其餘三顆鈕（prev/next/restart）的文字由 HTML 設定後 JS 不再改寫，所以拆成 span 後不需動 JS。

**(C) CSS —— span 基本樣式 + 手機版斷點（icon-only）**

桌機維持「icon + 中文」並排；`@media (max-width: 540px)` 時隱藏文字、放大 icon。

```css
/* 基本：span 並排，重建 icon 與文字間距 */
.btn .ticon  { font-style: normal; line-height: 1; }
.btn .tlabel { margin-left: 6px; }

/* 手機：左側純 icon 按鈕 + 右側時間（標準播放器佈局）。
   只縮字體不夠 —— .scene-chip 帶不定長度的中文場景標題、被 margin-left:auto 推到最右，
   窄螢幕仍會換行/溢出把控制列撐破版；故手機直接移除所有文字標籤與提示，只留 icon + 時間。 */
@media (max-width: 540px) {
  .controls      { padding-left: 10px; padding-right: 10px; gap: 6px; } /* 注意：勿用 padding shorthand，見功能二說明 */
  .btn           { padding: 9px 11px; flex-shrink: 0; }   /* 按鈕不被壓縮變形 */
  .btn .tlabel   { display: none; }                       /* 移除按鈕文字，只留 icon */
  .btn .ticon    { font-size: 22px; }                     /* 放大 icon */
  .timeinfo      { font-size: 12px; white-space: nowrap; flex-shrink: 0; margin-left: auto; } /* 時間不換行、推到最右 */
  .scene-chip    { display: none; }   /* 段落標題長度不定，移除避免破版（進度見頂部進度條） */
  .no-audio-note { display: none; }   /* 異常提示，手機移除以保版面（遇錯仍會自動前進） */
}
```

斷點取 **540px**：手機直式約 ≤430px，540 留餘裕並涵蓋大尺寸手機/小尺寸橫式；平板（≥768px）仍顯示中文。

> 寬度預算（border-box，最窄手機）：4 顆 icon 鈕 ≈ 184px + gap 24px + 時間 ≈ 63px + 左右 padding 20px ≈ **291px**，在 320px 視窗仍有 ~29px 餘裕；375px 以上更寬鬆。`flex-shrink:0` + `nowrap` + 移除不定長度元素 → 結構上不會溢出。

---

## 功能二：修正手機版 Safari 控制列消失

### 問題（iOS Safari 的 `100vh` 陷阱）
`#stage` 用 `height: 100vh`。**iOS Safari 的 `100vh` 把底部工具列佔的高度也算進去**，使舞台比實際可視範圍高；又因 `html, body { overflow: hidden }`，被推到工具列底下的**最底控制列就完全看不到、也無法捲動**。Android Chrome 工具列收合時也有類似落差。

### 做法（皆為標準、跨瀏覽器的修法，非 Safari hack）

**(D) `#stage` 改用動態可視高度 `100dvh`（保留 `100vh` fallback）**

```css
#stage {
  position: relative; width: 100vw;
  height: 100vh;       /* fallback：不支援 dvh 的舊瀏覽器 */
  height: 100dvh;      /* 支援者覆蓋：隨工具列收合即時調整 */
  ...
}
```

**(E) meta 加 `viewport-fit=cover` + 控制列/字幕條加底部安全區**

讓內容延伸到瀏海機底部，並用 `env(safe-area-inset-bottom)` 把按鈕墊高、避開 Home Indicator。

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
.controls {
  height: calc(64px + env(safe-area-inset-bottom, 0px)); /* 高度含安全區 */
  ...
  padding: 0 24px;
  padding-bottom: env(safe-area-inset-bottom, 0px);      /* 按鈕墊高，避開 Home Indicator */
  ...
}

.subtitle-bar {
  ...
  bottom: calc(88px + env(safe-area-inset-bottom, 0px)); /* 同步上抬，維持與控制列的間距 */
}
```

> ⚠️ **重點 / 易踩雷**：手機版 media query 內**不要用 `padding` shorthand**（例如 `padding: 0 10px`），那會把上面的 `padding-bottom: env(...)` 重設為 0，導致安全區在手機（最需要的地方）失效。所以功能一的 `.controls` 手機規則改用 `padding-left` / `padding-right`，保住 `padding-bottom`。

> 高度計算前提：模板有 `* { box-sizing: border-box }`。在 border-box 下，`height: calc(64px + inset)` 搭配 `padding-bottom: inset` → 內容區剛好 64px、底部 inset 為安全區。若主題改了 box-sizing 需重新核算。

---

## 跨瀏覽器安全性（為何不影響其他手機瀏覽器）

| 變更 | 不支援 / 無安全區的環境會發生什麼 |
|---|---|
| `height: 100vh; height: 100dvh;` | 不支援 `dvh` 者忽略該行、沿用 `100vh`（即原行為，無退步）。Chrome/Firefox 手機**支援 dvh**，同樣受惠。 |
| `viewport-fit=cover` | 無瀏海/不支援者忽略；不會把內容塞到 Android 導覽列底下（工具列由 `dvh` 處理）。 |
| `env(safe-area-inset-bottom, 0px)` | 無安全區（多數 Android、桌機）回傳 fallback **0px** → `calc` 結果回到 64px / 88px、`padding-bottom` 為 0，等同未加。 |
| icon-only `@media (max-width: 540px)` | 純 CSS media query，全瀏覽器一致;寬螢幕不觸發。 |
| `setPlayBtn()` / span 結構 | `querySelector`、`classList`、`textContent` 為標準 API，全瀏覽器支援。 |

結論：所有新增皆有 fallback，**在不支援的瀏覽器上等於回到原始行為**，不會比原本差。

---

## 附帶變更（可選）：播放鍵 CTA 脈動光環

非手機專屬，但同批加入，列此供 skill 維護者決定是否納入。未播放時，播放鍵有琥珀色呼吸光環提示去按;`setPlayBtn()` 會切換 `.is-playing` 來開關。

```css
@keyframes ctaPulse {
  0%   { box-shadow: 0 0 8px 2px rgba(216,162,74,0.55), 0 0 0 0 rgba(216,162,74,0.55); }
  70%  { box-shadow: 0 0 11px 3px rgba(216,162,74,0.40), 0 0 0 14px rgba(216,162,74,0); }
  100% { box-shadow: 0 0 8px 2px rgba(216,162,74,0.55), 0 0 0 0 rgba(216,162,74,0); }
}
#playBtn:not(.is-playing) { animation: ctaPulse 1.5s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) {
  #playBtn:not(.is-playing) { animation: none; box-shadow: 0 0 10px 2px rgba(216,162,74,0.55); }
}
```

> **可攜性提醒**：上面顏色 `rgba(216,162,74,…)` 是寫死的琥珀（本案 reunion 主題色）。要納入 skill（多主題）建議參數化，例如各主題定義 `--glow: 216,162,74;` 再用 `rgba(var(--glow), .55)`，或改用既有的強調色變數，以免在其他主題下色調不搭。

---

## 驗證

以 Playwright 三引擎、手機視窗（含 375 / 390 / 430px 直式）與桌機 1280px 實測：

| 引擎 | 控制列可見 | 橫向溢出 | 手機 icon-only | icon 尺寸 | Console 錯誤 |
|---|---|---|---|---|---|
| Blink（Chrome/Edge） | ✅ | 無 | ✅ 中文隱藏 | 22px | 無 |
| WebKit（Safari） | ✅ | 無 | ✅ 中文隱藏 | 22px | 無 |
| Gecko（Firefox） | ✅ | 無 | ✅ 中文隱藏 | 22px | 無 |

桌機：按鈕維持「icon + 中文」並排，與變更前一致。

> 註：headless 引擎無法重現 iOS Safari 動態工具列與真實 `safe-area-inset` 值;`dvh`/`env()`/flex 的渲染正確性已於 WebKit 驗證,**動態工具列與瀏海安全區建議於實機 iPhone Safari 最終確認**。

---

## 套用 checklist（給 skill 更新）

- [x] `templates/player.html.tmpl`：四顆按鈕 HTML 改為 `ticon`/`tlabel` 雙 span。
- [x] 同檔 JS：新增 `setPlayBtn()`;`play()`、`pause()`、`advance()` 結束分支改呼叫它。
- [x] CSS：`.btn .ticon` / `.btn .tlabel` 基本樣式 + `@media (max-width:540px)` 控制列「icon 按鈕 + 時間」佈局（移除 `.tlabel`/`.scene-chip`/`.no-audio-note` 文字、`flex-shrink:0`、時間 `nowrap`；控制列用 `padding-left/right`，勿用 shorthand）。
- [x] CSS：`#stage` 加 `height:100dvh`（保留 `100vh` 在前）。
- [x] `<meta viewport>` 加 `viewport-fit=cover`;`.controls` 高度與 `padding-bottom`、`.subtitle-bar` 的 `bottom` 套用 `env(safe-area-inset-bottom, 0px)`。
- [x] CTA 脈動:寫死的琥珀色已改為主題變數 `--glow`（預設 = `--warn`，主題可覆寫）。
- [ ] 實機 iPhone Safari 驗收控制列與安全區（headless 無法重現動態工具列與真實 safe-area，仍需實機）。
