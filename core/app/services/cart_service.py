import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.cart_repository import (
    create_cart_item,
    delete_cart_item,
    get_cart_item,
    get_cart_items_with_products,
    update_cart_item_quantity,
)
from app.services.product_service import get_product


class InsufficientStockError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


def add_to_cart(db: Session, user_id: uuid.UUID, product_id: int, quantity: int):
    product = get_product(db, product_id)

    existing = get_cart_item(db, user_id, product_id)
    new_quantity = quantity + (existing.quantity if existing is not None else 0)

    if new_quantity > product.stock:
        raise InsufficientStockError()

    if existing is not None:
        cart_item = update_cart_item_quantity(db, existing, new_quantity)
    else:
        cart_item = create_cart_item(db, user_id=user_id, product_id=product_id, quantity=new_quantity)

    db.commit()
    return cart_item


def update_quantity(db: Session, user_id: uuid.UUID, product_id: int, quantity: int):
    product = get_product(db, product_id)

    cart_item = get_cart_item(db, user_id, product_id)
    if cart_item is None:
        raise CartItemNotFoundError()

    if quantity > product.stock:
        raise InsufficientStockError()

    update_cart_item_quantity(db, cart_item, quantity)
    db.commit()
    return cart_item


def remove_from_cart(db: Session, user_id: uuid.UUID, product_id: int) -> None:
    cart_item = get_cart_item(db, user_id, product_id)
    if cart_item is None:
        raise CartItemNotFoundError()

    delete_cart_item(db, cart_item)
    db.commit()


def get_cart(db: Session, user_id: uuid.UUID):
    rows = get_cart_items_with_products(db, user_id)

    items = [
        {
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart_item.quantity,
            "subtotal": product.price * cart_item.quantity,
        }
        for cart_item, product in rows
    ]

    total = sum((item["subtotal"] for item in items), Decimal("0"))

    return items, total
