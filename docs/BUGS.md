# Bugs And Limitations

* `rembg` background removal is optional and not installed by default. Use
  `familiar[background]` to enable `--background remove`.
* `uv` is requested by the project task list, but this local environment did not
  have the `uv` executable available during implementation.
* Braille rendering is monochrome. ANSI color is deferred by design.
* Release automation builds artifacts on tags, but publishing is intentionally
  not configured yet.
* `chafa.py` is a Python wrapper and still requires `libchafa` at runtime. On
  systems without `libchafa`, Familiar can use a `chafa` executable on `PATH`
  for `--mode chafa`.
