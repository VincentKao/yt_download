# yt_download

將 YouTube 影片下載並轉換為 MP3 音訊檔的 Python 腳本。

## 需求

- Python 3
- [FFmpeg](https://ffmpeg.org/)（音訊轉換必要）
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（腳本會自動安裝）

安裝 FFmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

## 使用方式

1. 開啟 `youtube_to_mp3.py`，修改底部的兩個變數：

```python
VIDEO_URL  = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"  # YouTube 影片網址
OUTPUT_DIR = "."  # 儲存目錄，"." 表示當前資料夾
```

2. 執行腳本：

```bash
python youtube_to_mp3.py
```

若尚未安裝 `yt-dlp`，腳本會自動安裝（macOS 使用 Homebrew，其他系統使用 pip）。

## 輸出

- 格式：MP3
- 音質：192 kbps
- 檔名：以 YouTube 影片標題命名
