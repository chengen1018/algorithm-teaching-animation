# Kokoro TTS 環境設置說明

這份說明是給**人類使用者**在第一次使用此 skill 之前看的，用來幫你把 Kokoro TTS 的環境準備好。
設置只需要做一次，之後每個動畫製作都會共用這個環境。

---

## 你需要準備的東西

- Python 3.10、3.11 或 3.12（**不能用系統預設的 Python 3.9 或更舊的版本**）
- 網路連線（第一次使用時 Kokoro 會自動下載模型，之後就可以離線使用）

---

## 步驟一：確認 Python 版本

打開終端機，執行：

```bash
python3 --version
```

如果版本低於 3.10，需要另外安裝 Python 3.11：

- **macOS**：用 Homebrew 安裝
  ```bash
  brew install python@3.11
  ```
- **Windows**：從 [python.org](https://www.python.org/downloads/) 下載 3.11 安裝包

---

## 步驟二：建立專用虛擬環境

建議把這個環境放在**動畫專案資料夾之外**的地方（例如 `~/Developer/Senior-project/animation/`），讓多個動畫專案可以共用，也避免和 Manim 環境互相干擾。

```bash
# macOS / Linux（使用剛安裝的 Python 3.11）
python3.11 -m venv /你選定的路徑/.tts-env

# Windows
py -3.11 -m venv C:\你選定的路徑\.tts-env
```

---

## 步驟三：進入環境並安裝套件

```bash
# macOS / Linux
source /你選定的路徑/.tts-env/bin/activate

# Windows
C:\你選定的路徑\.tts-env\Scripts\activate
```

進入環境後，安裝所需套件：

```bash
pip install kokoro==0.9.4
pip install torch
pip install misaki[en,zh]
pip install numpy soundfile
```

安裝過程大約需要幾分鐘，請耐心等待。

---

## 步驟四：確認環境可以正常使用

在已啟動的虛擬環境中，執行以下指令來快速驗證：

```python
python -c "from kokoro import KPipeline; print('Kokoro OK')"
```

看到 `Kokoro OK` 就表示安裝成功。

---

## 步驟五：告訴 Skill 你的環境路徑

在你的動畫專案根目錄下建立 `.tts-config` 檔案（此檔案不會被 git 追蹤），寫入你的虛擬環境 Python 路徑：

```
# .tts-config
TTS_PYTHON=/你選定的路徑/.tts-env/bin/python
```

**Windows 範例：**
```
TTS_PYTHON=C:\你選定的路徑\.tts-env\Scripts\python.exe
```

Skill 的 Agent 在執行 TTS 時會讀取這個設定，確保使用正確的 Python 環境。

---

## 預設聲音

此 skill 預設使用以下聲音，無需額外設定：

| 語言 | 聲音 ID | 語言代碼 |
|------|---------|---------|
| 英文 | `af_heart` | `a` |
| 中文（普通話）| `zm_yunxi` | `z` |

---

## 注意事項

- **不要**把這個環境和 Manim 的環境混在一起。
- **不要**在 Skill 的執行腳本裡使用系統的 `python3`，一定要用虛擬環境的 Python。
- Kokoro 是本機推論，文字不會傳送到任何雲端，也沒有 API 金鑰或費用。
- 第一次使用某個聲音時會自動下載模型，之後就快取在本機，不再需要網路。
