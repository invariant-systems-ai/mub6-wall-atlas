#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Play the MUB(6) wall room: climb toward the feasibility wall and read a scorecard.

This is Mode B (teaching/search). It is NOT the proof: f=1 is unreachable here, and that
gap is the wall. To verify the exact statement max f = W = (88+3*sqrt6)/100, use the Zenodo
verification bundle (Mode A): `make verify-global`.

    python3 play.py            # random start, hill-climb toward the wall
"""
from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import numpy as np
from mub6_game.feasibility import canonical_triple, feasibility, score, D, W_EXACT


def hill_climb(triple, steps=4000, restarts=8, seed=0):
    """Gradient-free climb: random restarts + shrinking Gaussian perturbations."""
    rng = np.random.default_rng(seed)
    best_v, best_f = None, -1.0
    for r in range(restarts):
        v = rng.standard_normal(D) + 1j * rng.standard_normal(D)
        v /= np.linalg.norm(v)
        f = feasibility(v, triple)
        scale = 0.3
        for t in range(steps):
            cand = v + scale * (rng.standard_normal(D) + 1j * rng.standard_normal(D))
            cand /= np.linalg.norm(cand)
            cf = feasibility(cand, triple)
            if cf > f:
                v, f = cand, cf
            if t % 400 == 399:
                scale *= 0.7
        if f > best_f:
            best_v, best_f = v, f
    return best_v, best_f


def bar(frac, width=40):
    n = max(0, min(width, int(round(frac * width))))
    return "[" + "#" * n + "-" * (width - n) + "]"


def main():
    triple = canonical_triple()
    print("MUB(6) WALL ROOM  (Mode B: search, not proof)")
    print("=" * 56)
    print("Goal: make your measurement distributions as flat as")
    print("possible against all three mutually unbiased bases.")
    print("Perfect flatness is f = 1 (a fourth MUB vector). You will")
    print("not reach it. The ceiling you hit is the wall.\n")

    v, f = hill_climb(triple)
    sc = score(v, triple)
    print(f"best f found      : {sc['f']:.6f}")
    print(f"wall score        : {sc['wall_score']:.2f} / 100")
    print(f"defect (1 - f)    : {sc['defect']:.6f}")
    print(f"proven wall  W    : {W_EXACT:.10f}   = (88 + 3*sqrt(6)) / 100")
    print(f"wall completion   : {sc['wall_completion_pct']:.2f}%   {bar(sc['f']/W_EXACT)}")
    print()
    print("You climbed to the wall (Mode B search). Proof mode decides the ceiling:")
    print("  - download the verification bundle (DOI 10.5281/zenodo.20682233)")
    print("  - run  make verify-global   to check  max f <= W  exactly")
    print("  - then map the next brick (see ../ATLAS.md and ../SEED_ISSUES.md)")


if __name__ == "__main__":
    main()
