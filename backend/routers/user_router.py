from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models.user import Users, UserRole
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from dependencies.permission import admin_required

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    _: Users = Depends(admin_required)
):
    return db.query(Users).all()

@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _: Users = Depends(admin_required)
):
    if db.query(Users).filter(Users.username == data.username).first():
        raise HTTPException(400, "Username đã tồn tại")

    user = Users(
        username=data.username,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=UserRole(data.role)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _: Users = Depends(admin_required)
):
    user = db.query(Users).get(user_id)
    if not user:
        raise HTTPException(404, "User không tồn tại")

    if data.full_name:
        user.full_name = data.full_name
    if data.role:
        user.role = UserRole(data.role)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: Users = Depends(admin_required)
):
    user = db.query(Users).get(user_id)
    if not user:
        raise HTTPException(404, "User không tồn tại")

    db.delete(user)
    db.commit()
    return {"message": "Đã xoá user"}
