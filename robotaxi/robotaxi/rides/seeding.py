"""Deterministic random streams.

A run is reproducible if every random draw comes from a numpy Generator derived from
(run seed, component name, query). Python's built-in ``hash`` is salted per process, so
names are hashed with SHA-256 instead.
"""
from __future__ import annotations

import hashlib

import numpy as np


def _words(text: str) -> list[int]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [int.from_bytes(digest[i:i + 4], "little") for i in range(0, 16, 4)]


def rng_for(seed: int, *labels: str) -> np.random.Generator:
    """Independent stream for this seed and these labels (e.g. generator name, query key)."""
    entropy = [int(seed) & 0xFFFFFFFF]
    for label in labels:
        entropy.extend(_words(label))
    return np.random.default_rng(np.random.SeedSequence(entropy))
