import asyncio
import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from functools import cache
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from app.config import settings
from app.models import Role

_hasher = PasswordHasher()

_DUMMY_HASH = _hasher.hash(secrets.token_urlsafe(16))


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(_hasher.hash, password)


async def verify_password(password_hash: str | None, password: str) -> bool:
    try:
        ok = await asyncio.to_thread(_hasher.verify, password_hash or _DUMMY_HASH, password)
    except VerifyMismatchError:
        return False
    return ok and password_hash is not None


@cache
def private_key() -> Ed25519PrivateKey:
    key = load_pem_private_key(settings.private_key_path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError(f"{settings.private_key_path} is not an Ed25519 private key")
    return key


def create_access_token(user_id: uuid.UUID, username: str, role: Role) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role.value,
        "exp": datetime.now(UTC) + timedelta(seconds=settings.access_ttl_seconds),
    }
    return jwt.encode(payload, private_key(), algorithm="EdDSA")


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        private_key().public_key(),
        algorithms=["EdDSA"],
        options={"require": ["exp", "sub", "role"]},
    )


def new_refresh_family() -> str:
    return secrets.token_urlsafe(16)


def new_refresh_token(family: str) -> str:
    return f"{family}.{secrets.token_urlsafe(32)}"


def refresh_token_family(token: str) -> str | None:
    family, sep, secret = token.partition(".")
    if not (family and sep and secret):
        return None
    return family


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
