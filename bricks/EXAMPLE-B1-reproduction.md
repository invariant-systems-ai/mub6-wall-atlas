# EXAMPLE brick: B1 reproduction (a worked template)

**This is a worked example so the first real contributor can imitate rather than invent.** It is
the *maintainer's own* run, provided as a template. It does **not** count as an independent
verification and does **not** change `independent_reruns` in the ledger: B1 is closed only by a
rerun from a **different party**. Copy this shape for your own submission.

---

- **Brick:** B1 (run the verifier on your platform)
- **Kind:** reproduce
- **Targets node:** `C.global-wall` (bundle DOI `10.5281/zenodo.20682233`)
- **Claim:** `make verify-global` from the Zenodo bundle confirms `max f <= W` on this platform.
- **Evidence level:** n/a (reproduction). The *node's* level stays `exact`.

## Environment

- OS: Linux x86_64
- Python: CPython 3.11
- Bundle: unpacked from Zenodo DOI `10.5281/zenodo.20682233`, `sha256sum -c SHA256SUMS` clean
- Certificate identity `sha256:c6badfeb...9f0b7` reproduced by
  `gunzip -c evidence/global-wall-certificate-Q-exact.json.gz | sha256sum` (this is the hash of
  the *decompressed* certificate; `SHA256SUMS` pins the compressed `.gz` at `116f8e63...`). Matches
  the value recorded on node `C.global-wall`.

## Transcript (tail)

Verbatim captured stdout from the run (the runtime, the row index, the bit-lengths, and the prime
are copied from the program output, not reconstructed):

```text
[C2] PASS S = W^T Q W symmetric, positive diagonal, STRICTLY diagonally dominant (370/370 rows) (74s)
          worst margin at row 23: exact F4 element with component bit-lengths [7027, 7027, 7025, 7024];
          certified rational lower bound margin/diag >= 9.999986e-01
[C3] PASS det[W | K] != 0 (nonzero residue mod p = 67108439; certifies invertibility over R) (2s)

== VERDICT: ALL CHECKS PASS ==
   ... max_{|v|=1} f(v) <= W = (88+3 sqrt6)/100.
   total runtime 151s
```

(Checks [A] well-formedness and [B] the full symbolic identity also passed; the verdict line
`ALL CHECKS PASS` covers A, B, and C.)

## Result

`make verify-global` returned exit 0 with `ALL CHECKS PASS` in 151 s. The upper bound holds on
this platform.

## What would make this an *independent* B1

Someone who is not the maintainer runs the same steps on their own machine, from their own
download of the bundle, and posts their transcript. At that point node `C.global-wall` moves
from `self-verified` to `verified` and earns the 5-point independent-rerun award. **That run is
the one the project actually needs.** See [`../SEED_ISSUES.md`](../SEED_ISSUES.md) (B1) and
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).
