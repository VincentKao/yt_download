#!/usr/bin/env python3
"""
YouTube 影片下載為 MP3
使用方式：python youtube_to_mp3.py
"""

import subprocess
import sys


def check_yt_dlp():
    """檢查 yt-dlp 是否已安裝"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_brew():
    """檢查 Homebrew 是否已安裝"""
    try:
        subprocess.run(["brew", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_yt_dlp():
    """自動安裝 yt-dlp（優先使用 brew，macOS 相容）"""
    import platform
    system = platform.system()

    if system == "Darwin" and check_brew():
        # macOS + Homebrew：使用 brew 安裝（避免 externally-managed-environment 錯誤）
        # 注意：不用 check=True，因為 brew 可能因 symlink 衝突回傳非零，但 yt-dlp 仍安裝成功
        print("偵測到 macOS + Homebrew，使用 brew 安裝 yt-dlp...")
        subprocess.run(["brew", "install", "yt-dlp"])
        # 安裝後再確認是否真的可用
        if not check_yt_dlp():
            print("❌ yt-dlp 安裝後仍無法使用，請手動執行：brew install yt-dlp")
            sys.exit(1)
    else:
        # 其他系統：使用 pip --break-system-packages
        print("正在安裝 yt-dlp（pip）...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "yt-dlp", "--break-system-packages"],
            check=True
        )

    print("yt-dlp 安裝完成！\n")


def download_as_mp3(url: str, output_dir: str = "."):
    """
    使用 yt-dlp 命令列將 YouTube 影片下載為 MP3

    參數:
        url        - YouTube 影片網址
        output_dir - 儲存資料夾路徑（預設為當前目錄）
    """
    command = [
        "yt-dlp",
        "-x",                              # 僅提取音訊
        "--audio-format", "mp3",           # 輸出格式為 mp3
        "--audio-quality", "192K",         # 音質 192kbps
        "-o", f"{output_dir}/%(title)s.%(ext)s",  # 輸出檔名（以影片標題命名）
        url
    ]

    print(f"開始下載：{url}")
    print(f"儲存位置：{output_dir}\n")

    result = subprocess.run(command)

    if result.returncode == 0:
        print("\n✅ 下載完成！MP3 已儲存至：", output_dir)
    else:
        print("\n❌ 下載失敗，請確認網址是否正確，以及 FFmpeg 是否已安裝。")
        print("   macOS 安裝 FFmpeg：brew install ffmpeg")
        print("   Ubuntu 安裝 FFmpeg：sudo apt install ffmpeg")


if __name__ == "__main__":
    # ── 請在這裡修改設定 ──────────────────────────────
    VIDEO_URL  = "https://www.youtube.com/watch?v=-aZ9RQn57bU&t=1s"  # 替換成你想下載的影片網址
    OUTPUT_DIR = "."   # 儲存位置，"." 表示當前目錄，也可改成絕對路徑如 "/Users/你的名字/Downloads"
    # ─────────────────────────────────────────────────

    # 檢查並安裝 yt-dlp
    if not check_yt_dlp():
        print("未偵測到 yt-dlp，嘗試自動安裝...")
        install_yt_dlp()

    download_as_mp3(VIDEO_URL, OUTPUT_DIR)
