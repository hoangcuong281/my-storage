from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, DateTime
from database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    price = Column(DECIMAL(12,2))
    quantity = Column(Integer, default=0)
    location = Column(String(100))
    note = Column(Text)
