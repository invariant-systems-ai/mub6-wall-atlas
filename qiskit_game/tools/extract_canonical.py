#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Derive the EXACT canonical triple + attainment witness from the verified bundle.

This binds the game (Mode B) to the proof (Mode A). It imports the bundle's
`mub6_d6_wall_attainment_exact` module, evaluates its exact cyclotomic objects to
float, reconstructs the attainment witness v* from the documented coefficient
vector, checks f(v*) == W = (88+3*sqrt6)/100 numerically, and writes a
self-contained data file the game loads.

Run it from the atlas with the bundle's python/ on PYTHONPATH, e.g.:

    BUNDLE=../../public-export
    PYTHONPATH=$BUNDLE/python python3 qiskit_game/tools/extract_canonical.py $BUNDLE

It needs numpy and the bundle (which is published on Zenodo, DOI 10.5281/zenodo.20682233).
"""
from __future__ import annotations
import cmath
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

# Bundle location: argv[1] or a sensible default relative to the atlas.
BUNDLE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "public-export")
sys.path.insert(0, os.path.join(BUNDLE, "python"))

import mub6_d6_wall_attainment_exact as M       # the verified module
from mub6_game.feasibility import feasibility, W_EXACT, D


def cvec(cyc_list):
    return np.array([complex(c) for c in cyc_list], dtype=complex)


def main():
    # 1. the exact canonical triple, evaluated to float
    triple_cyc = M.build_triple()
    triple = [np.array([[complex(triple_cyc[b][col][k]) for col in range(6)]
                        for k in range(6)], dtype=complex) for b in range(3)]

    # 2. the attainment witness v* = sum_k lambda_k W_k, with the documented
    #    coefficient vector lambda (coefficient_gram docstring in the module):
    #      lambda = ( sqrt(N_B/N0) e^{-i pi/3}, sqrt(N_C/N1) e^{+i pi/3}, sqrt(N_A/N2) )
    W = [cvec(M.W0), cvec(M.W1), cvec(M.W2)]
    NA, NB, NC = (complex(M.N_A).real, complex(M.N_B).real, complex(M.N_C).real)
    N0, N1, N2 = (complex(M.N0).real, complex(M.N1).real, complex(M.N2).real)
    lam = [
        math.sqrt(NB / N0) * cmath.exp(-1j * math.pi / 3),
        math.sqrt(NC / N1) * cmath.exp(+1j * math.pi / 3),
        math.sqrt(NA / N2),
    ]
    vstar = lam[0] * W[0] + lam[1] * W[1] + lam[2] * W[2]

    # 3. check the binding: f(v*) == W
    f = feasibility(vstar, triple)
    err = abs(f - W_EXACT)
    print(f"f(v*)        = {f:.15f}")
    print(f"W exact      = {W_EXACT:.15f}")
    print(f"|f(v*) - W|  = {err:.2e}")
    if err > 1e-9:
        print("WARN: witness did not attain W; not writing data file.")
        return 1

    # 4. cross-check the game's own formula-built triple matches (up to MUB structure)
    from mub6_game.feasibility import canonical_like_triple
    assert abs(feasibility(vstar, canonical_like_triple()) - W_EXACT) < 1e-9, \
        "game formula triple does not match the canonical witness"

    # 5. write the self-contained data file
    out = {
        "_provenance": "Derived from mub6_d6_wall_attainment_exact (DOI 10.5281/zenodo.20682233). "
                       "f(witness) == W = (88+3*sqrt6)/100 checked to < 1e-9.",
        "d": D,
        "W_exact": W_EXACT,
        "triple": [[[ [z.real, z.imag] for z in basis[:, col]] for col in range(6)]
                   for basis in triple],
        "witness": [[z.real, z.imag] for z in vstar],
    }
    data_dir = os.path.join(HERE, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, "canonical_triple.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {os.path.relpath(path)}  (f(witness) - W = {err:.2e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
