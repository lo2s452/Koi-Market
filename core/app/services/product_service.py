from sqlalchemy.orm import Session

from app.repositories.product_repository import (
    create_product,
    get_product_by_id,
    list_products,
)
from app.schemas.product import ProductCreate


class ProductNotFoundError(Exception):
    pass


def add_product(db: Session, product: ProductCreate):
    created = create_product(
        db=db,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
    )
    db.commit()
    return created


def get_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise ProductNotFoundError()

    return product


def get_products(db: Session, skip: int = 0, limit: int = 20, q: str | None = None):
    return list_products(db, skip=skip, limit=limit, q=q)
