# Skeptical FAQ

Written for the reader whose first instinct is "this can't be right" or "what is this person
actually claiming?" Those are the right instincts. Here are the honest answers.

### Did you solve MUB(6)?

No. The open question, whether a fourth mutually unbiased basis exists in dimension six, is
untouched. This certifies one exact obstruction *after one specific triple of bases*. The
scope is deliberately small.

### Then what is the actual claim?

Exactly one load-bearing theorem: after the canonical product triple `{Z₂⊗Z₃, X₂⊗Q₀, Y₂⊗Q₁}`,
the maximum of the fourth-vector feasibility functional `f` over the unit sphere is
`W = (88 + 3√6)/100`, attained, with a matching exact global upper bound. Everything else in
the bundle (T1, d=10/12/24, boards) is labeled companion material.

### Didn't McNulty and Weigert already prove no vector extends this triple?

Yes, and that is the honest framing, not a gotcha. McNulty and Weigert proved analytically, years
ago, that no mutually unbiased vector extends a triple of mutually unbiased *product* bases, i.e.
that `f` never reaches `1` here. The **existence/impossibility** content for this triple is theirs,
and we do not reopen it. What is new in this brick is the **exact extremal value**
`W = (88 + 3√6)/100` and a **machine-checkable two-sided certificate** for it: we compute and
certify the constant the obstruction stops at. If your reaction is "they closed this and you
computed the number," that is correct, and the exact value plus a runnable certificate is
precisely the contribution. See [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md).

### Why should I believe the upper bound rather than just the attainment?

Because you do not have to believe it; you can check it. `make verify-global` runs a
standard-library-only Python verifier that loads a stored exact PSD certificate `Q` and checks,
in exact arithmetic, that `ztilde(v)ᵀ Q ztilde(v) = G_hom(v)·|v|⁴` as a polynomial identity
(full symbolic expansion, not sampling) and that `Q` is PSD on the complement of its exact
kernel. If both hold, `max f ≤ W` follows. ~150 s on commodity hardware.

### The dimensions 441, 432, 370 appear in different places. Do they cohere?

Yes; they are three distinct objects. `Q` is the `441×441` exact Veronese (degree-4 `Sym⁴`)
certificate matrix. It has an exact `71`-dimensional kernel. The PSD check therefore runs on the
congruence block `S = WᵀQW` of dimension `441 − 71 = 370` (the verifier reports
`370/370 rows` strictly diagonally dominant). The `432` is unrelated to those sizes: it is the
order of the triple's symmetry group, over which the closure that produces `Q` is deterministic.

### Does the verifier rebuild the certificate, or just check a stored one?

It checks a stored one, and says so plainly. `Q` ships in the bundle; the verifier imports
nothing from the construction pipeline, reruns no group BFS or solver, and rebuilds the
canonical triple from first principles before checking. That is the strong answer to the
referee question: the trusted base is "this stored matrix has these exact properties," and the
properties are machine-checkable.

### The certificate has a 2095-digit denominator. Is that a red flag?

It is the honest size of the exact object. The certificate solves a linear system whose Bareiss
pivot determinant lands in the denominators; the big integer is that determinant, not
obfuscation. The artifact records the hash of the exactified solution it was assembled from,
which matches the value committed in the certificate run, so the stored `Q` is byte-bound to
the run that produced it.

### Couldn't this be a plausible-looking false positive, like so many MUB(6) attempts?

That risk is exactly why the atlas exists and why nothing is labeled above its true evidence
level. The load-bearing claim is `exact`/`kernel`, not numerical. The numerical results
(d=10, d=24) are labeled `float`/`60-digit` and are explicitly *not* proof. If you find a gap,
that is the most useful possible contribution; please open an issue.

### Why Lean for only part of it?

The combinatorial board layer is in the Lean kernel today (`{propext, Quot.sound}` axioms, no
mathlib, no `native_decide`). The analytic chain (the PSD certificate, the local interval
bound) is `exact` in Python but not yet in Lean. Carrying more of it into the kernel is an open
brick (B4) and a great contribution.

### Isn't this just Lean? Why the receipts at all?

No, and the receipts are not a replacement for Lean; they sit *around* it. **Lean proves; the
receipts record provenance.** Lean answers "does this theorem follow inside the kernel from these
definitions and axioms?", which is one of the strongest evidence engines there is. It does not, by
itself, certify the Python exact-arithmetic verifier, the stored certificate file, the SHA-256
manifest, the Zenodo deposit, the relation between the manuscript theorem and the artifact bundle,
whether a rerun was independent, or the honest status label of each claim. The atlas's AIIR
research-evidence layer binds all of that to each claim. If Lean is the court-certified witness,
the receipt is the case file: claim, non-claims, witness, exhibits, hashes, who has independently
checked it, current evidence status, and the next gate. A Lean proof is the strongest exhibit the
case file can hold; the case file is still useful. Here the board layer *is* a Lean exhibit
(`atlas_status: kernel_checked`); the analytic wall is an exact-arithmetic exhibit
(`self_verified_exact`), pending an independent rerun.

### What stops two people redoing the same work?

Nothing formal, by design. Claiming a brick is a comment, not a lock. For the verification
bricks, *independent duplication is the point*: two from-scratch checks of the same certificate
in different systems is stronger than one.

### Can the atlas points or the reproduction counts be gamed?

The intrinsic points come from a node's evidence level and status, which any reader can re-derive
from the artifact, so there is nothing to inflate there. The two counts that *could* be gamed,
`independent_reruns` and `independent_implementations`, are not free integers: each is **derived**
from a list of checkable evidence entries (who, when, and an artifact a stranger can open), and the
scorer rejects any count that does not equal the number of entries backing it. CI runs that check,
and a separate regression test (`ledger/test_score_atlas.py`) keeps the check itself from being
quietly weakened. So a number can never run ahead of the proof behind it, and no maintainer has to
police it by hand. Points are also non-financial and revocable the moment a claim breaks.

### Who is behind this and what do they get out of it?

It is published research (DOI on Zenodo) released so others can audit, extend, and own pieces.
The author's interest is a mapped wall, not credit for the whole problem. The framing is
deliberate: smaller claim, easier check, open ownership. If that posture ever slips in
practice, call it out in an issue.

### Is AI use allowed here?

Yes. AI-assisted search, explanation, code drafting, and notebook exploration are welcome;
[`qiskit_game/PLAY-WITH-AI.md`](qiskit_game/PLAY-WITH-AI.md) gives one no-install route. The rule
is not "no AI." The rule is "label the evidence." A model's argument is not a certificate, but
an artifact it helps produce can count if others can run or check it. If the AI interaction is part
of the route, include the prompt, transcript, or a short note so others can reproduce what you did.

### I think the whole framing is wrong / the functional is the wrong object / the triple is unnatural.

Good, write that up. A reasoned critique of the framing, with a concrete alternative, is a
document-class brick and goes in the atlas. The map improves by disagreement in the open.
