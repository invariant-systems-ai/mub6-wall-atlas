# MUB(6) Wall Atlas: an exact-symbolic Wolfram challenge

The computational-exploration door, parallel to the Lean one. Where Lean is for theorem-level
trust ([`LEAN-LANDING.md`](LEAN-LANDING.md)), Wolfram is for **independent exact-symbolic
reproduction, visualization, and stress-testing**. The promise here is honest about its register:
*reproduce and inspect the obstruction exactly*, **not** "a machine-checked theorem." That is
Lean's job and the bundle's; this broadens the project from formal-proof audit to **computational
reproducibility audit**.

The narrow claim is the same and stays small: one exact feasibility wall after one canonical
product triple in dimension six, `max f = W = (88 + 3 Sqrt[6])/100`, not a solution to MUB(6).

## Run it now

A runnable starter is in [`wolfram/mub6_feasibility.wl`](wolfram/mub6_feasibility.wl):

```sh
wolframscript -file wolfram/mub6_feasibility.wl     # or paste the cells into a notebook
```

It rebuilds the canonical triple `{Z2(x)Z3, X2(x)F3, Y2(x)Q3}` from first principles and runs four
`VerificationTest`s, all `Success` on a stock kernel:

- **each basis orthonormal** (exact, via `RootReduce` over the cyclotomic field);
- **the triple is mutually unbiased** (exact: every cross overlap squared is `1/6`);
- **the witness attains the wall**, `f(v*) = W` to machine precision;
- **a basis vector is maximally biased**, `f = 0`.

So a Wolfram user can independently confirm, in exact-symbolic arithmetic, that the triple really is
a MUB triple and that the feasibility functional behaves as claimed, without trusting anyone's
Python.

## First bricks (pick one)

These are the contribution targets; see also the general brick list in `SEED_ISSUES.md` (B12).

1. **Computational essay.** A notebook that explains the obstruction visually and computationally:
   define the triple, define `f`, show the wall, let the reader run exact checks and change inputs.
2. **Independent verifier port.** A clean Wolfram Language check of one certificate step from the
   bundle, exact algebraic/rational data where possible, in `VerificationTest` / `TestReport` style.
   An independent rerun here is real evidence (it moves a ledger node toward independent verification).
3. **Exact witness.** Derive `v*` in closed exact-symbolic form so the witness test becomes exact
   rather than numeric. The starter uses a numeric `v*`; the exact form is an open target.
4. **Visualization layer.** `Manipulate`, graph/heatmap displays of the overlap profile, the
   product-vs-entangled structure, the wall as a function of a parameter. Make the atlas legible.
5. **Search sandbox.** Vary the triple, test nearby product triples, find failure modes.

## How to engage

- **Wolfram Community** (`community.wolfram.com`) for the broad post: title it as reproduction, not a
  proof claim ("exact-symbolic notebook challenge for reproducing a certified obstruction"). The
  Mathematics / Physics / Mathematica groups are the right rooms.
- **Mathematica Stack Exchange** only for targeted implementation questions (idiomatic
  `VerificationTest` structure, efficient cyclotomic/exact representation), not a project
  announcement.
- **The Notebook Archive** is a strong long-term home for a polished computational essay once it has
  had community feedback.

Do not pitch this as formal verification. Wolfram Language is excellent for exact/symbolic and
arbitrary-precision cross-checks; it is not a proof-assistant community in Lean's sense. The
honest promise is **independent exact-symbolic reproduction**.

## Prior work, first

This stands on decades of others' work (Wootters and Fields; Zauner; Bengtsson et al.; McNulty and
Weigert; and more); McNulty and Weigert already proved the existence obstruction analytically, and
what is new is the exact value and a checkable certificate. See
[`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md).
