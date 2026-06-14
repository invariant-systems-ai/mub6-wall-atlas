# The wall map

What is mapped, what is open, and how strong each piece of evidence is. The map is the
product, not any single result. Negative results (a closed form that does **not** exist, an SOS
certificate that is provably absent) are first-class entries.

The mapped walls below are *exact-certification* contributions on a board built over decades by
others (Wootters-Fields, Zauner, Bengtsson et al., McNulty-Weigert, and more); see
[`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md). What is new is exactness and checkability of particular
walls, not their existence.

**Evidence levels.** `exact` = end-to-end rational / cyclotomic-field arithmetic, no floats in
the claim path. `kernel` = Lean 4 theorem, axiom footprint at most `{propext, Quot.sound}`.
`60-digit` = high-precision numerics (evidence, not proof). `float` = float64 numerics
(reproducible experiment, not proof).

## Mapped walls (load-bearing and companion)

| # | wall / result | statement | level | artifact |
|---|---|---|---|---|
| M1 | **Canonical triple wall (two-sided)** | `max f = W = (88 + 3√6)/100` after `{Z₂⊗Z₃, X₂⊗Q₀, Y₂⊗Q₁}` | **exact** + independent verifier | `mub6_d6_wall_attainment_exact`, `mub6_global_wall_exact_certificate`, `mub6_transport_closure_exact`, `verify_global_certificate.py` |
| M2 | Local interval certificate | `f(u) < W` for all `0 < θ(u,v*) ≤ r₀ = 111/12640` | exact | `mub6_d6_wall_local_certificate` |
| M3 | Product-ceiling law | `f_prod = (d−a)/(d−1)`, plus the unaligned/conditioned extension | exact | `mub6_product_ceiling_law_verifier`, `mub6_unaligned_product_ceiling` |
| M4 | **T1 second wall (attainment)** | `W(T1) = (1163 + 38√3)/1265`, exact algebraic witness; minpoly `6325x² − 11630x + 5329` | exact (attainment side) | `mub6_t1_wall_study`, `mub6_t1_exact_attainment` |
| M5 | d12/d24 defect identity | `11·(1−W₁₂) = 23·(1−W₂₄)`, explained by the lift-law lemma | exact + 60-digit | `mub6_d12_d24_closed_form_hunt`, `mub6_round7_profile_lift_algebra`, `mub6_lift_law_lemma` |
| M6 | d=16 board room | 17 MUBs via dual-basis symplectic spread over GF(16), exact 255-dim tiling | exact chain | `mub6_d16_room_scan` |
| M7 | Two-board combinatorial frame | F₂⁶ hexagram board + Z₆² Weyl board (12 lines, 24 maximal triples, CRT factorization) | **kernel** (Lean) | `mub6_iching_weyl_boards`, `lean/Mub6Lemmas/IChingBoardCap.lean` |
| M8 | No naive SOS | no degree-4 and no degree-6 SOS certificate for `W − f` in the naive cone (a *negative* result) | exact | `mub6_degree6_refutation_exact` |

## Open frontiers (bricks to claim)

| brick | frontier | what "done" looks like | level target | difficulty |
|---|---|---|---|---|
| [B1](SEED_ISSUES.md) | Reproduce | `make verify-global` + attainment pass on Linux / macOS / NixOS / Windows, transcript posted | n/a (RSE) | easy |
| [B2](SEED_ISSUES.md) | Audit | Independently parse `global-wall-certificate-Q-exact.json.gz` and re-check the identity `[B]` from scratch | exact | medium |
| [B3](SEED_ISSUES.md) | Audit | Re-implement the upper-bound checker in **Sage / Julia / Lean / Magma** and confirm `max f ≤ W` | exact | medium-hard |
| [B4](SEED_ISSUES.md) | Formalize | Carry more of the analytic chain into the Lean kernel (a named paper lemma, the local certificate, or the attainment identities) | kernel | hard |
| [B5](SEED_ISSUES.md) | Extend | The matching **global upper bound** for T1, making `W(T1)` two-sided like M1 | exact | hard |
| [B6](SEED_ISSUES.md) | Extend | A closed form or a structural obstruction for the d=10 wall (defect ≈ 0.0225; no closed form found yet) | 60-digit → exact | hard |
| [B7](SEED_ISSUES.md) | Document | A standalone note on the Z₆² Weyl-board census (lines, triples, CRT structure) readable without the rest | exact | easy-medium |
| [B8](SEED_ISSUES.md) | Survey | A labeled census of prior MUB(6) obstruction / non-existence results and how M1 relates | n/a (survey) | medium |
| [B9](SEED_ISSUES.md) | Audit | Extend the skeptical FAQ: add the question you would ask, with the answer you find | n/a | easy |
| B10 | Extend | Parametric product triples between T0 and T1 (does the wall move continuously? in what field?) | 60-digit → exact | hard |
| B11 | Extend | The d=24 aligned product room: exactify the `21/23` ceiling prediction beyond float | float → exact | medium-hard |

If a brick you want is not listed, propose it (see the new-wall issue template). New frontiers
are welcome; so are corrections to anything above.

## How a brick enters the map

1. Claim it (comment on its issue, or open one from the template).
2. Do the work locally; keep the evidence level honest.
3. Submit it (PR adding your artifact + a one-paragraph result note, or a linked external repo).
4. It gets an independent check from at least one other contributor.
5. It lands in this table with your name and its evidence level.

A brick that *fails* (the closed form is not there, the certificate has a gap) is still a
contribution. Label it and it goes in the map as a negative result.
