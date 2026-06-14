# Start here

This is the short front door for the MUB(6) Wall Atlas.

The atlas is a community project for mapping small, checkable obstruction results around the
mutually unbiased bases problem in dimension six. The first mapped wall is deliberately narrow:
after one canonical product triple, the fourth-vector feasibility maximum is exactly

> **max f = W = (88 + 3√6) / 100**.

That does **not** solve MUB(6). It gives one exact, reproducible brick: an explicit attainment
witness plus a matching exact certificate for the upper bound. The invitation is to inspect it,
rerun it, formalize pieces of it, port a checker, visualize it, or find a flaw.

## Pick your door

| door | start here | what you can do |
|---|---|---|
| **Evaluate the theorem** | [`README.md`](README.md), [`FAQ.md`](FAQ.md) | Check the precise claim, non-claims, DOI pins, and verifier path. |
| **Run the atlas locally** | [`README.md#start-in-five-minutes`](README.md#start-in-five-minutes) | Validate the ledger, run the numerical wall room, then fetch the exact bundle. |
| **Contribute a brick** | [`SEED_ISSUES.md`](SEED_ISSUES.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) | Pick a small reproduction, audit, formalization, visualization, or survey task. |
| **Use Lean** | [`LEAN-LANDING.md`](LEAN-LANDING.md), [`lean/`](lean/) | Build the kernel-checked combinatorial layer and choose a scoped formalization target. |
| **Use Wolfram** | [`WOLFRAM-LANDING.md`](WOLFRAM-LANDING.md), [`wolfram/`](wolfram/) | Reproduce and visualize the wall in exact-symbolic Wolfram Language. |
| **Play with the wall** | [`qiskit_game/`](qiskit_game/) | Search numerically, use AI as a scratchpad, or run the Qiskit puzzle lab. |
| **Post it somewhere** | [`COMMUNITY-POSTS.md`](COMMUNITY-POSTS.md) | Use the prepared Lean, Wolfram, GitHub, and short-form launch drafts. |

## What is already checked here

From this repository, without the large Zenodo bundle, you can check the atlas ledger and run the
float64 puzzle layer:

```sh
python3 ledger/score_atlas.py
python3 ledger/emit_receipts.py --check
pip install numpy
python3 qiskit_game/src/mub6_game/feasibility.py
python3 qiskit_game/play.py
```

The exact upper-bound theorem is checked in the Zenodo verification bundle, not in this archive:

```sh
# after downloading and unpacking DOI 10.5281/zenodo.20682233
sha256sum -c SHA256SUMS
make verify-global
python3 python/mub6_d6_wall_attainment_exact.py
```

## AI is allowed; evidence still has to land

AI-assisted exploration is welcome. Use it for search, explanation, drafting, code review,
translation between systems, and sanity checks. Please say when AI materially helped. But do not
ask anyone to trust an AI transcript as evidence. A claim enters the atlas only when it leaves a
rerunnable artifact: a verifier transcript, exact script, Lean theorem, independent port, notebook,
or a clear written critique.

## The tone of the project

Bring skepticism. The atlas is meant to make disagreement easier, not harder: smaller claims,
public evidence, clear status labels, and room for independent reruns. A failed brick, a broken
script, or a better framing is useful progress.
