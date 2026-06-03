from __future__ import annotations

import shutil
import subprocess
import tempfile
from array import array
from pathlib import Path

from PIL import Image

FONT_RATIO = 0.5
CHAFA_SYMBOLS = "block,border,braille,ascii"


def chafa_size(image: Image.Image, height: int) -> tuple[int, int]:
    ratio = image.width / max(1, image.height)
    return max(1, round(height * ratio / FONT_RATIO)), max(1, height)


def _render_with_python(image: Image.Image, *, height: int) -> str:
    try:
        import chafa
    except ImportError as exc:
        raise RuntimeError(str(exc)) from exc

    width, height = chafa_size(image, height)
    rgba = image.convert("RGBA").resize(
        (width * 2, height * 4),
        Image.Resampling.LANCZOS,
    )

    symbol_map = chafa.SymbolMap()
    symbol_map.apply_selectors(CHAFA_SYMBOLS)

    config = chafa.CanvasConfig()
    config.width = width
    config.height = height
    config.pixel_mode = chafa.PixelMode.CHAFA_PIXEL_MODE_SYMBOLS
    config.canvas_mode = chafa.CanvasMode.CHAFA_CANVAS_MODE_FGBG
    config.set_symbol_map(symbol_map)

    canvas = chafa.Canvas(config)
    pixels = array("B", rgba.tobytes())
    canvas.draw_all_pixels(
        chafa.PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED,
        pixels,
        rgba.width,
        rgba.height,
        rgba.width * 4,
    )
    output = canvas.print()
    if isinstance(output, bytes):
        return output.decode("utf-8")
    return str(output)


def _render_with_cli(image: Image.Image, *, height: int) -> str:
    executable = shutil.which("chafa")
    if executable is None:
        raise RuntimeError("chafa executable was not found on PATH")

    width, height = chafa_size(image, height)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "familiar-chafa.png"
        image.save(path)
        result = subprocess.run(
            [
                executable,
                "--format",
                "symbols",
                "--colors",
                "none",
                "--symbols",
                CHAFA_SYMBOLS,
                "--size",
                f"{width}x{height}",
                str(path),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or "chafa command failed")
    return result.stdout


def render_chafa(image: Image.Image, *, height: int = 32) -> str:
    """Render an image with Chafa, using Python bindings or CLI fallback."""
    try:
        output = _render_with_python(image, height=height)
    except RuntimeError as python_error:
        try:
            output = _render_with_cli(image, height=height)
        except RuntimeError as cli_error:
            raise RuntimeError(
                "Chafa rendering requires libchafa with chafa.py, or a chafa "
                "executable on PATH. Install chafa and retry. "
                f"Python backend: {python_error}. CLI backend: {cli_error}."
            ) from cli_error
    return output.rstrip("\n") + "\n"
