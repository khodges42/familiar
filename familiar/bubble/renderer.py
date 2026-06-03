from __future__ import annotations

from dataclasses import dataclass
from textwrap import wrap


@dataclass(frozen=True)
class BoxStyle:
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str


BOX_STYLES: dict[str, BoxStyle | None] = {
    "single": BoxStyle("┌", "┐", "└", "┘", "─", "│"),
    "rounded": BoxStyle("╭", "╮", "╰", "╯", "─", "│"),
    "ascii": BoxStyle("+", "+", "+", "+", "-", "|"),
    "none": None,
}


def _wrap_paragraph(text: str, width: int) -> list[str]:
    if text == "":
        return [""]
    lines = wrap(
        text,
        width=max(1, width),
        break_long_words=True,
        break_on_hyphens=False,
        replace_whitespace=False,
        drop_whitespace=True,
    )
    return lines or [""]


def wrap_text(text: str, width: int) -> list[str]:
    """Wrap text while preserving explicit newlines."""
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        lines.extend(_wrap_paragraph(paragraph, width))
    return lines


def render_bubble(
    text: str,
    *,
    title: str | None = None,
    box: str = "single",
    max_width: int = 72,
    padding: int = 1,
) -> str:
    """Render text inside a speech bubble."""
    if box not in BOX_STYLES:
        raise ValueError(f"unsupported box style: {box}")

    padding = max(0, padding)
    max_width = max(8, max_width)
    content_width = max(1, max_width - (padding * 2) - 2)
    wrapped = wrap_text(text, content_width)
    inner_width = max(len(line) for line in wrapped)
    if title:
        inner_width = max(inner_width, len(title) + 2)
    inner_width = min(max(inner_width, 1), content_width)

    if box == "none":
        pad = " " * padding
        return "\n".join(f"{pad}{line}{pad}".rstrip() for line in wrapped)

    style = BOX_STYLES[box]
    assert style is not None
    body_width = inner_width + (padding * 2)

    if title:
        title_text = f" {title} "
        remaining = max(0, body_width - len(title_text))
        top = (
            f"{style.top_left}{style.horizontal}{title_text}"
            f"{style.horizontal * remaining}{style.top_right}"
        )
    else:
        top = f"{style.top_left}{style.horizontal * body_width}{style.top_right}"

    body = [
        (
            f"{style.vertical}{' ' * padding}{line.ljust(inner_width)}"
            f"{' ' * padding}{style.vertical}"
        )
        for line in wrapped
    ]
    bottom = f"{style.bottom_left}{style.horizontal * body_width}{style.bottom_right}"
    return "\n".join([top, *body, bottom])
