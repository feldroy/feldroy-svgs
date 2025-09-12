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
Convert an SVG file to PNG at specified rectangular size.

- Converts 'feldroy-logo-square.svg' to 'feldroy-logo-rect-{width}x{height}.png'.
- Centers the logo, scales to fill the rectangle, and crops centered.
- Optimizes the PNG using Pillow's built-in optimizer.

Usage:
    uv run svg_to_png_rect.py --width 320 --height 132
    uv run svg_to_png_rect.py --width 500 --height 500  # For square

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
    width: int = typer.Option(320, help="Width of the output image in pixels"),
    height: int = typer.Option(132, help="Height of the output image in pixels")
):
    """
    Generate a rectangular PNG from the SVG file.
    """
    svg_path = Path(SVG_FILE)
    if not svg_path.exists():
        typer.echo(f"SVG file not found: {SVG_FILE}")
        sys.exit(1)
    
    # Determine the size to render the SVG (scale to fill the rectangle)
    render_size = max(width, height)
    
    # Temporary PNG path for rendering
    temp_png_path = svg_path.with_suffix('.temp.png')
    final_png_path = svg_path.parent / f"{svg_path.stem}-rect-{width}x{height}.png"
    
    # Render SVG to PNG at render_size x render_size
    cairosvg.svg2png(url=str(svg_path), write_to=str(temp_png_path), output_width=render_size, output_height=render_size)
    
    # Open the rendered image
    with Image.open(temp_png_path) as im:
        # Crop to the desired width and height, centered
        left = (render_size - width) // 2
        top = (render_size - height) // 2
        right = left + width
        bottom = top + height
        
        cropped_im = im.crop((left, top, right, bottom))
        
        # Save the cropped image
        cropped_im.save(final_png_path, "PNG", optimize=True)
    
    # Remove the temporary file
    temp_png_path.unlink()
    
    typer.echo(f"Generated {final_png_path.name} ({width}x{height}).")

if __name__ == "__main__":
    app()
