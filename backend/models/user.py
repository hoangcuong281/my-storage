from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    manager = "manager"


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(
        Enum(UserRole, native_enum=False),
        default=UserRole.staff,
        nullable=False
    )
