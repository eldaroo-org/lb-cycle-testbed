"""Fixture 03 — type-error bug class.

``compute`` returns a string in one branch and an int in another, then
the test adds the result to an int. The branch mismatch produces a
``TypeError`` at runtime on the string branch.
"""


def compute(n: int) -> int:
    if n > 0:
        return str(n)  # type: ignore[return-value]
    return 0
