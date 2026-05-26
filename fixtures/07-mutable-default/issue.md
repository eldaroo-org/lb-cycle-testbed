# Fixture 07 — Mutable default argument leaks across calls

<!-- fixture-id: 07-mutable-default -->

## Failure

`fixtures/07-mutable-default/module.py::append_default` uses a mutable
default `container=[]`. The same list is reused across calls so two
successive calls without an explicit `container` accumulate state.

## Expected fix shape

```python
def append_default(value, container=None):
    if container is None:
        container = []
    container.append(value)
    return container
```

## Verify

`pytest fixtures/07-mutable-default/test_module.py` must pass after the fix.
