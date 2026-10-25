from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import engine, init_db
from app.routes import router
from app.security import private_key


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    private_key()
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title="auth", lifespan=lifespan)
app.include_router(router)
