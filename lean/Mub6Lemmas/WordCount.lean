/-
Word-count separation theorem (MUB(6) Sublemma 7D closure / word-count
obstruction closure, theorem ledger 2026-05-20).

The triad holonomy WORD COUNT is the number of directed 3-cycles in the
support graph of the 6×6 transition matrix H[i][j] = √6·⟨ref_i|basis_j⟩.
The five canonical strata have the five support graphs embedded below
(mirroring `mub6_word_count_analytic_proof.py` exactly), and their word
counts 7 / 4 / 6 / 12 / 21 are pairwise distinct — so the word count is a
complete separating invariant for the strata, closing the thirteen-family
elimination at 13/13.

Every theorem here is kernel-checked by `decide` over the embedded finite
data: no axioms, no native evaluation, no numerics.
-/

namespace Mub6.WordCount

/-- A support digraph on nodes 0..5: row `i` lists the successors of `i`. -/
abbrev Adj := List (List Nat)

def succs (g : Adj) (i : Nat) : List Nat := g.getD i []

/-- Ordered triples (l, m, r) with l→m, m→r, r→l all edges — the exact
    counting rule of `count_directed_3cycles` in the Python analytic proof. -/
def count3Cycles (g : Adj) : Nat :=
  (List.range g.length).foldl
    (fun acc l =>
      (succs g l).foldl
        (fun acc m =>
          (succs g m).foldl
            (fun acc r => acc + (if (succs g r).contains l then 1 else 0))
            acc)
        acc)
    0

/-- Entangled interior (θ > 0): each column supports a Z₃-cyclic two-block. -/
def entangledInterior : Adj := [[0,1],[2,3],[4,5],[4,5],[0,1],[2,3]]

/-- Tensor-grid boundary (θ = 0): permutation support. -/
def tensorGridBoundary : Adj := [[0],[2],[4],[5],[1],[3]]

/-- Non-grid origin (p₁₂ = p₂₃ = 0): both blocks identity. -/
def nonGridOrigin : Adj := [[0],[1],[2],[3],[4],[5]]

/-- Non-grid axis (one parameter active): one dense 2×2 sub-block. -/
def nonGridAxis : Adj := [[0],[1],[2],[3,4],[3,4],[5]]

/-- Non-grid interior (both parameters active): the structural zero
    T[2][0] = (R₁₂ row 2)·(R₂₃ col 0) = 0 caps row 5's support at {4,5}. -/
def nonGridInterior : Adj := [[0],[1],[2],[3,4,5],[3,4,5],[4,5]]

theorem entangled_interior_word_count : count3Cycles entangledInterior = 7 := by decide
theorem tensor_grid_boundary_word_count : count3Cycles tensorGridBoundary = 4 := by decide
theorem non_grid_origin_word_count : count3Cycles nonGridOrigin = 6 := by decide
theorem non_grid_axis_word_count : count3Cycles nonGridAxis = 12 := by decide
theorem non_grid_interior_word_count : count3Cycles nonGridInterior = 21 := by decide

/-- The five word counts in stratum order. -/
def strataWordCounts : List Nat :=
  [count3Cycles entangledInterior,
   count3Cycles tensorGridBoundary,
   count3Cycles nonGridOrigin,
   count3Cycles nonGridAxis,
   count3Cycles nonGridInterior]

/-- THE SEPARATION THEOREM: the word count takes five pairwise-distinct
    values across the five canonical strata, so it is a complete separating
    invariant for them. -/
theorem word_count_separates_strata : strataWordCounts.Pairwise (· ≠ ·) := by decide

/-- The structural-zero refinement: without the architectural zero
    T[2][0] = 0 the interior support would carry the full dense lower
    block (total ordered count 30 = 3 identity self-cycles + 27 block
    triples); the zero removes exactly 9 ordered 3-cycles, landing the
    interior at its separating value 21. -/
def nonGridInteriorWithoutZero : Adj := [[0],[1],[2],[3,4,5],[3,4,5],[3,4,5]]

theorem structural_zero_removes_nine_cycles :
    count3Cycles nonGridInteriorWithoutZero = 30 ∧
    count3Cycles nonGridInteriorWithoutZero - count3Cycles nonGridInterior = 9 := by decide

end Mub6.WordCount
