#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Validate the MUB(6) Wall Atlas node ledger and print its atlas points.

Standard-library only, by design: the points system is itself checkable, the same
posture the verifier applies to the math. Atlas points are reputation markers, not
currency: non-financial, non-transferable, artifact-linked, and revocable if a claim
is broken.

Usage:  python3 ledger/score_atlas.py [path/to/nodes.json]
Exit 0 = ledger well-formed; exit 1 = a schema/consistency problem (printed).
"""
import json
import sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
# First non-flag argument is an alternate ledger path; flags (--scoreboard, etc.) are not.
_positional = [a for a in sys.argv[1:] if not a.startswith("--")]
LEDGER = Path(_positional[0]) if _positional else HERE / "nodes.json"

KINDS = {"wall", "witness", "certificate", "defect"}
EVIDENCE = {"kernel", "exact", "60-digit", "float", "conjecture", "none"}
STATUS = {"verified", "self-verified", "partial", "open", "refuted"}
REQUIRED = ["id", "kind", "title", "claim", "scope", "artifact", "verifier",
            "evidence_level", "status", "independent_reruns",
            "independent_implementations", "dependencies", "known_weaknesses",
            "contributor"]

# Fibonacci atlas points. Independent work (reruns, reimplementations) is where the
# points are: it is what turns "trust me" into "checked".
RERUN_POINTS = 5          # an independent verifier run
REIMPL_POINTS = 13        # an independent implementation in another system


def intrinsic_points(n):
    """Points for the result itself, before independent-verification bonuses."""
    if n["status"] in ("open", "refuted"):
        return 0
    ev, kind = n["evidence_level"], n["kind"]
    if ev == "kernel":
        return 21                      # formalized theorem / major new wall
    if ev == "exact":
        if kind in ("wall", "certificate"):
            return 8                   # exact certificate or proof artifact
        return 3                       # new witness or failed-extension (defect) map
    if ev in ("60-digit", "float"):
        return 2                       # replicated numerical evidence
    if ev == "conjecture":
        return 1
    return 0


def badges(n):
    b = set()
    if n["evidence_level"] == "kernel":
        b.add("formalization")
    elif n["evidence_level"] == "exact" and n["kind"] in ("wall", "certificate"):
        b.add("certificate")
    if n["kind"] == "witness":
        b.add("witness")
    if n["kind"] == "defect":
        b.add("defect")
    if n["independent_reruns"] > 0 or n["independent_implementations"] > 0:
        b.add("reproduction")
    return b


STR_FIELDS = ("id", "title", "claim", "scope", "verifier", "known_weaknesses", "contributor")
LIST_FIELDS = ("artifact", "dependencies")

# Evidence-bound counters. The two reproduction counters are not free integers a PR
# can inflate: each is *derived* from a list of checkable evidence entries, and CI
# rejects any count that does not equal the number of entries backing it. To claim a
# rerun you file the receipt; the number follows the receipt, never the reverse. This
# is the "never label up" rule made mechanical, so the ledger stays honest with no
# human reconciling it.
EVIDENCE_LISTS = {
    "independent_reruns": "reruns",
    "independent_implementations": "implementations",
}
EVIDENCE_ENTRY_FIELDS = ("by", "date", "evidence")  # who, when, the checkable artifact/URL


def validate(nodes):
    errs, ids = [], set()
    for i, n in enumerate(nodes):
        where = n.get("id", f"#{i}")
        for k in REQUIRED:
            if k not in n:
                errs.append(f"{where}: missing field '{k}'")
        if n.get("kind") not in KINDS:
            errs.append(f"{where}: bad kind {n.get('kind')!r}")
        if n.get("evidence_level") not in EVIDENCE:
            errs.append(f"{where}: bad evidence_level {n.get('evidence_level')!r}")
        if n.get("status") not in STATUS:
            errs.append(f"{where}: bad status {n.get('status')!r}")
        for f in ("independent_reruns", "independent_implementations"):
            if not isinstance(n.get(f), int) or n.get(f, -1) < 0:
                errs.append(f"{where}: {f} must be a non-negative integer")
        # Each reproduction counter must equal the length of its evidence list. A bare
        # count with no backing entries (or entries missing a who/when/artifact) fails CI.
        for counter, listname in EVIDENCE_LISTS.items():
            entries = n.get(listname, [])
            if not isinstance(entries, list):
                errs.append(f"{where}: field '{listname}' must be a list of evidence entries")
                continue
            for j, e in enumerate(entries):
                if not isinstance(e, dict):
                    errs.append(f"{where}: {listname}[{j}] must be an object with {EVIDENCE_ENTRY_FIELDS}")
                    continue
                for ef in EVIDENCE_ENTRY_FIELDS:
                    if not isinstance(e.get(ef), str) or not e.get(ef).strip():
                        errs.append(f"{where}: {listname}[{j}] missing non-empty '{ef}' (who/when/checkable evidence)")
            if isinstance(n.get(counter), int) and n.get(counter) != len(entries):
                errs.append(
                    f"{where}: {counter} = {n.get(counter)} but {listname} has {len(entries)} "
                    f"evidence entr{'y' if len(entries) == 1 else 'ies'}; the count is derived from "
                    f"the evidence and cannot be set by hand")
        # "Never label up" at the status axis: the strongest status, 'verified', means an
        # outside party checked it, so it requires at least one independent rerun or
        # implementation (each itself evidence-bound above). The author's own ceiling is
        # 'self-verified'. This stops a node from wearing the strongest label on trust alone.
        if n.get("status") == "verified":
            independent = (n.get("independent_reruns") or 0) + (n.get("independent_implementations") or 0)
            if independent < 1:
                errs.append(
                    f"{where}: status 'verified' needs at least one independent rerun or "
                    f"implementation with evidence; use 'self-verified' until an outside party checks it")
        for f in STR_FIELDS:
            if f in n and not isinstance(n[f], str):
                errs.append(f"{where}: field '{f}' must be a string")
        for f in LIST_FIELDS:
            if f in n and (not isinstance(n[f], list)
                           or not all(isinstance(x, str) for x in n[f])):
                errs.append(f"{where}: field '{f}' must be a list of strings")
        nid = n.get("id")
        if nid in ids:
            errs.append(f"{where}: duplicate node id {nid!r}")
        ids.add(nid)
    for n in nodes:
        for dep in n.get("dependencies", []):
            if dep not in ids:
                errs.append(f"{n.get('id')}: dependency {dep!r} is not a known node id")
    return errs


def pct(x):
    return f"{100 * x:5.1f}%"


EV_WEIGHT = {"kernel": 1.0, "exact": 1.0, "60-digit": 0.6, "float": 0.35,
             "conjecture": 0.1, "none": 0.0}
STATUS_MULT = {"verified": 1.0, "self-verified": 0.7, "partial": 0.5,
               "open": 0.0, "refuted": 0.0}


def compute(data, nodes):
    """All derived metrics in one place, so the human readout, the markdown scoreboard,
    and any future surface read from a single source of truth and cannot drift."""
    mapped = [n for n in nodes if n["status"] in ("verified", "self-verified", "partial")]
    frontiers = [n for n in nodes if n["status"] == "open"]
    refuted = [n for n in nodes if n["status"] == "refuted"]
    total_reruns = sum(n["independent_reruns"] for n in nodes)
    total_impls = sum(n["independent_implementations"] for n in nodes)
    intrinsic = sum(intrinsic_points(n) for n in nodes)
    rerun_pts = RERUN_POINTS * total_reruns
    reimpl_pts = REIMPL_POINTS * total_impls
    has_verifier = [n for n in mapped if n["verifier"] != "none"]
    reproduced = [n for n in mapped if n["independent_reruns"] >= 1 or n["independent_implementations"] >= 1]
    badge_tally = Counter()
    for n in nodes:
        badge_tally.update(badges(n))
    return {
        "ledger_version": data.get("ledger_version", "?"),
        "node_count": len(nodes),
        "concepts": sorted({n["concept_doi"] for n in nodes if n.get("concept_doi")}),
        "versions": sorted({n["bundle_doi"] for n in nodes if n.get("bundle_doi")}),
        "certs": sorted({n["certificate_sha256"] for n in nodes if n.get("certificate_sha256")}),
        "by_kind": dict(Counter(n["kind"] for n in nodes)),
        "by_status": dict(Counter(n["status"] for n in nodes)),
        "badges": dict(badge_tally),
        "intrinsic": intrinsic, "rerun_pts": rerun_pts, "reimpl_pts": reimpl_pts,
        "total_pts": intrinsic + rerun_pts + reimpl_pts,
        "total_reruns": total_reruns, "total_impls": total_impls,
        "truth": (sum(EV_WEIGHT[n["evidence_level"]] * STATUS_MULT[n["status"]] for n in mapped)
                  / len(mapped)) if mapped else 0.0,
        "scopes": sorted({n["scope"] for n in nodes}),
        "mapped": mapped, "frontiers": frontiers, "refuted": refuted,
        "has_verifier": has_verifier, "reproduced": reproduced,
        "novelty": len([n for n in mapped if n["kind"] in ("wall", "witness", "certificate")]),
        "route": len(has_verifier) + len(frontiers),
        "nodes": nodes,
    }


def print_human(s):
    print(f"MUB(6) Wall Atlas ledger  v{s['ledger_version']}  ({s['node_count']} nodes)")
    print("=" * 66)
    print("ledger well-formed: every node has the required typed fields.")
    if s["concepts"]:
        print("concept DOI (work)  :", ", ".join(s["concepts"]))
    if s["versions"]:
        print("version DOI (pinned):", ", ".join(s["versions"]))
    for c in s["certs"]:
        print("certificate sha256  :", c)
    print()
    print("NODES BY KIND   :", s["by_kind"])
    print("NODES BY STATUS :", s["by_status"])
    print("BADGES          :", s["badges"])
    print()
    print("ATLAS POINTS (Fibonacci, nonfinancial, revocable)")
    print("-" * 66)
    print(f"  intrinsic (results)            : {s['intrinsic']:>5}")
    print(f"  + independent verifier reruns  : {s['rerun_pts']:>5}  ({s['total_reruns']} x {RERUN_POINTS})")
    print(f"  + independent implementations  : {s['reimpl_pts']:>5}  ({s['total_impls']} x {REIMPL_POINTS})")
    print(f"  TOTAL ATLAS POINTS             : {s['total_pts']:>5}")
    print()
    print("FIVE DIMENSIONS (the deeper readout, not a people-leaderboard)")
    print("-" * 66)
    m = len(s["mapped"])
    print(f"  Truth   : {pct(s['truth'])}   mean verification strength of mapped nodes")
    print(f"  Scope   : {len(s['scopes']):>5}    distinct regions of MUB(6) touched")
    print(f"  Repro   : {pct(len(s['has_verifier'])/m if m else 0)}   of mapped nodes ship a public verifier")
    print(f"            {pct(len(s['reproduced'])/m if m else 0)}   independently reproduced so far")
    print(f"  Novelty : {s['novelty']:>5}    distinct walls / witnesses / certificates")
    print(f"  Route   : {s['route']:>5}    runnable verifiers + open routeable frontiers")
    print()
    print("OPEN FRONTIERS (routeable bricks):")
    for n in s["frontiers"]:
        print(f"  - {n['id']:<22} {n['title']}  [{n['evidence_level']}]")
    if s["refuted"]:
        print("\nREFUTED (revoked nodes, points revoked):")
        for n in s["refuted"]:
            print(f"  - {n['id']:<22} {n['title']}")
    print()
    print("Atlas points are reputation markers, not currency. Revocable if a claim fails.")
    print("Earn 5 by independently rerunning a verifier; 13 by reimplementing a checker.")


def scoreboard_md(s):
    """Deterministic markdown scoreboard, generated from the ledger. Byte-stable so a CI
    staleness check can diff it; never hand-edit (the header says so)."""
    m = len(s["mapped"])
    L = []
    L.append("# MUB(6) Wall Atlas scoreboard")
    L.append("")
    L.append("<!-- GENERATED by ledger/score_atlas.py --write-scoreboard. Do not edit by hand. -->")
    L.append("<!-- Regenerate after any ledger change; CI fails if this file is stale. -->")
    L.append("")
    L.append(f"Ledger `v{s['ledger_version']}`, **{s['node_count']} nodes**. Atlas points are "
             "non-financial, artifact-linked, and revocable if a claim breaks.")
    L.append("")
    L.append("## Totals")
    L.append("")
    L.append("| metric | value |")
    L.append("|---|---|")
    L.append(f"| intrinsic points (results) | {s['intrinsic']} |")
    L.append(f"| independent rerun points | {s['rerun_pts']} ({s['total_reruns']} x {RERUN_POINTS}) |")
    L.append(f"| independent implementation points | {s['reimpl_pts']} ({s['total_impls']} x {REIMPL_POINTS}) |")
    L.append(f"| **total atlas points** | **{s['total_pts']}** |")
    L.append(f"| independently reproduced nodes | {len(s['reproduced'])} / {m} |")
    L.append("")
    L.append("## Nodes")
    L.append("")
    L.append("| id | kind | evidence | status | pts | reruns | impls |")
    L.append("|---|---|---|---|--:|--:|--:|")
    for n in s["nodes"]:
        L.append(f"| `{n['id']}` | {n['kind']} | {n['evidence_level']} | {n['status']} | "
                 f"{intrinsic_points(n)} | {n['independent_reruns']} | {n['independent_implementations']} |")
    L.append("")
    L.append("## Open frontiers (routeable bricks)")
    L.append("")
    for n in s["frontiers"]:
        L.append(f"- `{n['id']}` {n['title']} [{n['evidence_level']}]")
    if s["refuted"]:
        L.append("")
        L.append("## Refuted (points revoked)")
        L.append("")
        for n in s["refuted"]:
            L.append(f"- `{n['id']}` {n['title']}")
    L.append("")
    L.append("> Reproduction counts are evidence-bound: each is derived from a checkable "
             "evidence list and cannot be set by hand. See `POINTS.md`.")
    L.append("")
    return "\n".join(L)


SCOREBOARD = HERE.parent / "SCOREBOARD.md"


def load_and_validate():
    if not LEDGER.exists():
        print(f"FAIL: ledger not found at {LEDGER}")
        return None, None, ["ledger not found"]
    data = json.loads(LEDGER.read_text())
    nodes = data.get("nodes", [])
    return data, nodes, validate(nodes)


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    data, nodes, errs = load_and_validate()
    if errs:
        print(f"MUB(6) Wall Atlas ledger  ({len(nodes or [])} nodes)")
        print("=" * 66)
        print("SCHEMA / CONSISTENCY ERRORS:")
        for e in errs:
            print("  -", e)
        return 1
    s = compute(data, nodes)
    md = scoreboard_md(s)

    if "--scoreboard" in flags:                 # print markdown (for a CI job summary)
        print(md)
        return 0
    if "--write-scoreboard" in flags:           # regenerate the committed scoreboard
        SCOREBOARD.write_text(md)
        print(f"wrote {SCOREBOARD}")
        return 0
    if "--check-scoreboard" in flags:           # fail if the committed scoreboard is stale
        current = SCOREBOARD.read_text() if SCOREBOARD.exists() else None
        if current != md:
            print("FAIL: SCOREBOARD.md is stale or missing. "
                  "Run: python3 ledger/score_atlas.py --write-scoreboard")
            return 1
        print("OK: SCOREBOARD.md is in sync with the ledger.")
        return 0

    print_human(s)                              # default: human readout
    return 0


if __name__ == "__main__":
    # First non-flag argument (if any) is an alternate ledger path; the module-level
    # LEDGER already captured it, so here we just pass the flags through.
    sys.exit(main(sys.argv[1:]))
