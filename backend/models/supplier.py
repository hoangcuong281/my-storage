from sqlalchemy import Column, Integer, String, Text
from database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    address = Column(Text)
    note = Column(Text)
