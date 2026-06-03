from familiar import Familiar


def test_proxy_loads():
    proxy = Familiar.load("proxy")

    assert proxy.name == "Proxy"
    assert "neutral" in proxy.available_moods()


def test_missing_mood_falls_back_to_default():
    proxy = Familiar.load("proxy")

    assert proxy.avatar("missing") == proxy.avatar("neutral")


def test_say_renders_text():
    proxy = Familiar.load("proxy")

    rendered = proxy.say("neutral", "Hello")

    assert "Hello" in rendered
    assert "Proxy" in rendered
