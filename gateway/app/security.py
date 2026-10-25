from functools import cache
from typing import Any

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from app.config import settings


@cache
def public_key() -> Ed25519PublicKey:
    key = load_pem_public_key(settings.public_key_path.read_bytes())
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError(f"{settings.public_key_path} is not an Ed25519 public key")
    return key


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        public_key(),
        algorithms=["EdDSA"],
        options={"require": ["exp", "sub", "role"]},
    )
