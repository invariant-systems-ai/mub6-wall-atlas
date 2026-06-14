#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Summarise what a pull request does to the node ledger, as a friendly PR comment.

This is the thoughtful-interruption surface: most of the atlas polices itself silently,
but when a PR touches the ledger a human should glance at it, so the bot lays out exactly
what changed (points, reproduction counts, statuses, new or removed nodes) and reminds the
author of the rules CI enforces. It renders Markdown to stdout; the workflow posts it.

It reads two ledgers as DATA only (never executes anything from the PR), so it is safe to
run on fork pull requests.

Usage:  python3 ci/pr_ledger_report.py BASE_nodes.json HEAD_nodes.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ledger"))
from score_atlas import intrinsic_points, RERUN_POINTS, REIMPL_POINTS  # noqa: E402

MARKER = "<!-- mub6-ledger-bot -->"


def load(path):
    try:
        return {n["id"]: n for n in json.loads(Path(path).read_text()).get("nodes", [])}
    except Exception as e:                       # malformed head: validate.yml hard-fails it
        return e


def total_points(nodes):
    return (sum(intrinsic_points(n) for n in nodes.values())
            + RERUN_POINTS * sum(n.get("independent_reruns", 0) for n in nodes.values())
            + REIMPL_POINTS * sum(n.get("independent_implementations", 0) for n in nodes.values()))


def evidence_ok(node, counter, listname):
    return node.get(counter, 0) == len(node.get(listname, []))


def main(base_path, head_path):
    base, head = load(base_path), load(head_path)
    L = [MARKER, "## Ledger change report", ""]

    if isinstance(head, Exception):
        L += [f"The head ledger could not be parsed as JSON (`{head}`). "
              "The `validate atlas` check will have the details.", ""]
        print("\n".join(L))
        return 0
    if isinstance(base, Exception):
        base = {}

    added = sorted(set(head) - set(base))
    removed = sorted(set(base) - set(head))
    pts_base, pts_head = total_points(base) if base else 0, total_points(head)

    L.append(f"**Atlas points:** {pts_base} -> {pts_head} "
             f"({'+' if pts_head >= pts_base else ''}{pts_head - pts_base})")
    L.append("")

    if added:
        L.append("**New nodes**")
        for nid in added:
            n = head[nid]
            L.append(f"- `{nid}` ({n.get('kind')}, {n.get('evidence_level')}, "
                     f"{n.get('status')}) -> {intrinsic_points(n)} pts")
        L.append("")
    if removed:
        L.append("**Removed nodes**")
        for nid in removed:
            L.append(f"- `{nid}`")
        L.append("")

    # Per-node changes to the honesty-critical fields.
    flags = []
    changes = []
    for nid in sorted(set(base) & set(head)):
        b, h = base[nid], head[nid]
        for counter, listname, pts in (("independent_reruns", "reruns", RERUN_POINTS),
                                       ("independent_implementations", "implementations", REIMPL_POINTS)):
            if h.get(counter, 0) != b.get(counter, 0):
                delta = h.get(counter, 0) - b.get(counter, 0)
                changes.append(f"- `{nid}`: {counter} {b.get(counter,0)} -> {h.get(counter,0)} "
                               f"({'+' if delta >= 0 else ''}{delta * pts} pts)")
                if not evidence_ok(h, counter, listname):
                    flags.append(f"- `{nid}`: `{counter}` = {h.get(counter,0)} but "
                                 f"`{listname}` has {len(h.get(listname, []))} evidence "
                                 f"entr{'y' if len(h.get(listname, [])) == 1 else 'ies'} "
                                 "(CI will reject this).")
        if h.get("status") != b.get("status"):
            changes.append(f"- `{nid}`: status {b.get('status')} -> {h.get('status')}")
            if h.get("status") == "verified" and (h.get("independent_reruns", 0)
                                                   + h.get("independent_implementations", 0)) < 1:
                flags.append(f"- `{nid}`: status `verified` needs an independent rerun or "
                             "implementation with evidence (CI will reject this).")

    if changes:
        L.append("**Reproduction / status changes**")
        L += changes
        L.append("")

    if flags:
        L.append("> [!WARNING]")
        L.append("> These changes will fail CI as written:")
        for f in flags:
            L.append("> " + f)
        L.append("")

    L.append("---")
    L.append("Reproduction counts are **evidence-bound**: each is derived from a checkable "
             "`reruns[]` / `implementations[]` entry (who, when, an artifact a stranger can open), "
             "and `status: verified` needs independent evidence. The scorer enforces this, so the "
             "numbers can never run ahead of the proof. See `POINTS.md` and `CONTRIBUTING.md`.")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: pr_ledger_report.py BASE_nodes.json HEAD_nodes.json", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
