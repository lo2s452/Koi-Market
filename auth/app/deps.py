from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Role
from app.security import decode_access_token

DB = Annotated[AsyncSession, Depends(get_db)]

_bearer = HTTPBearer()


async def require_admin(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> None:
    try:
        claims = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if claims["role"] != Role.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "admin role required")
