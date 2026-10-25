from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.security import decode_access_token

_bearer = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def require_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> None:
    if credentials is None:
        raise _unauthorized()
    try:
        decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise _unauthorized()
