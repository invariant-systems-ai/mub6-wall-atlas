# The MUB(6) Wall Atlas

**A community project to map the feasibility walls of mutually unbiased bases in dimension six, one independently checkable brick at a time.**

---

This starts from one verified subproblem and an open invitation: help build a public
*defect atlas* for MUB(6), where many people can contribute independent bricks and own pieces
of the map.

The first brick is already on the table. After the canonical product triple
`{Z₂⊗Z₃, X₂⊗Q₀, Y₂⊗Q₁}`, the maximum fourth-vector feasibility value is exactly

> **max f = W = (88 + 3√6) / 100**

proved on both sides: attainment by an explicit algebraic witness, and the matching global
upper bound by an exact PSD/Veronese certificate (degree-4 Sym^4) with deterministic closure
over the triple's 432-element symmetry group, with no floating-point step in the proof path. It
is published on Zenodo under the concept DOI
[10.5281/zenodo.20670933](https://doi.org/10.5281/zenodo.20670933) (which always resolves to the
latest version), and it ships with a standard-library-only verifier you can run yourself.

**This does not solve MUB(6).** The 40-year open question is whether a fourth mutually unbiased
basis exists in dimension six at all. This brick certifies one exact obstruction *after one
specific triple*. That smaller, checkable scope is the whole point.

**And it does not discover the board.** The MUB(6) problem, Zauner's bound, the product-MUB
constructions, and the entanglement obstruction this work leans on are decades of prior work
(Wootters and Fields; Zauner; Bengtsson et al.; **McNulty and Weigert**; Jaming et al.; and
others). The contribution here is the *exactness and checkability of particular walls*, not their
existence or the machinery that frames them. See [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md).

## First time here

Start with [`START-HERE.md`](START-HERE.md) if you want the one-page route map. It points
researchers, Lean formalizers, Wolfram users, Qiskit players, and first-time contributors to the
right door without asking anyone to read the whole archive first. Prepared community launch drafts
live in [`COMMUNITY-POSTS.md`](COMMUNITY-POSTS.md).

AI-assisted exploration is welcome here. Use AI for search, explanation, drafting, code review, or
translation between systems; just keep the evidence boundary clear. Claims move only by rerunnable
artifacts: verifier transcripts, exact scripts, Lean theorems, independent ports, notebooks, or
clear written critiques.

## For researchers (verification path)

If you are here to evaluate the mathematics rather than to play: the result is the two-sided
exact theorem `max f = W = (88 + 3*sqrt(6))/100` for the canonical triple (an explicit
attainment witness plus a matching exact PSD/Veronese certificate, degree-4 Sym^4, with
deterministic closure over the triple's 432-element symmetry group). The honest non-claims live
in [`FAQ.md`](FAQ.md). The load-bearing claim and its evidence level are node `W.canonical-triple`
in [`ledger/nodes.json`](ledger/nodes.json). Cite the work by its concept DOI
`10.5281/zenodo.20670933` (always the latest version); for exact reproducibility the ledger pins
the v1.1 version DOI `10.5281/zenodo.20682233`. The certificate's identity is
`sha256:c6badfeb...9f0b7`, which is the hash of the **decompressed** certificate: the bundle's
`SHA256SUMS` pins the compressed file `evidence/global-wall-certificate-Q-exact.json.gz` at
`116f8e63...`, and `gunzip -c global-wall-certificate-Q-exact.json.gz | sha256sum` reproduces
`c6badfeb...` (so the pin is recomputable by anyone, not asserted). To verify the theorem itself,
fetch that version and run `make verify-global` (step 3 below). If you work in Lean, start at
[`LEAN-LANDING.md`](LEAN-LANDING.md): the combinatorial spine is kernel-checked in `lean/`
(`lake build Mub6Lemmas`, no mathlib), with scoped first formalization bricks. The `qiskit_game/`
puzzle lab is a separate on-ramp for newcomers; you can ignore it entirely.

## Why an atlas, and why now

MUB(6) has stayed hard partly because it is *too easy to generate plausible-looking false
positives*: a promising numerical search, a near-miss construction, a symmetry that almost
closes. A better path may be to break the problem into small, independently checkable pieces
that many people can audit or extend, with the evidence level of each piece labeled honestly.

That is what this atlas is: exact pinned-triple walls, failed extensions (negative results
matter), verifier bundles, formalized lemmas, SOS and certificate attempts, Weyl-board
structure, and carefully labeled numerical evidence. Every contribution can be local. No one
has to buy the whole story. Experts can contribute corrections without endorsing everything;
newcomers can help by running an artifact and reporting what happened.

The goal is not for one person to own the problem. **The goal is to make the wall mappable.**

## Start in five minutes

This repository is the **atlas plus the puzzle lab**: the wall map, the ledger, the coordination
docs, and a runnable game. The **exact proof** (the verifier, the PSD certificate, the 33
research modules) lives in the **verification bundle** on Zenodo, not here, by design. Here is
exactly what you can check, and where.

**1. See the map (this repo, no dependencies):**

```sh
python3 ledger/score_atlas.py      # validates the ledger, prints atlas points + open frontiers
```

**2. Feel the wall numerically (this repo, needs `numpy`):** Mode B, runs from what you hold.

```sh
pip install numpy
python3 qiskit_game/src/mub6_game/feasibility.py   # self-test: the witness sits at the wall, |f(v*) - W| = 0
python3 qiskit_game/play.py                         # climb toward the wall and stall just below it
```

**3. Decide the theorem exactly (the Zenodo bundle, Mode A):** the exact certificate is **not in
this repo**; you must fetch it.

```sh
# download and unpack the verification bundle from DOI 10.5281/zenodo.20682233, then:
cd <unpacked-bundle>
sha256sum -c SHA256SUMS            # every file matches its manifest hash
make verify-global                 # independent stdlib-only checker of max f <= W  (~150 s)
python3 python/mub6_d6_wall_attainment_exact.py   # the matching lower bound: f(v*) = W exactly
```

> **The split is deliberate.** Steps 1 and 2 are checkable from this archive, in float (Mode B):
> you can confirm the witness sits at the wall and watch a search stall just below it. Step 3,
> the exact proof, requires the bundle (Mode A). Numerical agreement is not a certificate; the
> bundle is where the theorem is decided. If any step fails on your platform, **that is a useful
> result**: open an issue (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).

## What's here

| file | what it is |
|---|---|
| [`START-HERE.md`](START-HERE.md) | The one-page route map: theorem check, Lean, Wolfram, Qiskit, contribution, and posting doors. |
| [`COMMUNITY-POSTS.md`](COMMUNITY-POSTS.md) | Prepared launch drafts for Lean, Wolfram, GitHub/GitLab, and short-form posts. |
| [`INTENT.md`](INTENT.md) | The statement of intent, in one paragraph. Quote it anywhere. |
| [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md) | The prior work this stands on, and what is actually new here vs not. |
| [`LEAN-LANDING.md`](LEAN-LANDING.md) | The Lean front door: build `lean/`, the theorem inventory, and the first formalization bricks. |
| [`lean/`](lean/) | The kernel-checked Lean 4 layer (`lake build Mub6Lemmas`, no mathlib); 4 modules, axiom-audited. |
| [`WOLFRAM-LANDING.md`](WOLFRAM-LANDING.md) | The exact-symbolic door: a runnable Wolfram starter that reproduces the wall (`wolfram/`). |
| [`wolfram/`](wolfram/) | A Wolfram Language starter: rebuilds the triple, proves mutual unbiasedness exactly, checks `f(v*) = W`. |
| [`ATLAS.md`](ATLAS.md) | The wall map: what is mapped (with evidence level), and what is open. |
| [`POINTS.md`](POINTS.md) | Atlas points and badges: verified progress as a nonfinancial, revocable score. |
| [`ledger/`](ledger/) | The machine-readable ledger (`nodes.json` + schema), the stdlib scorer, and the receipt emitter. |
| [`.aiir/`](.aiir/) | AIIR research-evidence receipts: a content-addressed, tamper-evident binding of every claim to its artifacts. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to claim a brick, the evidence-level rules, how to submit. |
| [`DCO.md`](DCO.md) | Developer Certificate of Origin: how contributions are signed and licensed. |
| [`FAQ.md`](FAQ.md) | A skeptical FAQ. Read this if your first instinct is "this can't be right." |
| [`SEED_ISSUES.md`](SEED_ISSUES.md) | Ready-to-open issues: the first bricks anyone can pick up. |
| [`bricks/`](bricks/) | A worked example brick to copy (a B1 reproduction template). |
| [`CHANGELOG.md`](CHANGELOG.md) | Releases, and the bundle deposit each one targets. |
| `.github/ISSUE_TEMPLATE/` | Issue templates for contributing a brick or proposing a new wall. |
| [`qiskit_game/`](qiskit_game/) | The puzzle lab: a Qiskit-powered teaching game that lets people *feel* the wall (search), then routes them to the proof (verify). |

The artifact bundle it wraps (verifier, 33 research modules, Lean project, evidence JSONs) is
the published companion to the paper; see its `README.md` for the full module inventory and
the independent-verification section.

## Provenance: the ledger carries its own receipts

The atlas runs Invariant's own evidence-receipt tool on itself. `ledger/emit_receipts.py`
projects every ledger node into an [`aiir/research_evidence_receipt.v0.1`](ledger/research_evidence_receipt.v0.1.schema.json)
record (content-addressed, tamper-evident, Apache-2.0 open format) written to
[`.aiir/research-evidence.jsonl`](.aiir/research-evidence.jsonl). Each receipt binds a claim to
its artifacts by **sha256 digest** (resolved from the bundle's `SHA256SUMS`, vendored at
`ledger/bundle.SHA256SUMS`), names its verifier, and records an honest `status`: a self-verified
exact result is `proof_sketch`, **not** `verified`. Nothing reaches `verified` until a node has
an independent rerun. CI regenerates the receipts and fails if they drift from the ledger or if
any content hash does not match (`python3 ledger/emit_receipts.py --check`).

To be clear about what that label means, because it is easy to misread: `proof_sketch` is AIIR's
coarse research-evidence enum value, and in this atlas it means *author-supplied exact
certificate, not yet independently rerun*. It does **not** mean the proof path is informal or the
theorem is downgraded. The certificate is exact and the bundle verifies it deterministically
(`make verify-global`); the label records only that the atlas has not yet received an *external*
reproduction. Because that one enum value is ambiguous to mathematicians, each receipt also
carries a finer label in `extensions.atlas_status`: `self_verified_exact`, `kernel_checked` (the
Lean board layer), `computational_evidence`, `hypothesis` (open), or `independently_reproduced`.
A node's AIIR `claim.status` reaches `verified` (and `atlas_status` reaches
`independently_reproduced`) the moment someone other than the author reruns it.

## The method

The pattern this repository runs on is general: a smaller claim, an easier check, open
ownership. Map a hard problem as a surface of small, independently checkable bricks rather than
one monolith. Here it is pointed entirely at MUB(6); the method is the only thing that travels.

## License

Code is licensed under the **Apache License 2.0** ([`LICENSE-CODE`](LICENSE-CODE)); documents
under **CC BY 4.0** ([`LICENSE-DOCS.md`](LICENSE-DOCS.md)). See [`LICENSE`](LICENSE) for the
summary and [`DCO.md`](DCO.md) for how contributions are signed. Evidence JSONs are program
output and carry no separate license. You keep authorship of your bricks. To cite the atlas,
see [`CITATION.cff`](CITATION.cff).
