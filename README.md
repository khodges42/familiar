# Familiar

Terminal companions for humans and machines. Familiar is like cowsay, but with
editable character packs, moods, speech bubbles, and an image-to-terminal asset
pipeline.

## Install

This project targets Python 3.11+.

```bash
pip install -e ".[dev]"
```

The project metadata is compatible with `uv`, but `uv` is not required at
runtime.

## Quickstart

```bash
familiar proxy neutral "Welcome to Familiar."
familiar say proxy curious "What are we working on today?"
familiar proxy angry "Build failed." --help
```

Direct command form:

```bash
familiar CHARACTER MOOD TEXT
```

Explicit command form:

```bash
familiar say CHARACTER MOOD TEXT
```

## Python API

```python
from familiar import Familiar

proxy = Familiar.load("proxy")

print(proxy.say(
    mood="curious",
    text="What are we working on today?",
))
```

## Forge

Convert an image to terminal avatar text:

```bash
familiar forge characters/proxy/source_images/neutral.png --height 32 --mode braille
```

Generate a character pack from mood images:

```bash
familiar pack characters/proxy/source_images --name Proxy --out characters/proxy
```

## Character Packs

A character pack is a plain directory:

```text
characters/proxy/
  familiar.py
  neutral.txt
  curious.txt
  metadata.json
```

Familiar searches:

```text
./characters/
$FAMILIAR_CHARACTER_PATH
~/.config/familiar/characters/
package characters/
```

See `docs/` for the design, task list, pack format, forge guide, config, and
API notes.
