"""
Stage 1: clean a raw photo for ASCII conversion.
Usage: python tools/clean_photo.py my-photo.jpg
Writes: assets/photo-ready.png
"""
import sys
import os
import numpy as np
import cv2
from rembg import remove
from PIL import Image

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/clean_photo.py <input-photo>")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    input_path = sys.argv[1]
    out_path = os.path.join(repo_root, "assets", "photo-ready.png")

    # 1. Remove background
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    output_bytes = remove(input_bytes)

    subject = Image.open(__import__("io").BytesIO(output_bytes)).convert("RGBA")

    # 2. CLAHE lighting correction on the RGB channels
    arr = np.array(subject)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    lab2 = cv2.merge((l2, a, b))
    rgb2 = cv2.cvtColor(lab2, cv2.COLOR_LAB2RGB)

    # 3. Composite onto white canvas using the alpha mask
    white_bg = np.full_like(rgb2, 255)
    alpha_f = (alpha.astype(np.float32) / 255.0)[:, :, None]
    composited = (rgb2.astype(np.float32) * alpha_f + white_bg.astype(np.float32) * (1 - alpha_f)).astype(np.uint8)

    result = Image.fromarray(composited, mode="RGB")
    result.save(out_path)
    print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
