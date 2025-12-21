from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.category import Category
from schemas.category_schema import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    exists = db.query(Category).filter(Category.name == data.name).first()
    if exists:
        raise HTTPException(400, "Category already exists")

    category = Category(**data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    category.name = data.name
    category.description = data.description
    db.commit()
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
