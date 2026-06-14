# Seed issues

The first bricks. Each block below is a ready-to-open issue: copy the title and body into a new
GitHub/GitLab issue, or just comment here to claim one. Labels in brackets.

Difficulty: 🟢 easy · 🟡 medium · 🔴 hard. Evidence target uses the levels from
[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## B1: Run the verifier on your platform  🟢  `[reproduce] [good-first-brick]`

**Goal.** Confirm the load-bearing theorem reproduces off the author's machine.

**Do.** From the artifact bundle root: `sha256sum -c SHA256SUMS`, then `make verify-global`,
then `python3 python/mub6_d6_wall_attainment_exact.py`. Record your OS, Python version, wall
time, and peak memory; paste the PASS/FAIL transcript.

**Done when.** A transcript is posted for at least one of Linux / macOS / NixOS / Windows that
was not already covered. A *failure* (build error, timeout, mismatch) is an equally valuable
result; post it.

---

## B2: Independently parse and re-check the certificate matrix  🟡  `[audit]`

**Goal.** Re-check the global-wall identity from the stored `Q` without using the bundle's
verifier.

**Do.** Load `evidence/global-wall-certificate-Q-exact.json.gz` yourself (441×441 symmetric
over `Q(√2,√3)`, upper triangle, common denominator). Re-expand `ztilde(v)ᵀ Q ztilde(v)` and
`G_hom(v)·|v|⁴` on the degree-4 monomial basis and confirm coefficient-by-coefficient equality
in exact arithmetic, in a language/tool of your choice.

**Done when.** An independent script (any system) reproduces identity check `[B]` and posts the
worst-case exact residual (should be exactly zero). **Evidence target: `exact`.**

---

## B3: Re-implement the upper-bound checker in another system  🔴  `[audit]`

**Goal.** A second, independent implementation of `max f ≤ W`.

**Do.** Re-implement the certificate check (identity + PSD-on-kernel-complement) in **Sage,
Julia, Lean, or Magma**, ideally rebuilding the canonical triple from first principles as the
Python verifier does. Ship it as your own repo.

**Done when.** Your checker confirms `max f ≤ W = (88+3√6)/100` and a link + headline result is
added to `ATLAS.md` (M1 gets a second independent checker). **Evidence target: `exact`.**

---

## B4: Formalize a piece of the analytic chain in Lean  🔴  `[formalize]`

**Goal.** Carry more of the proof into the kernel. Today the combinatorial spine is Lean
(`lean/Mub6Lemmas`: WordCount, RookBound, CatalogIncidence, IChingBoardCap); the analytic chain
is `exact` Python but not yet kernel. See [`LEAN-LANDING.md`](LEAN-LANDING.md) to build it.

Pick **one** of these scoped sub-bricks (each reviewable on its own). The right first message is
"is B4a a good Lean target?", not "evaluate the whole atlas."

- **B4a** Formalize the feasibility identity: `f(v) = 1` iff `v` is unbiased to all three bases of
  the canonical triple (a vanishing sum of squares). The natural entry point: small, self-contained.
- **B4b** Formalize the 18 exact attainment overlap identities for the witness `v*`.
- **B4c** Independently re-formalize the `Z6^2` board cap (`cap_three`) or the rook bound by a
  different route than `RookBound`'s dyadic `sweepD`, as a cross-check of the kernel work.
- **B4d** (design, not proof) Argue whether the **no-mathlib** constraint is wise here or whether a
  mathlib-dependent version is more community-friendly and reusable.

**Done when.** For a proof brick, `lake build` re-checks the new theorem and `AxiomAudit` shows
its footprint (`{propext, Quot.sound}` or fewer). For B4d, a reasoned recommendation is posted.
**Evidence target: `kernel`.**

---

## B5: Attack the T1 global upper bound  🔴  `[extend]`

**Goal.** Make the second wall two-sided. T1 currently has an exact *attainment* witness
(`W(T1) = (1163+38√3)/1265`) but no matching global upper bound.

**Do.** Construct an exact PSD certificate for `W(T1) − f_{T1} ≥ 0` over the relevant field
(`Q(i,√2,√3)` or its extension), by the X-space / transport route that worked for M1 or a new
one. Note: T0 and T1 walls live in *different* fields, so the M1 certificate does not transfer
directly.

**Done when.** An exact certificate establishes `max f_{T1} ≤ W(T1)`, closing the wall.
**Evidence target: `exact`.**

---

## B6: A closed form or obstruction for the d=10 wall  🔴  `[extend]`

**Goal.** Resolve the d=10 room. The wall is measured (defect ≈ 0.0225) but the closed-form
hunt (PSLQ at high precision) found nothing.

**Do.** Either find the exact algebraic value (and prove attainment), or give a structural
reason the d=10 wall has no small-degree closed form. The symmetry route (analogue of the
order-3 cycler at d=6) is one promising angle.

**Done when.** A closed form with an exact witness, or a labeled structural obstruction, is
posted. **Evidence target: `60-digit` → `exact`.**

---

## B7: Standalone note on the Weyl-board census  🟢  `[document]`

**Goal.** Make the Z₆² Weyl board readable on its own.

**Do.** Write a short note (a few pages) on Board B: the 12 full lines, the almost-disjoint cap
at 3, the 24 maximal triples, and the CRT factorization, with the combinatorics self-contained.
Cross-check against `mub6_iching_weyl_boards` output and the Lean `IChingBoardCap` lemma.

**Done when.** A standalone note (markdown or PDF) lands under the atlas. **Evidence target:
`exact` for any counted claims.**

---

## B8: Prior-work obstruction census  🟡  `[survey]`

**Goal.** Situate this work honestly in the MUB(6) literature.

**Do.** Anchor on the current authoritative survey, **McNulty and Weigert, "Mutually Unbiased
Bases in Composite Dimensions: A Review" (arXiv:2410.23997)**, then build out the lineage already
named in [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md) (Wootters-Fields, Zauner, Bengtsson et al.,
McNulty-Weigert, McConnell-Spencer-Tahir, Jaming et al., Raynal-Lu-Englert, Butterley-Hall,
Szollosi, Goyeneche, Tao's S6) into a properly dated, citation-complete census: each prior MUB(6)
result tagged by evidence level, with a line on how M1 and the product-ceiling law relate.

**State the boundary out loud.** McNulty-Weigert already proved analytically that no MU vector
extends the canonical product triple (`f` never reaches 1); the census must say plainly that the
*impossibility* is theirs and what is new is the *exact value* `W` plus a runnable certificate.
Do not let M1 read as if it discovered the obstruction.

**Done when.** A census note with full citations is posted; `ACKNOWLEDGMENTS.md` is updated with
anything it is missing. Corrections by experts welcome.

---

## B9: Extend the skeptical FAQ  🟢  `[audit] [good-first-brick]`

**Goal.** Strengthen the FAQ by adding the question *you* would ask.

**Do.** Pick the claim you trust least, try to break it, and write up the question and what you
actually found (whether it held or not). Add it to `FAQ.md`.

**Done when.** A new Q&A is merged, with the check you ran.

---

## B10: Parametric product triples between T0 and T1  🔴  `[extend]`

**Goal.** Understand how the wall moves. T0 and T1 are two points; the path between them is
unmapped.

**Do.** Parametrize a family of product triples interpolating T0 and T1; measure the wall along
it; ask whether `W(t)` varies continuously, in what field it lives, and where democracy breaks.

**Done when.** A labeled wall-vs-parameter study is posted (`float`/`60-digit` to start; exact
points are gold). **Evidence target: `60-digit` → `exact`.**

---

## B11: Exactify the d=24 aligned product room  🟡  `[extend]`

**Goal.** Push the `21/23` ceiling prediction from float to exact.

**Do.** The d=24 aligned 3×8 product room tests the ceiling-law prediction `21/23` numerically
(`mub6_d24_aligned_product_room`). Reproduce it in exact arithmetic and confirm (or refute) the
prediction.

**Done when.** An exact result confirms or breaks `21/23` in the aligned room. **Evidence
target: `float` → `exact`.**

---

## B12: Independent exact-symbolic reproduction in Wolfram  🟡  `[reproduce] [audit]`

**Goal.** Reproduce the wall in Wolfram Language, independently of the Python verifier and Lean.
This is the computational-exploration door; see [`WOLFRAM-LANDING.md`](WOLFRAM-LANDING.md).

**Do.** Start from the runnable starter [`wolfram/mub6_feasibility.wl`](wolfram/mub6_feasibility.wl)
(it rebuilds the triple, proves mutual unbiasedness exactly via `RootReduce`, defines `f`, and
checks `f(v*) = W`). Then take it further: an independent verifier port of one bundle certificate
step in `VerificationTest` / `TestReport` style, a closed exact-symbolic form of the witness `v*`
(the starter uses a numeric one), a `Manipulate` visualization of the wall, or a search over nearby
product triples.

**Done when.** A Wolfram notebook independently reproduces (and ideally visualizes) the obstruction,
posted to Wolfram Community or the Notebook Archive. An independent rerun by a non-author is real
evidence: it moves the relevant ledger node toward `independently_reproduced`. **Evidence target:
`exact` (symbolic) where possible; honest `float` otherwise.** This is reproduction, not formal
verification.
