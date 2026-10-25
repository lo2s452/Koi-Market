from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.error_messages import validation_exception_handler
from app.routers.cart import router as cart_router
from app.routers.me import router as me_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.security import public_key

public_key()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(me_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
