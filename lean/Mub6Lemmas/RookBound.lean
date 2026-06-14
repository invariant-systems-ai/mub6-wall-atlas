/-
Lemma 1 core (Pauli/CRT rook obstruction, lemma scaffold):
inside the Z₆² Pauli/Weyl control family, CRT reduces extension collisions
to the 3×4 rook board (3 projective lines of F₂², 4 of F₃²), with the
weighted collision defect

  defect = (2−1)·Σᵢ C(rowᵢ,2) + (3−1)·Σⱼ C(colⱼ,2).

The blocking bound: EVERY placement of 7 cells on the 3×4 board has
defect > 0 — in fact the minimum over all C(12,7) = 792 placements is
exactly 11 — so seven pairwise-collision-free stabilizer classes cannot
exist and the stabilizer path cannot complete MUB(6).

Placements are 12-bit masks (cell (r,c) ↦ bit r·4+c). A naive linear
`decide` over 4096 masks overflows the elaborator stack, so the sweep is a
BALANCED dyadic split (`sweepD`, recursion depth log₂ 4096 = 12) with a
once-proved soundness lemma transporting `sweepD … = true` to the bounded
universal statement. Everything is kernel-checked; no axioms.
-/

namespace Mub6.Rook

def rows : Nat := 3
def cols : Nat := 4

def choose2 (k : Nat) : Nat := k * (k - 1) / 2

def popcount (mask : Nat) : Nat :=
  ((List.range (rows * cols)).filter fun i => Nat.testBit mask i).length

def rowCount (mask r : Nat) : Nat :=
  ((List.range cols).filter fun c => Nat.testBit mask (r * cols + c)).length

def colCount (mask c : Nat) : Nat :=
  ((List.range rows).filter fun r => Nat.testBit mask (r * cols + c)).length

/-- Weighted collision defect: row weight (2−1)=1, column weight (3−1)=2 —
    the exact `rook_collision_defect` of the Python interface. -/
def defect (mask : Nat) : Nat :=
  1 * ((List.range rows).foldl (fun a r => a + choose2 (rowCount mask r)) 0)
  + 2 * ((List.range cols).foldl (fun a c => a + choose2 (colCount mask c)) 0)

/-! ### Balanced dyadic sweep (depth log₂ N, kernel-friendly) -/

/-- `sweepD check d lo` decides `check` on the dyadic block [lo, lo + 2^d). -/
def sweepD (check : Nat → Bool) : Nat → Nat → Bool
  | 0, lo => check lo
  | d + 1, lo => sweepD check d lo && sweepD check d (lo + 2 ^ d)

/-- Soundness: a true sweep covers every offset in its dyadic block. -/
theorem sweepD_sound (check : Nat → Bool) :
    ∀ d lo, sweepD check d lo = true → ∀ r < 2 ^ d, check (lo + r) = true := by
  intro d
  induction d with
  | zero =>
    intro lo h r hr
    have hr0 : r = 0 := Nat.lt_one_iff.mp hr
    simpa [hr0] using h
  | succ d ih =>
    intro lo h r hr
    rw [sweepD, Bool.and_eq_true] at h
    by_cases hcase : r < 2 ^ d
    · exact ih lo h.left r hcase
    · have hle : 2 ^ d ≤ r := Nat.le_of_not_lt hcase
      have hpow : 2 ^ (d + 1) = 2 ^ d + 2 ^ d := by
        rw [Nat.pow_succ, Nat.mul_two]
      have hr' : r - 2 ^ d < 2 ^ d := by omega
      have := ih (lo + 2 ^ d) h.right (r - 2 ^ d) hr'
      have harith : lo + 2 ^ d + (r - 2 ^ d) = lo + r := by omega
      simpa [harith] using this

/-! ### The blocking bounds -/

/-- Per-mask check for the sharp bound: 7 rooks force defect ≥ 11. -/
def checkEleven (mask : Nat) : Bool :=
  popcount mask != 7 || Nat.ble 11 (defect mask)

/-- Per-mask check for the disjoint-family cap: zero defect forces ≤ 3 rooks. -/
def checkCap (mask : Nat) : Bool :=
  defect mask != 0 || Nat.ble (popcount mask) 3

theorem sweep_eleven : sweepD checkEleven 12 0 = true := by decide +kernel

theorem sweep_cap : sweepD checkCap 12 0 = true := by decide +kernel

/-- THE BLOCKING BOUND (sharp form): every 7-rook placement on the 3×4
    CRT board has weighted collision defect at least 11. -/
theorem seven_rooks_defect_at_least_eleven :
    ∀ mask < 4096, popcount mask = 7 → 11 ≤ defect mask := by
  intro mask hmask hpop
  have h := sweepD_sound checkEleven 12 0 sweep_eleven mask (by simpa using hmask)
  simp only [Nat.zero_add, checkEleven] at h
  rcases Bool.or_eq_true_iff.mp h with hne | hble
  · exact absurd hpop (by simpa using hne)
  · exact Nat.le_of_ble_eq_true hble

/-- Lemma 1's cited form: the defect of any 7-class placement is positive —
    the stabilizer path is blocked. -/
theorem seven_rooks_always_collide :
    ∀ mask < 4096, popcount mask = 7 → 0 < defect mask := by
  intro mask hmask hpop
  have := seven_rooks_defect_at_least_eleven mask hmask hpop
  omega

/-- A witness placement attaining defect 11: rows split (3,2,2), columns
    split (2,2,2,1) — cells {(0,0),(0,1),(0,2),(1,0),(1,3),(2,1),(2,2)}.
    With the bound above, the minimum collision defect for 7 stabilizer
    classes is exactly 11. -/
def witnessMask : Nat := 0b011010010111

theorem witness_attains_eleven :
    popcount witnessMask = 7 ∧ defect witnessMask = 11 := by decide

/-- The disjoint-family cap: zero collision defect forces at most 3 classes
    — matching `largest disjoint family = 3` in the Python interface. The
    diagonal {(0,0),(1,1),(2,2)} attains it. -/
theorem zero_defect_caps_at_three :
    ∀ mask < 4096, defect mask = 0 → popcount mask ≤ 3 := by
  intro mask hmask hzero
  have h := sweepD_sound checkCap 12 0 sweep_cap mask (by simpa using hmask)
  simp only [Nat.zero_add, checkCap] at h
  rcases Bool.or_eq_true_iff.mp h with hne | hble
  · exact absurd hzero (by simpa using hne)
  · exact Nat.le_of_ble_eq_true hble

theorem diagonal_attains_three :
    popcount 0b10000100001 = 3 ∧ defect 0b10000100001 = 0 := by decide

end Mub6.Rook
