# Changelog

All notable changes to the MUB(6) Wall Atlas. The atlas and the Zenodo verification bundle are
two artifacts that must stay in lockstep; each release records the bundle deposit it targets.

## 0.1.0 (2026-06-13)

Initial public release.

- **Deposit citations (cite both).** The work is cited by its **concept DOI**
  `10.5281/zenodo.20670933`, which always resolves to the latest version, so future deposit
  versions need no docs edit here. This revision was **verified against version v1.1**, DOI
  `10.5281/zenodo.20682233`, certificate `sha256 c6badfeb...9f0b7`; that exact pin lives on the
  ledger nodes. The superseded v1.0 version DOI is blocked by the CI staleness gate so it cannot
  silently return.
- Wall map (`ATLAS.md`), node ledger (`ledger/`) with the stdlib scorer, atlas-points model
  (`POINTS.md`), contribution rules (`CONTRIBUTING.md` + `DCO.md`), skeptical FAQ, seed issues.
- Qiskit puzzle lab (`qiskit_game/`): exact-witness binding (`f(v*) = W` to machine precision),
  the `play.py` wall room, the executed embedded-wall notebook, and the "ways to play" tooling
  ladder including `PLAY-WITH-AI.md` and a by-hand appendix.
- Ledger nodes anchored to the deposit: `bundle_doi` + `concept_doi` on the M1 proof nodes and
  `certificate_sha256` on the global-wall certificate node. The certificate hash is the
  *decompressed* certificate (`SHA256SUMS` pins the `.gz` at `116f8e63...`); anyone reproduces it
  with `gunzip -c global-wall-certificate-Q-exact.json.gz | sha256sum`, recorded on the node as
  `certificate_recompute`.
- **AIIR receipt workflow.** `ledger/emit_receipts.py` projects every node into an
  `aiir/research_evidence_receipt.v0.1` (content-addressed, Apache-2.0 open format) in
  `.aiir/research-evidence.jsonl`, binding each claim to its artifacts by sha256 (from the
  vendored `bundle.SHA256SUMS`). Status is enforced honestly (self-verified exact -> `proof_sketch`,
  never `verified` without an independent rerun). CI gates it via `emit_receipts.py --check`, and a
  commit-receipt workflow (`.github/workflows/aiir.yml`) attests the repo's own AI-assisted commits.
