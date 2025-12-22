from pydantic import BaseModel
from typing import Optional

class SupplierCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None

class SupplierResponse(SupplierCreate):
    supplier_id: int

    class Config:
        from_attributes = True
