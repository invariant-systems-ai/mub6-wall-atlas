# Play with an AI (no install)

The wall room is a closed-form scalar function of a 6-vector, so you can play it by pasting it
into any capable model. No Python, no Qiskit, nothing to install. This is **rung 2** of the
ladder in `README.md`.

## Use AI as a scratchpad

This is **Mode B: search**. AI is useful here: it can hill-climb, explain the functional, write
small scripts, and help you find mistakes. The boundary is simply that search is not proof. An AI
run that climbs to `f ~ 0.953` has not certified `max f <= W`, and an AI-written argument is not a
verifier. The proof is the exact PSD certificate in the Zenodo bundle (`make verify-global`). If a
model helps produce a real artifact - a checker, formalization, notebook, or critique - bring that
as a brick (see `../CONTRIBUTING.md`) so others can inspect it.

## What the game is

For a unit vector `v` in C^6 and three fixed mutually unbiased bases (the canonical triple),

```
f(v) = 1 - ( sum over the 3 bases i, sum over the 6 outcomes j of (p_j^(i) - 1/6)^2 ) / (1 - 1/6)

where p_j^(i) = |<w_j^(i), v>|^2   (the outcome distribution of v in basis i)
```

`f = 1` exactly iff `v` is unbiased to all three bases (a fourth MUB vector). The wall says you
cannot reach it:

```
max_v f(v) = W = (88 + 3*sqrt(6)) / 100 ~ 0.95348469
```

The three bases (columns = basis vectors) are in [`data/canonical_triple.json`](data/canonical_triple.json)
as `[real, imag]` pairs, along with the attainment witness `v*` (which sits exactly at `W`). You
can also rebuild them from scratch: basis 0 is the standard basis of `C^6 = C^2 (x) C^3`; basis 1
is `H2 (x) F3` (qubit Hadamard times the qutrit Fourier basis); basis 2 is `Y2 (x) Q3`, where
`Y2` is the qubit Pauli-Y eigenbasis and `Q3` is the Gauss-sum qutrit basis with entries
`omega^(j^2 + m j)/sqrt(3)`, `omega = e^(2*pi*i/3)`.

## Copy-paste prompt

> I want to play a math puzzle about mutually unbiased bases in dimension 6.
>
> Define `f(v) = 1 - ( sum_{i=1..3} sum_{j=1..6} (p_j^(i) - 1/6)^2 ) / (1 - 1/6)` for a unit
> vector v in C^6, where `p_j^(i) = |<w_j^(i), v>|^2` and the three orthonormal bases `{w^(i)}`
> are a canonical mutually unbiased triple of `C^6 = C^2 (x) C^3`: basis 0 = standard basis;
> basis 1 = Hadamard(2) tensor Fourier(3); basis 2 = PauliY(2)-eigenbasis tensor the qutrit
> Gauss-sum basis with entries `omega^(j^2 + m j)/sqrt(3)`, `omega = exp(2*pi*i/3)`.
>
> 1. Build the three 6x6 bases and verify they are orthonormal and pairwise mutually unbiased
>    (every cross overlap squared = 1/6).
> 2. Numerically maximize `f(v)` over unit vectors v (hill-climb from random starts).
> 3. Report the best `f` you reach, and compare it to `W = (88 + 3*sqrt(6))/100`.
> 4. Explain, intuitively, why `f = 1` is unreachable for this triple.
> 5. Then attack brick B9: pick the claim here you trust least and try to stress-test it.
>
> Important: a numerical maximum is NOT a proof. Do not claim you have proved the bound. If you
> think you have a real certificate, say so explicitly and share the artifact so others can check it.

Expected: the model lands a bit below `0.95348` and cannot pass it. That is the wall. To
actually decide the bound, go to rung 6 (the Zenodo bundle).

**Tripwire (so you can catch the model, not just trust it):** if a model reports `f` above
about `0.9535`, its code has a bug, almost always a wrong normalization or the wrong bases. The
wall `W = (88 + 3*sqrt(6))/100` is a theorem, not a soft ceiling; nothing can exceed it. A
result *above* the wall is a refuted run, not a discovery.
