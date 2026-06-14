#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Project the atlas ledger into AIIR research-evidence receipts (dogfood).

Each ledger node becomes an `aiir/research_evidence_receipt.v0.1` record: a
content-addressed, tamper-evident binding of one claim to its artifacts (with
sha256 digests from the bundle manifest), its verifier, its governance, and its
honest status. This is the byte-binding the ledger was missing, expressed in
Invariant's own open receipt grammar (AIIR, Apache-2.0).

Standard-library only. The canonicalization (`aiir-canon-0`) is the AIIR research
-evidence conformance rule. On every run we recompute the content hash of the
conformance vectors in `ledger/aiir_research_evidence_vectors.v0.1.json` and require an
exact match, which keeps our content addressing self-consistent under that rule. Be
precise about what this is and is not: those vectors are OUR drafts for the AIIR profile
(`generated_by: manual-draft`), not third-party-published values, so the check is
intra-ecosystem self-consistency, NOT external validation. It does not run the `aiir`
CLI (whose `--verify` targets commit receipts). The receipts are tamper-evident, not
independently verified.

    python3 ledger/emit_receipts.py            # (re)generate .aiir/research-evidence.jsonl
    python3 ledger/emit_receipts.py --check    # CI gate: receipts match the ledger, untampered
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS = HERE.parent
NODES = HERE / "nodes.json"
SUMS = HERE / "bundle.SHA256SUMS"
OUT = ATLAS / ".aiir" / "research-evidence.jsonl"

REPO = "invariant-systems-ai/mub6-wall-atlas"
PROGRAM_ID = "mub6-wall-atlas"
RELEASE_TS = "2026-06-13T00:00:00Z"   # fixed for deterministic content hashes
RELEASE_DATE = "2026-06-13"
CONTRACT = "aiir/research_evidence_receipt.v0.1"

# Our draft conformance vectors for the AIIR research-evidence profile
# (generated_by: manual-draft). Each carries an input_core and an expected
# content_hash/record_id; if our canonicalization fails to reproduce them, we refuse to
# emit. This is self-consistency under aiir-canon-0, not third-party validation.
VECTORS = HERE / "aiir_research_evidence_vectors.v0.1.json"


def canon(obj) -> str:
    """aiir-canon-0: sorted keys, no whitespace, ASCII-safe, no NaN/Infinity."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def content_hash_and_id(core: dict):
    h = hashlib.sha256(canon(core).encode("utf-8")).hexdigest()
    return "sha256:" + h, "r1-" + h[:32]


def load_digests() -> dict:
    digests = {}
    for line in SUMS.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        h, _, path = line.partition("  ")
        digests[path.lstrip("./")] = "sha256:" + h
    return digests


STATUS_MAP = {
    ("open", None): "hypothesis",
    ("refuted", None): "retracted",
    ("verified", None): "verified",
}


def claim_status(node: dict) -> str:
    """Map to AIIR's fixed research-evidence enum (the schema requires one of these)."""
    st, ev = node["status"], node["evidence_level"]
    if st == "open":
        return "hypothesis"
    if st == "refuted":
        return "retracted"
    if st == "verified":
        return "verified"          # >=1 independent rerun
    if st in ("self-verified", "partial"):
        # exact/kernel proof exists but not independently checked -> proof_sketch;
        # numerical-only -> computational_evidence. Never "verified" without a rerun.
        return "proof_sketch" if ev in ("exact", "kernel") else "computational_evidence"
    return "hypothesis"


def atlas_status(node: dict) -> str:
    """A finer status than AIIR's v0.1 enum allows, carried in extensions so it does not
    break conformance. `proof_sketch` in claim.status reads as 'informal' to a mathematician;
    this says what is actually meant. (A candidate for an AIIR research-evidence v0.2 enum.)"""
    st, ev = node["status"], node["evidence_level"]
    if st == "open":
        return "hypothesis"
    if st == "refuted":
        return "retracted"
    if st == "verified":
        return "independently_reproduced"
    if st in ("self-verified", "partial"):
        if ev == "kernel":
            return "kernel_checked"
        if ev == "exact":
            return "self_verified_exact"   # exact certificate exists, no external rerun yet
        return "computational_evidence"
    return "hypothesis"


def artifact_entry(ref: str, digests: dict, role: str):
    key = ref.lstrip("./")
    if key not in digests:
        return None
    return {"type": "directory" if key.endswith("/") else "file",
            "ref": key, "digest": digests[key], "role": role}


def verifier_refs(node: dict, digests: dict):
    v = node.get("verifier", "none")
    cands = []
    if "verify-global" in v:
        cands.append("verify_global_certificate.py")
    for tok in v.replace("&&", " ").split():
        if tok.endswith(".py"):
            cands.append(tok)
    if "lake build" in v:
        cands.append("lean/lakefile.lean")
    out = []
    for ref in cands:
        e = artifact_entry(ref, digests, "verifier")
        if e:
            out.append(e)
    if not out and v != "none":
        # fall back to the node's own first resolvable artifact as the verifier
        for a in node.get("artifact", []):
            e = artifact_entry(a, digests, "verifier")
            if e:
                out.append(e)
                break
    return out


def build_receipt(node: dict, digests: dict) -> dict:
    arts = [a for a in (artifact_entry(p, digests, "evidence") for p in node.get("artifact", [])) if a]
    core = {
        "contract_version": CONTRACT,
        "timestamp": RELEASE_TS,
        "subject": {"kind": "research_claim", "repo": REPO, "program_id": PROGRAM_ID,
                    "claim_id": node["id"], "title": node["title"]},
        "claim": {"status": claim_status(node), "summary": node["claim"],
                  "non_claims": [node["known_weaknesses"]], "last_reviewed": RELEASE_DATE},
        "evidence": {"artifacts": arts, "verifiers": verifier_refs(node, digests)},
        "governance": {"public_safe": True, "ip_sensitive": False, "disclosure_tier": "public",
                       "next_gate": node["known_weaknesses"]},
        "proof": {"canonicalization": "aiir-canon-0"},
    }
    chash, rid = content_hash_and_id(core)
    receipt = dict(core)
    receipt["record_id"] = rid
    receipt["proof"] = {"canonicalization": "aiir-canon-0", "content_hash": chash}
    ext = {k: node[k] for k in ("concept_doi", "bundle_doi", "certificate_sha256",
                                "certificate_sha256_of", "certificate_recompute") if node.get(k)}
    ext["atlas_status"] = atlas_status(node)   # the finer label; claim.status is the coarse AIIR enum
    receipt["extensions"] = ext
    return receipt


def core_of(receipt: dict) -> dict:
    """Reconstruct the hashed core from a finished receipt (drop derived fields)."""
    core = {k: v for k, v in receipt.items() if k not in ("record_id", "extensions", "proof")}
    core["proof"] = {"canonicalization": receipt["proof"]["canonicalization"]}
    return core


_SHA = re.compile(r"^sha256:[0-9a-f]{64}$")
_RID = re.compile(r"^r1-[0-9a-f]{32}$")
_STATUS = {"hypothesis", "computational_evidence", "proof_sketch", "verified",
           "published", "disputed", "retracted"}
_TIER = {"public", "internal", "restricted", "embargoed"}


def structural_errors(r: dict):
    """Light structural check against aiir/research_evidence_receipt.v0.1 (stdlib)."""
    errs = []
    if r.get("contract_version") != CONTRACT:
        errs.append("bad contract_version")
    if not _RID.match(r.get("record_id", "")):
        errs.append("bad record_id format")
    if r.get("claim", {}).get("status") not in _STATUS:
        errs.append(f"bad claim.status {r.get('claim', {}).get('status')!r}")
    if r.get("governance", {}).get("disclosure_tier") not in _TIER:
        errs.append("bad disclosure_tier")
    for grp in ("artifacts", "verifiers"):
        for a in r.get("evidence", {}).get(grp, []):
            if not _SHA.match(a.get("digest", "")):
                errs.append(f"bad digest in evidence.{grp}: {a.get('ref')}")
    return errs


def conformance_ok():
    """Recompute the content hash of every recorded conformance vector; require exact
    match (self-consistency under aiir-canon-0). Returns (all_ok, n_checked)."""
    data = json.loads(VECTORS.read_text())
    n = 0
    for v in data["vectors"]:
        h, rid = content_hash_and_id(v["input_core"])
        exp = v["expected"]
        if h != exp["content_hash"] or rid != exp["record_id"]:
            return False, n
        n += 1
    return True, n


def generate(digests: dict) -> str:
    nodes = json.loads(NODES.read_text())["nodes"]
    lines = [json.dumps(build_receipt(n, digests), separators=(",", ":")) for n in nodes]
    return "\n".join(lines) + "\n"


def main(argv):
    ok, nvec = conformance_ok()
    if not ok:
        print("FAIL: canonicalization does not reproduce the recorded conformance vectors.")
        return 1
    digests = load_digests()
    fresh = generate(digests)

    if "--check" in argv:
        if not OUT.exists():
            print(f"FAIL: {OUT.relative_to(ATLAS)} missing; run emit_receipts.py.")
            return 1
        committed = OUT.read_text()
        if committed != fresh:
            print("FAIL: receipts are out of date with the ledger. Run emit_receipts.py.")
            return 1
        bad = 0
        for line in committed.splitlines():
            r = json.loads(line)
            for e in structural_errors(r):
                print(f"FAIL: {r.get('subject', {}).get('claim_id', '?')}: {e}")
                bad += 1
            h, rid = content_hash_and_id(core_of(r))
            if h != r["proof"]["content_hash"] or rid != r["record_id"]:
                print(f"FAIL: content hash mismatch on {r['subject']['claim_id']}")
                bad += 1
        if bad:
            return 1
        n = len(committed.splitlines())
        print(f"OK: {n} research-evidence receipts match the ledger; content hashes consistent; "
              f"self-consistent on {nvec} draft conformance vectors (aiir-canon-0). Tamper-evident, not independently verified.")
        return 0

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(fresh)
    n = len(fresh.splitlines())
    print(f"wrote {OUT.relative_to(ATLAS)}  ({n} aiir/research_evidence_receipt.v0.1 records)")
    print(f"self-consistent on {nvec} draft conformance vectors (aiir-canon-0); records content-addressed.")
    print("These are TAMPER-EVIDENT receipts, not independent verification. Verify with:")
    print("  python3 ledger/emit_receipts.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
