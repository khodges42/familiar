# Character Packs

A Familiar character pack is a plain directory containing a Python definition
file and text avatar assets.

```text
proxy/
  familiar.py
  neutral.txt
  curious.txt
  angry.txt
  metadata.json
```

`familiar.py` must define:

```python
NAME = "Proxy"
DEFAULT_MOOD = "neutral"
MOODS = {
    "neutral": "neutral.txt",
}
```

`STYLE` is optional:

```python
STYLE = {
    "layout": "avatar_above",
    "box": "single",
    "max_width": 72,
    "padding": 1,
}
```

Mood names should use lowercase letters, numbers, and underscores. Missing
requested moods fall back to the default mood. A missing default mood is an
error.
