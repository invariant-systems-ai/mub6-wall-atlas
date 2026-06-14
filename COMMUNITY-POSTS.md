# Community posts

Short, human-ready launch drafts. Edit names, links, and version pins before posting. Keep the
same restraint: one exact wall, not a solution to MUB(6); AI-assisted work is welcome, but claims
move only through checkable artifacts.

## Lean Zulip / Lean community

**Title:** MUB(6) Wall Atlas: a Lean formalization challenge around one exact wall

I am testing a research-game format for MUB(6): a wall atlas of small, independently checkable
bricks.

The narrow claim is not that MUB(6) is solved. It is one exact fourth-vector feasibility wall
after the canonical product triple in dimension six:

```text
max f = W = (88 + 3√6) / 100
```

The current artifact has an exact attainment witness and an exact PSD/Veronese certificate checked
by a standard-library-only verifier in the Zenodo bundle. The repo also includes a small Lean 4
layer for the finite combinatorial spine (`lake build Mub6Lemmas`, no mathlib) plus an axiom audit.

I would especially like feedback on the first formalization target: formalize the feasibility
identity `f(v) = 1` iff `v` is unbiased to the three fixed bases, then possibly the exact witness
overlap identities.

Is this better as a no-mathlib kernel-audit project, a small mathlib-dependent project, or
something else? Skeptical feedback is welcome; a broken or badly scoped brick is useful data.

## Wolfram Community

**Title:** MUB(6) Wall Atlas: exact-symbolic notebook challenge for reproducing a certified wall

I am preparing a Wolfram Language route into a small MUB(6) wall atlas. The goal is computational
reproducibility and visualization, not a formal proof claim.

The narrow claim is one exact fourth-vector feasibility wall after one canonical product triple in
dimension six:

```text
max f = W = (88 + 3 Sqrt[6]) / 100
```

The repo includes a Wolfram Language starter that rebuilds the triple, checks mutual unbiasedness
exactly, defines the feasibility functional, and verifies the published wall witness. The exact
upper-bound certificate is checked in the Zenodo bundle by a separate verifier; the Wolfram door is
for independent exact-symbolic reproduction, notebook explanation, visualization, and stress tests.

I would welcome advice on the cleanest Wolfram presentation: a computational essay, a
package/notebook pair, `VerificationTest` coverage for a certificate step, or interactive graphics
that make the wall legible.

## GitHub / GitLab release note

The first public MUB(6) Wall Atlas release is a community artifact, not a standalone proof paper.
It maps one narrow, exact obstruction after the canonical product triple:

```text
max f = W = (88 + 3√6) / 100
```

What is included:

- a ledger of mapped walls and open bricks;
- a five-minute local check of the atlas and puzzle layer;
- a pointer to the Zenodo verification bundle for the exact upper-bound check;
- a Lean 4 combinatorial layer with an axiom audit;
- a Wolfram Language exact-symbolic starter;
- seed issues for reproduction, independent checker ports, formalization, visualization, and survey work.

What is not claimed: this does not solve MUB(6), and it does not rediscover the product-triple
obstruction. The contribution is the exact value of this wall and a reproducible certificate path.

AI-assisted exploration is welcome, but evidence must land as a rerunnable artifact.

## Very short version

MUB(6) Wall Atlas maps one exact, checkable obstruction brick at a time. First wall:
`max f = (88 + 3√6)/100` after the canonical product triple. Not a solution to MUB(6); a public
invitation to reproduce, audit, formalize, visualize, or break scoped pieces of the map.
