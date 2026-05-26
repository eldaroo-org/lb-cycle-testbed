# Fixture 08 — heal jobs-file historical repro

<!-- fixture-id: 08-heal-jobs-file-repro -->

## Failure (historical)

Mirrors the live `heal` red chip Dario observed on the dashboard
2026-05-26 ("failed to read jobs file"). The substrate flip from MinIO
to Postgres in spec 009 left this code path reading a host filesystem
that may not exist on fresh Nomad allocs.

**Production fix shipped:** spec 012 PR #635 on Light-Brands/lb-cycle
(merged 2026-05-26T22:15Z) ported heal-cron from `raw_exec` to docker
and moved the substrate dependency. The bug is fixed in prod; this
fixture preserves the historical repro shape so the harness can prove
it catches this bug class going forward.

```
FileNotFoundError: [Errno 2] No such file or directory: '.../jobs.json'
```

## Expected fix shape

Pick one:
1. Catch `FileNotFoundError` + return `[]` + log a warning.
2. Switch the read to the substrate adapter (`storage_backend.get`).

Either path satisfies the test as long as `read_jobs()` returns an
empty list when the file is absent.

## Verify

`pytest fixtures/08-heal-jobs-file-repro/test_module.py` must pass after
the fix.
