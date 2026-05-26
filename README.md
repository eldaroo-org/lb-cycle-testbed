# lb-cycle-testbed

Sandbox testbed for the lb-cycle E2E harness (spec 011, `Light-Brands/lb-cycle`).

**This repo exists to be intentionally broken.** lb-cycle's `sandbox-mode` runs
its autodev / heal / pr-groomer components against this repo (and only this repo)
to prove the end-to-end loop works before pointing the same machinery at real
Light-Brands product repos.

## What lives here

- `src/lb_cycle_testbed/` — minimal Python package so `pytest` has something to
  collect against.
- `tests/test_known_failure.py` — a deliberately failing test. lb-cycle's
  autodev should detect the failure, open a PR against this repo with a fix,
  green CI, and merge. That round-trip is the harness's smoke test.
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
