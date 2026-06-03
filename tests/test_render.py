from pathlib import Path

from PIL import Image

from familiar.render.image import render_braille, render_image


def test_braille_bit_mapping():
    image = Image.new("RGBA", (2, 4), (255, 255, 255, 0))
    image.putpixel((0, 0), (0, 0, 0, 255))

    assert render_braille(image).strip() == "⠁"


def test_ascii_renderer_uses_alpha_spaces(tmp_path: Path):
    image = Image.new("RGBA", (2, 2), (255, 255, 255, 0))
    image.putpixel((0, 0), (0, 0, 0, 255))
    path = tmp_path / "sample.png"
    image.save(path)

    rendered = render_image(path, height=2, mode="ascii", crop=False)

    assert "@" in rendered
