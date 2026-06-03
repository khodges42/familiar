# Configuration

Familiar reads optional user defaults from:

```text
~/.config/familiar/config.toml
```

Example:

```toml
[defaults]
layout = "avatar_above"
box = "single"
max_width = 72
padding = 1

[paths]
characters = "~/.config/familiar/characters"
```

Character lookup order is:

```text
./characters/
$FAMILIAR_CHARACTER_PATH
configured user character directory
package characters/
```
