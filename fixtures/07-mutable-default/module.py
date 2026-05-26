"""Fixture 07 — mutable-default-argument bug class.

The classic Python footgun: ``append_default`` uses a mutable default
that persists across calls. Two successive calls without an explicit
``container`` accumulate state.
"""


def append_default(value, container=[]):
    container.append(value)
    return container
