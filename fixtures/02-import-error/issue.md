# Fixture 02 — ImportError on missing sibling

<!-- fixture-id: 02-import-error -->

## Failure

`fixtures/02-import-error/module.py` imports `nonexistent_sibling` which does
not exist:

```
from . import nonexistent_sibling  # noqa: F401
```

Running `pytest fixtures/02-import-error/test_module.py` fails at import time
with `ModuleNotFoundError`.

## Expected fix shape

Either:
1. Create `fixtures/02-import-error/nonexistent_sibling.py` with a `format_greeting(name)` function returning a string, OR
2. Remove the dead import and rewrite `greet()` to return `f"Hello, {name}"` directly.

Either path is acceptable; reviewer judges on whichever the fix lands on.

## Verify

After the fix, `pytest fixtures/02-import-error/test_module.py` must pass.
