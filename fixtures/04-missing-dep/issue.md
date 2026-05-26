# Fixture 04 — Missing runtime dependency

<!-- fixture-id: 04-missing-dep -->

## Failure

`fixtures/04-missing-dep/module.py` imports `lb_cycle_definitely_missing_pkg`
which is not on PyPI and not in pyproject.toml:

```
ModuleNotFoundError: No module named 'lb_cycle_definitely_missing_pkg'
```

## Expected fix shape

Drop the broken import and rewrite `normalize(text)` to return the
text lower-cased and stripped:

```python
def normalize(text: str) -> str:
    return text.strip().lower()
```

(The fixture is a tiny stand-in for the "missing dependency" failure
class; any reasonable fix that makes the module import cleanly and the
test pass is acceptable.)

## Verify

`pytest fixtures/04-missing-dep/test_module.py` must pass after the fix.
