"""
Stage 2: convert the cleaned photo into a self-drawing ASCII SVG.
Usage: python tools/render_portrait.py
Reads: assets/photo-ready.png
Writes: portrait.svg
"""
import os
import numpy as np
from PIL import Image

GLYPHS = " '.,:;~+*xXO#"  # left = light/empty, right = dense/dark
ACCENT = "#58a6ff"        # single accent color — keep it monochrome
COLS = 70                 # character grid width; rows derived from cropped aspect ratio
CHAR_W = 6.2
CHAR_H = 11
ROW_DELAY = 0.04          # stagger between rows, seconds

def autocrop_to_subject(img, threshold=245, pad_frac=0.06):
    """Crop tight to the non-near-white region (the subject), with a small padding margin."""
    arr = np.array(img)
    mask = arr < threshold  # True where content is (not near-white background)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return img
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    pad_x = int((x1 - x0) * pad_frac)
    pad_y = int((y1 - y0) * pad_frac)
    x0 = max(0, x0 - pad_x)
    y0 = max(0, y0 - pad_y)
    x1 = min(img.width, x1 + pad_x)
    y1 = min(img.height, y1 + pad_y)
    return img.crop((x0, y0, x1, y1))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    img_path = os.path.join(repo_root, "assets", "photo-ready.png")

    img = Image.open(img_path).convert("L")  # grayscale
    img = autocrop_to_subject(img)
    w, h = img.size
    print(f"cropped to subject: {w}x{h}")
    # character cells are taller than wide, so compress rows accordingly
    rows = int(COLS * (h / w) * (CHAR_W / CHAR_H))
    small = img.resize((COLS, rows))
    pixels = list(small.getdata())

    grid = []
    for r in range(rows):
        row_chars = []
        for c in range(COLS):
            brightness = pixels[r * COLS + c]  # 0=black, 255=white
            # invert: dark pixel -> dense glyph
            idx = int((255 - brightness) / 255 * (len(GLYPHS) - 1))
            row_chars.append(GLYPHS[idx])
        grid.append("".join(row_chars))

    svg_w = COLS * CHAR_W + 20
    svg_h = rows * CHAR_H + 20

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w:.0f} {svg_h:.0f}" width="{svg_w:.0f}" height="{svg_h:.0f}">')
    svg.append(f'''
<style>
  .bg {{ fill: #0d1117; }}
  .row text {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: {CHAR_H-1}px; fill: {ACCENT}; white-space: pre; }}
</style>
<rect class="bg" x="0" y="0" width="{svg_w:.0f}" height="{svg_h:.0f}" rx="8"/>
''')

    for r, row in enumerate(grid):
        y = 14 + r * CHAR_H
        delay = r * ROW_DELAY
        escaped = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg.append(
            f'<g class="row"><clipPath id="clip{r}"><rect x="10" y="{y-CHAR_H+2}" width="0" height="{CHAR_H}">'
            f'<animate attributeName="width" from="0" to="{COLS*CHAR_W:.0f}" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="10" y="{y}" clip-path="url(#clip{r})">{escaped}</text></g>'
        )

    svg.append('</svg>')

    out_path = os.path.join(repo_root, "portrait.svg")
    with open(out_path, "w") as f:
        f.write("\n".join(svg))
    print(f"wrote {out_path} ({COLS}x{rows} chars)")

if __name__ == "__main__":
    main()
