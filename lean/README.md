# mub6-lemmas, kernel-checked finite lemmas for the MUB(6) obstruction line

Lifts the combinatorial spine of the MUB(6) theorem ledger from
Python-checked evidence artifacts to Lean 4 theorems checked by the kernel.
`lake build Mub6Lemmas` on the pinned toolchain (`leanprover/lean4:v4.20.0`)
re-verifies everything; no mathlib, no `native_decide`, no numerics.

| Module | Source claim | Headline theorems | Axioms |
|---|---|---|---|
| `WordCount` | word-count obstruction closure (theorem ledger 2026-05-20; `mub6_word_count_analytic_proof.py`) | the five strata word counts are 7/4/6/12/21 and pairwise distinct (`word_count_separates_strata`); the structural zero removes exactly 9 ordered 3-cycles (30 → 21) | **none** |
| `RookBound` | Lemma 1, Pauli/CRT rook obstruction (lemma scaffold; `test_mub6_pauli_crt_rook_interface.py`) | every 7-rook placement on the 3×4 CRT board has weighted defect ≥ 11 (`seven_rooks_defect_at_least_eleven`, sharp by witness); zero defect caps families at 3 (`zero_defect_caps_at_three`) | `propext`, `Quot.sound` only |
| `CatalogIncidence` | flat-modulus X₂×Q₀ catalog incidence lemmas (`mub6_flat_modulus_x2q0_*` modules) | the 4 product bases form K₂,₂ ({0,3}/{1,2}, cross-share 3); the 12 entangled bases form K₆,₆ via the hexads {4,8,9,12,13,15}/{5,6,7,10,11,14} (cross-share 1, same-side 0); the 36 entangled vectors are exactly the K₆,₆ edges; product/entangled bases are disjoint | **none** |
| `IChingBoardCap` | the Z₆² Weyl phase-space board cap (projector-polytope game round 5; the Z₆² isotropic-subgroup ↔ CRT board equivalence target) | Z₆² has 24/8/3 points of order 6/3/2 (`order6_count`); exactly 12 full lines, canonical generators, complete (`lines_count`); seam incidence 1/3/4 per order stratum (`seam_incidence`); **no 4 pairwise almost-disjoint full lines, 3 exist** (`cap_three`); exactly 24 almost-disjoint triples (`maximal_triples_count`); line ↦ (Z₂-line, Z₃-line) is a bijection onto 3×4 and almost-disjointness ⟺ both projections differ (`lines_crt`) | `propext`, `Quot.sound` only |

Engineering notes:

- Bounded universals over the 4096 placement masks use a **balanced dyadic
  sweep** (`sweepD`, recursion depth log₂ N) with a once-proved soundness
  lemma, a naive linear `decide` overflows the elaborator stack. The sweep
  leaves are evaluated with `decide +kernel`.
- One claim in this lane was CORRECTED by the kernel during formalization:
  the structural-zero refinement removes 9 ordered 3-cycles (30 → 21 in the
  ordered-triple count used by the analytic module), not the 6 suggested by
  the prose's block-only convention. The separating counts themselves
  (7/4/6/12/21) verify exactly as published.

Declared next targets: the ℚ[√3] overlap-value laws completing the
catalog's no-MU closure in Lean; the 13-family catalog exhaustiveness.
(The Z₆² maximal-isotropic-subgroup ↔ CRT board equivalence landed as
`IChingBoardCap`, reusing `RookBound`'s `sweepD` for the two bounded
universals over the 4096 line-selection masks.)
