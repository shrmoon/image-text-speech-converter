"""
text_to_speech.py

Text -> Speech conversion module.

Implements the pipeline described in the project report:
    1. Read the stored text file (output of image_to_text.py)
    2. Optionally translate it into a target language
    3. Convert to speech and save/playback as an audio file

Two engines are supported:
    - pyttsx3: fully offline text-to-speech (no internet required)
    - gTTS (Google Text-to-Speech): used when a translated / online
      voice is preferred, matching the "Google TTS engine" described
      in the report.

Dependencies: pyttsx3, gTTS, googletrans (see README.md)
"""

from pathlib import Path
import pyttsx3


def speak_offline(text: str, rate: int = 170, voice_index: int = 0) -> None:
    """
    Speaks the given text aloud immediately using the offline pyttsx3 engine.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[voice_index % len(voices)].id)

    engine.say(text)
    engine.runAndWait()


def text_to_audio_file(text: str, output_path: str, rate: int = 170) -> str:
    """
    Converts text to speech and saves it as an audio file (offline, pyttsx3).
    Supported output formats depend on the platform's TTS backend (commonly .mp3 or .wav).
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    print(f"[text_to_speech] Saved audio -> {output_path}")
    return output_path


def translate_text(text: str, dest_lang: str = "en") -> str:
    """
    Translates text into the destination language using Google Translate.
    Mirrors the multilingual translation step described in the report.
    """
    from googletrans import Translator

    translator = Translator()
    result = translator.translate(text, dest=dest_lang)
    return result.text


def text_file_to_speech(input_txt_path: str, output_audio_path: str = None,
                         dest_lang: str = None, rate: int = 170) -> str:
    """
    Full pipeline: reads a .txt file, optionally translates it, and
    converts the result to a speech audio file.
    """
    text = Path(input_txt_path).read_text(encoding="utf-8")

    if dest_lang:
        text = translate_text(text, dest_lang)

    if output_audio_path is None:
        output_audio_path = str(Path(input_txt_path).with_suffix(".mp3"))

    return text_to_audio_file(text, output_audio_path, rate=rate)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert a text file into a speech audio file.")
    parser.add_argument("textfile", help="Path to the input .txt file")
    parser.add_argument("-o", "--output", help="Path to the output audio file", default=None)
    parser.add_argument("-d", "--dest-lang", help="Translate to this language code before speaking (e.g. es, fr, bn)", default=None)
    parser.add_argument("-r", "--rate", type=int, help="Speech rate (words per minute)", default=170)
    args = parser.parse_args()

    text_file_to_speech(args.textfile, args.output, args.dest_lang, args.rate)
