#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Generate notebooks/03_mub6_embedded_wall.ipynb (the milestone notebook).

Run with a Python that has nbformat installed. Execute the result with:
  jupyter nbconvert --to notebook --execute --inplace \\
      --ExecutePreprocessor.kernel_name=<kernel> notebooks/03_mub6_embedded_wall.ipynb
"""
import os
import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "notebooks", "03_mub6_embedded_wall.ipynb")

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

cells = [
md("""# Level 3: The MUB(6) wall (embedded in three qubits)

**MUB(6) Wall Atlas, the puzzle lab.** This notebook lets you *feel* the wall on a quantum
circuit, then hands you to the proof.

- **Mode B (this notebook):** prepare a candidate state, measure it in three mutually unbiased
  bases with Qiskit, and watch its feasibility `f` climb toward, but never past, the wall
  `W = (88 + 3*sqrt(6))/100`. This is search and simulation, **not** a proof.
- **Mode A (the bundle):** the exact statement `max f = W` is checked by `make verify-global`
  in the Zenodo verification bundle (DOI 10.5281/zenodo.20682233).

`C^6 = C^2 (x) C^3` is a qudit problem; we embed it in three qubits and treat `|110>, |111>` as
leakage states (amplitude 0)."""),

code("""import sys, os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join("..", "src")))
from mub6_game.feasibility import (
    canonical_triple, canonical_witness, feasibility,
    embed_c6_in_3q, W_EXACT, D, VALID_KETS, LEAKAGE_KETS,
)
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation, UnitaryGate
from qiskit.primitives import StatevectorSampler

print("dimension d =", D, " wall W = (88+3*sqrt6)/100 =", round(W_EXACT, 10))
print("valid kets:", VALID_KETS, " leakage kets:", LEAKAGE_KETS)"""),

md("""## The candidate state

We use the **exact attainment witness** `v*` of the canonical triple, the state proven to sit
right at the wall. It is loaded from a data file derived from the verified module (so
`f(v*) = W` to machine precision), then embedded into the 3-qubit register."""),

code("""triple = canonical_triple()          # the canonical MUB triple of C^6
vstar = canonical_witness()          # exact attainment witness, f(v*) = W
v8 = embed_c6_in_3q(vstar)
v8 = v8 / np.linalg.norm(v8)

f_exact = feasibility(vstar, triple)
print(f"exact feasibility  f(v*) = {f_exact:.12f}")
print(f"wall               W     = {W_EXACT:.12f}")
print(f"|f(v*) - W|              = {abs(f_exact - W_EXACT):.2e}")"""),

md("""## Measuring in a mutually unbiased basis

Measuring `v` in a basis `B` (columns = basis vectors) means rotating `B` to the computational
basis and reading out: outcome `j` has probability `p_j = |<B_j, v>|^2`. We extend each `6x6`
basis to an `8x8` unitary by acting as the identity on the two leakage states, prepare `v8`,
apply `U†`, and sample with Qiskit's `StatevectorSampler`."""),

code("""sampler = StatevectorSampler()
SHOTS = 40000

def sampled_distribution(basis6):
    U = np.eye(8, dtype=complex)
    U[:6, :6] = basis6                       # identity on leakage |110>,|111>
    qc = QuantumCircuit(3)
    qc.append(StatePreparation(v8), [0, 1, 2])
    qc.append(UnitaryGate(U.conj().T), [0, 1, 2])
    qc.measure_all()
    res = sampler.run([qc], shots=SHOTS).result()
    counts = res[0].data.meas.get_counts()
    p = np.zeros(8)
    for bits, c in counts.items():
        p[int(bits, 2)] = c / SHOTS
    return p

# one basis, to see a distribution
p0 = sampled_distribution(triple[0])
print("outcome probs in basis 0 (should be near-uniform 1/6 = 0.1667):")
print("  valid   :", np.round(p0[:6], 4))
print("  leakage :", np.round(p0[6:], 4), " (≈ 0)")"""),

md("""## The wall, sampled

Feasibility is `f = 1 - [ sum_i sum_j (p_j^(i) - 1/d)^2 ] / (1 - 1/d)`. We accumulate it over the
three bases from the **sampled** distributions and compare to the exact value and the wall."""),

code("""nonuniformity = 0.0
leakage = 0.0
for basis in triple:
    p = sampled_distribution(basis)
    leakage += p[LEAKAGE_KETS].sum()
    nonuniformity += np.sum((p[VALID_KETS] - 1.0 / D) ** 2)

f_sampled = 1.0 - nonuniformity / (1.0 - 1.0 / D)
print(f"sampled feasibility  f ~ {f_sampled:.6f}   ({SHOTS} shots/basis)")
print(f"exact feasibility    f = {f_exact:.6f}")
print(f"wall                 W = {W_EXACT:.6f}")
print(f"leakage mass           = {leakage:.2e}  (embedding is clean)")
print()
print(f"wall completion: {100*f_sampled/W_EXACT:.2f}%  (sampled near the wall; finite shots fluctuate, proof mode decides the ceiling)")"""),

md("""## Search is not proof

You just *felt* the wall: even the best state tops out at `W < 1`, never reaching the perfect
unbiasedness (`f = 1`) a fourth MUB would need. That is the obstruction, for this triple.

The game stops here. To **decide** it, switch to Mode A:

```sh
# from the Zenodo verification bundle (DOI 10.5281/zenodo.20682233)
make verify-global                                   # checks  max f <= W  exactly
python3 python/mub6_d6_wall_attainment_exact.py      # checks  f(v*) = W   exactly
```

Then earn atlas points by mapping the next brick: the T1 global certificate, the d=10 wall, an
independent verifier, a Lean formalization. See `../ATLAS.md` and `../SEED_ISSUES.md`.

**On hardware:** install `requirements-hardware.txt` and swap `StatevectorSampler()` for a real
`qiskit-ibm-runtime` SamplerV2 backend (after transpiling to its ISA) to run this on an IBM
Quantum device. That earns a *Hardware Scout* badge, an experimental badge, never a theorem
badge. Real hardware helps you feel the problem; exact certificates decide it.""")
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
nbf.write(nb, OUT)
print("wrote", os.path.relpath(OUT))
