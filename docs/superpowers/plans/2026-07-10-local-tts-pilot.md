# 本機 TTS 試用實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在共用的 `animation/` 根目錄建立免 API 金鑰的 Kokoro 本機 TTS 環境，並產生可聆聽、可驗證的英文與中文普通話試聽檔。

**Architecture:** 共用依賴安裝在 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/`，不觸及既有 Manim 環境。試用產生器只寫入 `/Users/lichengen/Developer/Senior-project/animation/tts-samples/`；它用固定的語言、聲音與文字生成兩個 24 kHz PCM WAV，再由獨立驗證器拒絕空白或實質靜音輸出。

**Tech Stack:** Python 3、`venv`、Kokoro 0.9.4、Misaki 英文與中文擴充、NumPy、SoundFile。

## 全域限制

- 共用環境必須位於 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/`；不得修改 `/Users/lichengen/Developer/Senior-project/algorithm-teaching-animation/.manim-env/`。
- 不得使用 API 金鑰、雲端 TTS 或作業系統內建語音。
- 英文試聽使用 Kokoro `lang_code='a'` 與 `af_heart`；中文普通話試聽使用 `lang_code='z'` 與 `zf_xiaobei`。
- 每個輸出必須是單聲道、24,000 Hz、16-bit PCM WAV，且可被標準函式庫解碼。
- 若模型下載、套件安裝、合成或驗證任何一步失敗，停止試用並回報錯誤；絕不以靜音檔替代。
- `/Users/lichengen/Developer/Senior-project/animation/` 不是 Git 工作樹；其中的環境、模型快取、試聽 WAV 與試用腳本均不提交。本計畫檔才是可追溯的工作紀錄。

---

### Task 1: 建立隔離的共用 TTS 環境

**Files:**
- Create: `/Users/lichengen/Developer/Senior-project/animation/.tts-env/`
- Verify: `/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python`

**Interfaces:**
- Consumes: 使用者已存在的 `/Users/lichengen/Developer/Senior-project/animation/` 資料夾與系統 `python3`。
- Produces: 可由後續任務以 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python` 呼叫的獨立 Python 環境。

- [ ] **Step 1: 確認目標資料夾與 Python 版本**

Run:

```bash
test -d /Users/lichengen/Developer/Senior-project/animation
python3 --version
```

Expected: 第一個指令結束狀態為 `0`；Python 顯示 `3.9` 或以上版本。

- [ ] **Step 2: 建立虛擬環境**

Run:

```bash
python3 -m venv /Users/lichengen/Developer/Senior-project/animation/.tts-env
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python -m pip install --upgrade pip
```

Expected: `.tts-env/bin/python` 存在，且 pip 升級成功；既有 `.manim-env` 未被讀取或寫入。

- [ ] **Step 3: 安裝固定的本機 TTS 相依套件**

Run:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python -m pip install "kokoro==0.9.4" "misaki[en,zh]" "soundfile==0.13.1"
```

Expected: pip 結束狀態為 `0`；Kokoro、中文／英文發音支援與 WAV 寫入套件皆安裝在 `.tts-env`。

- [ ] **Step 4: 驗證兩個語言 pipeline 均可建立**

Run:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python -c "from kokoro import KPipeline; KPipeline(lang_code='a'); KPipeline(lang_code='z'); print('Kokoro English and Mandarin pipelines ready')"
```

Expected: 輸出 `Kokoro English and Mandarin pipelines ready`，結束狀態為 `0`。

### Task 2: 寫入可重複執行的試聽產生器

**Files:**
- Create: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_samples.py`
- Create: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/README.md`
- Test: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_samples.py`

**Interfaces:**
- Consumes: Task 1 的 `.tts-env/bin/python`，以及 `kokoro.KPipeline(text, voice)` 產生的 float 音訊區塊。
- Produces: `english.wav`、`mandarin.wav`，以及可重複執行、不依賴 API 金鑰的試聽指令。

- [ ] **Step 1: 寫入會先失敗的輸出存在性檢查**

在尚未產生音檔前執行：

```bash
test -f /Users/lichengen/Developer/Senior-project/animation/tts-samples/english.wav && test -f /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin.wav
```

Expected: 結束狀態非 `0`，因為兩個試聽檔尚不存在。

- [ ] **Step 2: 建立試聽產生器**

建立 `/Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_samples.py`，內容如下：

```python
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


SAMPLE_RATE = 24_000
SAMPLES = (
    (
        "english.wav",
        "a",
        "af_heart",
        "Binary search repeatedly halves a sorted range. It quickly finds the target by discarding the half that cannot contain it.",
    ),
    (
        "mandarin.wav",
        "z",
        "zf_xiaobei",
        "二元搜尋會在已排序的範圍中反覆對半縮小。它會排除不可能包含目標值的那一半，因此能快速找到目標。",
    ),
)


def synthesize(output_dir: Path, language: str, voice: str, text: str, filename: str) -> Path:
    pipeline = KPipeline(lang_code=language)
    chunks = [audio for _, _, audio in pipeline(text, voice=voice)]
    if not chunks:
        raise RuntimeError(f"Kokoro produced no audio for {filename}")
    audio = np.concatenate(chunks)
    if audio.size == 0:
        raise RuntimeError(f"Kokoro produced empty audio for {filename}")
    output_path = output_dir / filename
    sf.write(output_path, audio, SAMPLE_RATE, subtype="PCM_16")
    return output_path


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, language, voice, text in SAMPLES:
        output_path = synthesize(output_dir, language, voice, text, filename)
        print(output_path)


if __name__ == "__main__":
    main()
```

建立 `README.md`，內容如下：

```markdown
# Kokoro 試聽

以共用環境產生英文與中文普通話 WAV：

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python /Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_samples.py
```

輸出為 `english.wav` 與 `mandarin.wav`。此工具只作聲音品質試用；正式動畫旁白須在各動畫子資料夾的 `audio/voiceover/` 中產生。
```

- [ ] **Step 3: 執行產生器**

Run:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python /Users/lichengen/Developer/Senior-project/animation/tts-samples/generate_samples.py
```

Expected: 依序印出 `english.wav` 與 `mandarin.wav` 的絕對路徑，兩檔均出現在 `tts-samples/`。

### Task 3: 驗證音檔並交付試聽結果

**Files:**
- Verify: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/english.wav`
- Verify: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin.wav`
- Create: `/Users/lichengen/Developer/Senior-project/animation/tts-samples/validation.json`

**Interfaces:**
- Consumes: Task 2 的兩個 24 kHz PCM WAV。
- Produces: 每一檔的時長、聲道數、取樣率、峰值與 RMS 音量；任何靜音、空白或格式錯誤均使此任務失敗。

- [ ] **Step 1: 寫入並執行音訊驗證器**

Run this exact command:

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python -c "import json,numpy as np,soundfile as sf; from pathlib import Path; root=Path('/Users/lichengen/Developer/Senior-project/animation/tts-samples'); report={};
for name in ('english.wav','mandarin.wav'):
 p=root/name; info=sf.info(p); samples,_=sf.read(p,dtype='float32'); peak=float(np.max(np.abs(samples))); rms=float(np.sqrt(np.mean(np.square(samples)))); item={'duration_seconds':round(info.duration,3),'sample_rate':info.samplerate,'channels':info.channels,'subtype':info.subtype,'peak':round(peak,6),'rms':round(rms,6)}; assert item['sample_rate']==24000 and item['channels']==1 and item['subtype']=='PCM_16' and item['duration_seconds']>0.5 and item['peak']>0.015 and item['rms']>0.0015, item; report[name]=item
(root/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\\n'); print(json.dumps(report,ensure_ascii=False))"
```

Expected: 結束狀態為 `0`；`validation.json` 包含兩檔各自大於 0.5 秒的時長、`24000` Hz、單聲道、`PCM_16` 與超過靜音門檻的 peak／RMS 音量。

- [ ] **Step 2: 檢查檔案與驗證報告的實際存在性**

Run:

```bash
ls -lh /Users/lichengen/Developer/Senior-project/animation/tts-samples/english.wav /Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin.wav /Users/lichengen/Developer/Senior-project/animation/tts-samples/validation.json
```

Expected: 三個檔案都存在且 WAV 檔大小非零。

- [ ] **Step 3: 交付兩段可聆聽試聽檔**

向使用者提供這兩個檔案的絕對路徑，請使用者分別評估英文與中文的自然度、清晰度、發音與教學旁白適用性：

```text
/Users/lichengen/Developer/Senior-project/animation/tts-samples/english.wav
/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin.wav
```

Expected: 使用者明確接受 Kokoro 的聲音，或指出應更換 provider／聲音；在使用者確認前，不把試用模型整合到 `VOICEOVER` workflow。
