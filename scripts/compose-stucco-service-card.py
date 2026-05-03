#!/usr/bin/env python3
"""Build a square 2x2 service card image from four stucco textures."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

# Order: top-left, top-right, bottom-left, bottom-right (filenames under stucco-quad-sources/)
SOURCES = (
    "stucco-veneziano-tradizionale-eaf46187-6e86-40f6-88fc-ef4b784d251f.png",
    "stucco-veneziano-parete-5299c469-f4b5-4e4f-b89c-d5c55efa8bc8.png",
    "stucco-veneziano-rosso-c2593c96-bdc0-4f03-950e-e232d5d8de1f.png",
    "stucco-veneziano-pink-37970a91-f5ee-4ecd-842d-ea4a54b34bac.png",
)

CELL = 800  # 1600px square output; sharp enough for cards


def cover_square(im: Image.Image, side: int) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    scale = max(side / w, side / h)
    nw, nh = int(w * scale), int(h * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - side) // 2
    top = (nh - side) // 2
    return im.crop((left, top, left + side, top + side))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "assets/private/stucco-quad-sources"
    out = root / "assets/private/service-card-stucco-quad.png"

    tiles: list[Image.Image] = []
    for name in SOURCES:
        src = src_dir / name
        if not src.is_file():
            raise SystemExit(f"Missing source: {src}")
        tiles.append(cover_square(Image.open(src), CELL))

    grid = Image.new("RGB", (CELL * 2, CELL * 2), (236, 232, 226))
    positions = ((0, 0), (CELL, 0), (0, CELL), (CELL, CELL))
    for tile, (x, y) in zip(tiles, positions, strict=True):
        grid.paste(tile, (x, y))

    out.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({grid.size[0]}x{grid.size[1]})")


if __name__ == "__main__":
    main()
