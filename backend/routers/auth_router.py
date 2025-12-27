from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models.user import Users
from schemas.user_schema import UserLogin, UserResponse
from dependencies.auth import get_current_user

# ================= ROUTER =================
router = APIRouter(prefix="/auth", tags=["Auth"])

# ================= SECURITY =================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user_by_username(db: Session, username: str) -> Users | None:
    return db.query(Users).filter(Users.username == username).first()

# ================= API =================
@router.post("/login")
def login(
    request: Request,
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, data.username)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password"
        )

    # ===== LƯU SESSION =====
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role.value  # ⚠️ ENUM → string

    return {
        "message": "Đăng nhập thành công",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value
        }
    }


@router.get("/me", response_model=UserResponse)
def me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Đã đăng xuất"}
