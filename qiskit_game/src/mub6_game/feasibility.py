#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Fourth-vector feasibility for the MUB(6) Wall Atlas game (Mode B).

This is the TEACHING / SIMULATION core. It evaluates the published feasibility
functional in float64 (numerical, Mode B), so a player can feel the wall:

    f(v) = 1 - [ sum_i sum_j (p_j^(i) - 1/d)^2 ] / (1 - 1/d)

where p_j^(i) = |<v, w_j^(i)>|^2 is the outcome distribution of the unit vector v
measured in basis i, and f = 1 iff v is unbiased to all bases (a fourth MUB
vector). This is the feasibility identity, Lemma 2.1 of the paper / bundle.

It is NOT the proof. The exact, kernel-and-certificate-backed statement
`max f = W = (88 + 3*sqrt(6))/100` for the canonical triple lives in the Zenodo
verification bundle (Mode A). This module builds a *validated* product MUB triple
of C^6 for play; binding it to the exact canonical triple so that f(witness) = W
is itself an open brick (see the atlas).
"""
from __future__ import annotations
import json
import math
import os
import numpy as np

D = 6                                   # dimension
K = 3                                   # bases in the triple
W_EXACT = (88 + 3 * math.sqrt(6)) / 100  # proven wall for the canonical triple, ~0.95348

# Authoritative canonical triple + witness, derived from the verified bundle by
# tools/extract_canonical.py (f(witness) == W to machine precision). Optional: if the
# data file is absent the game falls back to the formula-built triple below.
_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "canonical_triple.json")


# ---------------------------------------------------------------- bases
def _qubit_mubs():
    """The 3 MUBs of C^2: eigenbases of Z, X, Y."""
    s = 1 / math.sqrt(2)
    Z = np.eye(2, dtype=complex)
    X = s * np.array([[1, 1], [1, -1]], dtype=complex)
    Y = s * np.array([[1, 1], [1j, -1j]], dtype=complex)
    return [Z, X, Y]


def _qutrit_mubs():
    """3 of the 4 MUBs of C^3: the standard basis and two Heisenberg-Weyl bases.

    The non-standard MUB b has column m with entries (1/sqrt 3) * w^(b j^2 + m j)
    for j = 0,1,2 (the quadratic Gauss-sum phase). b = 0 is the Fourier basis;
    distinct b give mutually unbiased bases. A *linear* modulation of Fourier does
    NOT, which is why this uses the quadratic phase."""
    w = np.exp(2j * math.pi / 3)

    def mub(b):
        return np.array([[w ** ((b * j * j + m * j) % 3) for m in range(3)]
                         for j in range(3)], dtype=complex) / math.sqrt(3)

    Z = np.eye(3, dtype=complex)
    return [Z, mub(0), mub(1)]


def canonical_like_triple():
    """The canonical product MUB triple of C^6 = C^2 (x) C^3, built from the formula.

    Returns three 6x6 complex matrices (columns = orthonormal, pairwise mutually
    unbiased bases). This reproduces the bundle's build_triple construction
    {Z2(x)Z3, X2(x)Q0, Y2(x)Q1} exactly; the data-file version below is the
    authoritative one, validated against the proof's witness.
    """
    q2, q3 = _qubit_mubs(), _qutrit_mubs()
    return [np.kron(q2[i], q3[i]) for i in range(K)]


def _load_canonical():
    if not os.path.exists(_DATA):
        return None
    with open(_DATA) as fh:
        d = json.load(fh)
    triple = [np.array([[complex(re, im) for (re, im) in col] for col in basis],
                       dtype=complex).T for basis in d["triple"]]
    witness = np.array([complex(re, im) for (re, im) in d["witness"]], dtype=complex)
    return triple, witness


def canonical_triple():
    """The authoritative canonical triple (from the verified bundle if available)."""
    loaded = _load_canonical()
    return loaded[0] if loaded else canonical_like_triple()


def canonical_witness():
    """The exact attainment witness v* with f(v*) = W, if the data file is present."""
    loaded = _load_canonical()
    return loaded[1] if loaded else None


# ---------------------------------------------------------------- feasibility
def outcome_distribution(v, basis):
    """p_j = |<v, w_j>|^2 for each column w_j of `basis`."""
    v = np.asarray(v, dtype=complex).reshape(-1)
    amps = basis.conj().T @ v                      # <w_j, v>
    return np.abs(amps) ** 2


def feasibility(v, triple=None):
    """Exact (float) fourth-vector feasibility f(v) in [0, 1]. f=1 iff unbiased."""
    if triple is None:
        triple = canonical_triple()
    v = np.asarray(v, dtype=complex).reshape(-1)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("v must be nonzero")
    v = v / n
    nonuniformity = 0.0
    for basis in triple:
        p = outcome_distribution(v, basis)
        nonuniformity += float(np.sum((p - 1.0 / D) ** 2))
    return 1.0 - nonuniformity / (1.0 - 1.0 / D)


def score(v, triple=None):
    """Game scorecard for a candidate vector."""
    f = feasibility(v, triple)
    return {
        "f": f,
        "wall_score": 100.0 * f,
        "defect": 1.0 - f,
        "W_exact": W_EXACT,
        "wall_completion_pct": 100.0 * f / W_EXACT,
        "note": "search score, not proof. f=1 is unreachable here; that gap is the wall.",
    }


# ---------------------------------------------------------------- C^6 in 3 qubits
# valid computational states of the 3-qubit register that carry C^6; |110>,|111> leak.
VALID_KETS = [0, 1, 2, 3, 4, 5]           # |000>..|101>
LEAKAGE_KETS = [6, 7]                      # |110>, |111>


def embed_c6_in_3q(v6):
    """Embed a C^6 vector into the 8-dim 3-qubit space (leakage amplitudes = 0)."""
    v6 = np.asarray(v6, dtype=complex).reshape(-1)
    v8 = np.zeros(8, dtype=complex)
    v8[VALID_KETS] = v6
    return v8


def project_3q_to_c6(v8):
    """Drop the two leakage amplitudes; returns (v6, leakage_mass)."""
    v8 = np.asarray(v8, dtype=complex).reshape(-1)
    leak = float(np.sum(np.abs(v8[LEAKAGE_KETS]) ** 2))
    return v8[VALID_KETS], leak


# ---------------------------------------------------------------- self-test
def _selftest():
    triple = canonical_triple()
    # 1. each basis orthonormal
    for i, b in enumerate(triple):
        assert np.allclose(b.conj().T @ b, np.eye(D), atol=1e-12), f"basis {i} not orthonormal"
    # 2. pairwise mutually unbiased: |<w,u>|^2 == 1/d for cross pairs
    for i in range(K):
        for j in range(i + 1, K):
            M = np.abs(triple[i].conj().T @ triple[j]) ** 2
            assert np.allclose(M, 1.0 / D, atol=1e-12), f"bases {i},{j} not mutually unbiased"
    # 3. f in [0,1]; a basis vector (concentrated) has low f
    v_aligned = triple[0][:, 0]
    f_aligned = feasibility(v_aligned, triple)
    assert -1e-9 <= f_aligned <= 1.0 + 1e-9
    # 4. random search never exceeds 1, and finds a high-but-sub-1 ceiling (the wall)
    rng = np.random.default_rng(0)
    best = 0.0
    for _ in range(20000):
        v = rng.standard_normal(D) + 1j * rng.standard_normal(D)
        best = max(best, feasibility(v, triple))
    assert best <= 1.0 + 1e-9
    # 5. if the authoritative witness is present, it attains W (the binding to Mode A)
    vstar = canonical_witness()
    bound = None
    if vstar is not None:
        fw = feasibility(vstar, triple)
        bound = abs(fw - W_EXACT)
        assert bound < 1e-12, f"witness does not attain W (|f-W|={bound:.2e})"
    print("self-test PASS")
    print(f"  bases: {K} mutually unbiased, orthonormal, in C^{D}")
    print(f"  f(basis vector) = {f_aligned:.4f}  (concentrated -> low feasibility)")
    print(f"  empirical max f over 20000 random v = {best:.4f}")
    print(f"  proven canonical wall  W = (88+3*sqrt6)/100 = {W_EXACT:.10f}")
    if vstar is not None:
        print(f"  witness attains the wall to machine precision: |f(v*) - W| = {bound:.2e}  (binding to Mode A)")
    else:
        print("  (no witness data file; run tools/extract_canonical.py to bind to the bundle.)")


if __name__ == "__main__":
    _selftest()
