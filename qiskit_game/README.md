# MUB(6) Wall Atlas: the puzzle lab

**A Qiskit-powered quantum puzzle lab for mapping one of quantum information's stubborn walls,
one checkable brick at a time.**

The theorem bundle is the boss room: one exact pinned-triple wall in MUB(6). This game layer
does three things around it: *teach the geometry*, *let people play with states and measurement
bases*, and *route serious players toward exact verification and new wall-mapping bricks*. It
does not replace the proof.

## The honest split: search vs proof

There are two modes, and the line between them is the whole point.

- **Mode A (proof).** The exact, kernel-and-certificate-backed statement
  `max f = W = (88 + 3*sqrt(6))/100` for the canonical triple. It lives in the Zenodo
  verification bundle (`make verify-global` + the exact attainment module). Float never touches
  the claim path.
- **Mode B (play).** This game. It computes the published feasibility functional in float64 so a
  player can *feel* the wall, and (optionally) uses Qiskit to sample measurement outcomes. It is
  an embedded simulation, labeled as such. **Search points are not proof points.**

A wall touched in the game is an invitation to verify it in Mode A.

## What is exact here, and what is not

- The feasibility functional `f(v) = 1 - [ sum_i sum_j (p_j^(i) - 1/d)^2 ] / (1 - 1/d)` is the
  published feasibility identity (Lemma 2.1 of the paper / bundle), evaluated here in float64
  (numerical, Mode B). `f = 1` iff `v` is unbiased to all three bases (a fourth-MUB vector).
- `src/mub6_game/feasibility.py` scores candidates against the **exact canonical triple**.
  `tools/extract_canonical.py` derives that triple and the attainment witness `v*` from the
  verified bundle and writes `data/canonical_triple.json`; the self-test then asserts
  `f(v*) = W` to machine precision (`|f - W| = 0`). The game is *bound to the proof*, not a
  lookalike. (If the data file is absent, the game falls back to a formula-built triple of the
  same construction.)
- **Validation, end to end.** `play.py` (pure search) climbs to about `f ~ 0.9534` and stalls at
  the wall. The Qiskit notebook `notebooks/03_mub6_embedded_wall.ipynb` prepares `v*` on three
  qubits, measures it in the three MUBs with `StatevectorSampler`, and recovers `f ~ 0.953`
  (the exact figure fluctuates with shot count) against the proven `W = 0.95348`, with zero
  leakage. The exact and sampled feasibilities and the proven wall agree to within sampling noise.

## C^6 on qubit hardware

MUB(6) is a qudit problem (`C^6 = C^2 (x) C^3`); Qiskit hardware is qubit-based. The game embeds
`C^6` into three qubits and marks two states as leakage:

```
valid:   |000> |001> |010> |011> |100> |101>    (carry C^6)
leakage: |110> |111>                            (amplitude 0; flagged if populated)
```

`feasibility.embed_c6_in_3q` / `project_3q_to_c6` handle the embedding. Qiskit `Sampler` runs are
educational/experimental **badges**, never theorem badges: real hardware helps people *feel* the
problem; exact certificates *decide* it.

## Ways to play (pick your rung)

The rungs are ordered by **tooling cost**, cheapest first. The point of the cheap rungs is not
that they are easy but that they are **small**: a skeptic who hand-checks the parts they can will
more readily grant the 441x441 certificate they cannot. Pick the lowest rung you are comfortable
with and climb.

| rung | cost | what you do | mode |
|---|---|---|---|
| 1. **By hand** | none | The d=2 (Z/X/Y) and d=3 (Gauss-sum) MUBs are small explicit matrices; the product-ceiling law `f_prod = (d-a)/(d-1)` is hand-checkable; `W = (88+3*sqrt6)/100 ~ 0.9535` is a calculator sanity check. Worked out in [`BY-HAND.md`](BY-HAND.md). The 441x441 PSD certificate is deliberately *not* pen-and-paper. | B / A |
| 2. **With an AI** | none | Use any model as a scratchpad: build the triple, hill-climb `f`, explain the wall, and write sanity checks. See [`PLAY-WITH-AI.md`](PLAY-WITH-AI.md). | B |
| 3. **Python** | `numpy` | `play.py`, `feasibility.py`, `score_atlas.py`. The default. | B |
| 4. **Qiskit (local)** | `qiskit` | `notebooks/03_mub6_embedded_wall.ipynb`: prepare the state on 3 qubits, sample the three MUBs. | B |
| 5. **Real hardware** | IBM account | Optional: swap in an `qiskit-ibm-runtime` backend for a *feel-it* run. Earns a `Hardware Scout` badge, **never** a theorem badge. Terms change, so we do not document them; see <https://quantum.ibm.com> and IBM's own docs. | B |
| 6. **Proof** | the bundle | `make verify-global` in the Zenodo bundle. Where game play becomes a checked theorem. | A |

A note for rungs 1, 2, and 5, given the "never label up" rule: a search (by hand, by AI, or on
hardware) that reaches `f ~ 0.953` is **Mode B**. An AI-written explanation is not a certificate. The proof is rung 6, and only rung 6.

## Roles and badges

| role | does |
|---|---|
| **Explorer** | runs puzzles, searches for high-feasibility states |
| **Cartographer** | adds atlas nodes and visualizations |
| **Verifier** | reruns proofs/certificates (Mode A) |
| **Formalizer** | moves claims into Lean / Sage |
| **Scout** | explores T1, d=10, d=14, d=15, d=24 |

Badges: `First Run` · `Witness Found` · `Wall Touched` · `Verifier Passed` · `Bug Hunter` ·
`Lean Brick` · `Qiskit Room Builder` · `Hardware Scout` · `Atlas Cartographer`. Badges record
*what you did*; [atlas points](../POINTS.md) record *how strong it was*.

## Levels

See `puzzles/`. The arc: native qubit rooms (d=4, d=8) teach the measurement game; the d=6 room
introduces the wall; the advanced rooms hand off to Mode A and the open frontiers.

## Quick start

```sh
pip install numpy                         # the math core needs only numpy
python3 src/mub6_game/feasibility.py      # self-test: MUB triple + f, and f(v*) = W to machine precision
python3 play.py                           # climb toward the wall and read a scorecard
```

For the quantum notebook (Qiskit, local simulation):

```sh
pip install -r requirements.txt           # numpy, qiskit, jupyter (no hardware deps)
jupyter notebook notebooks/03_mub6_embedded_wall.ipynb
```

For real IBM Quantum hardware runs (optional, heavier):

```sh
pip install -r requirements-hardware.txt  # adds qiskit-ibm-runtime
```

To regenerate the canonical-triple binding from the verification bundle:

```sh
PYTHONPATH=<bundle>/python python3 tools/extract_canonical.py <bundle>
```

## Scope (read this)

This is **pure mathematics about MUB feasibility**: unbiasedness, the feasibility wall,
witnesses. It is not about error detection or correction, and contributions should not frame it
that way. Same lane as the rest of the atlas.

## License

Code Apache-2.0; docs CC BY 4.0. See the repository root `LICENSE`.
