# Fixture 06 — Off-by-one in list slice

<!-- fixture-id: 06-off-by-one -->

## Failure

`fixtures/06-off-by-one/module.py::first_n` returns the first `n - 1`
items instead of `n`:

```python
return items[: n - 1]   # bug: returns n-1 items
```

The test expects `first_n([1,2,3,4,5], 3) == [1,2,3]` and currently gets
`[1, 2]`.

## Expected fix shape

`return items[:n]`.

## Verify

`pytest fixtures/06-off-by-one/test_module.py` must pass after the fix.
