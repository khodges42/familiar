from __future__ import annotations

from familiar.text_width import display_width, pad_to_width

LAYOUTS = {"avatar_above", "avatar_left", "bubble_only", "avatar_only", "compact"}


def _split(value: str) -> list[str]:
    return value.splitlines()


def _width(lines: list[str]) -> int:
    return max((display_width(line) for line in lines), default=0)


def _indent(lines: list[str], width: int) -> list[str]:
    return [f"{' ' * width}{line}" if line else line for line in lines]


def _join_above(avatar: list[str], bubble: list[str]) -> str:
    avatar_width = _width(avatar)
    bubble_width = _width(bubble)
    indent = max(0, (avatar_width - bubble_width) // 2)
    return "\n\n".join(
        part
        for part in [
            "\n".join(avatar),
            "\n".join(_indent(bubble, indent)),
        ]
        if part
    )


def _join_side_by_side(left: list[str], right: list[str], gap: int = 2) -> str:
    left_width = _width(left)
    height = max(len(left), len(right))
    output: list[str] = []
    for index in range(height):
        left_line = left[index] if index < len(left) else ""
        right_line = right[index] if index < len(right) else ""
        output.append(
            f"{pad_to_width(left_line, left_width)}{' ' * gap}{right_line}".rstrip()
        )
    return "\n".join(output)


def render_layout(avatar: str, bubble: str, *, layout: str = "avatar_above") -> str:
    """Combine avatar and bubble text using a named layout."""
    if layout not in LAYOUTS:
        raise ValueError(f"unsupported layout: {layout}")

    avatar = avatar.rstrip("\n")
    bubble = bubble.rstrip("\n")

    if layout == "avatar_only":
        return avatar
    if layout == "bubble_only":
        return bubble
    if layout == "avatar_left":
        return _join_side_by_side(_split(avatar), _split(bubble))
    if layout == "compact":
        return "\n".join(part for part in [avatar, bubble] if part)
    return _join_above(_split(avatar), _split(bubble))
