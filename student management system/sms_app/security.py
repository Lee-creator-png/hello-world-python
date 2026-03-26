from __future__ import annotations

import hashlib
import hmac
import os


def hash_password(password: str, *, salt: bytes | None = None, rounds: int = 200_000) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    pw = password.encode("utf-8")
    digest = hashlib.pbkdf2_hmac("sha256", pw, salt, rounds)
    return salt, digest


def verify_password(password: str, salt: bytes, password_hash: bytes) -> bool:
    _, digest = hash_password(password, salt=salt)
    return hmac.compare_digest(digest, password_hash)

