from __future__ import annotations

import json
import re
from pathlib import Path

from familiar.render import render_image

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def mood_from_filename(path: Path) -> str:
    mood = path.stem.lower().replace("-", "_").replace(" ", "_")
    return re.sub(r"[^a-z0-9_]+", "", mood)


def discover_images(directory: Path) -> list[Path]:
    return sorted(
        path for path in directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES
    )


def _display_name(name: str) -> str:
    return name.strip() or "Familiar"


def generate_pack(
    source: Path,
    out: Path,
    *,
    name: str,
    default_mood: str = "neutral",
    height: int = 32,
    mode: str = "braille",
    background: str = "alpha",
    crop: bool = True,
    pad: int = 0,
    threshold: int = 128,
    contrast: float = 1.0,
    invert: bool = False,
) -> list[str]:
    """Generate a plain-file character pack from mood images."""
    images = discover_images(source)
    if not images:
        raise ValueError(f"no supported images found in {source}")

    out.mkdir(parents=True, exist_ok=True)
    moods: dict[str, str] = {}
    for image in images:
        mood = mood_from_filename(image)
        if not mood:
            continue
        target = f"{mood}.txt"
        rendered = render_image(
            image,
            height=height,
            mode=mode,
            crop=crop,
            pad=pad,
            background=background,
            threshold=threshold,
            contrast=contrast,
            invert=invert,
        )
        (out / target).write_text(rendered, encoding="utf-8")
        moods[mood] = target

    if not moods:
        raise ValueError("no valid mood images found")
    if default_mood not in moods:
        default_mood = sorted(moods)[0]

    mood_lines = "\n".join(
        f'    "{mood}": "{asset}",' for mood, asset in sorted(moods.items())
    )
    definition = f'''NAME = "{_display_name(name)}"

DEFAULT_MOOD = "{default_mood}"

MOODS = {{
{mood_lines}
}}

STYLE = {{
    "layout": "avatar_above",
    "box": "single",
    "max_width": 72,
    "padding": 1,
}}
'''
    (out / "familiar.py").write_text(definition, encoding="utf-8")
    metadata = {
        "name": _display_name(name),
        "default_mood": default_mood,
        "moods": sorted(moods),
        "source": str(source),
        "renderer": {"mode": mode, "height": height, "background": background},
    }
    (out / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return sorted(moods)
