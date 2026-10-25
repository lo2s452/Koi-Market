import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OrderStatus:
    PENDING = "pending"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)

    status: Mapped[str] = mapped_column(default=OrderStatus.PENDING)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product_name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    quantity: Mapped[int]
