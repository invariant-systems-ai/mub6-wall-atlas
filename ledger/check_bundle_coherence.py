#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Bind every ledger claim to a hash-pinned bundle artifact, without the network.

The Zenodo verification bundle is large and lives off-repo, but its hash manifest
(`ledger/bundle.SHA256SUMS`) is vendored here. This check enforces that the ledger and
that manifest stay coherent:

  1. Every `artifact` path a node points at is pinned in the manifest (or exists locally
     in the atlas, for atlas-native artifacts), so no claim can point at a file that is
     not under hash control.
  2. The decompressed-certificate node names the exact `.gz` pin the manifest records, so
     the documented recompute path (`gunzip -c ... | sha256sum`) is anchored to a real,
     pinned artifact rather than a free-floating hash.

It does not download the bundle or recompute the 441x441 certificate; that is the
deliberately heavier `make verify-global` in the bundle itself. This is the cheap,
offline coherence gate that runs on every push and in the monthly freshness sweep.

Usage:  python3 ledger/check_bundle_coherence.py   (exit 0 = ledger <-> manifest coherent)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NODES = HERE / "nodes.json"
MANIFEST = HERE / "bundle.SHA256SUMS"

# The .gz the certificate node documents as the source of its decompressed hash.
GZ_ARTIFACT = "evidence/global-wall-certificate-Q-exact.json.gz"


def manifest_map():
    out = {}
    for line in MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        sha, _, path = line.partition("  ")
        out[path.strip()] = sha.strip()
    return out


def main():
    errs = []
    pinned = manifest_map()
    nodes = json.loads(NODES.read_text())["nodes"]

    # 1. Every node artifact is hash-pinned (or atlas-local).
    for n in nodes:
        for a in n.get("artifact", []):
            if a not in pinned and not (ROOT / a).exists():
                errs.append(f"{n['id']}: artifact {a!r} is neither pinned in bundle.SHA256SUMS "
                            f"nor present locally")

    # 2. The certificate node's documented .gz pin matches the manifest.
    gz_pin = pinned.get(GZ_ARTIFACT)
    if gz_pin is None:
        errs.append(f"manifest is missing the certificate artifact {GZ_ARTIFACT!r}")
    else:
        cert_nodes = [n for n in nodes if n.get("certificate_sha256_of")]
        for n in cert_nodes:
            doc = n["certificate_sha256_of"]
            if gz_pin not in doc:
                errs.append(f"{n['id']}: certificate_sha256_of does not name the manifest .gz "
                            f"pin {gz_pin} for {GZ_ARTIFACT}")

    if errs:
        print("LEDGER <-> BUNDLE INCOHERENCE:")
        for e in errs:
            print("  -", e)
        return 1
    print(f"OK: every ledger artifact is hash-pinned or local, and the certificate .gz pin "
          f"matches the manifest ({len(nodes)} nodes, {len(pinned)} pinned artifacts).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
