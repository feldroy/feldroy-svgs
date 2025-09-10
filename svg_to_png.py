#!/usr/bin/env uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "cairosvg",
#   "pillow",
#   "typer",
# ]
# ///

"""
Convert an SVG file to PNG at specified size.

- Converts 'feldroy-logo-square.svg' to 'feldroy-logo-square.png' at specified size.
- Optimizes the PNG using Pillow's built-in optimizer.

Usage:
    uv run svg_to_png.py --size 500  # Default size
    uv run svg_to_png.py --size 2800

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
import typer

app = typer.Typer()

SVG_FILE = "static/feldroy-logo-square.svg"

@app.command()
def generate(
    size: int = typer.Option(500, help="Size of the output image in pixels (width and height)")
):
    """
    Generate a PNG from the SVG file.
    """
    svg_path = Path(SVG_FILE)
    if not svg_path.exists():
        typer.echo(f"SVG file not found: {SVG_FILE}")
        sys.exit(1)
    png_path = svg_path.with_suffix('.png')
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=size, output_height=size)
    # TODO: consider using optipng instead of or in addition to Pillow
    with Image.open(png_path) as im:
        im.save(png_path, "PNG", optimize=True)
    typer.echo(f"Generated {png_path.name} ({size}x{size}).")

if __name__ == "__main__":
    app()
