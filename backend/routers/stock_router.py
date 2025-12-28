from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.stock import StockIn, StockOut
from models.user import Users
from schemas.stock_schema import (
    StockInCreate, StockInUpdate,
    StockOutCreate, StockOutUpdate,
    StockInResponse, StockOutResponse
)
from dependencies.auth import get_current_user

router = APIRouter(prefix="/stock", tags=["Stock"])


# ==================================================
#                   STOCK IN
# ==================================================
@router.get("/stockin", response_model=List[StockInResponse])
def get_all_stock_in(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return db.query(StockIn).order_by(StockIn.import_date.desc()).all()


@router.get("/stockin/{stock_in_id}", response_model=StockInResponse)
def get_stock_in_by_id(
    stock_in_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    record = db.query(StockIn).filter_by(stock_in_id=stock_in_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="StockIn not found")
    return record


@router.post("/stockin", response_model=StockInResponse)
def create_stock_in(
    data: StockInCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    record = StockIn(
        **data.model_dump(),
        user_id=current_user.user_id  # 🔥 GÁN USER ĐANG LOGIN
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/stockin/{stock_in_id}", response_model=StockInResponse)
def update_stock_in(
    stock_in_id: int,
    data: StockInUpdate,
    db: Session = Depends(get_db)
):
    record = db.query(StockIn).filter_by(stock_in_id=stock_in_id).first()
    if not record:
        raise HTTPException(404, "StockIn not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)

    db.commit()
    db.refresh(record)
    return record



@router.delete("/stockin/{stock_in_id}")
def delete_stock_in(
    stock_in_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(StockIn).filter_by(stock_in_id=stock_in_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="StockIn not found")
    
    db.delete(record)
    db.commit()
    return {"message": "Deleted successfully"}


# ==================================================
#                   STOCK OUT
# ==================================================
@router.get("/stockout", response_model=List[StockOutResponse])
def get_all_stock_out(
    db: Session = Depends(get_db)
):
    return db.query(StockOut).order_by(StockOut.export_date.desc()).all()


@router.get("/stockout/{stock_out_id}", response_model=StockOutResponse)
def get_stock_out_by_id(
    stock_out_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(StockOut).filter_by(stock_out_id=stock_out_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="StockOut not found")
    return record


@router.post("/stockout", response_model=StockOutResponse)
def create_stock_out(
    data: StockOutCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    record = StockOut(
        **data.model_dump(),
        user_id=current_user.user_id  # 🔥 USER ĐANG LOGIN
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/stockout/{stock_out_id}", response_model=StockOutResponse)
def update_stock_out(
    stock_out_id: int,
    data: StockOutUpdate,
    db: Session = Depends(get_db)
):
    record = db.query(StockOut).filter_by(stock_out_id=stock_out_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="StockOut not found")
        
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/stockout/{stock_out_id}")
def delete_stock_out(
    stock_out_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(StockOut).filter_by(stock_out_id=stock_out_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="StockOut not found")

    db.delete(record)
    db.commit()
    return {"message": "Deleted successfully"}
