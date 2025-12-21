from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
import enum


class StockOutReason(enum.Enum):
    sell = "sell"
    damaged = "damaged"
    expired = "expired"
    adjust = "adjust"


class StockIn(Base):
    __tablename__ = "stock_in"

    stock_in_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    import_price = Column(DECIMAL(12, 2))
    import_date = Column(Date, nullable=False)


class StockOut(Base):
    __tablename__ = "stock_out"

    stock_out_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(Enum(StockOutReason), nullable=False)
    export_date = Column(Date, nullable=False)
