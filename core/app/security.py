from functools import cache
from typing import Any

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from app.config import settings


@cache
def public_key() -> Ed25519PublicKey:
    key = load_pem_public_key(settings.PUBLIC_KEY_PATH.read_bytes())
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError(f"{settings.PUBLIC_KEY_PATH} is not an Ed25519 public key")
    return key


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        public_key(),
        algorithms=["EdDSA"],
        options={"require": ["exp", "sub", "username", "role"]},
    )
