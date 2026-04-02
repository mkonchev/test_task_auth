from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.user_service import UserService
from app.services.permission_service import PermissionService, Action
from app.security.auth_handler import AuthHandler
from app.models.user import User


security = HTTPBearer()


async def get_current_user(
    creditials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = creditials.credentials
    payload = await AuthHandler.decode_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid creditials"
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No such user"
        )

    return user


def require_permission(
    element_name: str,
    action: Action,
    resource_owner_id: int | None = None
):
    async def dependency(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        permission_service = PermissionService(db)

        owner_id = resource_owner_id
        if callable(resource_owner_id):
            owner_id = await resource_owner_id(current_user, db)

        has_permission = await permission_service.check_permission(
            current_user,
            element_name,
            action,
            owner_id
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions to {action} {element_name}"
            )

        return current_user

    return dependency
