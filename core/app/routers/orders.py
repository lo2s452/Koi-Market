from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin_user, get_current_user
from app.schemas.user import CurrentUser
from app.schemas.order import OrderOut
from app.services.order_service import (
    EmptyCartError,
    InsufficientStockError,
    OrderNotFoundError,
    checkout,
    complete_order,
    get_all_orders,
    get_order_for_user,
    get_user_orders,
    list_order_items,
)

router = APIRouter()


def _to_order_out(order, items) -> OrderOut:
    return OrderOut(id=order.id, status=order.status, created_at=order.created_at, items=items)


@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order_endpoint(
    db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)
):
    try:
        order, items = checkout(db, current_user.id)
    except EmptyCartError:
        raise HTTPException(status_code=400, detail="Корзина пуста")
    except InsufficientStockError:
        raise HTTPException(status_code=409, detail="Недостаточно товара на складе для одного или нескольких товаров")

    return _to_order_out(order, items)


@router.get("/orders", response_model=list[OrderOut])
def list_my_orders(
    db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)
):
    orders = get_user_orders(db, current_user.id)
    return [_to_order_out(order, list_order_items(db, order.id)) for order in orders]


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_my_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        order, items = get_order_for_user(db, current_user.id, order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return _to_order_out(order, items)


@router.get("/admin/orders", response_model=list[OrderOut])
def list_all_orders_endpoint(
    db: Session = Depends(get_db), admin: CurrentUser = Depends(get_current_admin_user)
):
    orders = get_all_orders(db)
    return [_to_order_out(order, list_order_items(db, order.id)) for order in orders]


@router.patch("/admin/orders/{order_id}/complete", response_model=OrderOut)
def complete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    admin: CurrentUser = Depends(get_current_admin_user),
):
    try:
        order = complete_order(db, order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    items = list_order_items(db, order.id)
    return _to_order_out(order, items)
