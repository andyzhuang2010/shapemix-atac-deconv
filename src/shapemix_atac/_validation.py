"""Stable feature-axis hashing."""
import hashlib
from typing import Iterable

def ordered_feature_sha256(feature_names: Iterable[str]) -> str:
    """Hash an ordered feature axis using UTF-8 names with 8-byte length prefixes.

    Length prefixes make boundaries unambiguous: axes ``["ab", "c"]`` and
    ``["a", "bc"]`` cannot produce the same byte stream before hashing.
    """
    digest = hashlib.sha256()
    for feature_name in feature_names:
        if not isinstance(feature_name, str):
            raise TypeError("Feature names must be strings when computing feature_sha256.")
        encoded = feature_name.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big", signed=False))
        digest.update(encoded)
    return digest.hexdigest()
