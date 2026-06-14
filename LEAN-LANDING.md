# MUB(6) Wall Atlas: a Lean formalization challenge

A research game wrapped around a Lean 4 verification target. If you are a Lean person, this is
the front door; the points, badges, and Qiskit puzzle are an outer ring you can ignore.

The narrow claim is deliberately small: **one exact feasibility wall after one canonical product
triple in dimension six, not a solution to MUB(6).** That restraint is the point. The invitation
is to reproduce, audit, formalize, or break scoped pieces of it.

## Build the Lean layer now (it is in this repo)

The combinatorial spine of the obstruction is already kernel-checked. From the repo root:

```sh
cd lean
lake build Mub6Lemmas              # pinned toolchain leanprover/lean4:v4.20.0; no mathlib, no native_decide
lake env lean AxiomAudit.lean      # prints the axiom footprint of every headline theorem
```

`lake build` re-verifies everything from the kernel; there are no numerics in the proof path and
no network dependency beyond the toolchain. (This `lean/` tree mirrors the one in the Zenodo
verification bundle; the heavier analytic verifier and certificate live in the bundle, see
`README.md`.)

## Theorem inventory (`Mub6Lemmas`)

| module | headline theorems | axioms |
|---|---|---|
| `WordCount` | the five strata word counts are `7/4/6/12/21` and pairwise distinct (`word_count_separates_strata`); the structural zero removes exactly 9 ordered 3-cycles (`30 -> 21`) | **none** |
| `RookBound` | every 7-rook placement on the 3x4 CRT board has weighted defect `>= 11` (`seven_rooks_defect_at_least_eleven`, sharp by witness); zero defect caps families at 3 (`zero_defect_caps_at_three`) | `propext`, `Quot.sound` |
| `CatalogIncidence` | the 4 product bases form `K(2,2)`; the 12 entangled bases form `K(6,6)`; the 36 entangled vectors are exactly the `K(6,6)` edges; product and entangled bases are disjoint | **none** |
| `IChingBoardCap` | `Z6^2` has `24/8/3` points of order `6/3/2`; exactly 12 full lines; **no 4 pairwise almost-disjoint full lines, but 3 exist** (`cap_three`); exactly 24 almost-disjoint triples; the line-to-`(Z2,Z3)` map is a bijection onto the 3x4 board | `propext`, `Quot.sound` |

A nice honesty hook for skeptics: **the kernel corrected a claim during formalization.** The
structural-zero refinement removes 9 ordered 3-cycles (`30 -> 21`), not the 6 the prose's
block-only convention suggested; the separating counts `7/4/6/12/21` then verify exactly. That is
the formalization doing its job.

## What is Lean-checked and what is not

Lean here certifies the **finite combinatorial spine** (above). The **analytic chain** of the
load-bearing wall, the exact PSD/Veronese certificate that bounds the feasibility functional `f`,
is exact-arithmetic Python today (`make verify-global` in the bundle), **not yet in Lean**.
Carrying pieces of it into the kernel is the open frontier and the reason this is a challenge,
not a finished artifact. See `FAQ.md` ("Isn't this just Lean?") for how the Lean layer and the
receipt layer relate: Lean proves, the receipts record provenance.

## First formalization bricks (pick one, scoped small)

These are the concrete asks. Each is meant to be reviewable on its own.

- **B4a** Formalize the feasibility identity: `f(v) = 1` iff `v` is unbiased to all three bases of
  the canonical triple (a vanishing sum of squares). Small, self-contained, the natural entry.
- **B4b** Formalize the 18 exact attainment overlap identities for the witness `v*`.
- **B4c** Independently re-formalize the `Z6^2` Weyl-board cap (`cap_three`) or the rook bound,
  ideally by a different route than `RookBound`'s dyadic `sweepD`, to cross-check the kernel work.
- **B4d** A design question, not a proof: is the **no-mathlib** constraint wise here, or is a
  mathlib-dependent version more community-friendly and more reusable? Argue it either way.

See `SEED_ISSUES.md` for the full brick list. The right first message is "is B4a a good Lean
target?", not "please evaluate the whole atlas."

## How to engage (and how not to)

- **Do** discuss it on the Lean Zulip and run `lake build` / the axiom audit. Skepticism is
  wanted; a broken brick is useful data.
- **Not yet** a mathlib PR. Per mathlib's own contribution guidance, a fast-moving topic outside
  core maintainer expertise is better as a standalone project depending on mathlib (or, as here, a
  no-mathlib kernel-audit project) until it has settled. B4d is exactly that decision.
- **Later**, once there are 6 to 10 Lean-native levels that teach the needed finite linear algebra
  and combinatorics, a Lean Game Server game is the natural next step. This repo's "game" today is
  a research-coordination game, not yet a Lean proof game.

## Prior work, first

Before the project language gets ambitious: this stands on decades of others' work (Wootters and
Fields; Zauner; Bengtsson et al.; McNulty and Weigert; and more). McNulty and Weigert already
proved analytically that no MU vector extends this product triple; what is new is the exact value
and a machine-checkable certificate. See [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md).
