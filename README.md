# lb-cycle-testbed

Sandbox testbed for the lb-cycle E2E harness (spec 011, `Light-Brands/lb-cycle`).

**This repo exists to be intentionally broken.** lb-cycle's `sandbox-mode` runs
its autodev / heal / pr-groomer components against this repo (and only this repo)
to prove the end-to-end loop works before pointing the same machinery at real
Light-Brands product repos.

## What lives here

- `src/lb_cycle_testbed/` — minimal Python package + the canonical
  fixture #1 (`the_answer()` returning 0 when the test expects 42).
- `tests/test_known_failure.py` — fixture #1's failing pytest case.
- `fixtures/NN-<bug-class>/` — seven additional deliberately-broken
  fixtures, one per bug class autodev should learn to fix. See
  `fixtures/README.md` for the per-fixture table.
- `scripts/reset-and-seed.sh` — closes every open issue, deletes every
  non-main branch, and files one fresh GitHub issue per fixture with
  the `autodev` + `spec-task` + `lb-cycle/sandbox-fixture` labels.
  Idempotent over the structural snapshot (titles + labels + state).
- `scripts/idempotency-self-test.sh` — runs reset-and-seed.sh twice and
  asserts the sha256 of the post-run snapshot is identical (spec 011
  AC5).
- `scripts/must_fail_without_fix.py` — walks every fixture and asserts
  its test fails on the unfixed baseline. Exits non-zero with
  `fixture_no_longer_proves_anything` when a fixture green-passes.
  Spec 011 AC6 defends against Sage's fixture-decay-via-Claude-getting
  -smarter risk.
- `pyproject.toml` — build metadata for the package + pytest entry.

## Rules of engagement

- This repo is the **only** allowlisted destination for lb-cycle sandbox-mode
  writes. See `Light-Brands/lb-cycle/lib/cycle/sandbox_allowlist.py`
  (`SANDBOX_REPOS` frozenset).
- A scoped `gh` token (in `.qie/secrets/credentials.yaml` under `sandbox:`)
  guarantees lb-cycle cannot reach beyond this repo even if a wire-up bug
  composes the wrong allowlist.
- `reset-and-seed.sh` (spec 011 T-007) resets this repo to a known-failing
  baseline so each sandbox run starts from the same shape.

## Tracking

Parent spec: https://github.com/Light-Brands/lb-cycle/issues/630
