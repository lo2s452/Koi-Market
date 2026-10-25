import uuid

from sqlalchemy.orm import Session

from app.repositories.cart_repository import delete_cart_item, get_cart_items_with_products
from app.repositories.order_repository import (
    add_order_item,
    create_order,
    get_order_by_id,
    get_order_items,
    list_all_orders,
    list_orders_for_user,
    mark_order_completed,
)
from app.repositories.product_repository import decrement_stock


class EmptyCartError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class OrderNotFoundError(Exception):
    pass


def checkout(db: Session, user_id: uuid.UUID):
    cart_rows = get_cart_items_with_products(db, user_id)
    if not cart_rows:
        raise EmptyCartError()

    order = create_order(db, user_id=user_id)

    for cart_item, product in cart_rows:
        quantity = cart_item.quantity
        if not delete_cart_item(db, cart_item):
            db.rollback()
            raise EmptyCartError()
        if not decrement_stock(db, product.id, quantity):
            db.rollback()
            raise InsufficientStockError()
        add_order_item(
            db,
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
        )

    db.commit()
    return order, get_order_items(db, order.id)


def get_order_for_user(db: Session, user_id: uuid.UUID, order_id: int):
    order = get_order_by_id(db, order_id)
    if order is None or order.user_id != user_id:
        raise OrderNotFoundError()

    return order, get_order_items(db, order_id)


def get_user_orders(db: Session, user_id: uuid.UUID):
    return list_orders_for_user(db, user_id)


def get_all_orders(db: Session):
    return list_all_orders(db)


def list_order_items(db: Session, order_id: int):
    return get_order_items(db, order_id)


def complete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order is None:
        raise OrderNotFoundError()

    mark_order_completed(db, order)
    db.commit()
    return order
