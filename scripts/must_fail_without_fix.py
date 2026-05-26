#!/usr/bin/env python3
"""must_fail_without_fix.py — AC6 falsifiability probe (spec 011, T-008, #613).

Walks every fixture under ``fixtures/NN-<name>/`` AND the canonical
``tests/test_known_failure.py`` and runs each one's test in isolation.
The contract is inverted: each fixture's test MUST fail when run
against the unfixed baseline. A green test means the bug it claims to
catch is no longer reproducing — either the language got smarter, a
dependency moved, or someone accidentally checked in the fix.

Exit codes:
  0 — every fixture's test failed as expected.
  1 — at least one fixture green-passed; bug class no longer reproduces.
  2 — pytest itself crashed or the runner could not find a fixture.

When a fixture green-passes, the probe prints the offending fixture id
and a one-line summary so the operator can decide: bump the fixture,
delete the fixture, or relax the assertion.

Spec 011 risk R4 (Sage): fixture-decay-via-Claude-getting-smarter. This
probe IS the defense. It runs BEFORE reset-and-seed.sh stages new
issues so the harness never seeds a fixture that proves nothing.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURES_ROOT = ROOT / "fixtures"
KNOWN_FAILURE_TEST = ROOT / "tests" / "test_known_failure.py"


def _discover() -> list[Path]:
    """Return every fixture test path the probe must exercise.

    Order matches reset-and-seed.sh's seeding order: fixture #01 (the
    canonical assertion failure under tests/) first, then numerical
    fixtures/NN-* directories.
    """
    targets: list[Path] = []
    if KNOWN_FAILURE_TEST.exists():
        targets.append(KNOWN_FAILURE_TEST)
    for entry in sorted(FIXTURES_ROOT.glob("[0-9][0-9]-*")):
        test_file = entry / "test_module.py"
        if test_file.exists():
            targets.append(test_file)
    return targets


def _run_test(path: Path) -> int:
    """Return pytest's exit code for a single test file run in isolation."""
    cmd = [sys.executable, "-m", "pytest", str(path), "-q", "--no-header"]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        print(f"PROBE-CRASH: pytest invocation failed: {exc}", file=sys.stderr)
        sys.exit(2)
    if proc.returncode not in (0, 1, 2, 3, 4, 5):
        # pytest exits 0 on pass, 1 on fail, 2-5 on collection / usage
        # errors. Anything else is unexpected and should surface.
        print(
            f"PROBE-CRASH: pytest returned unexpected exit code "
            f"{proc.returncode} for {path}",
            file=sys.stderr,
        )
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(2)
    return proc.returncode


def main() -> int:
    targets = _discover()
    if not targets:
        print("PROBE-CRASH: no fixture tests discovered", file=sys.stderr)
        return 2

    print(f"must_fail_without_fix: walking {len(targets)} fixture(s)")
    green_passes: list[Path] = []
    for path in targets:
        rc = _run_test(path)
        rel = path.relative_to(ROOT)
        if rc == 0:
            green_passes.append(path)
            print(f"  FAIL — {rel} (green-passed; fixture no longer proves)")
        else:
            print(f"  ok   — {rel} (failed as expected; rc={rc})")

    if green_passes:
        print()
        print("fixture_no_longer_proves_anything")
        for path in green_passes:
            print(f"  - {path.relative_to(ROOT)}")
        print()
        print(
            "Each green-passed fixture above is no longer producing the "
            "bug it claims to catch. Refresh the fixture so the test fails "
            "again, or remove the fixture if the bug class is genuinely "
            "obsolete. The harness will NOT seed until this probe is green."
        )
        return 1

    print()
    print("OK: every fixture failed as expected. Harness may seed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
