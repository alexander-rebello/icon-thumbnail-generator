#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageColor


def tint_icon(icon: Image.Image, icon_color: str) -> Image.Image:
    r, g, b, _ = ImageColor.getcolor(icon_color, "RGBA")
    colored = Image.new("RGBA", icon.size, (r, g, b, 255))
    alpha = icon.getchannel("A")
    colored.putalpha(alpha)
    return colored


def build_image(
    svg_path: Path,
    output_path: Path,
    background_color: str,
    icon_color: str,
    width: int,
    height: int,
    scale: float,
) -> None:
    png_data = cairosvg.svg2png(url=str(svg_path))
    icon = Image.open(BytesIO(png_data)).convert("RGBA")
    icon = tint_icon(icon, icon_color)

    max_icon_w = max(1, int(width * scale))
    max_icon_h = max(1, int(height * scale))
    icon.thumbnail((max_icon_w, max_icon_h), Image.Resampling.LANCZOS)

    bg_rgba = ImageColor.getcolor(background_color, "RGBA")
    canvas = Image.new("RGBA", (width, height), bg_rgba)

    x = (width - icon.width) // 2
    y = (height - icon.height) // 2
    canvas.paste(icon, (x, y), icon)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images from SVGs with base color and centered icon."
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=440,
        help="Canvas width in pixels (default: 440)",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=int,
        default=250,
        help="Canvas height in pixels (default: 250)",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        default=0.75,
        help="Icon scale relative to canvas (0-1, default: 0.75)",
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        default=Path(__file__).parent,
        help="Directory containing SVG files (default: script directory)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "generated-images",
        help="Output directory for PNG files (default: ./generated-images)",
    )
    parser.add_argument(
        "-c",
        "--specs",
        type=Path,
        default=Path(__file__).parent / "icon_specs.json",
        help="JSON file with icon specifications (default: ./icon_specs.json)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.width <= 0 or args.height <= 0:
        raise ValueError("Width and height must be positive.")
    if not (0 < args.scale <= 1):
        raise ValueError("Scale must be between 0 and 1.")

    if not args.specs.exists():
        raise FileNotFoundError(f"Icon specs file not found: {args.specs}")

    with args.specs.open("r", encoding="utf-8") as f:
        icon_specs = json.load(f)

    generated = 0
    for spec in icon_specs:
        file_name = spec["file"]
        icon_color = spec["icon_color"]
        background_color = spec["background_color"]

        svg_path = args.input_dir / file_name
        if not svg_path.exists():
            print(f"Skipped (missing): {svg_path}")
            continue

        output_path = args.output_dir / f"{svg_path.stem}.png"
        build_image(
            svg_path=svg_path,
            output_path=output_path,
            background_color=background_color,
            icon_color=icon_color,
            width=args.width,
            height=args.height,
            scale=args.scale,
        )
        generated += 1
        print(f"Generated: {output_path}")

    print(f"Done. Generated {generated} image(s) in {args.output_dir}")


if __name__ == "__main__":
    main()
