from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from familiar import Familiar
from familiar.errors import FamiliarError
from familiar.forge import generate_pack, validate_character
from familiar.render import render_image

VERSION = "0.1.0"
DIRECT_OPTIONS = {"--layout", "--box", "--max-width"}
DIRECT_FLAGS = {"--plain", "--no-title"}
COMMANDS = {
    "say",
    "forge",
    "pack",
    "validate",
    "preview",
    "forge-preview",
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

app = typer.Typer(
    add_completion=False,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": False},
    no_args_is_help=True,
)
stdout = Console(file=sys.stdout, force_terminal=False, color_system=None, markup=False)
stderr = Console(file=sys.stderr, force_terminal=False, color_system=None, markup=False)


def _fail(message: str) -> None:
    stderr.print(f"familiar: {message}")
    raise typer.Exit(1)


def _render_say(
    character: str,
    mood: str,
    text: str,
    *,
    layout: str | None,
    box: str | None,
    max_width: int | None,
    plain: bool,
    title: bool,
) -> None:
    try:
        familiar = Familiar.load(character)
        if plain:
            stdout.print(familiar.avatar(mood), end="")
        else:
            stdout.print(
                familiar.say(
                    mood,
                    text,
                    layout=layout,
                    box=box,
                    max_width=max_width,
                    title=familiar.name if title else "",
                )
            )
    except (FamiliarError, ValueError) as exc:
        _fail(str(exc))


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", help="Show version.")] = False,
) -> None:
    """Terminal companions for humans and machines."""
    if version:
        stdout.print(VERSION)
        raise typer.Exit()
    if ctx.invoked_subcommand is None and ctx.args:
        if len(ctx.args) < 3:
            _fail("usage: familiar CHARACTER MOOD TEXT")
        character, mood, *parts = ctx.args
        _render_say(
            character,
            mood,
            " ".join(parts),
            layout=None,
            box=None,
            max_width=None,
            plain=False,
            title=True,
        )
        raise typer.Exit()


def _parse_direct_args(args: list[str]) -> dict[str, object]:
    if len(args) < 3:
        _fail("usage: familiar CHARACTER MOOD TEXT")
    character, mood, *rest = args
    options: dict[str, object] = {
        "character": character,
        "mood": mood,
        "layout": None,
        "box": None,
        "max_width": None,
        "plain": False,
        "title": True,
    }
    text_parts: list[str] = []
    index = 0
    while index < len(rest):
        value = rest[index]
        if value in DIRECT_OPTIONS:
            if index + 1 >= len(rest):
                _fail(f"{value} requires a value")
            raw = rest[index + 1]
            if value == "--layout":
                options["layout"] = raw
            elif value == "--box":
                options["box"] = raw
            else:
                try:
                    options["max_width"] = int(raw)
                except ValueError:
                    _fail("--max-width requires an integer")
            index += 2
            continue
        if value in DIRECT_FLAGS:
            if value == "--plain":
                options["plain"] = True
            elif value == "--no-title":
                options["title"] = False
            index += 1
            continue
        text_parts.append(value)
        index += 1
    options["text"] = " ".join(text_parts)
    return options


@app.command()
def say(
    character: str,
    mood: str,
    text: list[str],
    layout: Annotated[str | None, typer.Option("--layout")] = None,
    box: Annotated[str | None, typer.Option("--box")] = None,
    max_width: Annotated[int | None, typer.Option("--max-width")] = None,
    plain: Annotated[bool, typer.Option("--plain")] = False,
    no_title: Annotated[bool, typer.Option("--no-title")] = False,
) -> None:
    """Render a character mood and text."""
    _render_say(
        character,
        mood,
        " ".join(text),
        layout=layout,
        box=box,
        max_width=max_width,
        plain=plain,
        title=not no_title,
    )


@app.command()
def forge(
    image: Path,
    height: Annotated[int, typer.Option("--height", min=1)] = 32,
    mode: Annotated[str, typer.Option("--mode")] = "braille",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    crop: Annotated[bool, typer.Option("--crop/--no-crop")] = True,
    pad: Annotated[int, typer.Option("--pad", min=0)] = 0,
    background: Annotated[str, typer.Option("--background")] = "alpha",
    threshold: Annotated[int, typer.Option("--threshold", min=0, max=255)] = 128,
    contrast: Annotated[float, typer.Option("--contrast", min=0.1)] = 1.0,
    invert: Annotated[bool, typer.Option("--invert")] = False,
    debug: Annotated[Path | None, typer.Option("--debug")] = None,
) -> None:
    """Convert an image into terminal avatar text."""
    try:
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
            debug=debug,
        )
    except Exception as exc:
        _fail(str(exc))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    else:
        stdout.print(rendered, end="")


@app.command("pack")
def pack_command(
    directory: Path,
    name: Annotated[str | None, typer.Option("--name")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    default_mood: Annotated[str, typer.Option("--default-mood")] = "neutral",
    height: Annotated[int, typer.Option("--height", min=1)] = 32,
    mode: Annotated[str, typer.Option("--mode")] = "braille",
    background: Annotated[str, typer.Option("--background")] = "alpha",
    crop: Annotated[bool, typer.Option("--crop/--no-crop")] = True,
    pad: Annotated[int, typer.Option("--pad", min=0)] = 0,
    threshold: Annotated[int, typer.Option("--threshold", min=0, max=255)] = 128,
    contrast: Annotated[float, typer.Option("--contrast", min=0.1)] = 1.0,
    invert: Annotated[bool, typer.Option("--invert")] = False,
) -> None:
    """Generate a character pack from a directory of mood images."""
    character_name = name or directory.name.replace("-", " ").replace("_", " ").title()
    target = out or Path("characters") / character_name.lower().replace(" ", "_")
    try:
        moods = generate_pack(
            directory,
            target,
            name=character_name,
            default_mood=default_mood,
            height=height,
            mode=mode,
            background=background,
            crop=crop,
            pad=pad,
            threshold=threshold,
            contrast=contrast,
            invert=invert,
        )
    except Exception as exc:
        _fail(str(exc))
    stdout.print(f"wrote {target} ({', '.join(moods)})")


@app.command()
def validate(character: str) -> None:
    """Validate a character pack."""
    issues = validate_character(character)
    for issue in issues:
        stdout.print(f"{issue.level}: {issue.message}")
    if any(issue.level == "error" for issue in issues):
        raise typer.Exit(1)


@app.command()
def preview(
    character: str,
    mood: Annotated[str | None, typer.Option("--mood")] = None,
    text: Annotated[str, typer.Option("--text")] = "Hello from Familiar.",
    layouts: Annotated[bool, typer.Option("--layouts")] = False,
) -> None:
    """Preview moods or layouts for a character."""
    try:
        familiar = Familiar.load(character)
        moods = [mood] if mood else familiar.available_moods()
        layout_names = (
            ["avatar_above", "avatar_left", "bubble_only", "avatar_only", "compact"]
            if layouts
            else [None]
        )
        sections = []
        for current_mood in moods:
            for layout in layout_names:
                label = current_mood if layout is None else f"{current_mood} / {layout}"
                rendered = familiar.say(current_mood, text, layout=layout)
                sections.append(f"== {label} ==\n{rendered}")
        stdout.print("\n\n".join(sections))
    except (FamiliarError, ValueError) as exc:
        _fail(str(exc))


@app.command("forge-preview")
def forge_preview(
    image: Path,
    heights: Annotated[str, typer.Option("--heights")] = "16,24,32",
    modes: Annotated[str, typer.Option("--modes")] = "braille,ascii,block",
) -> None:
    """Compare render modes and heights for an image."""
    try:
        sections = []
        for mode in [part.strip() for part in modes.split(",") if part.strip()]:
            height_values = [
                part.strip() for part in heights.split(",") if part.strip()
            ]
            for height_text in height_values:
                height = int(height_text)
                sections.append(
                    f"== {mode} / {height} ==\n"
                    f"{render_image(image, height=height, mode=mode)}"
                )
        stdout.print("\n".join(sections))
    except Exception as exc:
        _fail(str(exc))


def main() -> None:
    args = sys.argv[1:]
    if args and not args[0].startswith("-") and args[0] not in COMMANDS:
        parsed = _parse_direct_args(args)
        _render_say(
            str(parsed["character"]),
            str(parsed["mood"]),
            str(parsed["text"]),
            layout=parsed["layout"] if isinstance(parsed["layout"], str) else None,
            box=parsed["box"] if isinstance(parsed["box"], str) else None,
            max_width=(
                parsed["max_width"] if isinstance(parsed["max_width"], int) else None
            ),
            plain=bool(parsed["plain"]),
            title=bool(parsed["title"]),
        )
        return
    app()


if __name__ == "__main__":
    main()
