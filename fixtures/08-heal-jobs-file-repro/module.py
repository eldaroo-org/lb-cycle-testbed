"""Fixture 08 — heal-jobs-file historical repro.

Mirrors the live `heal` red chip Dario saw on the dashboard 2026-05-26
("failed to read jobs file"). The substrate flip from MinIO to Postgres
in spec 009 left this code path reading a file that may not exist on
fresh allocs; spec 012 (PR #635 on Light-Brands/lb-cycle, merged
2026-05-26T22:15Z) shipped the docker-port fix in production.

This fixture preserves the repro shape as historical evidence that the
harness CATCHES this bug class. autodev's job is to either:
- swap the raw file read for a substrate-aware helper, OR
- catch FileNotFoundError + return an empty default + log a warning.

The harness asserts the test passes after the fix.
"""
from pathlib import Path
import json


JOBS_FILE = Path(__file__).resolve().parent / ".does-not-exist" / "jobs.json"


def read_jobs() -> list[dict]:
    """Read the resolve-jobs file. Currently bombs with FileNotFoundError
    because JOBS_FILE points at a path that does not exist."""
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
