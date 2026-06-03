from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance

ASCII_RAMP = " .:-=+*#%@"
BLOCK_RAMP = " ░▒▓█"
BRAILLE_DOTS = (0x01, 0x02, 0x04, 0x40, 0x08, 0x10, 0x20, 0x80)
QUADRANTS = {
    0b0000: " ",
    0b0001: "▘",
    0b0010: "▝",
    0b0011: "▀",
    0b0100: "▖",
    0b0101: "▌",
    0b0110: "▞",
    0b0111: "▛",
    0b1000: "▗",
    0b1001: "▚",
    0b1010: "▐",
    0b1011: "▜",
    0b1100: "▄",
    0b1101: "▙",
    0b1110: "▟",
    0b1111: "█",
}


def _visible_bbox(image: Image.Image, threshold: int = 8):
    if image.mode != "RGBA":
        return image.getbbox()
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    return mask.getbbox()


def prepare_image(
    image: Image.Image,
    *,
    height: int,
    crop: bool = True,
    pad: int = 0,
    background: str = "alpha",
    threshold: int = 128,
    contrast: float = 1.0,
    invert: bool = False,
) -> Image.Image:
    if background == "remove":
        try:
            from rembg import remove
        except ImportError as exc:
            raise RuntimeError(
                "background removal requires installing familiar[background]"
            ) from exc
        image = remove(image)
    elif background == "threshold":
        image = image.convert("RGBA")
        corner = image.getpixel((0, 0))[:3]
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                red, green, blue, alpha = pixels[x, y]
                distance = (
                    abs(red - corner[0])
                    + abs(green - corner[1])
                    + abs(blue - corner[2])
                )
                if distance < threshold:
                    pixels[x, y] = (red, green, blue, 0)
                else:
                    pixels[x, y] = (red, green, blue, alpha)
    elif background == "keep":
        image = image.convert("RGB").convert("RGBA")
    else:
        image = image.convert("RGBA")

    if crop:
        bbox = _visible_bbox(image)
        if bbox:
            image = image.crop(bbox)
    if pad:
        padded = Image.new(
            "RGBA",
            (image.width + pad * 2, image.height + pad * 2),
            (0, 0, 0, 0),
        )
        padded.alpha_composite(image, (pad, pad))
        image = padded

    ratio = image.width / max(1, image.height)
    # Terminal cells are taller than they are wide for ASCII/block output.
    width = max(1, round(height * ratio * 2))
    image = image.resize((width, max(1, height)), Image.Resampling.LANCZOS)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if invert:
        rgb = Image.eval(image.convert("RGB"), lambda value: 255 - value)
        rgb.putalpha(image.getchannel("A"))
        image = rgb
    return image


def prepare_square_subpixel_image(
    image: Image.Image,
    *,
    height: int,
    crop: bool = True,
    pad: int = 0,
    background: str = "threshold",
    threshold: int = 245,
    contrast: float = 1.0,
    invert: bool = False,
) -> Image.Image:
    """Prepare an image for renderers whose subpixels are roughly square."""
    image = prepare_image(
        image,
        height=height * 2,
        crop=crop,
        pad=pad,
        background=background,
        threshold=threshold,
        contrast=contrast,
        invert=invert,
    )
    ratio = image.width / max(1, image.height)
    width = max(2, round(height * ratio) * 2)
    pixel_height = max(2, height * 2)
    return image.resize((width, pixel_height), Image.Resampling.LANCZOS)


def _ramp(value: int, ramp: str) -> str:
    index = round((value / 255) * (len(ramp) - 1))
    return ramp[index]


def render_ascii(image: Image.Image, *, ramp: str = ASCII_RAMP) -> str:
    image = image.convert("RGBA")
    gray = image.convert("LA")
    lines: list[str] = []
    for y in range(image.height):
        line = []
        for x in range(image.width):
            value, alpha = gray.getpixel((x, y))
            line.append(" " if alpha == 0 else _ramp(255 - value, ramp))
        lines.append("".join(line).rstrip())
    return "\n".join(lines).rstrip() + "\n"


def render_block(image: Image.Image) -> str:
    return render_ascii(image, ramp=BLOCK_RAMP)


def render_ink(image: Image.Image, *, threshold: int = 180) -> str:
    """Render dark ink boundaries with Unicode quadrant block characters."""
    image = image.convert("RGBA")
    width = image.width if image.width % 2 == 0 else image.width + 1
    height = image.height if image.height % 2 == 0 else image.height + 1
    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    canvas.alpha_composite(image)
    gray = canvas.convert("LA")

    def is_dark(px: int, py: int) -> bool:
        if px < 0 or py < 0 or px >= width or py >= height:
            return False
        value, alpha = gray.getpixel((px, py))
        return alpha > 0 and value < threshold

    def is_boundary(px: int, py: int) -> bool:
        if not is_dark(px, py):
            return False
        for nx, ny in (
            (px - 1, py),
            (px + 1, py),
            (px, py - 1),
            (px, py + 1),
        ):
            if not is_dark(nx, ny):
                return True
        return False

    lines: list[str] = []
    for y in range(0, height, 2):
        chars: list[str] = []
        for x in range(0, width, 2):
            bits = 0
            for bit, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
                if is_boundary(x + dx, y + dy):
                    bits |= 1 << bit
            chars.append(QUADRANTS[bits])
        lines.append("".join(chars).rstrip())
    return "\n".join(lines).rstrip() + "\n"


def _line_char(gx: int, gy: int, magnitude: int, threshold: int) -> str:
    if magnitude < threshold:
        return " "
    abs_x = abs(gx)
    abs_y = abs(gy)
    if abs_x > abs_y * 2:
        return "│"
    if abs_y > abs_x * 2:
        return "─"
    return "╲" if gx * gy > 0 else "╱"


def render_line(image: Image.Image, *, threshold: int = 80) -> str:
    """Render image edges with line-drawing characters."""
    image = image.convert("RGBA")
    gray = image.convert("LA")

    def effective_intensity(px: int, py: int) -> int:
        value, alpha = gray.getpixel((px, py))
        return 255 if alpha == 0 else value

    lines: list[str] = []
    for y in range(image.height):
        line: list[str] = []
        for x in range(image.width):
            left = effective_intensity(max(0, x - 1), y)
            right = effective_intensity(min(image.width - 1, x + 1), y)
            up = effective_intensity(x, max(0, y - 1))
            down = effective_intensity(x, min(image.height - 1, y + 1))
            gx = int(right) - int(left)
            gy = int(down) - int(up)
            magnitude = abs(gx) + abs(gy)
            line.append(_line_char(gx, gy, magnitude, threshold))
        lines.append("".join(line).rstrip())
    return "\n".join(lines).rstrip() + "\n"


def render_braille(image: Image.Image, *, threshold: int = 128) -> str:
    image = image.convert("RGBA")
    width = image.width if image.width % 2 == 0 else image.width + 1
    height = (
        image.height
        if image.height % 4 == 0
        else image.height + (4 - image.height % 4)
    )
    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    canvas.alpha_composite(image)
    gray = canvas.convert("LA")
    lines: list[str] = []
    for y in range(0, height, 4):
        chars: list[str] = []
        for x in range(0, width, 2):
            bits = 0
            for idx, (dx, dy) in enumerate(
                ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3))
            ):
                value, alpha = gray.getpixel((x + dx, y + dy))
                if alpha > 0 and value < threshold:
                    bits |= BRAILLE_DOTS[idx]
            chars.append(chr(0x2800 + bits) if bits else " ")
        lines.append("".join(chars).rstrip())
    return "\n".join(lines).rstrip() + "\n"


def render_image(
    path: str | Path,
    *,
    height: int = 32,
    mode: str = "braille",
    crop: bool = True,
    pad: int = 0,
    background: str = "alpha",
    threshold: int = 128,
    contrast: float = 1.0,
    invert: bool = False,
    debug: Path | None = None,
) -> str:
    image = Image.open(path)
    if mode == "ink":
        prepared = prepare_square_subpixel_image(
            image,
            height=height,
            crop=crop,
            pad=pad,
            background=background if background != "alpha" else "threshold",
            threshold=threshold,
            contrast=contrast,
            invert=invert,
        )
        if debug:
            debug.parent.mkdir(parents=True, exist_ok=True)
            prepared.save(debug)
        return render_ink(prepared, threshold=threshold)

    prepared = prepare_image(
        image,
        height=height,
        crop=crop,
        pad=pad,
        background=background,
        threshold=threshold,
        contrast=contrast,
        invert=invert,
    )
    if debug:
        debug.parent.mkdir(parents=True, exist_ok=True)
        prepared.save(debug)
    if mode == "ascii":
        return render_ascii(prepared)
    if mode == "block":
        return render_block(prepared)
    if mode == "line":
        return render_line(prepared, threshold=threshold)
    if mode == "braille":
        return render_braille(prepared, threshold=threshold)
    raise ValueError(f"unsupported render mode: {mode}")
