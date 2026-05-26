"""Fixture 06 — off-by-one bug class.

``first_n`` is supposed to return the first ``n`` elements but uses a
slice that returns one fewer. The bug is the classic off-by-one on the
upper bound.
"""


def first_n(items: list, n: int) -> list:
    return items[: n - 1]
