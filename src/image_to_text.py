"""
image_to_text.py

Image -> Text conversion module.

Implements the pipeline described in the project report:
    1. Input image (from file or camera capture)
    2. Pre-processing (grayscale + noise removal, works on both plain
       and colored/noisy backgrounds)
    3. Feature extraction / character recognition via Tesseract OCR
       (through the pytesseract wrapper)
    4. Text generation, saved to a .txt file

Dependencies: pillow, pytesseract, and the Tesseract OCR engine itself
must be installed on the system (see README.md).
"""

from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
import pytesseract


def preprocess_image(image_path: str) -> Image.Image:
    """
    Prepares an input image for OCR.

    Converts to grayscale, applies a light denoise filter, and
    increases contrast so that both plain-background text and
    colored/noisy-background text can be recognized reliably.
    """
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Reduce noise
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Auto-contrast to sharpen character edges
    img = ImageOps.autocontrast(img)

    return img


def extract_text(image_path: str, lang: str = "eng") -> str:
    """
    Runs OCR on the given image and returns the extracted text.
    """
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed, lang=lang)
    return text.strip()


def image_to_text_file(image_path: str, output_path: str = None, lang: str = "eng") -> str:
    """
    Extracts text from an image and writes it to a .txt file.

    Returns the path to the generated text file.
    """
    text = extract_text(image_path, lang=lang)

    if output_path is None:
        output_path = str(Path(image_path).with_suffix(".txt"))

    Path(output_path).write_text(text, encoding="utf-8")
    print(f"[image_to_text] Extracted {len(text)} characters -> {output_path}")

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert an image containing text into a .txt file.")
    parser.add_argument("image", help="Path to the input image (png, jpg, bmp, tiff, etc.)")
    parser.add_argument("-o", "--output", help="Path to the output .txt file", default=None)
    parser.add_argument("-l", "--lang", help="Tesseract language code", default="eng")
    args = parser.parse_args()

    image_to_text_file(args.image, args.output, args.lang)
