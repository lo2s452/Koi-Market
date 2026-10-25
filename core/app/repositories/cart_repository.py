import uuid

from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.models.product import Product


def get_cart_item(db: Session, user_id: uuid.UUID, product_id: int) -> CartItem | None:
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )


def get_cart_items_with_products(db: Session, user_id: uuid.UUID) -> list[tuple[CartItem, Product]]:
    return (
        db.query(CartItem, Product)
        .join(Product, CartItem.product_id == Product.id)
        .filter(CartItem.user_id == user_id)
        .all()
    )


def create_cart_item(db: Session, user_id: uuid.UUID, product_id: int, quantity: int) -> CartItem:
    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.flush()
    return cart_item


def update_cart_item_quantity(db: Session, cart_item: CartItem, quantity: int) -> CartItem:
    cart_item.quantity = quantity
    return cart_item


def delete_cart_item(db: Session, cart_item: CartItem) -> bool:
    deleted = db.query(CartItem).filter(CartItem.id == cart_item.id).delete()
    return deleted == 1
