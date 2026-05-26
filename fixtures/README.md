# Fixtures

Each subdirectory carries one deliberately-broken fixture that lb-cycle's
sandbox-mode autodev practices on. The naming convention is
`NN-<bug-class>/` so the order in `ls` matches the chronological order
seeding produces them.

## What each fixture contains

- `module.py` — the broken Python that catches the bug. Lives outside
  `src/` so it does not affect the package's importability; the
  fixture's test imports it via `pathlib`.
- `test_module.py` — the failing pytest case that catches the bug.
- `issue.md` — the GitHub issue body the reset-and-seed script files
  when staging this fixture. Includes the failing-test repro, the
  expected fix shape, and a `<!-- fixture-id: NN-name -->` marker the
  must_fail_without_fix probe greps to map issue back to fixture.

## What lives where

- The original `tests/test_known_failure.py` + `src/lb_cycle_testbed/`
  pair is **fixture #1** (the assertion-failure smoke). It stays under
  the canonical pytest layout for backwards compatibility with the
  spec-008-era harness; new fixtures live here under `fixtures/` so
  `pytest` does NOT collect them by default and each can be exercised
  in isolation by the probe.

## Failure classes covered

| # | Bug class | Probe expected output |
|---|---|---|
| 01 | Assertion failure | `tests/test_known_failure.py::test_the_answer_is_forty_two` FAILED |
| 02 | Import error | `ModuleNotFoundError` on `from missing_pkg import ...` |
| 03 | Type error | `TypeError: unsupported operand type(s) for +: 'int' and 'str'` |
| 04 | Missing dependency | `ModuleNotFoundError: No module named 'requests'` |
| 05 | Syntax error | `SyntaxError: invalid syntax` at module import time |
| 06 | Off-by-one | List slice returns N-1 items instead of N |
| 07 | Mutable default | List default arg shared across calls |
| 08 | Heal jobs-file (historical repro) | `FileNotFoundError: jobs.json` (the spec-012 live bug, fixed in prod 2026-05-26 via PR #635; preserved here as historical fixture) |
