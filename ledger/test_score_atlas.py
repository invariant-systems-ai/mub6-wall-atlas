#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Self-test for the ledger guard, so the honesty rule cannot be silently weakened.

Stdlib only, like the scorer it protects. It checks the one property the project leans
on hardest: the reproduction counters (`independent_reruns`,
`independent_implementations`) are *derived* from checkable evidence and cannot be set by
hand. If a future change lets a bare count pass without backing entries, this test fails
and CI blocks it, with no maintainer in the loop.

Usage:  python3 ledger/test_score_atlas.py   (exit 0 = guard intact)
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCORER = HERE / "score_atlas.py"
NODES = HERE / "nodes.json"


def run(nodes_obj):
    """Run the scorer on an in-memory ledger; return its exit code."""
    tmp = HERE / "_test_tmp_nodes.json"
    tmp.write_text(json.dumps(nodes_obj))
    try:
        r = subprocess.run([sys.executable, str(SCORER), str(tmp)],
                           capture_output=True, text=True)
        return r.returncode
    finally:
        tmp.unlink(missing_ok=True)


def main():
    base = json.loads(NODES.read_text())
    cases = []

    # 1. The shipped ledger is well-formed.
    cases.append(("honest ledger passes", run(base) == 0))

    # 2. Inflating a counter with no evidence is rejected.
    inflated = copy.deepcopy(base)
    inflated["nodes"][0]["independent_reruns"] = 7
    cases.append(("inflated counter rejected", run(inflated) != 0))

    # 3. A genuine evidence entry that matches the count passes.
    backed = copy.deepcopy(base)
    backed["nodes"][0]["independent_reruns"] = 1
    backed["nodes"][0]["reruns"] = [{
        "by": "Test Stranger", "date": "2026-07-01",
        "evidence": "https://example.org/independent-rerun-log.txt",
        "sha256": "0" * 64,
    }]
    cases.append(("evidence-backed count passes", run(backed) == 0))

    # 4. An evidence entry missing who/when/artifact is rejected.
    malformed = copy.deepcopy(base)
    malformed["nodes"][0]["independent_reruns"] = 1
    malformed["nodes"][0]["reruns"] = [{"by": "Anon"}]   # no date, no evidence
    cases.append(("malformed evidence entry rejected", run(malformed) != 0))

    # 5. Count that does not match the number of entries is rejected.
    mismatch = copy.deepcopy(base)
    mismatch["nodes"][0]["independent_reruns"] = 2
    mismatch["nodes"][0]["reruns"] = [{
        "by": "One Person", "date": "2026-07-01",
        "evidence": "https://example.org/only-one.txt",
    }]
    cases.append(("count/evidence mismatch rejected", run(mismatch) != 0))

    # 6. Status 'verified' with no independent evidence is rejected (never label up).
    overstatus = copy.deepcopy(base)
    overstatus["nodes"][0]["status"] = "verified"   # but reruns/impls are 0
    cases.append(("'verified' without independent evidence rejected", run(overstatus) != 0))

    # 7. Status 'verified' backed by a real independent rerun passes.
    earned = copy.deepcopy(base)
    earned["nodes"][0]["status"] = "verified"
    earned["nodes"][0]["independent_reruns"] = 1
    earned["nodes"][0]["reruns"] = [{
        "by": "Outside Party", "date": "2026-07-01",
        "evidence": "https://example.org/independent-verify.txt",
    }]
    cases.append(("'verified' with independent evidence passes", run(earned) == 0))

    ok = True
    for name, passed in cases:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print("guard intact" if ok else "GUARD BROKEN: the honesty rule is not enforced")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
