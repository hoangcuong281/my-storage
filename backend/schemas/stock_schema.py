from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum


class StockOutReason(str, Enum):
    sell = "sell"
    damaged = "damaged"
    expired = "expired"
    adjust = "adjust"


# ---------- STOCK IN ----------
class StockInBase(BaseModel):
    product_id: int
    supplier_id: Optional[int] = None
    quantity: int
    import_price: Optional[float] = None
    import_date: date


class StockInCreate(StockInBase):
    pass


class StockInUpdate(BaseModel):
    quantity: int
    import_price: Optional[float] = None
    import_date: date


class StockInResponse(StockInBase):
    stock_in_id: int

    class Config:
        from_attributes = True


# ---------- STOCK OUT ----------
class StockOutBase(BaseModel):
    product_id: int
    quantity: int
    reason: StockOutReason
    export_date: date


class StockOutCreate(StockOutBase):
    pass


class StockOutUpdate(BaseModel):
    quantity: int
    reason: StockOutReason
    export_date: date


class StockOutResponse(StockOutBase):
    stock_out_id: int

    class Config:
        from_attributes = True
