import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus


def create_order(db: Session, user_id: uuid.UUID) -> Order:
    order = Order(user_id=user_id, status=OrderStatus.PENDING)
    db.add(order)
    db.flush()
    return order


def add_order_item(
    db: Session,
    order_id: int,
    product_id: int,
    product_name: str,
    price: Decimal,
    quantity: int,
) -> OrderItem:
    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        product_name=product_name,
        price=price,
        quantity=quantity,
    )
    db.add(item)
    db.flush()
    return item


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_items(db: Session, order_id: int) -> list[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def list_orders_for_user(db: Session, user_id: uuid.UUID) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()


def list_all_orders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).all()


def mark_order_completed(db: Session, order: Order) -> Order:
    order.status = OrderStatus.COMPLETED
    return order
