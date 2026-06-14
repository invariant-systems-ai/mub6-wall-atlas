#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""Check that every local link in the Markdown points at a file that exists.

A docs-heavy public repo rots first at its internal links: a renamed file, a moved
example, a typo'd path. This stdlib checker walks every tracked Markdown file, resolves
each local `[text](target)` and `![alt](target)` link relative to the file, and fails if
the target is missing. External links (http/https/mailto) and pure `#anchors` are left
alone; that is a different, network-flaky job best left to a human or a scheduled run.

Usage:  python3 ci/check_links.py   (exit 0 = every local link resolves)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")          # [text](target) and ![alt](target)
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")
SKIP_DIRS = {".git", "build", "__pycache__", ".lake", ".ipynb_checkpoints", "lake-packages"}


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def targets(text):
    for m in LINK.finditer(text):
        raw = m.group(1).strip()
        # strip a markdown title:  (path "the title")
        raw = raw.split(" ", 1)[0].strip("<>")
        if not raw or raw.startswith(SKIP_PREFIXES):
            continue
        yield raw


def main():
    broken = []
    for md in md_files():
        base = md.parent
        for raw in targets(md.read_text(errors="replace")):
            path = raw.split("#", 1)[0]            # drop any #anchor
            if not path:
                continue                            # was a pure anchor
            if not (base / path).exists():
                broken.append((md.relative_to(ROOT), raw))
    if broken:
        print("BROKEN LOCAL LINKS:")
        for src, raw in broken:
            print(f"  - {src}: -> {raw}")
        print(f"\n{len(broken)} broken link(s).")
        return 1
    print(f"OK: all local Markdown links resolve ({sum(1 for _ in md_files())} files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
