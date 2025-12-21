from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.supplier import Supplier
from schemas.supplier_schema import SupplierCreate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/")
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    exists = db.query(Supplier).filter(Supplier.name == data.name).first()
    if exists:
        raise HTTPException(400, "Supplier already exists")

    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.put("/{supplier_id}")
def update_supplier(supplier_id: int, data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")

    for key, value in data.dict().items():
        setattr(supplier, key, value)

    db.commit()
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")

    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted"}
