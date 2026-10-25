from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import CurrentUser
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut
from app.services.cart_service import (
    CartItemNotFoundError,
    InsufficientStockError,
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_quantity,
)
from app.services.product_service import ProductNotFoundError

router = APIRouter()


@router.get("/cart", response_model=CartOut)
def view_cart(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    items, total = get_cart(db, current_user.id)
    return CartOut(items=items, total=total)


@router.post("/cart/items", response_model=CartOut, status_code=201)
def add_item(
    payload: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        add_to_cart(db, current_user.id, payload.product_id, payload.quantity)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Товар не найден")
    except InsufficientStockError:
        raise HTTPException(status_code=409, detail="Недостаточно товара на складе")

    items, total = get_cart(db, current_user.id)
    return CartOut(items=items, total=total)


@router.patch("/cart/items/{product_id}", response_model=CartOut)
def update_item(
    product_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        update_quantity(db, current_user.id, product_id, payload.quantity)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Товар не найден")
    except CartItemNotFoundError:
        raise HTTPException(status_code=404, detail="Товара нет в корзине")
    except InsufficientStockError:
        raise HTTPException(status_code=409, detail="Недостаточно товара на складе")

    items, total = get_cart(db, current_user.id)
    return CartOut(items=items, total=total)


@router.delete("/cart/items/{product_id}", response_model=CartOut)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        remove_from_cart(db, current_user.id, product_id)
    except CartItemNotFoundError:
        raise HTTPException(status_code=404, detail="Товара нет в корзине")

    items, total = get_cart(db, current_user.id)
    return CartOut(items=items, total=total)
