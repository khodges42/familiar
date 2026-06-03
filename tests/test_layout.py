from familiar.layout import render_layout


def test_avatar_above_layout():
    assert render_layout("A", "B", layout="avatar_above") == "A\n\nB"


def test_avatar_left_layout():
    rendered = render_layout("A\nAA", "B", layout="avatar_left")

    assert rendered.splitlines()[0] == "A   B"
