#!/usr/bin/env bash
# idempotency-self-test.sh — AC5 self-test for reset-and-seed.sh.
#
# Spec 011 AC5 (T-007, #612). Asserts that running reset-and-seed.sh
# twice in a row produces identical sha256 over BOTH:
#   - gh issue list --json number,title,state,labels
#   - git ls-remote --tags origin
#
# Exits 0 on parity; non-zero on diff with the differing hashes printed.
set -euo pipefail

REPO="${GH_REPO:-Eldaroo-org/lb-cycle-testbed}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESET="${HERE}/reset-and-seed.sh"

if [ ! -x "${RESET}" ]; then
    chmod +x "${RESET}" || {
        echo "idempotency-self-test: cannot exec ${RESET}" >&2
        exit 1
    }
fi

snapshot() {
    # Stable JSON of issues (numbers + titles + state + labels) PLUS the
    # remote tags. We strip the "number" field because every reset opens
    # fresh issue numbers; the parity-target is structural (same set of
    # titles / labels / state), not numeric identity.
    local issues
    local tags
    # AC5: snapshot is over OPEN issues only. The closed-issues set
    # grows monotonically across runs (each reset closes the prior
    # run's issues), so including --state all guarantees the sha shifts.
    # Per spec wording "gh issue list --json ..." (no --state flag),
    # the default is open; that is the AC5 contract.
    issues=$(
        gh issue list \
            --repo "${REPO}" \
            --state open \
            --limit 200 \
            --json title,state,labels \
            | jq --sort-keys -c '
                sort_by(.title)
                | map({
                    title: .title,
                    state: .state,
                    labels: (.labels | map(.name) | sort),
                  })
            '
    )
    tags=$(git ls-remote --tags "https://github.com/${REPO}.git" 2>/dev/null | awk '{print $2}' | sort)
    printf '%s\n---\n%s\n' "${issues}" "${tags}" | sha256sum | awk '{print $1}'
}

echo "idempotency-self-test: run 1"
bash "${RESET}" >/dev/null
hash_a=$(snapshot)
echo "  snapshot A: ${hash_a}"

echo "idempotency-self-test: run 2"
bash "${RESET}" >/dev/null
hash_b=$(snapshot)
echo "  snapshot B: ${hash_b}"

if [ "${hash_a}" != "${hash_b}" ]; then
    echo "FAIL: snapshots differ" >&2
    echo "  A: ${hash_a}" >&2
    echo "  B: ${hash_b}" >&2
    exit 2
fi

echo "OK: idempotency holds (sha256=${hash_a})"
