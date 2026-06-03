from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

CONFIG_PATH = Path.home() / ".config" / "familiar" / "config.toml"


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def default_style() -> dict[str, object]:
    defaults = load_config().get("defaults", {})
    return {
        "layout": defaults.get("layout", "avatar_above"),
        "box": defaults.get("box", "single"),
        "max_width": int(defaults.get("max_width", 72)),
        "padding": int(defaults.get("padding", 1)),
    }


def configured_character_path() -> Path:
    paths = load_config().get("paths", {})
    configured = paths.get("characters", "~/.config/familiar/characters")
    return Path(str(configured)).expanduser()
