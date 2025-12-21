from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from schemas.product_schema import ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.put("/{product_id}")
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    for k, v in data.dict().items():
        setattr(product, k, v)

    db.commit()
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Deleted"}
