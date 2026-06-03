from __future__ import annotations

import unicodedata


def display_width(value: str) -> int:
    """Return a conservative terminal display width for a string."""
    width = 0
    for char in value:
        if unicodedata.combining(char):
            continue
        category = unicodedata.category(char)
        if category in {"Cc", "Cf"}:
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def pad_to_width(value: str, width: int) -> str:
    padding = max(0, width - display_width(value))
    return value + (" " * padding)
