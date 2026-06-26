# narrated-deck — 開工前必讀

## 先決條件：一開始就要有一把 TTS API key

本 plugin 的 Phase 4（TTS）會**實際花錢**呼叫語音合成服務，沒有金鑰會直接失敗。**在動手寫旁白之前**，請先確認使用者手上有下列其中一把 key，並把它設成對應的環境變數：

| 服務 | 用途 | 環境變數名稱（規定） | 金鑰格式 | 取得方式 |
| --- | --- | --- | --- | --- |
| **Voai.ai**（預設，繁中最佳） | zh-TW / zh-CN 旁白 | `VOAI_API_KEY` | `iq-...` 開頭 | https://voai.ai （API 文件：https://www.voai.ai/api） |
| **ElevenLabs**（多語／英文備援） | en / ja 或多語 | `ELEVENLABS_API_KEY` | `sk_...` 開頭 | https://elevenlabs.io/app/developers/api-keys |

**請使用者擇一提供**：

- 直接把金鑰**貼在 chat 裡**（例如「我的 voai key 是 iq-xxxx」），或
- 到 **https://voai.ai** 申請一把 Voai API key（繁中內容建議走這條），或
- 到 **https://elevenlabs.io/app/developers/api-keys** 申請一把 ElevenLabs API key（多語／英文內容）。

### 注意事項

- 環境變數名稱**必須完全相符**（`VOAI_API_KEY` / `ELEVENLABS_API_KEY`），腳本是用這兩個名字讀取的，拼錯會讀不到。
- 金鑰用「環境變數前綴」的方式帶入指令，**不要寫死在任何檔案裡、也不要 commit 進 git**（避免外洩）。
- 若使用者尚未提供金鑰，**先停下來詢問**，不要自行假造或猜測金鑰。

> 這份備忘對應 `skills/narrated-deck/SKILL.md` 的 **Phase 0 — prerequisites & intake**，該處會在流程一開始強制做這項檢查。
