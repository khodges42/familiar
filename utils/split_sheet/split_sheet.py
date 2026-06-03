#!/usr/bin/env python3


""" Split a sprite/expression sheet into individual images.

Examples:

    python split_sheet.py proxy.png

    python split_sheet.py proxy.png \
        --rows 2 \
        --cols 3 \
        --labels neutral curious excited sad angry surprised

    python split_sheet.py spritesheet.png \
        --rows 4 \
        --cols 4 \
        --out sprites 
"""

import argparse
from pathlib import Path

from PIL import Image

DEFAULT_LABELS = [
    "neutral",
    "curious",
    "excited",
    "sad",
    "angry",
    "surprised",
]


def main():
    parser = argparse.ArgumentParser(
        description="Split a grid-based sprite sheet into individual images."
    )

    parser.add_argument(
        "image",
        help="Path to the sprite sheet image",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=2,
        help="Number of rows in the sheet (default: 2)",
    )

    parser.add_argument(
        "--cols",
        type=int,
        default=3,
        help="Number of columns in the sheet (default: 3)",
    )

    parser.add_argument(
        "--labels",
        nargs="+",
        default=DEFAULT_LABELS,
        help="Output labels in row-major order",
    )

    parser.add_argument(
        "--out",
        default="output",
        help="Output directory (default: output)",
    )

    args = parser.parse_args()

    image_path = Path(args.image)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(image_path)

    width, height = img.size
    cell_w = width // args.cols
    cell_h = height // args.rows

    total_cells = args.rows * args.cols

    labels = list(args.labels)

    # Auto-fill missing labels
    while len(labels) < total_cells:
        labels.append(f"sprite_{len(labels)}")

    # Ignore extras
    labels = labels[:total_cells]

    for idx in range(total_cells):
        row = idx // args.cols
        col = idx % args.cols

        left = col * cell_w
        upper = row * cell_h
        right = left + cell_w
        lower = upper + cell_h

        sprite = img.crop((left, upper, right, lower))

        filename = out_dir / f"{labels[idx]}.png"
        sprite.save(filename)

        print(f"saved {filename}")

    print(f"\nDone. Wrote {total_cells} images to {out_dir}")


if __name__ == "__main__":
    main()
