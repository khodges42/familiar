from pathlib import Path

from PIL import Image

from familiar.forge import generate_pack, validate_character


def test_pack_generation_and_validation(tmp_path: Path, monkeypatch):
    source = tmp_path / "source"
    out = tmp_path / "characters" / "demo"
    source.mkdir()
    image = Image.new("RGBA", (4, 4), (255, 255, 255, 0))
    image.putpixel((1, 1), (0, 0, 0, 255))
    image.save(source / "neutral.png")

    generate_pack(source, out, name="Demo", mode="ascii", height=4)
    monkeypatch.chdir(tmp_path)

    issues = validate_character("demo")

    assert issues[0].level == "ok"
