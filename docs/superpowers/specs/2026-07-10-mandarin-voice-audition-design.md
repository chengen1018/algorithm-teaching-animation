# 中文旁白聲音試聽設計

## 目的

讓使用者從 Kokoro 現有的八個中文普通話聲音中，選出最適合教學影片的聲線。此試聽只比較音色、清晰度、節奏與使用台灣常用詞時的自然度；不宣稱任何聲音保證具有台灣華語口音。

## 範圍與輸出

- 使用相同的繁體中文、台灣常用詞文字，為每個聲音產生一個獨立 WAV。
- 試聽文字：`二分搜尋會在已排序的範圍中反覆對半縮小。它會排除不可能包含目標值的那一半，因此能快速找到目標。`
- 聲音清單：`zf_xiaobei`、`zf_xiaoni`、`zf_xiaoxiao`、`zf_xiaoyi`、`zm_yunjian`、`zm_yunxi`、`zm_yunxia`、`zm_yunyang`。
- 輸出資料夾：`/Users/lichengen/Developer/Senior-project/animation/tts-samples/mandarin-voices/`。
- 檔名以聲音 ID 命名，例如 `zf_xiaobei.wav`。

## 固定條件

- 使用既有 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/` 中的 Kokoro 0.9.4、`lang_code='z'` 與本機模型；不使用 API 金鑰或雲端 TTS。
- 每個輸出為單聲道、24,000 Hz、16-bit PCM WAV。
- 所有聲音使用完全相同的文字、取樣率與生成流程，確保比較公平。
- 每一檔都必須通過可解碼、非空、非靜音及時長大於 0.5 秒的驗證。

## 判讀與後續

使用者聆聽所有八檔後，選擇一個固定聲音 ID 作為後續中文旁白的預設。若沒有任何聲音足夠接近台灣華語，再另行評估具台灣華語訓練資料的本機模型；不把 Kokoro 的一般中文聲線誤標為台灣口音。
