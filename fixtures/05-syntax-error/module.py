"""Fixture 05 — syntax-error bug class.

The function declaration is missing a colon. Python refuses to compile
the module at import time.
"""


def add(a: int, b: int) -> int
    return a + b
