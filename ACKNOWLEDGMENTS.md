# Acknowledgments: the board was always there

> Read this before the points, badges, or game layer. The four-decade board comes first because it
> is what everything here stands on.

This atlas does not discover the MUB(6) problem, its structure, or the constructions it maps. It
adds **exact, machine-checkable bricks to a board built over four decades** by many people. The
contribution tracked here is narrow on purpose: making *specific* walls exact and certifiable,
with a public verifier, and coordinating others to check and extend them. The mathematics those
walls live in is prior art, and the credit for it belongs to the people below.

## Why the separation matters

The whole project runs on one rule: **never label up.** A float result stays float until someone
makes it exact; a self-verified node stays `proof_sketch` until an independent rerun. The same rule
applies socially: a reproduction transcript or atlas-points total should not be placed on the same
footing as Zauner's conjecture or McNulty-Weigert's obstruction. The board is prior work; the game
and ledger are a way to coordinate new checkable bricks. Keeping those roles separate is not just
courtesy; it is part of the evidence discipline that makes this atlas useful. The honesty that
protects those researchers is the honesty that protects this atlas's own bricks.

## Standing on prior work

The precise, dated bibliography is the job of brick **B8** (the prior-work census); it should be
built carefully and is not yet complete. Anchor it on the current authoritative survey:

- **D. McNulty and S. Weigert, "Mutually Unbiased Bases in Composite Dimensions: A Review"**
  (arXiv:2410.23997; published as Quantum 10, 2051, 2026). The natural backbone for the whole
  census; start B8 here.

The lineage this work most directly depends on:

- **W. K. Wootters and B. D. Fields** introduced the Gauss-sum / Fourier construction of mutually
  unbiased bases in prime-power dimension. The `d = 3` MUBs this atlas and its game use *are* that
  construction; the whole product triple is assembled from it.
- **G. Zauner** conjectured that dimension six admits at most three MUBs (between three and seven
  are known to exist). The entire question this atlas chips at is his.
- **I. Bengtsson, W. Bruzda, A. Ericsson, J.-A. Larsson, W. Tadej, and K. Zyczkowski** carried out
  the major study of MUBs and complex Hadamard matrices in dimension six.
- **D. McNulty and S. Weigert** are the most direct upstream of this atlas's product-triple
  results: "The Limited Role of Mutually Unbiased Product Bases in Dimension Six" (a full set of
  seven MUBs, if it exists, has at most one product basis), "All Mutually Unbiased Product Bases in
  Dimension Six" (every product-state MUB; pairs and two triples, no quadruple), and the analytic
  proof that **no MU vector extends a triple of mutually unbiased product bases**. In any honest
  accounting of this corner of the field, their contribution dwarfs any single exact wall here.
- **G. McConnell, H. Spencer, and A. Tahir, "Evidence for and against Zauner's MUB conjecture in
  C^6"** (Quantum Inf. Comput. 21, 721, 2021). Explores algebraic d=6 solutions via their
  *shadows* over finite fields. This is the same idea the atlas's own Galois-shadow module
  (`mub6_d6_w_prime_galois_shadow`) echoes, so it is a direct intellectual neighbor.
- **P. Jaming, M. Matolcsi, P. Mora, F. Szollosi, and M. Weiner** on MUB-triplets in dimension six.
- **P. Raynal, X. Lu, B.-G. Englert**, "Mutually unbiased bases in six dimensions: the four most
  distant bases" (2011), the neighborhood the numerical optima sit in.
- **P. Butterley and W. Hall** (2007), early numerical evidence on the maximum MUB count in d=6,
  part of the honest float-not-proof history; with **G. Brierley and S. Weigert**'s searches.
- The complex-Hadamard reduction: Bengtsson et al. above, **F. Szollosi** (the four-parameter
  family of order-six Hadamards), **D. Goyeneche** (MUB triplets from non-affine Hadamards), and
  **Tao's matrix `S_6`** (a pair admitting no third MU basis).

If your name or result belongs here and is missing, that is a bug; open an issue or a B8
contribution and it will be added with a proper citation.

## What is new here, and what is not

| not new (the board) | new (the bricks) |
|---|---|
| the MUB(6) problem and Zauner's bound | the *exact* value `W = (88 + 3 sqrt6)/100` for the canonical triple |
| **the impossibility itself**: McNulty-Weigert proved analytically that no MU vector extends the canonical product triple, i.e. `f` never reaches `1` | a *two-sided, machine-checkable certificate* for the exact extremal value of `f` |
| product-MUB constructions and their limits | the second exact wall `W(T1)`, the d12/d24 defect identity, the SOS non-existence |
| the symmetry / Heisenberg-Weyl structure | the kernel-checked board layer and the coordination atlas around it |

**Say the sharpest dismissal out loud before a referee does:** McNulty-Weigert closed the
*existence* question for this triple years ago. This atlas does not reopen it. What is new is the
**exact value** `W` and a **runnable two-sided certificate** for it. We compute and certify the
constant; we do not claim the obstruction's discovery. (This is also answered in `FAQ.md`.)

## Three classes, and how a brick graduates

To keep "two classes" from hardening into a binary that cannot grow:

1. **The board.** Foundational, published prior work (everything above). Not scored, not entered by
   anyone; it is the ground the scoring stands on.
2. **A brick.** A scoped contribution to *this* atlas (a reproduction, a witness, a note). It earns
   atlas points and a ledger entry. Running `play.py` or the verifier puts you in the ledger; it
   does **not** put you on the board. You cannot reach the board by accumulating points.
3. **Graduation.** A brick that turns out to be genuinely significant, a new exact wall, a real
   independent verification, a kernel proof of a named lemma, becomes board-class **the same way
   every existing board entry did**: by being real, published, independently-checkable mathematics
   that future work cites. It is earned by the work, not accumulated in points.

## A note on atlas points

Atlas points (`POINTS.md`) measure contributions *to this atlas's bricks*. They are **not** a
leaderboard of MUB(6) research, and it would be misleading to read them as one. The foundational
work above is the ground the scoring stands on, not an entry in it.
