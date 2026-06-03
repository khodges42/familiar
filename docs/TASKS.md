Yep — no Exoshell. **Familiar stands alone.**

# Familiar Full Task List

## P0 — Project Setup

* [ ] Create repository
* [ ] Add Python 3.11+ requirement
* [ ] Add `pyproject.toml`
* [ ] Use `uv` for dependency management
* [ ] Add `ruff`
* [ ] Add `pytest`
* [ ] Add `typer`
* [ ] Add `rich`
* [ ] Add `Pillow`
* [ ] Add basic package structure

```text
familiar/
  familiar/
    __init__.py
    cli.py
    runtime/
    layout/
    bubble/
    forge/
    render/
    character/
  characters/
  examples/
  tests/
  docs/
```

* [ ] Add `README.md`
* [ ] Add `LICENSE`
* [ ] Add `docs/design.md`
* [ ] Add `docs/tasks.md`

Success:

```bash
familiar --help
```

works.

---

# P1 — CLI Skeleton

* [ ] Implement top-level CLI
* [ ] Support command form:

```bash
familiar CHARACTER MOOD TEXT
```

* [ ] Support explicit form:

```bash
familiar say CHARACTER MOOD TEXT
```

* [ ] Add `--version`
* [ ] Add `--help`
* [ ] Add useful error messages
* [ ] Add shell-friendly stdout-only output
* [ ] Ensure errors go to stderr

Success:

```bash
familiar proxy neutral "Hello world"
```

dispatches correctly.

---

# P2 — Character Pack Format

* [ ] Define character directory format
* [ ] Define required files
* [ ] Define optional files
* [ ] Define mood naming conventions

Example:

```text
proxy/
  familiar.py
  neutral.txt
  curious.txt
  angry.txt
  sad.txt
  surprised.txt
  excited.txt
```

* [ ] Define required metadata fields
* [ ] Define optional style fields
* [ ] Define default mood fallback
* [ ] Define missing mood behavior

Example `familiar.py`:

```python
NAME = "Proxy"

DEFAULT_MOOD = "neutral"

MOODS = {
    "neutral": "neutral.txt",
    "curious": "curious.txt",
    "angry": "angry.txt",
    "sad": "sad.txt",
    "surprised": "surprised.txt",
    "excited": "excited.txt",
}

STYLE = {
    "layout": "avatar_above",
    "box": "single",
    "max_width": 72,
    "padding": 1,
}
```

Success:

Character packs are plain files and editable by hand.

---

# P3 — Character Loader

* [ ] Load character by name
* [ ] Search local project characters
* [ ] Search user character directory
* [ ] Search bundled examples

Suggested lookup order:

```text
./characters/
~/.config/familiar/characters/
package examples
```

* [ ] Load `familiar.py`
* [ ] Validate required fields
* [ ] Load mood asset
* [ ] Fallback to default mood
* [ ] Return clear error if character is missing
* [ ] Return clear error if default mood is missing

Success:

```bash
familiar proxy curious "Hello"
```

loads `proxy/curious.txt`.

---

# P4 — Speech Bubble Renderer

* [ ] Implement text wrapping
* [ ] Implement single-line box style
* [ ] Implement rounded box style
* [ ] Implement ASCII-only box style
* [ ] Implement title support
* [ ] Implement padding
* [ ] Implement max width
* [ ] Preserve newlines in input text
* [ ] Handle long words
* [ ] Handle empty text

Box styles:

```text
single
rounded
ascii
none
```

Success:

```text
┌─ Proxy ─────────────┐
│ Hello world         │
└─────────────────────┘
```

---

# P5 — Layout Renderer

Implement layouts:

* [ ] `avatar_above`
* [ ] `avatar_left`
* [ ] `bubble_only`
* [ ] `avatar_only`
* [ ] `compact`

Required behavior:

* [ ] Preserve avatar spacing
* [ ] Do not trim intentional whitespace inside art
* [ ] Align bubble with avatar
* [ ] Handle avatars wider than bubbles
* [ ] Handle bubbles wider than avatars

Success:

```bash
familiar proxy neutral "Hello"
familiar proxy neutral "Hello" --layout avatar_left
familiar proxy neutral "Hello" --layout bubble_only
```

all render cleanly.

---

# P6 — Python Runtime API

* [ ] Add `Familiar` class
* [ ] Add `Familiar.load(name)`
* [ ] Add `familiar.say(mood, text)`
* [ ] Add `familiar.avatar(mood)`
* [ ] Add `familiar.bubble(text)`
* [ ] Add `familiar.available_moods()`
* [ ] Add typed return values where helpful
* [ ] Add docstrings

Example:

```python
from familiar import Familiar

proxy = Familiar.load("proxy")

print(proxy.say(
    mood="curious",
    text="What are we working on today?"
))
```

Success:

Runtime works without invoking CLI.

---

# P7 — Forge: Basic Image Renderer

* [ ] Add `familiar forge IMAGE`
* [ ] Load image with Pillow
* [ ] Convert image to grayscale
* [ ] Resize by terminal character height
* [ ] Render classic ASCII brightness map
* [ ] Write to stdout by default
* [ ] Support `--out`

CLI:

```bash
familiar forge proxy.png --height 32 --mode ascii --out neutral.txt
```

Success:

Image becomes real text.

---

# P8 — Alpha-Aware Rendering

* [ ] Detect image alpha channel
* [ ] Treat transparent pixels as spaces
* [ ] Crop to visible foreground
* [ ] Add `--crop / --no-crop`
* [ ] Add `--pad`
* [ ] Preserve transparent interior gaps
* [ ] Do not render full image rectangle unless requested

Success:

Transparent-background character image produces character-only terminal art.

---

# P9 — Background Removal

* [ ] Add optional `rembg` dependency
* [ ] Add `--background remove`
* [ ] Add `--background keep`
* [ ] Add `--background alpha`
* [ ] Add `--background threshold`
* [ ] Save intermediate debug image with `--debug`
* [ ] Document best input image style

Success:

Plain-background character portrait becomes foreground-only terminal art.

---

# P10 — Braille Renderer

* [ ] Implement Unicode Braille rendering
* [ ] Map 2×4 pixel blocks to Braille codepoints
* [ ] Add threshold controls
* [ ] Add contrast controls
* [ ] Add invert option
* [ ] Add tests for Braille bit mapping
* [ ] Make Braille the default forge mode

CLI:

```bash
familiar forge proxy.png --height 32 --mode braille
```

Success:

Braille output looks better than ASCII for portraits.

---

# P11 — Block Renderer

* [ ] Implement block/shade renderer
* [ ] Support glyph ramp:

```text
 ░▒▓█
```

* [ ] Add `--mode block`
* [ ] Add tests

Success:

```bash
familiar forge proxy.png --mode block
```

works.

---

# P12 — Pack Generator

* [ ] Add `familiar pack DIR`
* [ ] Detect mood images by filename
* [ ] Generate `.txt` avatar files
* [ ] Generate `familiar.py`
* [ ] Generate `metadata.json`
* [ ] Support custom character name
* [ ] Support custom default mood
* [ ] Support output directory

Input:

```text
proxy-images/
  neutral.png
  curious.png
  angry.png
  sad.png
```

Command:

```bash
familiar pack proxy-images --name Proxy --out proxy
```

Output:

```text
proxy/
  familiar.py
  neutral.txt
  curious.txt
  angry.txt
  sad.txt
  metadata.json
```

Success:

Generated pack can immediately be used:

```bash
familiar proxy neutral "Hello"
```

---

# P13 — Validation

* [ ] Add `familiar validate CHARACTER`
* [ ] Check required files
* [ ] Check default mood exists
* [ ] Check all mood files exist
* [ ] Check invalid layout names
* [ ] Check invalid box names
* [ ] Check empty avatar files
* [ ] Check suspiciously wide avatars
* [ ] Check unsupported characters optionally

Success:

```bash
familiar validate proxy
```

reports useful results.

---

# P14 — Preview Tools

* [ ] Add `familiar preview CHARACTER`
* [ ] Preview all moods
* [ ] Preview a single mood
* [ ] Preview all layouts
* [ ] Add `familiar forge-preview IMAGE`
* [ ] Compare render modes
* [ ] Compare heights

Example:

```bash
familiar forge-preview proxy.png --heights 16,24,32,48
```

Success:

User can tune art without manually rerunning many commands.

---

# P15 — Configuration

* [ ] Add config file support
* [ ] Support user character directory
* [ ] Support default box style
* [ ] Support default layout
* [ ] Support default max width

Config path:

```text
~/.config/familiar/config.toml
```

Example:

```toml
[defaults]
layout = "avatar_above"
box = "single"
max_width = 72

[paths]
characters = "~/.config/familiar/characters"
```

Success:

Users can install and reuse familiar packs globally.

---

# P16 — Documentation

* [ ] Write README
* [ ] Add quickstart
* [ ] Add CLI examples
* [ ] Add Python API examples
* [ ] Add character pack guide
* [ ] Add image prompt guide
* [ ] Add forge guide
* [ ] Add troubleshooting guide
* [ ] Add examples gallery

Important docs:

```text
docs/
  design.md
  tasks.md
  character-packs.md
  forge.md
  prompts.md
  python-api.md
```

---

# P17 — Example Familiar

* [ ] Create bundled `proxy` example
* [ ] Include at least three moods
* [ ] Include simple hand-written avatar fallback
* [ ] Include generated Braille avatar
* [ ] Include example character definition

Moods:

```text
neutral
curious
angry
```

Success:

Fresh install includes a working demo:

```bash
familiar proxy curious "Hello from Familiar."
```

---

# P18 — Testing

* [ ] Test character loading
* [ ] Test missing character errors
* [ ] Test missing mood fallback
* [ ] Test bubble wrapping
* [ ] Test all layouts
* [ ] Test ASCII renderer
* [ ] Test Braille renderer
* [ ] Test alpha handling
* [ ] Test pack generation
* [ ] Test validation command
* [ ] Snapshot test rendered output

---

# P19 — Packaging

* [ ] Add console script entrypoint
* [ ] Verify install with `uv tool install`
* [ ] Verify install with `pipx`
* [ ] Build wheel
* [ ] Add release workflow
* [ ] Add version command

Success:

```bash
uv tool install .
familiar --version
```

works.

---

# P20 — Polish

* [ ] Better error messages
* [ ] Better terminal width detection
* [ ] Graceful Unicode fallback
* [ ] ASCII-only mode
* [ ] Debug output for forge
* [ ] Golden examples
* [ ] Screenshot examples
* [ ] Add `--plain`
* [ ] Add `--no-title`
* [ ] Add `--max-width`
* [ ] Add `--layout`
* [ ] Add `--box`

---

# Deferred Features

Do not build in v1.

* [ ] ANSI color
* [ ] Animation
* [ ] Mood classifier
* [ ] LLM integration
* [ ] Voice
* [ ] Web UI
* [ ] Character marketplace
* [ ] Live image generation
* [ ] Terminal input handling
* [ ] Agent behavior

---

# Recommended First Vertical Slice

Build this first:

* [ ] CLI skeleton
* [ ] Character loader
* [ ] Static example character
* [ ] Bubble renderer
* [ ] `avatar_above` layout
* [ ] Python API
* [ ] Basic tests

End result:

```bash
familiar proxy neutral "Welcome to Familiar."
```

Then build forge.

Reason:

The runtime defines the product. Forge is the asset pipeline.
