import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import ColumnElement, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.deps import DB, require_admin
from app.models import Role, User, UserSession
from app.schemas import AccessToken, Credentials, UserOut
from app.security import (
    create_access_token,
    hash_password,
    hash_refresh_token,
    new_refresh_family,
    new_refresh_token,
    refresh_token_family,
    verify_password,
)

router = APIRouter(prefix="/auth")

REFRESH_COOKIE = "refresh_token"
RefreshCookie = Annotated[str | None, Cookie(alias=REFRESH_COOKIE)]

_cookie_params = {
    "path": "/auth",
    "httponly": True,
    "secure": settings.cookie_secure,
    "samesite": "strict",
}


def _issue_tokens(
    response: Response,
    user_id: uuid.UUID,
    username: str,
    role: Role,
    refresh_token: str,
) -> AccessToken:
    response.set_cookie(
        REFRESH_COOKIE, refresh_token, max_age=settings.refresh_ttl_seconds, **_cookie_params
    )
    return AccessToken(
        access_token=create_access_token(user_id, username, role),
        expires_in=settings.access_ttl_seconds,
    )


async def _end_session(db: AsyncSession, where: ColumnElement[bool]) -> None:
    await db.execute(delete(UserSession).where(where))


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(body: Credentials, db: DB) -> User:
    user = User(username=body.username, password_hash=await hash_password(body.password))
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "username already taken")
    return user


@router.post("/login")
async def login(body: Credentials, response: Response, db: DB) -> AccessToken:
    user = await db.scalar(select(User).where(User.username == body.username))
    password_ok = await verify_password(user.password_hash if user else None, body.password)
    if user is None or not password_ok:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid username or password")

    await _end_session(db, UserSession.user_id == user.id)

    family = new_refresh_family()
    refresh_token = new_refresh_token(family)
    now = datetime.now(UTC)
    db.add(
        UserSession(
            user_id=user.id,
            family_hash=hash_refresh_token(family),
            refresh_hash=hash_refresh_token(refresh_token),
            refresh_expires_at=now + timedelta(seconds=settings.refresh_ttl_seconds),
            created_at=now,
        )
    )
    await db.commit()
    return _issue_tokens(response, user.id, user.username, user.role, refresh_token)


@router.post("/refresh")
async def refresh(response: Response, db: DB, refresh_token: RefreshCookie = None) -> AccessToken:
    if refresh_token is None or (family := refresh_token_family(refresh_token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid refresh token")

    presented_hash = hash_refresh_token(refresh_token)
    new_token = new_refresh_token(family)
    now = datetime.now(UTC)
    session = (
        await db.execute(
            update(UserSession)
            .where(
                UserSession.refresh_hash == presented_hash,
                UserSession.refresh_expires_at > now,
                UserSession.created_at > now - timedelta(seconds=settings.session_max_age_seconds),
            )
            .values(
                refresh_hash=hash_refresh_token(new_token),
                refresh_expires_at=now + timedelta(seconds=settings.refresh_ttl_seconds),
            )
            .returning(UserSession.user_id)
        )
    ).one_or_none()
    if session is None:
        owner = (
            await db.execute(
                select(UserSession.id, UserSession.refresh_hash).where(
                    UserSession.family_hash == hash_refresh_token(family)
                )
            )
        ).one_or_none()
        if owner is not None and owner.refresh_hash != presented_hash:
            await _end_session(db, UserSession.id == owner.id)
            await db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid refresh token")

    user = (
        await db.execute(select(User.username, User.role).where(User.id == session.user_id))
    ).one()
    await db.commit()
    return _issue_tokens(response, session.user_id, user.username, user.role, new_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, db: DB, refresh_token: RefreshCookie = None) -> None:
    if refresh_token is not None and (family := refresh_token_family(refresh_token)) is not None:
        await _end_session(db, UserSession.family_hash == hash_refresh_token(family))
        await db.commit()
    response.delete_cookie(REFRESH_COOKIE, **_cookie_params)


@router.post(
    "/admin/users/{username}/revoke",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
async def revoke_user_session(username: str, db: DB) -> None:
    user_id = await db.scalar(select(User.id).where(User.username == username))
    if user_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    await _end_session(db, UserSession.user_id == user_id)
    await db.commit()
