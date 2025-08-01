"""
Generate a 500x500 PNG avatar from the Feldroy SVG logo for GitHub profile upload.

- Converts 'feldroy-logo-square.svg' to 'feldroy-github-avatar.png' at 500x500 px.
- Optimizes the PNG using Pillow's built-in optimizer.
- Output is suitable for GitHub profile images (PNG, <1MB, 500x500 recommended).

If you get errors about missing 'cairo' libraries on macOS, ensure you have run:
    brew install cairo libffi
and set environment variables if needed:
    export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig"
    export DYLD_LIBRARY_PATH="/opt/homebrew/lib"
and install cairosvg and pillow into your virtual environment:
    uv pip install cairosvg pillow
"""

import sys
from pathlib import Path
import cairosvg
from PIL import Image

SVG_FILE = "static/feldroy-logo-square.svg"
OUTPUT_SIZE = 500  # px, for GitHub avatar
OUTPUT_FILE = "feldroy-github-avatar.png"

if __name__ == "__main__":
    svg_path = Path(SVG_FILE)
    if not svg_path.exists():
        print(f"SVG file not found: {SVG_FILE}")
        sys.exit(1)
    png_path = svg_path.with_name(OUTPUT_FILE)
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=OUTPUT_SIZE, output_height=OUTPUT_SIZE)
    # TODO: consider using optipng instead of or in addition to Pillow
    with Image.open(png_path) as im:
        im.save(png_path, "PNG", optimize=True)
    print(f"Generated {OUTPUT_FILE} ({OUTPUT_SIZE}x{OUTPUT_SIZE}) for GitHub avatar upload.")
