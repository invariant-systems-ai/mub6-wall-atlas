/-
The I Ching board cap (Z₆² Weyl phase-space board, projector-polytope
game round 5) — the long-declared "Z₆² isotropic-subgroup ↔ CRT board
equivalence" Lean target, upgrading the 3×4 rook board of `RookBound`
from board-level to subgroup-level.

The board is Z₆² = Z₆ × Z₆, the phase-space index set of the d = 6
Weyl–Heisenberg displacement operators. A FULL LINE is the cyclic
subgroup ⟨g⟩ = {t•g : t < 6} of an order-6 generator g — the board
shadow of a maximal-isotropic / monomial-stabilizer class. Two lines
are ALMOST-DISJOINT when they meet only at the origin (0,0). Proved
here, all kernel-checked `decide` over embedded finite data:

  • `order6_count`            Z₆² has 24 order-6 / 8 order-3 / 3 order-2 points
  • `lines_count`             there are exactly 12 full lines (canonical
                              generator list, pairwise distinct, complete)
  • `seam_incidence`          each order-6 point is on exactly 1 line,
                              each order-3 point on 3, each order-2 point on 4
  • `cap_three`               THE HEADLINE: no 4 full lines are pairwise
                              almost-disjoint, and 3 are (lines of
                              (0,1), (1,0), (1,1)) — the board cap is 3
  • `maximal_triples_count`   exactly 24 pairwise almost-disjoint triples
  • `lines_crt`               the structured reason: line ↦ (Z₂²-line,
                              Z₃²-line) is a bijection onto the 3 × 4 CRT
                              product, and almost-disjointness ⟺ BOTH
                              projections differ

CRT explanation of the cap: Z₆² ≅ Z₂² × Z₃², so every full line factors
as a (Z₂-line, Z₃-line) pair — 3 × 4 = 12 lines. Two lines sharing a
Z₂-line share its order-2 point; sharing a Z₃-line shares its order-3
points; so pairwise almost-disjoint families need pairwise-distinct
Z₂-lines — pigeonhole at 3. Together with `cap_three`'s witness the cap
is exactly 3: this is the board-level reason the MUB(6) Weyl/monomial
territory caps at 3 bases (3 < 7 needed; the analytic side lives in the
Python lane — this file is the combinatorial spine).

Conventions: a point p = (x, z) with x z < 6 is coded as the Nat
`6*x + z` (so lex order on (x, z) is numeric order on codes); a line is
its 36-bit characteristic mask (bit p ⟺ point p on the line); masks
embedded as literals are certified against the defining orbit folds
(`lineMasks_eq`, `adMatrix_eq`, `z2z3_lines_certified`). The two
bounded universals over the 4096 line-selection masks reuse the
balanced dyadic sweep of `RookBound` (`Mub6.Rook.sweepD` + its
soundness lemma) — a linear `decide` overflows the elaborator. No
axioms beyond `propext` / `Quot.sound`; no mathlib; no `native_decide`.
-/

import Mub6Lemmas.RookBound

namespace Mub6.IChing

/-! ### The board: Z₆² points coded as `6*x + z` -/

def px (p : Nat) : Nat := p / 6
def pz (p : Nat) : Nat := p % 6

/-- Scalar action `t • (x, z) = (t·x mod 6, t·z mod 6)` on codes. -/
def smul (t p : Nat) : Nat := 6 * ((t * px p) % 6) + ((t * pz p) % 6)

/-- Additive order: the least `n ∈ [1, 6]` with `n • p = 0`
    (well-defined on the board — every order divides 6). -/
def orderOf (p : Nat) : Nat :=
  (((List.range 6).map (· + 1)).filter fun n => smul n p == 0).headD 0

/-- The 36 board points. -/
def points : List Nat := List.range 36

/-- ORDER CENSUS: 24 points of order 6, 8 of order 3, 3 of order 2,
    and the origin alone of order 1 (24 + 8 + 3 + 1 = 36). -/
theorem order6_count :
    ((points.filter fun p => orderOf p == 6).length = 24)
    ∧ ((points.filter fun p => orderOf p == 3).length = 8)
    ∧ ((points.filter fun p => orderOf p == 2).length = 3)
    ∧ ((points.filter fun p => orderOf p == 1).length = 1) := by decide

/-! ### The 12 full lines -/

/-- The full line through `g`: the orbit {t•g : t < 6} as a 36-bit
    characteristic mask over board codes. -/
def lineMask (g : Nat) : Nat :=
  (List.range 6).foldl (fun m t => m ||| (1 <<< smul t g)) 0

/-- Canonical generators: the lexicographically least order-6 element of
    each full line — (0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5),
    (2,1), (2,3), (2,5), (3,1), (3,2). -/
def gens : List Nat := [1, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 20]

/-- The 12 line masks as literals (certified by `lineMasks_eq`), so the
    downstream sweeps reduce to constant-time bit tests. -/
def lineMasks : List Nat :=
  [63, 1090785345, 34630287489, 17247305985, 8608813569, 4563682305,
   2216757249, 604053513, 151031817, 302137353, 11010069, 5505045]

theorem lineMasks_eq : lineMasks = gens.map lineMask := by decide

/-- Number of board points on a mask. -/
def maskCard (m : Nat) : Nat :=
  ((List.range 36).filter fun p => Nat.testBit m p).length

/-- LINES COUNT: there are exactly 12 distinct full lines —
    (a) the 12 canonical generators all have order 6 and each is the
        lex-least order-6 element of its own line (canonicity),
    (b) each line carries exactly 6 points,
    (c) the 12 lines are pairwise distinct,
    (d) COMPLETENESS: every order-6 point generates one of the 12. -/
theorem lines_count :
    gens.length = 12
    ∧ (gens.all fun g => orderOf g == 6)
    ∧ (gens.all fun g =>
        ((points.filter fun p =>
          Nat.testBit (lineMask g) p && orderOf p == 6).headD 99) == g)
    ∧ (lineMasks.all fun m => maskCard m == 6)
    ∧ lineMasks.Pairwise (· ≠ ·)
    ∧ (points.all fun p =>
        orderOf p != 6 || lineMasks.contains (lineMask p)) := by decide

/-! ### Seam incidence -/

/-- Number of the 12 full lines through a point. -/
def linesThrough (p : Nat) : Nat :=
  (lineMasks.filter fun m => Nat.testBit m p).length

/-- SEAM INCIDENCE: every order-6 point lies on exactly 1 of the 12
    lines, every order-3 point on exactly 3, every order-2 point on
    exactly 4, and the origin on all 12. (Double count:
    24·1 + 8·3 + 3·4 + 1·12 = 72 = 12 lines × 6 points.) -/
theorem seam_incidence :
    points.all fun p =>
      (orderOf p != 6 || linesThrough p == 1)
      && (orderOf p != 3 || linesThrough p == 3)
      && (orderOf p != 2 || linesThrough p == 4)
      && (p != 0 || linesThrough p == 12) := by decide

/-! ### Almost-disjointness and the cap -/

/-- Lines `i, j` (indices into `lineMasks`) are almost-disjoint: their
    masks meet in exactly bit 0 — they share only the origin. -/
def almostDisjoint (i j : Nat) : Bool :=
  (lineMasks.getD i 0) &&& (lineMasks.getD j 0) == 1

def idx : List Nat := List.range 12

/-- The 12×12 Boolean almost-disjointness matrix as an explicit value
    (row i, column j), certified against the masks by `adMatrix_eq`.
    Each row has exactly six `true`s — the 2 other Z₂-lines × 3 other
    Z₃-lines of `lines_crt`. -/
def adMatrix : List (List Bool) :=
  [[false, true,  true,  true,  true,  true,  true,  false, false, false, false, false],
   [true,  false, true,  false, false, false, true,  true,  false, true,  true,  false],
   [true,  true,  false, true,  false, false, false, true,  true,  false, false, true ],
   [true,  false, true,  false, true,  false, false, false, true,  true,  true,  false],
   [true,  false, false, true,  false, true,  false, true,  false, true,  false, true ],
   [true,  false, false, false, true,  false, true,  true,  true,  false, true,  false],
   [true,  true,  false, false, false, true,  false, false, true,  true,  false, true ],
   [false, true,  true,  false, true,  true,  false, false, false, false, true,  true ],
   [false, false, true,  true,  false, true,  true,  false, false, false, true,  true ],
   [false, true,  false, true,  true,  false, true,  false, false, false, true,  true ],
   [false, true,  false, true,  false, true,  false, true,  true,  true,  false, false],
   [false, false, true,  false, true,  false, true,  true,  true,  true,  false, false]]

theorem adMatrix_eq :
    adMatrix = idx.map fun i => idx.map fun j => almostDisjoint i j := by decide

/-- The lines selected by a 12-bit mask: the indices of its set bits.
    Masks `< 4096` enumerate exactly the subsets of the 12 lines. -/
def selected (mask : Nat) : List Nat :=
  (List.range 12).filter fun i => Nat.testBit mask i

/-- Every pair from the list is almost-disjoint. -/
def allPairsAD : List Nat → Bool
  | [] => true
  | i :: rest => rest.all (almostDisjoint i) && allPairsAD rest

/-- Per-mask check for the cap: no 4-line selection is pairwise
    almost-disjoint. -/
def checkNoFour (mask : Nat) : Bool :=
  (selected mask).length != 4 || !allPairsAD (selected mask)

theorem sweep_no_four : Mub6.Rook.sweepD checkNoFour 12 0 = true := by
  decide +kernel

/-- THE HEADLINE CAP: there is NO set of 4 pairwise almost-disjoint full
    lines — every one of the C(12,4) = 495 four-line selections fails —
    while the lines of (0,1), (1,0), (1,1) (indices 0, 1, 2) are 3
    pairwise almost-disjoint full lines. The board cap is exactly 3. -/
theorem cap_three :
    (∀ mask < 4096, (selected mask).length = 4 →
        allPairsAD (selected mask) = false)
    ∧ allPairsAD [0, 1, 2] = true := by
  refine ⟨?_, by decide⟩
  intro mask hmask hlen
  have h := Mub6.Rook.sweepD_sound checkNoFour 12 0 sweep_no_four mask
    (by simpa using hmask)
  simp only [Nat.zero_add, checkNoFour] at h
  rcases Bool.or_eq_true_iff.mp h with hne | hnot
  · exact absurd hlen (by simpa using hne)
  · simpa using hnot

/-- The 24 pairwise almost-disjoint triples, as 12-bit selection masks
    (the 3 set bits = the 3 line indices), certified exhaustive by
    `maximal_triples_count`. -/
def adTriples : List Nat :=
  [7, 13, 25, 49, 67, 97, 134, 176, 268, 352, 536, 578,
   1154, 1184, 1288, 1312, 1538, 1544, 2180, 2192, 2308, 2368, 2576, 2624]

/-- Per-mask check: a 3-line selection is pairwise almost-disjoint iff
    its mask is listed in `adTriples`. -/
def checkTriples (mask : Nat) : Bool :=
  ((selected mask).length == 3 && allPairsAD (selected mask))
    == adTriples.contains mask

theorem sweep_triples : Mub6.Rook.sweepD checkTriples 12 0 = true := by
  decide +kernel

/-- TRIPLE CENSUS: exactly 24 unordered triples of pairwise
    almost-disjoint full lines — the 24 distinct masks of `adTriples`
    are pairwise almost-disjoint 3-line selections, and every pairwise
    almost-disjoint 3-line selection is one of them. All 24 are maximal,
    since `cap_three` forbids any 4th line. (CRT count: 3! injections of
    the 3 Z₂-lines into the 4 Z₃-lines = 4·3·2 = 24.) -/
theorem maximal_triples_count :
    adTriples.length = 24
    ∧ adTriples.Pairwise (· ≠ ·)
    ∧ (adTriples.all fun m =>
        (selected m).length == 3 && allPairsAD (selected m))
    ∧ (∀ mask < 4096, (selected mask).length = 3 →
        allPairsAD (selected mask) = true → adTriples.contains mask = true) := by
  refine ⟨by decide, by decide, by decide, ?_⟩
  intro mask hmask h3 had
  have h := Mub6.Rook.sweepD_sound checkTriples 12 0 sweep_triples mask
    (by simpa using hmask)
  simp only [Nat.zero_add, checkTriples, beq_iff_eq] at h
  rw [← h, Bool.and_eq_true]
  exact ⟨by simp [h3], had⟩

/-! ### CRT factorization: full lines = (Z₂²-line) × (Z₃²-line) -/

/-- Project a board mask to Z₂² (point (x, z) ↦ code `2*(x%2) + z%2`). -/
def projZ2 (m : Nat) : Nat :=
  (List.range 36).foldl
    (fun a p => if Nat.testBit m p
      then a ||| (1 <<< (2 * (px p % 2) + pz p % 2)) else a) 0

/-- Project a board mask to Z₃² (point (x, z) ↦ code `3*(x%3) + z%3`). -/
def projZ3 (m : Nat) : Nat :=
  (List.range 36).foldl
    (fun a p => if Nat.testBit m p
      then a ||| (1 <<< (3 * (px p % 3) + pz p % 3)) else a) 0

/-- Orbit mask of `g` on the Z₂² board (codes `2*x + z`, x z < 2). -/
def lineMask2 (g : Nat) : Nat :=
  (List.range 2).foldl
    (fun m t => m ||| (1 <<< (2 * ((t * (g / 2)) % 2) + (t * (g % 2)) % 2))) 0

/-- Orbit mask of `g` on the Z₃² board (codes `3*x + z`, x z < 3). -/
def lineMask3 (g : Nat) : Nat :=
  (List.range 3).foldl
    (fun m t => m ||| (1 <<< (3 * ((t * (g / 3)) % 3) + (t * (g % 3)) % 3))) 0

/-- The 3 full lines of Z₂²: ⟨(0,1)⟩, ⟨(1,0)⟩, ⟨(1,1)⟩. -/
def z2Lines : List Nat := [3, 5, 9]

/-- The 4 full lines of Z₃²: ⟨(0,1)⟩, ⟨(1,0)⟩, ⟨(1,1)⟩, ⟨(1,2)⟩. -/
def z3Lines : List Nat := [7, 73, 273, 161]

/-- The factor-board line lists are exactly the orbit masks of the factor
    generators, and they are COMPLETE: every nonzero point of Z₂² (resp.
    Z₃²) generates a listed line. -/
theorem z2z3_lines_certified :
    z2Lines = [lineMask2 1, lineMask2 2, lineMask2 3]
    ∧ z3Lines = [lineMask3 1, lineMask3 3, lineMask3 4, lineMask3 5]
    ∧ ((List.range 4).all fun g => g == 0 || z2Lines.contains (lineMask2 g))
    ∧ ((List.range 9).all fun g => g == 0 || z3Lines.contains (lineMask3 g)) := by
  decide

/-- CRT STRUCTURE THEOREM: the projection map
    line ↦ (its Z₂²-line, its Z₃²-line)
    (a) lands in the 3 × 4 product of factor-board lines,
    (b) is injective on the 12 lines — hence a BIJECTION onto the 12
        pairs (3 Z₂-lines) × (4 Z₃-lines), and
    (c) two lines are almost-disjoint ⟺ BOTH projections differ.
    So pairwise almost-disjoint families need pairwise-distinct Z₂-lines:
    pigeonhole caps them at 3 — `cap_three` as structured fact. -/
theorem lines_crt :
    (lineMasks.all fun m =>
      z2Lines.contains (projZ2 m) && z3Lines.contains (projZ3 m))
    ∧ (lineMasks.map fun m => (projZ2 m, projZ3 m)).Pairwise (· ≠ ·)
    ∧ (idx.all fun i => idx.all fun j =>
        almostDisjoint i j
          == (projZ2 (lineMasks.getD i 0) != projZ2 (lineMasks.getD j 0)
              && projZ3 (lineMasks.getD i 0) != projZ3 (lineMasks.getD j 0))) := by
  decide

end Mub6.IChing
