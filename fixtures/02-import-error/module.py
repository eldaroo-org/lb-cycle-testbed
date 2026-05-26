"""Fixture 02 — import-error bug class.

The module imports from a sibling module that does not exist. autodev's
job is to either create the sibling, switch to a real import, or remove
the dead import path.
"""
from . import nonexistent_sibling  # noqa: F401


def greet(name: str) -> str:
    return nonexistent_sibling.format_greeting(name)
