from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.core.dependencies import get_current_user


def require_role(*roles: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return role_checker
