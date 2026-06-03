# Python API

```python
from familiar import Familiar

proxy = Familiar.load("proxy")

print(proxy.avatar("neutral"))
print(proxy.bubble("Hello."))
print(proxy.say("curious", "What are we working on today?"))
print(proxy.available_moods())
```

`Familiar.load(name)` searches local project characters first, then configured
user paths, then bundled package characters.

The runtime does not infer mood. Callers decide which mood to render.
