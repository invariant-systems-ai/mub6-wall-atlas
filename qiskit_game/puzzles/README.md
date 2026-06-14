# Puzzle levels

A ramp from "what does mutually unbiased even mean" to "map an open frontier." Each level states
its room, its task, and how it scores. Native qubit rooms (d=4, d=8) come first; d=6 is where the
wall lives; the last levels hand off to Mode A (exact proof) and the open bricks.

> Reminder: these are search/teaching tasks. A high game score is not a proof. The line is the
> whole point (see `../README.md`).

## Level 0: Three qubit lenses  (d=2)

Measure one qubit in the Z, X, and Y bases and watch the outcome distributions. Discover what
"mutually unbiased" means: a state sharp in one lens is maximally flat in the others. Onboarding.

## Level 1: Build a MUB pair  (d=2 or d=3)

Find a state, or a whole basis, unbiased to a given basis. Score: reach flat distributions
(`f = 1` against the single known basis). Teaches the target the d=6 room will deny you.

## Level 2: The solved board  (d=8)

Three qubits, a native room. Reconstruct the Pauli classes: partition the 63 nonidentity Paulis
into 9 commuting classes of 7. This is the control case where everything *does* close, so the
d=6 obstruction afterward is meaningful rather than mysterious.

## Level 3: The MUB(6) wall  (d=6, the milestone)

Embed `C^6` in three qubits (`|110>, |111>` are leakage). Search for a state with high
fourth-vector feasibility against the canonical-style triple. The game shows your `f`, the proven
wall `W = (88 + 3*sqrt(6))/100`, and the remaining defect. Run:

```sh
python3 ../play.py
```

You will climb to about `f = 0.9534` and stop. You touched the wall. Score: `wall_completion =
100 * f / W`.

## Level 4: Certificate forge  (d=6)

High score is not enough. Switch from search to proof: download the verification bundle and run

```sh
make verify-global
python3 python/mub6_d6_wall_attainment_exact.py
```

Earn the `Verifier Passed` badge. This is where game points become atlas points.

## Level 5: Map the next wall  (open frontiers)

Pick a real brick: the T1 global certificate, the d=10 closed-form hunt, an independent verifier
in Sage/Julia, a Lean formalization, a Weyl-board visualization, or a noisy-hardware
demonstration. See `../ATLAS.md` and `../SEED_ISSUES.md`. These mint new atlas nodes.
