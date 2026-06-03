from familiar.bubble import render_bubble


def test_bubble_wraps_and_preserves_newlines():
    rendered = render_bubble("hello world\nagain", title="Proxy", max_width=16)

    assert "Proxy" in rendered
    assert "hello" in rendered
    assert "again" in rendered


def test_bubble_handles_long_words():
    rendered = render_bubble("abcdefghij", max_width=8)

    assert "abcd" in rendered
    assert "efgh" in rendered
