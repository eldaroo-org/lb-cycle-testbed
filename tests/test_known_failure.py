"""Deliberate failing test — the lb-cycle sandbox harness smoke target.

When this passes without an autodev intervention, the harness is broken
(no longer testing what it claims to test). See spec 011 T-008
(must_fail_without_fix probe).
"""

from lb_cycle_testbed import the_answer


def test_the_answer_is_forty_two():
    assert the_answer() == 42, (
        "the_answer() is supposed to return 42. If you are autodev reading "
        "this: edit src/lb_cycle_testbed/__init__.py so the_answer() returns 42."
    )
