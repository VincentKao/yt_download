# yt_download

將 YouTube 影片下載為 MP3，並使用 faster-whisper large-v3 轉換為逐字稿。

## 需求

- Python 3
- [FFmpeg](https://ffmpeg.org/)（音訊轉換必要）
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（`youtube_to_mp3.py` 會自動安裝）
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)（`mp3_to_transcript.py` 會自動安裝）

安裝 FFmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

---

## 腳本一：YouTube → MP3

### 使用方式

1. 開啟 `youtube_to_mp3.py`，修改底部的兩個變數：

```python
VIDEO_URL  = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
OUTPUT_DIR = "."  # 儲存目錄
```

2. 執行：

```bash
python youtube_to_mp3.py
```

### 輸出

- 格式：MP3，192 kbps
- 檔名：以 YouTube 影片標題命名

---

## 腳本二：MP3 → 逐字稿

使用 [faster-whisper](https://github.com/SYSTRAN/faster-whisper) large-v3 模型，支援中文、英文、韓文等 99 種語言。

> 首次執行會自動下載模型（約 3.1 GB）。

### 使用方式

```bash
# 處理當前目錄所有 MP3
python mp3_to_transcript.py

# 指定單一檔案
python mp3_to_transcript.py "video.mp3"

# 強制指定語言（不指定則自動偵測）
python mp3_to_transcript.py -l zh   # 中文
python mp3_to_transcript.py -l ko   # 韓文
python mp3_to_transcript.py -l en   # 英文

# 翻譯成英文
python mp3_to_transcript.py -t

# 跳過已有逐字稿的檔案
python mp3_to_transcript.py --skip-existing
```

### 輸出

- 每個 MP3 產生對應的 `.txt` 逐字稿
- 每行格式：`[mm:ss.ss → mm:ss.ss] 內容`
- 啟用 VAD 過濾，自動跳過靜音段落
