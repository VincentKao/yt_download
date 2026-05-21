#!/usr/bin/env python3
"""
MP3 → 逐字稿（使用 faster-whisper large-v3）

使用方式：
  python mp3_to_transcript.py                     # 處理當前目錄所有 MP3
  python mp3_to_transcript.py "file.mp3"          # 指定單一檔案
  python mp3_to_transcript.py -l ko               # 強制指定語言（zh/ko/en）
  python mp3_to_transcript.py -t                  # 逐字稿 + 翻譯成英文
  python mp3_to_transcript.py --skip-existing     # 跳過已有逐字稿的檔案
"""

import subprocess
import sys
import argparse
from pathlib import Path


def check_faster_whisper() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def install_faster_whisper():
    print("未偵測到 faster-whisper，自動安裝中...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "faster-whisper", "--break-system-packages"],
        check=True
    )
    print("faster-whisper 安裝完成！\n")


def load_model():
    from faster_whisper import WhisperModel
    print("載入模型 large-v3（首次執行會下載約 3.1 GB）...")
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    print("模型載入完成！\n")
    return model


def transcribe_file(model, mp3_path: Path, language: str = None, translate: bool = False) -> str:
    task = "translate" if translate else "transcribe"

    print(f"轉錄中：{mp3_path.name}")
    segments, info = model.transcribe(
        str(mp3_path),
        language=language,
        task=task,
        beam_size=5,
        vad_filter=True,          # 過濾靜音段落
        vad_parameters={"min_silence_duration_ms": 500},
    )

    detected = info.language
    confidence = info.language_probability
    print(f"  偵測語言：{detected}（信心度 {confidence:.0%}）")

    lines = []
    for segment in segments:
        start = f"{int(segment.start // 60):02d}:{segment.start % 60:05.2f}"
        end   = f"{int(segment.end   // 60):02d}:{segment.end   % 60:05.2f}"
        lines.append(f"[{start} → {end}] {segment.text.strip()}")

    return "\n".join(lines)


def process_file(model, mp3_path: Path, language: str, translate: bool, skip_existing: bool):
    output_path = mp3_path.with_suffix(".txt")

    if skip_existing and output_path.exists():
        print(f"跳過（已有逐字稿）：{mp3_path.name}")
        return

    transcript = transcribe_file(model, mp3_path, language=language, translate=translate)
    output_path.write_text(transcript, encoding="utf-8")
    print(f"  ✅ 儲存至：{output_path.name}\n")


def main():
    parser = argparse.ArgumentParser(description="MP3 轉逐字稿（faster-whisper large-v3）")
    parser.add_argument(
        "input", nargs="?", default=".",
        help="MP3 檔案路徑或資料夾（預設：當前目錄）"
    )
    parser.add_argument(
        "--language", "-l", default=None,
        help="語言代碼（zh / ko / en），不填則自動偵測"
    )
    parser.add_argument(
        "--translate", "-t", action="store_true",
        help="將音訊翻譯成英文（僅支援輸出英文）"
    )
    parser.add_argument(
        "--skip-existing", "-s", action="store_true",
        help="跳過已存在 .txt 逐字稿的檔案"
    )
    args = parser.parse_args()

    if not check_faster_whisper():
        install_faster_whisper()

    input_path = Path(args.input)

    if input_path.is_file():
        if input_path.suffix.lower() != ".mp3":
            print(f"錯誤：不是 MP3 檔案：{input_path}")
            sys.exit(1)
        mp3_files = [input_path]
    elif input_path.is_dir():
        mp3_files = sorted(input_path.glob("*.mp3"))
        if not mp3_files:
            print(f"找不到 MP3 檔案：{input_path}")
            sys.exit(1)
        print(f"找到 {len(mp3_files)} 個 MP3 檔案\n")
    else:
        print(f"路徑不存在：{args.input}")
        sys.exit(1)

    model = load_model()

    for mp3 in mp3_files:
        process_file(
            model, mp3,
            language=args.language,
            translate=args.translate,
            skip_existing=args.skip_existing,
        )

    print(f"全部完成，共處理 {len(mp3_files)} 個檔案。")


if __name__ == "__main__":
    main()
