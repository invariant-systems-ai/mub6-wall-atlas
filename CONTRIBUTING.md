# Contributing a brick

The atlas grows by bricks: small, independently checkable contributions. You do not need to
endorse the whole program, agree with the framing, or trust the author. You need to do one
local, checkable thing and label its evidence level honestly.

## The four kinds of brick

1. **Reproduce**: run an existing artifact on your platform and report the result (including
   failures). The easiest way to help, and genuinely valuable: a verifier that only runs on the
   author's machine is not a verifier.
2. **Audit**: independently re-check a claim by a different route: parse the certificate from
   scratch, re-implement a checker in another system, find a hidden assumption.
3. **Extend**: map a new wall, attack an open bound, push a numerical result to exact.
4. **Document / survey**: write a standalone note, a skeptical FAQ entry, or a prior-work census.

## Evidence levels (label every claim)

| level | meaning | counts as |
|---|---|---|
| `exact` | end-to-end rational / cyclotomic-field arithmetic, no floats in the claim path | proof |
| `kernel` | Lean 4 theorem, axiom footprint at most `{propext, Quot.sound}` | proof |
| `60-digit` | high-precision numerics (e.g. mpmath ≥ 60 sig. digits) | strong evidence, not proof |
| `float` | float64 numerics, reproducible experiment | evidence, not proof |

**The cardinal rule: never label up.** A float experiment that looks like a closed form is
`float` until someone makes it `exact`. Most past MUB(6) confusion came from treating strong
numerical evidence as if it were proof. Here it never is, and that is a feature.

## AI-assisted work

AI-assisted work is welcome. Use AI as a scratchpad for search, explanation, drafting, debugging,
translation between systems, and sanity checks. Please mention material AI assistance in the brick
note or PR description, the same way you would mention a solver, notebook, or code generator. The
evidence bar does not change: an AI transcript is not proof, and it is not a rerun. A contribution
counts when it leaves a checkable artifact that another person can inspect or execute.

## How to claim and submit

1. **Claim it.** Comment on the brick's issue ("taking B5") so two people do not duplicate.
   No permission needed; claiming just signals intent. If you go quiet for a couple of weeks
   it reverts to open.
2. **Do the work.** Keep it reproducible: pin your tool versions, commit the script, write the
   evidence to a file like the existing modules do.
3. **Submit** one of:
   - a **pull / merge request** adding your artifact under a clearly named path plus a
     one-paragraph result note, or
   - a **link** to your own repo (Sage/Julia/Lean/Magma reimplementations are great as separate
     repos), with a short PR that adds the link and the headline result to `ATLAS.md`.
4. **Get checked.** A brick lands in the map once at least one other contributor independently
   confirms it (for `exact`/`kernel`) or reproduces it (for `float`/`60-digit`).

### Claiming a rerun or reimplementation (how the counters move)

The two reproduction counters on a node, `independent_reruns` and `independent_implementations`,
are not numbers you edit by hand. Each is **derived** from an evidence list, so to claim one you
add an entry, not a digit. In the node's record add (or append to) a `reruns` or
`implementations` array with one object per independent check:

```json
"reruns": [
  { "by": "your name or handle",
    "date": "2026-07-01",
    "evidence": "https://... or a path/commit a stranger can open and run",
    "sha256": "optional content hash of the evidence",
    "note": "optional one line on what you ran and what you got" }
]
```

`independent_reruns` must then equal the number of entries (here, `1`). The scorer, and therefore
CI, **rejects any count that does not match its evidence**, so a number can never run ahead of the
proof behind it. You raise the count by filing the receipt, never the other way round. Nothing
here needs a maintainer to reconcile, which is the point: the ledger polices itself.

When your PR touches the ledger, a bot posts a short summary of what it changes (points,
reproduction counts, statuses) and pre-flags anything CI will reject, so you get the feedback
before a human looks. A monthly job also re-runs every verifier on fresh dependencies, so a brick
that quietly stops reproducing is caught even in a slow month.

## A worked example

If you have never submitted a brick, copy the shape of the worked example in
[`bricks/EXAMPLE-B1-reproduction.md`](bricks/EXAMPLE-B1-reproduction.md): it shows the fields, an
environment block, a transcript, and the honest line on what would make it count as an
*independent* result.

## What makes a good brick

- It states exactly what it claims and what it does **not** claim.
- It is checkable without trusting you: someone can rerun or re-derive it.
- It labels its evidence level honestly, including "this failed."
- It is scoped small enough that one person can finish it.

## What we do not need

- Claims that MUB(6) is solved (or that it is impossible) without an exact or kernel-level
  certificate. Bring the certificate and it is the most important brick in the atlas.
- Numerical near-misses presented as results. Label them `float`, say what is suggestive, and
  invite someone to exactify.

## Provenance and licensing

Contributions are accepted under the **Developer Certificate of Origin 1.1** (see
[`DCO.md`](DCO.md)): sign each commit with `git commit -s`. Inbound license is the project
license, Apache-2.0 for code and CC BY 4.0 for documents, unless you state otherwise. You keep
authorship of your bricks; the DCO just keeps every brick's provenance clean so anyone can
reuse the atlas without ambiguity.

## Scope of this project

This atlas is **pure mathematics**: the feasibility walls of mutually unbiased bases in
dimension six. That is its whole subject. Contributions should stay in that lane, exact walls,
witnesses, certificates, formalizations, surveys, and reproductions. It is not an applied
engineering project and bricks should not be framed as one.

## Code of conduct, briefly

Skepticism is welcome and wanted; contempt is not. Critique bricks, not people. A found break
in someone's brick (including the author's) is a success for the atlas: it tells everyone where
to look next. Disagree in the open, with the artifact in hand.
