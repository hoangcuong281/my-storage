from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    code: str
    name: str
    category_id: Optional[int]
    supplier_id: Optional[int]
    price: float
    location: Optional[str]
    note: Optional[str]

class ProductResponse(ProductCreate):
    product_id: int
    quantity: int
    class Config:
        from_attributes = True
