import os
from typing import Any

from argon2 import PasswordHasher

from .config import DEFAULT_ADMIN_PASSWORD

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    if not password or not str(password).strip():
        raise ValueError("كلمة المرور لا يمكن أن تكون فارغة.")
    return _hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return _hasher.verify(hashed_password, password)
    except Exception:
        return False


def default_admin_password() -> str:
    return DEFAULT_ADMIN_PASSWORD
