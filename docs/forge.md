# Forge

Forge converts images into terminal-native text assets.

```bash
familiar forge image.png --height 32 --mode braille
```

Modes:

* `braille`: default and highest fidelity for portraits.
* `ascii`: classic brightness ramp.
* `block`: shade blocks for stronger silhouettes.

Alpha handling is enabled by default. Transparent pixels render as spaces, and
visible content is cropped unless `--no-crop` is passed.

Background options:

* `alpha`: use the input alpha channel.
* `keep`: keep the full image background.
* `threshold`: treat pixels similar to the top-left pixel as background.
* `remove`: use optional `rembg`; install `familiar[background]`.

Useful tuning flags:

```bash
familiar forge image.png --height 40 --mode braille --contrast 1.4 --threshold 120
familiar forge-preview image.png --heights 16,24,32 --modes braille,ascii,block
```
