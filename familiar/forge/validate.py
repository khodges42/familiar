from __future__ import annotations

from dataclasses import dataclass

from familiar.bubble.renderer import BOX_STYLES
from familiar.character.loader import load_character
from familiar.errors import FamiliarError
from familiar.layout import LAYOUTS


@dataclass(frozen=True)
class ValidationIssue:
    level: str
    message: str


def validate_character(name: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        pack = load_character(name)
    except FamiliarError as exc:
        return [ValidationIssue("error", str(exc))]

    if pack.default_mood not in pack.moods:
        issues.append(ValidationIssue("error", "default mood is not declared in MOODS"))

    layout = str(pack.style.get("layout", "avatar_above"))
    if layout not in LAYOUTS:
        issues.append(ValidationIssue("error", f"invalid layout: {layout}"))

    box = str(pack.style.get("box", "single"))
    if box not in BOX_STYLES:
        issues.append(ValidationIssue("error", f"invalid box style: {box}"))

    for mood, filename in sorted(pack.moods.items()):
        path = pack.path / filename
        if not path.exists():
            issues.append(
                ValidationIssue(
                    "error", f"mood '{mood}' asset is missing: {filename}"
                )
            )
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            issues.append(ValidationIssue("error", f"mood '{mood}' asset is empty"))
        width = max((len(line) for line in text.splitlines()), default=0)
        if width > 140:
            issues.append(
                ValidationIssue(
                    "warning", f"mood '{mood}' is very wide: {width} columns"
                )
            )

    if not issues:
        issues.append(ValidationIssue("ok", f"{pack.name} is valid"))
    return issues
