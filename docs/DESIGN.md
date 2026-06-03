# Familiar

Terminal companions for humans and machines.

## Overview

Familiar is a terminal character framework inspired by cowsay, shell culture, BBS artwork, roguelikes, and terminal user interfaces.

A Familiar is a terminal-native character that can display:

* avatar art
* moods / expressions
* speech bubbles
* status messages
* notifications
* command output summaries

Familiars can be rendered from shell scripts, Python programs, AI agents, terminal applications, or interactive tools.

The project consists of two major components:

1. Runtime renderer
2. Asset generation pipeline

The runtime renderer displays characters.

The asset generation pipeline converts images into terminal-native avatar assets.

Familiar is not an agent framework.

Familiar does not perform reasoning.

Familiar is presentation infrastructure.

---

# Design Goals

## Primary Goals

* Terminal-first
* Human-readable assets
* Easy scripting
* Easy Python integration
* Character packs
* Mood support
* Modern Unicode support
* Local-first

## Non Goals

* VTuber software
* Real-time animation
* Character editors
* Live image generation
* Agent orchestration
* LLM integration
* Voice synthesis

Those may be built on top of Familiar but are not part of Familiar itself.

---

# Philosophy

Unix tools separate concerns.

Familiar follows the same approach.

A shell, agent, application, or AI system decides:

* what happened
* what should be said
* what mood to display

Familiar decides:

* how the character looks
* how text is displayed
* how the output is rendered

Example:

```python
mood = determine_mood(build_result)

print(
    proxy.say(
        mood=mood,
        text="Build completed."
    )
)
```

Familiar does not determine the mood.

It renders the mood.

---

# Concepts

## Familiar

A terminal character.

Examples:

* Proxy
* Lain
* Telly
* Wizard
* Robot
* Cat

A Familiar contains:

* metadata
* styles
* layouts
* expression assets

---

## Expression

An avatar variant.

Examples:

* neutral
* happy
* excited
* curious
* surprised
* sad
* angry

Each expression is stored as terminal-native text.

Example:

```text
neutral.txt
angry.txt
curious.txt
```

---

## Layout

Controls how text and avatars are arranged.

Examples:

```text
avatar_left
avatar_above
bubble_only
avatar_only
compact
```

---

## Speech Bubble

A formatted text container.

Example:

```text
┌─ Proxy ─────────────────────┐
│ Build completed successfully│
└─────────────────────────────┘
```

Bubble styles are configurable.

---

# Runtime

## CLI

Basic usage:

```bash
familiar say proxy neutral "Hello world"
```

Example:

```bash
familiar say proxy curious \
  "The build failed. Want me to investigate?"
```

Output:

```text
<avatar>

┌─ Proxy ─────────────────────────┐
│ The build failed. Want me to    │
│ investigate?                    │
└─────────────────────────────────┘
```

---

## Python API

```python
from familiar import Familiar

proxy = Familiar.load("proxy")

print(
    proxy.say(
        mood="curious",
        text="The build failed."
    )
)
```

---

# Asset Format

A Familiar is a directory.

Example:

```text
proxy/
├── familiar.py
├── neutral.txt
├── curious.txt
├── angry.txt
├── sad.txt
└── metadata.json
```

---

## Character Definition

```python
NAME = "Proxy"

DEFAULT_MOOD = "neutral"

LAYOUT = "avatar_above"

MOODS = {
    "neutral": "neutral.txt",
    "curious": "curious.txt",
    "angry": "angry.txt",
    "sad": "sad.txt"
}
```

Assets are intentionally simple.

Users should be able to edit them in a text editor.

---

# Forge

Forge converts images into Familiar assets.

Example:

```bash
familiar forge proxy.png \
  --height 32 \
  --mode braille
```

Output:

```text
neutral.txt
```

---

## Supported Renderers

### Braille

Default renderer.

Uses Unicode Braille Pattern characters.

Highest fidelity.

Best for character portraits.

---

### ASCII

Traditional brightness mapping.

Maximum compatibility.

---

### Block

Uses:

```text
░▒▓█
```

Strong silhouette rendering.

---

# Background Removal

Foreground extraction is a first-class feature.

The primary use case is:

```text
character portrait
without background
```

Transparent pixels become spaces.

The output should contain only the character.

---

# Future Extensions

The following are explicitly out of scope for v1 but should remain possible:

* ANSI color
* Animated expressions
* Character repositories
* Theme systems
* Mood classifiers
* LLM integrations
* Exoshell integrations
* Status widgets
* Progress indicators

---

# Roadmap

## Phase 1

Runtime renderer.

* CLI
* Python API
* Layouts
* Speech bubbles
* Character packs

## Phase 2

Forge.

* Image loading
* Foreground extraction
* Braille renderer
* Asset generation

## Phase 3

Polish.

* ANSI color
* Packaging
* Preview tooling
* Asset validation

---

# Success Criteria

A user can:

1. Create a character pack.
2. Generate terminal avatars from images.
3. Display moods from Python.
4. Display moods from shell scripts.
5. Integrate Familiar into another project.

without needing an AI model, network connection, or graphical interface.
