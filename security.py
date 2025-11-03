"""Simple reversible encryption (XOR + Base64)."""

import base64
from itertools import cycle

_SECRET = "CheckMyGradeKey"

def _xor_bytes(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes([b ^ k for b, k in zip(data, cycle(key_bytes))])

def encrypt_password(plain: str) -> str:
    raw = plain.encode("utf-8")
    xored = _xor_bytes(raw, _SECRET)
    return base64.urlsafe_b64encode(xored).decode("ascii")

def decrypt_password(token: str) -> str:
    data = base64.urlsafe_b64decode(token.encode("ascii"))
    raw = _xor_bytes(data, _SECRET)
    return raw.decode("utf-8")



