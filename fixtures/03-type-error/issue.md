# Fixture 03 — TypeError from inconsistent return type

<!-- fixture-id: 03-type-error -->

## Failure

`fixtures/03-type-error/module.py::compute` returns a string when `n > 0`
and an int otherwise. The test adds the result to an int and crashes:

```
TypeError: unsupported operand type(s) for +: 'str' and 'int'
```

## Expected fix shape

Remove the `str()` wrap so `compute(n: int) -> int` always returns an int.

## Verify

`pytest fixtures/03-type-error/test_module.py` must pass.
