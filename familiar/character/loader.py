from __future__ import annotations

import importlib.util
import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from familiar.config import configured_character_path, default_style
from familiar.errors import (
    CharacterDefinitionError,
    CharacterNotFoundError,
    MoodNotFoundError,
)


@dataclass(frozen=True)
class CharacterPack:
    name: str
    slug: str
    path: Path
    default_mood: str
    moods: dict[str, str]
    style: dict[str, object]
    metadata: dict[str, object]

    def available_moods(self) -> list[str]:
        return sorted(self.moods)

    def avatar(self, mood: str | None = None) -> str:
        resolved = self.resolve_mood(mood)
        asset = self.path / self.moods[resolved]
        if not asset.exists():
            raise MoodNotFoundError(
                f"mood '{resolved}' points to missing asset: {asset.name}"
            )
        return asset.read_text(encoding="utf-8")

    def resolve_mood(self, mood: str | None) -> str:
        requested = mood or self.default_mood
        if requested in self.moods:
            return requested
        if self.default_mood in self.moods:
            return self.default_mood
        raise MoodNotFoundError(
            f"mood '{requested}' is missing and default mood "
            f"'{self.default_mood}' is unavailable"
        )


def character_search_paths() -> list[Path]:
    cwd = Path.cwd()
    paths = [cwd / "characters"]
    configured = os.environ.get("FAMILIAR_CHARACTER_PATH")
    if configured:
        paths.extend(Path(part).expanduser() for part in configured.split(os.pathsep))
    paths.append(configured_character_path())
    paths.append(Path(__file__).resolve().parents[1] / "characters")
    paths.append(Path(__file__).resolve().parents[2] / "characters")
    return paths


def find_character(name: str) -> Path:
    for root in character_search_paths():
        candidate = root / name
        if candidate.is_dir():
            return candidate
    searched = ", ".join(str(path) for path in character_search_paths())
    raise CharacterNotFoundError(
        f"character '{name}' was not found. Searched: {searched}"
    )


def _load_module(definition: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        f"_familiar_character_{definition.parent.name}", definition
    )
    if spec is None or spec.loader is None:
        raise CharacterDefinitionError(
            f"cannot load character definition: {definition}"
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_metadata(path: Path) -> dict[str, object]:
    metadata = path / "metadata.json"
    if not metadata.exists():
        return {}
    try:
        return json.loads(metadata.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CharacterDefinitionError(f"invalid metadata.json: {exc}") from exc


def load_character(name: str) -> CharacterPack:
    path = find_character(name)
    definition = path / "familiar.py"
    if not definition.exists():
        raise CharacterDefinitionError(f"missing required file: {definition}")

    module = _load_module(definition)
    display_name = getattr(module, "NAME", None)
    default_mood = getattr(module, "DEFAULT_MOOD", None)
    moods = getattr(module, "MOODS", None)
    style = {**default_style(), **getattr(module, "STYLE", {})}

    if not isinstance(display_name, str) or not display_name:
        raise CharacterDefinitionError(
            "familiar.py must define NAME as a non-empty string"
        )
    if not isinstance(default_mood, str) or not default_mood:
        raise CharacterDefinitionError(
            "familiar.py must define DEFAULT_MOOD as a non-empty string"
        )
    if not isinstance(moods, dict) or not moods:
        raise CharacterDefinitionError(
            "familiar.py must define non-empty MOODS mapping"
        )
    if default_mood not in moods:
        raise CharacterDefinitionError(
            f"default mood '{default_mood}' is not present in MOODS"
        )

    normalized = {str(key): str(value) for key, value in moods.items()}
    default_asset = path / normalized[default_mood]
    if not default_asset.exists():
        raise CharacterDefinitionError(
            f"default mood asset is missing: {default_asset.name}"
        )

    return CharacterPack(
        name=display_name,
        slug=name,
        path=path,
        default_mood=default_mood,
        moods=normalized,
        style=style,
        metadata=_load_metadata(path),
    )
