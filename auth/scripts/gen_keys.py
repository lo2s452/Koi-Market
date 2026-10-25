import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

out = Path(sys.argv[1] if len(sys.argv) > 1 else "keys")
out.mkdir(parents=True, exist_ok=True)

key = Ed25519PrivateKey.generate()

fd = os.open(out / "private.pem", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "wb") as f:
    f.write(key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))

(out / "public.pem").write_bytes(
    key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
)
print(f"keys written to {out}/")
