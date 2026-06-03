from __future__ import annotations

from dataclasses import dataclass

from familiar.bubble import render_bubble
from familiar.character import CharacterPack, load_character
from familiar.layout import render_layout


@dataclass(frozen=True)
class Familiar:
    """A loaded Familiar character pack."""

    pack: CharacterPack

    @classmethod
    def load(cls, name: str) -> Familiar:
        """Load a character pack by slug."""
        return cls(load_character(name))

    @property
    def name(self) -> str:
        """Display name for the character."""
        return self.pack.name

    def available_moods(self) -> list[str]:
        """Return all moods declared by this character."""
        return self.pack.available_moods()

    def avatar(self, mood: str | None = None) -> str:
        """Return terminal avatar art for a mood."""
        return self.pack.avatar(mood)

    def bubble(
        self,
        text: str,
        *,
        box: str | None = None,
        max_width: int | None = None,
        padding: int | None = None,
        title: str | None = None,
    ) -> str:
        """Render a speech bubble using this character's default style."""
        style = self.pack.style
        return render_bubble(
            text,
            title=self.name if title is None else title,
            box=box or str(style["box"]),
            max_width=max_width or int(style["max_width"]),
            padding=padding if padding is not None else int(style["padding"]),
        )

    def say(
        self,
        mood: str,
        text: str,
        *,
        layout: str | None = None,
        box: str | None = None,
        max_width: int | None = None,
        padding: int | None = None,
        title: str | None = None,
    ) -> str:
        """Render an avatar and speech bubble."""
        style = self.pack.style
        avatar = self.avatar(mood)
        bubble = self.bubble(
            text,
            box=box,
            max_width=max_width,
            padding=padding,
            title=title,
        )
        return render_layout(
            avatar,
            bubble,
            layout=layout or str(style["layout"]),
        )
