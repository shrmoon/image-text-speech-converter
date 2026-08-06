"""
main.py

End-to-end demo of the full project pipeline:

    Image  --(OCR)-->  Text file  --(TTS)-->  Speech audio

Usage:
    python main.py path/to/image.jpg
    python main.py path/to/image.jpg --dest-lang es
"""

import argparse
from pathlib import Path

from image_to_text import image_to_text_file
from text_to_speech import text_file_to_speech


def run_pipeline(image_path: str, dest_lang: str = None) -> None:
    print(f"[main] Starting pipeline for: {image_path}")

    # Step 1: Image -> Text
    txt_path = image_to_text_file(image_path)

    # Step 2: Text -> Speech
    audio_path = text_file_to_speech(txt_path, dest_lang=dest_lang)

    print("[main] Pipeline complete.")
    print(f"  Text file : {txt_path}")
    print(f"  Audio file: {audio_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image -> Text -> Speech pipeline")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("-d", "--dest-lang", help="Translate extracted text to this language before speaking", default=None)
    args = parser.parse_args()

    run_pipeline(args.image, args.dest_lang)
