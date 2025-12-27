from fastapi import Depends, HTTPException, status
from dependencies.auth import get_current_user
from models.user import Users

def admin_required(
    current_user: Users = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin được phép"
        )
    return current_user
