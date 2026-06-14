# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Noah Erlwein (Invariant Systems)
"""mub6_game: the MUB(6) Wall Atlas puzzle lab (Mode B, teaching/search)."""
from .feasibility import (
    canonical_triple,
    canonical_like_triple,
    canonical_witness,
    feasibility,
    score,
    embed_c6_in_3q,
    project_3q_to_c6,
    W_EXACT,
    D,
    K,
)

__all__ = [
    "canonical_triple", "canonical_like_triple", "canonical_witness",
    "feasibility", "score", "embed_c6_in_3q", "project_3q_to_c6",
    "W_EXACT", "D", "K",
]
