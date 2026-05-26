# Fixture 05 — SyntaxError in module

<!-- fixture-id: 05-syntax-error -->

## Failure

`fixtures/05-syntax-error/module.py` is missing a colon on the function
declaration:

```python
def add(a: int, b: int) -> int
    return a + b
```

Python refuses to parse the module:

```
SyntaxError: expected ':'
```

## Expected fix shape

Add the colon: `def add(a: int, b: int) -> int:`.

## Verify

`pytest fixtures/05-syntax-error/test_module.py` must pass after the fix.
