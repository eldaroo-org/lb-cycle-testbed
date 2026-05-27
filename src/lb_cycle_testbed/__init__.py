"""lb-cycle-testbed — sandbox harness target for spec 011."""

__version__ = "0.0.1"


def the_answer() -> int:
    """Return the canonical sandbox answer.

    The deliberately-failing test asserts this returns 42. The current
    implementation returns 0, so the test fails. autodev's job in the
    sandbox loop is to fix this function and prove the round-trip.
    """
    return 42
