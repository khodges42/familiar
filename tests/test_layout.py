from familiar.layout import render_layout


def test_avatar_above_layout():
    assert render_layout("A", "B", layout="avatar_above") == "A\n\nB"


def test_avatar_left_layout():
    rendered = render_layout("A\nAA", "B", layout="avatar_left")

    assert rendered.splitlines()[0] == "A   B"


def test_avatar_above_centers_narrow_bubble():
    rendered = render_layout("  A  ", "B", layout="avatar_above")

    assert rendered == "  A  \n\n  B"


def test_avatar_left_uses_display_width():
    rendered = render_layout("界\n界界", "B", layout="avatar_left")

    assert rendered.splitlines()[0] == "界    B"
