from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    price: Decimal
    quantity: int


class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
