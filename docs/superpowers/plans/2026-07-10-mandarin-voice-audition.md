# 中文旁白聲音試聽實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 使用 Kokoro 的八個中文普通話聲音，產生並驗證公平、可供使用者挑選的八段台灣用詞旁白試聽 WAV。

**Architecture:** 一個產生器固定文字、取樣率與 `lang_code='z'`，只迭代聲音 ID，將 WAV 寫到獨立的 `mandarin-voices/` 子資料夾。驗證器讀取每一檔的音訊中繼資料與浮點取樣值，拒絕空白、靜音或格式不符的輸出，並寫出 JSON 報告。

**Tech Stack:** Python 3.11、Kokoro 0.9.4、NumPy、SoundFile。

## 全域限制

- 使用 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python`；不得修改既有 Manim 環境。
- 只使用本機 Kokoro 與既有快取模型，不使用 API 金鑰或雲端 TTS。
- 八個聲音為 `zf_xiaobei`、`zf_xiaoni`、`zf_xiaoxiao`、`zf_xiaoyi`、`zm_yunjian`、`zm_yunxi`、`zm_yunxia`、`zm_yunyang`。
- 每個輸出都是單聲道、24,000 Hz、16-bit PCM WAV，且使用完全相同的文字。
- 不把任何輸出標示為保證的台灣華語口音；此試聽僅供比較自然度、音色與台灣用詞的可懂度。
- `/Users/lichengen/Developer/Senior-project/animation/` 不是 Git 工作樹；生成器、WAV 與驗證報告皆不提交。

---

### Task 1: 建立八聲音試聽產生器

**Files:**
- Create: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_mandarin_voice_samples.py`
- Test: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/zf_xiaobei.wav`

**Interfaces:**
- Consumes: 已安裝 Kokoro 的 `.tts-env/bin/python` 與 `KPipeline(lang_code='z')`。
- Produces: `mandarin-voices/<voice_id>.wav`，每檔對應一個固定的 Kokoro 聲音 ID。

- [ ] **Step 1: 確認首個預期輸出尚不存在**

Run:

```bash
test ! -e /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/zf_xiaobei.wav
```

Expected: 結束狀態為 `0`，因為尚未開始產生八聲音試聽。

- [ ] **Step 2: 建立最小產生器**

建立 `/Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_mandarin_voice_samples.py`，內容如下：

```python
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


SAMPLE_RATE = 24_000
TEXT = "二分搜尋會在已排序的範圍中反覆對半縮小。它會排除不可能包含目標值的那一半，因此能快速找到目標。"
VOICES = (
    "zf_xiaobei",
    "zf_xiaoni",
    "zf_xiaoxiao",
    "zf_xiaoyi",
    "zm_yunjian",
    "zm_yunxi",
    "zm_yunxia",
    "zm_yunyang",
)


def synthesize(output_dir: Path, voice: str) -> Path:
    pipeline = KPipeline(lang_code="z")
    chunks = [audio for _, _, audio in pipeline(TEXT, voice=voice)]
    if not chunks:
        raise RuntimeError(f"Kokoro produced no audio for {voice}")
    audio = np.concatenate(chunks)
    if audio.size == 0:
        raise RuntimeError(f"Kokoro produced empty audio for {voice}")
    output_path = output_dir / f"{voice}.wav"
    sf.write(output_path, audio, SAMPLE_RATE, subtype="PCM_16")
    return output_path


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "mandarin-voices"
    output_dir.mkdir(parents=True, exist_ok=True)
    for voice in VOICES:
        print(synthesize(output_dir, voice))


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 執行產生器並檢查八個路徑**

Run:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python /Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_mandarin_voice_samples.py
find /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices -maxdepth 1 -name '*.wav' -type f | wc -l
```

Expected: 依序印出八個 WAV 絕對路徑，最後輸出 `8`。

### Task 2: 驗證並交付聲音比較結果

**Files:**
- Verify: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/*.wav`
- Create: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/validation.json`

**Interfaces:**
- Consumes: Task 1 的八個 `PCM_16` WAV。
- Produces: 每個聲音 ID 的時長、取樣率、聲道數、peak 與 RMS 音量；任一檔不符合條件即失敗。

- [ ] **Step 1: 執行八檔格式與非靜音驗證**

Run:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python -c "import json,numpy as np,soundfile as sf; from pathlib import Path; root=Path('/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices'); voices=('zf_xiaobei','zf_xiaoni','zf_xiaoxiao','zf_xiaoyi','zm_yunjian','zm_yunxi','zm_yunxia','zm_yunyang'); report={};
for voice in voices:
 p=root/(voice+'.wav'); info=sf.info(p); samples,_=sf.read(p,dtype='float32'); peak=float(np.max(np.abs(samples))); rms=float(np.sqrt(np.mean(np.square(samples)))); item={'duration_seconds':round(info.duration,3),'sample_rate':info.samplerate,'channels':info.channels,'subtype':info.subtype,'peak':round(peak,6),'rms':round(rms,6)}; assert item['sample_rate']==24000 and item['channels']==1 and item['subtype']=='PCM_16' and item['duration_seconds']>0.5 and item['peak']>0.015 and item['rms']>0.0015, {voice:item}; report[voice]=item
(root/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\\n'); print(json.dumps(report,ensure_ascii=False))"
```

Expected: 結束狀態為 `0`；報告包含全部八個聲音，且每一項都符合取樣率、聲道、PCM 子類型、時長及非靜音門檻。

- [ ] **Step 2: 檢查輸出清單與驗證報告**

Run:

```bash
ls -lh /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/*.wav /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/validation.json
```

Expected: 八個非零大小 WAV 與一個 `validation.json` 都存在。

- [ ] **Step 3: 交給使用者選擇預設聲音**

提供八個音檔的絕對路徑與聲音 ID 對照，請使用者選出一個 ID 作為後續中文旁白預設。使用者未選定前，不修改正式 `VOICEOVER` 的預設聲音。
