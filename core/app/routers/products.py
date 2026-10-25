from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin_user
from app.schemas.user import CurrentUser
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import (
    ProductNotFoundError,
    add_product,
    get_product,
    get_products,
)

router = APIRouter()


@router.post("/admin/products", response_model=ProductOut, status_code=201)
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin: CurrentUser = Depends(get_current_admin_user),
):
    return add_product(db, product)


@router.get("/products", response_model=list[ProductOut])
def list_products_endpoint(
    skip: int = 0, limit: int = 20, q: str | None = None, db: Session = Depends(get_db)
):
    return get_products(db, skip=skip, limit=limit, q=q)


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    try:
        return get_product(db, product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Товар не найден")
