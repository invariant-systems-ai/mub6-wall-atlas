/-
Mub6Lemmas — kernel-checked finite lemmas for the MUB(6) obstruction line.

Lifts the combinatorial spine of the theorem ledger from Python-checked
evidence artifacts to Lean theorems with an empty axiom footprint:

  • WordCount         the five-strata word-count separation theorem
  • RookBound         Lemma 1's Pauli/CRT 3×4 rook blocking bound
  • CatalogIncidence  the flat-modulus X₂×Q₀ K₂,₂ / K₆,₆ incidence laws
  • IChingBoardCap    the Z₆² full-line board: 12 lines, seam incidence,
                      the almost-disjoint cap at 3, and the CRT (Z₂-line,
                      Z₃-line) factorization — the isotropic-subgroup ↔
                      CRT board equivalence target

All proofs are `decide` over embedded finite data — no axioms, no
`native_decide`, no numerics. Declared next: the ℚ[√3] overlap-value laws
(catalog no-MU closure, second half).
-/

import Mub6Lemmas.WordCount
import Mub6Lemmas.RookBound
import Mub6Lemmas.CatalogIncidence
import Mub6Lemmas.IChingBoardCap
