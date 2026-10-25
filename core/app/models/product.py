from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    description: Mapped[str]

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    stock: Mapped[int] = mapped_column(default=0)

    image_url: Mapped[str | None] = mapped_column(default=None)
