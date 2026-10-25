from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(
    db: Session,
    name: str,
    description: str,
    price: Decimal,
    stock: int,
    image_url: str | None = None,
) -> Product:
    product = Product(
        name=name, description=description, price=price, stock=stock, image_url=image_url
    )
    db.add(product)
    db.flush()
    return product


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def list_products(db: Session, skip: int = 0, limit: int = 20, q: str | None = None) -> list[Product]:
    query = db.query(Product)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(pattern), Product.description.ilike(pattern)))
    return query.offset(skip).limit(limit).all()


def decrement_stock(db: Session, product_id: int, quantity: int) -> bool:
    updated = (
        db.query(Product)
        .filter(Product.id == product_id, Product.stock >= quantity)
        .update({Product.stock: Product.stock - quantity})
    )
    return updated == 1
