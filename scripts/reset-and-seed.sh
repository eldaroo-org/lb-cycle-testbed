#!/usr/bin/env bash
# reset-and-seed.sh — restore the testbed to a known seeded baseline.
#
# Spec 011 T-007 (#612). Idempotent: running twice in a row produces
# identical sha256 over both:
#   - gh issue list --json number,title,state,labels
#   - git ls-remote --tags origin
#
# The script:
#   1. Walks every open issue on Eldaroo-org/lb-cycle-testbed and closes
#      it. (Sandbox runs file fresh issues per fixture; previous runs
#      leave fixture-NN issues around that must clear between iterations.)
#   2. Deletes every remote branch except `main`. (Sandbox autodev opens
#      one branch per fix attempt; we wipe them so each run starts clean.)
#   3. Tags + creates one new issue per fixture under fixtures/NN-<name>/,
#      titled `Fixture NN: <name>`, body from fixtures/NN-<name>/issue.md,
#      labelled `autodev` + `spec-task` + `lb-cycle/sandbox-fixture`.
#
# Required env:
#   GH_REPO   — defaults to Eldaroo-org/lb-cycle-testbed
#   GH_TOKEN  — gh CLI must be authenticated against eldaroo (`gh auth status`).
#
# Output: prints one line per close + one line per create, then a final
# `OK: <N> issues seeded` line. Exits 0 on success; non-zero on any gh
# failure.
set -euo pipefail

REPO="${GH_REPO:-Eldaroo-org/lb-cycle-testbed}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${HERE}/fixtures"

if [ ! -d "${FIXTURES_DIR}" ]; then
    echo "reset-and-seed: fixtures dir not found: ${FIXTURES_DIR}" >&2
    exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
    echo "reset-and-seed: gh CLI not on PATH" >&2
    exit 1
fi

echo "reset-and-seed: target = ${REPO}"

# ----------------------------------------------------------------------
# Phase 1: close every open issue.
# ----------------------------------------------------------------------
open_issues=$(gh issue list --repo "${REPO}" --state open --limit 200 --json number --jq '.[].number')
if [ -n "${open_issues}" ]; then
    while IFS= read -r number; do
        [ -z "${number}" ] && continue
        echo "close issue #${number}"
        gh issue close "${number}" --repo "${REPO}" --comment "reset-and-seed.sh: closing previous-run fixture issue" >/dev/null
    done <<< "${open_issues}"
else
    echo "no open issues to close"
fi

# ----------------------------------------------------------------------
# Phase 2: delete every remote branch except main.
# ----------------------------------------------------------------------
branches=$(gh api "repos/${REPO}/branches?per_page=100" --jq '.[].name')
while IFS= read -r branch; do
    [ -z "${branch}" ] && continue
    if [ "${branch}" = "main" ]; then
        continue
    fi
    echo "delete branch ${branch}"
    gh api -X DELETE "repos/${REPO}/git/refs/heads/${branch}" >/dev/null || true
done <<< "${branches}"

# ----------------------------------------------------------------------
# Phase 3: walk fixtures + file one issue per fixture (idempotent on
# title because we just nuked every prior issue above).
# ----------------------------------------------------------------------
seeded=0
for fixture_dir in $(ls -1d "${FIXTURES_DIR}"/[0-9][0-9]-*/ 2>/dev/null | sort); do
    fixture_id=$(basename "${fixture_dir%/}")
    issue_md="${fixture_dir}issue.md"
    if [ ! -f "${issue_md}" ]; then
        echo "skip ${fixture_id}: no issue.md" >&2
        continue
    fi
    # Title shape mirrors the in-issue header for human-grep symmetry.
    title="Fixture ${fixture_id%%-*}: ${fixture_id#*-}"
    echo "create issue: ${title}"
    gh issue create \
        --repo "${REPO}" \
        --title "${title}" \
        --body-file "${issue_md}" \
        --label "autodev" \
        --label "spec-task" \
        --label "lb-cycle/sandbox-fixture" >/dev/null
    seeded=$((seeded + 1))
done

# ----------------------------------------------------------------------
# Also re-file fixture #1 (the canonical assertion bug in
# tests/test_known_failure.py + src/lb_cycle_testbed/__init__.py). This
# fixture sits under the canonical pytest layout, not under fixtures/.
# ----------------------------------------------------------------------
known_failure_issue=$(mktemp)
cat > "${known_failure_issue}" <<'EOF'
# Fixture 01 — Assertion failure (the_answer)

<!-- fixture-id: 01-the-answer -->

## Failure

`tests/test_known_failure.py::test_the_answer_is_forty_two` fails:

```
AssertionError: the_answer() is supposed to return 42.
```

`src/lb_cycle_testbed/__init__.py` defines `the_answer()` to return `0`.

## Expected fix shape

Edit `src/lb_cycle_testbed/__init__.py` so `the_answer()` returns `42`.

## Verify

`pytest tests/test_known_failure.py` must pass after the fix.
EOF
gh issue create \
    --repo "${REPO}" \
    --title "Fixture 01: the-answer" \
    --body-file "${known_failure_issue}" \
    --label "autodev" \
    --label "spec-task" \
    --label "lb-cycle/sandbox-fixture" >/dev/null
seeded=$((seeded + 1))
rm -f "${known_failure_issue}"

echo "OK: ${seeded} issues seeded"
