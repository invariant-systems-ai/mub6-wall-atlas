/-
Finite-geometry lemmas of the flat-modulus X₂×Q₀ catalog
(theorem ledger 2026-05-20; `mub6_flat_modulus_x2q0_basis_catalog.py`
and `…_catalog_geometry.py`).

The 48 catalog vectors split 12 product / 36 entangled; the 16 catalog
bases (embedded verbatim below) split 4 product / 12 entangled. The
incidence laws proved here, kernel-checked over the embedded data:

  • the 4 product bases form K₂,₂ with sides {0,3} / {1,2}: cross-side
    pairs share exactly 3 vectors, same-side pairs share 0;
  • the 12 entangled bases split into the two hexads
    {4,8,9,12,13,15} / {5,6,7,10,11,14}: cross-hexad pairs share exactly
    1 vector, same-hexad pairs share 0 — the intersection graph is K₆,₆;
  • every entangled vector lies in exactly 2 bases, one per hexad, and
    the 36 resulting (left, right) pairs are pairwise distinct — since
    |K₆,₆ edges| = 36, the entangled vectors are EXACTLY the edges of
    that geometry;
  • product and entangled bases never intersect (kind partition).

These are the combinatorial halves of the catalog's no-MU closure; the
overlap-value laws over ℚ[√3] are the declared next module.
-/

namespace Mub6.Catalog

/-- The 16 catalog bases, verbatim from `CATALOG_BASES`. -/
def bases : List (List Nat) :=
  [[0, 1, 16, 17, 34, 35],
   [0, 3, 16, 19, 33, 35],
   [1, 2, 17, 18, 32, 34],
   [2, 3, 18, 19, 32, 33],
   [4, 5, 20, 21, 36, 37],
   [4, 15, 22, 24, 42, 44],
   [5, 14, 23, 25, 43, 45],
   [6, 8, 27, 28, 36, 47],
   [6, 9, 24, 25, 39, 41],
   [7, 8, 22, 23, 38, 40],
   [7, 9, 26, 29, 37, 46],
   [10, 12, 21, 30, 38, 41],
   [10, 13, 26, 27, 44, 45],
   [11, 12, 28, 29, 42, 43],
   [11, 13, 20, 31, 39, 40],
   [14, 15, 30, 31, 46, 47]]

/-- The 12 product vectors, verbatim from the catalog kind column. -/
def productVectors : List Nat := [0, 1, 2, 3, 16, 17, 18, 19, 32, 33, 34, 35]

def isProductVector (v : Nat) : Bool := productVectors.contains v

def basis (i : Nat) : List Nat := bases.getD i []

/-- |A ∩ B| for embedded bases (entries are duplicate-free by inspection,
    proved below in `bases_are_six_distinct`). -/
def interCount (a b : List Nat) : Nat := (a.filter b.contains).length

def productBases : List Nat := [0, 1, 2, 3]
def leftHexad : List Nat := [4, 8, 9, 12, 13, 15]
def rightHexad : List Nat := [5, 6, 7, 10, 11, 14]

/-- Every basis lists 6 pairwise-distinct vector indices. -/
theorem bases_are_six_distinct :
    bases.all (fun b => b.length = 6 && b.Pairwise (· ≠ ·)) = true := by decide

/-- Kind partition: bases 0–3 are entirely product, bases 4–15 entirely
    entangled. -/
theorem basis_kind_partition :
    (productBases.all fun i => (basis i).all isProductVector)
    ∧ ((leftHexad ++ rightHexad).all fun i => (basis i).all (!isProductVector ·)) := by
  decide

/-- K₂,₂ law on the product side: sides {0,3} / {1,2}; cross-side pairs
    share exactly 3 vectors, same-side pairs share 0. -/
theorem product_bases_form_K22 :
    interCount (basis 0) (basis 1) = 3 ∧ interCount (basis 0) (basis 2) = 3
    ∧ interCount (basis 3) (basis 1) = 3 ∧ interCount (basis 3) (basis 2) = 3
    ∧ interCount (basis 0) (basis 3) = 0 ∧ interCount (basis 1) (basis 2) = 0 := by
  decide

/-- K₆,₆ law on the entangled side: cross-hexad pairs share exactly one
    vector; same-hexad pairs are disjoint. -/
theorem entangled_bases_form_K66 :
    (leftHexad.all fun l => rightHexad.all fun r => interCount (basis l) (basis r) = 1)
    ∧ (leftHexad.all fun l => leftHexad.all fun l' =>
        l = l' || interCount (basis l) (basis l') = 0)
    ∧ (rightHexad.all fun r => rightHexad.all fun r' =>
        r = r' || interCount (basis r) (basis r') = 0) := by
  decide

/-- The bases containing a vector. -/
def basesContaining (v : Nat) : List Nat :=
  (List.range bases.length).filter fun i => (basis i).contains v

/-- The 36 entangled vectors (catalog indices outside the product list,
    range 0..47). -/
def entangledVectors : List Nat :=
  (List.range 48).filter fun v => !isProductVector v

/-- Edge law: every entangled vector lies in exactly two bases — one in
    each hexad. -/
theorem entangled_vectors_are_edges :
    entangledVectors.all (fun v =>
      (basesContaining v).length = 2
      && ((basesContaining v).filter leftHexad.contains).length = 1
      && ((basesContaining v).filter rightHexad.contains).length = 1) = true := by
  decide

/-- The 36 edges are pairwise distinct: no two entangled vectors produce the
    same (left, right) basis pair. With 6 × 6 = 36 possible pairs and 36
    vectors, the entangled catalog is EXACTLY the edge set of K₆,₆. -/
def edgeOf (v : Nat) : Nat × Nat :=
  (((basesContaining v).filter leftHexad.contains).getD 0 0,
   ((basesContaining v).filter rightHexad.contains).getD 0 0)

theorem entangled_edges_cover_K66 :
    entangledVectors.length = 36
    ∧ (entangledVectors.map edgeOf).Pairwise (· ≠ ·) := by decide

/-- Product/entangled bases never share a vector (the kind partition at the
    incidence level — one of the structural halves of the no-MU closure). -/
theorem product_entangled_bases_disjoint :
    (productBases.all fun p => (leftHexad ++ rightHexad).all fun e =>
      interCount (basis p) (basis e) = 0) = true := by decide

end Mub6.Catalog
