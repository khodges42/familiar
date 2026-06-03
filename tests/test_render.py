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


def test_line_renderer_emits_line_characters(tmp_path: Path):
    image = Image.new("RGBA", (4, 4), (255, 255, 255, 0))
    for y in range(4):
        image.putpixel((2, y), (0, 0, 0, 255))
    path = tmp_path / "line.png"
    image.save(path)

    rendered = render_image(path, height=4, mode="line", crop=False, threshold=10)

    assert any(char in rendered for char in "│─╱╲")


def test_ink_renderer_uses_quadrants(tmp_path: Path):
    image = Image.new("RGB", (8, 8), "white")
    for x in range(2, 6):
        for y in range(2, 6):
            image.putpixel((x, y), (0, 0, 0))
    path = tmp_path / "ink.png"
    image.save(path)

    rendered = render_image(path, height=4, mode="ink", threshold=200)

    assert any(char in rendered for char in "·─│╱╲▘▝▀▖▌▞▛▗▚▐▜▄▙▟▪")


def test_chafa_mode_reports_missing_backend(tmp_path: Path):
    image = Image.new("RGB", (4, 4), "white")
    path = tmp_path / "chafa.png"
    image.save(path)

    try:
        render_image(path, height=4, mode="chafa")
    except RuntimeError as exc:
        assert "Chafa rendering requires" in str(exc)
